# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/check_dated_claims.py fetch retries.

The weekly run failed three times in five on a refused or timed-out
connection to the Internet Archive while every claim held when read again.
A transient network error is retried; a source that stays unreadable is
still a failure, so the check never silently skips.
"""

from __future__ import annotations

import datetime as dt
import io
import urllib.error

import pytest

import check_dated_claims as gate

CLAIM = {
    "id": "example",
    "source": "https://example.org/notice",
    "expect": ["the release moves to November"],
    "review_by": "2099-01-01",
}
PAGE = b"<html><body><p>The release moves to November.</p></body></html>"


class _Response(io.BytesIO):
    url = "https://example.org/notice"
    headers: dict[str, str] = {}

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@pytest.fixture
def no_sleep(monkeypatch):
    monkeypatch.setattr(gate.time, "sleep", lambda _seconds: None)


def _urlopen(failures: int, calls: list[int]):
    def fake(_request, timeout):
        calls.append(timeout)
        if len(calls) <= failures:
            raise urllib.error.URLError("[Errno 111] Connection refused")
        return _Response(PAGE)

    return fake


def test_a_transient_error_is_retried(monkeypatch, no_sleep):
    calls: list[int] = []
    monkeypatch.setattr(gate.urllib.request, "urlopen", _urlopen(1, calls))
    row = gate.check(CLAIM, dt.date(2026, 10, 26))
    assert row["ok"], row["problems"]
    assert len(calls) == 2


def test_a_source_that_stays_unreadable_still_fails(monkeypatch, no_sleep):
    calls: list[int] = []
    monkeypatch.setattr(gate.urllib.request, "urlopen", _urlopen(99, calls))
    row = gate.check(CLAIM, dt.date(2026, 10, 26))
    assert not row["ok"]
    assert row["problems"][0].startswith("source could not be read: URLError")
    assert len(calls) == gate.ATTEMPTS


def test_an_http_error_is_not_retried(monkeypatch, no_sleep):
    calls: list[int] = []

    def forbidden(_request, timeout):
        calls.append(timeout)
        raise urllib.error.HTTPError(CLAIM["source"], 403, "Forbidden", {}, None)

    monkeypatch.setattr(gate.urllib.request, "urlopen", forbidden)
    row = gate.check(CLAIM, dt.date(2026, 10, 26))
    assert not row["ok"]
    assert len(calls) == 1


def _throttled(code: int, failures: int, calls: list[int], retry_after: str | None = None):
    def fake(_request, timeout):
        calls.append(timeout)
        if len(calls) <= failures:
            headers = {"Retry-After": retry_after} if retry_after else {}
            raise urllib.error.HTTPError(CLAIM["source"], code, "Busy", headers, None)
        return _Response(PAGE)

    return fake


@pytest.mark.parametrize("code", [429, 502, 503, 504])
def test_a_throttled_answer_is_retried(monkeypatch, no_sleep, code):
    calls: list[int] = []
    monkeypatch.setattr(gate.urllib.request, "urlopen", _throttled(code, 1, calls))
    row = gate.check(CLAIM, dt.date(2026, 11, 5))
    assert row["ok"], row["problems"]
    assert len(calls) == 2


def test_a_source_that_stays_throttled_still_fails(monkeypatch, no_sleep):
    calls: list[int] = []
    monkeypatch.setattr(gate.urllib.request, "urlopen", _throttled(503, 99, calls))
    row = gate.check(CLAIM, dt.date(2026, 11, 5))
    assert not row["ok"]
    assert row["problems"][0].startswith("source could not be read: HTTPError")
    assert len(calls) == gate.ATTEMPTS


def test_retry_after_is_honoured_within_the_cap(monkeypatch):
    waits: list[float] = []
    monkeypatch.setattr(gate.time, "sleep", waits.append)
    calls: list[int] = []
    monkeypatch.setattr(gate.urllib.request, "urlopen", _throttled(429, 2, calls, "45"))
    assert gate.check(CLAIM, dt.date(2026, 11, 5))["ok"]
    calls.clear()
    monkeypatch.setattr(gate.urllib.request, "urlopen", _throttled(429, 1, calls, "9999"))
    assert gate.check(CLAIM, dt.date(2026, 11, 5))["ok"]
    assert waits == [45, 45, gate.MAX_WAIT_SECONDS]
