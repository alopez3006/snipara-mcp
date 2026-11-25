# Changelog

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
