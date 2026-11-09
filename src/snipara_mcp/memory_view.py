"""Fail closed when an older hosted server ignores explicit history intent."""

from datetime import datetime, timezone
from typing import Any


def require_memory_view(result: dict[str, Any], memory_view: str, as_of: str | None) -> dict[str, Any]:
    if memory_view not in ("current", "history") or (as_of is not None and memory_view != "history"):
        raise ValueError("memory_view must be current or history; as_of requires history")
    if memory_view == "current" and as_of is None:
        return result
    metadata = result.get("temporal_context")
    if not isinstance(metadata, dict) or metadata.get("contract") != "snipara.memory-temporal.v1" or metadata.get("view") != memory_view:
        raise RuntimeError("Hosted server did not confirm the requested memory view; refusing a silent current-view fallback")
    if as_of is not None:
        try:
            requested = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
            actual = datetime.fromisoformat(metadata["as_of"].replace("Z", "+00:00"))
            if requested.tzinfo is None or actual.tzinfo is None or requested > datetime.now(timezone.utc) or requested != actual:
                raise ValueError()
        except (KeyError, TypeError, ValueError, AttributeError):
            raise RuntimeError("Hosted server did not confirm the requested as_of cutoff") from None
    return result
