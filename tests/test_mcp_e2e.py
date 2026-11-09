"""E2E-style tests for the packaged MCP server and SDK transport client."""

from __future__ import annotations

import asyncio
import json
from copy import deepcopy
from typing import Any

import httpx
import pytest

from snipara_mcp import server as mcp_server
from snipara_mcp.rlm_tools import SniparaClient


class LocalMcpBackend:
    """Small hosted-MCP fixture that records real HTTP requests."""

    def __init__(self, context_payload: dict[str, Any] | None = None) -> None:
        self.requests: list[dict[str, Any]] = []
        self.context_payload = context_payload

    def __call__(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content.decode("utf-8"))
        self.requests.append(
            {
                "method": request.method,
                "path": request.url.path,
                "headers": dict(request.headers),
                "body": body,
            }
        )

        if request.url.path.endswith("/api/mcp/e2e-project"):
            return self._tool_response(body)

        if request.url.path != "/v1/e2e-project/mcp":
            return httpx.Response(404, json={"success": False, "error": "not found"})

        return self._tool_response(body)

    def _tool_response(self, body: dict[str, Any]) -> httpx.Response:
        tool = body["tool"]
        params = body.get("params") or {}
        if tool == "rlm_context_query":
            payload = {
                "sections": [
                    {
                        "title": "SDK Endpoint Contract",
                        "file": "docs/sdk.md",
                        "content": f"Context for {params['query']}",
                        "relevance_score": 0.97,
                    }
                ],
                "total_tokens": 42,
            }
            if self.context_payload is not None:
                payload = self.context_payload
        elif tool == "rlm_remember_if_novel":
            payload = {
                "stored": True,
                "reason": "novel",
                "memory_id": "mem_e2e",
            }
        elif tool == "rlm_memory_health":
            payload = {
                "status": "healthy",
                "orphaned_memories": 0,
            }
        elif tool == "rlm_htask_get":
            payload = {
                "task_id": params.get("task_id"),
                "title": "E2E htask",
                "status": "OPEN",
            }
        else:
            return httpx.Response(400, json={"success": False, "error": f"unknown tool {tool}"})
        return httpx.Response(200, json={"success": True, "result": payload})


def _install_mock_transport(monkeypatch, backend: LocalMcpBackend) -> None:
    original_async_client = httpx.AsyncClient
    transport = httpx.MockTransport(backend)

    def async_client_factory(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
        kwargs["transport"] = transport
        return original_async_client(*args, **kwargs)

    monkeypatch.setattr(mcp_server.httpx, "AsyncClient", async_client_factory)


def _disable_bootstrap(monkeypatch) -> None:
    async def settings() -> dict[str, Any]:
        return {
            "maxTokensPerQuery": 4000,
            "searchMode": "hybrid",
            "includeSummaries": True,
            "memoryAutoRecallOnSessionStart": False,
            "memoryAutoRecallOnResume": False,
        }

    monkeypatch.setattr(mcp_server, "get_project_settings", settings)
    monkeypatch.setattr(mcp_server, "_get_shared_context_bootstrap_config", lambda: (False, 30))
    monkeypatch.setattr(mcp_server, "_session_initialized", False)
    monkeypatch.setattr(mcp_server, "_shared_context_bootstrapped", False)
    monkeypatch.setattr(mcp_server, "_session_context", "")


def test_server_e2e_list_tools_and_real_tool_calls(monkeypatch) -> None:
    """The stdio server should list tools and execute real HTTP tool payloads."""
    backend = LocalMcpBackend()
    _install_mock_transport(monkeypatch, backend)
    _disable_bootstrap(monkeypatch)
    monkeypatch.setattr(mcp_server, "API_URL", "https://fixture.snipara.test")
    monkeypatch.setattr(mcp_server, "PROJECT_ID", "e2e-project")
    monkeypatch.setattr(mcp_server, "_auth_type", "api_key")
    monkeypatch.setattr(mcp_server, "_auth_token", "rlm_e2e_key")
    monkeypatch.setattr(mcp_server, "API_KEY", "")
    monkeypatch.setenv("SNIPARA_TOOL_PROFILE", "full")

    async def run_calls() -> tuple[set[str], Any, Any, Any, Any]:
        tools = {tool.name for tool in await mcp_server.list_tools()}
        context = await mcp_server.call_tool(
            "snipara_context_query", {"query": "endpoint contract", "include_metadata": True}
        )
        remember = await mcp_server.call_tool(
            "snipara_remember_if_novel",
            {"text": "The SDK prefers the hosted MCP endpoint.", "type": "learning"},
        )
        health = await mcp_server.call_tool("snipara_memory_health", {})
        htask = await mcp_server.call_tool("snipara_htask_get", {"task_id": "task-e2e"})
        return tools, context, remember, health, htask

    tools, context, remember, health, htask = asyncio.run(run_calls())
    assert {
        "snipara_context_query",
        "snipara_remember_if_novel",
        "snipara_memory_health",
        "snipara_htask_get",
    }.issubset(tools)
    assert "rlm_context_query" not in tools

    assert "SDK Endpoint Contract" in context[0].text
    assert "Context for endpoint contract" in context[0].text
    assert "**Memory stored**" in remember[0].text
    assert "mem_e2e" in remember[0].text
    assert '"status": "healthy"' in health[0].text
    assert '"orphaned_memories": 0' in health[0].text
    assert '"task_id": "task-e2e"' in htask[0].text

    assert [request["body"]["tool"] for request in backend.requests] == [
        "rlm_context_query",
        "rlm_remember_if_novel",
        "rlm_memory_health",
        "rlm_htask_get",
    ]
    assert all(request["path"] == "/v1/e2e-project/mcp" for request in backend.requests)
    assert all(request["headers"]["x-api-key"] == "rlm_e2e_key" for request in backend.requests)


def _context_backend(monkeypatch, payload: dict[str, Any]) -> LocalMcpBackend:
    backend = LocalMcpBackend(payload)
    _install_mock_transport(monkeypatch, backend)
    _disable_bootstrap(monkeypatch)
    monkeypatch.setattr(mcp_server, "API_URL", "https://fixture.snipara.test")
    monkeypatch.setattr(mcp_server, "PROJECT_ID", "e2e-project")
    monkeypatch.setattr(mcp_server, "_auth_type", "api_key")
    monkeypatch.setattr(mcp_server, "_auth_token", "rlm_e2e_key")
    monkeypatch.setattr(mcp_server, "API_KEY", "")
    return backend


@pytest.mark.parametrize("name", ["snipara_context_query", "rlm_context_query"])
@pytest.mark.parametrize("metadata", [None, False])
@pytest.mark.parametrize("auto", [None, False, True])
def test_compact_context_preserves_entire_payload_and_separate_session_context(monkeypatch, name, metadata, auto):
    payload = {
        "sections": [{
            "title": "Équipe policy", "file": "policy.md", "lines": [2, 7],
            "content": "No permission to act; 12 per item, not per batch.", "evidence_id": "e-1",
            "quality_flags": ["stale_source", "incomplete"], "truncated": True,
            "quality_provenance": {"method": "indexed"},
        }],
        "section_refs": [{"chunk_id": "opaque-1", "preview": "read full source", "lines": [8, 9]}],
        "answer_pack": {"facts": [], "caveats": ["conflict unresolved"]},
        "system_instructions": "Tenant rule: keep private records confidential.",
        "timing": {"total_ms": 4}, "routing_reason": "source read required",
        "retrieval_diagnostics": {
            "low_confidence": True, "stale_source_count": 1,
            "source_conflict": {"status": "conflicting", "sources": ["e-1", "e-2"]},
            "retrieval_plan": {"facets": [{"query": "exceptions", "supported": False}]},
            "recommendations": ["Do not infer missing exceptions"],
        },
        "recovery_guidance": ["Read source before answering"],
        "recommended_tool": "snipara_get_chunk", "recommended_tool_arguments": {"chunk_id": "opaque-1"},
        "future_warning": {"authority": "unverified", "nested": ["preserve"]},
    }
    before = deepcopy(payload)
    backend = _context_backend(monkeypatch, payload)
    session = "Existing decision: do not claim execution proof.\nÉquipe context."
    monkeypatch.setattr(mcp_server, "_session_context", session)
    arguments = {
        "query": "policy limits", "include_answer_pack": True, "include_shared_context": False,
        "retrieval_queries": ["limits", "counterevidence"],
        "correlation_context": {"session_id": "e2e-session"},
    }
    if metadata is not None:
        arguments["include_metadata"] = metadata
    if auto is not None:
        arguments["auto_decompose"] = auto
    original = deepcopy(arguments)

    response = asyncio.run(mcp_server.call_tool(name, arguments))

    assert len(response) == 2
    assert response[0].text == json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str)
    assert json.loads(response[0].text) == before
    assert response[1].text == f"## Session Context\n{session}"
    assert payload == before
    assert arguments == original
    sent = backend.requests[0]["body"]
    assert sent["tool"] == "rlm_context_query"
    assert sent["params"]["include_metadata"] is False
    assert sent["params"]["auto_decompose"] is (auto if auto is not None else False)
    for key in ("include_answer_pack", "include_shared_context", "retrieval_queries", "correlation_context"):
        assert sent["params"][key] == arguments[key]
    assert sent["params"]["query"] == "policy limits"
    assert session not in sent["params"]["query"]


def test_compact_empty_sources_retains_conflict_recovery_and_unknowns(monkeypatch):
    payload = {
        "sections": [], "section_refs": [], "answer_pack": None,
        "retrieval_diagnostics": {"status": "empty", "source_conflict": {"status": "unknown"}},
        "recovery_guidance": ["No supporting project source was found"],
        "fast_context_parameters": {"max_tokens": 800, "return_references": True},
        "future_warning": "missing required source",
    }
    backend = _context_backend(monkeypatch, payload)
    response = asyncio.run(mcp_server.call_tool("snipara_context_query", {"query": "policy"}))
    assert len(response) == 1
    assert json.loads(response[0].text) == payload
    assert backend.requests[0]["body"]["params"]["include_answer_pack"] is False
    assert "include_shared_context" not in backend.requests[0]["body"]["params"]


@pytest.mark.parametrize("references", [False, True])
def test_explicit_full_context_keeps_legacy_formatted_response_exactly(monkeypatch, references):
    payload = {
        "sections": [] if references else [{
            "title": "Policy", "file": "policy.md", "relevance_score": 0.8, "content": "Facts.",
        }],
        "section_refs": [{
            "title": "Policy", "file": "policy.md", "lines": [2, 7], "relevance_score": 0.8,
            "chunk_id": "opaque-1", "preview": "Facts preview.",
        }] if references else [],
        "system_instructions": "Tenant policy.", "total_tokens": 42,
    }
    backend = _context_backend(monkeypatch, payload)
    monkeypatch.setattr(mcp_server, "_session_context", "Active decision.")
    response = asyncio.run(mcp_server.call_tool(
        "snipara_context_query", {"query": "policy", "include_metadata": True}
    ))
    expected = "Tenant policy.\n## Session Context\nActive decision.\n\n"
    if references:
        expected += (
            "## Relevant Documentation References\n\n### Policy\n"
            "*policy.md | Lines: [2, 7] | Score: 0.80*\nChunk: `opaque-1`\nFacts preview.\n\n"
            "---\n*1 references, 42 preview tokens*"
        )
    else:
        expected += (
            "## Relevant Documentation\n\n### Policy\n*policy.md | Score: 0.80*\n\n"
            "Facts.\n\n---\n*1 sections, 42 tokens*"
        )
    assert len(response) == 1
    assert response[0].text == expected
    sent = backend.requests[0]["body"]["params"]
    assert sent["include_metadata"] is True
    assert sent["auto_decompose"] is True
    assert "include_answer_pack" not in sent
    assert "include_shared_context" not in sent


@pytest.mark.parametrize("flag", ["include_metadata", "include_answer_pack", "include_shared_context", "auto_decompose"])
def test_context_call_rejects_non_boolean_controls_without_query_http(monkeypatch, flag):
    backend = _context_backend(monkeypatch, {})
    response = asyncio.run(mcp_server.call_tool("snipara_context_query", {"query": "policy", flag: "false"}))
    assert response[0].text == f"**Error:** ValueError: {flag} must be a boolean"
    assert backend.requests == []


def test_compact_context_keeps_existing_error_and_timeout_recovery_paths(monkeypatch):
    backend = _context_backend(monkeypatch, {})
    calls = []

    async def failing_api(tool, params, *, timeout):
        calls.append((tool, params, timeout))
        if len(calls) == 1:
            raise httpx.ReadTimeout("primary timeout")
        return {"success": False, "error": "source access denied"}

    monkeypatch.setattr(mcp_server, "call_api", failing_api)
    response = asyncio.run(mcp_server.call_tool("snipara_context_query", {"query": "policy limits"}))
    assert response[0].text == "**Error:** source access denied"
    assert len(calls) == 2
    assert calls[0][2] == mcp_server.CONTEXT_QUERY_PRIMARY_TIMEOUT_SECONDS
    assert calls[1][2] == mcp_server.CONTEXT_QUERY_FAST_RETRY_TIMEOUT_SECONDS
    assert calls[1][1]["return_references"] is True
    assert calls[1][1]["include_metadata"] is False
    assert calls[1][1]["include_answer_pack"] is False
    assert backend.requests == []


def test_compact_fast_retry_preserves_recovery_details_and_success_data(monkeypatch):
    _context_backend(monkeypatch, {})
    calls = []
    payload = {"section_refs": [], "future_warning": "read before acting", "recovery_guidance": ["narrow query"]}
    before = deepcopy(payload)

    async def retrying_api(tool, params, *, timeout):
        calls.append(params)
        if len(calls) == 1:
            raise httpx.ReadTimeout("primary timeout")
        return {"success": True, "result": payload}

    monkeypatch.setattr(mcp_server, "call_api", retrying_api)
    response = asyncio.run(mcp_server.call_tool("rlm_context_query", {"query": "policy limits"}))
    data = json.loads(response[0].text)
    assert data["query_fallback_used"] is True
    assert data["query_fallback_reason"] == "primary_timeout"
    assert data["fast_context_parameters"] == calls[1]
    assert data["future_warning"] == "read before acting"
    assert data["recovery_guidance"][1:] == ["narrow query"]
    assert payload == before


def test_snipara_client_endpoint_contract_prefers_hosted_mcp_and_falls_back(
    monkeypatch,
) -> None:
    """SDK transport should target /v1/{project}/mcp before legacy /api/mcp/{project}."""
    backend = LocalMcpBackend()
    original_async_client = httpx.AsyncClient
    transport = httpx.MockTransport(backend)

    def async_client_factory(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
        kwargs["transport"] = transport
        return original_async_client(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", async_client_factory)
    client = SniparaClient(
        api_key="rlm_sdk_key",
        project_slug="e2e-project",
        api_url="https://fixture.snipara.test",
    )

    result = asyncio.run(client.call_tool("rlm_memory_health", {}))

    assert result == {"status": "healthy", "orphaned_memories": 0}
    assert [request["path"] for request in backend.requests] == ["/v1/e2e-project/mcp"]
    assert backend.requests[0]["headers"]["x-api-key"] == "rlm_sdk_key"

    backend_404_first = LocalMcpBackend()
    first_call = True

    def fallback_backend(request: httpx.Request) -> httpx.Response:
        nonlocal first_call
        if first_call:
            first_call = False
            backend_404_first.requests.append({"path": request.url.path})
            return httpx.Response(404, json={"success": False, "error": "not found"})
        return backend_404_first(request)

    transport = httpx.MockTransport(fallback_backend)
    fallback_client = SniparaClient(
        api_key="rlm_sdk_key",
        project_slug="e2e-project",
        api_url="https://fixture.snipara.test",
    )

    fallback_result = asyncio.run(
        fallback_client.call_tool("rlm_htask_get", {"task_id": "task-e2e"})
    )

    assert fallback_result["task_id"] == "task-e2e"
    assert [request["path"] for request in backend_404_first.requests] == [
        "/v1/e2e-project/mcp",
        "/api/mcp/e2e-project",
    ]
