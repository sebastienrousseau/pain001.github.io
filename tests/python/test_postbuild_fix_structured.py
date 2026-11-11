# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Structured data and generated text in postbuild_fix.

Pins the TechArticle and Dataset JSON-LD blocks, the homepage software
graph, the package-count heading, llms.txt and llms-full.txt, and the
footer suite-version stamp. Every value is read from the built page or
the corpus index, so each test checks that the output follows its input
and that pages already carrying the data are not changed.
"""

import json

import pytest

import postbuild_fix as pb


def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if isinstance(text, str) else json.dumps(text), encoding="utf-8")


def read(path):
    return path.read_text(encoding="utf-8")


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(pb, "__file__", str(tmp_path / "scripts" / "postbuild_fix.py"))
    return tmp_path


def ld_blocks(html):
    return [json.loads(m.group(2)) for m in pb._LD_BLOCK_RE.finditer(html)]


def test_inject_article_ld(tmp_path, capsys):
    head = ('<html lang="fr"><head><title> Qu&#x27;est-ce </title>'
            '<meta name="description" content="A &amp; B">'
            '<link rel="canonical" href="https://pain001.com/fr/pain-001/"></head></html>')
    put(tmp_path / "fr" / "pain-001" / "index.html", head)
    put(tmp_path / "pain-001" / "index.html", "<html><head><title>T</title>"
        '<link rel="canonical" href="https://pain001.com/pain-001/"></head></html>')
    put(tmp_path / "de" / "pain-001" / "index.html", "<head><title>no canonical</title></head>")
    done = '<head>"@type": "TechArticle"</head>'
    put(tmp_path / "es" / "pain-001" / "index.html", done)
    assert pb.inject_article_ld(tmp_path, "pain-001") == 2
    fr = ld_blocks(read(tmp_path / "fr" / "pain-001" / "index.html"))[0]
    assert fr["headline"] == "Qu'est-ce" and fr["description"] == "A & B"
    assert fr["inLanguage"] == "fr" and fr["url"] == fr["mainEntityOfPage"] == "https://pain001.com/fr/pain-001/"
    en = ld_blocks(read(tmp_path / "pain-001" / "index.html"))[0]
    assert en["description"] == "" and en["inLanguage"] == "en" and en["@type"] == "TechArticle"
    assert "ld+json" not in read(tmp_path / "de" / "pain-001" / "index.html")
    assert read(tmp_path / "es" / "pain-001" / "index.html") == done
    assert "TechArticle structured data on 2 /pain-001/ page(s)" in capsys.readouterr().out


def test_inject_article_ld_escapes_script_close(tmp_path):
    put(tmp_path / "p" / "index.html", "<head><title>&lt;/script&gt;</title>"
        '<link rel="canonical" href="u"></head>')
    pb.inject_article_ld(tmp_path, "p")
    html = read(tmp_path / "p" / "index.html")
    assert '"headline": "\\u003c/script>"' in html


def test_inject_dataset_ld(root):
    site = root / "site"
    pb.inject_dataset_ld(site)
    assert not site.exists()
    put(root / "scripts" / "corpus_pages.json", {
        "corpus-a": {"@type": "Dataset", "name": "Ä"},
        "corpus-b": {"@type": "Dataset"},
        "corpus-missing": {"@type": "Dataset"},
    })
    put(site / "corpus-a" / "index.html", "<head></head>")
    done = '<head><script>{"@type": "Dataset"}</script></head>'
    put(site / "corpus-b" / "index.html", done)
    pb.inject_dataset_ld(site)
    assert read(site / "corpus-a" / "index.html") == (
        '<head><script type="application/ld+json">{"@type": "Dataset", "name": "Ä"}</script>\n</head>')
    assert read(site / "corpus-b" / "index.html") == done


def tiles(n):
    return "".join('<article class="t" data-package="p%d">' % i for i in range(n))


def test_stamp_package_count():
    assert pb.stamp_package_count("<h2>Five</h2>") == "<h2>Five</h2>"
    html = "<h2><span data-package-count>Five</span> packages</h2>" + tiles(4) + tiles(2)
    assert pb.stamp_package_count(html).startswith("<h2><span data-package-count>Four</span>")
    with pytest.raises(ValueError, match="count 0"):
        pb.stamp_package_count("<span data-package-count>x</span>")
    with pytest.raises(ValueError, match="count 13"):
        pb.stamp_package_count("<span data-package-count>x</span>" + tiles(13))


def test_stamp_home_package_count(tmp_path):
    pb.stamp_home_package_count(tmp_path)
    assert not (tmp_path / "index.html").exists()
    put(tmp_path / "index.html", "<span data-package-count>?</span>" + tiles(3))
    pb.stamp_home_package_count(tmp_path)
    assert read(tmp_path / "index.html").startswith("<span data-package-count>Three</span>")


GRAPH = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "@id": "s"}, {"@type": "WebPage", "@id": "p"}, {"@type": "BreadcrumbList"}]}


def home(data):
    return '<head><script type="application/ld+json">%s</script></head>' % json.dumps(data)


def test_enrich_home_ld():
    assert pb.enrich_home_ld("<head></head>", "1") == "<head></head>"
    assert pb.enrich_home_ld(home(GRAPH), "") == home(GRAPH)
    flat = home({"@type": "WebSite"})
    assert pb.enrich_home_ld(flat, "1") == flat
    out = pb.enrich_home_ld(home(GRAPH), "0.0.86")
    graph = ld_blocks(out)[0]["@graph"]
    assert graph[0]["publisher"] == {"@id": pb.ORG_ID}
    assert graph[1]["about"] == {"@id": pb.SOFTWARE_ID}
    assert graph[2] == {"@type": "BreadcrumbList"}
    assert [n["@type"] for n in graph[3:]] == ["SoftwareApplication", "Organization"]
    assert graph[3]["softwareVersion"] == "0.0.86" and graph[3]["isAccessibleForFree"] is True
    assert pb.enrich_home_ld(out, "0.0.86") == out


def test_add_home_software_ld(root, capsys):
    site = root / "site"
    pb.add_home_software_ld(site)
    put(site / "index.html", home(GRAPH))
    pb.add_home_software_ld(site)
    assert read(site / "index.html") == home(GRAPH)
    put(root / "static" / "corpus" / "index.json", {"pain001": "0.0.86"})
    pb.add_home_software_ld(site)
    assert '"softwareVersion": "0.0.86"' in read(site / "index.html")
    assert "SoftwareApplication 0.0.86 + Organization" in capsys.readouterr().out


def test_write_llms_without_index(root):
    site = root / "site"
    site.mkdir()
    pb.write_llms(site)
    short = read(site / "llms.txt")
    assert short.startswith("# Pain001\n\n> Open-source ISO 20022")
    assert "Suite version . Dual-licensed" in short
    assert "0 validated payment scenarios" in short
    assert read(site / "llms-full.txt").endswith("## Scenarios\n\n")


def test_write_llms_lists_each_scenario(root):
    put(root / "static" / "corpus" / "index.json", {"pain001": "0.0.86", "scenarios": [
        {"id": "a", "country": "gb", "family": "fps", "description": "Faster", "page": "https://p/a/"},
        {"id": "b", "country": None, "family": "x", "description": "None", "page": "https://p/b/"},
    ]})
    site = root / "site"
    site.mkdir()
    pb.write_llms(site)
    assert "Suite version 0.0.86." in read(site / "llms.txt")
    assert "2 validated payment scenarios" in read(site / "llms.txt")
    full = read(site / "llms-full.txt")
    assert "- a (GB, fps): Faster https://p/a/\n- b (, x): None https://p/b/\n" in full


FOOTER = '<footer class="site-footer"><div class="footer-bottom"><p class="footer-credit">Made</p></div></footer>'


def test_stamp_suite_version(root):
    site = root / "site"
    assert pb.stamp_suite_version(site) == 0
    put(root / "static" / "corpus" / "index.json", {"pain001": ""})
    assert pb.stamp_suite_version(site) == 0
    put(root / "static" / "corpus" / "index.json", {"pain001": "0.0.86"})
    put(site / "a" / "index.html", "<body>" + FOOTER + "</body>")
    put(site / "b" / "index.html", '<footer><p class="suite-version">Generated against pain001 0.0.1</p></footer>')
    put(site / "c" / "index.html", "<footer><p>no credit</p></footer>")
    put(site / "d" / "index.html", "<body>no footer</body>")
    put(site / "e" / "index.html", "<footer>unclosed")
    assert pb.stamp_suite_version(site) == 2
    stamp = '<p class="suite-version">Generated against pain001 0.0.86</p>'
    assert read(site / "a" / "index.html") == (
        '<body><footer class="site-footer"><div class="footer-bottom"><p class="footer-credit">Made</p>\n      '
        + stamp + "</div></footer></body>")
    assert read(site / "b" / "index.html") == "<footer>" + stamp + "</footer>"
    assert read(site / "c" / "index.html") == "<footer><p>no credit</p></footer>"
