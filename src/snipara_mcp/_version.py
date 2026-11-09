"""Package identity without importing the MCP server or optional TOML parsers."""

import re
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def _discover_version() -> str:
    """Prefer the owning checkout metadata; installed wheels use dist-info.

    Only the canonical project's literal version string is read. This bounded
    extraction avoids requiring tomllib (Python3.11+) or another dependency on
    supported Python3.10 checkouts. It does not evaluate arbitrary TOML.
    """
    pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
    try:
        if pyproject.is_file() and pyproject.stat().st_size <= 131_072:
            text = pyproject.read_text(encoding="utf-8")
            project = re.search(r"(?ms)^\[project\][ \t]*\n(.*?)(?=^\[|\Z)", text)
            match = re.search(r"(?m)^version\s*=\s*(['\"])([^'\"\r\n]{1,128})\1\s*(?:#.*)?$", project[1]) if project else None
            if match:
                return match[2]
    except OSError:
        pass
    try:
        return version("snipara-mcp")
    except PackageNotFoundError:
        return "0.0.0"


__version__ = _discover_version()
