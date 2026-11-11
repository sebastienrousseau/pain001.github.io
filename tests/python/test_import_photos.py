# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""import_photos.py licenses, crops, encodes and credits the site photos.

Pins the licence gate (only Unsplash and Pexels stems are used), the
credit parsing, the crops, the AVIF budget ladder, the credits table in
THIRD_PARTY_NOTICES.md, and main()'s refusals and stale-file cleanup.
Pillow is not installed in the test environment, so a small fake
`PIL` package records what the script asks of it.
"""

import json
import sys
import types
from pathlib import Path
from types import SimpleNamespace

import pytest

import import_photos as photos

U1 = "alev-takil-7ojyp-IXW7w-unsplash"
U2 = "francais-a-londres-b07tX5xgZ5U-unsplash"
U3 = "christoph-duschl-CE_TvPHF3lA"
P1 = "jane-doe-1234567"


class FakeImage:
    """Enough of PIL.Image.Image for the importer: sizes, crops, encodes."""

    saved = []
    sizes = {}

    def __init__(self, size, box=None):
        self.size = size
        self.box = box

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    def convert(self, mode):
        return self

    def crop(self, box):
        return FakeImage((box[2] - box[0], box[3] - box[1]), box)

    def resize(self, size, *resampling):
        return FakeImage(size)

    def filter(self, kind):
        assert kind == "FIND_EDGES"
        return self

    def getpixel(self, xy):
        return xy[1]  # detail grows towards the bottom of the photo

    def save(self, path, fmt, quality, **options):
        FakeImage.saved.append((Path(path).name, fmt, quality))
        size = FakeImage.sizes.get(fmt, 100)
        Path(path).write_bytes(b"x" * (size(quality) if callable(size) else size))


@pytest.fixture
def fake_pil(monkeypatch):
    opened = {}
    image = types.ModuleType("PIL.Image")
    image.LANCZOS = 1
    image.open = lambda path: FakeImage(opened[Path(path).name])
    image_filter = types.ModuleType("PIL.ImageFilter")
    image_filter.FIND_EDGES = "FIND_EDGES"
    pil = types.ModuleType("PIL")
    pil.Image, pil.ImageFilter = image, image_filter
    for name, module in (("PIL", pil), ("PIL.Image", image), ("PIL.ImageFilter", image_filter)):
        monkeypatch.setitem(sys.modules, name, module)
    monkeypatch.setattr(photos, "Image", image, raising=False)
    monkeypatch.setattr(FakeImage, "saved", [])
    monkeypatch.setattr(FakeImage, "sizes", {})
    return opened


@pytest.fixture
def env(tmp_path, monkeypatch, fake_pil):
    out = tmp_path / "static" / "img" / "photos"
    for name, value in (("ROOT", tmp_path), ("OUT", out), ("BAND_DIR", out / "band"),
                        ("MAP", tmp_path / "page_photos.json"),
                        ("NOTICES", tmp_path / "NOTICES.md"),
                        ("DEFAULT_SRC", tmp_path / "default-src")):
        monkeypatch.setattr(photos, name, value)
    photos.NOTICES.write_text(f"intro\n{photos.CREDITS_START}\nold\n{photos.CREDITS_END}\ntail\n",
                              encoding="utf-8")
    src = tmp_path / "src"
    src.mkdir()
    monkeypatch.setattr(sys, "argv", ["import_photos.py", str(src)])

    def setup(home, pages, sizes):
        photos.MAP.write_text(json.dumps({"homepage": home, "pages": pages}), encoding="utf-8")
        for stem, size in sizes.items():
            (src / f"{stem}.webp").write_bytes(b"")
            fake_pil[f"{stem}.webp"] = size

    return SimpleNamespace(root=tmp_path, out=out, src=src, setup=setup)


def test_photo_source_admits_only_unsplash_and_pexels():
    assert photos.photo_source(U1) == "unsplash"
    assert photos.photo_source(U3) == "unsplash"
    assert photos.photo_source("benjamin-davies-Oja2ty_9ZLMb") == "unsplash"
    assert photos.photo_source(P1) == "pexels"
    assert photos.photo_source("getty-images-ABCDEFGHIJK") is None
    assert photos.photo_source("someone-abcdefghijk") is None
    assert photos.photo_source("short") is None
    assert photos.band_path(P1) == f"/img/photos/band/pexels/{P1}"


def test_credit_names_the_photographer_and_photo():
    assert photos.credit(U1) == ("Alev Takil", "7ojyp-IXW7w")
    assert photos.credit(U2) == ("Français à Londres", "b07tX5xgZ5U")
    assert photos.credit(P1) == ("Jane Doe", "1234567")
    assert photos.credit("benjamin-davies-Oja2ty_9ZLMb") == ("Benjamin Davies", "Oja2ty_9ZLMb")


def test_source_prefers_the_plain_file_then_the_1920_one(tmp_path):
    (tmp_path / "b-1920.webp").write_bytes(b"")
    (tmp_path / "a.webp").write_bytes(b"")
    (tmp_path / "a-1920.webp").write_bytes(b"")
    assert photos.source(tmp_path, "a") == tmp_path / "a.webp"
    assert photos.source(tmp_path, "b") == tmp_path / "b-1920.webp"
    with pytest.raises(FileNotFoundError, match="c"):
        photos.source(tmp_path, "c")


def test_crop_centres_on_the_long_axis():
    assert photos.crop(FakeImage((3000, 1000)), (3, 2)).box == (750, 0, 2250, 1000)
    assert photos.crop(FakeImage((1000, 1000)), (2, 1)).box == (0, 250, 1000, 750)


def test_band_with_a_focus_uses_it(fake_pil):
    assert photos.band(FakeImage((2000, 1500)), 0.0).box == (0, 0, 2000, 1000)
    assert photos.band(FakeImage((3000, 1000)), 1.0).box == (500, 0, 2500, 1000)


def test_band_without_a_focus_follows_the_detail(fake_pil):
    # Detail sits at the bottom; the window is pulled halfway back to centre.
    assert photos.band(FakeImage((2000, 1500)), None).box == (0, 375, 2000, 1375)


def test_save_without_budget_writes_one_avif_at_the_default_quality(env, capsys):
    avif = photos.save(FakeImage((10, 10)), env.root / "a.webp", 480, (3, 2), 72)
    assert avif == env.root / "a.avif"
    assert FakeImage.saved == [("a.webp", "WEBP", 72), ("a.avif", "AVIF", photos.AVIF_QUALITY)]
    assert capsys.readouterr().out == "a.webp  480x320  0 KB (avif 0 KB)\n"


def test_save_over_budget_at_every_rung_keeps_the_last(env):
    FakeImage.sizes["AVIF"] = 50_000
    photos.save(FakeImage((10, 10)), env.root / "a.webp", 640, (2, 1), 60, avif_budget=12_000)
    rungs = [q for _, fmt, q in FakeImage.saved if fmt == "AVIF"]
    assert rungs == list(photos.AVIF_LADDER)


def test_save_stops_at_the_first_rung_that_fits(env):
    FakeImage.sizes["AVIF"] = lambda q: 100 if q <= 36 else 50_000
    photos.save(FakeImage((10, 10)), env.root / "a.webp", 640, (2, 1), 60, avif_budget=12_000)
    assert [q for _, fmt, q in FakeImage.saved if fmt == "AVIF"] == [45, 40, 36]


def test_write_credits_replaces_only_the_marked_table(env):
    photos.write_credits([("homepage: hero-city", "Alev Takil", "7ojyp-IXW7w", U1),
                          ("/about/", "Jane Doe", "1234567", P1)])
    assert photos.NOTICES.read_text(encoding="utf-8") == (
        f"intro\n{photos.CREDITS_START}\n\n"
        "| Used for | Photographer | Source |\n| :--- | :--- | :--- |\n"
        "| homepage: hero-city | Alev Takil | [Unsplash 7ojyp-IXW7w](https://unsplash.com/photos/7ojyp-IXW7w) |\n"
        "| /about/ | Jane Doe | [Pexels 1234567](https://www.pexels.com/photo/1234567/) |\n"
        f"\n{photos.CREDITS_END}\ntail\n")


def _import_all(env, monkeypatch):
    """Run main() over four photos with two stale files already in place."""
    monkeypatch.setattr(photos, "BAND_FOCUS", {P1: 0.0})
    env.setup({"hero-city": U1, "columns": U2}, {"": U3, "about": P1},
              {U1: (4200, 1800), U2: (3000, 2000), U3: (2000, 1400), P1: (2800, 1400)})
    stale = [env.out / "old-480.webp", env.out / "band" / "unsplash" / "gone.avif"]
    for path in stale:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"")
    assert photos.main() == 0


def _expected_files():
    def both(stem, widths):
        return {f"{stem}-{w}.{ext}" for w in widths for ext in ("webp", "avif")}

    return (both("hero-city", (800, 1200, 1600, 2400)) | both("columns", photos.WIDTHS)
            | both(f"band/unsplash/{U3}", photos.BAND_WIDTHS) | both(f"band/pexels/{P1}", photos.BAND_WIDTHS))


def test_main_imports_crops_credits_and_removes_stale_files(env, capsys, monkeypatch):
    _import_all(env, monkeypatch)
    names = {p.relative_to(env.out).as_posix() for p in env.out.rglob("*") if p.is_file()}
    assert names == _expected_files()
    out = capsys.readouterr().out
    assert "removed static/img/photos/old-480.webp\n" in out
    assert "removed static/img/photos/band/unsplash/gone.avif\n" in out


def test_main_writes_the_credits_table(env, monkeypatch):
    _import_all(env, monkeypatch)
    notices = photos.NOTICES.read_text(encoding="utf-8")
    assert "| homepage: hero-city | Alev Takil |" in notices
    assert "| homepage: columns | Français à Londres |" in notices
    assert "| locale home pages | Christoph Duschl |" in notices
    assert "| /about/ | Jane Doe | [Pexels 1234567]" in notices
    assert "\nold\n" not in notices


def test_main_reads_the_default_library_without_an_argument(env, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["import_photos.py"])
    monkeypatch.setattr(photos, "DEFAULT_SRC", env.src)
    env.setup({}, {"x": U3}, {U3: (2000, 1400)})
    assert photos.main() == 0
    assert (env.out / "band" / "unsplash" / f"{U3}-640.webp").is_file()


@pytest.mark.parametrize(("home", "pages", "sizes", "message"), [
    ({"hero-city": U1}, {"x": U1}, {}, f"each photo is used once; repeated: ['{U1}']"),
    ({}, {"x": "getty-images-ABCDEFGHIJK"}, {},
     "not an Unsplash or Pexels photo: ['getty-images-ABCDEFGHIJK']"),
    ({"hero-city": P1}, {}, {P1: (4200, 1800)},
     f"homepage photos sit under the Unsplash annotation: {P1}"),
    ({}, {"x": U3}, {U3: (1000, 1000)},
     f"/x/: {U3} is 1000x1000; bands need landscape photos (at least 1.4:1)"),
])
def test_main_refuses_what_the_site_may_not_ship(env, capsys, home, pages, sizes, message):
    env.setup(home, pages, sizes)
    assert photos.main() == 1
    assert capsys.readouterr().err == message + "\n"
    assert photos.NOTICES.read_text(encoding="utf-8").count("\nold\n") == 1
