"""Shared package-test fixtures."""

from __future__ import annotations

import pytest

from snipara_mcp import server as mcp_server


@pytest.fixture(autouse=True)
def authenticated_stdio_server(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep existing handler tests authenticated unless they test discovery mode."""
    monkeypatch.setattr(mcp_server, "_auth_token", "rlm_package_test")
    monkeypatch.setattr(mcp_server, "_auth_type", "api_key")
    monkeypatch.setattr(mcp_server, "API_KEY", "")
    monkeypatch.setattr(mcp_server, "PROJECT_ID", "package-test-project")
