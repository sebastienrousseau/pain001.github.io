# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Per-page markup repairs in postbuild_fix.

Pins the string transforms main() chains over every built page: the
entity-escaping repairs for ssg's head and body output, inline code
protection, article furniture (anchors, contents rail, reading time),
table wrapping and labelling, code-block unwrapping, align stripping and
stylesheet relocation. Each must leave unaffected markup byte-identical.
"""

import postbuild_fix as pb


def test_fix_head_unescapes_only_escaped_head_tags():
    assert pb.fix_head("<p>no head</p>") == "<p>no head</p>"
    clean = "<head><title>x</title></head><body>&lt;meta&gt;</body>"
    assert pb.fix_head(clean) == clean
    broken = '<head><title>t</title>&lt;meta name="a" content="b"&gt;</head><body></body>'
    assert pb.fix_head(broken) == '<head><title>t</title><meta name="a" content="b"></head><body></body>'
    linked = "<head>&lt;link rel=icon href=/x.svg&gt;</head>"
    assert pb.fix_head(linked) == "<head><link rel=icon href=/x.svg></head>"


def test_dedupe_head_metas_keeps_the_first_of_each_name():
    assert pb.dedupe_head_metas("<body></body>") == "<body></body>"
    html = (
        '<head><meta name="description" content="authored" />\n'
        '<meta content="synth" name=description>\n'
        '<meta name="viewport" content="a">'
        "<meta content=b name=viewport>"
        '<meta name="theme-color" content="1"><meta name="theme-color" content="2">'
        "</head><body><meta name=description content=body></body>"
    )
    out = pb.dedupe_head_metas(html)
    head = out[: out.find("</head>")]
    assert head.count("description") == 1 and "authored" in head
    assert head.count("viewport") == 1 and 'content="a"' in head
    assert head.count("theme-color") == 2
    assert out.endswith("<body><meta name=description content=body></body>")


def test_fix_body_unescapes_marked_containers_only():
    escaped = "&lt;div lang=&quot;en&quot;&gt;&lt;p&gt;Hi&lt;/p&gt;&lt;/div&gt;"
    html = '<article class="content-body">' + escaped + "</article>"
    assert pb.fix_body(html) == '<article class="content-body"><div lang="en"><p>Hi</p></div></article>'
    unmarked = "<article>&lt;p&gt;keep&lt;/p&gt;</article>"
    assert pb.fix_body(unmarked) == unmarked
    unclosed = "<div class=content-body>" + escaped
    assert pb.fix_body(unclosed) == unclosed


def test_escape_inline_code_protects_element_names_outside_pre():
    html = (
        '<pre><code><span class="k">x</span></code></pre>'
        "<p><code><BIC></code> and <code>plain</code></p>"
    )
    out = pb.escape_inline_code(html)
    assert out.startswith('<pre><code><span class="k">x</span></code></pre>')
    assert "<code>&lt;BIC&gt;</code>" in out
    assert "<code>plain</code>" in out


def test_slugify_falls_back_to_section():
    assert pb._slugify("<em>Hello</em> World!") == "hello-world"
    assert pb._slugify("&amp;") == "section"


def test_article_furniture_adds_anchors_toc_and_reading_time():
    body = "<h2>01. Intro</h2><p>" + "word " * 500 + "</p><h2>Intro</h2><h2>01. Intro</h2>"
    html = (
        '<div class="article-meta"><span>x</span></div>'
        '<article class="post content-body">' + body + "</article>"
    )
    out = pb.add_article_furniture(html)
    assert '<h2 id="01-intro">01. Intro<a class="heading-anchor" href="#01-intro"' in out
    assert 'id="intro"' in out and 'id="01-intro-2"' in out
    assert '<nav class="article-toc" aria-label="Contents" data-local-nav>' in out
    assert '<li><a href="#01-intro">Intro</a></li>' in out
    assert '<div class="article-meta"><span>2 min read</span>' in out
    assert pb.add_article_furniture(out) == out


def test_article_furniture_short_page_has_no_toc():
    html = '<div class=article-meta></div><article class="content-body"><h2>Only</h2></article>'
    out = pb.add_article_furniture(html)
    assert "article-toc" not in out
    assert "<span>1 min read</span>" in out
    assert pb.add_article_furniture("<p>no article</p>") == "<p>no article</p>"


def test_wrap_tables_wraps_bare_tables_inside_main(capsys):
    assert pb.wrap_tables("<table></table>") == "<table></table>"
    html = "<main><p>a</p><table><tr><td>1</td></tr></table></main><table></table>"
    out = pb.wrap_tables(html)
    assert out == (
        '<main><p>a</p><div class="table-responsive"><table><tr><td>1</td></tr></table></div>'
        "</main><table></table>"
    )
    assert pb.wrap_tables(out) == out
    scroll = '<main><div class="ssg-table-scroll" role="region"><table></table></div></main>'
    assert pb.wrap_tables(scroll) == scroll
    nested = "<main><table><tr><td><table></table></td></tr></table></main>"
    assert pb.wrap_tables(nested) == nested
    assert "nested table left unwrapped" in capsys.readouterr().out


def test_stamp_table_labels_by_column_position():
    table = (
        '<table><thead><tr><th>Name</th><th>Say "hi"</th></tr></thead>'
        "<tbody><tr><th>r1</th><td>a</td><td class=x>b</td></tr>"
        "<tr><td>c</td><td>d</td></tr></tbody></table>"
    )
    out = pb.stamp_table_labels(table)
    assert "<th>r1</th>" in out
    assert '<td data-label="Say &quot;hi&quot;">a</td>' in out
    assert "<td class=x>b</td>" in out
    assert '<td data-label="Name">c</td><td data-label="Say &quot;hi&quot;">d</td>' in out
    assert pb.stamp_table_labels(out) == out
    no_head = "<table><tr><td>1</td></tr></table>"
    assert pb.stamp_table_labels(no_head) == no_head
    empty_head = "<table><thead><tr><td>x</td></tr></thead><tr><td>1</td></tr></table>"
    assert pb.stamp_table_labels(empty_head) == empty_head


def test_fix_code_blocks_restores_delimiters_and_unwraps_highlighter():
    escaped = (
        '<pre>&lt;code class="language-xml"&gt;\n<pre style="background:x">'
        "&lt;BIC&gt;</pre>\n&lt;/code&gt;&lt;/pre&gt;"
    )
    assert pb.fix_code_blocks(escaped) == '<pre><code class="language-xml">&lt;BIC&gt;</code></pre>'
    nested = '<pre><code>\n<pre style="a"><span style="c">x</span> y</pre>\n</code></pre>'
    assert pb.fix_code_blocks(nested) == "<pre><code>x y</code></pre>"


def test_restore_encoded_code_keeps_payload_escaped():
    html = "&lt;code class=&quot;k&quot;&gt;&amp;lt;BIC&amp;gt;&lt;/code&gt;"
    assert pb.restore_encoded_code(html) == '<code class="k">&amp;lt;BIC&amp;gt;</code>'


def test_strip_align_attrs():
    html = '<tr align=left><th align="center">a</th><td class="n" align="right">1</td><p align="x">'
    assert pb.strip_align_attrs(html) == '<tr><th>a</th><td class="n">1</td><p align="x">'


def test_relocate_body_stylesheets_moves_links_into_head():
    assert pb.relocate_body_stylesheets("<body></body>") == "<body></body>"
    plain = "<head></head><body><p>x</p></body>"
    assert pb.relocate_body_stylesheets(plain) == plain
    link = '<link rel="stylesheet" href="/s.css" integrity="sha384-x">'
    html = "<head><title>t</title></head><body>" + link + "<p>x</p></body>"
    assert pb.relocate_body_stylesheets(html) == "<head><title>t</title>" + link + "</head><body><p>x</p></body>"
