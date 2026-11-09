"""Retrieval facets and compact context controls preserve explicit caller choices."""

from copy import deepcopy

import pytest

from snipara_mcp.server import _build_context_query_payload, _build_fast_context_query_payload
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


@pytest.mark.parametrize("metadata", [None, False, True])
@pytest.mark.parametrize("answer_pack", [None, False, True])
@pytest.mark.parametrize("shared", [None, False, True])
def test_context_controls_matrix_preserves_defaults_explicit_choices_and_input(metadata, answer_pack, shared):
    arguments = {
        "max_tokens": 1800, "search_mode": "semantic", "return_references": True,
        "retrieval_queries": ["limits", "counterevidence"],
        "correlation_context": {"session_id": "caller-session"},
    }
    for key, value in (
        ("include_metadata", metadata), ("include_answer_pack", answer_pack),
        ("include_shared_context", shared),
    ):
        if value is not None:
            arguments[key] = value
    before = deepcopy(arguments)
    payload = _build_context_query_payload(arguments, {}, query="inspection")

    assert payload["include_metadata"] is (metadata is True)
    assert payload["auto_decompose"] is (metadata is True)
    if answer_pack is None and metadata is True:
        assert "include_answer_pack" not in payload
    else:
        assert payload["include_answer_pack"] is (answer_pack is True)
    if shared is None:
        assert "include_shared_context" not in payload
    else:
        assert payload["include_shared_context"] is shared
    assert payload["max_tokens"] == 1800
    assert payload["search_mode"] == "semantic"
    assert payload["return_references"] is True
    assert payload["retrieval_queries"] == arguments["retrieval_queries"]
    assert payload["correlation_context"] == arguments["correlation_context"]
    assert arguments == before


def test_explicit_full_payload_matches_legacy_builder_without_new_defaults():
    assert _build_context_query_payload({"include_metadata": True}, {}, query="inspection") == {
        "query": "inspection", "max_tokens": 4000, "search_mode": "hybrid",
        "include_metadata": True, "prefer_summaries": True, "return_references": False,
        "auto_decompose": True, "include_all_tiers": False,
    }


@pytest.mark.parametrize("flag", ["include_metadata", "include_answer_pack", "include_shared_context", "auto_decompose"])
@pytest.mark.parametrize("value", [None, "false", "true", 0, 1, [], {}])
def test_context_controls_reject_non_boolean_values(flag, value):
    with pytest.raises(ValueError, match=f"{flag} must be a boolean"):
        _build_context_query_payload({flag: value}, {}, query="inspection")


@pytest.mark.parametrize("metadata", [None, False, True])
@pytest.mark.parametrize("auto", [None, False, True])
def test_auto_decompose_defaults_follow_response_mode_without_overriding_explicit_choice(metadata, auto):
    arguments = {}
    if metadata is not None:
        arguments["include_metadata"] = metadata
    if auto is not None:
        arguments["auto_decompose"] = auto
    before = deepcopy(arguments)
    payload = _build_context_query_payload(arguments, {}, query="inspection")
    assert payload["auto_decompose"] is (auto if auto is not None else metadata is True)
    assert arguments == before


def test_fast_retry_keeps_explicit_context_controls_facets_and_correlation():
    arguments = {
        "include_metadata": False, "include_answer_pack": True, "include_shared_context": False,
        "max_tokens": 3000, "retrieval_queries": ["limits", "counterevidence"],
        "correlation_context": {"session_id": "retry-session"},
    }
    before = deepcopy(arguments)
    payload = _build_fast_context_query_payload(arguments, {}, query="How do limits work?")
    for key in (
        "include_metadata", "include_answer_pack", "include_shared_context",
        "retrieval_queries", "correlation_context",
    ):
        assert payload[key] == arguments[key]
    assert payload["max_tokens"] == 1200
    assert payload["search_mode"] == "keyword"
    assert payload["return_references"] is True
    assert payload["auto_decompose"] is False
    assert payload["include_all_tiers"] is False
    assert arguments == before
