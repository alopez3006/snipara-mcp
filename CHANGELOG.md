# Changelog

## 5.0.0

- Move to version 2 of the MCP Python SDK (`mcp>=2.3.0,<3`). The stdio server answers MCP 2026-07-28 clients as well as the handshake versions up to 2025-11-25. An environment that also needs `mcp<2` keeps 4.0.4.
- Arguments of listed tools are still checked against their schema; the SDK no longer does it. The check adds a direct dependency on `jsonschema`.
- Tool metadata is sent as `_meta`, as MCP defines it. It was sent as `meta`, which clients ignore.
- Remove the `multi_project_query` helper. It called the project endpoint, which does not serve team-wide queries, so it always failed. Use `POST /v1/team/{team_slug}/mcp`.

## 4.0.4

- Regenerated tool contract: `minimum_change_evidence` describes its check object once instead of eleven times, which takes `snipara_context_query` from 6,806 to 1,796 tokens and `snipara_code_impact` from 6,040 to 1,030. The accepted fields are unchanged; the hosted server bounds and filters them. `snipara_remember_if_novel` takes `include_metadata`: the hosted server answers with a compact receipt unless it is true.

## 4.0.3

- Regenerated tool contract: `snipara_remember_if_novel` takes `supersedes`, the memories the new one replaces; they are marked superseded when it is stored.

## 4.0.2

- Regenerated tool contract: `snipara_help` no longer lists `orchestrator` among `runtimes`. Orchestrator was folded into Companion; the hosted server reports a declared `orchestrator` as retired.

## 4.0.1

- Regenerated tool contract: `include_all_tiers` of `snipara_context_query` is documented as deprecated (every tier is searched).

## 4.0.0

- Remove swarm and hierarchical-task tool wrappers, dispatch branches and public tool definitions, including legacy rlm*task*\* queue aliases.
- Forward memory sources and expose the retained memory lifecycle tools in the regenerated contract.
- Migration: remove calls to deleted swarm, htask and queue tools; rediscover the supported tool contract before updating clients.
