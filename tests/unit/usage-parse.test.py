"""
Purpose: check parsing of the usage endpoint JSON and token-expiry logic.
Expected: weekly %, reset time and session % are read; broken shapes raise UsageError.
Related: plan v0.1.0 (docs/tasks/todo.md). No bug/lesson ID.
Preconditions: none. Canned JSON (trimmed real response), no network.
"""
from datetime import datetime, timezone

import pytest

from clawd_pacer.credentials import is_expired
from clawd_pacer.usage_client import UsageError, parse_usage

SAMPLE = {
    "five_hour": {"utilization": 6.0,
                  "resets_at": "2026-10-05T09:30:00.081110+00:00"},
    "seven_day": {"utilization": 20.0,
                  "resets_at": "2026-10-11T03:00:00.081135+00:00"},
    "seven_day_opus": None,
}


def test_parse_real_shape():
    u = parse_usage(SAMPLE)
    assert u.weekly_pct == 20.0
    assert u.session_pct == 6.0
    assert u.resets_at == datetime(2026, 10, 11, 3, 0, 0, 81135,
                                   tzinfo=timezone.utc)


def test_missing_session_is_ok():
    u = parse_usage({"seven_day": SAMPLE["seven_day"], "five_hour": None})
    assert u.session_pct is None


@pytest.mark.parametrize("bad", [
    {},
    {"seven_day": {"utilization": 20.0}},
    {"seven_day": {"utilization": "x", "resets_at": "2026-10-11T03:00:00+00:00"}},
    {"seven_day": {"utilization": 1, "resets_at": "not a date"}},
])
def test_bad_shapes_raise_usage_error(bad):
    with pytest.raises(UsageError):
        parse_usage(bad)


def test_token_expiry():
    assert is_expired(1000, now_ms=2000)
    assert not is_expired(3000, now_ms=2000)
    assert not is_expired(None, now_ms=2000)


@pytest.mark.parametrize("code,msg", [(401, "Login expired"), (500, "HTTP 500")])
def test_http_errors_become_friendly_usage_errors(monkeypatch, code, msg):
    import urllib.error
    from clawd_pacer import usage_client

    def fake_urlopen(req, timeout):
        raise urllib.error.HTTPError(req.full_url, code, "x", {}, None)

    monkeypatch.setattr(usage_client.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(UsageError, match=msg):
        usage_client.fetch_usage("fake-token")


def test_no_weekly_limit_says_pro_max():
    with pytest.raises(UsageError, match="Pro/Max"):
        parse_usage({"seven_day": None})


def test_credentials_path_respects_claude_config_dir():
    import os
    from clawd_pacer.credentials import credentials_path
    assert credentials_path({"CLAUDE_CONFIG_DIR": "D:/cc"}) == os.path.join("D:/cc", ".credentials.json")
    default = credentials_path({})
    assert default.endswith(os.path.join(".claude", ".credentials.json"))
    assert "~" not in default
