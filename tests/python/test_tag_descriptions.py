# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tag pages get a description a search result can use.

ssg's taxonomy pages said only "393 page(s) under Tags: SEPA." (29 to
38 characters), under the 50 a search engine treats as a description.
"""

import re

import tag_descriptions as td

SSG = ('<html><head><title>Pages tagged pain.001 on Pain001</title>'
       '<meta name="description" content="1 page(s) under Tags: pain.001.">'
       '<meta property="og:description" content="393 page(s) under Tags: SEPA."></head></html>')


def test_the_ssg_sentence_is_replaced_in_every_meta():
    out = td.rewrite(SSG)
    assert 'content="1 pain001.com page tagged pain.001: guides, references and example files' in out
    assert 'content="393 pain001.com pages tagged SEPA: guides, references and example files' in out
    assert "page(s) under" not in out
    assert all(50 <= len(d) <= 160 for d in re.findall(r'content="([^"]*)"', out))
    assert td.rewrite(out) == out


def test_main_rewrites_only_tag_pages(tmp_path, capsys, monkeypatch):
    (tmp_path / "tags" / "sepa").mkdir(parents=True)
    (tmp_path / "tags" / "sepa" / "index.html").write_text(SSG, encoding="utf-8")
    (tmp_path / "tags" / "index.html").write_text("<head></head>", encoding="utf-8")
    (tmp_path / "other.html").write_text(SSG, encoding="utf-8")
    assert td.main([str(tmp_path)]) == 0
    assert "page(s) under" not in (tmp_path / "tags" / "sepa" / "index.html").read_text(encoding="utf-8")
    assert (tmp_path / "other.html").read_text(encoding="utf-8") == SSG
    assert capsys.readouterr().out == "[tag_descriptions] described 1 tag page(s)\n"
    monkeypatch.setattr("sys.argv", ["tag_descriptions.py"])
    assert td.main() == 2
