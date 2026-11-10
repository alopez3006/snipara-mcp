"""Stdio retrieval must preserve file selection and inherited retirement labels."""

from copy import deepcopy

import pytest

from snipara_mcp import server as server_module


AUTHORITY = {
    "status": "RETIRED",
    "reason": "Historical deployment instructions",
    "replacement": "deploy/ovh/README.md",
}


@pytest.fixture(autouse=True)
def isolated_session(monkeypatch):
    async def no_bootstrap():
        pass

    monkeypatch.setattr(server_module, "ensure_session_bootstrap", no_bootstrap)
    monkeypatch.setattr(server_module, "_session_context", "")


@pytest.mark.asyncio
@pytest.mark.parametrize("arguments", [
    {},
    {"file_path": "retired/child.md"},
    {"file": "retired/child.md", "start_line": 2},
    {"path": "retired/child.md", "end_line": 8},
    {"document": "retired/child.md", "start_line": 2, "end_line": 8,
     "correlation_context": {"session_id": "read-fixture"}},
])
async def test_read_forwards_optional_file_and_bounds_without_losing_authority(monkeypatch, arguments):
    captured = {}
    before = deepcopy(arguments)

    async def fake_api(name, params):
        captured.update(name=name, params=params)
        return {"success": True, "result": {
            "file_path": "retired/child.md", "start_line": 1, "end_line": 3,
            "content": "Child content without a retirement heading.",
            "source_authority": AUTHORITY,
        }}

    monkeypatch.setattr(server_module, "call_api", fake_api)
    response = await server_module.call_tool("snipara_read", arguments)
    assert captured == {"name": "rlm_read", "params": before}
    assert arguments == before
    text = response[0].text
    assert "Child content" in text
    assert '"start_line": 1' in text
    assert '"end_line": 3' in text
    for value in AUTHORITY.values():
        assert value in text


@pytest.mark.asyncio
@pytest.mark.parametrize("metadata", [False, True])
@pytest.mark.parametrize("references", [False, True])
async def test_context_modes_keep_inherited_authority(monkeypatch, metadata, references):
    row = {"title": "Child", "file": "retired/child.md", "content": "Child body",
           "preview": "Child preview", "chunk_id": "child-1", "lines": [1, 3],
           "source_authority": AUTHORITY}
    data = {"sections": [] if references else [row],
            "section_refs": [row] if references else [], "total_tokens": 10}

    async def settings():
        return {}

    async def query(*args, **kwargs):
        return {"success": True, "result": data}

    monkeypatch.setattr(server_module, "get_project_settings", settings)
    monkeypatch.setattr(server_module, "_call_context_query_with_fast_retry", query)
    response = await server_module.call_tool("snipara_context_query", {
        "query": "historical deployment", "include_metadata": metadata,
        "return_references": references,
    })
    for value in AUTHORITY.values():
        assert value in response[0].text


@pytest.mark.asyncio
@pytest.mark.parametrize("name,data", [
    ("snipara_get_chunk", {"content": "Child body", "source_authority": AUTHORITY}),
    ("snipara_ask", {"sections": [{"content": "Child body", "source_authority": AUTHORITY}]}),
    ("snipara_search", {"matches": [{"content": "Child body", "source_authority": AUTHORITY}]}),
    ("snipara_multi_query", {"results": [{"sections": [{"source_authority": AUTHORITY}]}]}),
])
async def test_other_retrieval_formatters_keep_authority(monkeypatch, name, data):
    async def fake_api(tool, arguments):
        return {"success": True, "result": data}

    monkeypatch.setattr(server_module, "call_api", fake_api)
    response = await server_module.call_tool(name, {
        "query": "historical deployment", "pattern": "deployment", "queries": ["deployment"],
        "chunk_id": "child-1",
    })
    for value in AUTHORITY.values():
        assert value in response[0].text


@pytest.mark.asyncio
async def test_read_preserves_document_not_found_error(monkeypatch):
    async def fake_api(name, arguments):
        return {"success": True, "result": {
            "error": "Document not found: missing.md", "candidates": ["current.md"],
        }}

    monkeypatch.setattr(server_module, "call_api", fake_api)
    response = await server_module.call_tool("snipara_read", {"file_path": "missing.md"})
    assert "Document not found: missing.md" in response[0].text
    assert "current.md" in response[0].text
