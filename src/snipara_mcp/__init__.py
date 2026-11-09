"""Snipara MCP Server - Context optimization for LLMs."""

from ._version import __version__
from ._version import _discover_version as _discover_version
from .server import main


__all__ = ["main", "get_snipara_tools", "__version__"]


def get_snipara_tools(*args, **kwargs):
    """Get Snipara tools for Snipara Sandbox runtime integration.

    This is a lazy import to avoid requiring the runtime package
    when using snipara-mcp as a standalone MCP server.

    See rlm_tools.get_snipara_tools for full documentation.
    """
    from .rlm_tools import get_snipara_tools as _get_snipara_tools
    return _get_snipara_tools(*args, **kwargs)
