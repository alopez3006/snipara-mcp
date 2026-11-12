"""The stdio package forwards source pointers, the session id and the phase outcome to the hosted server unchanged."""

from __future__ import annotations

import pytest

from snipara_mcp import server as server_module

SOURCES = [
    {"path": ".snipara/plans/core.json", "json_pointer": "/phases/3"},
    {"commit": "0123456789abcdef0123456789abcdef01234567"},
]


@pytest.fixture
def calls(monkeypatch):
    seen: list[tuple[str, dict]] = []

    async def fake_api(name, arguments):
        seen.append((name, arguments))
        return {"success": True, "result": {"stored": True, "memory_id": "m1", "stored_count": 1, "recorded": 1}}

    monkeypatch.setattr(server_module, "call_api", fake_api)
    return seen


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool", "hosted", "base"),
    [
        ("snipara_remember", "rlm_remember", {"text": "The cascade keeps rerank before the judge."}),
        ("snipara_remember_if_novel", "rlm_remember_if_novel", {"text": "The cascade keeps rerank before the judge."}),
        ("snipara_end_of_task_commit", "rlm_end_of_task_commit", {"summary": "Phase 3 done: the cascade keeps rerank first."}),
    ],
)
async def test_memory_writes_forward_sources_and_session_id(calls, tool, hosted, base):
    await server_module.call_tool(tool, {**base, "sources": SOURCES, "session_id": "wf-session-1"})

    arguments = next(args for name, args in calls if name == hosted)  # a session bootstrap call may come first
    assert arguments["sources"] == SOURCES
    assert arguments["session_id"] == "wf-session-1"


@pytest.mark.asyncio
async def test_phase_outcome_forwards_every_phase_field(calls):
    payload = {
        "phase_id": "plan-slug:3",
        "result": "succeeded_verified",
        "memory_ids": ["m1", "m2"],
        "receipt_ref": "sandbox-run-17",
        "verdicts": {"m2": "misled"},
        "session_id": "wf-session-1",
    }

    await server_module.call_tool("snipara_memory_outcome", payload)

    assert [args for name, args in calls if name == "rlm_memory_outcome"] == [payload]
