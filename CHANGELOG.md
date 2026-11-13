# Changelog

## 4.0.1

- Regenerated tool contract: `include_all_tiers` of `snipara_context_query` is documented as deprecated (every tier is searched).

## 4.0.0

- Remove swarm and hierarchical-task tool wrappers, dispatch branches and public tool definitions, including legacy rlm_task_* queue aliases.
- Forward memory sources and expose the retained memory lifecycle tools in the regenerated contract.
- Migration: remove calls to deleted swarm, htask and queue tools; rediscover the supported tool contract before updating clients.
