# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""validate_seo_meta holds every indexable page to search-result sizes.

An audit in November 2026 found 234 indexable pages with a description
over 160 characters or under 50 and 44 with a title over 65. The gate
counts characters after entity decoding (an apostrophe written as
&#39; is one character, and one inside a double-quoted attribute does
not end it) and skips noindex pages and redirect stubs.
"""

import validate_seo_meta as v

OK_DESC = "d" * 50


def page(title="Short title", description=OK_DESC, extra=""):
    return (f'<html><head><title>{title}</title>{extra}'
            f'<meta name="description" content="{description}"></head><body></body></html>')


def test_a_page_within_limits_passes():
    assert v.page_problems("a.html", page()) == []
    assert v.page_problems("a.html", page(title="t" * 65, description="d" * 160)) == []


def test_each_limit_is_reported():
    assert v.page_problems("a.html", page(title="t" * 66)) == [
        "a.html: title is 66 characters, over 65: " + "t" * 66]
    assert v.page_problems("b.html", page(description="d" * 161)) == [
        "b.html: description is 161 characters, not 50 to 160"]
    assert v.page_problems("c.html", page(description="d" * 49)) == [
        "c.html: description is 49 characters, not 50 to 160"]
    assert v.page_problems("d.html", "<html><head></head></html>") == [
        "d.html: description is 0 characters, not 50 to 160"]


def test_entities_and_apostrophes_count_as_one_character():
    description = "Turn your bank&#39;s guideline into a profile, " + "x" * 3
    assert len("Turn your bank's guideline into a profile, xxx") == 46
    assert v.page_problems("a.html", page(description=description)) == [
        "a.html: description is 46 characters, not 50 to 160"]
    assert v.page_problems("b.html", page(title="&eacute;t&eacute; " + "t" * 61)) == []


def test_noindex_pages_and_redirect_stubs_are_skipped():
    noindex = '<meta name="robots" content="noindex, follow">'
    refresh = '<meta http-equiv="refresh" content="0; url=/x/">'
    assert v.page_problems("a.html", page(title="t" * 99, extra=noindex)) == []
    assert v.page_problems("b.html", page(description="", extra=refresh)) == []


def test_main_reports_on_stderr_and_skips_fingerprinted_assets(tmp_path, capsys, monkeypatch):
    (tmp_path / "_csp").mkdir()
    (tmp_path / "_csp" / "x.html").write_text(page(title="t" * 99), encoding="utf-8")
    (tmp_path / "index.html").write_text(page(), encoding="utf-8")
    assert v.main([str(tmp_path)]) == 0
    assert capsys.readouterr().out == "SEO meta: titles and descriptions within limits on 1 page(s)\n"
    (tmp_path / "bad.html").write_text(page(title="t" * 70), encoding="utf-8")
    assert v.main([str(tmp_path)]) == 1
    assert capsys.readouterr().err.endswith("SEO meta: 1 problem(s) on 2 page(s)\n")
    monkeypatch.setattr(v, "ROOT", tmp_path / "missing")
    monkeypatch.setattr("sys.argv", ["validate_seo_meta.py"])
    assert v.main() == 0


def test_only_the_first_title_and_description_count():
    head = ('<html><head><meta charset="utf-8"><link rel="icon" href="/i.svg"><style>p{}</style>'
            '<title>First</title><title>' + "t" * 99 + '</title>'
            f'<meta name="description" content="{OK_DESC}"><meta name="description" content="x"></head></html>')
    parsed = v.head(head)
    assert parsed.title == "First" and parsed.meta["description"] == OK_DESC
    assert v.page_problems("a.html", head) == []
