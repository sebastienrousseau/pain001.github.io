# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Regression tests for the corpus zip writer in generate_corpus_page.py.

Guards fix bf8fc2fb ("keep corpus zips whose contents match"): DEFLATE
output differs between zlib builds, so a regeneration on Linux rewrote
zips built on macOS although nothing had changed. Also guards fix
9f9e07ae ("give the zip check's except a result"): a damaged zip must
be replaced, not kept or allowed to stop the build.
"""

import zipfile

import generate_corpus_page as gcp

ENTRIES = [
    ("coverage.json", b'{"files": 2}\n'),
    ("a.xml", b"<Document>" + b"x" * 4000 + b"</Document>"),
]


def _recompress(path, level):
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp, "w") as dst:
        for info in src.infolist():
            dst.writestr(info, src.read(info.filename), compresslevel=level)
    tmp.replace(path)


def test_new_zip_is_written_with_fixed_metadata(tmp_path):
    target = tmp_path / "c.zip"
    gcp.write_zip(target, ENTRIES)
    with zipfile.ZipFile(target) as zf:
        assert [(i.filename, i.date_time, i.external_attr) for i in zf.infolist()] == [
            (name, gcp.ZIP_TIME, 0o644 << 16) for name, _ in ENTRIES]
        assert [zf.read(name) for name, _ in ENTRIES] == [data for _, data in ENTRIES]


def test_same_content_compressed_differently_is_kept_byte_for_byte(tmp_path):
    target = tmp_path / "c.zip"
    gcp.write_zip(target, ENTRIES)
    _recompress(target, 1)  # what another zlib build produces
    before = target.read_bytes()

    gcp.write_zip(target, ENTRIES)

    assert target.read_bytes() == before


def test_changed_member_is_rewritten(tmp_path):
    target = tmp_path / "c.zip"
    gcp.write_zip(target, ENTRIES)
    changed = [ENTRIES[0], ("a.xml", ENTRIES[1][1] + b"<!-- new -->")]

    gcp.write_zip(target, changed)

    with zipfile.ZipFile(target) as zf:
        assert zf.read("a.xml").endswith(b"<!-- new -->")


def test_damaged_zip_is_replaced(tmp_path):
    target = tmp_path / "c.zip"
    gcp.write_zip(target, ENTRIES)
    target.write_bytes(target.read_bytes()[:40])  # a truncated file

    assert gcp.zip_holds(target, ENTRIES) is False
    gcp.write_zip(target, ENTRIES)

    assert gcp.zip_holds(target, ENTRIES) is True


def test_missing_zip_holds_nothing(tmp_path):
    assert gcp.zip_holds(tmp_path / "absent.zip", ENTRIES) is False
