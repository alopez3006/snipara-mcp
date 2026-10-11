"""New plans are opt-in; older hosted payloads remain unchanged."""

from snipara_mcp.server import _build_context_query_payload
from snipara_mcp.tool_contract import TOOL_DEFINITION_BY_NAME


def test_client_forwards_optional_plan_without_adding_legacy_field():
    original = _build_context_query_payload({}, {}, query="inspection")
    assert "retrieval_queries" not in original
    planned = _build_context_query_payload(
        {"retrieval_queries": ["traceability lot"]}, {}, query="inspection"
    )
    assert planned == {**original, "retrieval_queries": ["traceability lot"]}


def test_public_contract_advertises_bounded_plan():
    schema = TOOL_DEFINITION_BY_NAME["snipara_context_query"]["inputSchema"]["properties"][
        "retrieval_queries"
    ]
    assert schema["maxItems"] == 4
    assert schema["items"]["type"] == "string"
