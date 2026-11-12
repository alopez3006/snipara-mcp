from __future__ import annotations

from typing import Any

import pytest

from snipara_mcp import server as server_module


def _tool_by_name(tools: list[Any], name: str) -> Any:
    return next(tool for tool in tools if tool.name == name)


@pytest.mark.asyncio
@pytest.mark.parametrize("params", [
    {"branch": "dev", "task": "handoff", "changedFiles": ["a.py"], "max_tokens": 4000},
    {"mode": "context", "memory_ids": ["m1"], "proposed_citations": ["m1"]},
    {"mode": "validate_actions", "proposed_actions": [], "proposed_citations": []},
])
async def test_resume_dispatch_preserves_both_legacy_and_source_requests(monkeypatch, params):
    call = {}

    async def fake_api(name, arguments):
        call.update(name=name, arguments=arguments)
        return {"success": True, "result": {"resumeContext": {"version": "fixture"}}}

    monkeypatch.setattr(server_module, "call_api", fake_api)
    response = await server_module.call_tool("snipara_resume_context", params)
    assert call == {"name": "rlm_resume_context", "arguments": params}
    assert "fixture" in response[0].text


@pytest.mark.asyncio
async def test_full_profile_exposes_graveyard_lite_memory_surface(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv("SNIPARA_TOOL_PROFILE", "full")
    tools = await server_module.list_tools()

    recall = _tool_by_name(tools, "snipara_recall")
    memories = _tool_by_name(tools, "snipara_memories")
    invalidate = _tool_by_name(tools, "snipara_memory_invalidate")
    supersede = _tool_by_name(tools, "snipara_memory_supersede")

    recall_props = recall.inputSchema["properties"]
    assert "include_inactive" in recall_props
    assert recall_props["include_inactive"]["default"] is False
    assert "warning_threshold" not in recall_props

    memories_props = memories.inputSchema["properties"]
    assert memories_props["status"]["enum"] == ["ACTIVE", "INVALIDATED", "SUPERSEDED"]
    assert memories_props["include_inactive"]["default"] is False

    assert invalidate.inputSchema["required"] == ["memory_id"]
    assert "invalidated_at" in invalidate.inputSchema["properties"]
    assert supersede.inputSchema["required"] == ["old_memory_id", "new_memory_id"]


@pytest.mark.asyncio
async def test_call_tool_forwards_recall_warning_controls(monkeypatch: pytest.MonkeyPatch):
    captured: dict[str, Any] = {}

    async def fake_call_api(tool: str, params: dict[str, Any]) -> dict[str, Any]:
        captured["tool"] = tool
        captured["params"] = params
        return {
            "success": True,
            "result": {
                "memories": [
                    {
                        "memory_id": "mem_active",
                        "content": "Bearer auth is the current path.",
                        "type": "decision",
                        "status": "ACTIVE",
                        "relevance": 0.91,
                        "confidence": 1.0,
                        "access_count": 3,
                    }
                ],
                "warnings": [
                    {
                        "memory_id": "mem_old",
                        "status": "SUPERSEDED",
                        "content": "Use API key only.",
                        "reason": "Replaced by bearer-auth decision",
                        "relevance": 0.84,
                    }
                ],
                "total_searched": 2,
            },
        }

    monkeypatch.setattr(server_module, "call_api", fake_call_api)

    contents = await server_module.call_tool(
        "rlm_recall",
        {
            "query": "auth flow",
            "retrieval_queries": ["authentication decisions"],
            "include_inactive": True,
            "correlation_context": {
                "version": "retrieval-correlation-v1",
                "session_id": "agent-session:recall",
            },
        },
    )

    assert captured["tool"] == "rlm_recall"
    assert captured["params"]["retrieval_queries"] == ["authentication decisions"]
    assert captured["params"]["include_inactive"] is True
    assert "warning_threshold" not in captured["params"]
    assert captured["params"]["correlation_context"]["session_id"] == ("agent-session:recall")
    assert "Inactive memory warnings" in contents[0].text
    assert "SUPERSEDED" in contents[0].text


@pytest.mark.asyncio
async def test_call_tool_supports_memory_lifecycle_mutations(monkeypatch: pytest.MonkeyPatch):
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call_api(tool: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((tool, params))
        if tool == "rlm_memory_invalidate":
            return {
                "success": True,
                "result": {
                    "memory_id": "mem_123",
                    "status": "INVALIDATED",
                    "invalidated_at": "2026-04-22T06:00:00Z",
                },
            }
        if tool == "rlm_memory_supersede":
            return {
                "success": True,
                "result": {
                    "old_memory_id": "mem_123",
                    "new_memory_id": "mem_456",
                    "old_status": "SUPERSEDED",
                    "new_status": "ACTIVE",
                },
            }
        raise AssertionError(f"Unexpected tool {tool}")

    monkeypatch.setattr(server_module, "call_api", fake_call_api)

    invalidate = await server_module.call_tool(
        "rlm_memory_invalidate",
        {"memory_id": "mem_123", "reason": "obsolete"},
    )
    supersede = await server_module.call_tool(
        "rlm_memory_supersede",
        {
            "old_memory_id": "mem_123",
            "new_memory_id": "mem_456",
            "reason": "OAuth rollout",
        },
    )

    assert calls[0] == (
        "rlm_memory_invalidate",
        {"memory_id": "mem_123", "reason": "obsolete"},
    )
    assert calls[1][0] == "rlm_memory_supersede"
    assert calls[1][1]["old_memory_id"] == "mem_123"
    assert calls[1][1]["new_memory_id"] == "mem_456"

    assert "Memory invalidated" in invalidate[0].text
    assert "Memory superseded" in supersede[0].text
    assert "mem_456" in supersede[0].text


@pytest.mark.asyncio
async def test_stdio_history_never_silently_accepts_legacy_current_result(monkeypatch):
    calls = []
    async def old_server(tool, arguments):
        calls.append(arguments)
        return {"success": True, "result": {"memories": []}}
    monkeypatch.setattr(server_module, "call_api", old_server)
    response = await server_module.call_tool("snipara_recall", {"query": "decision", "memory_view": "history", "as_of": "2020-01-01T00:00:00Z"})
    assert calls[0]["memory_view"] == "history" and calls[0]["as_of"] == "2020-01-01T00:00:00Z"
    assert "did not confirm" in response[0].text
