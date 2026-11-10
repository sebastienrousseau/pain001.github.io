# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Busy hero photographs must fit their existing critical-image budget."""

from types import SimpleNamespace

import import_photos as photos


def test_encoder_can_meet_budget_below_previous_quality_floor(tmp_path, monkeypatch):
    """The old last rung left the tablet hero above its 28,000-byte budget."""
    monkeypatch.setattr(photos, "ROOT", tmp_path)
    monkeypatch.setattr(photos, "Image", SimpleNamespace(LANCZOS=1), raising=False)

    class Encoder:
        """Represent the measured sizes without Pillow in the CI test suite."""

        def resize(self, size, resampling):
            assert size == (1600, 800)
            return self

        def save(self, path, format, quality, **options):
            size = 27_586 if quality <= 20 else 31_696
            path.write_bytes(b"x" * size)

    output = photos.save(Encoder(), tmp_path / "hero.webp", 1600, (2, 1), 60,
                         avif_budget=photos.BAND_AVIF_BUDGET[1600])
    assert output.stat().st_size <= photos.BAND_AVIF_BUDGET[1600]
