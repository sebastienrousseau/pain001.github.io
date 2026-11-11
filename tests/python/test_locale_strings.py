# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The locale chrome tables keep the shape postbuild_fix indexes into.

postbuild_fix.translate_chrome reads STRINGS[locale] by position (26
slots, documented at the top of locale_strings.py) and
translate_status_strip reads STATUS_STRIP[locale] the same way (8
slots). A locale with a missing or extra entry would shift every later
string onto the wrong element, so the shape is pinned here.
"""

import locale_strings

CHROME_SLOTS = 26
STRIP_SLOTS = 8


def test_every_locale_has_every_chrome_slot():
    assert len(locale_strings.STRINGS) == 34
    for slug, strings in locale_strings.STRINGS.items():
        assert len(strings) == CHROME_SLOTS, slug


def test_every_locale_has_a_status_strip_of_the_same_shape():
    assert set(locale_strings.STATUS_STRIP) == set(locale_strings.STRINGS)
    for slug, strings in locale_strings.STATUS_STRIP.items():
        assert len(strings) == STRIP_SLOTS, slug


def test_no_string_is_empty_or_padded():
    for table in (locale_strings.STRINGS, locale_strings.STATUS_STRIP):
        for slug, strings in table.items():
            for text in strings:
                assert text and text == text.strip(), (slug, text)


def test_known_slots_hold_what_the_header_says():
    fr = locale_strings.STRINGS["fr"]
    assert fr[0] == "Accueil"
    assert fr[16] == "Cet aperçu en 34 langues"
    assert fr[CHROME_SLOTS - 1] == "ouvrir"
