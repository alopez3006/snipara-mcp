"""Package-local regression tests for snipara-mcp."""

from contextlib import asynccontextmanager
import json
from pathlib import Path
import sys
import types

import pytest
from typer.testing import CliRunner

import snipara_mcp
import snipara_mcp.auth as mcp_auth
import snipara_mcp.server as mcp_server
from snipara_mcp.cli import app
from snipara_mcp.tool_contract import DEFAULT_AGENT_TOOL_DEFINITIONS, MCP_TOOL_DEFINITIONS


def _package_version_from_pyproject() -> str:
    import tomllib

    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    return data["project"]["version"]


def test_package_version_matches_pyproject() -> None:
    """The installed package should report the same version as pyproject.toml."""
    assert snipara_mcp.__version__ == _package_version_from_pyproject()


def test_glama_metadata_claims_public_repository() -> None:
    """The generated public mirror should carry valid Glama ownership metadata."""
    glama_path = Path(__file__).resolve().parents[1] / "glama.json"
    metadata = json.loads(glama_path.read_text(encoding="utf-8"))

    assert metadata == {
        "$schema": "https://glama.ai/mcp/schemas/server.json",
        "maintainers": ["alopez3006"],
    }


def test_cli_version_reports_package_version() -> None:
    """The CLI version command should reuse the package version."""
    runner = CliRunner()

    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert f"Snipara CLI v{snipara_mcp.__version__}" in result.stdout
    assert f"snipara-mcp: {snipara_mcp.__version__}" in result.stdout


def test_cli_tools_list_renders_tool_names(monkeypatch) -> None:
    """The generic tools list command should surface the hosted tool inventory."""
    runner = CliRunner()

    async def fake_call_mcp_jsonrpc(api_url, project_slug, auth_header, method, params):
        assert method == "tools/list"
        assert project_slug == "snipara"
        return {
            "result": {
                "tools": [
                    {"name": "snipara_help", "description": "Recommend the right tool for a task."},
                    {
                        "name": "snipara_session_memories",
                        "description": "Load tiered session memories.",
                    },
                ]
            }
        }

    monkeypatch.setattr("snipara_mcp.cli.load_auth_header", lambda: "rlm_test")
    monkeypatch.setattr("snipara_mcp.cli.call_mcp_jsonrpc", fake_call_mcp_jsonrpc)

    result = runner.invoke(app, ["tools", "list", "--slug", "snipara"])

    assert result.exit_code == 0
    assert "Available MCP tools: 2" in result.stdout
    assert "snipara_help" in result.stdout
    assert "snipara_session_memories" in result.stdout


def test_cli_tools_call_decodes_json_text_payload(monkeypatch) -> None:
    """The generic tools call command should pretty-print decoded JSON text payloads."""
    runner = CliRunner()

    async def fake_call_mcp_tool(api_url, project_slug, auth_header, tool_name, arguments):
        assert tool_name == "rlm_help"
        assert arguments == {"query": "session automation"}
        return {
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": '{"recommended_tools":["rlm_session_memories","rlm_remember_if_novel"]}',
                    }
                ]
            }
        }

    monkeypatch.setattr("snipara_mcp.cli.load_auth_header", lambda: "rlm_test")
    monkeypatch.setattr("snipara_mcp.cli.call_mcp_tool", fake_call_mcp_tool)

    result = runner.invoke(
        app,
        [
            "tools",
            "call",
            "rlm_help",
            "--slug",
            "snipara",
            "--args",
            '{"query":"session automation"}',
        ],
    )

    assert result.exit_code == 0
    assert '"recommended_tools"' in result.stdout
    assert "rlm_session_memories" in result.stdout


async def test_list_tools_defaults_to_generated_agent_contract(monkeypatch) -> None:
    """Default stdio discovery should match the hosted lean agent contract."""
    monkeypatch.delenv("SNIPARA_TOOL_PROFILE", raising=False)
    listed_tools = {tool.name: tool.inputSchema for tool in await mcp_server.list_tools()}
    contract_tools = {
        tool["name"]: tool["inputSchema"] for tool in DEFAULT_AGENT_TOOL_DEFINITIONS
    }

    assert listed_tools == contract_tools
    assert len(listed_tools) <= 13
    assert all(name.startswith("snipara_") for name in listed_tools)


async def test_list_tools_supports_explicit_full_compatibility_profile(monkeypatch) -> None:
    """Advanced clients may opt into every generated public tool definition."""
    monkeypatch.setenv("SNIPARA_TOOL_PROFILE", "full")

    listed_tools = {tool.name: tool.inputSchema for tool in await mcp_server.list_tools()}
    contract_tools = {tool["name"]: tool["inputSchema"] for tool in MCP_TOOL_DEFINITIONS}

    assert listed_tools == contract_tools
    assert len(listed_tools) > len(DEFAULT_AGENT_TOOL_DEFINITIONS)


@pytest.mark.asyncio
async def test_run_server_allows_unauthenticated_mcp_discovery(monkeypatch) -> None:
    """Registries must reach initialize/tools/list without project credentials."""
    run_calls = []

    monkeypatch.setattr(mcp_server, "_load_auth", lambda: (None, "none", None))
    monkeypatch.delenv("SNIPARA_API_KEY", raising=False)
    monkeypatch.delenv("SNIPARA_PROJECT_ID", raising=False)
    monkeypatch.delenv("SNIPARA_PROJECT_SLUG", raising=False)

    @asynccontextmanager
    async def fake_stdio_server():
        yield "read-stream", "write-stream"

    async def fake_run(read_stream, write_stream, initialization_options):
        run_calls.append((read_stream, write_stream, initialization_options))

    monkeypatch.setattr(mcp_server, "stdio_server", fake_stdio_server)
    monkeypatch.setattr(mcp_server.server, "run", fake_run)

    await mcp_server.run_server()

    assert len(run_calls) == 1
    assert run_calls[0][:2] == ("read-stream", "write-stream")


@pytest.mark.asyncio
async def test_tool_calls_fail_closed_without_authentication(monkeypatch) -> None:
    """Public schema discovery must never make unauthenticated tools callable."""
    bootstrap_called = False

    async def unexpected_bootstrap():
        nonlocal bootstrap_called
        bootstrap_called = True

    monkeypatch.setattr(mcp_server, "_auth_token", None)
    monkeypatch.setattr(mcp_server, "_auth_type", "none")
    monkeypatch.setattr(mcp_server, "API_KEY", "")
    monkeypatch.setattr(mcp_server, "PROJECT_ID", "")
    monkeypatch.setattr(mcp_server, "ensure_session_bootstrap", unexpected_bootstrap)

    result = await mcp_server.call_tool(
        "snipara_context_query",
        {"query": "authentication contract"},
    )

    assert bootstrap_called is False
    assert "Authentication required" in result[0].text
    assert "SNIPARA_API_KEY" in result[0].text


@pytest.mark.asyncio
async def test_tool_calls_require_project_after_authentication(monkeypatch) -> None:
    """A credential without a project may inspect schemas but may not execute tools."""
    monkeypatch.setattr(mcp_server, "_auth_token", "rlm_test_key")
    monkeypatch.setattr(mcp_server, "_auth_type", "api_key")
    monkeypatch.setattr(mcp_server, "API_KEY", "")
    monkeypatch.setattr(mcp_server, "PROJECT_ID", "")

    result = await mcp_server.call_tool("snipara_stats", {})

    assert "Project selection required" in result[0].text
    assert "SNIPARA_PROJECT_SLUG" in result[0].text


def test_generated_contract_exposes_agent_context_surface() -> None:
    """The static Codex/stdio wrapper contract must track hosted agent context tools."""
    contract_tools = {tool["name"]: tool for tool in MCP_TOOL_DEFINITIONS}

    context_schema = contract_tools["snipara_context_query"]["inputSchema"]
    context_props = context_schema["properties"]
    help_props = contract_tools["snipara_help"]["inputSchema"]["properties"]

    assert "include_answer_pack" in context_props
    assert context_props["include_answer_pack"]["default"] is True
    assert "list_all" in help_props
    assert help_props["list_all"]["default"] is False
    assert "snipara_code_symbol_card" in contract_tools
    assert "snipara_code_impact" in contract_tools
    assert "snipara_decision_review_queue" in contract_tools
    assert "snipara_decision_review_plan" in contract_tools
    review_apply = contract_tools["snipara_decision_review_apply"]
    assert review_apply["inputSchema"]["required"] == ["review_plan_id", "reason", "actions"]
    assert review_apply["annotations"]["destructiveHint"] is True


def test_generated_contract_exposes_bounded_retrieval_correlation() -> None:
    """The packaged stdio contract must match hosted retrieval correlation inputs."""
    contract_tools = {tool["name"]: tool for tool in MCP_TOOL_DEFINITIONS}

    for tool_name in (
        "snipara_context_query",
        "snipara_ask",
        "snipara_search",
        "snipara_recall",
        "snipara_get_chunk",
    ):
        schema = contract_tools[tool_name]["inputSchema"]["properties"]["correlation_context"]
        assert schema["additionalProperties"] is False
        assert schema["properties"]["version"]["enum"] == ["retrieval-correlation-v1"]
        assert schema["properties"]["session_id"]["maxLength"] == 128
        assert "project_id" not in schema["properties"]


async def test_upload_document_forwards_metadata(monkeypatch) -> None:
    """Single-file stdio uploads should preserve document metadata fields."""
    calls = []

    async def fake_call_api(tool, params):
        calls.append((tool, params))
        return {
            "success": True,
            "result": {
                "action": "metadata_updated",
                "path": params["path"],
                "size": len(params["content"]),
            },
        }

    monkeypatch.setattr(mcp_server, "call_api", fake_call_api)

    await mcp_server.call_tool(
        "rlm_upload_document",
        {
            "path": "clients/acme/current.md",
            "content": "# Current",
            "kind": "DOC",
            "format": "md",
            "language": "markdown",
            "metadata": {"assetClass": "BUSINESS_DOCUMENT", "usageMode": "current_truth"},
        },
    )

    assert calls[-1] == (
        "rlm_upload_document",
        {
            "path": "clients/acme/current.md",
            "content": "# Current",
            "kind": "DOC",
            "format": "md",
            "language": "markdown",
            "metadata": {"assetClass": "BUSINESS_DOCUMENT", "usageMode": "current_truth"},
        },
    )


async def test_document_tombstones_forwards_params(monkeypatch) -> None:
    """The packaged stdio server should forward document tombstone params verbatim."""
    calls = []

    async def fake_call_api(tool, params):
        calls.append((tool, params))
        return {
            "success": True,
            "result": {
                "tombstones": [],
                "returned": 0,
                "total": 0,
                "active": 0,
                "expired": 0,
                "retention_days": 30,
                "message": "No document tombstones found for this project",
            },
        }

    monkeypatch.setattr(mcp_server, "call_api", fake_call_api)

    await mcp_server.call_tool(
        "rlm_document_tombstones",
        {"limit": 10, "include_expired": True},
    )

    assert calls[-1] == (
        "rlm_document_tombstones",
        {"limit": 10, "include_expired": True},
    )


def _clear_auth_env(monkeypatch) -> None:
    for key in (
        "SNIPARA_IGNORE_OAUTH",
        "SNIPARA_PROJECT_ID",
        "SNIPARA_PROJECT_SLUG",
        "SNIPARA_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)


def _stub_empty_sdk_config(monkeypatch) -> None:
    package = types.ModuleType("snipara")
    package.__path__ = []  # type: ignore[attr-defined]
    config_module = types.ModuleType("snipara.config")
    config_module.load_config = lambda: types.SimpleNamespace(
        project=types.SimpleNamespace(api_key="", slug="")
    )
    monkeypatch.setitem(sys.modules, "snipara", package)
    monkeypatch.setitem(sys.modules, "snipara.config", config_module)


def test_load_auth_uses_matching_workspace_oauth_token(monkeypatch) -> None:
    """An explicit workspace slug should select the matching OAuth token only."""
    _clear_auth_env(monkeypatch)
    _stub_empty_sdk_config(monkeypatch)
    monkeypatch.setenv("SNIPARA_PROJECT_SLUG", "snipara")
    monkeypatch.setattr(
        mcp_auth,
        "load_tokens",
        lambda: {
            "proj-vutler": {
                "access_token": "snipara_at_vutler",
                "project_slug": "vutler",
            },
            "proj-snipara": {
                "access_token": "snipara_at_snipara",
                "project_slug": "snipara",
            },
        },
    )

    token, auth_type, project_id = mcp_server._load_auth()

    assert token == "snipara_at_snipara"
    assert auth_type == "oauth"
    assert project_id == "snipara"


def test_load_auth_does_not_fallback_to_other_project_when_workspace_is_explicit(
    monkeypatch,
) -> None:
    """An explicit workspace should never silently borrow another project's token."""
    _clear_auth_env(monkeypatch)
    _stub_empty_sdk_config(monkeypatch)
    monkeypatch.setenv("SNIPARA_PROJECT_SLUG", "snipara")
    monkeypatch.setattr(
        mcp_auth,
        "load_tokens",
        lambda: {
            "proj-vutler": {
                "access_token": "snipara_at_vutler",
                "project_slug": "vutler",
            }
        },
    )

    token, auth_type, project_id = mcp_server._load_auth()

    assert token is None
    assert auth_type == "none"
    assert project_id == "snipara"


def test_load_auth_uses_env_api_key_after_explicit_project_miss(monkeypatch) -> None:
    """Explicit workspaces should fall back to env auth, not another token."""
    _clear_auth_env(monkeypatch)
    _stub_empty_sdk_config(monkeypatch)
    monkeypatch.setenv("SNIPARA_PROJECT_SLUG", "snipara")
    monkeypatch.setenv("SNIPARA_API_KEY", "rlm_pk_env")
    monkeypatch.setattr(
        mcp_auth,
        "load_tokens",
        lambda: {
            "proj-vutler": {
                "access_token": "snipara_at_vutler",
                "project_slug": "vutler",
            }
        },
    )

    token, auth_type, project_id = mcp_server._load_auth()

    assert token == "rlm_pk_env"
    assert auth_type == "api_key"
    assert project_id == "snipara"


def test_load_auth_prefers_project_api_key_for_legacy_v1_routes(monkeypatch) -> None:
    """Stored API keys should win over bearer tokens for legacy /v1 project calls."""
    _clear_auth_env(monkeypatch)
    _stub_empty_sdk_config(monkeypatch)
    monkeypatch.setenv("SNIPARA_PROJECT_SLUG", "snipara")
    monkeypatch.setattr(
        mcp_auth,
        "load_tokens",
        lambda: {
            "proj-snipara": {
                "access_token": "snipara_at_snipara",
                "api_key": "rlm_pk_snipara",
                "project_slug": "snipara",
            }
        },
    )

    token, auth_type, project_id = mcp_server._load_auth()

    assert token == "rlm_pk_snipara"
    assert auth_type == "api_key"
    assert project_id == "snipara"


def test_get_headers_uses_auth_type_specific_header(monkeypatch) -> None:
    """Legacy project calls should emit the header that matches the selected auth type."""
    monkeypatch.setattr(mcp_server, "_auth_token", "snipara_at_snipara")
    monkeypatch.setattr(mcp_server, "_auth_type", "oauth")
    monkeypatch.setattr(mcp_server, "API_KEY", "")

    oauth_headers = mcp_server.get_headers()

    assert oauth_headers["Authorization"] == "Bearer snipara_at_snipara"
    assert "X-API-Key" not in oauth_headers

    monkeypatch.setattr(mcp_server, "_auth_token", "rlm_pk_snipara")
    monkeypatch.setattr(mcp_server, "_auth_type", "api_key")

    api_key_headers = mcp_server.get_headers()

    assert api_key_headers["X-API-Key"] == "rlm_pk_snipara"
    assert "Authorization" not in api_key_headers
