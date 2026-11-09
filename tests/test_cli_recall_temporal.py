"""Actual CLI recall regressions for protected historical intent; no network."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
from typer.testing import CliRunner

from snipara_mcp import cli


CUTOFF = "2026-10-25T10:00:00Z"
REJECTED_MEMORY = "UNCONFIRMED_CURRENT_MEMORY_SENTINEL"


def _invoke_recall_response(
    monkeypatch: pytest.MonkeyPatch,
    response_body: Any,
    controls: list[str],
) -> tuple[Any, list[dict[str, Any]]]:
    calls: list[dict[str, Any]] = []

    class FakeAsyncClient:
        def __init__(self, **_kwargs: Any) -> None:
            pass

        async def __aenter__(self) -> "FakeAsyncClient":
            return self

        async def __aexit__(self, *_args: Any) -> None:
            return None

        async def post(
            self,
            url: str,
            *,
            headers: dict[str, str],
            json: dict[str, Any],
        ) -> httpx.Response:
            assert url == "https://offline.invalid/mcp/recall-test"
            assert headers["X-API-Key"] == "synthetic-cli-test-key"
            calls.append(json)
            return httpx.Response(200, json=response_body)

    monkeypatch.setenv("SNIPARA_API_KEY", "synthetic-cli-test-key")
    monkeypatch.setenv("SNIPARA_API_URL", "https://offline.invalid")
    monkeypatch.setattr(cli.httpx, "AsyncClient", FakeAsyncClient)
    result = CliRunner().invoke(cli.app, ["recall", "probe", "--slug", "recall-test", *controls])
    assert len(calls) == 1
    assert calls[0]["params"]["name"] == "rlm_recall"
    return result, calls


def _invoke_recall(monkeypatch, raw_text: str, controls: list[str]):
    return _invoke_recall_response(
        monkeypatch,
        {"result": {"content": [{"type": "text", "text": raw_text}]}},
        controls,
    )


def _confirmed_text(memories: list[dict[str, Any]]) -> dict[str, str]:
    return {
        "type": "text",
        "text": json.dumps({
            "memories": memories,
            "temporal_context": {
                "contract": "snipara.memory-temporal.v1", "view": "history", "as_of": CUTOFF,
            },
        }),
    }


@pytest.mark.parametrize(
    "temporal_context",
    [
        pytest.param(None, id="missing-confirmation"),
        pytest.param(
            {"contract": "snipara.memory-temporal.v1", "view": "current", "as_of": CUTOFF},
            id="wrong-view",
        ),
        pytest.param(
            {
                "contract": "snipara.memory-temporal.v1",
                "view": "history",
                "as_of": "2026-10-24T10:00:00Z",
            },
            id="wrong-cutoff",
        ),
    ],
)
def test_cli_recall_refuses_unconfirmed_history(monkeypatch, temporal_context) -> None:
    payload = {"memories": [{"text": REJECTED_MEMORY, "relevance": 0.9}]}
    if temporal_context is not None:
        payload["temporal_context"] = temporal_context
    result, calls = _invoke_recall(
        monkeypatch,
        json.dumps(payload),
        ["--memory-view", "history", "--as-of", CUTOFF],
    )
    assert result.exit_code == 1
    assert "Hosted server did not confirm" in result.output
    assert REJECTED_MEMORY not in result.output
    assert "Found " not in result.output
    assert calls[0]["params"]["arguments"] == {
        "query": "probe", "limit": 5, "memory_view": "history", "as_of": CUTOFF,
    }


def test_cli_recall_accepts_confirmed_history(monkeypatch) -> None:
    payload = {
        "memories": [{"type": "fact", "text": "CONFIRMED_HISTORY_SENTINEL", "relevance": 0.9}],
        "temporal_context": {
            "contract": "snipara.memory-temporal.v1", "view": "history", "as_of": CUTOFF,
        },
    }
    result, calls = _invoke_recall(
        monkeypatch,
        json.dumps(payload),
        ["--memory-view", "history", "--as-of", CUTOFF],
    )
    assert result.exit_code == 0
    assert "CONFIRMED_HISTORY_SENTINEL" in result.output
    assert "Retained historical evidence; no current source authority or check reuse." in result.output
    assert calls[0]["params"]["arguments"]["as_of"] == CUTOFF


def test_cli_recall_preserves_default_current_output(monkeypatch) -> None:
    payload = {"memories": [{"type": "fact", "text": "CURRENT_MEMORY_SENTINEL", "relevance": 0.9}]}
    result, calls = _invoke_recall(monkeypatch, json.dumps(payload), [])
    assert result.exit_code == 0
    assert "Found 1 memory(ies)" in result.output
    assert "CURRENT_MEMORY_SENTINEL" in result.output
    assert "Retained historical evidence" not in result.output
    assert calls[0]["params"]["arguments"] == {"query": "probe", "limit": 5}


def test_cli_recall_preserves_unstructured_current_output(monkeypatch) -> None:
    result, _ = _invoke_recall(monkeypatch, "LEGACY_CURRENT_TEXT_SENTINEL", [])
    assert result.exit_code == 0
    assert "LEGACY_CURRENT_TEXT_SENTINEL" in result.output


@pytest.mark.parametrize(
    "raw_text",
    [
        pytest.param("UNCONFIRMED_HISTORY_TEXT_SENTINEL", id="unstructured-text"),
        pytest.param('["UNCONFIRMED_HISTORY_TEXT_SENTINEL"]', id="non-object-json"),
    ],
)
def test_cli_recall_refuses_invalid_history_payload(monkeypatch, raw_text) -> None:
    result, _ = _invoke_recall(monkeypatch, raw_text, ["--memory-view", "history"])
    assert result.exit_code == 1
    assert "Hosted server did not confirm" in result.output
    assert "UNCONFIRMED_HISTORY_TEXT_SENTINEL" not in result.output


@pytest.mark.parametrize(
    "response_body",
    [
        pytest.param({}, id="missing-rpc-result"),
        pytest.param([], id="non-object-envelope"),
        pytest.param({"result": None}, id="non-object-tool-result"),
        pytest.param({"result": {}}, id="missing-content"),
        pytest.param({"result": {"content": []}}, id="empty-content"),
        pytest.param({"result": {"content": {}}}, id="non-list-content"),
        pytest.param({"result": {"content": [None]}}, id="invalid-content-item"),
        pytest.param(
            {"result": {"content": [{"type": "text"}]}}, id="missing-text",
        ),
        pytest.param(
            {"result": {"content": [{"type": "image", "data": REJECTED_MEMORY}]}},
            id="nontext-only",
        ),
        pytest.param({"error": {"message": REJECTED_MEMORY}}, id="rpc-error"),
        pytest.param(
            {"result": {
                "isError": True,
                "content": [_confirmed_text([{"text": REJECTED_MEMORY}])],
            }},
            id="confirmed-payload-with-tool-error",
        ),
        pytest.param(
            {"result": {
                "isError": "true",
                "content": [_confirmed_text([{"text": REJECTED_MEMORY}])],
            }},
            id="malformed-tool-error-flag",
        ),
        pytest.param(
            {
                "error": {"message": REJECTED_MEMORY},
                "result": {"content": [_confirmed_text([{"text": REJECTED_MEMORY}])]},
            },
            id="rpc-error-wins-confirmed-result",
        ),
    ],
)
def test_cli_recall_refuses_unconfirmed_or_error_envelope(monkeypatch, response_body) -> None:
    result, _ = _invoke_recall_response(
        monkeypatch, response_body, ["--memory-view", "history", "--as-of", CUTOFF],
    )
    assert result.exit_code == 1
    assert "Historical recall refused:" in result.output
    assert REJECTED_MEMORY not in result.output
    assert "Found " not in result.output


@pytest.mark.parametrize(
    "later_text",
    [
        pytest.param("UNCONFIRMED_LATER_TEXT_SENTINEL", id="unstructured-later-text"),
        pytest.param(
            json.dumps({"memories": [{"text": "UNCONFIRMED_LATER_TEXT_SENTINEL"}]}),
            id="unconfirmed-later-text",
        ),
    ],
)
def test_cli_recall_validates_all_text_before_showing_any_memory(monkeypatch, later_text) -> None:
    body = {"result": {"content": [
        _confirmed_text([{"text": "EARLIER_CONFIRMED_MEMORY_SENTINEL", "relevance": 0.9}]),
        {"type": "text", "text": later_text},
    ]}}
    result, _ = _invoke_recall_response(monkeypatch, body, ["--memory-view", "history"])
    assert result.exit_code == 1
    assert "Historical recall refused:" in result.output
    assert "EARLIER_CONFIRMED_MEMORY_SENTINEL" not in result.output
    assert "UNCONFIRMED_LATER_TEXT_SENTINEL" not in result.output
    assert "Retained historical evidence" not in result.output
    assert "Found " not in result.output


def test_cli_recall_accepts_confirmed_empty_history(monkeypatch) -> None:
    result, _ = _invoke_recall_response(
        monkeypatch,
        {"result": {"isError": False, "content": [_confirmed_text([])]}},
        ["--memory-view", "history", "--as-of", CUTOFF],
    )
    assert result.exit_code == 0
    assert "Found 0 memory(ies)" in result.output
    assert "Retained historical evidence" in result.output


def test_cli_recall_refuses_invalid_memories_after_temporal_confirmation(monkeypatch) -> None:
    item = _confirmed_text([])
    payload = json.loads(item["text"])
    payload["memories"] = [REJECTED_MEMORY]
    item["text"] = json.dumps(payload)
    result, _ = _invoke_recall_response(
        monkeypatch, {"result": {"content": [item]}}, ["--memory-view", "history"],
    )
    assert result.exit_code == 1
    assert "Historical recall refused:" in result.output
    assert REJECTED_MEMORY not in result.output
    assert "Found " not in result.output


def test_cli_recall_accepts_confirmed_text_with_nontext_content(monkeypatch) -> None:
    body = {"result": {"content": [
        {"type": "image", "data": "NON_TEXT_SENTINEL"},
        _confirmed_text([{"text": "CONFIRMED_HISTORY_SENTINEL", "relevance": 0.9}]),
    ]}}
    result, _ = _invoke_recall_response(monkeypatch, body, ["--memory-view", "history"])
    assert result.exit_code == 0
    assert "CONFIRMED_HISTORY_SENTINEL" in result.output
    assert "NON_TEXT_SENTINEL" not in result.output


@pytest.mark.parametrize("separate_blocks", [False, True], ids=["same-payload", "later-block"])
@pytest.mark.parametrize(
    "field,bad_value",
    [
        pytest.param("text", None, id="null-text"),
        pytest.param("text", ["MALFORMED_DISPLAY_SENTINEL"], id="non-string-text"),
        pytest.param("relevance", "INVALID_RELEVANCE_SENTINEL", id="string-relevance"),
        pytest.param("relevance", None, id="null-relevance"),
        pytest.param("relevance", True, id="boolean-relevance"),
        pytest.param("relevance", float("nan"), id="nan-relevance"),
        pytest.param("relevance", float("inf"), id="infinite-relevance"),
        pytest.param("relevance", 10 ** 400, id="overflowing-relevance"),
        pytest.param("type", None, id="non-string-type"),
    ],
)
def test_cli_recall_prepares_all_historical_display_before_output(
    monkeypatch, separate_blocks, field, bad_value,
) -> None:
    earlier = {"type": "fact", "text": "EARLIER_HISTORY_SENTINEL", "relevance": 0.9}
    later = {"type": "fact", "text": "LATER_HISTORY_SENTINEL", "relevance": 0.8}
    later[field] = bad_value
    content = (
        [_confirmed_text([earlier]), _confirmed_text([later])]
        if separate_blocks else [_confirmed_text([earlier, later])]
    )
    result, _ = _invoke_recall_response(
        monkeypatch, {"result": {"content": content}}, ["--memory-view", "history"],
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert "Historical recall refused: invalid memory display data" in result.output
    assert "Retained historical evidence" not in result.output
    assert "Found " not in result.output
    assert "EARLIER_HISTORY_SENTINEL" not in result.output
    assert "LATER_HISTORY_SENTINEL" not in result.output
    assert "MALFORMED_DISPLAY_SENTINEL" not in result.output
    assert "INVALID_RELEVANCE_SENTINEL" not in result.output
    assert all(item["text"] not in result.output for item in content)


def test_cli_recall_accepts_all_confirmed_display_blocks_and_omitted_field_defaults(
    monkeypatch,
) -> None:
    body = {"result": {"content": [
        _confirmed_text([{"type": "fact", "text": "FIRST_HISTORY_SENTINEL", "relevance": 1}]),
        _confirmed_text([]),
        _confirmed_text([{"text": "LAST_HISTORY_SENTINEL"}, {}]),
    ]}}
    result, _ = _invoke_recall_response(monkeypatch, body, ["--memory-view", "history"])
    assert result.exit_code == 0
    assert result.output.count("Retained historical evidence") == 3
    assert "FIRST_HISTORY_SENTINEL" in result.output
    assert "LAST_HISTORY_SENTINEL" in result.output
    assert "[fact] (relevance: 1.00)" in result.output
    assert result.output.count("[unknown] (relevance: 0.00)") == 2
    assert all(f"Found {count} memory(ies)" in result.output for count in (0, 1, 2))


@pytest.mark.parametrize("memory", [
    pytest.param({"text": None, "relevance": 0.9}, id="null-text"),
    pytest.param(
        {"text": "CURRENT_LEGACY_SENTINEL", "relevance": "invalid"},
        id="string-relevance",
    ),
])
def test_cli_recall_preserves_legacy_current_display_fallback(monkeypatch, memory) -> None:
    raw_text = json.dumps({"memories": [memory]})
    result, _ = _invoke_recall(monkeypatch, raw_text, [])
    assert result.exit_code == 0
    assert raw_text in result.output
    assert "Retained historical evidence" not in result.output
    assert "Historical recall refused" not in result.output


INVALID_RECALL_TEXT_CASES = [
    pytest.param(None, id="null-text"),
    pytest.param(["NON_STRING_TEXT_SENTINEL"], id="list-text"),
    pytest.param(31337, id="integer-text"),
    pytest.param("[" * 1100 + "0" + "]" * 1100, id="deep-json"),
    pytest.param("9" * 5000, id="large-integer-json"),
]


@pytest.mark.parametrize("bad_text", INVALID_RECALL_TEXT_CASES)
def test_cli_recall_current_decoder_fallback_preserves_surrounding_blocks(
    monkeypatch, bad_text,
) -> None:
    before = json.dumps({"memories": [{"text": "BEFORE_CURRENT_SENTINEL", "relevance": 0.9}]})
    after = json.dumps({"memories": [{"text": "AFTER_CURRENT_SENTINEL", "relevance": 0.8}]})
    body = {"result": {"content": [
        {"type": "text", "text": before},
        {"type": "text", "text": bad_text},
        {"type": "text", "text": after},
    ]}}
    result, _ = _invoke_recall_response(monkeypatch, body, [])
    assert result.exit_code == 0
    assert "BEFORE_CURRENT_SENTINEL" in result.output
    assert "AFTER_CURRENT_SENTINEL" in result.output
    raw_fallback = str(bad_text)
    assert raw_fallback in result.output
    assert (
        result.output.index("BEFORE_CURRENT_SENTINEL")
        < result.output.index(raw_fallback)
        < result.output.index("AFTER_CURRENT_SENTINEL")
    )
    assert "Retained historical evidence" not in result.output
    assert "Historical recall refused" not in result.output


@pytest.mark.parametrize("bad_text", INVALID_RECALL_TEXT_CASES)
def test_cli_recall_historical_decoder_errors_refuse_all_surrounding_blocks(
    monkeypatch, bad_text,
) -> None:
    body = {"result": {"content": [
        _confirmed_text([{"text": "BEFORE_HISTORY_SENTINEL", "relevance": 0.9}]),
        {"type": "text", "text": bad_text},
        _confirmed_text([{"text": "AFTER_HISTORY_SENTINEL", "relevance": 0.8}]),
    ]}}
    result, _ = _invoke_recall_response(monkeypatch, body, ["--memory-view", "history"])
    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert "Historical recall refused:" in result.output
    assert "Retained historical evidence" not in result.output
    assert "Found " not in result.output
    assert "BEFORE_HISTORY_SENTINEL" not in result.output
    assert "AFTER_HISTORY_SENTINEL" not in result.output
    assert str(bad_text) not in result.output
    assert "maximum recursion depth" not in result.output.casefold()
    assert "exceeds the limit" not in result.output.casefold()


HOSTED_V2_MEMORY_FIELDS = {
    "memory_id": "synthetic-hosted-v2-1",
    "type": "fact",
    "scope": "project",
    "relevance": 0.9123,
}


@pytest.mark.parametrize("memory_view", ["current", "history"])
def test_cli_recall_displays_hosted_v2_content_with_existing_preview_limit(
    monkeypatch, memory_view,
) -> None:
    content = "CANONICAL_BODY_SENTINEL_" + "x" * 240 + "_TRUNCATED_TAIL_SENTINEL"
    memory = {**HOSTED_V2_MEMORY_FIELDS, "content": content}
    if memory_view == "history":
        raw_text = _confirmed_text([memory])["text"]
        controls = ["--memory-view", "history", "--as-of", CUTOFF]
    else:
        raw_text = json.dumps({"memories": [memory]})
        controls = []
    result, _ = _invoke_recall(monkeypatch, raw_text, controls)
    assert result.exit_code == 0
    assert "Found 1 memory(ies)" in result.output
    assert "[fact] (relevance: 0.91)" in result.output
    assert f"  {content[:200]}\n" in result.output
    assert "_TRUNCATED_TAIL_SENTINEL" not in result.output
    assert raw_text not in result.output


@pytest.mark.parametrize("memory_view", ["current", "history"])
def test_cli_recall_preserves_legacy_body_when_canonical_content_is_absent(
    monkeypatch, memory_view,
) -> None:
    memory = {**HOSTED_V2_MEMORY_FIELDS, "text": "LEGACY_BODY_SENTINEL"}
    if memory_view == "history":
        raw_text = _confirmed_text([memory])["text"]
        controls = ["--memory-view", "history"]
    else:
        raw_text = json.dumps({"memories": [memory]})
        controls = []
    result, _ = _invoke_recall(monkeypatch, raw_text, controls)
    assert result.exit_code == 0
    assert "  LEGACY_BODY_SENTINEL\n" in result.output
    assert raw_text not in result.output


@pytest.mark.parametrize("memory_view", ["current", "history"])
@pytest.mark.parametrize("content", ["CANONICAL_WINS_SENTINEL", ""], ids=["text", "empty"])
def test_cli_recall_canonical_content_presence_wins_over_conflicting_legacy_text(
    monkeypatch, memory_view, content,
) -> None:
    memory = {
        **HOSTED_V2_MEMORY_FIELDS,
        "content": content,
        "text": "LEGACY_MUST_NOT_WIN_SENTINEL",
    }
    if memory_view == "history":
        raw_text = _confirmed_text([memory])["text"]
        controls = ["--memory-view", "history"]
    else:
        raw_text = json.dumps({"memories": [memory]})
        controls = []
    result, _ = _invoke_recall(monkeypatch, raw_text, controls)
    assert result.exit_code == 0
    assert "Found 1 memory(ies)" in result.output
    assert f"  {content}\n" in result.output
    assert "LEGACY_MUST_NOT_WIN_SENTINEL" not in result.output
    assert raw_text not in result.output


@pytest.mark.parametrize("separate_blocks", [False, True], ids=["same-payload", "later-block"])
@pytest.mark.parametrize("invalid_content", [
    pytest.param(None, id="null"),
    pytest.param(["INVALID_CANONICAL_VALUE_SENTINEL"], id="list"),
    pytest.param(31337, id="integer"),
    pytest.param(True, id="boolean"),
    pytest.param({"value": "INVALID_CANONICAL_VALUE_SENTINEL"}, id="object"),
])
def test_cli_recall_invalid_canonical_history_never_uses_legacy_or_partial_output(
    monkeypatch, separate_blocks, invalid_content,
) -> None:
    earlier = {
        **HOSTED_V2_MEMORY_FIELDS,
        "memory_id": "synthetic-hosted-v2-before",
        "content": "EARLIER_CANONICAL_BODY_SENTINEL",
    }
    later = {
        **HOSTED_V2_MEMORY_FIELDS,
        "content": invalid_content,
        "text": "LEGACY_FALLBACK_MUST_NOT_APPEAR_SENTINEL",
    }
    content = (
        [_confirmed_text([earlier]), _confirmed_text([later])]
        if separate_blocks else [_confirmed_text([earlier, later])]
    )
    result, _ = _invoke_recall_response(
        monkeypatch, {"result": {"content": content}}, ["--memory-view", "history"],
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert "Historical recall refused: invalid memory display data" in result.output
    assert "Retained historical evidence" not in result.output
    assert "Found " not in result.output
    assert "EARLIER_CANONICAL_BODY_SENTINEL" not in result.output
    assert "LEGACY_FALLBACK_MUST_NOT_APPEAR_SENTINEL" not in result.output
    assert "INVALID_CANONICAL_VALUE_SENTINEL" not in result.output
    assert all(item["text"] not in result.output for item in content)
