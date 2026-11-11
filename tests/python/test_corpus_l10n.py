# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""corpus_l10n.check() finds every way a locale can drift from English.

The scenario pages format each locale's strings with the English
placeholders, so a locale missing a key, a nested key or a placeholder
would fail or silently drop content at generation time. check() is the
gate; these tests prove it passes on the shipped table and reports each
kind of drift.
"""

import copy

import corpus_l10n


def test_shipped_strings_are_consistent():
    assert corpus_l10n.check() == []
    assert set(corpus_l10n.STRINGS) == {"en", *corpus_l10n.CORPUS_LOCALES}


def _with(monkeypatch, mutate):
    strings = copy.deepcopy(corpus_l10n.STRINGS)
    mutate(strings)
    monkeypatch.setattr(corpus_l10n, "STRINGS", strings)
    return corpus_l10n.check()


def test_missing_top_level_key_is_reported(monkeypatch):
    problems = _with(monkeypatch, lambda s: s["de"].pop("eyebrow"))
    assert problems == ["de: keys differ: ['eyebrow']"]


def test_missing_nested_key_is_reported(monkeypatch):
    problems = _with(monkeypatch, lambda s: s["fr"]["levels"].pop("assumed"))
    assert problems == ["fr.levels: keys differ"]


def test_changed_placeholder_is_reported(monkeypatch):
    def mutate(strings):
        strings["it"]["title"] = "Esempio {sid}: {paese}"

    assert _with(monkeypatch, mutate) == ["it.title: placeholders differ"]
