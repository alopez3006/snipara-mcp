"""
Snipara Sandbox tool plugins for Snipara context optimization.

This module provides Snipara tools in the runtime tool format. The current
compatibility package is rlm-runtime until the Snipara Sandbox package rename is
published.

Usage:
    # Automatic (in the Snipara Sandbox compatibility runtime)
    rlm = RLM(snipara_api_key="...", snipara_project_slug="...")
    # Tools are auto-registered

    # Manual
    from snipara_mcp.rlm_tools import get_snipara_tools
    tools = get_snipara_tools(api_key="...", project_slug="...")
"""

from __future__ import annotations

import os
from typing import Any, Literal, TYPE_CHECKING

import httpx
from .tool_contract import MCP_TOOL_DEFINITIONS
from .memory_view import require_memory_view

if TYPE_CHECKING:
    from rlm.backends.base import Tool

# Default API URL - matches the MCP endpoint format
DEFAULT_API_URL = "https://api.snipara.com"
OutcomeRerankMode = Literal["disabled", "shadow", "enabled"]

CORRELATION_CONTEXT_PARAMETER: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "description": "Optional bounded opaque correlation IDs; never changes project access.",
    "properties": {
        "version": {
            "type": "string",
            "enum": ["retrieval-correlation-v1"],
            "default": "retrieval-correlation-v1",
        },
        **{
            key: {
                "type": "string",
                "minLength": 1,
                "maxLength": 128,
                "pattern": r"^[A-Za-z0-9][A-Za-z0-9._~:/@+\-]{0,127}$",
            }
            for key in ("session_id", "workflow_session_id", "correlation_id", "request_id")
        },
    },
}


class SniparaClient:
    """HTTP client for Snipara MCP API."""

    def __init__(
        self,
        api_key: str,
        project_slug: str,
        api_url: str | None = None,
    ):
        """Initialize the Snipara client.

        Args:
            api_key: Snipara API key (starts with 'snp-' or legacy 'rlm_')
            project_slug: Project identifier
            api_url: Optional custom API URL (e.g., https://snipara.com)
        """
        self.api_key = api_key
        self.project_slug = project_slug
        self.api_url = api_url or os.environ.get("SNIPARA_API_URL", DEFAULT_API_URL)
        self._client: httpx.AsyncClient | None = None
        self._tool_endpoint_url: str | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                headers={
                    "X-API-Key": self.api_key,
                    "Content-Type": "application/json",
                },
                timeout=60.0,
            )
        return self._client

    async def call_tool(self, tool_name: str, params: dict[str, Any]) -> dict[str, Any]:
        """Call a Snipara MCP tool.

        Args:
            tool_name: Name of the tool to call
            params: Tool parameters

        Returns:
            Tool result dictionary
        """
        client = await self._get_client()
        last_response: httpx.Response | None = None

        for endpoint_url in self._candidate_tool_urls():
            response = await client.post(
                endpoint_url,
                json={"tool": tool_name, "params": params},
            )

            if response.status_code == 404:
                last_response = response
                continue

            response.raise_for_status()
            result = response.json()

            if not result.get("success"):
                raise RuntimeError(result.get("error", "Unknown error"))

            self._tool_endpoint_url = endpoint_url
            payload = result.get("result", {})
            if tool_name in ("rlm_recall", "snipara_recall"):
                return require_memory_view(payload, params.get("memory_view", "current"), params.get("as_of"))
            return payload

        if last_response is not None:
            last_response.raise_for_status()

        raise RuntimeError("Unable to resolve a working Snipara MCP tool endpoint.")

    def _candidate_tool_urls(self) -> list[str]:
        """Return candidate REST endpoints for tool calls.

        Prefer the hosted MCP backend endpoint and fall back to the web proxy
        route for self-hosted or older deployments.
        """
        if self._tool_endpoint_url:
            return [self._tool_endpoint_url]

        base_url = self.api_url.rstrip("/")
        candidates = [
            f"{base_url}/v1/{self.project_slug}/mcp",
            f"{base_url}/api/mcp/{self.project_slug}",
        ]

        deduped: list[str] = []
        for candidate in candidates:
            if candidate not in deduped:
                deduped.append(candidate)
        return deduped

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None


def _build_contract_handler(client: SniparaClient, tool_name: str):
    """Create a generic handler that forwards kwargs to a hosted MCP tool."""

    async def _handler(**kwargs: Any) -> dict[str, Any]:
        return await client.call_tool(tool_name, kwargs)

    _handler.__name__ = tool_name
    return _handler


def _build_contract_tools(
    Tool: type["Tool"], client: SniparaClient, legacy_tools: list["Tool"]
) -> list["Tool"]:
    """Expose the advertised hosted tool contract alongside the built-in runtime tools."""
    legacy_names = {tool.name for tool in legacy_tools}
    generated_tools: list["Tool"] = []

    for tool_definition in MCP_TOOL_DEFINITIONS:
        tool_name = tool_definition["name"]
        if tool_name in legacy_names:
            continue

        generated_tools.append(
            Tool(
                name=tool_name,
                description=tool_definition["description"],
                parameters=tool_definition["inputSchema"],
                handler=_build_contract_handler(client, tool_name),
            )
        )

    return generated_tools


def get_snipara_tools(
    api_key: str | None = None,
    project_slug: str | None = None,
    api_url: str | None = None,
) -> list[Tool]:
    """Get Snipara tools as runtime-compatible Tool objects.

    This function is called by the runtime when snipara-mcp is installed and
    Snipara credentials are configured.

    Args:
        api_key: Snipara API key (or SNIPARA_API_KEY env var)
        project_slug: Project slug (or SNIPARA_PROJECT_SLUG env var)
        api_url: Optional custom API URL

    Returns:
        List of Tool objects compatible with the runtime

    Raises:
        ImportError: If the runtime package is not installed
        ValueError: If credentials are missing
    """
    # Import Tool from the current compatibility runtime package
    try:
        from rlm.backends.base import Tool
    except ImportError:
        raise ImportError(
            "Snipara Sandbox runtime support is required to use Snipara tools. "
            "Install the current compatibility package with: pip install rlm-runtime"
        )

    # Get credentials from args, .snipara.toml, or environment
    # Try loading from unified config if snipara SDK is installed
    _snipara_config = None
    if not (api_key and project_slug):
        try:
            from snipara.config import load_config

            _snipara_config = load_config()
        except ImportError:
            pass  # snipara SDK not installed — use env vars

    api_key = api_key or os.environ.get("SNIPARA_API_KEY")
    project_slug = project_slug or os.environ.get("SNIPARA_PROJECT_SLUG")

    # Fall back to .snipara.toml values
    if _snipara_config:
        api_key = api_key or _snipara_config.project.api_key
        project_slug = project_slug or _snipara_config.project.slug
        if not api_url and _snipara_config.project.api_url != "https://api.snipara.com":
            api_url = _snipara_config.project.api_url

    if not api_key:
        raise ValueError("Snipara API key required. Set SNIPARA_API_KEY or pass api_key parameter.")
    if not project_slug:
        raise ValueError(
            "Snipara project slug required. Set SNIPARA_PROJECT_SLUG or pass project_slug parameter."
        )

    # Create client
    client = SniparaClient(api_key, project_slug, api_url)

    # Define tool handlers
    async def context_query(
        query: str,
        max_tokens: int = 4000,
        search_mode: str = "hybrid",
        include_metadata: bool = True,
        task: str | None = None,
        context_chunk_outcome_rerank_mode: OutcomeRerankMode = "disabled",
        context_chunk_outcome_window_hours: int = 72,
        correlation_context: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Query Snipara for optimized, relevant context.

        Args:
            query: The question or topic to search for
            max_tokens: Maximum tokens to return (default: 4000)
            search_mode: Search mode - keyword, semantic, or hybrid
            include_metadata: Include file paths and relevance scores
            task: Optional task label that scopes the live-join fallback and retrieval
                correlation; persisted outcome posterior statistics remain project-wide
            context_chunk_outcome_rerank_mode: Requested disabled, shadow, or enabled mode
            context_chunk_outcome_window_hours: Strict attribution window (1-336 hours)

        Returns:
            Dictionary with sections, total_tokens, and suggestions
        """
        params: dict[str, Any] = {
            "query": query,
            "max_tokens": max_tokens,
            "search_mode": search_mode,
            "include_metadata": include_metadata,
            "context_chunk_outcome_rerank_mode": context_chunk_outcome_rerank_mode,
            "context_chunk_outcome_window_hours": context_chunk_outcome_window_hours,
        }
        if task is not None:
            params["task"] = task
        if correlation_context is not None:
            params["correlation_context"] = correlation_context
        return await client.call_tool("rlm_context_query", params)

    async def sections() -> dict[str, Any]:
        """List all available documentation sections.

        Returns:
            Dictionary with sections list containing paths and chunk counts
        """
        return await client.call_tool("rlm_sections", {})

    async def search(
        pattern: str,
        max_results: int = 20,
        correlation_context: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Search documentation for a regex pattern.

        Args:
            pattern: Regex pattern to search for
            max_results: Maximum number of results

        Returns:
            Dictionary with matches list
        """
        params: dict[str, Any] = {
            "pattern": pattern,
            "max_results": max_results,
        }
        if correlation_context is not None:
            params["correlation_context"] = correlation_context
        return await client.call_tool("rlm_search", params)

    async def read(
        file: str,
        start_line: int = 1,
        end_line: int | None = None,
    ) -> dict[str, Any]:
        """Read specific lines from a documentation file.

        Args:
            file: File path to read
            start_line: Starting line number (default: 1)
            end_line: Ending line number (optional, reads to end if not specified)

        Returns:
            Dictionary with content string
        """
        params: dict[str, Any] = {"file": file, "start_line": start_line}
        if end_line is not None:
            params["end_line"] = end_line
        return await client.call_tool("rlm_read", params)

    async def shared_context(
        max_tokens: int = 4000,
        categories: list[str] | None = None,
        include_content: bool = True,
    ) -> dict[str, Any]:
        """Get merged context from linked shared collections.

        Returns team best practices, coding standards, and guidelines
        organized by priority category.

        Args:
            max_tokens: Token budget for context
            categories: Filter to specific categories (MANDATORY, BEST_PRACTICES, etc.)
            include_content: Include the actual content

        Returns:
            Dictionary with documents, collections_loaded, and merged_content
        """
        params: dict[str, Any] = {
            "max_tokens": max_tokens,
            "include_content": include_content,
        }
        if categories:
            params["categories"] = categories
        return await client.call_tool("rlm_shared_context", params)

    async def decompose(
        query: str,
        max_depth: int = 2,
    ) -> dict[str, Any]:
        """Break a complex query into sub-queries with execution order.

        Args:
            query: Complex question to decompose
            max_depth: Maximum decomposition depth

        Returns:
            Dictionary with sub_queries and suggested_sequence
        """
        return await client.call_tool(
            "rlm_decompose",
            {
                "query": query,
                "max_depth": max_depth,
            },
        )

    async def multi_query(
        queries: list[dict[str, str]],
        max_tokens: int = 8000,
    ) -> dict[str, Any]:
        """Execute multiple queries with shared token budget.

        Args:
            queries: List of query objects with 'query' key
            max_tokens: Total token budget

        Returns:
            Dictionary with results for each query
        """
        return await client.call_tool(
            "rlm_multi_query",
            {
                "queries": queries,
                "max_tokens": max_tokens,
            },
        )

    async def multi_project_query(
        query: str,
        max_tokens: int = 4000,
        per_project_limit: int = 3,
        project_ids: list[str] | None = None,
        exclude_project_ids: list[str] | None = None,
        search_mode: str = "keyword",
        include_metadata: bool = True,
    ) -> dict[str, Any]:
        """Query across multiple projects in your team.

        Args:
            query: The query/question to get context for
            max_tokens: Maximum tokens to return across all projects
            per_project_limit: Maximum sections to return per project
            project_ids: Optional list of project IDs or slugs to include
            exclude_project_ids: Optional list of project IDs or slugs to exclude
            search_mode: Search strategy (keyword, semantic, hybrid)
            include_metadata: Include file paths, line numbers, and relevance scores

        Returns:
            Dictionary with results from multiple projects
        """
        params: dict[str, Any] = {
            "query": query,
            "max_tokens": max_tokens,
            "per_project_limit": per_project_limit,
            "search_mode": search_mode,
            "include_metadata": include_metadata,
        }
        if project_ids:
            params["project_ids"] = project_ids
        if exclude_project_ids:
            params["exclude_project_ids"] = exclude_project_ids
        return await client.call_tool("rlm_multi_project_query", params)

    async def stats() -> dict[str, Any]:
        """Get documentation statistics.

        Returns:
            Dictionary with files_loaded, total_lines, total_characters, sections
        """
        return await client.call_tool("rlm_stats", {})

    async def list_templates(
        category: str | None = None,
    ) -> dict[str, Any]:
        """List available prompt templates from shared collections.

        Args:
            category: Optional category filter

        Returns:
            Dictionary with templates list
        """
        params: dict[str, Any] = {}
        if category:
            params["category"] = category
        return await client.call_tool("rlm_list_templates", params)

    async def get_template(
        template_id: str | None = None,
        slug: str | None = None,
        variables: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get and optionally render a prompt template.

        Args:
            template_id: Template ID
            slug: Template slug (alternative to ID)
            variables: Variables to substitute in template

        Returns:
            Dictionary with template and rendered_prompt
        """
        params: dict[str, Any] = {}
        if template_id:
            params["template_id"] = template_id
        if slug:
            params["slug"] = slug
        if variables:
            params["variables"] = variables
        return await client.call_tool("rlm_get_template", params)

    # ============ SESSION MANAGEMENT TOOLS ============

    async def ask(
        question: str,
        correlation_context: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Basic documentation query.

        Args:
            question: The question to ask about the documentation

        Returns:
            Dictionary with answer
        """
        params: dict[str, Any] = {"query": question}
        if correlation_context is not None:
            params["correlation_context"] = correlation_context
        return await client.call_tool("rlm_ask", params)

    async def inject(context: str, append: bool = False) -> dict[str, Any]:
        """Inject context into the session.

        Args:
            context: The context to inject
            append: Append to existing context instead of replacing

        Returns:
            Dictionary with success status
        """
        return await client.call_tool(
            "rlm_inject",
            {
                "context": context,
                "append": append,
            },
        )

    async def get_context() -> dict[str, Any]:
        """Get the current session context.

        Returns:
            Dictionary with current context
        """
        return await client.call_tool("rlm_context", {})

    async def clear_context() -> dict[str, Any]:
        """Clear the current session context.

        Returns:
            Dictionary with success status
        """
        return await client.call_tool("rlm_clear_context", {})

    async def get_settings() -> dict[str, Any]:
        """Get project settings.

        Returns:
            Dictionary with project settings
        """
        return await client.call_tool("rlm_settings", {})

    async def plan(
        query: str,
        strategy: str = "relevance_first",
        max_tokens: int = 16000,
    ) -> dict[str, Any]:
        """Create an execution plan for a complex query.

        Args:
            query: The complex question to plan for
            strategy: Execution strategy (breadth_first, depth_first, relevance_first)
            max_tokens: Total token budget

        Returns:
            Dictionary with plan steps
        """
        return await client.call_tool(
            "rlm_plan",
            {
                "query": query,
                "strategy": strategy,
                "max_tokens": max_tokens,
            },
        )

    # ============ SUMMARY STORAGE TOOLS ============

    async def store_summary(
        document_path: str,
        summary: str,
        summary_type: str = "concise",
        section_id: str | None = None,
        line_start: int | None = None,
        line_end: int | None = None,
        generated_by: str | None = None,
    ) -> dict[str, Any]:
        """Store a summary for a document or section.

        Args:
            document_path: Path to the document
            summary: The summary text to store
            summary_type: Type of summary (concise, detailed, technical, keywords, custom)
            section_id: Optional section identifier
            line_start: Start line for section summary
            line_end: End line for section summary
            generated_by: Model that generated the summary

        Returns:
            Dictionary with summary_id and status
        """
        params: dict[str, Any] = {
            "document_path": document_path,
            "summary": summary,
            "summary_type": summary_type,
        }
        if section_id:
            params["section_id"] = section_id
        if line_start is not None:
            params["line_start"] = line_start
        if line_end is not None:
            params["line_end"] = line_end
        if generated_by:
            params["generated_by"] = generated_by
        return await client.call_tool("rlm_store_summary", params)

    async def get_summaries(
        document_path: str | None = None,
        summary_type: str | None = None,
        section_id: str | None = None,
        include_content: bool = True,
    ) -> dict[str, Any]:
        """Get stored summaries.

        Args:
            document_path: Filter by document path
            summary_type: Filter by summary type
            section_id: Filter by section ID
            include_content: Include summary content in response

        Returns:
            Dictionary with summaries list
        """
        params: dict[str, Any] = {"include_content": include_content}
        if document_path:
            params["document_path"] = document_path
        if summary_type:
            params["summary_type"] = summary_type
        if section_id:
            params["section_id"] = section_id
        return await client.call_tool("rlm_get_summaries", params)

    async def delete_summary(
        summary_id: str | None = None,
        document_path: str | None = None,
        summary_type: str | None = None,
    ) -> dict[str, Any]:
        """Delete stored summaries.

        Args:
            summary_id: Specific summary ID to delete
            document_path: Delete all summaries for document
            summary_type: Delete summaries of this type

        Returns:
            Dictionary with deleted count
        """
        params: dict[str, Any] = {}
        if summary_id:
            params["summary_id"] = summary_id
        if document_path:
            params["document_path"] = document_path
        if summary_type:
            params["summary_type"] = summary_type
        return await client.call_tool("rlm_delete_summary", params)

    # ============ AGENT MEMORY TOOLS ============

    async def remember(
        content: str,
        type: str = "fact",
        scope: str = "project",
        category: str | None = None,
        ttl_days: int | None = None,
        related_to: list[str] | None = None,
        document_refs: list[str] | None = None,
        source: str | None = None,
    ) -> dict[str, Any]:
        """Store a memory.

        Args:
            content: The memory content to store
            type: Memory type (fact, decision, learning, preference, todo, context)
            scope: Visibility scope (agent, project, team, user)
            category: Optional grouping category
            ttl_days: Days until memory expires (null = permanent)
            related_to: IDs of related memories
            document_refs: Referenced document paths
            source: What created this memory

        Returns:
            Dictionary with memory_id and status
        """
        params: dict[str, Any] = {
            "text": content,
            "type": type,
            "scope": scope,
        }
        if category:
            params["category"] = category
        if ttl_days is not None:
            params["ttl_days"] = ttl_days
        if related_to:
            params["related_to"] = related_to
        if document_refs:
            params["document_refs"] = document_refs
        if source:
            params["source"] = source
        return await client.call_tool("rlm_remember", params)

    async def recall(
        query: str,
        type: str | None = None,
        scope: str | None = None,
        category: str | None = None,
        limit: int = 5,
        min_relevance: float = 0.5,
        include_expired: bool = False,
        include_inactive: bool = False,
        task: str | None = None,
        outcome_rerank_mode: OutcomeRerankMode | None = None,
        correlation_context: dict[str, str] | None = None,
        retrieval_queries: list[str] | None = None,
        memory_view: str = "current",
        as_of: str | None = None,
    ) -> dict[str, Any]:
        """Recall memories semantically.

        Args:
            query: Search query for semantic recall
            type: Filter by memory type
            scope: Filter by scope
            category: Filter by category
            limit: Maximum memories to return
            min_relevance: Minimum relevance score (0-1)
            include_expired: Include expired memories
            include_inactive: Include inactive memories in primary results
            task: Optional task label recorded for retrieval/outcome correlation
            outcome_rerank_mode: Optional disabled, shadow, or enabled mode bounded by server config

        Returns:
            Dictionary with recalled memories and optional warnings
        """
        params: dict[str, Any] = {
            "query": query,
            "limit": limit,
            "min_relevance": min_relevance,
            "include_expired": include_expired,
            "include_inactive": include_inactive,
        }
        if retrieval_queries is not None:
            params["retrieval_queries"] = retrieval_queries
        if type:
            params["type"] = type
        if scope:
            params["scope"] = scope
        if category:
            params["category"] = category
        if task is not None:
            params["task"] = task
        if outcome_rerank_mode is not None:
            params["outcome_rerank_mode"] = outcome_rerank_mode
        if correlation_context is not None:
            params["correlation_context"] = correlation_context
        if memory_view != "current" or as_of is not None:
            params["memory_view"] = memory_view
            if as_of is not None:
                params["as_of"] = as_of
        result = await client.call_tool("rlm_recall", params)
        return require_memory_view(result, memory_view, as_of)

    async def memories(
        type: str | None = None,
        scope: str | None = None,
        category: str | None = None,
        status: str | None = None,
        search: str | None = None,
        limit: int = 20,
        offset: int = 0,
        include_expired: bool = False,
        include_inactive: bool = False,
    ) -> dict[str, Any]:
        """List stored memories.

        Args:
            type: Filter by memory type
            scope: Filter by scope
            category: Filter by category
            status: Filter by lifecycle status
            search: Text search in content
            limit: Maximum memories to return
            offset: Offset for pagination
            include_expired: Include expired memories
            include_inactive: Include inactive memories in the result set

        Returns:
            Dictionary with memories list
        """
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
            "include_expired": include_expired,
            "include_inactive": include_inactive,
        }
        if type:
            params["type"] = type
        if scope:
            params["scope"] = scope
        if category:
            params["category"] = category
        if status:
            params["status"] = status
        if search:
            params["search"] = search
        return await client.call_tool("rlm_memories", params)

    async def memory_invalidate(
        memory_id: str,
        invalidated_at: str | None = None,
        reason: str | None = None,
    ) -> dict[str, Any]:
        """Invalidate a stored memory without deleting it.

        Args:
            memory_id: Memory ID to invalidate
            invalidated_at: Optional ISO timestamp for the invalidation event
            reason: Optional invalidation reason

        Returns:
            Dictionary with updated status and timestamp
        """
        params: dict[str, Any] = {"memory_id": memory_id}
        if invalidated_at:
            params["invalidated_at"] = invalidated_at
        if reason:
            params["reason"] = reason
        return await client.call_tool("rlm_memory_invalidate", params)

    async def memory_supersede(
        old_memory_id: str,
        new_memory_id: str,
        reason: str | None = None,
    ) -> dict[str, Any]:
        """Replace an existing memory with an updated one.

        Args:
            old_memory_id: Memory ID being replaced
            new_memory_id: Memory ID replacing the old one
            reason: Optional supersession reason

        Returns:
            Dictionary with old/new memory IDs and statuses
        """
        params: dict[str, Any] = {
            "old_memory_id": old_memory_id,
            "new_memory_id": new_memory_id,
        }
        if reason:
            params["reason"] = reason
        return await client.call_tool("rlm_memory_supersede", params)

    async def forget(
        memory_id: str | None = None,
        type: str | None = None,
        category: str | None = None,
        older_than_days: int | None = None,
    ) -> dict[str, Any]:
        """Delete memories.

        Args:
            memory_id: Specific memory ID to delete
            type: Delete all memories of this type
            category: Delete all memories in this category
            older_than_days: Delete memories older than N days

        Returns:
            Dictionary with deleted count
        """
        params: dict[str, Any] = {}
        if memory_id:
            params["memory_id"] = memory_id
        if type:
            params["type"] = type
        if category:
            params["category"] = category
        if older_than_days is not None:
            params["older_than_days"] = older_than_days
        return await client.call_tool("rlm_forget", params)











    # ============ DOCUMENT MANAGEMENT TOOLS ============

    async def upload_document(
        path: str,
        content: str,
        kind: str | None = None,
        format: str | None = None,
        language: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Upload a document.

        Args:
            path: Document path
            content: Document content
            kind: Optional document kind (DOC or BINARY)
            format: Optional document format
            language: Optional language hint
            metadata: Optional structured document metadata

        Returns:
            Dictionary with upload status
        """
        params: dict[str, Any] = {
            "path": path,
            "content": content,
        }
        if kind:
            params["kind"] = kind
        if format:
            params["format"] = format
        if language:
            params["language"] = language
        if metadata is not None:
            params["metadata"] = metadata
        return await client.call_tool("rlm_upload_document", params)

    async def sync_documents(
        documents: list[dict[str, str]],
        delete_missing: bool = False,
    ) -> dict[str, Any]:
        """Sync multiple documents.

        Args:
            documents: List of documents with path and content
            delete_missing: Delete documents not in list

        Returns:
            Dictionary with sync stats
        """
        return await client.call_tool(
            "rlm_sync_documents",
            {
                "documents": documents,
                "delete_missing": delete_missing,
            },
        )

    async def document_tombstones(
        limit: int = 50,
        include_expired: bool = False,
    ) -> dict[str, Any]:
        """List deleted or pruned document tombstones for the current project.

        Args:
            limit: Maximum number of tombstones to return
            include_expired: Include tombstones past retention but not yet purged

        Returns:
            Dictionary with tombstone rows and retention summary
        """
        return await client.call_tool(
            "rlm_document_tombstones",
            {
                "limit": limit,
                "include_expired": include_expired,
            },
        )

    # ============ INDEX HEALTH & ANALYTICS TOOLS (Sprint 3) ============

    async def index_health(
        stale_threshold_days: int = 30,
    ) -> dict[str, Any]:
        """Get comprehensive index health metrics.

        Args:
            stale_threshold_days: Days after which content is considered stale

        Returns:
            Dictionary with health score, coverage, quality, tier distribution, stale docs
        """
        return await client.call_tool(
            "rlm_index_health",
            {
                "stale_threshold_days": stale_threshold_days,
            },
        )

    async def index_recommendations() -> dict[str, Any]:
        """Get actionable recommendations to improve index health.

        Returns:
            Dictionary with prioritized recommendations
        """
        return await client.call_tool("rlm_index_recommendations", {})

    async def reindex(
        job_id: str | None = None,
        mode: str = "incremental",
        kind: str = "doc",
    ) -> dict[str, Any]:
        """Trigger a reindex job or poll an existing one.

        Args:
            job_id: Existing job ID to poll
            mode: Reindex mode when creating a job (incremental or full)
            kind: Reindex kind when creating a job (doc or code)

        Returns:
            Dictionary with job creation or status info
        """
        payload: dict[str, Any] = {}
        if job_id:
            payload["job_id"] = job_id
        else:
            payload["mode"] = mode
            payload["kind"] = kind
        return await client.call_tool("rlm_reindex", payload)

    async def search_analytics(
        days: int = 30,
    ) -> dict[str, Any]:
        """Get comprehensive search analytics.

        Args:
            days: Number of days to analyze (1-90)

        Returns:
            Dictionary with query stats, latency percentiles, tool usage, errors
        """
        return await client.call_tool(
            "rlm_search_analytics",
            {
                "days": days,
            },
        )

    async def query_trends(
        days: int = 7,
        granularity: str = "day",
    ) -> dict[str, Any]:
        """Get query trends over time.

        Args:
            days: Number of days to analyze (1-30)
            granularity: Time bucket size (hour, day, week)

        Returns:
            Dictionary with time-bucketed query counts and metrics
        """
        return await client.call_tool(
            "rlm_query_trends",
            {
                "days": days,
                "granularity": granularity,
            },
        )

    # Build and return tool list
    legacy_tools = [
        Tool(
            name="context_query",
            description=(
                "Query Snipara for optimized, relevant context. "
                "Returns the most relevant documentation sections within your token budget. "
                "This is the PRIMARY tool for any documentation questions. "
                "Uses hybrid search (keyword + semantic) by default for best results."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The question or topic to search for",
                    },
                    "max_tokens": {
                        "type": "integer",
                        "default": 4000,
                        "description": "Maximum tokens to return",
                    },
                    "search_mode": {
                        "type": "string",
                        "enum": ["keyword", "semantic", "hybrid"],
                        "default": "hybrid",
                        "description": "Search mode",
                    },
                    "include_metadata": {
                        "type": "boolean",
                        "default": True,
                        "description": "Include file paths and relevance scores",
                    },
                    "task": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 512,
                        "description": (
                            "Optional task label that scopes the live-join fallback and retrieval "
                            "correlation; persisted outcome posterior statistics remain project-wide"
                        ),
                    },
                    "context_chunk_outcome_rerank_mode": {
                        "type": "string",
                        "enum": ["disabled", "shadow", "enabled"],
                        "default": "disabled",
                        "description": "Requested mode cannot escalate beyond the server configuration",
                    },
                    "context_chunk_outcome_window_hours": {
                        "type": "integer",
                        "default": 72,
                        "minimum": 1,
                        "maximum": 336,
                        "description": "Strict attribution window for compatible chunk outcomes",
                    },
                    "correlation_context": CORRELATION_CONTEXT_PARAMETER,
                },
                "required": ["query"],
            },
            handler=context_query,
        ),
        Tool(
            name="sections",
            description=(
                "List all available documentation sections in the project. "
                "Returns file paths and chunk counts for each document."
            ),
            parameters={
                "type": "object",
                "properties": {},
            },
            handler=sections,
        ),
        Tool(
            name="search",
            description=(
                "Search documentation for a regex pattern. "
                "Returns matching lines with file paths and line numbers."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Regex pattern to search for",
                    },
                    "max_results": {
                        "type": "integer",
                        "default": 20,
                        "description": "Maximum number of results",
                    },
                    "correlation_context": CORRELATION_CONTEXT_PARAMETER,
                },
                "required": ["pattern"],
            },
            handler=search,
        ),
        Tool(
            name="read",
            description=(
                "Read specific lines from a documentation file. "
                "Use after search or sections to get full content."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description": "File path to read",
                    },
                    "start_line": {
                        "type": "integer",
                        "default": 1,
                        "description": "Starting line number (default: 1)",
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "Ending line number (optional)",
                    },
                },
                "required": ["file"],
            },
            handler=read,
        ),
        Tool(
            name="shared_context",
            description=(
                "Get merged context from linked shared collections. "
                "Returns team best practices, coding standards, and guidelines "
                "organized by priority (MANDATORY > BEST_PRACTICES > GUIDELINES > REFERENCE). "
                "Use this to ensure code follows team conventions."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "max_tokens": {
                        "type": "integer",
                        "default": 4000,
                        "description": "Token budget for context",
                    },
                    "categories": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["MANDATORY", "BEST_PRACTICES", "GUIDELINES", "REFERENCE"],
                        },
                        "description": "Filter to specific categories",
                    },
                    "include_content": {
                        "type": "boolean",
                        "default": True,
                        "description": "Include the actual content",
                    },
                },
            },
            handler=shared_context,
        ),
        Tool(
            name="decompose",
            description=(
                "Break a complex query into sub-queries with execution order. "
                "Use for multi-part questions that need to be answered step by step."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Complex question to decompose",
                    },
                    "max_depth": {
                        "type": "integer",
                        "default": 2,
                        "description": "Maximum decomposition depth",
                    },
                },
                "required": ["query"],
            },
            handler=decompose,
        ),
        Tool(
            name="multi_query",
            description=(
                "Execute multiple queries with shared token budget. "
                "More efficient than calling context_query multiple times."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "queries": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"},
                            },
                            "required": ["query"],
                        },
                        "description": "List of queries to execute",
                    },
                    "max_tokens": {
                        "type": "integer",
                        "default": 8000,
                        "description": "Total token budget",
                    },
                },
                "required": ["queries"],
            },
            handler=multi_query,
        ),
        Tool(
            name="multi_project_query",
            description=(
                "Query across multiple projects in your team. "
                "Useful for finding context across related codebases or shared documentation."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query/question to get context for",
                    },
                    "max_tokens": {
                        "type": "integer",
                        "default": 4000,
                        "description": "Maximum tokens to return across all projects",
                    },
                    "per_project_limit": {
                        "type": "integer",
                        "default": 3,
                        "description": "Maximum sections to return per project",
                    },
                    "project_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of project IDs or slugs to include",
                    },
                    "exclude_project_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of project IDs or slugs to exclude",
                    },
                    "search_mode": {
                        "type": "string",
                        "enum": ["keyword", "semantic", "hybrid"],
                        "default": "keyword",
                        "description": "Search strategy",
                    },
                    "include_metadata": {
                        "type": "boolean",
                        "default": True,
                        "description": "Include file paths, line numbers, and relevance scores",
                    },
                },
                "required": ["query"],
            },
            handler=multi_project_query,
        ),
        Tool(
            name="stats",
            description=(
                "Get documentation statistics. Returns file count, line count, and section count."
            ),
            parameters={
                "type": "object",
                "properties": {},
            },
            handler=stats,
        ),
        Tool(
            name="list_templates",
            description=(
                "List available prompt templates from shared collections. "
                "Templates can be used with get_template to generate prompts."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category",
                    },
                },
            },
            handler=list_templates,
        ),
        Tool(
            name="get_template",
            description=(
                "Get and optionally render a prompt template. "
                "Pass variables to substitute placeholders in the template."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "template_id": {
                        "type": "string",
                        "description": "Template ID",
                    },
                    "slug": {
                        "type": "string",
                        "description": "Template slug (alternative to ID)",
                    },
                    "variables": {
                        "type": "object",
                        "additionalProperties": {"type": "string"},
                        "description": "Variables to substitute",
                    },
                },
            },
            handler=get_template,
        ),
        # ============ SESSION MANAGEMENT TOOLS ============
        Tool(
            name="ask",
            description=(
                "Basic documentation query. "
                "Ask a question and get an answer based on the documentation."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question to ask about the documentation",
                    },
                    "correlation_context": CORRELATION_CONTEXT_PARAMETER,
                },
                "required": ["question"],
            },
            handler=ask,
        ),
        Tool(
            name="inject",
            description=(
                "Inject context into the session. "
                "This context will be included in subsequent queries."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "The context to inject",
                    },
                    "append": {
                        "type": "boolean",
                        "default": False,
                        "description": "Append to existing context instead of replacing",
                    },
                },
                "required": ["context"],
            },
            handler=inject,
        ),
        Tool(
            name="context",
            description=(
                "Get the current session context. Returns any context that was previously injected."
            ),
            parameters={
                "type": "object",
                "properties": {},
            },
            handler=get_context,
        ),
        Tool(
            name="clear_context",
            description=(
                "Clear the current session context. Removes any previously injected context."
            ),
            parameters={
                "type": "object",
                "properties": {},
            },
            handler=clear_context,
        ),
        Tool(
            name="settings",
            description=(
                "Get project settings. Returns configuration like max tokens, search mode, etc."
            ),
            parameters={
                "type": "object",
                "properties": {},
            },
            handler=get_settings,
        ),
        Tool(
            name="plan",
            description=(
                "Create an execution plan for a complex query. "
                "Returns a sequence of steps to answer complex multi-part questions."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The complex question to plan for",
                    },
                    "strategy": {
                        "type": "string",
                        "enum": ["breadth_first", "depth_first", "relevance_first"],
                        "default": "relevance_first",
                        "description": "Execution strategy",
                    },
                    "max_tokens": {
                        "type": "integer",
                        "default": 16000,
                        "description": "Total token budget",
                    },
                },
                "required": ["query"],
            },
            handler=plan,
        ),
        # ============ SUMMARY STORAGE TOOLS ============
        Tool(
            name="store_summary",
            description=(
                "Store a summary for a document or section. "
                "Summaries are used to provide concise context in queries."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description": "Path to the document",
                    },
                    "summary": {
                        "type": "string",
                        "description": "The summary text to store",
                    },
                    "summary_type": {
                        "type": "string",
                        "enum": ["concise", "detailed", "technical", "keywords", "custom"],
                        "default": "concise",
                        "description": "Type of summary",
                    },
                    "section_id": {
                        "type": "string",
                        "description": "Optional section identifier",
                    },
                    "line_start": {
                        "type": "integer",
                        "description": "Start line for section summary",
                    },
                    "line_end": {
                        "type": "integer",
                        "description": "End line for section summary",
                    },
                    "generated_by": {
                        "type": "string",
                        "description": "Model that generated the summary",
                    },
                },
                "required": ["document_path", "summary"],
            },
            handler=store_summary,
        ),
        Tool(
            name="get_summaries",
            description=("Get stored summaries. Filter by document path, type, or section."),
            parameters={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description": "Filter by document path",
                    },
                    "summary_type": {
                        "type": "string",
                        "enum": ["concise", "detailed", "technical", "keywords", "custom"],
                        "description": "Filter by summary type",
                    },
                    "section_id": {
                        "type": "string",
                        "description": "Filter by section ID",
                    },
                    "include_content": {
                        "type": "boolean",
                        "default": True,
                        "description": "Include summary content in response",
                    },
                },
            },
            handler=get_summaries,
        ),
        Tool(
            name="delete_summary",
            description=("Delete stored summaries. Delete by ID, document path, or type."),
            parameters={
                "type": "object",
                "properties": {
                    "summary_id": {
                        "type": "string",
                        "description": "Specific summary ID to delete",
                    },
                    "document_path": {
                        "type": "string",
                        "description": "Delete all summaries for document",
                    },
                    "summary_type": {
                        "type": "string",
                        "enum": ["concise", "detailed", "technical", "keywords", "custom"],
                        "description": "Delete summaries of this type",
                    },
                },
            },
            handler=delete_summary,
        ),
        # ============ AGENT MEMORY TOOLS ============
        Tool(
            name="remember",
            description=(
                "Store a memory for later recall. "
                "Memories can be facts, decisions, learnings, preferences, todos, or context. "
                "Use this to persist important information across sessions."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The memory content to store",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["fact", "decision", "learning", "preference", "todo", "context"],
                        "default": "fact",
                        "description": "Type of memory",
                    },
                    "scope": {
                        "type": "string",
                        "enum": ["agent", "project", "team", "user"],
                        "default": "project",
                        "description": "Visibility scope",
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional grouping category",
                    },
                    "ttl_days": {
                        "type": "integer",
                        "description": "Days until memory expires (null = permanent)",
                    },
                    "related_to": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "IDs of related memories",
                    },
                    "document_refs": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Referenced document paths",
                    },
                    "source": {
                        "type": "string",
                        "description": "What created this memory",
                    },
                },
                "required": ["content"],
            },
            handler=remember,
        ),
        Tool(
            name="recall",
            description=(
                "Recall memories semantically. "
                "Search for relevant memories using natural language queries."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "memory_view": {"type": "string", "enum": ["current", "history"], "default": "current", "description": "Explicit retained history or current evidence; history grants no current authority."},
                    "as_of": {"type": "string", "maxLength": 64, "description": "Past ISO timestamp with timezone; requires memory_view=history and current access/retention."},
                    "retrieval_queries": {
                        "type": "array", "maxItems": 4,
                        "items": {"type": "string", "minLength": 1, "maxLength": 512},
                        "description": "Optional source-language translations or question facets; preserve entities and do not assume answers.",
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query for semantic recall",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["fact", "decision", "learning", "preference", "todo", "context"],
                        "description": "Filter by memory type",
                    },
                    "scope": {
                        "type": "string",
                        "enum": ["agent", "project", "team", "user"],
                        "description": "Filter by scope",
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter by category",
                    },
                    "limit": {
                        "type": "integer",
                        "default": 5,
                        "description": "Maximum memories to return",
                    },
                    "min_relevance": {
                        "type": "number",
                        "default": 0.5,
                        "description": "Minimum relevance score (0-1)",
                    },
                    "include_expired": {
                        "type": "boolean",
                        "default": False,
                        "description": "Include expired memories",
                    },
                    "include_inactive": {
                        "type": "boolean",
                        "default": False,
                        "description": "Include inactive memories in the primary results",
                    },
                    "task": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 512,
                        "description": "Optional task label recorded for retrieval/outcome correlation",
                    },
                    "outcome_rerank_mode": {
                        "type": "string",
                        "enum": ["disabled", "shadow", "enabled"],
                        "description": "Optional mode bounded by the server configuration",
                    },
                    "correlation_context": CORRELATION_CONTEXT_PARAMETER,
                },
                "required": ["query"],
            },
            handler=recall,
        ),
        Tool(
            name="memories",
            description=(
                "List stored memories with filters. "
                "Browse memories by type, scope, category, or search text."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["fact", "decision", "learning", "preference", "todo", "context"],
                        "description": "Filter by memory type",
                    },
                    "scope": {
                        "type": "string",
                        "enum": ["agent", "project", "team", "user"],
                        "description": "Filter by scope",
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter by category",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["ACTIVE", "INVALIDATED", "SUPERSEDED"],
                        "description": "Filter by memory lifecycle",
                    },
                    "search": {
                        "type": "string",
                        "description": "Text search in content",
                    },
                    "limit": {
                        "type": "integer",
                        "default": 20,
                        "description": "Maximum memories to return",
                    },
                    "offset": {
                        "type": "integer",
                        "default": 0,
                        "description": "Offset for pagination",
                    },
                    "include_expired": {
                        "type": "boolean",
                        "default": False,
                        "description": "Include expired memories",
                    },
                    "include_inactive": {
                        "type": "boolean",
                        "default": False,
                        "description": "Include inactive memories in the result set",
                    },
                },
            },
            handler=memories,
        ),
        Tool(
            name="memory_invalidate",
            description=(
                "Invalidate a stored memory without deleting it. "
                "Useful when the information is obsolete but should remain discoverable as inactive history."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "memory_id": {
                        "type": "string",
                        "description": "Memory ID to invalidate",
                    },
                    "invalidated_at": {
                        "type": "string",
                        "description": "Optional ISO timestamp for the invalidation event",
                    },
                    "reason": {
                        "type": "string",
                        "description": "Optional reason why the memory is no longer valid",
                    },
                },
                "required": ["memory_id"],
            },
            handler=memory_invalidate,
        ),
        Tool(
            name="memory_supersede",
            description=(
                "Replace an existing memory with updated content. "
                "Creates a new active memory and marks the old one as superseded."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "old_memory_id": {
                        "type": "string",
                        "description": "Memory ID being replaced",
                    },
                    "new_memory_id": {
                        "type": "string",
                        "description": "Memory ID replacing the old one",
                    },
                    "reason": {
                        "type": "string",
                        "description": "Why the previous memory is being superseded",
                    },
                },
                "required": ["old_memory_id", "new_memory_id"],
            },
            handler=memory_supersede,
        ),
        Tool(
            name="forget",
            description=("Delete memories. Remove memories by ID, type, category, or age."),
            parameters={
                "type": "object",
                "properties": {
                    "memory_id": {
                        "type": "string",
                        "description": "Specific memory ID to delete",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["fact", "decision", "learning", "preference", "todo", "context"],
                        "description": "Delete all memories of this type",
                    },
                    "category": {
                        "type": "string",
                        "description": "Delete all memories in this category",
                    },
                    "older_than_days": {
                        "type": "integer",
                        "description": "Delete memories older than N days",
                    },
                },
            },
            handler=forget,
        ),
        # ============ DOCUMENT MANAGEMENT TOOLS ============
        Tool(
            name="upload_document",
            description=(
                "Upload a document to the project. "
                "Creates or updates a document in the documentation store."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Document path",
                    },
                    "content": {
                        "type": "string",
                        "description": "Document content",
                    },
                    "kind": {
                        "type": "string",
                        "enum": ["DOC", "BINARY"],
                        "description": "Optional document kind",
                    },
                    "format": {
                        "type": "string",
                        "description": "Optional document format",
                    },
                    "language": {
                        "type": "string",
                        "description": "Optional language hint",
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional structured document metadata",
                    },
                },
                "required": ["path", "content"],
            },
            handler=upload_document,
        ),
        Tool(
            name="sync_documents",
            description=(
                "Sync multiple documents. "
                "Bulk create/update/delete documents to match provided list."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "documents": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                                "content": {"type": "string"},
                            },
                            "required": ["path", "content"],
                        },
                        "description": "List of documents with path and content",
                    },
                    "delete_missing": {
                        "type": "boolean",
                        "default": False,
                        "description": "Delete documents not in list",
                    },
                },
                "required": ["documents"],
            },
            handler=sync_documents,
        ),
        Tool(
            name="document_tombstones",
            description=(
                "List deleted or pruned document tombstones. "
                "Use this to inspect soft-deleted project context and expiration windows."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "default": 50,
                        "description": "Maximum number of tombstones to return",
                    },
                    "include_expired": {
                        "type": "boolean",
                        "default": False,
                        "description": "Include tombstones past retention but not yet purged",
                    },
                },
            },
            handler=document_tombstones,
        ),
        # ============ INDEX HEALTH & ANALYTICS TOOLS (Sprint 3) ============
        Tool(
            name="index_health",
            description=(
                "Get comprehensive index health metrics for your project. "
                "Returns coverage, quality scores, tier distribution, stale document detection, "
                "and overall health score. Use this to monitor the health of your documentation index."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "stale_threshold_days": {
                        "type": "integer",
                        "default": 30,
                        "description": "Days after which content is considered stale (1-365)",
                    },
                },
            },
            handler=index_health,
        ),
        Tool(
            name="index_recommendations",
            description=(
                "Get actionable recommendations to improve your index health. "
                "Returns prioritized list of recommendations based on current health metrics. "
                "Recommendations include actions like reindexing, improving coverage, and reviewing quality."
            ),
            parameters={
                "type": "object",
                "properties": {},
            },
            handler=index_recommendations,
        ),
        Tool(
            name="reindex",
            description=(
                "Trigger a project reindex job or poll an existing reindex job. "
                "Use this after syncs or when index coverage is degraded."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "Existing job ID to poll instead of creating a new one",
                    },
                    "mode": {
                        "type": "string",
                        "default": "incremental",
                        "description": "Reindex mode when creating a job (incremental or full)",
                    },
                    "kind": {
                        "type": "string",
                        "default": "doc",
                        "description": "Index kind when creating a job (doc or code)",
                    },
                },
            },
            handler=reindex,
        ),
        Tool(
            name="search_analytics",
            description=(
                "Get comprehensive search analytics for your project. "
                "Returns query counts, success rates, latency percentiles (p50/p75/p90/p95/p99), "
                "tool usage breakdown, daily trends, and error analysis."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "default": 30,
                        "description": "Number of days to analyze (1-90)",
                    },
                },
            },
            handler=search_analytics,
        ),
        Tool(
            name="query_trends",
            description=(
                "Get query trends over time with configurable granularity. "
                "Returns time-bucketed query counts, success rates, and latency for trend analysis."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "default": 7,
                        "description": "Number of days to analyze (1-30)",
                    },
                    "granularity": {
                        "type": "string",
                        "enum": ["hour", "day", "week"],
                        "default": "day",
                        "description": "Time bucket size",
                    },
                },
            },
            handler=query_trends,
        ),
    ]

    return legacy_tools + _build_contract_tools(Tool, client, legacy_tools)
