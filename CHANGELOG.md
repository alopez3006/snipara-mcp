# Changelog

## 4.0.2

- Regenerated tool contract: `snipara_help` no longer lists `orchestrator` among `runtimes`. Orchestrator was folded into Companion; the hosted server reports a declared `orchestrator` as retired.

## 4.0.1

- Regenerated tool contract: `include_all_tiers` of `snipara_context_query` is documented as deprecated (every tier is searched).

## 4.0.0

- Remove swarm and hierarchical-task tool wrappers, dispatch branches and public tool definitions, including legacy rlm*task*\* queue aliases.
- Forward memory sources and expose the retained memory lifecycle tools in the regenerated contract.
- Migration: remove calls to deleted swarm, htask and queue tools; rediscover the supported tool contract before updating clients.
