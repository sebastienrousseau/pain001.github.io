# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for scripts/seo_scoreboard.py's authenticated POST.

google-auth is not installed in CI, so small fakes stand in for it. Pins
that Application Default Credentials are asked for the read-only scope,
that the query goes to the encoded property URL with a timeout, and that
an HTTP error is raised rather than reported as an empty scoreboard.
"""

from __future__ import annotations

import sys
import types

import pytest

import seo_scoreboard as sb


class _Response:
    def __init__(self, payload, error=None):
        self.payload, self.error = payload, error

    def raise_for_status(self):
        if self.error:
            raise self.error

    def json(self):
        return self.payload


@pytest.fixture
def fake_google(monkeypatch):
    calls = {"scopes": [], "posts": [], "responses": []}

    def default(scopes):
        calls["scopes"].append(scopes)
        return "CREDENTIALS", "project"

    class AuthorizedSession:
        def __init__(self, credentials):
            calls["credentials"] = credentials

        def post(self, url, json, timeout):
            calls["posts"].append((url, json, timeout))
            return calls["responses"].pop(0)

    google = types.ModuleType("google")
    auth = types.ModuleType("google.auth")
    transport = types.ModuleType("google.auth.transport")
    requests = types.ModuleType("google.auth.transport.requests")
    auth.default = default
    google.auth = auth
    auth.transport = transport
    transport.requests = requests
    requests.AuthorizedSession = AuthorizedSession
    for name, module in (("google", google), ("google.auth", auth),
                         ("google.auth.transport", transport), ("google.auth.transport.requests", requests)):
        monkeypatch.setitem(sys.modules, name, module)
    return calls


def test_authorized_post_queries_the_property(fake_google):
    fake_google["responses"].append(_Response({"rows": []}))
    post = sb.authorized_post()
    assert post({"startDate": "a"}) == {"rows": []}
    assert fake_google["scopes"] == [[sb.SCOPE]]
    assert fake_google["credentials"] == "CREDENTIALS"
    url = "https://searchconsole.googleapis.com/webmasters/v3/sites/sc-domain%3Apain001.com/searchAnalytics/query"
    assert fake_google["posts"] == [(url, {"startDate": "a"}, 60)]


def test_authorized_post_raises_on_http_error(fake_google):
    fake_google["responses"].append(_Response({}, RuntimeError("403 Forbidden")))
    with pytest.raises(RuntimeError, match="403"):
        sb.authorized_post()({})


def test_main_with_credentials_uses_the_authorized_post(fake_google, monkeypatch, capsys):
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "/tmp/creds.json")
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    fake_google["responses"].extend(_Response({"rows": []}) for _ in range(8))
    assert sb.main([]) == 0
    assert len(fake_google["posts"]) == 8
    assert capsys.readouterr().out.startswith("# pain001.com Search Console scoreboard")
