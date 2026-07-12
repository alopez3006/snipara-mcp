"""Generated MCP tool contract for the snipara-mcp package.

Source of truth: apps/mcp-server/src/mcp/tool_defs.py
Regenerate with: python3 apps/mcp-server/scripts/sync_snipara_mcp_contract.py
"""

from __future__ import annotations

TOOL_DEFINITIONS = [{'name': 'rlm_context_query',
  'description': 'Query project documents, parsed business files, and shared context. Use this '
                 'first for source truth and narrative documentation. Returns a source-grounded '
                 'answer_pack plus retrieval_diagnostics and ranked sections within token budget. '
                 'If a broad query times out, retry once with a narrow 3-8 term query, max_tokens '
                 "800-1500, search_mode='keyword', return_references=true, auto_decompose=false, "
                 'and include_all_tiers=false. For exact text use snipara_search; for structural '
                 'code context use snipara_code_neighbors, snipara_code_callers, or '
                 'snipara_code_imports.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'Documentation, business-context, or '
                                                          'current-truth question. For timeout '
                                                          'recovery, narrow this to the key file, '
                                                          'feature, symbol, or 3-8 terms.'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 100,
                                                'maximum': 100000,
                                                'description': 'Token budget. Use 800-1500 for '
                                                               'fast recovery retries after a '
                                                               'timeout.'},
                                 'search_mode': {'type': 'string',
                                                 'enum': ['keyword', 'semantic', 'hybrid'],
                                                 'default': 'hybrid',
                                                 'description': 'Search strategy. Use keyword for '
                                                                'fast retry/recovery paths; use '
                                                                'hybrid for normal documentation '
                                                                'discovery.'},
                                 'include_metadata': {'type': 'boolean', 'default': True},
                                 'prefer_summaries': {'type': 'boolean', 'default': False},
                                 'return_references': {'type': 'boolean',
                                                       'default': False,
                                                       'description': 'Return chunk references '
                                                                      '(IDs + previews) instead of '
                                                                      'full content. Use '
                                                                      'rlm_get_chunk to retrieve '
                                                                      'full content by ID. Reduces '
                                                                      'hallucination by '
                                                                      'maintaining clear source '
                                                                      'attribution and is the '
                                                                      'preferred fast retry path '
                                                                      'after a timeout.'},
                                 'include_answer_pack': {'type': 'boolean',
                                                         'default': True,
                                                         'description': 'Include a structured '
                                                                        'answer pack with source '
                                                                        'facts, caveats, '
                                                                        'verification checklist, '
                                                                        'and code/context hints '
                                                                        'before the ranked context '
                                                                        'sections.'},
                                 'auto_decompose': {'type': 'boolean',
                                                    'default': True,
                                                    'description': 'Auto-decompose complex queries '
                                                                   'into sub-queries (Pro+ only). '
                                                                   'Complex queries (50+ words, '
                                                                   'multiple questions, '
                                                                   'comparisons) are automatically '
                                                                   'broken down and results '
                                                                   'merged. Set to False for fast '
                                                                   'timeout recovery retries.'},
                                 'include_all_tiers': {'type': 'boolean',
                                                       'default': False,
                                                       'description': 'Include all context tiers '
                                                                      'including COLD and ARCHIVE. '
                                                                      'By default, searches only '
                                                                      'HOT and WARM tiers for '
                                                                      'faster, more relevant '
                                                                      'results.'},
                                 'task': {'type': 'string',
                                          'minLength': 1,
                                          'maxLength': 512,
                                          'description': 'Optional task label that scopes the '
                                                         'live-join fallback and retrieval '
                                                         'correlation; persisted outcome posterior '
                                                         'statistics remain project-wide'},
                                 'context_chunk_outcome_rerank_mode': {'type': 'string',
                                                                       'enum': ['disabled',
                                                                                'shadow',
                                                                                'enabled'],
                                                                       'default': 'disabled',
                                                                       'description': 'Requested '
                                                                                      'bounded '
                                                                                      'chunk-outcome '
                                                                                      'rerank '
                                                                                      'mode. This '
                                                                                      'request can '
                                                                                      'disable or '
                                                                                      'lower the '
                                                                                      'server-configured '
                                                                                      'mode but '
                                                                                      'cannot '
                                                                                      'escalate '
                                                                                      'beyond it.'},
                                 'context_chunk_outcome_window_hours': {'type': 'integer',
                                                                        'default': 72,
                                                                        'minimum': 1,
                                                                        'maximum': 336,
                                                                        'description': 'Strict '
                                                                                       'attribution '
                                                                                       'window for '
                                                                                       'compatible '
                                                                                       'chunk '
                                                                                       'outcomes.'},
                                 'correlation_context': {'type': 'object',
                                                         'additionalProperties': False,
                                                         'description': 'Optional '
                                                                        'retrieval-correlation '
                                                                        'context. Reuse session_id '
                                                                        'across retrieval and '
                                                                        'outcome calls so '
                                                                        'telemetry can be joined '
                                                                        'inside the authenticated '
                                                                        'project. These '
                                                                        'identifiers never change '
                                                                        'authorization or project '
                                                                        'scope; do not include '
                                                                        'secrets, tenant IDs, or '
                                                                        'user data.',
                                                         'properties': {'version': {'type': 'string',
                                                                                    'enum': ['retrieval-correlation-v1'],
                                                                                    'default': 'retrieval-correlation-v1'},
                                                                        'session_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Preferred '
                                                                                                      'stable '
                                                                                                      'opaque '
                                                                                                      'session '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'for '
                                                                                                      'telemetry '
                                                                                                      'association.'},
                                                                        'workflow_session_id': {'type': 'string',
                                                                                                'minLength': 1,
                                                                                                'maxLength': 128,
                                                                                                'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                                'description': 'Opaque '
                                                                                                               'workflow '
                                                                                                               'ID '
                                                                                                               'used '
                                                                                                               'when '
                                                                                                               'session_id '
                                                                                                               'is '
                                                                                                               'absent.'},
                                                                        'correlation_id': {'type': 'string',
                                                                                           'minLength': 1,
                                                                                           'maxLength': 128,
                                                                                           'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                           'description': 'Opaque '
                                                                                                          'request-chain '
                                                                                                          'ID '
                                                                                                          'used '
                                                                                                          'when '
                                                                                                          'session '
                                                                                                          'fields '
                                                                                                          'are '
                                                                                                          'absent.'},
                                                                        'request_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Opaque '
                                                                                                      'per-call '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'only '
                                                                                                      'as '
                                                                                                      'a '
                                                                                                      'final '
                                                                                                      'telemetry '
                                                                                                      'fallback.'}}}},
                  'required': ['query']},
  'annotations': {'title': 'Query Snipara context',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 24.0,
            'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_context_query'},
  'exposed': False},
 {'name': 'rlm_ask',
  'description': 'Query documentation with a question (basic). Use rlm_context_query for better '
                 'results.',
  'alias_of': 'rlm_context_query',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string', 'description': 'The question to ask'},
                                 'correlation_context': {'type': 'object',
                                                         'additionalProperties': False,
                                                         'description': 'Optional '
                                                                        'retrieval-correlation '
                                                                        'context. Reuse session_id '
                                                                        'across retrieval and '
                                                                        'outcome calls so '
                                                                        'telemetry can be joined '
                                                                        'inside the authenticated '
                                                                        'project. These '
                                                                        'identifiers never change '
                                                                        'authorization or project '
                                                                        'scope; do not include '
                                                                        'secrets, tenant IDs, or '
                                                                        'user data.',
                                                         'properties': {'version': {'type': 'string',
                                                                                    'enum': ['retrieval-correlation-v1'],
                                                                                    'default': 'retrieval-correlation-v1'},
                                                                        'session_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Preferred '
                                                                                                      'stable '
                                                                                                      'opaque '
                                                                                                      'session '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'for '
                                                                                                      'telemetry '
                                                                                                      'association.'},
                                                                        'workflow_session_id': {'type': 'string',
                                                                                                'minLength': 1,
                                                                                                'maxLength': 128,
                                                                                                'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                                'description': 'Opaque '
                                                                                                               'workflow '
                                                                                                               'ID '
                                                                                                               'used '
                                                                                                               'when '
                                                                                                               'session_id '
                                                                                                               'is '
                                                                                                               'absent.'},
                                                                        'correlation_id': {'type': 'string',
                                                                                           'minLength': 1,
                                                                                           'maxLength': 128,
                                                                                           'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                           'description': 'Opaque '
                                                                                                          'request-chain '
                                                                                                          'ID '
                                                                                                          'used '
                                                                                                          'when '
                                                                                                          'session '
                                                                                                          'fields '
                                                                                                          'are '
                                                                                                          'absent.'},
                                                                        'request_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Opaque '
                                                                                                      'per-call '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'only '
                                                                                                      'as '
                                                                                                      'a '
                                                                                                      'final '
                                                                                                      'telemetry '
                                                                                                      'fallback.'}}}},
                  'required': ['query']},
  '_meta': {'snipara_tool_weight': -6.0,
            'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_ask'},
  'exposed': False},
 {'name': 'rlm_search',
  'description': 'Search indexed documentation with an exact regex pattern. This is a grep-like '
                 'text search, not semantic retrieval; use rlm_context_query(query=...) for '
                 'source-truth semantic/context search.',
  'inputSchema': {'type': 'object',
                  'properties': {'pattern': {'type': 'string',
                                             'description': 'Regex text pattern to search for.'},
                                 'query': {'type': 'string',
                                           'description': 'Alias for pattern for clients that '
                                                          'normalize search inputs to query.'},
                                 'max_results': {'type': 'integer',
                                                 'default': 20,
                                                 'minimum': 1,
                                                 'maximum': 100,
                                                 'description': 'Maximum regex matches to return.'},
                                 'correlation_context': {'type': 'object',
                                                         'additionalProperties': False,
                                                         'description': 'Optional '
                                                                        'retrieval-correlation '
                                                                        'context. Reuse session_id '
                                                                        'across retrieval and '
                                                                        'outcome calls so '
                                                                        'telemetry can be joined '
                                                                        'inside the authenticated '
                                                                        'project. These '
                                                                        'identifiers never change '
                                                                        'authorization or project '
                                                                        'scope; do not include '
                                                                        'secrets, tenant IDs, or '
                                                                        'user data.',
                                                         'properties': {'version': {'type': 'string',
                                                                                    'enum': ['retrieval-correlation-v1'],
                                                                                    'default': 'retrieval-correlation-v1'},
                                                                        'session_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Preferred '
                                                                                                      'stable '
                                                                                                      'opaque '
                                                                                                      'session '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'for '
                                                                                                      'telemetry '
                                                                                                      'association.'},
                                                                        'workflow_session_id': {'type': 'string',
                                                                                                'minLength': 1,
                                                                                                'maxLength': 128,
                                                                                                'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                                'description': 'Opaque '
                                                                                                               'workflow '
                                                                                                               'ID '
                                                                                                               'used '
                                                                                                               'when '
                                                                                                               'session_id '
                                                                                                               'is '
                                                                                                               'absent.'},
                                                                        'correlation_id': {'type': 'string',
                                                                                           'minLength': 1,
                                                                                           'maxLength': 128,
                                                                                           'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                           'description': 'Opaque '
                                                                                                          'request-chain '
                                                                                                          'ID '
                                                                                                          'used '
                                                                                                          'when '
                                                                                                          'session '
                                                                                                          'fields '
                                                                                                          'are '
                                                                                                          'absent.'},
                                                                        'request_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Opaque '
                                                                                                      'per-call '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'only '
                                                                                                      'as '
                                                                                                      'a '
                                                                                                      'final '
                                                                                                      'telemetry '
                                                                                                      'fallback.'}}}},
                  'required': []},
  '_meta': {'snipara_tool_weight': 4.0,
            'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_search'},
  'exposed': False},
 {'name': 'rlm_read',
  'description': 'Read specific lines from indexed documentation. Pass file_path to read a '
                 'document-local line range; omit file_path to read global indexed lines.',
  'inputSchema': {'type': 'object',
                  'properties': {'file_path': {'type': 'string',
                                               'description': 'Indexed document path. Also '
                                                              'accepted by the handler as file, '
                                                              'path, or document.'},
                                 'start_line': {'type': 'integer',
                                                'default': 1,
                                                'description': 'Starting line number. Relative to '
                                                               'file_path when provided; otherwise '
                                                               'global index line.'},
                                 'end_line': {'type': 'integer',
                                              'description': 'Ending line number. Defaults to '
                                                             'start_line + 50.'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_read'}},
 {'name': 'rlm_code_callers',
  'description': 'USE WHEN: who calls this symbol, especially before renaming, deleting, or '
                 'changing a signature. Hosted fallback/canonical indexed graph: if you have shell '
                 'access and local commits or a dirty working tree may matter, run '
                 '`snipara-companion code callers` first because it auto-selects the local '
                 'overlay; use this MCP tool when companion is unavailable or after push/reindex.',
  'inputSchema': {'type': 'object',
                  'properties': {'qualified_name': {'type': 'string',
                                                    'description': 'Repo-qualified symbol name'},
                                 'symbol_key': {'type': 'string',
                                                'description': 'Stable symbol key for an exact '
                                                               'match'},
                                 'depth': {'type': 'integer',
                                           'default': 1,
                                           'minimum': 1,
                                           'maximum': 4},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 200},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Find code callers',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 6.0,
            'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_code_callers'},
  'exposed': False},
 {'name': 'rlm_code_imports',
  'description': 'USE WHEN: what a file or symbol imports, or who imports a module before moving '
                 'or renaming it. Hosted fallback/canonical indexed graph: if you have shell '
                 'access and local commits or a dirty working tree may matter, run '
                 '`snipara-companion code imports` first because it auto-selects the local '
                 'overlay; use this MCP tool when companion is unavailable or after push/reindex.',
  'inputSchema': {'type': 'object',
                  'properties': {'qualified_name': {'type': 'string',
                                                    'description': 'Repo-qualified symbol name'},
                                 'symbol_key': {'type': 'string',
                                                'description': 'Stable symbol key for an exact '
                                                               'match'},
                                 'file_path': {'type': 'string',
                                               'description': 'Resolve imports for a specific file '
                                                              'path'},
                                 'direction': {'type': 'string',
                                               'enum': ['out', 'in'],
                                               'default': 'out'},
                                 'include_file_nodes': {'type': 'boolean',
                                                        'default': False,
                                                        'description': 'For file_path lookups, '
                                                                       'include every scanned '
                                                                       'symbol in matched_targets '
                                                                       'instead of the compact '
                                                                       'module anchor'},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 200},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Inspect code imports',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 6.0,
            'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_code_imports'},
  'exposed': False},
 {'name': 'rlm_code_neighbors',
  'description': 'USE WHEN: getting oriented in unfamiliar code before editing; returns nearby '
                 'callers, callees, imports, and references within N hops. Hosted '
                 'fallback/canonical indexed graph: if you have shell access and local commits or '
                 'a dirty working tree may matter, run `snipara-companion code neighbors` first '
                 'because it auto-selects the local overlay; use this MCP tool when companion is '
                 'unavailable or after push/reindex.',
  'inputSchema': {'type': 'object',
                  'properties': {'qualified_name': {'type': 'string',
                                                    'description': 'Repo-qualified symbol name'},
                                 'symbol_key': {'type': 'string',
                                                'description': 'Stable symbol key for an exact '
                                                               'match'},
                                 'depth': {'type': 'integer',
                                           'default': 2,
                                           'minimum': 1,
                                           'maximum': 4},
                                 'edge_kinds': {'type': 'array',
                                                'items': {'type': 'string',
                                                          'enum': ['CALLS',
                                                                   'CONTAINS',
                                                                   'IMPORTS',
                                                                   'REFERENCES']},
                                                'description': 'Optional edge kinds to include'},
                                 'limit': {'type': 'integer',
                                           'default': 200,
                                           'minimum': 1,
                                           'maximum': 500},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Inspect nearby code graph',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 6.0,
            'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_code_neighbors'},
  'exposed': False},
 {'name': 'rlm_code_shortest_path',
  'description': 'USE WHEN: how is A connected to B, such as whether a route reaches a service or '
                 'a handler touches a model. Returns the shortest call/import/reference path from '
                 'the indexed hosted code graph. If you have shell access and local commits or a '
                 'dirty working tree may matter, run `snipara-companion code shortest-path` first; '
                 'use this MCP tool when companion is unavailable or after push/reindex.',
  'inputSchema': {'type': 'object',
                  'properties': {'from': {'type': 'string',
                                          'description': 'Source repo-qualified symbol name'},
                                 'from_symbol_key': {'type': 'string',
                                                     'description': 'Exact source symbol key'},
                                 'to': {'type': 'string',
                                        'description': 'Target repo-qualified symbol name'},
                                 'to_symbol_key': {'type': 'string',
                                                   'description': 'Exact target symbol key'},
                                 'edge_kinds': {'type': 'array',
                                                'items': {'type': 'string',
                                                          'enum': ['CALLS',
                                                                   'CONTAINS',
                                                                   'IMPORTS',
                                                                   'REFERENCES']},
                                                'description': 'Optional edge kinds to traverse'},
                                 'max_hops': {'type': 'integer',
                                              'default': 6,
                                              'minimum': 1,
                                              'maximum': 12},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Find code graph path',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_code_shortest_path'}},
 {'name': 'rlm_code_symbol_card',
  'description': 'USE WHEN: about to edit an important symbol, especially route, service, job, '
                 'auth, billing, or schema-adjacent code. Returns role, layer, framework, risk, '
                 'freshness, and related tests/docs/routes/config hints from the indexed hosted '
                 'graph.',
  'inputSchema': {'type': 'object',
                  'properties': {'qualified_name': {'type': 'string',
                                                    'description': 'Repo-qualified symbol name'},
                                 'symbol_key': {'type': 'string',
                                                'description': 'Stable symbol key for an exact '
                                                               'match'},
                                 'limit': {'type': 'integer',
                                           'default': 20,
                                           'minimum': 1,
                                           'maximum': 100},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Load agent code symbol card',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_code_symbol_card'}},
 {'name': 'rlm_code_impact',
  'description': 'USE WHEN: what breaks if this changes; run before risky edits, PR reviews, '
                 'routes/services/jobs work, or explicit gap analysis. Primary code surface for '
                 'local work is `snipara-companion code impact`: if you have shell access and '
                 'local commits or a dirty working tree may matter, run that first because it '
                 'auto-selects local_overlay. Use this hosted MCP tool as the fallback when '
                 'companion is unavailable, or after push/reindex for the canonical hosted graph. '
                 'Pass changed_files for a committed diff or PR file list.',
  'inputSchema': {'type': 'object',
                  'properties': {'qualified_name': {'type': 'string',
                                                    'description': 'Repo-qualified symbol name'},
                                 'symbol_key': {'type': 'string',
                                                'description': 'Stable symbol key for an exact '
                                                               'match'},
                                 'file_path': {'type': 'string',
                                               'description': 'Analyze impact for all indexed '
                                                              'symbols in this file'},
                                 'changed_files': {'type': 'array',
                                                   'items': {'type': 'string'},
                                                   'description': 'Analyze impact across multiple '
                                                                  'changed files, such as a PR '
                                                                  'diff file list'},
                                 'diff_summary': {'type': 'string',
                                                  'description': 'Optional natural-language '
                                                                 'summary of the change or PR'},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 200},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Analyze code change impact',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 8.0,
            'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_code_impact'},
  'exposed': False},
 {'name': 'rlm_local_code_overlay_upload',
  'description': 'Upload a non-canonical local code overlay manifest produced by '
                 'snipara-companion. This stores local working tree or local commit metadata '
                 'separately from the canonical hosted code graph.',
  'inputSchema': {'type': 'object',
                  'properties': {'overlay': {'type': 'object',
                                             'description': 'The snipara.local_code_overlay.v1 '
                                                            'manifest to store.'},
                                 'source_client': {'type': 'string',
                                                   'default': 'snipara-companion',
                                                   'description': 'Client that generated the '
                                                                  'overlay.'},
                                 'session_id': {'type': 'string',
                                                'description': 'Optional local agent/session '
                                                               'identifier for correlation.'},
                                 'ttl_hours': {'type': 'integer',
                                               'default': 48,
                                               'minimum': 1,
                                               'maximum': 168,
                                               'description': 'How long the uploaded overlay '
                                                              'should remain active.'},
                                 'retire_previous': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Retire older active overlays '
                                                                    'for the same repository and '
                                                                    'branch.'}},
                  'required': ['overlay']},
  'annotations': {'title': 'Upload local code overlay',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': False,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_local_code_overlay_upload'}},
 {'name': 'rlm_local_code_overlay_status',
  'description': 'List active hosted local code overlays for this project. Results are '
                 'non-canonical and do not change what snipara_code_* tools query.',
  'inputSchema': {'type': 'object',
                  'properties': {'repository_id': {'type': 'string'},
                                 'branch': {'type': 'string'},
                                 'local_head_sha': {'type': 'string'},
                                 'dirty_tree_hash': {'type': 'string'},
                                 'limit': {'type': 'integer',
                                           'default': 5,
                                           'minimum': 1,
                                           'maximum': 50}},
                  'required': []},
  'annotations': {'title': 'List local code overlays',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_local_code_overlay_status'}},
 {'name': 'rlm_local_code_overlay_get',
  'description': 'Fetch one hosted local code overlay by id or latest matching filters. Use '
                 'include_graph=true only when the full local overlay payload is needed.',
  'inputSchema': {'type': 'object',
                  'properties': {'overlay_id': {'type': 'string'},
                                 'repository_id': {'type': 'string'},
                                 'branch': {'type': 'string'},
                                 'local_head_sha': {'type': 'string'},
                                 'dirty_tree_hash': {'type': 'string'},
                                 'include_graph': {'type': 'boolean', 'default': False}},
                  'required': []},
  'annotations': {'title': 'Fetch local code overlay',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_local_code_overlay_get'}},
 {'name': 'rlm_local_code_overlay_retire',
  'description': 'Retire a hosted local code overlay without deleting historical records. Use this '
                 'when local overlay metadata is superseded before TTL expiry.',
  'inputSchema': {'type': 'object',
                  'properties': {'overlay_id': {'type': 'string'},
                                 'repository_id': {'type': 'string'},
                                 'branch': {'type': 'string'},
                                 'local_head_sha': {'type': 'string'},
                                 'dirty_tree_hash': {'type': 'string'},
                                 'all_matching': {'type': 'boolean',
                                                  'default': False,
                                                  'description': 'Retire every active overlay '
                                                                 'matching the filters instead of '
                                                                 'the latest one.'}},
                  'required': []},
  'annotations': {'title': 'Retire local code overlay',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': False,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_local_code_overlay_retire'}},
 {'name': 'rlm_decompose',
  'description': 'Break complex query into sub-queries with execution order.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string', 'maxLength': 20480},
                                 'max_depth': {'type': 'integer',
                                               'default': 2,
                                               'minimum': 1,
                                               'maximum': 5},
                                 'hints': {'type': 'array',
                                           'items': {'type': 'string', 'maxLength': 512},
                                           'maxItems': 10}},
                  'required': ['query']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_decompose'}},
 {'name': 'rlm_multi_query',
  'description': 'Execute multiple queries in one call with shared token budget.',
  'inputSchema': {'type': 'object',
                  'properties': {'queries': {'type': 'array',
                                             'items': {'type': 'object',
                                                       'properties': {'query': {'type': 'string',
                                                                                'maxLength': 20480},
                                                                      'max_tokens': {'type': 'integer',
                                                                                     'minimum': 50,
                                                                                     'maximum': 20000}},
                                                       'required': ['query']},
                                             'minItems': 1,
                                             'maxItems': 10},
                                 'max_tokens': {'type': 'integer',
                                                'default': 8000,
                                                'minimum': 500,
                                                'maximum': 50000}},
                  'required': ['queries']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_multi_query'}},
 {'name': 'rlm_plan',
  'description': 'Generate full execution plan for complex questions. Returns steps for '
                 'decomposition, context queries, and synthesis.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'The complex question to plan for'},
                                 'strategy': {'type': 'string',
                                              'enum': ['breadth_first',
                                                       'depth_first',
                                                       'relevance_first'],
                                              'default': 'relevance_first',
                                              'description': 'Execution strategy'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 16000,
                                                'minimum': 1000,
                                                'maximum': 100000}},
                  'required': ['query']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_plan'}},
 {'name': 'rlm_multi_project_query',
  'description': 'Query across projects in a team. Requires a service account key.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string', 'description': 'Question or topic'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 100,
                                                'maximum': 100000},
                                 'per_project_limit': {'type': 'integer',
                                                       'default': 3,
                                                       'minimum': 1,
                                                       'maximum': 20},
                                 'project_ids': {'type': 'array',
                                                 'items': {'type': 'string'},
                                                 'description': 'Optional project IDs/slugs to '
                                                                'include'},
                                 'exclude_project_ids': {'type': 'array',
                                                         'items': {'type': 'string'},
                                                         'description': 'Optional project '
                                                                        'IDs/slugs to exclude'},
                                 'search_mode': {'type': 'string',
                                                 'enum': ['keyword', 'semantic', 'hybrid'],
                                                 'default': 'keyword'},
                                 'include_metadata': {'type': 'boolean', 'default': True},
                                 'prefer_summaries': {'type': 'boolean', 'default': False}},
                  'required': ['query']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_multi_project_query'}},
 {'name': 'rlm_inject',
  'description': 'Set session context for subsequent queries.',
  'inputSchema': {'type': 'object',
                  'properties': {'context': {'type': 'string'},
                                 'append': {'type': 'boolean', 'default': False}},
                  'required': ['context']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_inject'}},
 {'name': 'rlm_context',
  'description': 'Show current session context.',
  'inputSchema': {'type': 'object', 'properties': {}, 'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_context'}},
 {'name': 'rlm_clear_context',
  'description': 'Clear session context.',
  'inputSchema': {'type': 'object', 'properties': {}, 'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_clear_context'}},
 {'name': 'rlm_stats',
  'description': 'Show compact documentation statistics. File lists and DB-backed index health are '
                 'opt-in so interactive stats calls stay small and fast.',
  'inputSchema': {'type': 'object',
                  'properties': {'include_files': {'type': 'boolean',
                                                   'default': False,
                                                   'description': 'Include a capped sample of '
                                                                  'indexed file paths.'},
                                 'max_files': {'type': 'integer',
                                               'default': 25,
                                               'minimum': 0,
                                               'maximum': 200,
                                               'description': 'Maximum file paths to include when '
                                                              'include_files=true.'},
                                 'include_index_health': {'type': 'boolean',
                                                          'default': False,
                                                          'description': 'Include a compact '
                                                                         'DB-backed index-health '
                                                                         'snapshot. For full '
                                                                         'health, call '
                                                                         'rlm_index_health.'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_stats'}},
 {'name': 'rlm_sections',
  'description': 'List indexed document sections with optional pagination and filtering.',
  'inputSchema': {'type': 'object',
                  'properties': {'limit': {'type': 'integer',
                                           'description': 'Maximum sections to return (default: '
                                                          '50, max: 500)'},
                                 'offset': {'type': 'integer',
                                            'description': 'Number of sections to skip for '
                                                           'pagination (default: 0)'},
                                 'filter': {'type': 'string',
                                            'description': 'Filter sections by title prefix '
                                                           '(case-insensitive)'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_sections'}},
 {'name': 'rlm_settings',
  'description': 'Get current project settings from dashboard (max_tokens, search_mode, etc.).',
  'inputSchema': {'type': 'object',
                  'properties': {'refresh': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Force refresh from API'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_settings'}},
 {'name': 'rlm_help',
  'description': 'Get intelligent tool recommendations based on what you want to do. Helps '
                 'discover the right tool for your task.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'Describe what you want to do (e.g., '
                                                          "'search across all team projects', "
                                                          "'remember a decision')"},
                                 'tool': {'type': 'string',
                                          'description': 'Get detailed info about a specific tool '
                                                         "(e.g., 'rlm_context_query')"},
                                 'tier': {'type': 'string',
                                          'enum': ['primary',
                                                   'power_user',
                                                   'team',
                                                   'utility',
                                                   'advanced'],
                                          'description': 'List all tools in a specific tier'},
                                 'list_all': {'type': 'boolean',
                                              'default': False,
                                              'description': 'Return a deterministic catalog of '
                                                             'all tools available to this caller'},
                                 'limit': {'type': 'integer',
                                           'default': 5,
                                           'minimum': 1,
                                           'maximum': 20,
                                           'description': 'Maximum recommendations to return'}},
                  'required': []},
  '_meta': {'snipara_tool_weight': 3.0,
            'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_help'},
  'exposed': False},
 {'name': 'rlm_store_summary',
  'description': 'Store an LLM-generated summary for a document.',
  'inputSchema': {'type': 'object',
                  'properties': {'document_path': {'type': 'string'},
                                 'summary': {'type': 'string'},
                                 'summary_type': {'type': 'string',
                                                  'enum': ['concise',
                                                           'detailed',
                                                           'technical',
                                                           'keywords',
                                                           'custom'],
                                                  'default': 'concise'},
                                 'generated_by': {'type': 'string'}},
                  'required': ['document_path', 'summary']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_store_summary'}},
 {'name': 'rlm_get_summaries',
  'description': 'Retrieve stored summaries.',
  'inputSchema': {'type': 'object',
                  'properties': {'document_path': {'type': 'string'},
                                 'summary_type': {'type': 'string',
                                                  'enum': ['concise',
                                                           'detailed',
                                                           'technical',
                                                           'keywords',
                                                           'custom']},
                                 'include_content': {'type': 'boolean', 'default': True}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_get_summaries'}},
 {'name': 'rlm_delete_summary',
  'description': 'Delete stored summaries.',
  'inputSchema': {'type': 'object',
                  'properties': {'summary_id': {'type': 'string'},
                                 'document_path': {'type': 'string'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_delete_summary'}},
 {'name': 'rlm_shared_context',
  'description': 'Load project-linked shared standards, business playbooks, and reusable guidance. '
                 'Use for linked source documents, not durable memory.',
  'inputSchema': {'type': 'object',
                  'properties': {'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 100,
                                                'maximum': 100000},
                                 'categories': {'type': 'array',
                                                'items': {'type': 'string',
                                                          'enum': ['MANDATORY',
                                                                   'BEST_PRACTICES',
                                                                   'GUIDELINES',
                                                                   'REFERENCE']},
                                                'description': 'Filter by categories (default: '
                                                               'all)'},
                                 'include_content': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Include merged content'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_shared_context'}},
 {'name': 'rlm_list_templates',
  'description': 'List available prompt templates from shared collections.',
  'inputSchema': {'type': 'object',
                  'properties': {'category': {'type': 'string',
                                              'description': 'Filter by category'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_list_templates'}},
 {'name': 'rlm_get_template',
  'description': 'Get a specific prompt template by ID or slug. Optionally render with variables.',
  'inputSchema': {'type': 'object',
                  'properties': {'template_id': {'type': 'string', 'description': 'Template ID'},
                                 'slug': {'type': 'string', 'description': 'Template slug'},
                                 'variables': {'type': 'object',
                                               'additionalProperties': {'type': 'string'},
                                               'description': 'Variables to substitute in '
                                                              'template'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_get_template'}},
 {'name': 'rlm_list_collections',
  'description': 'List all shared context collections accessible to you. Returns collections you '
                 "own, team collections you're a member of, and public collections. Use this to "
                 'find collection IDs for uploading documents.',
  'inputSchema': {'type': 'object',
                  'properties': {'include_public': {'type': 'boolean',
                                                    'default': True,
                                                    'description': 'Include public collections in '
                                                                   'the results'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_list_collections'}},
 {'name': 'rlm_create_collection',
  'description': "Create a new TEAM shared context collection in the current project's team. Use "
                 'this to separate project-specific best practices from broader team context.',
  'inputSchema': {'type': 'object',
                  'properties': {'name': {'type': 'string',
                                          'description': 'Collection display name'},
                                 'slug': {'type': 'string',
                                          'description': 'Optional collection slug. Defaults to a '
                                                         'slugified version of name.'},
                                 'description': {'type': 'string',
                                                 'description': 'Optional collection description'},
                                 'is_public': {'type': 'boolean',
                                               'default': False,
                                               'description': 'Whether the collection should be '
                                                              'public'}},
                  'required': ['name']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_create_collection'}},
 {'name': 'rlm_get_collection_documents',
  'description': 'Inspect the documents stored in a shared context collection, including optional '
                 'full content. Use this before copying or splitting mixed collections.',
  'inputSchema': {'type': 'object',
                  'properties': {'collection_id': {'type': 'string',
                                                   'description': 'The shared collection ID'},
                                 'include_content': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Include the full document '
                                                                    'content in the response'}},
                  'required': ['collection_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_get_collection_documents'}},
 {'name': 'rlm_link_collection',
  'description': 'Link an existing shared collection to a project you can access. Defaults to the '
                 'current project when project_id_or_slug is omitted.',
  'inputSchema': {'type': 'object',
                  'properties': {'collection_id': {'type': 'string',
                                                   'description': 'The shared collection ID'},
                                 'project_id_or_slug': {'type': 'string',
                                                        'description': 'Optional target project '
                                                                       'ID, slug, or github repo. '
                                                                       'Defaults to the current '
                                                                       'project.'},
                                 'priority': {'type': 'integer',
                                              'minimum': 0,
                                              'description': 'Optional link priority (lower = '
                                                             'higher priority)'},
                                 'token_budget_percent': {'type': 'integer',
                                                          'minimum': 0,
                                                          'maximum': 100,
                                                          'description': 'Optional token budget '
                                                                         'override for this '
                                                                         'collection'},
                                 'enabled_categories': {'type': 'array',
                                                        'items': {'type': 'string',
                                                                  'enum': ['MANDATORY',
                                                                           'BEST_PRACTICES',
                                                                           'GUIDELINES',
                                                                           'REFERENCE']},
                                                        'description': 'Optional category '
                                                                       'allowlist for this project '
                                                                       'link'}},
                  'required': ['collection_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_link_collection'}},
 {'name': 'rlm_unlink_collection',
  'description': 'Unlink a shared collection from a project you can access. Defaults to the '
                 'current project when project_id_or_slug is omitted.',
  'inputSchema': {'type': 'object',
                  'properties': {'collection_id': {'type': 'string',
                                                   'description': 'The shared collection ID'},
                                 'project_id_or_slug': {'type': 'string',
                                                        'description': 'Optional target project '
                                                                       'ID, slug, or github repo. '
                                                                       'Defaults to the current '
                                                                       'project.'}},
                  'required': ['collection_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_unlink_collection'}},
 {'name': 'rlm_upload_shared_document',
  'description': 'Upload or update a document in a shared context collection. Use for team best '
                 'practices, coding standards, business playbooks, reusable examples, and '
                 'guidelines. Requires Team plan or higher.',
  'inputSchema': {'type': 'object',
                  'properties': {'collection_id': {'type': 'string',
                                                   'description': 'The shared collection ID'},
                                 'title': {'type': 'string', 'description': 'Document title'},
                                 'content': {'type': 'string',
                                             'description': 'Document content (markdown)'},
                                 'category': {'type': 'string',
                                              'enum': ['MANDATORY',
                                                       'BEST_PRACTICES',
                                                       'GUIDELINES',
                                                       'REFERENCE'],
                                              'default': 'BEST_PRACTICES',
                                              'description': 'Document category for token budget '
                                                             'allocation'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Tags for filtering and organization'},
                                 'priority': {'type': 'integer',
                                              'default': 0,
                                              'minimum': 0,
                                              'maximum': 100,
                                              'description': 'Priority within category (higher = '
                                                             'more important)'}},
                  'required': ['collection_id', 'title', 'content']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_upload_shared_document'}},
 {'name': 'rlm_list_business_collections',
  'description': 'List Team Business Context collections for the current team, including Business '
                 'Response Playbook, Business Library, Offer Templates, Company Presentations, and '
                 'Reference Diagrams. Use this before uploading reusable business knowledge.',
  'inputSchema': {'type': 'object',
                  'properties': {'include_custom': {'type': 'boolean',
                                                    'default': False,
                                                    'description': 'Also include custom '
                                                                   'collections that look '
                                                                   'business-oriented. Preset '
                                                                   'business collections are '
                                                                   'always included.'},
                                 'include_missing_presets': {'type': 'boolean',
                                                             'default': True,
                                                             'description': 'Return missing preset '
                                                                            'definitions so the '
                                                                            'caller can create '
                                                                            'them with '
                                                                            'rlm_ensure_business_collection.'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_list_business_collections'}},
 {'name': 'rlm_ensure_business_collection',
  'description': 'Create or return an existing Team Business Context collection. Prefer preset '
                 'slugs for the standard workspace business library.',
  'inputSchema': {'type': 'object',
                  'properties': {'preset': {'type': 'string',
                                            'enum': ['business_response_playbook',
                                                     'business_library',
                                                     'offer_templates',
                                                     'company_presentations',
                                                     'reference_diagrams'],
                                            'description': 'Standard Team Business Context preset '
                                                           'to create or return.'},
                                 'name': {'type': 'string',
                                          'description': 'Custom collection display name. Required '
                                                         'when preset is omitted.'},
                                 'slug': {'type': 'string',
                                          'description': 'Custom collection slug. Defaults to a '
                                                         'slugified name.'},
                                 'description': {'type': 'string',
                                                 'description': 'Optional collection description'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_ensure_business_collection'}},
 {'name': 'rlm_upload_business_document',
  'description': 'Upload or update a reusable document in a Team Business Context collection. For '
                 'current client/project files with metadata, use rlm_upload_document instead.',
  'inputSchema': {'type': 'object',
                  'properties': {'collection_id': {'type': 'string',
                                                   'description': 'Business collection ID. If '
                                                                  'omitted, provide preset or '
                                                                  'collection_slug.'},
                                 'preset': {'type': 'string',
                                            'enum': ['business_response_playbook',
                                                     'business_library',
                                                     'offer_templates',
                                                     'company_presentations',
                                                     'reference_diagrams'],
                                            'description': 'Business preset to resolve or create '
                                                           'before upload.'},
                                 'collection_slug': {'type': 'string',
                                                     'description': 'Business collection slug to '
                                                                    'resolve when collection_id is '
                                                                    'omitted.'},
                                 'title': {'type': 'string', 'description': 'Document title'},
                                 'content': {'type': 'string',
                                             'description': 'Document content (usually markdown)'},
                                 'category': {'type': 'string',
                                              'enum': ['MANDATORY',
                                                       'BEST_PRACTICES',
                                                       'GUIDELINES',
                                                       'REFERENCE'],
                                              'default': 'REFERENCE',
                                              'description': 'Shared-context category used for '
                                                             'token budget allocation.'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Tags such as offer, template, diagram, '
                                                         'client-example, or methodology.'},
                                 'priority': {'type': 'integer',
                                              'default': 0,
                                              'minimum': 0,
                                              'maximum': 100,
                                              'description': 'Priority within category (higher = '
                                                             'more important).'},
                                 'allow_custom_collection': {'type': 'boolean',
                                                             'default': False,
                                                             'description': 'Allow upload to a '
                                                                            'custom '
                                                                            'business-looking '
                                                                            'collection instead of '
                                                                            'a standard preset.'}},
                  'required': ['title', 'content']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_upload_business_document'}},
 {'name': 'rlm_list_client_projects',
  'description': 'List client/project business-context workspaces in the current team. These are '
                 'project-scoped containers for current client documents, deliverables, diagrams, '
                 'and history.',
  'inputSchema': {'type': 'object',
                  'properties': {'include_internal': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Also return internal, '
                                                                     'research, and code projects '
                                                                     'with their scope '
                                                                     'classification.'},
                                 'limit': {'type': 'integer',
                                           'default': 100,
                                           'minimum': 1,
                                           'maximum': 500}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_list_client_projects'}},
 {'name': 'rlm_create_client_project',
  'description': 'Create a client/project business-context workspace in the current team. Use this '
                 'before uploading current client documents with rlm_upload_document.',
  'inputSchema': {'type': 'object',
                  'properties': {'name': {'type': 'string',
                                          'description': 'Client/project display name'},
                                 'slug': {'type': 'string',
                                          'description': 'Optional stable project slug. Defaults '
                                                         'to a slugified name.'},
                                 'description': {'type': 'string',
                                                 'description': 'Optional description. Snipara '
                                                                'prefixes it as Client business '
                                                                'context when needed.'},
                                 'project_mode': {'type': 'string',
                                                  'enum': ['active_client', 'reference_archive'],
                                                  'description': 'Optional client project mode. '
                                                                 'active_client keeps business '
                                                                 'health enabled; '
                                                                 'reference_archive is for '
                                                                 'past-client precedent.'},
                                 'external_client_id': {'type': 'string',
                                                        'description': 'Optional external client '
                                                                       'identifier echoed back for '
                                                                       'integrator workflows.'}},
                  'required': ['name']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_create_client_project'}},
 {'name': 'rlm_remember',
  'description': 'Store a durable Memory V2 record for later semantic recall. Direct writes '
                 'support fact, decision, learning, preference, todo, and context. Use the '
                 'narrowest owner scope: agent for one agent role, project for one '
                 'client/project/RFP, team for reviewed shared standards, and user for one '
                 "person's preferences. Do not store source truth here; use rlm_context_query, "
                 'rlm_load_document, or rlm_shared_context for specs, RFPs, diagrams, and raw '
                 'docs. Use rlm_end_of_task_commit for workflow capture.',
  'inputSchema': {'type': 'object',
                  'properties': {'text': {'type': 'string',
                                          'maxLength': 65536,
                                          'description': 'The memory text to store'},
                                 'content': {'type': 'string',
                                             'maxLength': 65536,
                                             'description': "DEPRECATED: Use 'text' instead. The "
                                                            'memory content to store.'},
                                 'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context'],
                                          'default': 'fact'},
                                 'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'default': 'project',
                                           'description': 'Memory owner boundary. scope=agent '
                                                          'requires agent_id; scope=user is '
                                                          'personal to the authenticated user or '
                                                          'integrator external_user_id; scope=team '
                                                          'requires the current project to belong '
                                                          'to a team.'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required when scope=agent; '
                                                             'identifies the agent-owned memory '
                                                             'namespace'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'scope=user memory. Snipara '
                                                                     'hashes and namespaces it per '
                                                                     'integrator client.'},
                                 'category': {'type': 'string',
                                              'maxLength': 200,
                                              'description': 'Optional category for grouping'},
                                 'ttl_days': {'type': 'integer',
                                              'description': 'Days until expiration (null = '
                                                             'permanent)'},
                                 'related_to': {'type': 'array',
                                                'items': {'type': 'string', 'maxLength': 256},
                                                'maxItems': 50,
                                                'description': 'IDs of related memories'},
                                 'document_refs': {'type': 'array',
                                                   'items': {'type': 'string', 'maxLength': 512},
                                                   'maxItems': 100,
                                                   'description': 'Referenced document paths'},
                                 'source': {'type': 'string',
                                            'maxLength': 200,
                                            'description': 'Optional source label for the memory '
                                                           'write'},
                                 'memory_reconciliation_mode': {'type': 'string',
                                                                'enum': ['off',
                                                                         'recommend',
                                                                         'auto_safe'],
                                                                'default': 'recommend',
                                                                'description': 'After storing, '
                                                                               'find older similar '
                                                                               'memories. '
                                                                               'recommend returns '
                                                                               'supersede '
                                                                               'candidates only; '
                                                                               'auto_safe '
                                                                               'supersedes only '
                                                                               'high-confidence '
                                                                               'same-scope/type/category '
                                                                               'matches. No '
                                                                               'physical '
                                                                               'deletion.'}},
                  'required': []},
  'annotations': {'title': 'Store reviewed memory',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': False,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_remember'}},
 {'name': 'rlm_remember_if_novel',
  'description': 'Store a durable Memory V2 record only if it is sufficiently novel compared with '
                 'existing memories. Direct writes support fact, decision, learning, preference, '
                 'todo, and context. Use context tools for source truth and rlm_end_of_task_commit '
                 'for workflow capture. Returns duplicate matches when skipped.',
  'inputSchema': {'type': 'object',
                  'properties': {'text': {'type': 'string',
                                          'maxLength': 65536,
                                          'description': 'The memory text to store'},
                                 'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context'],
                                          'default': 'fact'},
                                 'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'default': 'project',
                                           'description': 'Memory owner boundary. scope=agent '
                                                          'requires agent_id; scope=user is '
                                                          'personal to the authenticated user or '
                                                          'integrator external_user_id.'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required when scope=agent; '
                                                             'identifies the agent-owned memory '
                                                             'namespace'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'scope=user memory. Snipara '
                                                                     'hashes and namespaces it per '
                                                                     'integrator client.'},
                                 'category': {'type': 'string', 'maxLength': 200},
                                 'ttl_days': {'type': 'integer'},
                                 'related_to': {'type': 'array',
                                                'items': {'type': 'string', 'maxLength': 256},
                                                'maxItems': 50},
                                 'document_refs': {'type': 'array',
                                                   'items': {'type': 'string', 'maxLength': 512},
                                                   'maxItems': 100},
                                 'source': {'type': 'string',
                                            'maxLength': 200,
                                            'description': 'Optional source label for the memory '
                                                           'write'},
                                 'novelty_threshold': {'type': 'number',
                                                       'minimum': 0,
                                                       'maximum': 1,
                                                       'description': 'Similarity threshold above '
                                                                      'which a memory is treated '
                                                                      'as duplicate'},
                                 'dedupe_limit': {'type': 'integer',
                                                  'default': 5,
                                                  'minimum': 1,
                                                  'maximum': 20},
                                 'allow_supersede': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Reserved for future conflict '
                                                                    'handling'},
                                 'memory_reconciliation_mode': {'type': 'string',
                                                                'enum': ['off',
                                                                         'recommend',
                                                                         'auto_safe'],
                                                                'default': 'recommend',
                                                                'description': 'After storing, '
                                                                               'find older similar '
                                                                               'memories. '
                                                                               'recommend returns '
                                                                               'supersede '
                                                                               'candidates only; '
                                                                               'auto_safe '
                                                                               'supersedes only '
                                                                               'high-confidence '
                                                                               'same-scope/type/category '
                                                                               'matches. No '
                                                                               'physical '
                                                                               'deletion.'}},
                  'required': ['text']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_remember_if_novel'}},
 {'name': 'rlm_end_of_task_commit',
  'description': 'Persist durable outcomes from a task summary into memory. Extracts decisions, '
                 'learnings, preferences, todos, and durable workflow context while filtering '
                 'operational receipts; not for source documents or specs.',
  'inputSchema': {'type': 'object',
                  'properties': {'summary': {'type': 'string', 'description': 'Task summary'},
                                 'outcome': {'type': 'string',
                                             'enum': ['completed',
                                                      'partial',
                                                      'blocked',
                                                      'abandoned'],
                                             'default': 'completed'},
                                 'files_touched': {'type': 'array', 'items': {'type': 'string'}},
                                 'artifacts': {'type': 'array', 'items': {'type': 'string'}},
                                 'persist_types': {'type': 'array',
                                                   'items': {'type': 'string',
                                                             'enum': ['decision',
                                                                      'learning',
                                                                      'preference',
                                                                      'todo',
                                                                      'context',
                                                                      'workflow']}},
                                 'category': {'type': 'string'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'user-owned memories created '
                                                                     'from task commits.'},
                                 'handoff_only': {'type': 'boolean',
                                                  'default': False,
                                                  'description': 'For final workflow commits, '
                                                                 'create the Team Sync handoff and '
                                                                 'skip durable-memory extraction.'},
                                 'memory_reconciliation_mode': {'type': 'string',
                                                                'enum': ['off',
                                                                         'recommend',
                                                                         'auto_safe'],
                                                                'default': 'recommend',
                                                                'description': 'For newly created '
                                                                               'task memories, '
                                                                               'find older similar '
                                                                               'memories. '
                                                                               'recommend returns '
                                                                               'candidates only; '
                                                                               'auto_safe '
                                                                               'supersedes only '
                                                                               'high-confidence '
                                                                               'same-scope/type/category '
                                                                               'matches.'},
                                 'dry_run': {'type': 'boolean', 'default': False}},
                  'required': ['summary']},
  'annotations': {'title': 'Commit durable task memory',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': False,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_end_of_task_commit'}},
 {'name': 'rlm_remember_bulk',
  'description': 'Store multiple durable Memory V2 records in a single call. Batch embedding for '
                 'efficiency. Max 50 memories per call. Do not bulk-store source documents; upload '
                 'or query source truth through context tools instead.',
  'inputSchema': {'type': 'object',
                  'properties': {'memories': {'type': 'array',
                                              'items': {'type': 'object',
                                                        'properties': {'text': {'type': 'string',
                                                                                'maxLength': 65536,
                                                                                'description': 'Memory '
                                                                                               'text '
                                                                                               'to '
                                                                                               'store'},
                                                                       'type': {'type': 'string',
                                                                                'enum': ['fact',
                                                                                         'decision',
                                                                                         'learning',
                                                                                         'preference',
                                                                                         'todo',
                                                                                         'context'],
                                                                                'default': 'fact'},
                                                                       'scope': {'type': 'string',
                                                                                 'enum': ['agent',
                                                                                          'project',
                                                                                          'team',
                                                                                          'user'],
                                                                                 'default': 'project'},
                                                                       'agent_id': {'type': 'string',
                                                                                    'description': 'Required '
                                                                                                   'when '
                                                                                                   'scope=agent'},
                                                                       'category': {'type': 'string',
                                                                                    'maxLength': 200},
                                                                       'ttl_days': {'type': 'integer'},
                                                                       'related_to': {'type': 'array',
                                                                                      'items': {'type': 'string',
                                                                                                'maxLength': 256},
                                                                                      'maxItems': 50},
                                                                       'document_refs': {'type': 'array',
                                                                                         'items': {'type': 'string',
                                                                                                   'maxLength': 512},
                                                                                         'maxItems': 100}},
                                                        'required': ['text']},
                                              'minItems': 1,
                                              'maxItems': 50,
                                              'description': 'Array of memories to store (max 50)'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'user-scoped bulk memories. '
                                                                     'Applies to all memories in '
                                                                     'the call.'}},
                  'required': ['memories']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_remember_bulk'}},
 {'name': 'rlm_recall',
  'description': 'Semantically recall durable Memory V2 records such as decisions, learnings, '
                 'preferences, and session carryover. Not for source document retrieval; use '
                 'rlm_context_query, rlm_load_document, or rlm_shared_context for specs, RFPs, '
                 'diagrams, and raw docs.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'Memory question such as a past '
                                                          'decision, preference, or validated '
                                                          'learning'},
                                 'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context']},
                                 'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user']},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required when scope=agent; limits '
                                                             'recall to one agent namespace'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'scope=user recall. Snipara '
                                                                     'hashes and namespaces it per '
                                                                     'integrator client.'},
                                 'category': {'type': 'string',
                                              'description': 'Filter by category'},
                                 'limit': {'type': 'integer',
                                           'default': 5,
                                           'description': 'Maximum memories to return'},
                                 'min_relevance': {'type': 'number',
                                                   'default': 0.5,
                                                   'description': 'Minimum relevance score (0-1)'},
                                 'include_inactive': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include inactive memories in '
                                                                     'the main result set'},
                                 'warning_threshold': {'type': 'number',
                                                       'default': 0.72,
                                                       'description': 'Minimum relevance score for '
                                                                      'inactive-memory warnings'},
                                 'task': {'type': 'string',
                                          'minLength': 1,
                                          'maxLength': 512,
                                          'description': 'Optional task label recorded for '
                                                         'retrieval/outcome correlation.'},
                                 'outcome_rerank_mode': {'type': 'string',
                                                         'enum': ['disabled', 'shadow', 'enabled'],
                                                         'description': 'Optional bounded '
                                                                        'memory-outcome rerank '
                                                                        'mode. Omission uses the '
                                                                        'server configuration; a '
                                                                        'request cannot escalate '
                                                                        'beyond it.'},
                                 'correlation_context': {'type': 'object',
                                                         'additionalProperties': False,
                                                         'description': 'Optional '
                                                                        'retrieval-correlation '
                                                                        'context. Reuse session_id '
                                                                        'across retrieval and '
                                                                        'outcome calls so '
                                                                        'telemetry can be joined '
                                                                        'inside the authenticated '
                                                                        'project. These '
                                                                        'identifiers never change '
                                                                        'authorization or project '
                                                                        'scope; do not include '
                                                                        'secrets, tenant IDs, or '
                                                                        'user data.',
                                                         'properties': {'version': {'type': 'string',
                                                                                    'enum': ['retrieval-correlation-v1'],
                                                                                    'default': 'retrieval-correlation-v1'},
                                                                        'session_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Preferred '
                                                                                                      'stable '
                                                                                                      'opaque '
                                                                                                      'session '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'for '
                                                                                                      'telemetry '
                                                                                                      'association.'},
                                                                        'workflow_session_id': {'type': 'string',
                                                                                                'minLength': 1,
                                                                                                'maxLength': 128,
                                                                                                'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                                'description': 'Opaque '
                                                                                                               'workflow '
                                                                                                               'ID '
                                                                                                               'used '
                                                                                                               'when '
                                                                                                               'session_id '
                                                                                                               'is '
                                                                                                               'absent.'},
                                                                        'correlation_id': {'type': 'string',
                                                                                           'minLength': 1,
                                                                                           'maxLength': 128,
                                                                                           'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                           'description': 'Opaque '
                                                                                                          'request-chain '
                                                                                                          'ID '
                                                                                                          'used '
                                                                                                          'when '
                                                                                                          'session '
                                                                                                          'fields '
                                                                                                          'are '
                                                                                                          'absent.'},
                                                                        'request_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Opaque '
                                                                                                      'per-call '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'only '
                                                                                                      'as '
                                                                                                      'a '
                                                                                                      'final '
                                                                                                      'telemetry '
                                                                                                      'fallback.'}}}},
                  'required': ['query']},
  'annotations': {'title': 'Recall reviewed memory',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 12.0,
            'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_recall'},
  'exposed': False},
 {'name': 'rlm_resume_context',
  'description': 'Load a compact agent-ready continuity bundle for the current project. Returns '
                 'the latest Team Sync handoff match, What Changed summary, active decisions, '
                 'execution-memory snapshot, and an optional task-scoped work brief so an agent '
                 'can resume work without manually stitching these surfaces together.',
  'inputSchema': {'type': 'object',
                  'properties': {'sessionId': {'type': 'string',
                                               'description': 'Optional session identifier to '
                                                              'resolve handoff and checkpoint '
                                                              'context.'},
                                 'branch': {'type': 'string',
                                            'description': 'Optional branch name to scope What '
                                                           'Changed and handoff matching.'},
                                 'task': {'type': 'string',
                                          'description': 'Optional task summary. When supplied, '
                                                         'the response includes a task-scoped work '
                                                         'brief.'},
                                 'since': {'type': 'string',
                                           'description': 'Optional ISO timestamp for filtering '
                                                          'What Changed decision signals.'},
                                 'recentFiles': {'type': 'array',
                                                 'items': {'type': 'string'},
                                                 'description': 'Recent files relevant to the '
                                                                'task; improves handoff matching '
                                                                'and read recommendations.'},
                                 'changedFiles': {'type': 'array',
                                                  'items': {'type': 'string'},
                                                  'description': 'Changed files already known to '
                                                                 'the agent; used to scope '
                                                                 'work-brief candidates.'},
                                 'limit': {'type': 'integer',
                                           'default': 12,
                                           'minimum': 1,
                                           'maximum': 25,
                                           'description': 'Maximum PR Answer Pack records to '
                                                          'consider when composing continuity '
                                                          'context.'},
                                 'sessionLimit': {'type': 'integer',
                                                  'default': 3,
                                                  'minimum': 1,
                                                  'maximum': 10,
                                                  'description': 'Maximum execution-memory '
                                                                 'sessions to summarize.'},
                                 'eventLimit': {'type': 'integer',
                                                'default': 10,
                                                'minimum': 1,
                                                'maximum': 25,
                                                'description': 'Maximum execution-memory events '
                                                               'per session to summarize.'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 8000,
                                                'minimum': 1000,
                                                'maximum': 20000,
                                                'description': 'Hard token budget for the returned '
                                                               'continuity bundle.'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_resume_context'}},
 {'name': 'snipara_collaboration_status',
  'description': 'Inspect active collaboration state for safe parallel coding. Returns active work '
                 'sessions, claimed resources, and snapshots so a human or agent can see who is '
                 'touching files, routes, symbols, schemas, docs, or project-wide resources.',
  'inputSchema': {'type': 'object', 'properties': {}, 'required': []},
  'annotations': {'title': 'Inspect collaboration state',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False}},
 {'name': 'snipara_collaboration_start',
  'description': 'Start or heartbeat a collaboration work session for the current project. Use '
                 'this before coding so other humans and agents can see presence, branch, summary, '
                 'and the files, routes, symbols, or resources currently being touched.',
  'inputSchema': {'type': 'object',
                  'properties': {'actorId': {'type': 'string',
                                             'description': 'Stable human or agent identifier. '
                                                            'Defaults to the MCP/API caller '
                                                            'identity.'},
                                 'actorType': {'type': 'string',
                                               'enum': ['HUMAN', 'AGENT', 'SYSTEM'],
                                               'description': 'Type of actor performing the work.'},
                                 'actorLabel': {'type': 'string',
                                                'description': 'Human-readable actor name shown in '
                                                               'conflict and presence summaries.'},
                                 'sessionId': {'type': 'string',
                                               'description': 'Stable local agent/session '
                                                              'identifier used to correlate '
                                                              'heartbeats and guards.'},
                                 'client': {'type': 'string',
                                            'description': 'Client name such as codex, claude, '
                                                           'companion, or human.'},
                                 'swarmId': {'type': 'string',
                                             'description': 'Optional swarm/group identifier for '
                                                            'related agents.'},
                                 'branch': {'type': 'string', 'description': 'Current git branch.'},
                                 'summary': {'type': 'string',
                                             'description': 'Concise description of the work in '
                                                            'progress.'},
                                 'files': {'type': 'array',
                                           'items': {'type': 'string'},
                                           'description': 'Local file paths currently being edited '
                                                          'or inspected.'},
                                 'routes': {'type': 'array',
                                            'items': {'type': 'string'},
                                            'description': 'Application routes or API routes '
                                                           'currently being touched.'},
                                 'symbols': {'type': 'array',
                                             'items': {'type': 'string'},
                                             'description': 'Code symbols currently being '
                                                            'touched.'},
                                 'resources': {'type': 'array',
                                               'items': {'type': 'object',
                                                         'properties': {'kind': {'type': 'string',
                                                                                 'enum': ['FILE',
                                                                                          'ROUTE',
                                                                                          'SYMBOL',
                                                                                          'PACKAGE',
                                                                                          'SCHEMA',
                                                                                          'DOC',
                                                                                          'PROJECT'],
                                                                                 'description': 'Resource '
                                                                                                'namespace '
                                                                                                'to '
                                                                                                'protect.'},
                                                                        'id': {'type': 'string',
                                                                               'description': 'Normalized '
                                                                                              'resource '
                                                                                              'identifier, '
                                                                                              'such '
                                                                                              'as '
                                                                                              'a '
                                                                                              'file '
                                                                                              'path '
                                                                                              'or '
                                                                                              'route.'},
                                                                        'label': {'type': 'string',
                                                                                  'description': 'Optional '
                                                                                                 'display '
                                                                                                 'label '
                                                                                                 'for '
                                                                                                 'the '
                                                                                                 'protected '
                                                                                                 'resource.'},
                                                                        'sourcePath': {'type': 'string',
                                                                                       'description': 'Optional '
                                                                                                      'originating '
                                                                                                      'path '
                                                                                                      'when '
                                                                                                      'the '
                                                                                                      'resource '
                                                                                                      'came '
                                                                                                      'from '
                                                                                                      'route/symbol '
                                                                                                      'inference.'}},
                                                         'required': ['kind', 'id']},
                                               'description': 'Explicit resources to protect or '
                                                              'evaluate.'},
                                 'metadata': {'type': 'object',
                                              'additionalProperties': True,
                                              'description': 'Small JSON metadata object for '
                                                             'diagnostics. Do not include '
                                                             'secrets.'}},
                  'required': []},
  'annotations': {'title': 'Start collaboration session',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False}},
 {'name': 'snipara_collaboration_claim',
  'description': 'Create advisory or exclusive claims on files, routes, symbols, schemas, docs, '
                 'packages, or project resources. Use this to make collisions visible before '
                 'multiple humans or agents edit the same surface.',
  'inputSchema': {'type': 'object',
                  'properties': {'actorId': {'type': 'string',
                                             'description': 'Stable human or agent identifier. '
                                                            'Defaults to the MCP/API caller '
                                                            'identity.'},
                                 'actorType': {'type': 'string',
                                               'enum': ['HUMAN', 'AGENT', 'SYSTEM'],
                                               'description': 'Type of actor performing the work.'},
                                 'actorLabel': {'type': 'string',
                                                'description': 'Human-readable actor name shown in '
                                                               'conflict and presence summaries.'},
                                 'sessionId': {'type': 'string',
                                               'description': 'Stable local agent/session '
                                                              'identifier used to correlate '
                                                              'heartbeats and guards.'},
                                 'workSessionId': {'type': 'string',
                                                   'description': 'Optional hosted work session id '
                                                                  'returned by '
                                                                  'snipara_collaboration_start.'},
                                 'mode': {'type': 'string',
                                          'enum': ['WATCH',
                                                   'ADVISORY',
                                                   'REQUIRES_ACK',
                                                   'EXCLUSIVE',
                                                   'HARD_BLOCK'],
                                          'default': 'ADVISORY',
                                          'description': 'WATCH/ADVISORY are consultative; '
                                                         'REQUIRES_ACK asks for acknowledgement; '
                                                         'EXCLUSIVE and HARD_BLOCK require a TTL '
                                                         'and are renewed by heartbeat.'},
                                 'reason': {'type': 'string',
                                            'description': 'Concise reason for the claim.'},
                                 'ttlSeconds': {'type': 'integer',
                                                'minimum': 30,
                                                'maximum': 86400,
                                                'description': 'Canonical lease TTL in seconds. '
                                                               'Required modes '
                                                               'EXCLUSIVE/HARD_BLOCK default to '
                                                               '300 seconds when omitted; '
                                                               'consultative modes may omit it.'},
                                 'expiresInMinutes': {'type': 'integer',
                                                      'minimum': 1,
                                                      'maximum': 1440,
                                                      'description': 'Deprecated compatibility '
                                                                     'alias for ttlSeconds. Prefer '
                                                                     'ttlSeconds.'},
                                 'resources': {'type': 'array',
                                               'items': {'type': 'object',
                                                         'properties': {'kind': {'type': 'string',
                                                                                 'enum': ['FILE',
                                                                                          'ROUTE',
                                                                                          'SYMBOL',
                                                                                          'PACKAGE',
                                                                                          'SCHEMA',
                                                                                          'DOC',
                                                                                          'PROJECT'],
                                                                                 'description': 'Resource '
                                                                                                'namespace '
                                                                                                'to '
                                                                                                'protect.'},
                                                                        'id': {'type': 'string',
                                                                               'description': 'Normalized '
                                                                                              'resource '
                                                                                              'identifier, '
                                                                                              'such '
                                                                                              'as '
                                                                                              'a '
                                                                                              'file '
                                                                                              'path '
                                                                                              'or '
                                                                                              'route.'},
                                                                        'label': {'type': 'string',
                                                                                  'description': 'Optional '
                                                                                                 'display '
                                                                                                 'label '
                                                                                                 'for '
                                                                                                 'the '
                                                                                                 'protected '
                                                                                                 'resource.'},
                                                                        'sourcePath': {'type': 'string',
                                                                                       'description': 'Optional '
                                                                                                      'originating '
                                                                                                      'path '
                                                                                                      'when '
                                                                                                      'the '
                                                                                                      'resource '
                                                                                                      'came '
                                                                                                      'from '
                                                                                                      'route/symbol '
                                                                                                      'inference.'}},
                                                         'required': ['kind', 'id']},
                                               'description': 'Explicit resources to protect or '
                                                              'evaluate.'},
                                 'metadata': {'type': 'object',
                                              'additionalProperties': True,
                                              'description': 'Small JSON metadata object for '
                                                             'diagnostics. Do not include '
                                                             'secrets.'}},
                  'required': ['resources']},
  'annotations': {'title': 'Claim collaboration resources',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': False,
                  'openWorldHint': False}},
 {'name': 'snipara_collaboration_release',
  'description': 'Release or expire one hosted collaboration lease after the guarded work is done.',
  'inputSchema': {'type': 'object',
                  'properties': {'actorId': {'type': 'string',
                                             'description': 'Stable human or agent identifier. '
                                                            'Defaults to the MCP/API caller '
                                                            'identity.'},
                                 'actorType': {'type': 'string',
                                               'enum': ['HUMAN', 'AGENT', 'SYSTEM'],
                                               'description': 'Type of actor performing the work.'},
                                 'actorLabel': {'type': 'string',
                                                'description': 'Human-readable actor name shown in '
                                                               'conflict and presence summaries.'},
                                 'sessionId': {'type': 'string',
                                               'description': 'Stable local agent/session '
                                                              'identifier used to correlate '
                                                              'heartbeats and guards.'},
                                 'leaseId': {'type': 'string',
                                             'description': 'Hosted resource lease id to release.'},
                                 'status': {'type': 'string',
                                            'enum': ['RELEASED', 'EXPIRED'],
                                            'default': 'RELEASED',
                                            'description': 'Final status to apply to the lease.'}},
                  'required': ['leaseId']},
  'annotations': {'title': 'Release collaboration lease',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False}},
 {'name': 'snipara_collaboration_guard',
  'description': 'Evaluate conflict risk before editing, committing, or handing off work. Returns '
                 'ALLOW, REQUIRES_ACK, REVIEW_REQUIRED, or BLOCKED with conflicts and recommended '
                 'actions; optionally persists the guard event as an alarm for the team.',
  'inputSchema': {'type': 'object',
                  'properties': {'actorId': {'type': 'string',
                                             'description': 'Stable human or agent identifier. '
                                                            'Defaults to the MCP/API caller '
                                                            'identity.'},
                                 'actorType': {'type': 'string',
                                               'enum': ['HUMAN', 'AGENT', 'SYSTEM'],
                                               'description': 'Type of actor performing the work.'},
                                 'actorLabel': {'type': 'string',
                                                'description': 'Human-readable actor name shown in '
                                                               'conflict and presence summaries.'},
                                 'sessionId': {'type': 'string',
                                               'description': 'Stable local agent/session '
                                                              'identifier used to correlate '
                                                              'heartbeats and guards.'},
                                 'workSessionId': {'type': 'string',
                                                   'description': 'Optional hosted work session id '
                                                                  'returned by '
                                                                  'snipara_collaboration_start.'},
                                 'branch': {'type': 'string', 'description': 'Current git branch.'},
                                 'summary': {'type': 'string',
                                             'description': 'Concise description of the guarded '
                                                            'change.'},
                                 'files': {'type': 'array',
                                           'items': {'type': 'string'},
                                           'description': 'Local file paths that may be edited, '
                                                          'committed, or reviewed.'},
                                 'routes': {'type': 'array',
                                            'items': {'type': 'string'},
                                            'description': 'Application routes or API routes that '
                                                           'may be affected.'},
                                 'symbols': {'type': 'array',
                                             'items': {'type': 'string'},
                                             'description': 'Code symbols that may be affected.'},
                                 'resources': {'type': 'array',
                                               'items': {'type': 'object',
                                                         'properties': {'kind': {'type': 'string',
                                                                                 'enum': ['FILE',
                                                                                          'ROUTE',
                                                                                          'SYMBOL',
                                                                                          'PACKAGE',
                                                                                          'SCHEMA',
                                                                                          'DOC',
                                                                                          'PROJECT'],
                                                                                 'description': 'Resource '
                                                                                                'namespace '
                                                                                                'to '
                                                                                                'protect.'},
                                                                        'id': {'type': 'string',
                                                                               'description': 'Normalized '
                                                                                              'resource '
                                                                                              'identifier, '
                                                                                              'such '
                                                                                              'as '
                                                                                              'a '
                                                                                              'file '
                                                                                              'path '
                                                                                              'or '
                                                                                              'route.'},
                                                                        'label': {'type': 'string',
                                                                                  'description': 'Optional '
                                                                                                 'display '
                                                                                                 'label '
                                                                                                 'for '
                                                                                                 'the '
                                                                                                 'protected '
                                                                                                 'resource.'},
                                                                        'sourcePath': {'type': 'string',
                                                                                       'description': 'Optional '
                                                                                                      'originating '
                                                                                                      'path '
                                                                                                      'when '
                                                                                                      'the '
                                                                                                      'resource '
                                                                                                      'came '
                                                                                                      'from '
                                                                                                      'route/symbol '
                                                                                                      'inference.'}},
                                                         'required': ['kind', 'id']},
                                               'description': 'Explicit resources to protect or '
                                                              'evaluate.'},
                                 'metadata': {'type': 'object',
                                              'additionalProperties': True,
                                              'description': 'Small JSON metadata object for '
                                                             'diagnostics. Do not include '
                                                             'secrets.'},
                                 'persist': {'type': 'boolean',
                                             'default': True,
                                             'description': 'Persist the guard event/alarm in '
                                                            'hosted collaboration history.'}},
                  'required': []},
  'annotations': {'title': 'Evaluate collaboration guard',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': False,
                  'openWorldHint': False}},
 {'name': 'rlm_memories',
  'description': 'List memories with optional filters and sorting.',
  'inputSchema': {'type': 'object',
                  'properties': {'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context']},
                                 'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user']},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required when scope=agent; limits '
                                                             'listing to one agent namespace'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'scope=user memory listing. '
                                                                     'Snipara hashes and '
                                                                     'namespaces it per integrator '
                                                                     'client.'},
                                 'category': {'type': 'string'},
                                 'status': {'type': 'string',
                                            'enum': ['ACTIVE', 'INVALIDATED', 'SUPERSEDED'],
                                            'description': 'Filter by lifecycle status'},
                                 'search': {'type': 'string',
                                            'description': 'Text search in content'},
                                 'limit': {'type': 'integer', 'default': 20},
                                 'offset': {'type': 'integer', 'default': 0},
                                 'include_inactive': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include inactive memories in '
                                                                     'results'},
                                 'sort_by': {'type': 'string',
                                             'enum': ['created_at',
                                                      'confidence',
                                                      'access_count',
                                                      'last_accessed',
                                                      'expires_at'],
                                             'default': 'created_at',
                                             'description': 'Field to sort by'},
                                 'sort_order': {'type': 'string',
                                                'enum': ['asc', 'desc'],
                                                'default': 'desc',
                                                'description': 'Sort direction'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_memories'}},
 {'name': 'rlm_forget',
  'description': 'Delete memories by ID or filter criteria.',
  'inputSchema': {'type': 'object',
                  'properties': {'memory_id': {'type': 'string',
                                               'maxLength': 256,
                                               'description': 'Specific memory ID to delete'},
                                 'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context']},
                                 'category': {'type': 'string',
                                              'maxLength': 200,
                                              'description': 'Delete all in this category'},
                                 'older_than_days': {'type': 'integer',
                                                     'description': 'Delete memories older than N '
                                                                    'days'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_forget'}},
 {'name': 'rlm_memory_invalidate',
  'description': 'Invalidate a Memory V2 record without deleting it. Accepts a legacy memory ID if '
                 'a migration map exists.',
  'inputSchema': {'type': 'object',
                  'properties': {'memory_id': {'type': 'string',
                                               'maxLength': 256,
                                               'description': 'Legacy or V2 memory ID'},
                                 'invalidated_at': {'type': 'string',
                                                    'description': 'Optional ISO timestamp. '
                                                                   'Defaults to now.'},
                                 'reason': {'type': 'string',
                                            'maxLength': 2048,
                                            'description': 'Optional human-readable invalidation '
                                                           'reason'}},
                  'required': ['memory_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_memory_invalidate'}},
 {'name': 'rlm_memory_attach_source',
  'description': 'Attach structured evidence to a Memory V2 record. Accepts a legacy memory ID if '
                 'a migration map exists.',
  'inputSchema': {'type': 'object',
                  'properties': {'memory_id': {'type': 'string',
                                               'maxLength': 256,
                                               'description': 'Legacy or V2 memory ID'},
                                 'evidence_type': {'type': 'string',
                                                   'enum': ['DOCUMENT',
                                                            'CHUNK',
                                                            'SESSION',
                                                            'PR',
                                                            'ISSUE',
                                                            'COMMIT',
                                                            'WEBHOOK',
                                                            'EXTERNAL_URL'],
                                                   'description': 'Evidence type'},
                                 'document_id': {'type': 'string',
                                                 'maxLength': 256,
                                                 'description': 'Optional document ID'},
                                 'chunk_id': {'type': 'string',
                                              'maxLength': 256,
                                              'description': 'Optional chunk ID'},
                                 'external_ref': {'type': 'string',
                                                  'maxLength': 512,
                                                  'description': 'Optional path or URL'},
                                 'snippet': {'type': 'string',
                                             'maxLength': 4096,
                                             'description': 'Optional supporting excerpt'},
                                 'line_start': {'type': 'integer',
                                                'description': 'Optional start line'},
                                 'line_end': {'type': 'integer',
                                              'description': 'Optional end line'},
                                 'weight': {'type': 'number',
                                            'default': 1.0,
                                            'minimum': 0.0,
                                            'maximum': 1.0,
                                            'description': 'Evidence weight'}},
                  'required': ['memory_id', 'evidence_type']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_memory_attach_source'}},
 {'name': 'rlm_memory_supersede',
  'description': 'Mark one Memory V2 record as superseded by another. Accepts legacy memory IDs if '
                 'migration maps exist.',
  'inputSchema': {'type': 'object',
                  'properties': {'old_memory_id': {'type': 'string',
                                                   'maxLength': 256,
                                                   'description': 'Legacy or V2 memory ID being '
                                                                  'replaced'},
                                 'new_memory_id': {'type': 'string',
                                                   'maxLength': 256,
                                                   'description': 'Legacy or V2 replacement memory '
                                                                  'ID'},
                                 'reason': {'type': 'string',
                                            'maxLength': 2048,
                                            'description': 'Optional supersession reason'}},
                  'required': ['old_memory_id', 'new_memory_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_memory_supersede'}},
 {'name': 'rlm_memory_verify',
  'description': 'Verify whether a Memory V2 record still has valid supporting evidence.',
  'inputSchema': {'type': 'object',
                  'properties': {'memory_id': {'type': 'string',
                                               'description': 'Legacy or V2 memory ID'},
                                 'mark_stale_if_missing': {'type': 'boolean',
                                                           'default': True,
                                                           'description': 'Mark memory stale when '
                                                                          'all evidence is '
                                                                          'invalid'}},
                  'required': ['memory_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_memory_verify'}},
 {'name': 'rlm_memory_review_queue',
  'description': 'Private review surface for candidate, stale, or rejected memories that need '
                 'human inspection before they become agent memory.',
  'inputSchema': {'type': 'object',
                  'properties': {'status': {'type': 'string',
                                            'enum': ['candidate',
                                                     'pending',
                                                     'stale',
                                                     'rejected',
                                                     'invalidated',
                                                     'superseded',
                                                     'archived',
                                                     'active',
                                                     'approved',
                                                     'all'],
                                            'default': 'candidate',
                                            'description': 'Queue lifecycle status to inspect.'},
                                 'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context'],
                                          'description': 'Optional memory type filter.'},
                                 'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'description': 'Optional owner scope filter.'},
                                 'category': {'type': 'string',
                                              'description': 'Optional category filter.'},
                                 'search': {'type': 'string',
                                            'description': 'Optional content search filter.'},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 100,
                                           'description': 'Maximum queue items to return.'},
                                 'offset': {'type': 'integer',
                                            'default': 0,
                                            'minimum': 0,
                                            'description': 'Pagination offset.'},
                                 'include_evidence': {'type': 'boolean',
                                                      'default': True,
                                                      'description': 'Include Memory V2 evidence '
                                                                     'links and legacy document '
                                                                     'refs.'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required when scope=agent; limits '
                                                             'queue reads to one agent namespace.'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'scope=user queue reads.'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_memory_review_queue'}},
 {'name': 'rlm_memory_resolve_queue_item',
  'description': 'Private review surface to accept, reject, archive, invalidate, merge, or '
                 'supersede one queued memory item.',
  'inputSchema': {'type': 'object',
                  'properties': {'memory_id': {'type': 'string',
                                               'description': 'Legacy or V2 memory ID to resolve.'},
                                 'action': {'type': 'string',
                                            'enum': ['accept',
                                                     'approve',
                                                     'reject',
                                                     'archive',
                                                     'invalidate',
                                                     'merge',
                                                     'supersede'],
                                            'description': 'Review resolution action.'},
                                 'target_memory_id': {'type': 'string',
                                                      'description': 'Required for merge and '
                                                                     'supersede actions.'},
                                 'notes': {'type': 'string',
                                           'description': 'Optional reviewer notes or rationale.'}},
                  'required': ['memory_id', 'action']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_memory_resolve_queue_item'}},
 {'name': 'rlm_journal_append',
  'description': "Append an entry to today's journal. Journals are daily logs of operational "
                 'notes, decisions, and context. Auto-loads today + yesterday on session start.',
  'inputSchema': {'type': 'object',
                  'properties': {'text': {'type': 'string',
                                          'description': 'Journal entry text (markdown supported)'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Optional tags for categorization'}},
                  'required': ['text']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_journal_append'}},
 {'name': 'rlm_journal_get',
  'description': "Get journal entries for a specific date. Returns all entries from that day's "
                 'operational log.',
  'inputSchema': {'type': 'object',
                  'properties': {'date': {'type': 'string',
                                          'description': 'Date in YYYY-MM-DD format (default: '
                                                         'today)'},
                                 'include_yesterday': {'type': 'boolean',
                                                       'default': False,
                                                       'description': "Also include yesterday's "
                                                                      'entries'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_journal_get'}},
 {'name': 'rlm_journal_summarize',
  'description': 'Get journal entries for a date, ready for summarization. Use before archiving '
                 'old journals.',
  'inputSchema': {'type': 'object',
                  'properties': {'date': {'type': 'string',
                                          'description': 'Date to summarize (YYYY-MM-DD)'}},
                  'required': ['date']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_journal_summarize'}},
 {'name': 'rlm_session_memories',
  'description': 'Get tiered durable memories for session bootstrap, with optional short-lived '
                 'carryover. Use at session start to restore memory state, not to retrieve source '
                 'documents.',
  'inputSchema': {'type': 'object',
                  'properties': {'max_critical_tokens': {'type': 'integer',
                                                         'default': 8000,
                                                         'description': 'Token budget for CRITICAL '
                                                                        'tier'},
                                 'max_daily_tokens': {'type': 'integer',
                                                      'default': 4000,
                                                      'description': 'Token budget for DAILY tier'},
                                 'include_yesterday': {'type': 'boolean',
                                                       'default': True,
                                                       'description': "Include yesterday's daily "
                                                                      'memories'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Optional agent namespace to include '
                                                             'in the session bundle'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID whose '
                                                                     'personal memories should be '
                                                                     'included in the session '
                                                                     'bundle.'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_session_memories'}},
 {'name': 'rlm_memory_compact',
  'description': 'Compact and optimize memories. Deduplicates similar memories, promotes frequent '
                 'learnings to CRITICAL tier, and archives old entries.',
  'inputSchema': {'type': 'object',
                  'properties': {'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'default': 'project',
                                           'description': 'Memory scope to compact'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required agent namespace when '
                                                             'scope=agent'},
                                 'external_user_id': {'type': 'string',
                                                      'maxLength': 256,
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID whose '
                                                                     'user-scoped memories should '
                                                                     'be compacted.'},
                                 'deduplicate': {'type': 'boolean',
                                                 'default': True,
                                                 'description': 'Merge similar memories'},
                                 'promote_threshold': {'type': 'integer',
                                                       'default': 3,
                                                       'description': 'If learning accessed N '
                                                                      'times, promote to CRITICAL'},
                                 'archive_older_than_days': {'type': 'integer',
                                                             'default': 30,
                                                             'description': 'Archive memories '
                                                                            'older than N days'},
                                 'dry_run': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Preview changes without applying'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_memory_compact'}},
 {'name': 'rlm_session_bootstrap_status',
  'description': 'Read-only status for the current engine session memory bootstrap. Reports '
                 'whether bootstrap ran, when it ran, and how many memories/profiles were '
                 'injected.',
  'inputSchema': {'type': 'object', 'properties': {}, 'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_session_bootstrap_status'}},
 {'name': 'rlm_owner_profile_get',
  'description': 'Get the canonical personal owner profile for the authenticated user. The profile '
                 'is user-scoped across projects and is used for deterministic session bootstrap. '
                 'Integrator client keys must pass external_user_id.',
  'inputSchema': {'type': 'object',
                  'properties': {'external_user_id': {'type': 'string',
                                                      'maxLength': 256,
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID whose '
                                                                     'personal owner profile '
                                                                     'should be returned.'}},
                  'required': [],
                  'additionalProperties': False},
  'annotations': {'title': 'Get personal owner profile',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_owner_profile_get'}},
 {'name': 'rlm_owner_profile_update',
  'description': "Patch or replace the authenticated user's canonical personal owner profile. "
                 'Stores durable preferences and operating principles in user-scoped memory; never '
                 'include secrets. Integrator client keys must pass external_user_id.',
  'inputSchema': {'type': 'object',
                  'properties': {'profile': {'type': 'object',
                                             'description': 'Structured personal profile fields to '
                                                            'patch or use as the replacement '
                                                            'profile.',
                                             'properties': {'preferred_language': {'type': 'string',
                                                                                   'maxLength': 2048,
                                                                                   'description': 'Preferred '
                                                                                                  'language '
                                                                                                  'for '
                                                                                                  'agent '
                                                                                                  'communication.'},
                                                            'communication_style': {'type': 'string',
                                                                                    'maxLength': 2048,
                                                                                    'description': 'Preferred '
                                                                                                   'tone, '
                                                                                                   'density, '
                                                                                                   'and '
                                                                                                   'communication '
                                                                                                   'style.'},
                                                            'decision_style': {'type': 'string',
                                                                               'maxLength': 2048,
                                                                               'description': 'How '
                                                                                              'the '
                                                                                              'owner '
                                                                                              'prefers '
                                                                                              'decisions '
                                                                                              'and '
                                                                                              'tradeoffs '
                                                                                              'to '
                                                                                              'be '
                                                                                              'handled.'},
                                                            'autonomy_preference': {'type': 'string',
                                                                                    'maxLength': 2048,
                                                                                    'description': 'Expected '
                                                                                                   'agent '
                                                                                                   'autonomy '
                                                                                                   'and '
                                                                                                   'approval '
                                                                                                   'boundaries.'},
                                                            'risk_tolerance': {'type': 'string',
                                                                               'maxLength': 2048,
                                                                               'description': "Owner's "
                                                                                              'general '
                                                                                              'risk '
                                                                                              'tolerance '
                                                                                              'and '
                                                                                              'escalation '
                                                                                              'preference.'},
                                                            'evidence_preferences': {'type': 'string',
                                                                                     'maxLength': 2048,
                                                                                     'description': 'Preferred '
                                                                                                    'proof, '
                                                                                                    'verification, '
                                                                                                    'and '
                                                                                                    'sourcing '
                                                                                                    'style.'},
                                                            'product_principles': {'type': 'array',
                                                                                   'maxItems': 12,
                                                                                   'items': {'type': 'string',
                                                                                             'maxLength': 512},
                                                                                   'description': 'Durable '
                                                                                                  'product '
                                                                                                  'principles '
                                                                                                  'that '
                                                                                                  'should '
                                                                                                  'guide '
                                                                                                  'work.'},
                                                            'non_negotiables': {'type': 'array',
                                                                                'maxItems': 12,
                                                                                'items': {'type': 'string',
                                                                                          'maxLength': 512},
                                                                                'description': 'Boundaries '
                                                                                               'and '
                                                                                               'constraints '
                                                                                               'that '
                                                                                               'agents '
                                                                                               'must '
                                                                                               'preserve.'},
                                                            'working_preferences': {'type': 'array',
                                                                                    'maxItems': 12,
                                                                                    'items': {'type': 'string',
                                                                                              'maxLength': 512},
                                                                                    'description': 'Stable '
                                                                                                   'workflow '
                                                                                                   'and '
                                                                                                   'collaboration '
                                                                                                   'preferences.'}},
                                             'additionalProperties': False},
                                 'replace': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Replace the canonical profile instead '
                                                            'of patching the supplied fields into '
                                                            'it.'},
                                 'evidence_refs': {'type': 'array',
                                                   'maxItems': 24,
                                                   'items': {'type': 'string', 'maxLength': 512},
                                                   'description': 'Optional source references '
                                                                  'supporting this profile '
                                                                  'update.'},
                                 'external_user_id': {'type': 'string',
                                                      'maxLength': 256,
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID whose '
                                                                     'personal owner profile '
                                                                     'should be updated.'}},
                  'required': ['profile'],
                  'additionalProperties': False},
  'annotations': {'title': 'Update personal owner profile',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_owner_profile_update'}},
 {'name': 'rlm_memory_health',
  'description': 'Read-only memory hygiene diagnostics. Returns active memory counts, top '
                 'categories, auto-compaction threshold status, and samples of known noise/anomaly '
                 'patterns without mutating memory.',
  'inputSchema': {'type': 'object',
                  'properties': {'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'description': 'Optional memory scope to inspect. '
                                                          'Defaults to all visible project-owned '
                                                          'scopes.'},
                                 'include_inactive': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include INVALIDATED and '
                                                                     'SUPERSEDED memories in the '
                                                                     'scan.'},
                                 'sample_limit': {'type': 'integer',
                                                  'default': 5,
                                                  'minimum': 0,
                                                  'maximum': 20,
                                                  'description': 'Maximum anomaly samples to '
                                                                 'return.'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_memory_health'}},
 {'name': 'rlm_memory_duplicate_candidates',
  'description': 'Read-only duplicate/supersession review candidates. Groups exact and near '
                 'duplicate memories and suggests which IDs to keep or supersede without mutating '
                 'memory.',
  'inputSchema': {'type': 'object',
                  'properties': {'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'description': 'Optional memory scope to inspect.'},
                                 'include_inactive': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include INVALIDATED and '
                                                                     'SUPERSEDED memories in '
                                                                     'duplicate grouping.'},
                                 'limit': {'type': 'integer',
                                           'default': 20,
                                           'minimum': 1,
                                           'maximum': 100,
                                           'description': 'Maximum duplicate groups to return.'},
                                 'min_similarity': {'type': 'number',
                                                    'default': 0.9,
                                                    'minimum': 0,
                                                    'maximum': 1,
                                                    'description': 'Lexical similarity threshold '
                                                                   'for near-duplicate groups.'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_memory_duplicate_candidates'}},
 {'name': 'rlm_memory_clean_candidates',
  'description': 'Read-only grouped memory cleanup candidates. Returns noise, duplicates, possibly '
                 'stale memories, category anomalies, and review-queue items without mutating '
                 'memory.',
  'inputSchema': {'type': 'object',
                  'properties': {'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'description': 'Optional memory scope to inspect.'},
                                 'include_inactive': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include INVALIDATED and '
                                                                     'SUPERSEDED memories in the '
                                                                     'scan.'},
                                 'limit_per_bucket': {'type': 'integer',
                                                      'default': 10,
                                                      'minimum': 1,
                                                      'maximum': 50,
                                                      'description': 'Maximum candidates to return '
                                                                     'per bucket.'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_memory_clean_candidates'}},
 {'name': 'rlm_memory_daily_brief',
  'description': "Generate a 'Top N active constraints' daily brief. Summarizes critical "
                 'decisions, active rules, and pending todos.',
  'inputSchema': {'type': 'object',
                  'properties': {'date': {'type': 'string',
                                          'description': 'Date for brief (default: today)'},
                                 'max_items': {'type': 'integer',
                                               'default': 10,
                                               'description': 'Maximum items to include'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_memory_daily_brief'}},
 {'name': 'rlm_tenant_profile_create',
  'description': 'Create a structured tenant/client profile. Stored as CRITICAL memory for '
                 'auto-loading. Use for client onboarding.',
  'inputSchema': {'type': 'object',
                  'properties': {'client_name': {'type': 'string',
                                                 'description': 'Name of the client/tenant '
                                                                '(required)'},
                                 'business_model': {'type': 'string',
                                                    'description': 'How the business works'},
                                 'industry': {'type': 'string', 'description': 'Industry vertical'},
                                 'tech_stack': {'type': 'string',
                                                'description': 'Technology stack used'},
                                 'legal_constraints': {'type': 'string',
                                                       'description': 'Legal requirements'},
                                 'security_requirements': {'type': 'string',
                                                           'description': 'Security constraints'},
                                 'ui_ux_prefs': {'type': 'string',
                                                 'description': 'UI/UX preferences'},
                                 'communication_style': {'type': 'string',
                                                         'description': 'How to communicate'},
                                 'risk_tolerance': {'type': 'string',
                                                    'enum': ['low', 'medium', 'high'],
                                                    'description': 'Risk tolerance level'},
                                 'dos': {'type': 'array',
                                         'items': {'type': 'string'},
                                         'description': 'List of things to do'},
                                 'donts': {'type': 'array',
                                           'items': {'type': 'string'},
                                           'description': 'List of things to avoid'},
                                 'custom_fields': {'type': 'object',
                                                   'description': 'Additional custom fields'}},
                  'required': ['client_name']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_tenant_profile_create'}},
 {'name': 'rlm_tenant_profile_get',
  'description': 'Get tenant profile(s) for a project. Returns latest profile if tenant_id not '
                 'specified.',
  'inputSchema': {'type': 'object',
                  'properties': {'tenant_id': {'type': 'string',
                                               'description': 'Specific profile ID (optional, '
                                                              'returns all if not specified)'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_tenant_profile_get'}},
 {'name': 'rlm_swarm_create',
  'description': 'Create a new agent swarm for multi-agent coordination.',
  'inputSchema': {'type': 'object',
                  'properties': {'name': {'type': 'string', 'description': 'Swarm name'},
                                 'description': {'type': 'string'},
                                 'max_agents': {'type': 'integer', 'default': 10},
                                 'task_timeout': {'type': 'integer',
                                                  'default': 600,
                                                  'description': 'Task lease timeout in seconds'},
                                 'claim_timeout': {'type': 'integer',
                                                   'default': 300,
                                                   'description': 'Resource claim lease timeout in '
                                                                  'seconds'},
                                 'reuse_existing': {'type': 'boolean',
                                                    'default': False,
                                                    'description': 'Return an active same-name '
                                                                   'swarm instead of creating a '
                                                                   'duplicate'},
                                 'config': {'type': 'object'}},
                  'required': ['name']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_swarm_create'}},
 {'name': 'rlm_swarm_delete',
  'description': 'Delete an agent swarm and its related runtime data. Requires ADMIN access.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string',
                                              'description': 'Swarm ID to delete'}},
                  'required': ['swarm_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_swarm_delete'}},
 {'name': 'rlm_swarm_join',
  'description': 'Join an existing swarm as an agent.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm to join'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Your unique agent identifier'},
                                 'role': {'type': 'string',
                                          'enum': ['coordinator', 'worker', 'observer'],
                                          'default': 'worker'},
                                 'capabilities': {'type': 'array', 'items': {'type': 'string'}}},
                  'required': ['swarm_id', 'agent_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_swarm_join'}},
 {'name': 'rlm_agent_profile_get',
  'description': "Get an agent's profile (identity, personality, boundaries). Auto-loaded on "
                 'session start for swarm agents.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'agent_id': {'type': 'string', 'description': 'Agent identifier'}},
                  'required': ['swarm_id', 'agent_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_agent_profile_get'}},
 {'name': 'rlm_agent_profile_update',
  'description': "Update an agent's profile. Use to set personality, boundaries, communication "
                 'style.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'agent_id': {'type': 'string', 'description': 'Agent identifier'},
                                 'profile': {'type': 'object',
                                             'description': 'Profile data (merged with existing)',
                                             'properties': {'display_name': {'type': 'string',
                                                                             'description': 'Display '
                                                                                            'name '
                                                                                            '(e.g., '
                                                                                            "'Jarvis "
                                                                                            "⚡')"},
                                                            'personality': {'type': 'string',
                                                                            'description': 'Personality '
                                                                                           'type '
                                                                                           '(e.g., '
                                                                                           "'INTJ "
                                                                                           '- '
                                                                                           "Strategic')"},
                                                            'role_description': {'type': 'string',
                                                                                 'description': 'Role '
                                                                                                'description'},
                                                            'boundaries': {'type': 'array',
                                                                           'items': {'type': 'string'},
                                                                           'description': 'Boundaries '
                                                                                          'and '
                                                                                          'limits'},
                                                            'communication_style': {'type': 'string',
                                                                                    'description': 'Preferred '
                                                                                                   'communication '
                                                                                                   'style'},
                                                            'decision_making': {'type': 'string',
                                                                                'description': 'Decision-making '
                                                                                               'approach'},
                                                            'soul_document_path': {'type': 'string',
                                                                                   'description': 'Path '
                                                                                                  'to '
                                                                                                  'SOUL.md '
                                                                                                  'document'},
                                                            'memory_scope': {'type': 'string',
                                                                             'enum': ['agent',
                                                                                      'project',
                                                                                      'team'],
                                                                             'description': 'Memory '
                                                                                            'scope'}}}},
                  'required': ['swarm_id', 'agent_id', 'profile']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_agent_profile_update'}},
 {'name': 'rlm_claim',
  'description': 'Claim exclusive access to a resource (file, function, module). Claims '
                 'auto-expire.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'agent_id': {'type': 'string'},
                                 'resource_type': {'type': 'string',
                                                   'enum': ['file',
                                                            'function',
                                                            'module',
                                                            'component',
                                                            'other']},
                                 'resource_id': {'type': 'string',
                                                 'description': 'Resource identifier (e.g., file '
                                                                'path)'},
                                 'timeout_seconds': {'type': 'integer', 'default': 300}},
                  'required': ['swarm_id', 'agent_id', 'resource_type', 'resource_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_claim'}},
 {'name': 'rlm_release',
  'description': 'Release a claimed resource.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'agent_id': {'type': 'string'},
                                 'claim_id': {'type': 'string'},
                                 'resource_type': {'type': 'string'},
                                 'resource_id': {'type': 'string'}},
                  'required': ['swarm_id', 'agent_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_release'}},
 {'name': 'rlm_state_get',
  'description': 'Read shared swarm state by key.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'key': {'type': 'string', 'description': 'State key to read'}},
                  'required': ['swarm_id', 'key']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_state_get'}},
 {'name': 'rlm_state_set',
  'description': 'Write shared swarm state with optimistic locking and optional TTL.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'agent_id': {'type': 'string'},
                                 'key': {'type': 'string'},
                                 'value': {'description': 'Value to set (any JSON-serializable '
                                                          'type)'},
                                 'expected_version': {'type': 'integer',
                                                      'description': 'Expected version for '
                                                                     'optimistic locking'},
                                 'ttl_seconds': {'type': 'integer',
                                                 'description': 'Time to live in seconds '
                                                                '(optional, state expires after '
                                                                'this)'}},
                  'required': ['swarm_id', 'agent_id', 'key', 'value']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_state_set'}},
 {'name': 'rlm_state_poll',
  'description': 'Poll for state changes across multiple keys. Returns only keys that changed '
                 'since last_versions. Use for efficient multi-key monitoring without individual '
                 'get calls.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'keys': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'List of state keys to monitor'},
                                 'last_versions': {'type': 'object',
                                                   'additionalProperties': {'type': 'integer'},
                                                   'description': 'Map of key -> last known '
                                                                  'version. Only keys with newer '
                                                                  'versions are returned.',
                                                   'default': {}}},
                  'required': ['swarm_id', 'keys']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_state_poll'}},
 {'name': 'rlm_broadcast',
  'description': 'Send an event to all agents in the swarm.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'agent_id': {'type': 'string'},
                                 'event_type': {'type': 'string', 'description': 'Event type'},
                                 'payload': {'type': 'object', 'description': 'Event data'}},
                  'required': ['swarm_id', 'agent_id', 'event_type']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_broadcast'}},
 {'name': 'rlm_swarm_events',
  'description': 'Query and filter broadcast events plus htask audit events in a swarm. Use '
                 'rlm_htask_audit_trail for task-only polling.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'event_type': {'type': 'string',
                                                'description': 'Filter by event type'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Filter by sending agent'},
                                 'since': {'type': 'string',
                                           'format': 'date-time',
                                           'description': 'Only events after this timestamp (ISO '
                                                          '8601)'},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'description': 'Maximum events to return'}},
                  'required': ['swarm_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_swarm_events'}},
 {'name': 'rlm_agent_status',
  'description': 'Get swarm agent status with pending tasks and clear instructions.\n'
                 '\n'
                 'Call this at session start to discover tasks assigned to you. Returns:\n'
                 '- Pending tasks assigned to your agent (use rlm_htask_recommend_batch to '
                 'inspect)\n'
                 "- Active swarms you've joined\n"
                 "- Current task you're working on (if any)\n"
                 '- Clear instructions on what to do next\n'
                 '\n'
                 'This is THE discovery tool for swarm agents - tells you what work is waiting.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string',
                                              'description': 'Swarm ID to check status for'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Your agent identifier in the swarm'}},
                  'required': ['swarm_id', 'agent_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_agent_status'}},
 {'name': 'rlm_swarm_leave',
  'description': 'Remove an agent from a swarm.\n'
                 '\n'
                 'Use this to:\n'
                 '- Clean up inactive/crashed agents\n'
                 '- Remove yourself from a swarm when done\n'
                 '- Free up agent slots for others\n'
                 '\n'
                 'What happens on removal:\n'
                 '1. All resource claims held by the agent are released\n'
                 '2. Pending/claimed tasks assigned to the agent are unassigned\n'
                 '3. The agent record is deleted from the swarm\n'
                 '\n'
                 'The agent can rejoin later with rlm_swarm_join.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Agent ID to remove (can be yourself '
                                                             'or another agent)'}},
                  'required': ['swarm_id', 'agent_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_swarm_leave'}},
 {'name': 'rlm_swarm_members',
  'description': 'List all agents in a swarm with their status.\n'
                 '\n'
                 "Returns each agent's:\n"
                 "- agent_id: The agent's identifier\n"
                 '- role: coordinator, worker, or observer\n'
                 '- status: active, idle, busy\n'
                 '- capabilities: What the agent can do\n'
                 "- current_task: What they're working on (if any)\n"
                 '- joined_at: When they joined\n'
                 '\n'
                 'Use this to:\n'
                 "- See who's in the swarm\n"
                 '- Find available agents for task assignment\n'
                 '- Monitor agent activity',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'}},
                  'required': ['swarm_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_swarm_members'}},
 {'name': 'rlm_swarm_update',
  'description': 'Update swarm configuration (requires ADMIN access).\n'
                 '\n'
                 'Updatable settings:\n'
                 '- name: Swarm display name\n'
                 '- description: What the swarm is for\n'
                 '- max_agents: Maximum agents allowed (plan-limited)\n'
                 '- task_timeout: Seconds before unclaimed task expires (60-3600)\n'
                 '- claim_timeout: Seconds a resource claim lasts (60-7200)',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string',
                                              'description': 'Swarm ID to update'},
                                 'name': {'type': 'string', 'description': 'New swarm name'},
                                 'description': {'type': 'string',
                                                 'description': 'New description'},
                                 'max_agents': {'type': 'integer',
                                                'minimum': 1,
                                                'maximum': 100,
                                                'description': 'Maximum agents allowed'},
                                 'task_timeout': {'type': 'integer',
                                                  'minimum': 60,
                                                  'maximum': 3600,
                                                  'description': 'Task claim timeout in seconds'},
                                 'claim_timeout': {'type': 'integer',
                                                   'minimum': 60,
                                                   'maximum': 7200,
                                                   'description': 'Resource claim timeout in '
                                                                  'seconds'}},
                  'required': ['swarm_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_swarm_update'}},
 {'name': 'rlm_upload_document',
  'description': 'Upload or update a document in the project. Supports text documents (.md, '
                 '.markdown, .mdx, .txt, .rst, .adoc) and binary parser documents (.pdf, .docx, '
                 '.pptx, .svg, .vsdx, .xlsx). Binary payloads should use base64:<payload> except '
                 'SVG, which may use raw XML.',
  'inputSchema': {'type': 'object',
                  'properties': {'path': {'type': 'string',
                                          'description': "Document path (e.g., 'docs/api.md')"},
                                 'content': {'type': 'string',
                                             'description': 'Document content, or base64:<payload> '
                                                            'for binary files'},
                                 'kind': {'type': 'string',
                                          'enum': ['DOC', 'BINARY'],
                                          'description': 'Document pipeline kind. Inferred from '
                                                         'path when omitted.'},
                                 'format': {'type': 'string',
                                            'enum': ['adoc',
                                                     'docx',
                                                     'markdown',
                                                     'md',
                                                     'mdx',
                                                     'pdf',
                                                     'pptx',
                                                     'rst',
                                                     'svg',
                                                     'txt',
                                                     'vsdx',
                                                     'xlsx'],
                                            'description': 'Document format. Inferred from file '
                                                           'extension when omitted.'},
                                 'language': {'type': 'string',
                                              'description': 'Optional language hint. Usually '
                                                             'omitted for DOC and BINARY uploads.'},
                                 'metadata': {'type': 'object',
                                              'description': 'Optional structured metadata such as '
                                                             'assetClass, usageMode '
                                                             '(current_truth|historical_reference|template|global_knowledge), '
                                                             'clientId, sourceKind, '
                                                             'sourceModifiedAt, sourceSnapshotAt, '
                                                             'sourceContentHash, freshnessPolicy, '
                                                             'parser, and provenance fields',
                                              'additionalProperties': True}},
                  'required': ['path', 'content']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_upload_document'}},
 {'name': 'rlm_sync_documents',
  'description': 'Bulk sync multiple documents. Use for batch uploads or CI/CD integration.',
  'inputSchema': {'type': 'object',
                  'properties': {'documents': {'type': 'array',
                                               'items': {'type': 'object',
                                                         'properties': {'path': {'type': 'string'},
                                                                        'content': {'type': 'string',
                                                                                    'description': 'Plain '
                                                                                                   'text '
                                                                                                   'or '
                                                                                                   'base64:<payload> '
                                                                                                   'for '
                                                                                                   'binary '
                                                                                                   'files'},
                                                                        'kind': {'type': 'string',
                                                                                 'enum': ['DOC',
                                                                                          'BINARY'],
                                                                                 'description': 'Document '
                                                                                                'pipeline '
                                                                                                'kind. '
                                                                                                'Inferred '
                                                                                                'from '
                                                                                                'path '
                                                                                                'when '
                                                                                                'omitted.'},
                                                                        'format': {'type': 'string',
                                                                                   'enum': ['adoc',
                                                                                            'docx',
                                                                                            'markdown',
                                                                                            'md',
                                                                                            'mdx',
                                                                                            'pdf',
                                                                                            'pptx',
                                                                                            'rst',
                                                                                            'svg',
                                                                                            'txt',
                                                                                            'vsdx',
                                                                                            'xlsx'],
                                                                                   'description': 'Document '
                                                                                                  'format. '
                                                                                                  'Inferred '
                                                                                                  'from '
                                                                                                  'file '
                                                                                                  'extension '
                                                                                                  'when '
                                                                                                  'omitted.'},
                                                                        'language': {'type': 'string',
                                                                                     'description': 'Optional '
                                                                                                    'language '
                                                                                                    'hint. '
                                                                                                    'Usually '
                                                                                                    'omitted '
                                                                                                    'for '
                                                                                                    'DOC '
                                                                                                    'and '
                                                                                                    'BINARY '
                                                                                                    'uploads.'},
                                                                        'metadata': {'type': 'object',
                                                                                     'description': 'Optional '
                                                                                                    'structured '
                                                                                                    'metadata '
                                                                                                    'for '
                                                                                                    'business '
                                                                                                    'context, '
                                                                                                    'diagrams, '
                                                                                                    'source '
                                                                                                    'freshness, '
                                                                                                    'historical '
                                                                                                    'references, '
                                                                                                    'templates, '
                                                                                                    'and '
                                                                                                    'provenance',
                                                                                     'additionalProperties': True}},
                                                         'required': ['path', 'content']},
                                               'description': 'Documents to sync'},
                                 'delete_missing': {'type': 'boolean',
                                                    'default': False,
                                                    'description': 'Delete docs not in list. '
                                                                   'Requires '
                                                                   'confirm_delete_missing=true.'},
                                 'confirm_delete_missing': {'type': 'boolean',
                                                            'default': False,
                                                            'description': 'Required true when '
                                                                           'delete_missing=true to '
                                                                           'confirm destructive '
                                                                           'pruning.'}},
                  'required': ['documents']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_sync_documents'}},
 {'name': 'rlm_document_tombstones',
  'description': 'List project-scoped tombstones for deleted or pruned documents. Use this to '
                 'inspect soft-deleted context, understand what was removed, and review expiration '
                 'windows before permanent purge.',
  'inputSchema': {'type': 'object',
                  'properties': {'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 200,
                                           'description': 'Maximum number of tombstones to return'},
                                 'include_expired': {'type': 'boolean',
                                                     'default': False,
                                                     'description': 'Include tombstones that are '
                                                                    'past retention but not yet '
                                                                    'purged'}}},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_document_tombstones'}},
 {'name': 'rlm_svg_bundle_ingest',
  'description': 'Generate a native SVG companion context bundle and optionally upload the '
                 'generated Markdown documents. Use dry_run=true to preview bundle IDs, paths, and '
                 'payload size. Uploaded bundle documents store '
                 'bundleId/sourceHash/sourcePath/artifactRole metadata.',
  'inputSchema': {'type': 'object',
                  'properties': {'svg_content': {'type': 'string',
                                                 'description': 'Raw SVG XML content'},
                                 'source_path': {'type': 'string',
                                                 'description': 'Original SVG path used for stable '
                                                                'bundle identity'},
                                 'upload_prefix': {'type': 'string',
                                                   'default': 'svg-context',
                                                   'description': 'Destination path prefix for '
                                                                  'generated companion documents'},
                                 'include_enriched_svg': {'type': 'boolean',
                                                          'default': True,
                                                          'description': 'Include an enriched SVG '
                                                                         'XML markdown companion'},
                                 'dry_run': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Return the bundle summary without '
                                                            'writing documents'},
                                 'reindex': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Trigger a document reindex job after '
                                                            'a non-dry-run upload'},
                                 'reindex_mode': {'type': 'string',
                                                  'enum': ['incremental', 'full'],
                                                  'default': 'incremental',
                                                  'description': 'Document reindex mode to use '
                                                                 'when reindex=true'}},
                  'required': ['svg_content', 'source_path']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_svg_bundle_ingest'}},
 {'name': 'rlm_request_access',
  'description': 'Request access to a project.\n'
                 '\n'
                 'Allows team members with NONE access level to request higher access levels\n'
                 '(VIEWER, EDITOR, ADMIN) from project admins. Creates an access request that\n'
                 'admins can approve or deny via the dashboard.',
  'inputSchema': {'type': 'object',
                  'properties': {'requested_level': {'type': 'string',
                                                     'enum': ['VIEWER', 'EDITOR', 'ADMIN'],
                                                     'default': 'VIEWER',
                                                     'description': 'The access level to request'},
                                 'reason': {'type': 'string',
                                            'description': 'Optional reason for requesting '
                                                           'access'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_request_access'}},
 {'name': 'rlm_load_document',
  'description': 'Load one exact source document by path. Use when you already know the document '
                 'path and need direct source truth instead of ranked retrieval or memory recall.',
  'inputSchema': {'type': 'object',
                  'properties': {'path': {'type': 'string',
                                          'description': 'Exact document path (for example '
                                                         "'docs/api.md' or "
                                                         "'clients/acme/rfp.md')"}},
                  'required': ['path']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_load_document'}},
 {'name': 'rlm_load_project',
  'description': 'Load structured map of all project documents with content. Returns a '
                 'token-budgeted dump of every file, with optional path filtering. Use for '
                 'full-project exploration.',
  'inputSchema': {'type': 'object',
                  'properties': {'max_tokens': {'type': 'integer',
                                                'default': 16000,
                                                'description': 'Total token budget for returned '
                                                               'content'},
                                 'paths_filter': {'type': 'array',
                                                  'items': {'type': 'string'},
                                                  'description': 'Only include files matching '
                                                                 'these path prefixes (e.g., '
                                                                 "['docs/', 'src/'])"},
                                 'include_content': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Include file content (false = '
                                                                    'metadata only)'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_load_project'}},
 {'name': 'rlm_orchestrate',
  'description': 'Multi-round context exploration in a single call. Performs: (1) section scan for '
                 'project structure, (2) ranked search for top relevant sections, (3) raw file '
                 'load for highest-scoring documents. Combines search intelligence with raw '
                 'access.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'maxLength': 20480,
                                           'description': 'The question or topic to explore'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 16000,
                                                'minimum': 500,
                                                'maximum': 50000,
                                                'description': 'Token budget for raw file content'},
                                 'top_k': {'type': 'integer',
                                           'default': 5,
                                           'minimum': 1,
                                           'maximum': 20,
                                           'description': 'Number of top sections to use for file '
                                                          'selection'},
                                 'search_mode': {'type': 'string',
                                                 'enum': ['keyword', 'semantic', 'hybrid'],
                                                 'default': 'hybrid'}},
                  'required': ['query']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_orchestrate'}},
 {'name': 'rlm_repl_context',
  'description': "Bridge between Snipara's context optimization and Snipara Sandbox code "
                 'execution.\n'
                 '\n'
                 'PURPOSE: Package project documentation into a Python-ready format that can be '
                 'injected into a Snipara Sandbox REPL session for context-aware code execution.\n'
                 '\n'
                 'WORKFLOW:\n'
                 '1. Call rlm_repl_context to get context_data + setup_code\n'
                 "2. Use set_repl_context(key='context', value=context_data) to inject data\n"
                 '3. Use execute_python(setup_code) to load helper functions\n'
                 '4. Use helpers (peek, grep, find_function, etc.) to explore context\n'
                 '5. Execute code with full documentation context available\n'
                 '\n'
                 'USE CASES:\n'
                 '- Implement features with documentation awareness\n'
                 '- Debug code with access to related docs\n'
                 '- Write tests referencing specifications\n'
                 '- Refactor with architecture docs available\n'
                 '\n'
                 'Returns context_data (files + sections), setup_code (helper functions), and '
                 'usage hints.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'Optional query to filter context by '
                                                          'relevance. If empty, loads files in '
                                                          'order within budget.'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 8000,
                                                'description': 'Token budget for file content'},
                                 'include_helpers': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Include Python helper '
                                                                    'functions: peek(), grep(), '
                                                                    'sections(), files(), '
                                                                    'get_file(), search(), trim(), '
                                                                    'find_function(), '
                                                                    'list_imports(), '
                                                                    'context_summary()'},
                                 'search_mode': {'type': 'string',
                                                 'enum': ['keyword', 'semantic', 'hybrid'],
                                                 'default': 'hybrid',
                                                 'description': 'Search mode when query is '
                                                                'provided'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_repl_context'}},
 {'name': 'rlm_get_chunk',
  'description': 'Retrieve full content by chunk ID. Use with '
                 'rlm_context_query(return_references=True) to fetch full content of specific '
                 'sections. This pass-by-reference pattern reduces hallucination by maintaining '
                 'clear source attribution.',
  'inputSchema': {'type': 'object',
                  'properties': {'chunk_id': {'type': 'string',
                                              'description': 'The chunk ID from rlm_context_query '
                                                             'results (when '
                                                             'return_references=True)'},
                                 'correlation_context': {'type': 'object',
                                                         'additionalProperties': False,
                                                         'description': 'Optional '
                                                                        'retrieval-correlation '
                                                                        'context. Reuse session_id '
                                                                        'across retrieval and '
                                                                        'outcome calls so '
                                                                        'telemetry can be joined '
                                                                        'inside the authenticated '
                                                                        'project. These '
                                                                        'identifiers never change '
                                                                        'authorization or project '
                                                                        'scope; do not include '
                                                                        'secrets, tenant IDs, or '
                                                                        'user data.',
                                                         'properties': {'version': {'type': 'string',
                                                                                    'enum': ['retrieval-correlation-v1'],
                                                                                    'default': 'retrieval-correlation-v1'},
                                                                        'session_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Preferred '
                                                                                                      'stable '
                                                                                                      'opaque '
                                                                                                      'session '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'for '
                                                                                                      'telemetry '
                                                                                                      'association.'},
                                                                        'workflow_session_id': {'type': 'string',
                                                                                                'minLength': 1,
                                                                                                'maxLength': 128,
                                                                                                'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                                'description': 'Opaque '
                                                                                                               'workflow '
                                                                                                               'ID '
                                                                                                               'used '
                                                                                                               'when '
                                                                                                               'session_id '
                                                                                                               'is '
                                                                                                               'absent.'},
                                                                        'correlation_id': {'type': 'string',
                                                                                           'minLength': 1,
                                                                                           'maxLength': 128,
                                                                                           'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                           'description': 'Opaque '
                                                                                                          'request-chain '
                                                                                                          'ID '
                                                                                                          'used '
                                                                                                          'when '
                                                                                                          'session '
                                                                                                          'fields '
                                                                                                          'are '
                                                                                                          'absent.'},
                                                                        'request_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Opaque '
                                                                                                      'per-call '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'only '
                                                                                                      'as '
                                                                                                      'a '
                                                                                                      'final '
                                                                                                      'telemetry '
                                                                                                      'fallback.'}}}},
                  'required': ['chunk_id']},
  'annotations': {'title': 'Load cited context chunk',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 8.0,
            'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_get_chunk'},
  'exposed': False},
 {'name': 'rlm_decision_create',
  'description': 'Create a structured decision record (ADR-style) for architectural or technical '
                 'decisions.\n'
                 '\n'
                 'Records decisions with context, rationale, alternatives considered, and revert '
                 'plans.\n'
                 'Auto-generates DEC-XXX IDs. Supports tags for categorization.\n'
                 '\n'
                 'Use for:\n'
                 '- Architectural decisions (database choice, framework selection)\n'
                 '- Technical trade-offs (performance vs maintainability)\n'
                 '- Process decisions (deployment strategy, testing approach)',
  'inputSchema': {'type': 'object',
                  'properties': {'title': {'type': 'string',
                                           'description': 'Short title for the decision (e.g., '
                                                          "'Use Redis for caching')"},
                                 'owner': {'type': 'string',
                                           'description': 'Who made or is responsible for this '
                                                          'decision'},
                                 'scope': {'type': 'string',
                                           'description': "Scope/area affected (e.g., 'backend', "
                                                          "'authentication', 'database')"},
                                 'impact': {'type': 'string',
                                            'enum': ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
                                            'default': 'MEDIUM',
                                            'description': 'Impact level of this decision'},
                                 'context': {'type': 'string',
                                             'description': 'Background and context for why this '
                                                            'decision was needed'},
                                 'decision': {'type': 'string',
                                              'description': 'The actual decision made (what was '
                                                             'chosen)'},
                                 'rationale': {'type': 'string',
                                               'description': 'Why this option was chosen over '
                                                              'alternatives'},
                                 'alternatives': {'type': 'array',
                                                  'items': {'type': 'string'},
                                                  'description': 'List of alternatives that were '
                                                                 'considered'},
                                 'revert_plan': {'type': 'string',
                                                 'description': 'How to revert this decision if '
                                                                'needed (optional)'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Tags for categorization (e.g., '
                                                         "['architecture', 'caching', "
                                                         "'performance'])"}},
                  'required': ['title', 'owner', 'scope', 'context', 'decision', 'rationale']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_decision_create'}},
 {'name': 'rlm_decision_query',
  'description': 'Query project decisions with filters.\n'
                 '\n'
                 'Search by status, impact, scope, tags, or text query.\n'
                 'Returns decisions sorted by recency with supersession chain info.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'Text search in title, context, '
                                                          'decision, rationale'},
                                 'status': {'type': 'string',
                                            'enum': ['ACTIVE', 'SUPERSEDED', 'REVERTED', 'DRAFT'],
                                            'description': 'Filter by decision status'},
                                 'impact': {'type': 'string',
                                            'enum': ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
                                            'description': 'Filter by impact level'},
                                 'scope': {'type': 'string', 'description': 'Filter by scope/area'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Filter by tags (OR logic)'},
                                 'limit': {'type': 'integer',
                                           'default': 10,
                                           'description': 'Maximum decisions to return'},
                                 'include_superseded': {'type': 'boolean',
                                                        'default': False,
                                                        'description': 'Include superseded '
                                                                       'decisions in results'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_decision_query'}},
 {'name': 'rlm_decision_supersede',
  'description': 'Supersede an existing decision with a new one.\n'
                 '\n'
                 'Creates a new decision that replaces an old one, maintaining the chain of '
                 'evolution.\n'
                 'The old decision is marked as SUPERSEDED with a link to the new decision.',
  'inputSchema': {'type': 'object',
                  'properties': {'old_decision_id': {'type': 'string',
                                                     'description': 'The DEC-XXX ID of the '
                                                                    'decision being superseded'},
                                 'title': {'type': 'string',
                                           'description': 'Title for the new decision'},
                                 'owner': {'type': 'string',
                                           'description': 'Who made this new decision'},
                                 'scope': {'type': 'string', 'description': 'Scope/area affected'},
                                 'impact': {'type': 'string',
                                            'enum': ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
                                            'description': 'Impact level'},
                                 'context': {'type': 'string',
                                             'description': 'Why the original decision is being '
                                                            'changed'},
                                 'decision': {'type': 'string', 'description': 'The new decision'},
                                 'rationale': {'type': 'string',
                                               'description': 'Why this change is being made'},
                                 'alternatives': {'type': 'array',
                                                  'items': {'type': 'string'},
                                                  'description': 'Alternatives considered for the '
                                                                 'new decision'},
                                 'revert_plan': {'type': 'string',
                                                 'description': 'How to revert this decision if '
                                                                'needed'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Tags for the new decision'}},
                  'required': ['old_decision_id',
                               'title',
                               'owner',
                               'context',
                               'decision',
                               'rationale']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_decision_supersede'}},
 {'name': 'rlm_index_health',
  'description': 'Get comprehensive index health metrics for your project.\n'
                 '\n'
                 'Returns coverage, quality scores, tier distribution, stale document detection, '
                 'and overall health score.\n'
                 'Use this to monitor the health of your documentation index and identify issues.',
  'inputSchema': {'type': 'object',
                  'properties': {'stale_threshold_days': {'type': 'integer',
                                                          'default': 30,
                                                          'minimum': 1,
                                                          'maximum': 365,
                                                          'description': 'Days after which content '
                                                                         'is considered stale'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_index_health'}},
 {'name': 'rlm_index_recommendations',
  'description': 'Get actionable recommendations to improve your index health.\n'
                 '\n'
                 'Returns prioritized list of recommendations based on current index health '
                 'metrics.\n'
                 'Recommendations include actions like reindexing, improving coverage, and '
                 'reviewing quality.',
  'inputSchema': {'type': 'object', 'properties': {}, 'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_index_recommendations'}},
 {'name': 'rlm_reindex',
  'description': 'Trigger a project reindex job or poll an existing reindex job.\n'
                 '\n'
                 'Use this when index coverage is low, documents are missing chunks, or you need '
                 'to rebuild\n'
                 'documentation/code indexes after large sync operations. Call without job_id to '
                 'create a job,\n'
                 'or pass job_id to check progress via MCP.',
  'inputSchema': {'type': 'object',
                  'properties': {'job_id': {'type': 'string',
                                            'description': 'Existing reindex job ID to poll '
                                                           'instead of creating a new one'},
                                 'mode': {'type': 'string',
                                          'enum': ['incremental', 'full'],
                                          'default': 'incremental',
                                          'description': 'Reindex mode when creating a new job'},
                                 'kind': {'type': 'string',
                                          'enum': ['doc', 'code'],
                                          'default': 'doc',
                                          'description': 'Which index to rebuild when creating a '
                                                         'new job'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_reindex'}},
 {'name': 'rlm_search_analytics',
  'description': 'Get comprehensive search analytics for your project.\n'
                 '\n'
                 'Returns query counts, success rates, latency percentiles, tool usage breakdown,\n'
                 'daily trends, and error analysis for the specified time period.',
  'inputSchema': {'type': 'object',
                  'properties': {'days': {'type': 'integer',
                                          'default': 30,
                                          'minimum': 1,
                                          'maximum': 90,
                                          'description': 'Number of days to analyze'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_search_analytics'}},
 {'name': 'rlm_query_trends',
  'description': 'Get query trends over time with configurable granularity.\n'
                 '\n'
                 'Returns time-bucketed query counts, success rates, and latency for trend '
                 'analysis.',
  'inputSchema': {'type': 'object',
                  'properties': {'days': {'type': 'integer',
                                          'default': 7,
                                          'minimum': 1,
                                          'maximum': 30,
                                          'description': 'Number of days to analyze'},
                                 'granularity': {'type': 'string',
                                                 'enum': ['hour', 'day'],
                                                 'default': 'hour',
                                                 'description': 'Time bucket granularity'}},
                  'required': []},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_query_trends'}},
 {'name': 'rlm_adaptive_routing_catalog',
  'description': 'Build a sanitized Adaptive Work Routing runtime catalog for the current '
                 'project.\n'
                 '\n'
                 'Returns provider-neutral worker candidates from project BYOM/local provider '
                 'configuration. Secrets, API keys, ciphertext, and endpoint credentials are never '
                 'returned; workers must use the server-side gateway for execution.',
  'inputSchema': {'type': 'object',
                  'properties': {'work_profile': {'type': 'object',
                                                  'description': 'Optional task profile from '
                                                                 'Adaptive Work Routing.'},
                                 'model_requirements': {'type': 'object',
                                                        'description': 'Optional provider-neutral '
                                                                       'worker requirements used '
                                                                       'to filter endpoint types.'},
                                 'include_disabled': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include disabled provider '
                                                                     'configs for diagnostics.'},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 100,
                                           'description': 'Maximum number of sanitized candidates '
                                                          'to return.'}},
                  'required': []},
  'annotations': {'title': 'Build adaptive routing catalog',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_adaptive_routing_catalog'}},
 {'name': 'rlm_adaptive_routing_approve',
  'description': 'Approve or reject an Adaptive Work Routing recommendation through a direct MCP '
                 'coding-agent contract.\n'
                 '\n'
                 'Returns a project-scoped approval receipt that companion, orchestrator, and '
                 'gateway code can verify before treating delegated work as approved. This is not '
                 'a UI approval surface; it is intended for explicit coding-agent approval calls.',
  'inputSchema': {'type': 'object',
                  'properties': {'decision': {'type': 'string',
                                              'enum': ['approve', 'reject', 'needs_changes'],
                                              'default': 'approve',
                                              'description': 'Approval decision for the routed '
                                                             'work package.'},
                                 'idempotency_key': {'type': 'string',
                                                     'minLength': 8,
                                                     'maxLength': 160,
                                                     'description': 'Stable key supplied by the '
                                                                    'coding agent to make approval '
                                                                    'retries idempotent.'},
                                 'approval_subject': {'type': 'object',
                                                      'description': 'Optional structured routing '
                                                                     'recommendation, handoff, or '
                                                                     'task subject.'},
                                 'approval_subject_id': {'type': 'string',
                                                         'description': 'Optional stable subject '
                                                                        'identifier.'},
                                 'routing_recommendation_id': {'type': 'string',
                                                               'description': 'Optional routing '
                                                                              'recommendation '
                                                                              'identifier.'},
                                 'handoff_id': {'type': 'string',
                                                'description': 'Optional orchestrator or companion '
                                                               'handoff identifier.'},
                                 'routing_card': {'type': 'object',
                                                  'description': 'Optional routing card being '
                                                                 'approved.'},
                                 'approved_write_scope': {'type': 'array',
                                                          'items': {'type': 'string'},
                                                          'default': [],
                                                          'description': 'Exact write scopes '
                                                                         'approved for the worker. '
                                                                         'Empty means no writes '
                                                                         'approved.'},
                                 'approved_endpoint_types': {'type': 'array',
                                                             'items': {'type': 'string'},
                                                             'default': [],
                                                             'description': 'Endpoint types '
                                                                            'approved for this '
                                                                            'handoff, for example '
                                                                            'local or cloud.'},
                                 'max_cost_cents': {'type': 'integer',
                                                    'minimum': 0,
                                                    'maximum': 1000000,
                                                    'description': 'Optional per-approval cost '
                                                                   'ceiling in cents.'},
                                 'expires_at': {'type': 'string',
                                                'format': 'date-time',
                                                'description': 'Optional ISO timestamp after which '
                                                               'the approval must fail closed.'},
                                 'reason': {'type': 'string',
                                            'maxLength': 2000,
                                            'description': 'Short rationale for the approval '
                                                           'decision.'},
                                 'evidence_refs': {'type': 'array',
                                                   'items': {'type': 'string'},
                                                   'default': [],
                                                   'maxItems': 25,
                                                   'description': 'Evidence references used by the '
                                                                  'coding agent to approve or '
                                                                  'reject.'},
                                 'approver_agent_id': {'type': 'string',
                                                       'maxLength': 160,
                                                       'description': 'Stable coding-agent '
                                                                      'identifier supplied by the '
                                                                      'caller.'}},
                  'required': ['idempotency_key']},
  'annotations': {'title': 'Approve adaptive routing handoff',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_adaptive_routing_approve'}},
 {'name': 'rlm_htask_create',
  'description': 'Create a hierarchical task at any level (N0-N3).\n'
                 '\n'
                 'Supports 4-level hierarchy: N0_INITIATIVE > N1_FEATURE > N2_WORKSTREAM > '
                 'N3_TASK.\n'
                 'Tasks have owners, priorities, acceptance criteria, and evidence requirements.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string',
                                              'description': 'Swarm ID. Optional when '
                                                             'auto_create_swarm is true.'},
                                 'auto_create_swarm': {'type': 'boolean',
                                                       'default': True,
                                                       'description': 'Create or reuse a default '
                                                                      'project swarm when swarm_id '
                                                                      'is omitted'},
                                 'swarm_name': {'type': 'string',
                                                'description': 'Project-scoped swarm name to '
                                                               'create or reuse when swarm_id is '
                                                               'omitted'},
                                 'swarm_description': {'type': 'string',
                                                       'description': 'Description for the '
                                                                      'auto-created swarm'},
                                 'swarm_max_agents': {'type': 'integer',
                                                      'default': 10,
                                                      'description': 'Max agents for the '
                                                                     'auto-created swarm'},
                                 'level': {'type': 'string',
                                           'enum': ['N0_INITIATIVE',
                                                    'N1_FEATURE',
                                                    'N2_WORKSTREAM',
                                                    'N3_TASK'],
                                           'default': 'N3_TASK',
                                           'description': 'Task hierarchy level'},
                                 'title': {'type': 'string', 'description': 'Task title'},
                                 'description': {'type': 'string',
                                                 'description': 'Task description'},
                                 'owner': {'type': 'string',
                                           'description': 'Task owner (required)'},
                                 'parent_id': {'type': 'string',
                                               'description': 'Parent task ID (required for '
                                                              'N1-N3)'},
                                 'priority': {'type': 'string',
                                              'enum': ['P0', 'P1', 'P2'],
                                              'default': 'P1',
                                              'description': 'Priority level'},
                                 'eta_target': {'type': 'string',
                                                'description': 'Target completion date (ISO '
                                                               'format)'},
                                 'execution_target': {'type': 'string',
                                                      'enum': ['LOCAL',
                                                               'CLOUD',
                                                               'HYBRID',
                                                               'EXTERNAL'],
                                                      'description': 'Where the task executes'},
                                 'workstream_type': {'type': 'string',
                                                     'enum': ['API',
                                                              'FRONTEND',
                                                              'QA',
                                                              'BUGFIX_HARDENING',
                                                              'DEPLOY_PROD_VERIFY',
                                                              'DATA',
                                                              'SECURITY',
                                                              'DOCUMENTATION',
                                                              'CUSTOM',
                                                              'OTHER'],
                                                     'description': 'Workstream type for N2 tasks'},
                                 'custom_workstream_type': {'type': 'string',
                                                            'description': 'Required label when '
                                                                           'workstream_type is '
                                                                           'CUSTOM'},
                                 'acceptance_criteria': {'type': 'array',
                                                         'items': {'type': 'object'},
                                                         'description': 'List of acceptance '
                                                                        'criteria [{id, text, '
                                                                        'checked}]'},
                                 'context_refs': {'type': 'array',
                                                  'items': {'type': 'string'},
                                                  'description': 'Context references (URLs, file '
                                                                 'paths)'},
                                 'context_query': {'type': 'string',
                                                   'description': 'Auto-fetch relevant docs via '
                                                                  'rlm_context_query and add to '
                                                                  "context_refs (e.g., 'JWT "
                                                                  "authentication patterns')"},
                                 'evidence_required': {'type': 'array',
                                                       'items': {'type': 'object'},
                                                       'description': 'Required evidence [{type, '
                                                                      'description}]'},
                                 'is_blocking': {'type': 'boolean',
                                                 'default': True,
                                                 'description': 'Whether task blocks parent '
                                                                'closure when failed/incomplete'}},
                  'required': ['title', 'description', 'owner']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_create'}},
 {'name': 'rlm_htask_create_feature',
  'description': 'Create a N1 feature with standard workstreams.\n'
                 '\n'
                 'Creates a feature (N1) with automatic N2 workstreams: API, FRONTEND, QA, '
                 'BUGFIX_HARDENING, DEPLOY_PROD_VERIFY.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string',
                                              'description': 'Swarm ID. Optional when '
                                                             'auto_create_swarm is true.'},
                                 'auto_create_swarm': {'type': 'boolean',
                                                       'default': True,
                                                       'description': 'Create or reuse a default '
                                                                      'project swarm when swarm_id '
                                                                      'is omitted'},
                                 'swarm_name': {'type': 'string',
                                                'description': 'Project-scoped swarm name to '
                                                               'create or reuse when swarm_id is '
                                                               'omitted'},
                                 'swarm_description': {'type': 'string',
                                                       'description': 'Description for the '
                                                                      'auto-created swarm'},
                                 'swarm_max_agents': {'type': 'integer',
                                                      'default': 10,
                                                      'description': 'Max agents for the '
                                                                     'auto-created swarm'},
                                 'title': {'type': 'string', 'description': 'Feature title'},
                                 'description': {'type': 'string',
                                                 'description': 'Feature description'},
                                 'owner': {'type': 'string', 'description': 'Feature owner'},
                                 'parent_id': {'type': 'string',
                                               'description': 'Optional N0 parent'},
                                 'create_initiative': {'type': 'boolean',
                                                       'default': False,
                                                       'description': 'Create an N0 initiative '
                                                                      'parent when parent_id is '
                                                                      'omitted'},
                                 'initiative_title': {'type': 'string',
                                                      'description': 'Optional title for the N0 '
                                                                     'initiative'},
                                 'initiative_description': {'type': 'string',
                                                            'description': 'Optional description '
                                                                           'for the N0 initiative'},
                                 'workstreams': {'type': 'array',
                                                 'items': {'type': 'string'},
                                                 'description': 'Standard workstream types or '
                                                                'custom labels to create (defaults '
                                                                'to standard set)'},
                                 'custom_workstreams': {'type': 'array',
                                                        'items': {'type': 'string'},
                                                        'description': 'Custom N2 workstream '
                                                                       'labels created as CUSTOM '
                                                                       'workstreams'},
                                 'workstream_owners': {'type': 'object',
                                                       'additionalProperties': {'type': 'string'},
                                                       'description': 'Map of workstream type or '
                                                                      'CUSTOM:<label> to owner'},
                                 'create_actionable_tasks': {'type': 'boolean',
                                                             'default': True,
                                                             'description': 'Create actionable N3 '
                                                                            'starter tasks under '
                                                                            'each N2 workstream'},
                                 'task_blueprints': {'type': 'object',
                                                     'description': 'Optional per-workstream N3 '
                                                                    'task blueprint overrides'}},
                  'required': ['title', 'description', 'owner']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_htask_create_feature'}},
 {'name': 'rlm_htask_get',
  'description': 'Get a hierarchical task with its children.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'include_children': {'type': 'boolean',
                                                      'default': True,
                                                      'description': 'Include direct children'}},
                  'required': ['swarm_id', 'task_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_get'}},
 {'name': 'rlm_htask_tree',
  'description': 'Get full hierarchical tree from a node.\n'
                 '\n'
                 'Returns recursive tree structure with all descendants up to max_depth.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string',
                                             'description': 'Root task ID (optional, defaults to '
                                                            'all roots)'},
                                 'max_depth': {'type': 'integer',
                                               'default': 4,
                                               'description': 'Maximum depth to traverse'},
                                 'include_archived': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include archived tasks'},
                                 'include_completed': {'type': 'boolean',
                                                       'default': True,
                                                       'description': 'Include completed and '
                                                                      'cancelled descendants in '
                                                                      'the tree'}},
                  'required': ['swarm_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_tree'}},
 {'name': 'rlm_htask_update',
  'description': 'Update task fields (whitelist enforced by status).\n'
                 '\n'
                 'Different fields are updatable based on task status. Structural fields require '
                 'admin.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'updates': {'type': 'object', 'description': 'Fields to update'},
                                 'is_admin': {'type': 'boolean',
                                              'default': False,
                                              'description': 'Admin privileges for structural '
                                                             'updates'}},
                  'required': ['swarm_id', 'task_id', 'updates']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_update'}},
 {'name': 'rlm_htask_block',
  'description': 'Block a task with detailed payload.\n'
                 '\n'
                 'Requires blocker_type and blocker_reason. Automatically propagates to ancestors '
                 'if is_blocking=true.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'blocker_type': {'type': 'string',
                                                  'enum': ['TECH',
                                                           'DEPENDENCY',
                                                           'ACCESS',
                                                           'PRODUCT',
                                                           'INFRA',
                                                           'SECURITY',
                                                           'OTHER'],
                                                  'description': 'Type of blocker'},
                                 'blocker_reason': {'type': 'string',
                                                    'description': 'Detailed explanation'},
                                 'blocked_by_task_id': {'type': 'string',
                                                        'description': 'ID of blocking task'},
                                 'required_input': {'type': 'string',
                                                    'description': "What's needed to unblock"},
                                 'eta_recovery': {'type': 'string',
                                                  'description': 'Expected unblock date (ISO)'},
                                 'escalation_to': {'type': 'string',
                                                   'description': 'Who to escalate to'}},
                  'required': ['swarm_id', 'task_id', 'blocker_type', 'blocker_reason']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_block'}},
 {'name': 'rlm_htask_unblock',
  'description': 'Unblock a task and re-evaluate ancestor status.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'resolution': {'type': 'string',
                                                'description': 'How the blocker was resolved'}},
                  'required': ['swarm_id', 'task_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_unblock'}},
 {'name': 'rlm_htask_complete',
  'description': 'Complete an N3 task with evidence and optional memory creation.\n'
                 '\n'
                 'Evidence may be required based on policy. Use for leaf tasks (N3_TASK).\n'
                 'Automatically creates a linked memory with task outcome, learnings, and decision '
                 'impact.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'evidence': {'type': 'array',
                                              'items': {'type': 'object'},
                                              'description': 'Evidence list [{type, description, '
                                                             '...}]'},
                                 'result': {'type': 'object', 'description': 'Task result data'},
                                 'learnings': {'type': 'array',
                                               'items': {'type': 'string'},
                                               'description': 'Lessons learned from this task'},
                                 'decision_impact': {'type': 'string',
                                                     'description': 'How this task affects future '
                                                                    'decisions'},
                                 'work_profile': {'type': 'object',
                                                  'description': 'Optional Adaptive Work Routing '
                                                                 'work profile used for '
                                                                 'delegation.'},
                                 'model_requirements': {'type': 'object',
                                                        'description': 'Optional provider-neutral '
                                                                       'worker requirements used '
                                                                       'by routing.'},
                                 'routing_receipt': {'type': 'object',
                                                     'description': 'Optional worker cost/outcome '
                                                                    'receipt for quality-adjusted '
                                                                    'routing.'},
                                 'create_memory': {'type': 'boolean',
                                                   'default': True,
                                                   'description': 'Auto-create a memory with task '
                                                                  'outcome (default: true)'}},
                  'required': ['swarm_id', 'task_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_complete'}},
 {'name': 'rlm_htask_verify_closure',
  'description': 'Verify if a parent task can be closed.\n'
                 '\n'
                 'Checks all children status against closure policy. Returns blockers and waiver '
                 'requirements.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'}},
                  'required': ['swarm_id', 'task_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_htask_verify_closure'}},
 {'name': 'rlm_htask_close',
  'description': 'Close a parent task (with optional waiver).\n'
                 '\n'
                 'Use waiver_reason and waiver_approved_by when closing with exceptions (if policy '
                 'allows).',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'waiver_reason': {'type': 'string',
                                                   'description': 'Reason for waiver'},
                                 'waiver_approved_by': {'type': 'string',
                                                        'description': 'Who approved the waiver'}},
                  'required': ['swarm_id', 'task_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_close'}},
 {'name': 'rlm_htask_delete',
  'description': 'Delete a task (soft by default, hard with force flag).\n'
                 '\n'
                 'Soft delete archives the task. Hard delete removes permanently (requires policy '
                 '+ admin).',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'force': {'type': 'boolean',
                                           'default': False,
                                           'description': 'Hard delete (requires policy + admin)'},
                                 'cascade': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Delete all descendants'},
                                 'is_admin': {'type': 'boolean',
                                              'default': False,
                                              'description': 'Admin privileges'}},
                  'required': ['swarm_id', 'task_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_delete'}},
 {'name': 'rlm_htask_recommend_batch',
  'description': 'Get recommended batch of N3 tasks ready to work on.\n'
                 '\n'
                 'Returns prioritized list of unblocked, pending N3 tasks. Filter by feature_id or '
                 'workstream_type for focused recommendations.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'feature_id': {'type': 'string',
                                                'description': 'Filter to tasks under this N1 '
                                                               'feature'},
                                 'workstream_type': {'type': 'string',
                                                     'enum': ['API',
                                                              'FRONTEND',
                                                              'QA',
                                                              'BUGFIX_HARDENING',
                                                              'DEPLOY_PROD_VERIFY',
                                                              'DATA',
                                                              'SECURITY',
                                                              'DOCUMENTATION',
                                                              'CUSTOM',
                                                              'OTHER'],
                                                     'description': 'Filter to tasks in this '
                                                                    'workstream type'},
                                 'limit': {'type': 'integer',
                                           'default': 5,
                                           'description': 'Maximum tasks to return'},
                                 'owner': {'type': 'string', 'description': 'Filter by owner'},
                                 'exclude_blocked': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Exclude blocked tasks'},
                                 'claim_for_agent': {'type': 'string',
                                                     'description': 'If set, atomically claim '
                                                                    'returned ready N3 tasks for '
                                                                    'this agent'}},
                  'required': ['swarm_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_htask_recommend_batch'}},
 {'name': 'rlm_htask_policy_get',
  'description': 'Get the htask policy configuration for a swarm.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'}},
                  'required': ['swarm_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_policy_get'}},
 {'name': 'rlm_htask_policy_update',
  'description': 'Update the htask policy for a swarm.\n'
                 '\n'
                 'Admin-only fields: allowStructuralUpdate, allowHardDelete, compatMode.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'updates': {'type': 'object',
                                             'description': 'Policy fields to update'},
                                 'is_admin': {'type': 'boolean',
                                              'default': False,
                                              'description': 'Admin privileges'}},
                  'required': ['swarm_id', 'updates']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_policy_update'}},
 {'name': 'rlm_htask_metrics',
  'description': 'Get comprehensive metrics for htasks in a swarm.\n'
                 '\n'
                 'Includes throughput, aging by level, blocked/recovered ratio, and top blockers.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'period_hours': {'type': 'integer',
                                                  'default': 24,
                                                  'description': 'Period for time-based metrics'}},
                  'required': ['swarm_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_metrics'}},
 {'name': 'rlm_htask_audit_trail',
  'description': 'Get complete audit trail for a specific task.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'}},
                  'required': ['swarm_id', 'task_id']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True, 'snipara_advertised_tool': 'snipara_htask_audit_trail'}},
 {'name': 'rlm_htask_checkpoint_delta',
  'description': 'Get delta report since last checkpoint.\n'
                 '\n'
                 'Returns events, closures, blocks since the specified timestamp.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'since': {'type': 'string',
                                           'description': 'ISO timestamp of last checkpoint'}},
                  'required': ['swarm_id', 'since']},
  'exposed': False,
  '_meta': {'snipara_legacy_tool': True,
            'snipara_advertised_tool': 'snipara_htask_checkpoint_delta'}},
 {'name': 'snipara_context_query',
  'description': 'Query project documents, parsed business files, and shared context. Use this '
                 'first for source truth and narrative documentation. Returns a source-grounded '
                 'answer_pack plus retrieval_diagnostics and ranked sections within token budget. '
                 'If a broad query times out, retry once with a narrow 3-8 term query, max_tokens '
                 "800-1500, search_mode='keyword', return_references=true, auto_decompose=false, "
                 'and include_all_tiers=false. For exact text use snipara_search; for structural '
                 'code context use snipara_code_neighbors, snipara_code_callers, or '
                 'snipara_code_imports.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'Documentation, business-context, or '
                                                          'current-truth question. For timeout '
                                                          'recovery, narrow this to the key file, '
                                                          'feature, symbol, or 3-8 terms.'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 100,
                                                'maximum': 100000,
                                                'description': 'Token budget. Use 800-1500 for '
                                                               'fast recovery retries after a '
                                                               'timeout.'},
                                 'search_mode': {'type': 'string',
                                                 'enum': ['keyword', 'semantic', 'hybrid'],
                                                 'default': 'hybrid',
                                                 'description': 'Search strategy. Use keyword for '
                                                                'fast retry/recovery paths; use '
                                                                'hybrid for normal documentation '
                                                                'discovery.'},
                                 'include_metadata': {'type': 'boolean', 'default': True},
                                 'prefer_summaries': {'type': 'boolean', 'default': False},
                                 'return_references': {'type': 'boolean',
                                                       'default': False,
                                                       'description': 'Return chunk references '
                                                                      '(IDs + previews) instead of '
                                                                      'full content. Use '
                                                                      'snipara_get_chunk to '
                                                                      'retrieve full content by '
                                                                      'ID. Reduces hallucination '
                                                                      'by maintaining clear source '
                                                                      'attribution and is the '
                                                                      'preferred fast retry path '
                                                                      'after a timeout.'},
                                 'include_answer_pack': {'type': 'boolean',
                                                         'default': True,
                                                         'description': 'Include a structured '
                                                                        'answer pack with source '
                                                                        'facts, caveats, '
                                                                        'verification checklist, '
                                                                        'and code/context hints '
                                                                        'before the ranked context '
                                                                        'sections.'},
                                 'auto_decompose': {'type': 'boolean',
                                                    'default': True,
                                                    'description': 'Auto-decompose complex queries '
                                                                   'into sub-queries (Pro+ only). '
                                                                   'Complex queries (50+ words, '
                                                                   'multiple questions, '
                                                                   'comparisons) are automatically '
                                                                   'broken down and results '
                                                                   'merged. Set to False for fast '
                                                                   'timeout recovery retries.'},
                                 'include_all_tiers': {'type': 'boolean',
                                                       'default': False,
                                                       'description': 'Include all context tiers '
                                                                      'including COLD and ARCHIVE. '
                                                                      'By default, searches only '
                                                                      'HOT and WARM tiers for '
                                                                      'faster, more relevant '
                                                                      'results.'},
                                 'task': {'type': 'string',
                                          'minLength': 1,
                                          'maxLength': 512,
                                          'description': 'Optional task label that scopes the '
                                                         'live-join fallback and retrieval '
                                                         'correlation; persisted outcome posterior '
                                                         'statistics remain project-wide'},
                                 'context_chunk_outcome_rerank_mode': {'type': 'string',
                                                                       'enum': ['disabled',
                                                                                'shadow',
                                                                                'enabled'],
                                                                       'default': 'disabled',
                                                                       'description': 'Requested '
                                                                                      'bounded '
                                                                                      'chunk-outcome '
                                                                                      'rerank '
                                                                                      'mode. This '
                                                                                      'request can '
                                                                                      'disable or '
                                                                                      'lower the '
                                                                                      'server-configured '
                                                                                      'mode but '
                                                                                      'cannot '
                                                                                      'escalate '
                                                                                      'beyond it.'},
                                 'context_chunk_outcome_window_hours': {'type': 'integer',
                                                                        'default': 72,
                                                                        'minimum': 1,
                                                                        'maximum': 336,
                                                                        'description': 'Strict '
                                                                                       'attribution '
                                                                                       'window for '
                                                                                       'compatible '
                                                                                       'chunk '
                                                                                       'outcomes.'},
                                 'correlation_context': {'type': 'object',
                                                         'additionalProperties': False,
                                                         'description': 'Optional '
                                                                        'retrieval-correlation '
                                                                        'context. Reuse session_id '
                                                                        'across retrieval and '
                                                                        'outcome calls so '
                                                                        'telemetry can be joined '
                                                                        'inside the authenticated '
                                                                        'project. These '
                                                                        'identifiers never change '
                                                                        'authorization or project '
                                                                        'scope; do not include '
                                                                        'secrets, tenant IDs, or '
                                                                        'user data.',
                                                         'properties': {'version': {'type': 'string',
                                                                                    'enum': ['retrieval-correlation-v1'],
                                                                                    'default': 'retrieval-correlation-v1'},
                                                                        'session_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Preferred '
                                                                                                      'stable '
                                                                                                      'opaque '
                                                                                                      'session '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'for '
                                                                                                      'telemetry '
                                                                                                      'association.'},
                                                                        'workflow_session_id': {'type': 'string',
                                                                                                'minLength': 1,
                                                                                                'maxLength': 128,
                                                                                                'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                                'description': 'Opaque '
                                                                                                               'workflow '
                                                                                                               'ID '
                                                                                                               'used '
                                                                                                               'when '
                                                                                                               'session_id '
                                                                                                               'is '
                                                                                                               'absent.'},
                                                                        'correlation_id': {'type': 'string',
                                                                                           'minLength': 1,
                                                                                           'maxLength': 128,
                                                                                           'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                           'description': 'Opaque '
                                                                                                          'request-chain '
                                                                                                          'ID '
                                                                                                          'used '
                                                                                                          'when '
                                                                                                          'session '
                                                                                                          'fields '
                                                                                                          'are '
                                                                                                          'absent.'},
                                                                        'request_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Opaque '
                                                                                                      'per-call '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'only '
                                                                                                      'as '
                                                                                                      'a '
                                                                                                      'final '
                                                                                                      'telemetry '
                                                                                                      'fallback.'}}}},
                  'required': ['query']},
  'annotations': {'title': 'Query Snipara context',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 24.0}},
 {'name': 'snipara_ask',
  'description': 'Query documentation with a question (basic). Use snipara_context_query for '
                 'better results.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string', 'description': 'The question to ask'},
                                 'correlation_context': {'type': 'object',
                                                         'additionalProperties': False,
                                                         'description': 'Optional '
                                                                        'retrieval-correlation '
                                                                        'context. Reuse session_id '
                                                                        'across retrieval and '
                                                                        'outcome calls so '
                                                                        'telemetry can be joined '
                                                                        'inside the authenticated '
                                                                        'project. These '
                                                                        'identifiers never change '
                                                                        'authorization or project '
                                                                        'scope; do not include '
                                                                        'secrets, tenant IDs, or '
                                                                        'user data.',
                                                         'properties': {'version': {'type': 'string',
                                                                                    'enum': ['retrieval-correlation-v1'],
                                                                                    'default': 'retrieval-correlation-v1'},
                                                                        'session_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Preferred '
                                                                                                      'stable '
                                                                                                      'opaque '
                                                                                                      'session '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'for '
                                                                                                      'telemetry '
                                                                                                      'association.'},
                                                                        'workflow_session_id': {'type': 'string',
                                                                                                'minLength': 1,
                                                                                                'maxLength': 128,
                                                                                                'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                                'description': 'Opaque '
                                                                                                               'workflow '
                                                                                                               'ID '
                                                                                                               'used '
                                                                                                               'when '
                                                                                                               'session_id '
                                                                                                               'is '
                                                                                                               'absent.'},
                                                                        'correlation_id': {'type': 'string',
                                                                                           'minLength': 1,
                                                                                           'maxLength': 128,
                                                                                           'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                           'description': 'Opaque '
                                                                                                          'request-chain '
                                                                                                          'ID '
                                                                                                          'used '
                                                                                                          'when '
                                                                                                          'session '
                                                                                                          'fields '
                                                                                                          'are '
                                                                                                          'absent.'},
                                                                        'request_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Opaque '
                                                                                                      'per-call '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'only '
                                                                                                      'as '
                                                                                                      'a '
                                                                                                      'final '
                                                                                                      'telemetry '
                                                                                                      'fallback.'}}}},
                  'required': ['query']},
  '_meta': {'snipara_tool_weight': -6.0}},
 {'name': 'snipara_search',
  'description': 'Search indexed documentation with an exact regex pattern. This is a grep-like '
                 'text search, not semantic retrieval; use snipara_context_query(query=...) for '
                 'source-truth semantic/context search.',
  'inputSchema': {'type': 'object',
                  'properties': {'pattern': {'type': 'string',
                                             'description': 'Regex text pattern to search for.'},
                                 'query': {'type': 'string',
                                           'description': 'Alias for pattern for clients that '
                                                          'normalize search inputs to query.'},
                                 'max_results': {'type': 'integer',
                                                 'default': 20,
                                                 'minimum': 1,
                                                 'maximum': 100,
                                                 'description': 'Maximum regex matches to return.'},
                                 'correlation_context': {'type': 'object',
                                                         'additionalProperties': False,
                                                         'description': 'Optional '
                                                                        'retrieval-correlation '
                                                                        'context. Reuse session_id '
                                                                        'across retrieval and '
                                                                        'outcome calls so '
                                                                        'telemetry can be joined '
                                                                        'inside the authenticated '
                                                                        'project. These '
                                                                        'identifiers never change '
                                                                        'authorization or project '
                                                                        'scope; do not include '
                                                                        'secrets, tenant IDs, or '
                                                                        'user data.',
                                                         'properties': {'version': {'type': 'string',
                                                                                    'enum': ['retrieval-correlation-v1'],
                                                                                    'default': 'retrieval-correlation-v1'},
                                                                        'session_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Preferred '
                                                                                                      'stable '
                                                                                                      'opaque '
                                                                                                      'session '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'for '
                                                                                                      'telemetry '
                                                                                                      'association.'},
                                                                        'workflow_session_id': {'type': 'string',
                                                                                                'minLength': 1,
                                                                                                'maxLength': 128,
                                                                                                'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                                'description': 'Opaque '
                                                                                                               'workflow '
                                                                                                               'ID '
                                                                                                               'used '
                                                                                                               'when '
                                                                                                               'session_id '
                                                                                                               'is '
                                                                                                               'absent.'},
                                                                        'correlation_id': {'type': 'string',
                                                                                           'minLength': 1,
                                                                                           'maxLength': 128,
                                                                                           'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                           'description': 'Opaque '
                                                                                                          'request-chain '
                                                                                                          'ID '
                                                                                                          'used '
                                                                                                          'when '
                                                                                                          'session '
                                                                                                          'fields '
                                                                                                          'are '
                                                                                                          'absent.'},
                                                                        'request_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Opaque '
                                                                                                      'per-call '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'only '
                                                                                                      'as '
                                                                                                      'a '
                                                                                                      'final '
                                                                                                      'telemetry '
                                                                                                      'fallback.'}}}},
                  'required': []},
  '_meta': {'snipara_tool_weight': 4.0}},
 {'name': 'snipara_read',
  'description': 'Read specific lines from indexed documentation. Pass file_path to read a '
                 'document-local line range; omit file_path to read global indexed lines.',
  'inputSchema': {'type': 'object',
                  'properties': {'file_path': {'type': 'string',
                                               'description': 'Indexed document path. Also '
                                                              'accepted by the handler as file, '
                                                              'path, or document.'},
                                 'start_line': {'type': 'integer',
                                                'default': 1,
                                                'description': 'Starting line number. Relative to '
                                                               'file_path when provided; otherwise '
                                                               'global index line.'},
                                 'end_line': {'type': 'integer',
                                              'description': 'Ending line number. Defaults to '
                                                             'start_line + 50.'}},
                  'required': []}},
 {'name': 'snipara_code_callers',
  'description': 'USE WHEN: who calls this symbol, especially before renaming, deleting, or '
                 'changing a signature. Hosted fallback/canonical indexed graph: if you have shell '
                 'access and local commits or a dirty working tree may matter, run '
                 '`snipara-companion code callers` first because it auto-selects the local '
                 'overlay; use this MCP tool when companion is unavailable or after push/reindex.',
  'inputSchema': {'type': 'object',
                  'properties': {'qualified_name': {'type': 'string',
                                                    'description': 'Repo-qualified symbol name'},
                                 'symbol_key': {'type': 'string',
                                                'description': 'Stable symbol key for an exact '
                                                               'match'},
                                 'depth': {'type': 'integer',
                                           'default': 1,
                                           'minimum': 1,
                                           'maximum': 4},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 200},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Find code callers',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 6.0}},
 {'name': 'snipara_code_imports',
  'description': 'USE WHEN: what a file or symbol imports, or who imports a module before moving '
                 'or renaming it. Hosted fallback/canonical indexed graph: if you have shell '
                 'access and local commits or a dirty working tree may matter, run '
                 '`snipara-companion code imports` first because it auto-selects the local '
                 'overlay; use this MCP tool when companion is unavailable or after push/reindex.',
  'inputSchema': {'type': 'object',
                  'properties': {'qualified_name': {'type': 'string',
                                                    'description': 'Repo-qualified symbol name'},
                                 'symbol_key': {'type': 'string',
                                                'description': 'Stable symbol key for an exact '
                                                               'match'},
                                 'file_path': {'type': 'string',
                                               'description': 'Resolve imports for a specific file '
                                                              'path'},
                                 'direction': {'type': 'string',
                                               'enum': ['out', 'in'],
                                               'default': 'out'},
                                 'include_file_nodes': {'type': 'boolean',
                                                        'default': False,
                                                        'description': 'For file_path lookups, '
                                                                       'include every scanned '
                                                                       'symbol in matched_targets '
                                                                       'instead of the compact '
                                                                       'module anchor'},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 200},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Inspect code imports',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 6.0}},
 {'name': 'snipara_code_neighbors',
  'description': 'USE WHEN: getting oriented in unfamiliar code before editing; returns nearby '
                 'callers, callees, imports, and references within N hops. Hosted '
                 'fallback/canonical indexed graph: if you have shell access and local commits or '
                 'a dirty working tree may matter, run `snipara-companion code neighbors` first '
                 'because it auto-selects the local overlay; use this MCP tool when companion is '
                 'unavailable or after push/reindex.',
  'inputSchema': {'type': 'object',
                  'properties': {'qualified_name': {'type': 'string',
                                                    'description': 'Repo-qualified symbol name'},
                                 'symbol_key': {'type': 'string',
                                                'description': 'Stable symbol key for an exact '
                                                               'match'},
                                 'depth': {'type': 'integer',
                                           'default': 2,
                                           'minimum': 1,
                                           'maximum': 4},
                                 'edge_kinds': {'type': 'array',
                                                'items': {'type': 'string',
                                                          'enum': ['CALLS',
                                                                   'CONTAINS',
                                                                   'IMPORTS',
                                                                   'REFERENCES']},
                                                'description': 'Optional edge kinds to include'},
                                 'limit': {'type': 'integer',
                                           'default': 200,
                                           'minimum': 1,
                                           'maximum': 500},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Inspect nearby code graph',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 6.0}},
 {'name': 'snipara_code_shortest_path',
  'description': 'USE WHEN: how is A connected to B, such as whether a route reaches a service or '
                 'a handler touches a model. Returns the shortest call/import/reference path from '
                 'the indexed hosted code graph. If you have shell access and local commits or a '
                 'dirty working tree may matter, run `snipara-companion code shortest-path` first; '
                 'use this MCP tool when companion is unavailable or after push/reindex.',
  'inputSchema': {'type': 'object',
                  'properties': {'from': {'type': 'string',
                                          'description': 'Source repo-qualified symbol name'},
                                 'from_symbol_key': {'type': 'string',
                                                     'description': 'Exact source symbol key'},
                                 'to': {'type': 'string',
                                        'description': 'Target repo-qualified symbol name'},
                                 'to_symbol_key': {'type': 'string',
                                                   'description': 'Exact target symbol key'},
                                 'edge_kinds': {'type': 'array',
                                                'items': {'type': 'string',
                                                          'enum': ['CALLS',
                                                                   'CONTAINS',
                                                                   'IMPORTS',
                                                                   'REFERENCES']},
                                                'description': 'Optional edge kinds to traverse'},
                                 'max_hops': {'type': 'integer',
                                              'default': 6,
                                              'minimum': 1,
                                              'maximum': 12},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Find code graph path',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False}},
 {'name': 'snipara_code_symbol_card',
  'description': 'USE WHEN: about to edit an important symbol, especially route, service, job, '
                 'auth, billing, or schema-adjacent code. Returns role, layer, framework, risk, '
                 'freshness, and related tests/docs/routes/config hints from the indexed hosted '
                 'graph.',
  'inputSchema': {'type': 'object',
                  'properties': {'qualified_name': {'type': 'string',
                                                    'description': 'Repo-qualified symbol name'},
                                 'symbol_key': {'type': 'string',
                                                'description': 'Stable symbol key for an exact '
                                                               'match'},
                                 'limit': {'type': 'integer',
                                           'default': 20,
                                           'minimum': 1,
                                           'maximum': 100},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Load agent code symbol card',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False}},
 {'name': 'snipara_code_impact',
  'description': 'USE WHEN: what breaks if this changes; run before risky edits, PR reviews, '
                 'routes/services/jobs work, or explicit gap analysis. Primary code surface for '
                 'local work is `snipara-companion code impact`: if you have shell access and '
                 'local commits or a dirty working tree may matter, run that first because it '
                 'auto-selects local_overlay. Use this hosted MCP tool as the fallback when '
                 'companion is unavailable, or after push/reindex for the canonical hosted graph. '
                 'Pass changed_files for a committed diff or PR file list.',
  'inputSchema': {'type': 'object',
                  'properties': {'qualified_name': {'type': 'string',
                                                    'description': 'Repo-qualified symbol name'},
                                 'symbol_key': {'type': 'string',
                                                'description': 'Stable symbol key for an exact '
                                                               'match'},
                                 'file_path': {'type': 'string',
                                               'description': 'Analyze impact for all indexed '
                                                              'symbols in this file'},
                                 'changed_files': {'type': 'array',
                                                   'items': {'type': 'string'},
                                                   'description': 'Analyze impact across multiple '
                                                                  'changed files, such as a PR '
                                                                  'diff file list'},
                                 'diff_summary': {'type': 'string',
                                                  'description': 'Optional natural-language '
                                                                 'summary of the change or PR'},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 200},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 500,
                                                'maximum': 20000,
                                                'description': 'Hard response token budget for '
                                                               'returned JSON. The response '
                                                               'includes budget.omittedSections '
                                                               'when compacted.'}},
                  'required': []},
  'annotations': {'title': 'Analyze code change impact',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 8.0}},
 {'name': 'snipara_local_code_overlay_upload',
  'description': 'Upload a non-canonical local code overlay manifest produced by '
                 'snipara-companion. This stores local working tree or local commit metadata '
                 'separately from the canonical hosted code graph.',
  'inputSchema': {'type': 'object',
                  'properties': {'overlay': {'type': 'object',
                                             'description': 'The snipara.local_code_overlay.v1 '
                                                            'manifest to store.'},
                                 'source_client': {'type': 'string',
                                                   'default': 'snipara-companion',
                                                   'description': 'Client that generated the '
                                                                  'overlay.'},
                                 'session_id': {'type': 'string',
                                                'description': 'Optional local agent/session '
                                                               'identifier for correlation.'},
                                 'ttl_hours': {'type': 'integer',
                                               'default': 48,
                                               'minimum': 1,
                                               'maximum': 168,
                                               'description': 'How long the uploaded overlay '
                                                              'should remain active.'},
                                 'retire_previous': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Retire older active overlays '
                                                                    'for the same repository and '
                                                                    'branch.'}},
                  'required': ['overlay']},
  'annotations': {'title': 'Upload local code overlay',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': False,
                  'openWorldHint': False}},
 {'name': 'snipara_local_code_overlay_status',
  'description': 'List active hosted local code overlays for this project. Results are '
                 'non-canonical and do not change what snipara_code_* tools query.',
  'inputSchema': {'type': 'object',
                  'properties': {'repository_id': {'type': 'string'},
                                 'branch': {'type': 'string'},
                                 'local_head_sha': {'type': 'string'},
                                 'dirty_tree_hash': {'type': 'string'},
                                 'limit': {'type': 'integer',
                                           'default': 5,
                                           'minimum': 1,
                                           'maximum': 50}},
                  'required': []},
  'annotations': {'title': 'List local code overlays',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False}},
 {'name': 'snipara_local_code_overlay_get',
  'description': 'Fetch one hosted local code overlay by id or latest matching filters. Use '
                 'include_graph=true only when the full local overlay payload is needed.',
  'inputSchema': {'type': 'object',
                  'properties': {'overlay_id': {'type': 'string'},
                                 'repository_id': {'type': 'string'},
                                 'branch': {'type': 'string'},
                                 'local_head_sha': {'type': 'string'},
                                 'dirty_tree_hash': {'type': 'string'},
                                 'include_graph': {'type': 'boolean', 'default': False}},
                  'required': []},
  'annotations': {'title': 'Fetch local code overlay',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False}},
 {'name': 'snipara_local_code_overlay_retire',
  'description': 'Retire a hosted local code overlay without deleting historical records. Use this '
                 'when local overlay metadata is superseded before TTL expiry.',
  'inputSchema': {'type': 'object',
                  'properties': {'overlay_id': {'type': 'string'},
                                 'repository_id': {'type': 'string'},
                                 'branch': {'type': 'string'},
                                 'local_head_sha': {'type': 'string'},
                                 'dirty_tree_hash': {'type': 'string'},
                                 'all_matching': {'type': 'boolean',
                                                  'default': False,
                                                  'description': 'Retire every active overlay '
                                                                 'matching the filters instead of '
                                                                 'the latest one.'}},
                  'required': []},
  'annotations': {'title': 'Retire local code overlay',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': False,
                  'openWorldHint': False}},
 {'name': 'snipara_decompose',
  'description': 'Break complex query into sub-queries with execution order.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string', 'maxLength': 20480},
                                 'max_depth': {'type': 'integer',
                                               'default': 2,
                                               'minimum': 1,
                                               'maximum': 5},
                                 'hints': {'type': 'array',
                                           'items': {'type': 'string', 'maxLength': 512},
                                           'maxItems': 10}},
                  'required': ['query']}},
 {'name': 'snipara_multi_query',
  'description': 'Execute multiple queries in one call with shared token budget.',
  'inputSchema': {'type': 'object',
                  'properties': {'queries': {'type': 'array',
                                             'items': {'type': 'object',
                                                       'properties': {'query': {'type': 'string',
                                                                                'maxLength': 20480},
                                                                      'max_tokens': {'type': 'integer',
                                                                                     'minimum': 50,
                                                                                     'maximum': 20000}},
                                                       'required': ['query']},
                                             'minItems': 1,
                                             'maxItems': 10},
                                 'max_tokens': {'type': 'integer',
                                                'default': 8000,
                                                'minimum': 500,
                                                'maximum': 50000}},
                  'required': ['queries']}},
 {'name': 'snipara_plan',
  'description': 'Generate full execution plan for complex questions. Returns steps for '
                 'decomposition, context queries, and synthesis.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'The complex question to plan for'},
                                 'strategy': {'type': 'string',
                                              'enum': ['breadth_first',
                                                       'depth_first',
                                                       'relevance_first'],
                                              'default': 'relevance_first',
                                              'description': 'Execution strategy'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 16000,
                                                'minimum': 1000,
                                                'maximum': 100000}},
                  'required': ['query']}},
 {'name': 'snipara_multi_project_query',
  'description': 'Query across projects in a team. Requires a service account key.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string', 'description': 'Question or topic'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 100,
                                                'maximum': 100000},
                                 'per_project_limit': {'type': 'integer',
                                                       'default': 3,
                                                       'minimum': 1,
                                                       'maximum': 20},
                                 'project_ids': {'type': 'array',
                                                 'items': {'type': 'string'},
                                                 'description': 'Optional project IDs/slugs to '
                                                                'include'},
                                 'exclude_project_ids': {'type': 'array',
                                                         'items': {'type': 'string'},
                                                         'description': 'Optional project '
                                                                        'IDs/slugs to exclude'},
                                 'search_mode': {'type': 'string',
                                                 'enum': ['keyword', 'semantic', 'hybrid'],
                                                 'default': 'keyword'},
                                 'include_metadata': {'type': 'boolean', 'default': True},
                                 'prefer_summaries': {'type': 'boolean', 'default': False}},
                  'required': ['query']}},
 {'name': 'snipara_inject',
  'description': 'Set session context for subsequent queries.',
  'inputSchema': {'type': 'object',
                  'properties': {'context': {'type': 'string'},
                                 'append': {'type': 'boolean', 'default': False}},
                  'required': ['context']}},
 {'name': 'snipara_context',
  'description': 'Show current session context.',
  'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
 {'name': 'snipara_clear_context',
  'description': 'Clear session context.',
  'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
 {'name': 'snipara_stats',
  'description': 'Show compact documentation statistics. File lists and DB-backed index health are '
                 'opt-in so interactive stats calls stay small and fast.',
  'inputSchema': {'type': 'object',
                  'properties': {'include_files': {'type': 'boolean',
                                                   'default': False,
                                                   'description': 'Include a capped sample of '
                                                                  'indexed file paths.'},
                                 'max_files': {'type': 'integer',
                                               'default': 25,
                                               'minimum': 0,
                                               'maximum': 200,
                                               'description': 'Maximum file paths to include when '
                                                              'include_files=true.'},
                                 'include_index_health': {'type': 'boolean',
                                                          'default': False,
                                                          'description': 'Include a compact '
                                                                         'DB-backed index-health '
                                                                         'snapshot. For full '
                                                                         'health, call '
                                                                         'snipara_index_health.'}},
                  'required': []}},
 {'name': 'snipara_sections',
  'description': 'List indexed document sections with optional pagination and filtering.',
  'inputSchema': {'type': 'object',
                  'properties': {'limit': {'type': 'integer',
                                           'description': 'Maximum sections to return (default: '
                                                          '50, max: 500)'},
                                 'offset': {'type': 'integer',
                                            'description': 'Number of sections to skip for '
                                                           'pagination (default: 0)'},
                                 'filter': {'type': 'string',
                                            'description': 'Filter sections by title prefix '
                                                           '(case-insensitive)'}},
                  'required': []}},
 {'name': 'snipara_settings',
  'description': 'Get current project settings from dashboard (max_tokens, search_mode, etc.).',
  'inputSchema': {'type': 'object',
                  'properties': {'refresh': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Force refresh from API'}},
                  'required': []}},
 {'name': 'snipara_help',
  'description': 'Get intelligent tool recommendations based on what you want to do. Helps '
                 'discover the right tool for your task.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'Describe what you want to do (e.g., '
                                                          "'search across all team projects', "
                                                          "'remember a decision')"},
                                 'tool': {'type': 'string',
                                          'description': 'Get detailed info about a specific tool '
                                                         "(e.g., 'snipara_context_query')"},
                                 'tier': {'type': 'string',
                                          'enum': ['primary',
                                                   'power_user',
                                                   'team',
                                                   'utility',
                                                   'advanced'],
                                          'description': 'List all tools in a specific tier'},
                                 'list_all': {'type': 'boolean',
                                              'default': False,
                                              'description': 'Return a deterministic catalog of '
                                                             'all tools available to this caller'},
                                 'limit': {'type': 'integer',
                                           'default': 5,
                                           'minimum': 1,
                                           'maximum': 20,
                                           'description': 'Maximum recommendations to return'}},
                  'required': []},
  '_meta': {'snipara_tool_weight': 3.0}},
 {'name': 'snipara_store_summary',
  'description': 'Store an LLM-generated summary for a document.',
  'inputSchema': {'type': 'object',
                  'properties': {'document_path': {'type': 'string'},
                                 'summary': {'type': 'string'},
                                 'summary_type': {'type': 'string',
                                                  'enum': ['concise',
                                                           'detailed',
                                                           'technical',
                                                           'keywords',
                                                           'custom'],
                                                  'default': 'concise'},
                                 'generated_by': {'type': 'string'}},
                  'required': ['document_path', 'summary']}},
 {'name': 'snipara_get_summaries',
  'description': 'Retrieve stored summaries.',
  'inputSchema': {'type': 'object',
                  'properties': {'document_path': {'type': 'string'},
                                 'summary_type': {'type': 'string',
                                                  'enum': ['concise',
                                                           'detailed',
                                                           'technical',
                                                           'keywords',
                                                           'custom']},
                                 'include_content': {'type': 'boolean', 'default': True}},
                  'required': []}},
 {'name': 'snipara_delete_summary',
  'description': 'Delete stored summaries.',
  'inputSchema': {'type': 'object',
                  'properties': {'summary_id': {'type': 'string'},
                                 'document_path': {'type': 'string'}},
                  'required': []}},
 {'name': 'snipara_shared_context',
  'description': 'Load project-linked shared standards, business playbooks, and reusable guidance. '
                 'Use for linked source documents, not durable memory.',
  'inputSchema': {'type': 'object',
                  'properties': {'max_tokens': {'type': 'integer',
                                                'default': 4000,
                                                'minimum': 100,
                                                'maximum': 100000},
                                 'categories': {'type': 'array',
                                                'items': {'type': 'string',
                                                          'enum': ['MANDATORY',
                                                                   'BEST_PRACTICES',
                                                                   'GUIDELINES',
                                                                   'REFERENCE']},
                                                'description': 'Filter by categories (default: '
                                                               'all)'},
                                 'include_content': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Include merged content'}},
                  'required': []}},
 {'name': 'snipara_list_templates',
  'description': 'List available prompt templates from shared collections.',
  'inputSchema': {'type': 'object',
                  'properties': {'category': {'type': 'string',
                                              'description': 'Filter by category'}},
                  'required': []}},
 {'name': 'snipara_get_template',
  'description': 'Get a specific prompt template by ID or slug. Optionally render with variables.',
  'inputSchema': {'type': 'object',
                  'properties': {'template_id': {'type': 'string', 'description': 'Template ID'},
                                 'slug': {'type': 'string', 'description': 'Template slug'},
                                 'variables': {'type': 'object',
                                               'additionalProperties': {'type': 'string'},
                                               'description': 'Variables to substitute in '
                                                              'template'}},
                  'required': []}},
 {'name': 'snipara_list_collections',
  'description': 'List all shared context collections accessible to you. Returns collections you '
                 "own, team collections you're a member of, and public collections. Use this to "
                 'find collection IDs for uploading documents.',
  'inputSchema': {'type': 'object',
                  'properties': {'include_public': {'type': 'boolean',
                                                    'default': True,
                                                    'description': 'Include public collections in '
                                                                   'the results'}},
                  'required': []}},
 {'name': 'snipara_create_collection',
  'description': "Create a new TEAM shared context collection in the current project's team. Use "
                 'this to separate project-specific best practices from broader team context.',
  'inputSchema': {'type': 'object',
                  'properties': {'name': {'type': 'string',
                                          'description': 'Collection display name'},
                                 'slug': {'type': 'string',
                                          'description': 'Optional collection slug. Defaults to a '
                                                         'slugified version of name.'},
                                 'description': {'type': 'string',
                                                 'description': 'Optional collection description'},
                                 'is_public': {'type': 'boolean',
                                               'default': False,
                                               'description': 'Whether the collection should be '
                                                              'public'}},
                  'required': ['name']}},
 {'name': 'snipara_get_collection_documents',
  'description': 'Inspect the documents stored in a shared context collection, including optional '
                 'full content. Use this before copying or splitting mixed collections.',
  'inputSchema': {'type': 'object',
                  'properties': {'collection_id': {'type': 'string',
                                                   'description': 'The shared collection ID'},
                                 'include_content': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Include the full document '
                                                                    'content in the response'}},
                  'required': ['collection_id']}},
 {'name': 'snipara_link_collection',
  'description': 'Link an existing shared collection to a project you can access. Defaults to the '
                 'current project when project_id_or_slug is omitted.',
  'inputSchema': {'type': 'object',
                  'properties': {'collection_id': {'type': 'string',
                                                   'description': 'The shared collection ID'},
                                 'project_id_or_slug': {'type': 'string',
                                                        'description': 'Optional target project '
                                                                       'ID, slug, or github repo. '
                                                                       'Defaults to the current '
                                                                       'project.'},
                                 'priority': {'type': 'integer',
                                              'minimum': 0,
                                              'description': 'Optional link priority (lower = '
                                                             'higher priority)'},
                                 'token_budget_percent': {'type': 'integer',
                                                          'minimum': 0,
                                                          'maximum': 100,
                                                          'description': 'Optional token budget '
                                                                         'override for this '
                                                                         'collection'},
                                 'enabled_categories': {'type': 'array',
                                                        'items': {'type': 'string',
                                                                  'enum': ['MANDATORY',
                                                                           'BEST_PRACTICES',
                                                                           'GUIDELINES',
                                                                           'REFERENCE']},
                                                        'description': 'Optional category '
                                                                       'allowlist for this project '
                                                                       'link'}},
                  'required': ['collection_id']}},
 {'name': 'snipara_unlink_collection',
  'description': 'Unlink a shared collection from a project you can access. Defaults to the '
                 'current project when project_id_or_slug is omitted.',
  'inputSchema': {'type': 'object',
                  'properties': {'collection_id': {'type': 'string',
                                                   'description': 'The shared collection ID'},
                                 'project_id_or_slug': {'type': 'string',
                                                        'description': 'Optional target project '
                                                                       'ID, slug, or github repo. '
                                                                       'Defaults to the current '
                                                                       'project.'}},
                  'required': ['collection_id']}},
 {'name': 'snipara_upload_shared_document',
  'description': 'Upload or update a document in a shared context collection. Use for team best '
                 'practices, coding standards, business playbooks, reusable examples, and '
                 'guidelines. Requires Team plan or higher.',
  'inputSchema': {'type': 'object',
                  'properties': {'collection_id': {'type': 'string',
                                                   'description': 'The shared collection ID'},
                                 'title': {'type': 'string', 'description': 'Document title'},
                                 'content': {'type': 'string',
                                             'description': 'Document content (markdown)'},
                                 'category': {'type': 'string',
                                              'enum': ['MANDATORY',
                                                       'BEST_PRACTICES',
                                                       'GUIDELINES',
                                                       'REFERENCE'],
                                              'default': 'BEST_PRACTICES',
                                              'description': 'Document category for token budget '
                                                             'allocation'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Tags for filtering and organization'},
                                 'priority': {'type': 'integer',
                                              'default': 0,
                                              'minimum': 0,
                                              'maximum': 100,
                                              'description': 'Priority within category (higher = '
                                                             'more important)'}},
                  'required': ['collection_id', 'title', 'content']}},
 {'name': 'snipara_list_business_collections',
  'description': 'List Team Business Context collections for the current team, including Business '
                 'Response Playbook, Business Library, Offer Templates, Company Presentations, and '
                 'Reference Diagrams. Use this before uploading reusable business knowledge.',
  'inputSchema': {'type': 'object',
                  'properties': {'include_custom': {'type': 'boolean',
                                                    'default': False,
                                                    'description': 'Also include custom '
                                                                   'collections that look '
                                                                   'business-oriented. Preset '
                                                                   'business collections are '
                                                                   'always included.'},
                                 'include_missing_presets': {'type': 'boolean',
                                                             'default': True,
                                                             'description': 'Return missing preset '
                                                                            'definitions so the '
                                                                            'caller can create '
                                                                            'them with '
                                                                            'snipara_ensure_business_collection.'}},
                  'required': []}},
 {'name': 'snipara_ensure_business_collection',
  'description': 'Create or return an existing Team Business Context collection. Prefer preset '
                 'slugs for the standard workspace business library.',
  'inputSchema': {'type': 'object',
                  'properties': {'preset': {'type': 'string',
                                            'enum': ['business_response_playbook',
                                                     'business_library',
                                                     'offer_templates',
                                                     'company_presentations',
                                                     'reference_diagrams'],
                                            'description': 'Standard Team Business Context preset '
                                                           'to create or return.'},
                                 'name': {'type': 'string',
                                          'description': 'Custom collection display name. Required '
                                                         'when preset is omitted.'},
                                 'slug': {'type': 'string',
                                          'description': 'Custom collection slug. Defaults to a '
                                                         'slugified name.'},
                                 'description': {'type': 'string',
                                                 'description': 'Optional collection description'}},
                  'required': []}},
 {'name': 'snipara_upload_business_document',
  'description': 'Upload or update a reusable document in a Team Business Context collection. For '
                 'current client/project files with metadata, use snipara_upload_document instead.',
  'inputSchema': {'type': 'object',
                  'properties': {'collection_id': {'type': 'string',
                                                   'description': 'Business collection ID. If '
                                                                  'omitted, provide preset or '
                                                                  'collection_slug.'},
                                 'preset': {'type': 'string',
                                            'enum': ['business_response_playbook',
                                                     'business_library',
                                                     'offer_templates',
                                                     'company_presentations',
                                                     'reference_diagrams'],
                                            'description': 'Business preset to resolve or create '
                                                           'before upload.'},
                                 'collection_slug': {'type': 'string',
                                                     'description': 'Business collection slug to '
                                                                    'resolve when collection_id is '
                                                                    'omitted.'},
                                 'title': {'type': 'string', 'description': 'Document title'},
                                 'content': {'type': 'string',
                                             'description': 'Document content (usually markdown)'},
                                 'category': {'type': 'string',
                                              'enum': ['MANDATORY',
                                                       'BEST_PRACTICES',
                                                       'GUIDELINES',
                                                       'REFERENCE'],
                                              'default': 'REFERENCE',
                                              'description': 'Shared-context category used for '
                                                             'token budget allocation.'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Tags such as offer, template, diagram, '
                                                         'client-example, or methodology.'},
                                 'priority': {'type': 'integer',
                                              'default': 0,
                                              'minimum': 0,
                                              'maximum': 100,
                                              'description': 'Priority within category (higher = '
                                                             'more important).'},
                                 'allow_custom_collection': {'type': 'boolean',
                                                             'default': False,
                                                             'description': 'Allow upload to a '
                                                                            'custom '
                                                                            'business-looking '
                                                                            'collection instead of '
                                                                            'a standard preset.'}},
                  'required': ['title', 'content']}},
 {'name': 'snipara_list_client_projects',
  'description': 'List client/project business-context workspaces in the current team. These are '
                 'project-scoped containers for current client documents, deliverables, diagrams, '
                 'and history.',
  'inputSchema': {'type': 'object',
                  'properties': {'include_internal': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Also return internal, '
                                                                     'research, and code projects '
                                                                     'with their scope '
                                                                     'classification.'},
                                 'limit': {'type': 'integer',
                                           'default': 100,
                                           'minimum': 1,
                                           'maximum': 500}},
                  'required': []}},
 {'name': 'snipara_create_client_project',
  'description': 'Create a client/project business-context workspace in the current team. Use this '
                 'before uploading current client documents with snipara_upload_document.',
  'inputSchema': {'type': 'object',
                  'properties': {'name': {'type': 'string',
                                          'description': 'Client/project display name'},
                                 'slug': {'type': 'string',
                                          'description': 'Optional stable project slug. Defaults '
                                                         'to a slugified name.'},
                                 'description': {'type': 'string',
                                                 'description': 'Optional description. Snipara '
                                                                'prefixes it as Client business '
                                                                'context when needed.'},
                                 'project_mode': {'type': 'string',
                                                  'enum': ['active_client', 'reference_archive'],
                                                  'description': 'Optional client project mode. '
                                                                 'active_client keeps business '
                                                                 'health enabled; '
                                                                 'reference_archive is for '
                                                                 'past-client precedent.'},
                                 'external_client_id': {'type': 'string',
                                                        'description': 'Optional external client '
                                                                       'identifier echoed back for '
                                                                       'integrator workflows.'}},
                  'required': ['name']}},
 {'name': 'snipara_remember',
  'description': 'Store a durable Memory V2 record for later semantic recall. Direct writes '
                 'support fact, decision, learning, preference, todo, and context. Use the '
                 'narrowest owner scope: agent for one agent role, project for one '
                 'client/project/RFP, team for reviewed shared standards, and user for one '
                 "person's preferences. Do not store source truth here; use snipara_context_query, "
                 'snipara_load_document, or snipara_shared_context for specs, RFPs, diagrams, and '
                 'raw docs. Use snipara_end_of_task_commit for workflow capture.',
  'inputSchema': {'type': 'object',
                  'properties': {'text': {'type': 'string',
                                          'maxLength': 65536,
                                          'description': 'The memory text to store'},
                                 'content': {'type': 'string',
                                             'maxLength': 65536,
                                             'description': "DEPRECATED: Use 'text' instead. The "
                                                            'memory content to store.'},
                                 'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context'],
                                          'default': 'fact'},
                                 'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'default': 'project',
                                           'description': 'Memory owner boundary. scope=agent '
                                                          'requires agent_id; scope=user is '
                                                          'personal to the authenticated user or '
                                                          'integrator external_user_id; scope=team '
                                                          'requires the current project to belong '
                                                          'to a team.'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required when scope=agent; '
                                                             'identifies the agent-owned memory '
                                                             'namespace'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'scope=user memory. Snipara '
                                                                     'hashes and namespaces it per '
                                                                     'integrator client.'},
                                 'category': {'type': 'string',
                                              'maxLength': 200,
                                              'description': 'Optional category for grouping'},
                                 'ttl_days': {'type': 'integer',
                                              'description': 'Days until expiration (null = '
                                                             'permanent)'},
                                 'related_to': {'type': 'array',
                                                'items': {'type': 'string', 'maxLength': 256},
                                                'maxItems': 50,
                                                'description': 'IDs of related memories'},
                                 'document_refs': {'type': 'array',
                                                   'items': {'type': 'string', 'maxLength': 512},
                                                   'maxItems': 100,
                                                   'description': 'Referenced document paths'},
                                 'source': {'type': 'string',
                                            'maxLength': 200,
                                            'description': 'Optional source label for the memory '
                                                           'write'},
                                 'memory_reconciliation_mode': {'type': 'string',
                                                                'enum': ['off',
                                                                         'recommend',
                                                                         'auto_safe'],
                                                                'default': 'recommend',
                                                                'description': 'After storing, '
                                                                               'find older similar '
                                                                               'memories. '
                                                                               'recommend returns '
                                                                               'supersede '
                                                                               'candidates only; '
                                                                               'auto_safe '
                                                                               'supersedes only '
                                                                               'high-confidence '
                                                                               'same-scope/type/category '
                                                                               'matches. No '
                                                                               'physical '
                                                                               'deletion.'}},
                  'required': []},
  'annotations': {'title': 'Store reviewed memory',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': False,
                  'openWorldHint': False}},
 {'name': 'snipara_remember_if_novel',
  'description': 'Store a durable Memory V2 record only if it is sufficiently novel compared with '
                 'existing memories. Direct writes support fact, decision, learning, preference, '
                 'todo, and context. Use context tools for source truth and '
                 'snipara_end_of_task_commit for workflow capture. Returns duplicate matches when '
                 'skipped.',
  'inputSchema': {'type': 'object',
                  'properties': {'text': {'type': 'string',
                                          'maxLength': 65536,
                                          'description': 'The memory text to store'},
                                 'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context'],
                                          'default': 'fact'},
                                 'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'default': 'project',
                                           'description': 'Memory owner boundary. scope=agent '
                                                          'requires agent_id; scope=user is '
                                                          'personal to the authenticated user or '
                                                          'integrator external_user_id.'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required when scope=agent; '
                                                             'identifies the agent-owned memory '
                                                             'namespace'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'scope=user memory. Snipara '
                                                                     'hashes and namespaces it per '
                                                                     'integrator client.'},
                                 'category': {'type': 'string', 'maxLength': 200},
                                 'ttl_days': {'type': 'integer'},
                                 'related_to': {'type': 'array',
                                                'items': {'type': 'string', 'maxLength': 256},
                                                'maxItems': 50},
                                 'document_refs': {'type': 'array',
                                                   'items': {'type': 'string', 'maxLength': 512},
                                                   'maxItems': 100},
                                 'source': {'type': 'string',
                                            'maxLength': 200,
                                            'description': 'Optional source label for the memory '
                                                           'write'},
                                 'novelty_threshold': {'type': 'number',
                                                       'minimum': 0,
                                                       'maximum': 1,
                                                       'description': 'Similarity threshold above '
                                                                      'which a memory is treated '
                                                                      'as duplicate'},
                                 'dedupe_limit': {'type': 'integer',
                                                  'default': 5,
                                                  'minimum': 1,
                                                  'maximum': 20},
                                 'allow_supersede': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Reserved for future conflict '
                                                                    'handling'},
                                 'memory_reconciliation_mode': {'type': 'string',
                                                                'enum': ['off',
                                                                         'recommend',
                                                                         'auto_safe'],
                                                                'default': 'recommend',
                                                                'description': 'After storing, '
                                                                               'find older similar '
                                                                               'memories. '
                                                                               'recommend returns '
                                                                               'supersede '
                                                                               'candidates only; '
                                                                               'auto_safe '
                                                                               'supersedes only '
                                                                               'high-confidence '
                                                                               'same-scope/type/category '
                                                                               'matches. No '
                                                                               'physical '
                                                                               'deletion.'}},
                  'required': ['text']}},
 {'name': 'snipara_end_of_task_commit',
  'description': 'Persist durable outcomes from a task summary into memory. Extracts decisions, '
                 'learnings, preferences, todos, and durable workflow context while filtering '
                 'operational receipts; not for source documents or specs.',
  'inputSchema': {'type': 'object',
                  'properties': {'summary': {'type': 'string', 'description': 'Task summary'},
                                 'outcome': {'type': 'string',
                                             'enum': ['completed',
                                                      'partial',
                                                      'blocked',
                                                      'abandoned'],
                                             'default': 'completed'},
                                 'files_touched': {'type': 'array', 'items': {'type': 'string'}},
                                 'artifacts': {'type': 'array', 'items': {'type': 'string'}},
                                 'persist_types': {'type': 'array',
                                                   'items': {'type': 'string',
                                                             'enum': ['decision',
                                                                      'learning',
                                                                      'preference',
                                                                      'todo',
                                                                      'context',
                                                                      'workflow']}},
                                 'category': {'type': 'string'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'user-owned memories created '
                                                                     'from task commits.'},
                                 'handoff_only': {'type': 'boolean',
                                                  'default': False,
                                                  'description': 'For final workflow commits, '
                                                                 'create the Team Sync handoff and '
                                                                 'skip durable-memory extraction.'},
                                 'memory_reconciliation_mode': {'type': 'string',
                                                                'enum': ['off',
                                                                         'recommend',
                                                                         'auto_safe'],
                                                                'default': 'recommend',
                                                                'description': 'For newly created '
                                                                               'task memories, '
                                                                               'find older similar '
                                                                               'memories. '
                                                                               'recommend returns '
                                                                               'candidates only; '
                                                                               'auto_safe '
                                                                               'supersedes only '
                                                                               'high-confidence '
                                                                               'same-scope/type/category '
                                                                               'matches.'},
                                 'dry_run': {'type': 'boolean', 'default': False}},
                  'required': ['summary']},
  'annotations': {'title': 'Commit durable task memory',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': False,
                  'openWorldHint': False}},
 {'name': 'snipara_remember_bulk',
  'description': 'Store multiple durable Memory V2 records in a single call. Batch embedding for '
                 'efficiency. Max 50 memories per call. Do not bulk-store source documents; upload '
                 'or query source truth through context tools instead.',
  'inputSchema': {'type': 'object',
                  'properties': {'memories': {'type': 'array',
                                              'items': {'type': 'object',
                                                        'properties': {'text': {'type': 'string',
                                                                                'maxLength': 65536,
                                                                                'description': 'Memory '
                                                                                               'text '
                                                                                               'to '
                                                                                               'store'},
                                                                       'type': {'type': 'string',
                                                                                'enum': ['fact',
                                                                                         'decision',
                                                                                         'learning',
                                                                                         'preference',
                                                                                         'todo',
                                                                                         'context'],
                                                                                'default': 'fact'},
                                                                       'scope': {'type': 'string',
                                                                                 'enum': ['agent',
                                                                                          'project',
                                                                                          'team',
                                                                                          'user'],
                                                                                 'default': 'project'},
                                                                       'agent_id': {'type': 'string',
                                                                                    'description': 'Required '
                                                                                                   'when '
                                                                                                   'scope=agent'},
                                                                       'category': {'type': 'string',
                                                                                    'maxLength': 200},
                                                                       'ttl_days': {'type': 'integer'},
                                                                       'related_to': {'type': 'array',
                                                                                      'items': {'type': 'string',
                                                                                                'maxLength': 256},
                                                                                      'maxItems': 50},
                                                                       'document_refs': {'type': 'array',
                                                                                         'items': {'type': 'string',
                                                                                                   'maxLength': 512},
                                                                                         'maxItems': 100}},
                                                        'required': ['text']},
                                              'minItems': 1,
                                              'maxItems': 50,
                                              'description': 'Array of memories to store (max 50)'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'user-scoped bulk memories. '
                                                                     'Applies to all memories in '
                                                                     'the call.'}},
                  'required': ['memories']}},
 {'name': 'snipara_recall',
  'description': 'Semantically recall durable Memory V2 records such as decisions, learnings, '
                 'preferences, and session carryover. Not for source document retrieval; use '
                 'snipara_context_query, snipara_load_document, or snipara_shared_context for '
                 'specs, RFPs, diagrams, and raw docs.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'Memory question such as a past '
                                                          'decision, preference, or validated '
                                                          'learning'},
                                 'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context']},
                                 'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user']},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required when scope=agent; limits '
                                                             'recall to one agent namespace'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'scope=user recall. Snipara '
                                                                     'hashes and namespaces it per '
                                                                     'integrator client.'},
                                 'category': {'type': 'string',
                                              'description': 'Filter by category'},
                                 'limit': {'type': 'integer',
                                           'default': 5,
                                           'description': 'Maximum memories to return'},
                                 'min_relevance': {'type': 'number',
                                                   'default': 0.5,
                                                   'description': 'Minimum relevance score (0-1)'},
                                 'include_inactive': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include inactive memories in '
                                                                     'the main result set'},
                                 'warning_threshold': {'type': 'number',
                                                       'default': 0.72,
                                                       'description': 'Minimum relevance score for '
                                                                      'inactive-memory warnings'},
                                 'task': {'type': 'string',
                                          'minLength': 1,
                                          'maxLength': 512,
                                          'description': 'Optional task label recorded for '
                                                         'retrieval/outcome correlation.'},
                                 'outcome_rerank_mode': {'type': 'string',
                                                         'enum': ['disabled', 'shadow', 'enabled'],
                                                         'description': 'Optional bounded '
                                                                        'memory-outcome rerank '
                                                                        'mode. Omission uses the '
                                                                        'server configuration; a '
                                                                        'request cannot escalate '
                                                                        'beyond it.'},
                                 'correlation_context': {'type': 'object',
                                                         'additionalProperties': False,
                                                         'description': 'Optional '
                                                                        'retrieval-correlation '
                                                                        'context. Reuse session_id '
                                                                        'across retrieval and '
                                                                        'outcome calls so '
                                                                        'telemetry can be joined '
                                                                        'inside the authenticated '
                                                                        'project. These '
                                                                        'identifiers never change '
                                                                        'authorization or project '
                                                                        'scope; do not include '
                                                                        'secrets, tenant IDs, or '
                                                                        'user data.',
                                                         'properties': {'version': {'type': 'string',
                                                                                    'enum': ['retrieval-correlation-v1'],
                                                                                    'default': 'retrieval-correlation-v1'},
                                                                        'session_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Preferred '
                                                                                                      'stable '
                                                                                                      'opaque '
                                                                                                      'session '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'for '
                                                                                                      'telemetry '
                                                                                                      'association.'},
                                                                        'workflow_session_id': {'type': 'string',
                                                                                                'minLength': 1,
                                                                                                'maxLength': 128,
                                                                                                'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                                'description': 'Opaque '
                                                                                                               'workflow '
                                                                                                               'ID '
                                                                                                               'used '
                                                                                                               'when '
                                                                                                               'session_id '
                                                                                                               'is '
                                                                                                               'absent.'},
                                                                        'correlation_id': {'type': 'string',
                                                                                           'minLength': 1,
                                                                                           'maxLength': 128,
                                                                                           'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                           'description': 'Opaque '
                                                                                                          'request-chain '
                                                                                                          'ID '
                                                                                                          'used '
                                                                                                          'when '
                                                                                                          'session '
                                                                                                          'fields '
                                                                                                          'are '
                                                                                                          'absent.'},
                                                                        'request_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Opaque '
                                                                                                      'per-call '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'only '
                                                                                                      'as '
                                                                                                      'a '
                                                                                                      'final '
                                                                                                      'telemetry '
                                                                                                      'fallback.'}}}},
                  'required': ['query']},
  'annotations': {'title': 'Recall reviewed memory',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 12.0}},
 {'name': 'snipara_resume_context',
  'description': 'Load a compact agent-ready continuity bundle for the current project. Returns '
                 'the latest Team Sync handoff match, What Changed summary, active decisions, '
                 'execution-memory snapshot, and an optional task-scoped work brief so an agent '
                 'can resume work without manually stitching these surfaces together.',
  'inputSchema': {'type': 'object',
                  'properties': {'sessionId': {'type': 'string',
                                               'description': 'Optional session identifier to '
                                                              'resolve handoff and checkpoint '
                                                              'context.'},
                                 'branch': {'type': 'string',
                                            'description': 'Optional branch name to scope What '
                                                           'Changed and handoff matching.'},
                                 'task': {'type': 'string',
                                          'description': 'Optional task summary. When supplied, '
                                                         'the response includes a task-scoped work '
                                                         'brief.'},
                                 'since': {'type': 'string',
                                           'description': 'Optional ISO timestamp for filtering '
                                                          'What Changed decision signals.'},
                                 'recentFiles': {'type': 'array',
                                                 'items': {'type': 'string'},
                                                 'description': 'Recent files relevant to the '
                                                                'task; improves handoff matching '
                                                                'and read recommendations.'},
                                 'changedFiles': {'type': 'array',
                                                  'items': {'type': 'string'},
                                                  'description': 'Changed files already known to '
                                                                 'the agent; used to scope '
                                                                 'work-brief candidates.'},
                                 'limit': {'type': 'integer',
                                           'default': 12,
                                           'minimum': 1,
                                           'maximum': 25,
                                           'description': 'Maximum PR Answer Pack records to '
                                                          'consider when composing continuity '
                                                          'context.'},
                                 'sessionLimit': {'type': 'integer',
                                                  'default': 3,
                                                  'minimum': 1,
                                                  'maximum': 10,
                                                  'description': 'Maximum execution-memory '
                                                                 'sessions to summarize.'},
                                 'eventLimit': {'type': 'integer',
                                                'default': 10,
                                                'minimum': 1,
                                                'maximum': 25,
                                                'description': 'Maximum execution-memory events '
                                                               'per session to summarize.'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 8000,
                                                'minimum': 1000,
                                                'maximum': 20000,
                                                'description': 'Hard token budget for the returned '
                                                               'continuity bundle.'}},
                  'required': []}},
 {'name': 'snipara_memories',
  'description': 'List memories with optional filters and sorting.',
  'inputSchema': {'type': 'object',
                  'properties': {'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context']},
                                 'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user']},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required when scope=agent; limits '
                                                             'listing to one agent namespace'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'scope=user memory listing. '
                                                                     'Snipara hashes and '
                                                                     'namespaces it per integrator '
                                                                     'client.'},
                                 'category': {'type': 'string'},
                                 'status': {'type': 'string',
                                            'enum': ['ACTIVE', 'INVALIDATED', 'SUPERSEDED'],
                                            'description': 'Filter by lifecycle status'},
                                 'search': {'type': 'string',
                                            'description': 'Text search in content'},
                                 'limit': {'type': 'integer', 'default': 20},
                                 'offset': {'type': 'integer', 'default': 0},
                                 'include_inactive': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include inactive memories in '
                                                                     'results'},
                                 'sort_by': {'type': 'string',
                                             'enum': ['created_at',
                                                      'confidence',
                                                      'access_count',
                                                      'last_accessed',
                                                      'expires_at'],
                                             'default': 'created_at',
                                             'description': 'Field to sort by'},
                                 'sort_order': {'type': 'string',
                                                'enum': ['asc', 'desc'],
                                                'default': 'desc',
                                                'description': 'Sort direction'}},
                  'required': []}},
 {'name': 'snipara_forget',
  'description': 'Delete memories by ID or filter criteria.',
  'inputSchema': {'type': 'object',
                  'properties': {'memory_id': {'type': 'string',
                                               'maxLength': 256,
                                               'description': 'Specific memory ID to delete'},
                                 'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context']},
                                 'category': {'type': 'string',
                                              'maxLength': 200,
                                              'description': 'Delete all in this category'},
                                 'older_than_days': {'type': 'integer',
                                                     'description': 'Delete memories older than N '
                                                                    'days'}},
                  'required': []}},
 {'name': 'snipara_memory_invalidate',
  'description': 'Invalidate a Memory V2 record without deleting it. Accepts a legacy memory ID if '
                 'a migration map exists.',
  'inputSchema': {'type': 'object',
                  'properties': {'memory_id': {'type': 'string',
                                               'maxLength': 256,
                                               'description': 'Legacy or V2 memory ID'},
                                 'invalidated_at': {'type': 'string',
                                                    'description': 'Optional ISO timestamp. '
                                                                   'Defaults to now.'},
                                 'reason': {'type': 'string',
                                            'maxLength': 2048,
                                            'description': 'Optional human-readable invalidation '
                                                           'reason'}},
                  'required': ['memory_id']}},
 {'name': 'snipara_memory_attach_source',
  'description': 'Attach structured evidence to a Memory V2 record. Accepts a legacy memory ID if '
                 'a migration map exists.',
  'inputSchema': {'type': 'object',
                  'properties': {'memory_id': {'type': 'string',
                                               'maxLength': 256,
                                               'description': 'Legacy or V2 memory ID'},
                                 'evidence_type': {'type': 'string',
                                                   'enum': ['DOCUMENT',
                                                            'CHUNK',
                                                            'SESSION',
                                                            'PR',
                                                            'ISSUE',
                                                            'COMMIT',
                                                            'WEBHOOK',
                                                            'EXTERNAL_URL'],
                                                   'description': 'Evidence type'},
                                 'document_id': {'type': 'string',
                                                 'maxLength': 256,
                                                 'description': 'Optional document ID'},
                                 'chunk_id': {'type': 'string',
                                              'maxLength': 256,
                                              'description': 'Optional chunk ID'},
                                 'external_ref': {'type': 'string',
                                                  'maxLength': 512,
                                                  'description': 'Optional path or URL'},
                                 'snippet': {'type': 'string',
                                             'maxLength': 4096,
                                             'description': 'Optional supporting excerpt'},
                                 'line_start': {'type': 'integer',
                                                'description': 'Optional start line'},
                                 'line_end': {'type': 'integer',
                                              'description': 'Optional end line'},
                                 'weight': {'type': 'number',
                                            'default': 1.0,
                                            'minimum': 0.0,
                                            'maximum': 1.0,
                                            'description': 'Evidence weight'}},
                  'required': ['memory_id', 'evidence_type']}},
 {'name': 'snipara_memory_supersede',
  'description': 'Mark one Memory V2 record as superseded by another. Accepts legacy memory IDs if '
                 'migration maps exist.',
  'inputSchema': {'type': 'object',
                  'properties': {'old_memory_id': {'type': 'string',
                                                   'maxLength': 256,
                                                   'description': 'Legacy or V2 memory ID being '
                                                                  'replaced'},
                                 'new_memory_id': {'type': 'string',
                                                   'maxLength': 256,
                                                   'description': 'Legacy or V2 replacement memory '
                                                                  'ID'},
                                 'reason': {'type': 'string',
                                            'maxLength': 2048,
                                            'description': 'Optional supersession reason'}},
                  'required': ['old_memory_id', 'new_memory_id']}},
 {'name': 'snipara_memory_verify',
  'description': 'Verify whether a Memory V2 record still has valid supporting evidence.',
  'inputSchema': {'type': 'object',
                  'properties': {'memory_id': {'type': 'string',
                                               'description': 'Legacy or V2 memory ID'},
                                 'mark_stale_if_missing': {'type': 'boolean',
                                                           'default': True,
                                                           'description': 'Mark memory stale when '
                                                                          'all evidence is '
                                                                          'invalid'}},
                  'required': ['memory_id']}},
 {'name': 'snipara_memory_review_queue',
  'description': 'Private review surface for candidate, stale, or rejected memories that need '
                 'human inspection before they become agent memory.',
  'inputSchema': {'type': 'object',
                  'properties': {'status': {'type': 'string',
                                            'enum': ['candidate',
                                                     'pending',
                                                     'stale',
                                                     'rejected',
                                                     'invalidated',
                                                     'superseded',
                                                     'archived',
                                                     'active',
                                                     'approved',
                                                     'all'],
                                            'default': 'candidate',
                                            'description': 'Queue lifecycle status to inspect.'},
                                 'type': {'type': 'string',
                                          'enum': ['fact',
                                                   'decision',
                                                   'learning',
                                                   'preference',
                                                   'todo',
                                                   'context'],
                                          'description': 'Optional memory type filter.'},
                                 'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'description': 'Optional owner scope filter.'},
                                 'category': {'type': 'string',
                                              'description': 'Optional category filter.'},
                                 'search': {'type': 'string',
                                            'description': 'Optional content search filter.'},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 100,
                                           'description': 'Maximum queue items to return.'},
                                 'offset': {'type': 'integer',
                                            'default': 0,
                                            'minimum': 0,
                                            'description': 'Pagination offset.'},
                                 'include_evidence': {'type': 'boolean',
                                                      'default': True,
                                                      'description': 'Include Memory V2 evidence '
                                                                     'links and legacy document '
                                                                     'refs.'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required when scope=agent; limits '
                                                             'queue reads to one agent namespace.'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID for '
                                                                     'scope=user queue reads.'}},
                  'required': []}},
 {'name': 'snipara_memory_resolve_queue_item',
  'description': 'Private review surface to accept, reject, archive, invalidate, merge, or '
                 'supersede one queued memory item.',
  'inputSchema': {'type': 'object',
                  'properties': {'memory_id': {'type': 'string',
                                               'description': 'Legacy or V2 memory ID to resolve.'},
                                 'action': {'type': 'string',
                                            'enum': ['accept',
                                                     'approve',
                                                     'reject',
                                                     'archive',
                                                     'invalidate',
                                                     'merge',
                                                     'supersede'],
                                            'description': 'Review resolution action.'},
                                 'target_memory_id': {'type': 'string',
                                                      'description': 'Required for merge and '
                                                                     'supersede actions.'},
                                 'notes': {'type': 'string',
                                           'description': 'Optional reviewer notes or rationale.'}},
                  'required': ['memory_id', 'action']}},
 {'name': 'snipara_journal_append',
  'description': "Append an entry to today's journal. Journals are daily logs of operational "
                 'notes, decisions, and context. Auto-loads today + yesterday on session start.',
  'inputSchema': {'type': 'object',
                  'properties': {'text': {'type': 'string',
                                          'description': 'Journal entry text (markdown supported)'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Optional tags for categorization'}},
                  'required': ['text']}},
 {'name': 'snipara_journal_get',
  'description': "Get journal entries for a specific date. Returns all entries from that day's "
                 'operational log.',
  'inputSchema': {'type': 'object',
                  'properties': {'date': {'type': 'string',
                                          'description': 'Date in YYYY-MM-DD format (default: '
                                                         'today)'},
                                 'include_yesterday': {'type': 'boolean',
                                                       'default': False,
                                                       'description': "Also include yesterday's "
                                                                      'entries'}},
                  'required': []}},
 {'name': 'snipara_journal_summarize',
  'description': 'Get journal entries for a date, ready for summarization. Use before archiving '
                 'old journals.',
  'inputSchema': {'type': 'object',
                  'properties': {'date': {'type': 'string',
                                          'description': 'Date to summarize (YYYY-MM-DD)'}},
                  'required': ['date']}},
 {'name': 'snipara_session_memories',
  'description': 'Get tiered durable memories for session bootstrap, with optional short-lived '
                 'carryover. Use at session start to restore memory state, not to retrieve source '
                 'documents.',
  'inputSchema': {'type': 'object',
                  'properties': {'max_critical_tokens': {'type': 'integer',
                                                         'default': 8000,
                                                         'description': 'Token budget for CRITICAL '
                                                                        'tier'},
                                 'max_daily_tokens': {'type': 'integer',
                                                      'default': 4000,
                                                      'description': 'Token budget for DAILY tier'},
                                 'include_yesterday': {'type': 'boolean',
                                                       'default': True,
                                                       'description': "Include yesterday's daily "
                                                                      'memories'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Optional agent namespace to include '
                                                             'in the session bundle'},
                                 'external_user_id': {'type': 'string',
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID whose '
                                                                     'personal memories should be '
                                                                     'included in the session '
                                                                     'bundle.'}},
                  'required': []}},
 {'name': 'snipara_memory_compact',
  'description': 'Compact and optimize memories. Deduplicates similar memories, promotes frequent '
                 'learnings to CRITICAL tier, and archives old entries.',
  'inputSchema': {'type': 'object',
                  'properties': {'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'default': 'project',
                                           'description': 'Memory scope to compact'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Required agent namespace when '
                                                             'scope=agent'},
                                 'external_user_id': {'type': 'string',
                                                      'maxLength': 256,
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID whose '
                                                                     'user-scoped memories should '
                                                                     'be compacted.'},
                                 'deduplicate': {'type': 'boolean',
                                                 'default': True,
                                                 'description': 'Merge similar memories'},
                                 'promote_threshold': {'type': 'integer',
                                                       'default': 3,
                                                       'description': 'If learning accessed N '
                                                                      'times, promote to CRITICAL'},
                                 'archive_older_than_days': {'type': 'integer',
                                                             'default': 30,
                                                             'description': 'Archive memories '
                                                                            'older than N days'},
                                 'dry_run': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Preview changes without applying'}},
                  'required': []}},
 {'name': 'snipara_session_bootstrap_status',
  'description': 'Read-only status for the current engine session memory bootstrap. Reports '
                 'whether bootstrap ran, when it ran, and how many memories/profiles were '
                 'injected.',
  'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
 {'name': 'snipara_owner_profile_get',
  'description': 'Get the canonical personal owner profile for the authenticated user. The profile '
                 'is user-scoped across projects and is used for deterministic session bootstrap. '
                 'Integrator client keys must pass external_user_id.',
  'inputSchema': {'type': 'object',
                  'properties': {'external_user_id': {'type': 'string',
                                                      'maxLength': 256,
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID whose '
                                                                     'personal owner profile '
                                                                     'should be returned.'}},
                  'required': [],
                  'additionalProperties': False},
  'annotations': {'title': 'Get personal owner profile',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False}},
 {'name': 'snipara_owner_profile_update',
  'description': "Patch or replace the authenticated user's canonical personal owner profile. "
                 'Stores durable preferences and operating principles in user-scoped memory; never '
                 'include secrets. Integrator client keys must pass external_user_id.',
  'inputSchema': {'type': 'object',
                  'properties': {'profile': {'type': 'object',
                                             'description': 'Structured personal profile fields to '
                                                            'patch or use as the replacement '
                                                            'profile.',
                                             'properties': {'preferred_language': {'type': 'string',
                                                                                   'maxLength': 2048,
                                                                                   'description': 'Preferred '
                                                                                                  'language '
                                                                                                  'for '
                                                                                                  'agent '
                                                                                                  'communication.'},
                                                            'communication_style': {'type': 'string',
                                                                                    'maxLength': 2048,
                                                                                    'description': 'Preferred '
                                                                                                   'tone, '
                                                                                                   'density, '
                                                                                                   'and '
                                                                                                   'communication '
                                                                                                   'style.'},
                                                            'decision_style': {'type': 'string',
                                                                               'maxLength': 2048,
                                                                               'description': 'How '
                                                                                              'the '
                                                                                              'owner '
                                                                                              'prefers '
                                                                                              'decisions '
                                                                                              'and '
                                                                                              'tradeoffs '
                                                                                              'to '
                                                                                              'be '
                                                                                              'handled.'},
                                                            'autonomy_preference': {'type': 'string',
                                                                                    'maxLength': 2048,
                                                                                    'description': 'Expected '
                                                                                                   'agent '
                                                                                                   'autonomy '
                                                                                                   'and '
                                                                                                   'approval '
                                                                                                   'boundaries.'},
                                                            'risk_tolerance': {'type': 'string',
                                                                               'maxLength': 2048,
                                                                               'description': "Owner's "
                                                                                              'general '
                                                                                              'risk '
                                                                                              'tolerance '
                                                                                              'and '
                                                                                              'escalation '
                                                                                              'preference.'},
                                                            'evidence_preferences': {'type': 'string',
                                                                                     'maxLength': 2048,
                                                                                     'description': 'Preferred '
                                                                                                    'proof, '
                                                                                                    'verification, '
                                                                                                    'and '
                                                                                                    'sourcing '
                                                                                                    'style.'},
                                                            'product_principles': {'type': 'array',
                                                                                   'maxItems': 12,
                                                                                   'items': {'type': 'string',
                                                                                             'maxLength': 512},
                                                                                   'description': 'Durable '
                                                                                                  'product '
                                                                                                  'principles '
                                                                                                  'that '
                                                                                                  'should '
                                                                                                  'guide '
                                                                                                  'work.'},
                                                            'non_negotiables': {'type': 'array',
                                                                                'maxItems': 12,
                                                                                'items': {'type': 'string',
                                                                                          'maxLength': 512},
                                                                                'description': 'Boundaries '
                                                                                               'and '
                                                                                               'constraints '
                                                                                               'that '
                                                                                               'agents '
                                                                                               'must '
                                                                                               'preserve.'},
                                                            'working_preferences': {'type': 'array',
                                                                                    'maxItems': 12,
                                                                                    'items': {'type': 'string',
                                                                                              'maxLength': 512},
                                                                                    'description': 'Stable '
                                                                                                   'workflow '
                                                                                                   'and '
                                                                                                   'collaboration '
                                                                                                   'preferences.'}},
                                             'additionalProperties': False},
                                 'replace': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Replace the canonical profile instead '
                                                            'of patching the supplied fields into '
                                                            'it.'},
                                 'evidence_refs': {'type': 'array',
                                                   'maxItems': 24,
                                                   'items': {'type': 'string', 'maxLength': 512},
                                                   'description': 'Optional source references '
                                                                  'supporting this profile '
                                                                  'update.'},
                                 'external_user_id': {'type': 'string',
                                                      'maxLength': 256,
                                                      'description': 'Integrator client keys only: '
                                                                     'stable end-user ID whose '
                                                                     'personal owner profile '
                                                                     'should be updated.'}},
                  'required': ['profile'],
                  'additionalProperties': False},
  'annotations': {'title': 'Update personal owner profile',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False}},
 {'name': 'snipara_memory_health',
  'description': 'Read-only memory hygiene diagnostics. Returns active memory counts, top '
                 'categories, auto-compaction threshold status, and samples of known noise/anomaly '
                 'patterns without mutating memory.',
  'inputSchema': {'type': 'object',
                  'properties': {'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'description': 'Optional memory scope to inspect. '
                                                          'Defaults to all visible project-owned '
                                                          'scopes.'},
                                 'include_inactive': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include INVALIDATED and '
                                                                     'SUPERSEDED memories in the '
                                                                     'scan.'},
                                 'sample_limit': {'type': 'integer',
                                                  'default': 5,
                                                  'minimum': 0,
                                                  'maximum': 20,
                                                  'description': 'Maximum anomaly samples to '
                                                                 'return.'}},
                  'required': []}},
 {'name': 'snipara_memory_duplicate_candidates',
  'description': 'Read-only duplicate/supersession review candidates. Groups exact and near '
                 'duplicate memories and suggests which IDs to keep or supersede without mutating '
                 'memory.',
  'inputSchema': {'type': 'object',
                  'properties': {'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'description': 'Optional memory scope to inspect.'},
                                 'include_inactive': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include INVALIDATED and '
                                                                     'SUPERSEDED memories in '
                                                                     'duplicate grouping.'},
                                 'limit': {'type': 'integer',
                                           'default': 20,
                                           'minimum': 1,
                                           'maximum': 100,
                                           'description': 'Maximum duplicate groups to return.'},
                                 'min_similarity': {'type': 'number',
                                                    'default': 0.9,
                                                    'minimum': 0,
                                                    'maximum': 1,
                                                    'description': 'Lexical similarity threshold '
                                                                   'for near-duplicate groups.'}},
                  'required': []}},
 {'name': 'snipara_memory_clean_candidates',
  'description': 'Read-only grouped memory cleanup candidates. Returns noise, duplicates, possibly '
                 'stale memories, category anomalies, and review-queue items without mutating '
                 'memory.',
  'inputSchema': {'type': 'object',
                  'properties': {'scope': {'type': 'string',
                                           'enum': ['agent', 'project', 'team', 'user'],
                                           'description': 'Optional memory scope to inspect.'},
                                 'include_inactive': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include INVALIDATED and '
                                                                     'SUPERSEDED memories in the '
                                                                     'scan.'},
                                 'limit_per_bucket': {'type': 'integer',
                                                      'default': 10,
                                                      'minimum': 1,
                                                      'maximum': 50,
                                                      'description': 'Maximum candidates to return '
                                                                     'per bucket.'}},
                  'required': []}},
 {'name': 'snipara_memory_daily_brief',
  'description': "Generate a 'Top N active constraints' daily brief. Summarizes critical "
                 'decisions, active rules, and pending todos.',
  'inputSchema': {'type': 'object',
                  'properties': {'date': {'type': 'string',
                                          'description': 'Date for brief (default: today)'},
                                 'max_items': {'type': 'integer',
                                               'default': 10,
                                               'description': 'Maximum items to include'}},
                  'required': []}},
 {'name': 'snipara_tenant_profile_create',
  'description': 'Create a structured tenant/client profile. Stored as CRITICAL memory for '
                 'auto-loading. Use for client onboarding.',
  'inputSchema': {'type': 'object',
                  'properties': {'client_name': {'type': 'string',
                                                 'description': 'Name of the client/tenant '
                                                                '(required)'},
                                 'business_model': {'type': 'string',
                                                    'description': 'How the business works'},
                                 'industry': {'type': 'string', 'description': 'Industry vertical'},
                                 'tech_stack': {'type': 'string',
                                                'description': 'Technology stack used'},
                                 'legal_constraints': {'type': 'string',
                                                       'description': 'Legal requirements'},
                                 'security_requirements': {'type': 'string',
                                                           'description': 'Security constraints'},
                                 'ui_ux_prefs': {'type': 'string',
                                                 'description': 'UI/UX preferences'},
                                 'communication_style': {'type': 'string',
                                                         'description': 'How to communicate'},
                                 'risk_tolerance': {'type': 'string',
                                                    'enum': ['low', 'medium', 'high'],
                                                    'description': 'Risk tolerance level'},
                                 'dos': {'type': 'array',
                                         'items': {'type': 'string'},
                                         'description': 'List of things to do'},
                                 'donts': {'type': 'array',
                                           'items': {'type': 'string'},
                                           'description': 'List of things to avoid'},
                                 'custom_fields': {'type': 'object',
                                                   'description': 'Additional custom fields'}},
                  'required': ['client_name']}},
 {'name': 'snipara_tenant_profile_get',
  'description': 'Get tenant profile(s) for a project. Returns latest profile if tenant_id not '
                 'specified.',
  'inputSchema': {'type': 'object',
                  'properties': {'tenant_id': {'type': 'string',
                                               'description': 'Specific profile ID (optional, '
                                                              'returns all if not specified)'}},
                  'required': []}},
 {'name': 'snipara_swarm_create',
  'description': 'Create a new agent swarm for multi-agent coordination.',
  'inputSchema': {'type': 'object',
                  'properties': {'name': {'type': 'string', 'description': 'Swarm name'},
                                 'description': {'type': 'string'},
                                 'max_agents': {'type': 'integer', 'default': 10},
                                 'task_timeout': {'type': 'integer',
                                                  'default': 600,
                                                  'description': 'Task lease timeout in seconds'},
                                 'claim_timeout': {'type': 'integer',
                                                   'default': 300,
                                                   'description': 'Resource claim lease timeout in '
                                                                  'seconds'},
                                 'reuse_existing': {'type': 'boolean',
                                                    'default': False,
                                                    'description': 'Return an active same-name '
                                                                   'swarm instead of creating a '
                                                                   'duplicate'},
                                 'config': {'type': 'object'}},
                  'required': ['name']}},
 {'name': 'snipara_swarm_delete',
  'description': 'Delete an agent swarm and its related runtime data. Requires ADMIN access.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string',
                                              'description': 'Swarm ID to delete'}},
                  'required': ['swarm_id']}},
 {'name': 'snipara_swarm_join',
  'description': 'Join an existing swarm as an agent.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm to join'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Your unique agent identifier'},
                                 'role': {'type': 'string',
                                          'enum': ['coordinator', 'worker', 'observer'],
                                          'default': 'worker'},
                                 'capabilities': {'type': 'array', 'items': {'type': 'string'}}},
                  'required': ['swarm_id', 'agent_id']}},
 {'name': 'snipara_agent_profile_get',
  'description': "Get an agent's profile (identity, personality, boundaries). Auto-loaded on "
                 'session start for swarm agents.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'agent_id': {'type': 'string', 'description': 'Agent identifier'}},
                  'required': ['swarm_id', 'agent_id']}},
 {'name': 'snipara_agent_profile_update',
  'description': "Update an agent's profile. Use to set personality, boundaries, communication "
                 'style.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'agent_id': {'type': 'string', 'description': 'Agent identifier'},
                                 'profile': {'type': 'object',
                                             'description': 'Profile data (merged with existing)',
                                             'properties': {'display_name': {'type': 'string',
                                                                             'description': 'Display '
                                                                                            'name '
                                                                                            '(e.g., '
                                                                                            "'Jarvis "
                                                                                            "⚡')"},
                                                            'personality': {'type': 'string',
                                                                            'description': 'Personality '
                                                                                           'type '
                                                                                           '(e.g., '
                                                                                           "'INTJ "
                                                                                           '- '
                                                                                           "Strategic')"},
                                                            'role_description': {'type': 'string',
                                                                                 'description': 'Role '
                                                                                                'description'},
                                                            'boundaries': {'type': 'array',
                                                                           'items': {'type': 'string'},
                                                                           'description': 'Boundaries '
                                                                                          'and '
                                                                                          'limits'},
                                                            'communication_style': {'type': 'string',
                                                                                    'description': 'Preferred '
                                                                                                   'communication '
                                                                                                   'style'},
                                                            'decision_making': {'type': 'string',
                                                                                'description': 'Decision-making '
                                                                                               'approach'},
                                                            'soul_document_path': {'type': 'string',
                                                                                   'description': 'Path '
                                                                                                  'to '
                                                                                                  'SOUL.md '
                                                                                                  'document'},
                                                            'memory_scope': {'type': 'string',
                                                                             'enum': ['agent',
                                                                                      'project',
                                                                                      'team'],
                                                                             'description': 'Memory '
                                                                                            'scope'}}}},
                  'required': ['swarm_id', 'agent_id', 'profile']}},
 {'name': 'snipara_claim',
  'description': 'Claim exclusive access to a resource (file, function, module). Claims '
                 'auto-expire.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'agent_id': {'type': 'string'},
                                 'resource_type': {'type': 'string',
                                                   'enum': ['file',
                                                            'function',
                                                            'module',
                                                            'component',
                                                            'other']},
                                 'resource_id': {'type': 'string',
                                                 'description': 'Resource identifier (e.g., file '
                                                                'path)'},
                                 'timeout_seconds': {'type': 'integer', 'default': 300}},
                  'required': ['swarm_id', 'agent_id', 'resource_type', 'resource_id']}},
 {'name': 'snipara_release',
  'description': 'Release a claimed resource.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'agent_id': {'type': 'string'},
                                 'claim_id': {'type': 'string'},
                                 'resource_type': {'type': 'string'},
                                 'resource_id': {'type': 'string'}},
                  'required': ['swarm_id', 'agent_id']}},
 {'name': 'snipara_state_get',
  'description': 'Read shared swarm state by key.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'key': {'type': 'string', 'description': 'State key to read'}},
                  'required': ['swarm_id', 'key']}},
 {'name': 'snipara_state_set',
  'description': 'Write shared swarm state with optimistic locking and optional TTL.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'agent_id': {'type': 'string'},
                                 'key': {'type': 'string'},
                                 'value': {'description': 'Value to set (any JSON-serializable '
                                                          'type)'},
                                 'expected_version': {'type': 'integer',
                                                      'description': 'Expected version for '
                                                                     'optimistic locking'},
                                 'ttl_seconds': {'type': 'integer',
                                                 'description': 'Time to live in seconds '
                                                                '(optional, state expires after '
                                                                'this)'}},
                  'required': ['swarm_id', 'agent_id', 'key', 'value']}},
 {'name': 'snipara_state_poll',
  'description': 'Poll for state changes across multiple keys. Returns only keys that changed '
                 'since last_versions. Use for efficient multi-key monitoring without individual '
                 'get calls.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'keys': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'List of state keys to monitor'},
                                 'last_versions': {'type': 'object',
                                                   'additionalProperties': {'type': 'integer'},
                                                   'description': 'Map of key -> last known '
                                                                  'version. Only keys with newer '
                                                                  'versions are returned.',
                                                   'default': {}}},
                  'required': ['swarm_id', 'keys']}},
 {'name': 'snipara_broadcast',
  'description': 'Send an event to all agents in the swarm.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'agent_id': {'type': 'string'},
                                 'event_type': {'type': 'string', 'description': 'Event type'},
                                 'payload': {'type': 'object', 'description': 'Event data'}},
                  'required': ['swarm_id', 'agent_id', 'event_type']}},
 {'name': 'snipara_swarm_events',
  'description': 'Query and filter broadcast events plus htask audit events in a swarm. Use '
                 'snipara_htask_audit_trail for task-only polling.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string'},
                                 'event_type': {'type': 'string',
                                                'description': 'Filter by event type'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Filter by sending agent'},
                                 'since': {'type': 'string',
                                           'format': 'date-time',
                                           'description': 'Only events after this timestamp (ISO '
                                                          '8601)'},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'description': 'Maximum events to return'}},
                  'required': ['swarm_id']}},
 {'name': 'snipara_agent_status',
  'description': 'Get swarm agent status with pending tasks and clear instructions.\n'
                 '\n'
                 'Call this at session start to discover tasks assigned to you. Returns:\n'
                 '- Pending tasks assigned to your agent (use snipara_htask_recommend_batch to '
                 'inspect)\n'
                 "- Active swarms you've joined\n"
                 "- Current task you're working on (if any)\n"
                 '- Clear instructions on what to do next\n'
                 '\n'
                 'This is THE discovery tool for swarm agents - tells you what work is waiting.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string',
                                              'description': 'Swarm ID to check status for'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Your agent identifier in the swarm'}},
                  'required': ['swarm_id', 'agent_id']}},
 {'name': 'snipara_swarm_leave',
  'description': 'Remove an agent from a swarm.\n'
                 '\n'
                 'Use this to:\n'
                 '- Clean up inactive/crashed agents\n'
                 '- Remove yourself from a swarm when done\n'
                 '- Free up agent slots for others\n'
                 '\n'
                 'What happens on removal:\n'
                 '1. All resource claims held by the agent are released\n'
                 '2. Pending/claimed tasks assigned to the agent are unassigned\n'
                 '3. The agent record is deleted from the swarm\n'
                 '\n'
                 'The agent can rejoin later with snipara_swarm_join.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'agent_id': {'type': 'string',
                                              'description': 'Agent ID to remove (can be yourself '
                                                             'or another agent)'}},
                  'required': ['swarm_id', 'agent_id']}},
 {'name': 'snipara_swarm_members',
  'description': 'List all agents in a swarm with their status.\n'
                 '\n'
                 "Returns each agent's:\n"
                 "- agent_id: The agent's identifier\n"
                 '- role: coordinator, worker, or observer\n'
                 '- status: active, idle, busy\n'
                 '- capabilities: What the agent can do\n'
                 "- current_task: What they're working on (if any)\n"
                 '- joined_at: When they joined\n'
                 '\n'
                 'Use this to:\n'
                 "- See who's in the swarm\n"
                 '- Find available agents for task assignment\n'
                 '- Monitor agent activity',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'}},
                  'required': ['swarm_id']}},
 {'name': 'snipara_swarm_update',
  'description': 'Update swarm configuration (requires ADMIN access).\n'
                 '\n'
                 'Updatable settings:\n'
                 '- name: Swarm display name\n'
                 '- description: What the swarm is for\n'
                 '- max_agents: Maximum agents allowed (plan-limited)\n'
                 '- task_timeout: Seconds before unclaimed task expires (60-3600)\n'
                 '- claim_timeout: Seconds a resource claim lasts (60-7200)',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string',
                                              'description': 'Swarm ID to update'},
                                 'name': {'type': 'string', 'description': 'New swarm name'},
                                 'description': {'type': 'string',
                                                 'description': 'New description'},
                                 'max_agents': {'type': 'integer',
                                                'minimum': 1,
                                                'maximum': 100,
                                                'description': 'Maximum agents allowed'},
                                 'task_timeout': {'type': 'integer',
                                                  'minimum': 60,
                                                  'maximum': 3600,
                                                  'description': 'Task claim timeout in seconds'},
                                 'claim_timeout': {'type': 'integer',
                                                   'minimum': 60,
                                                   'maximum': 7200,
                                                   'description': 'Resource claim timeout in '
                                                                  'seconds'}},
                  'required': ['swarm_id']}},
 {'name': 'snipara_upload_document',
  'description': 'Upload or update a document in the project. Supports text documents (.md, '
                 '.markdown, .mdx, .txt, .rst, .adoc) and binary parser documents (.pdf, .docx, '
                 '.pptx, .svg, .vsdx, .xlsx). Binary payloads should use base64:<payload> except '
                 'SVG, which may use raw XML.',
  'inputSchema': {'type': 'object',
                  'properties': {'path': {'type': 'string',
                                          'description': "Document path (e.g., 'docs/api.md')"},
                                 'content': {'type': 'string',
                                             'description': 'Document content, or base64:<payload> '
                                                            'for binary files'},
                                 'kind': {'type': 'string',
                                          'enum': ['DOC', 'BINARY'],
                                          'description': 'Document pipeline kind. Inferred from '
                                                         'path when omitted.'},
                                 'format': {'type': 'string',
                                            'enum': ['adoc',
                                                     'docx',
                                                     'markdown',
                                                     'md',
                                                     'mdx',
                                                     'pdf',
                                                     'pptx',
                                                     'rst',
                                                     'svg',
                                                     'txt',
                                                     'vsdx',
                                                     'xlsx'],
                                            'description': 'Document format. Inferred from file '
                                                           'extension when omitted.'},
                                 'language': {'type': 'string',
                                              'description': 'Optional language hint. Usually '
                                                             'omitted for DOC and BINARY uploads.'},
                                 'metadata': {'type': 'object',
                                              'description': 'Optional structured metadata such as '
                                                             'assetClass, usageMode '
                                                             '(current_truth|historical_reference|template|global_knowledge), '
                                                             'clientId, sourceKind, '
                                                             'sourceModifiedAt, sourceSnapshotAt, '
                                                             'sourceContentHash, freshnessPolicy, '
                                                             'parser, and provenance fields',
                                              'additionalProperties': True}},
                  'required': ['path', 'content']}},
 {'name': 'snipara_sync_documents',
  'description': 'Bulk sync multiple documents. Use for batch uploads or CI/CD integration.',
  'inputSchema': {'type': 'object',
                  'properties': {'documents': {'type': 'array',
                                               'items': {'type': 'object',
                                                         'properties': {'path': {'type': 'string'},
                                                                        'content': {'type': 'string',
                                                                                    'description': 'Plain '
                                                                                                   'text '
                                                                                                   'or '
                                                                                                   'base64:<payload> '
                                                                                                   'for '
                                                                                                   'binary '
                                                                                                   'files'},
                                                                        'kind': {'type': 'string',
                                                                                 'enum': ['DOC',
                                                                                          'BINARY'],
                                                                                 'description': 'Document '
                                                                                                'pipeline '
                                                                                                'kind. '
                                                                                                'Inferred '
                                                                                                'from '
                                                                                                'path '
                                                                                                'when '
                                                                                                'omitted.'},
                                                                        'format': {'type': 'string',
                                                                                   'enum': ['adoc',
                                                                                            'docx',
                                                                                            'markdown',
                                                                                            'md',
                                                                                            'mdx',
                                                                                            'pdf',
                                                                                            'pptx',
                                                                                            'rst',
                                                                                            'svg',
                                                                                            'txt',
                                                                                            'vsdx',
                                                                                            'xlsx'],
                                                                                   'description': 'Document '
                                                                                                  'format. '
                                                                                                  'Inferred '
                                                                                                  'from '
                                                                                                  'file '
                                                                                                  'extension '
                                                                                                  'when '
                                                                                                  'omitted.'},
                                                                        'language': {'type': 'string',
                                                                                     'description': 'Optional '
                                                                                                    'language '
                                                                                                    'hint. '
                                                                                                    'Usually '
                                                                                                    'omitted '
                                                                                                    'for '
                                                                                                    'DOC '
                                                                                                    'and '
                                                                                                    'BINARY '
                                                                                                    'uploads.'},
                                                                        'metadata': {'type': 'object',
                                                                                     'description': 'Optional '
                                                                                                    'structured '
                                                                                                    'metadata '
                                                                                                    'for '
                                                                                                    'business '
                                                                                                    'context, '
                                                                                                    'diagrams, '
                                                                                                    'source '
                                                                                                    'freshness, '
                                                                                                    'historical '
                                                                                                    'references, '
                                                                                                    'templates, '
                                                                                                    'and '
                                                                                                    'provenance',
                                                                                     'additionalProperties': True}},
                                                         'required': ['path', 'content']},
                                               'description': 'Documents to sync'},
                                 'delete_missing': {'type': 'boolean',
                                                    'default': False,
                                                    'description': 'Delete docs not in list. '
                                                                   'Requires '
                                                                   'confirm_delete_missing=true.'},
                                 'confirm_delete_missing': {'type': 'boolean',
                                                            'default': False,
                                                            'description': 'Required true when '
                                                                           'delete_missing=true to '
                                                                           'confirm destructive '
                                                                           'pruning.'}},
                  'required': ['documents']}},
 {'name': 'snipara_document_tombstones',
  'description': 'List project-scoped tombstones for deleted or pruned documents. Use this to '
                 'inspect soft-deleted context, understand what was removed, and review expiration '
                 'windows before permanent purge.',
  'inputSchema': {'type': 'object',
                  'properties': {'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 200,
                                           'description': 'Maximum number of tombstones to return'},
                                 'include_expired': {'type': 'boolean',
                                                     'default': False,
                                                     'description': 'Include tombstones that are '
                                                                    'past retention but not yet '
                                                                    'purged'}}}},
 {'name': 'snipara_svg_bundle_ingest',
  'description': 'Generate a native SVG companion context bundle and optionally upload the '
                 'generated Markdown documents. Use dry_run=true to preview bundle IDs, paths, and '
                 'payload size. Uploaded bundle documents store '
                 'bundleId/sourceHash/sourcePath/artifactRole metadata.',
  'inputSchema': {'type': 'object',
                  'properties': {'svg_content': {'type': 'string',
                                                 'description': 'Raw SVG XML content'},
                                 'source_path': {'type': 'string',
                                                 'description': 'Original SVG path used for stable '
                                                                'bundle identity'},
                                 'upload_prefix': {'type': 'string',
                                                   'default': 'svg-context',
                                                   'description': 'Destination path prefix for '
                                                                  'generated companion documents'},
                                 'include_enriched_svg': {'type': 'boolean',
                                                          'default': True,
                                                          'description': 'Include an enriched SVG '
                                                                         'XML markdown companion'},
                                 'dry_run': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Return the bundle summary without '
                                                            'writing documents'},
                                 'reindex': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Trigger a document reindex job after '
                                                            'a non-dry-run upload'},
                                 'reindex_mode': {'type': 'string',
                                                  'enum': ['incremental', 'full'],
                                                  'default': 'incremental',
                                                  'description': 'Document reindex mode to use '
                                                                 'when reindex=true'}},
                  'required': ['svg_content', 'source_path']}},
 {'name': 'snipara_request_access',
  'description': 'Request access to a project.\n'
                 '\n'
                 'Allows team members with NONE access level to request higher access levels\n'
                 '(VIEWER, EDITOR, ADMIN) from project admins. Creates an access request that\n'
                 'admins can approve or deny via the dashboard.',
  'inputSchema': {'type': 'object',
                  'properties': {'requested_level': {'type': 'string',
                                                     'enum': ['VIEWER', 'EDITOR', 'ADMIN'],
                                                     'default': 'VIEWER',
                                                     'description': 'The access level to request'},
                                 'reason': {'type': 'string',
                                            'description': 'Optional reason for requesting '
                                                           'access'}},
                  'required': []}},
 {'name': 'snipara_load_document',
  'description': 'Load one exact source document by path. Use when you already know the document '
                 'path and need direct source truth instead of ranked retrieval or memory recall.',
  'inputSchema': {'type': 'object',
                  'properties': {'path': {'type': 'string',
                                          'description': 'Exact document path (for example '
                                                         "'docs/api.md' or "
                                                         "'clients/acme/rfp.md')"}},
                  'required': ['path']}},
 {'name': 'snipara_load_project',
  'description': 'Load structured map of all project documents with content. Returns a '
                 'token-budgeted dump of every file, with optional path filtering. Use for '
                 'full-project exploration.',
  'inputSchema': {'type': 'object',
                  'properties': {'max_tokens': {'type': 'integer',
                                                'default': 16000,
                                                'description': 'Total token budget for returned '
                                                               'content'},
                                 'paths_filter': {'type': 'array',
                                                  'items': {'type': 'string'},
                                                  'description': 'Only include files matching '
                                                                 'these path prefixes (e.g., '
                                                                 "['docs/', 'src/'])"},
                                 'include_content': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Include file content (false = '
                                                                    'metadata only)'}},
                  'required': []}},
 {'name': 'snipara_orchestrate',
  'description': 'Multi-round context exploration in a single call. Performs: (1) section scan for '
                 'project structure, (2) ranked search for top relevant sections, (3) raw file '
                 'load for highest-scoring documents. Combines search intelligence with raw '
                 'access.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'maxLength': 20480,
                                           'description': 'The question or topic to explore'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 16000,
                                                'minimum': 500,
                                                'maximum': 50000,
                                                'description': 'Token budget for raw file content'},
                                 'top_k': {'type': 'integer',
                                           'default': 5,
                                           'minimum': 1,
                                           'maximum': 20,
                                           'description': 'Number of top sections to use for file '
                                                          'selection'},
                                 'search_mode': {'type': 'string',
                                                 'enum': ['keyword', 'semantic', 'hybrid'],
                                                 'default': 'hybrid'}},
                  'required': ['query']}},
 {'name': 'snipara_repl_context',
  'description': "Bridge between Snipara's context optimization and Snipara Sandbox code "
                 'execution.\n'
                 '\n'
                 'PURPOSE: Package project documentation into a Python-ready format that can be '
                 'injected into a Snipara Sandbox REPL session for context-aware code execution.\n'
                 '\n'
                 'WORKFLOW:\n'
                 '1. Call snipara_repl_context to get context_data + setup_code\n'
                 "2. Use set_repl_context(key='context', value=context_data) to inject data\n"
                 '3. Use execute_python(setup_code) to load helper functions\n'
                 '4. Use helpers (peek, grep, find_function, etc.) to explore context\n'
                 '5. Execute code with full documentation context available\n'
                 '\n'
                 'USE CASES:\n'
                 '- Implement features with documentation awareness\n'
                 '- Debug code with access to related docs\n'
                 '- Write tests referencing specifications\n'
                 '- Refactor with architecture docs available\n'
                 '\n'
                 'Returns context_data (files + sections), setup_code (helper functions), and '
                 'usage hints.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'Optional query to filter context by '
                                                          'relevance. If empty, loads files in '
                                                          'order within budget.'},
                                 'max_tokens': {'type': 'integer',
                                                'default': 8000,
                                                'description': 'Token budget for file content'},
                                 'include_helpers': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Include Python helper '
                                                                    'functions: peek(), grep(), '
                                                                    'sections(), files(), '
                                                                    'get_file(), search(), trim(), '
                                                                    'find_function(), '
                                                                    'list_imports(), '
                                                                    'context_summary()'},
                                 'search_mode': {'type': 'string',
                                                 'enum': ['keyword', 'semantic', 'hybrid'],
                                                 'default': 'hybrid',
                                                 'description': 'Search mode when query is '
                                                                'provided'}},
                  'required': []}},
 {'name': 'snipara_get_chunk',
  'description': 'Retrieve full content by chunk ID. Use with '
                 'snipara_context_query(return_references=True) to fetch full content of specific '
                 'sections. This pass-by-reference pattern reduces hallucination by maintaining '
                 'clear source attribution.',
  'inputSchema': {'type': 'object',
                  'properties': {'chunk_id': {'type': 'string',
                                              'description': 'The chunk ID from '
                                                             'snipara_context_query results (when '
                                                             'return_references=True)'},
                                 'correlation_context': {'type': 'object',
                                                         'additionalProperties': False,
                                                         'description': 'Optional '
                                                                        'retrieval-correlation '
                                                                        'context. Reuse session_id '
                                                                        'across retrieval and '
                                                                        'outcome calls so '
                                                                        'telemetry can be joined '
                                                                        'inside the authenticated '
                                                                        'project. These '
                                                                        'identifiers never change '
                                                                        'authorization or project '
                                                                        'scope; do not include '
                                                                        'secrets, tenant IDs, or '
                                                                        'user data.',
                                                         'properties': {'version': {'type': 'string',
                                                                                    'enum': ['retrieval-correlation-v1'],
                                                                                    'default': 'retrieval-correlation-v1'},
                                                                        'session_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Preferred '
                                                                                                      'stable '
                                                                                                      'opaque '
                                                                                                      'session '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'for '
                                                                                                      'telemetry '
                                                                                                      'association.'},
                                                                        'workflow_session_id': {'type': 'string',
                                                                                                'minLength': 1,
                                                                                                'maxLength': 128,
                                                                                                'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                                'description': 'Opaque '
                                                                                                               'workflow '
                                                                                                               'ID '
                                                                                                               'used '
                                                                                                               'when '
                                                                                                               'session_id '
                                                                                                               'is '
                                                                                                               'absent.'},
                                                                        'correlation_id': {'type': 'string',
                                                                                           'minLength': 1,
                                                                                           'maxLength': 128,
                                                                                           'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                           'description': 'Opaque '
                                                                                                          'request-chain '
                                                                                                          'ID '
                                                                                                          'used '
                                                                                                          'when '
                                                                                                          'session '
                                                                                                          'fields '
                                                                                                          'are '
                                                                                                          'absent.'},
                                                                        'request_id': {'type': 'string',
                                                                                       'minLength': 1,
                                                                                       'maxLength': 128,
                                                                                       'pattern': '^[A-Za-z0-9][A-Za-z0-9._~:/@+\\-]{0,127}$',
                                                                                       'description': 'Opaque '
                                                                                                      'per-call '
                                                                                                      'ID '
                                                                                                      'used '
                                                                                                      'only '
                                                                                                      'as '
                                                                                                      'a '
                                                                                                      'final '
                                                                                                      'telemetry '
                                                                                                      'fallback.'}}}},
                  'required': ['chunk_id']},
  'annotations': {'title': 'Load cited context chunk',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False},
  '_meta': {'snipara_tool_weight': 8.0}},
 {'name': 'snipara_decision_create',
  'description': 'Create a structured decision record (ADR-style) for architectural or technical '
                 'decisions.\n'
                 '\n'
                 'Records decisions with context, rationale, alternatives considered, and revert '
                 'plans.\n'
                 'Auto-generates DEC-XXX IDs. Supports tags for categorization.\n'
                 '\n'
                 'Use for:\n'
                 '- Architectural decisions (database choice, framework selection)\n'
                 '- Technical trade-offs (performance vs maintainability)\n'
                 '- Process decisions (deployment strategy, testing approach)',
  'inputSchema': {'type': 'object',
                  'properties': {'title': {'type': 'string',
                                           'description': 'Short title for the decision (e.g., '
                                                          "'Use Redis for caching')"},
                                 'owner': {'type': 'string',
                                           'description': 'Who made or is responsible for this '
                                                          'decision'},
                                 'scope': {'type': 'string',
                                           'description': "Scope/area affected (e.g., 'backend', "
                                                          "'authentication', 'database')"},
                                 'impact': {'type': 'string',
                                            'enum': ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
                                            'default': 'MEDIUM',
                                            'description': 'Impact level of this decision'},
                                 'context': {'type': 'string',
                                             'description': 'Background and context for why this '
                                                            'decision was needed'},
                                 'decision': {'type': 'string',
                                              'description': 'The actual decision made (what was '
                                                             'chosen)'},
                                 'rationale': {'type': 'string',
                                               'description': 'Why this option was chosen over '
                                                              'alternatives'},
                                 'alternatives': {'type': 'array',
                                                  'items': {'type': 'string'},
                                                  'description': 'List of alternatives that were '
                                                                 'considered'},
                                 'revert_plan': {'type': 'string',
                                                 'description': 'How to revert this decision if '
                                                                'needed (optional)'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Tags for categorization (e.g., '
                                                         "['architecture', 'caching', "
                                                         "'performance'])"}},
                  'required': ['title', 'owner', 'scope', 'context', 'decision', 'rationale']}},
 {'name': 'snipara_decision_query',
  'description': 'Query project decisions with filters.\n'
                 '\n'
                 'Search by status, impact, scope, tags, or text query.\n'
                 'Returns decisions sorted by recency with supersession chain info.',
  'inputSchema': {'type': 'object',
                  'properties': {'query': {'type': 'string',
                                           'description': 'Text search in title, context, '
                                                          'decision, rationale'},
                                 'status': {'type': 'string',
                                            'enum': ['ACTIVE', 'SUPERSEDED', 'REVERTED', 'DRAFT'],
                                            'description': 'Filter by decision status'},
                                 'impact': {'type': 'string',
                                            'enum': ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
                                            'description': 'Filter by impact level'},
                                 'scope': {'type': 'string', 'description': 'Filter by scope/area'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Filter by tags (OR logic)'},
                                 'limit': {'type': 'integer',
                                           'default': 10,
                                           'description': 'Maximum decisions to return'},
                                 'include_superseded': {'type': 'boolean',
                                                        'default': False,
                                                        'description': 'Include superseded '
                                                                       'decisions in results'}},
                  'required': []}},
 {'name': 'snipara_decision_supersede',
  'description': 'Supersede an existing decision with a new one.\n'
                 '\n'
                 'Creates a new decision that replaces an old one, maintaining the chain of '
                 'evolution.\n'
                 'The old decision is marked as SUPERSEDED with a link to the new decision.',
  'inputSchema': {'type': 'object',
                  'properties': {'old_decision_id': {'type': 'string',
                                                     'description': 'The DEC-XXX ID of the '
                                                                    'decision being superseded'},
                                 'title': {'type': 'string',
                                           'description': 'Title for the new decision'},
                                 'owner': {'type': 'string',
                                           'description': 'Who made this new decision'},
                                 'scope': {'type': 'string', 'description': 'Scope/area affected'},
                                 'impact': {'type': 'string',
                                            'enum': ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
                                            'description': 'Impact level'},
                                 'context': {'type': 'string',
                                             'description': 'Why the original decision is being '
                                                            'changed'},
                                 'decision': {'type': 'string', 'description': 'The new decision'},
                                 'rationale': {'type': 'string',
                                               'description': 'Why this change is being made'},
                                 'alternatives': {'type': 'array',
                                                  'items': {'type': 'string'},
                                                  'description': 'Alternatives considered for the '
                                                                 'new decision'},
                                 'revert_plan': {'type': 'string',
                                                 'description': 'How to revert this decision if '
                                                                'needed'},
                                 'tags': {'type': 'array',
                                          'items': {'type': 'string'},
                                          'description': 'Tags for the new decision'}},
                  'required': ['old_decision_id',
                               'title',
                               'owner',
                               'context',
                               'decision',
                               'rationale']}},
 {'name': 'snipara_index_health',
  'description': 'Get comprehensive index health metrics for your project.\n'
                 '\n'
                 'Returns coverage, quality scores, tier distribution, stale document detection, '
                 'and overall health score.\n'
                 'Use this to monitor the health of your documentation index and identify issues.',
  'inputSchema': {'type': 'object',
                  'properties': {'stale_threshold_days': {'type': 'integer',
                                                          'default': 30,
                                                          'minimum': 1,
                                                          'maximum': 365,
                                                          'description': 'Days after which content '
                                                                         'is considered stale'}},
                  'required': []}},
 {'name': 'snipara_index_recommendations',
  'description': 'Get actionable recommendations to improve your index health.\n'
                 '\n'
                 'Returns prioritized list of recommendations based on current index health '
                 'metrics.\n'
                 'Recommendations include actions like reindexing, improving coverage, and '
                 'reviewing quality.',
  'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
 {'name': 'snipara_reindex',
  'description': 'Trigger a project reindex job or poll an existing reindex job.\n'
                 '\n'
                 'Use this when index coverage is low, documents are missing chunks, or you need '
                 'to rebuild\n'
                 'documentation/code indexes after large sync operations. Call without job_id to '
                 'create a job,\n'
                 'or pass job_id to check progress via MCP.',
  'inputSchema': {'type': 'object',
                  'properties': {'job_id': {'type': 'string',
                                            'description': 'Existing reindex job ID to poll '
                                                           'instead of creating a new one'},
                                 'mode': {'type': 'string',
                                          'enum': ['incremental', 'full'],
                                          'default': 'incremental',
                                          'description': 'Reindex mode when creating a new job'},
                                 'kind': {'type': 'string',
                                          'enum': ['doc', 'code'],
                                          'default': 'doc',
                                          'description': 'Which index to rebuild when creating a '
                                                         'new job'}},
                  'required': []}},
 {'name': 'snipara_search_analytics',
  'description': 'Get comprehensive search analytics for your project.\n'
                 '\n'
                 'Returns query counts, success rates, latency percentiles, tool usage breakdown,\n'
                 'daily trends, and error analysis for the specified time period.',
  'inputSchema': {'type': 'object',
                  'properties': {'days': {'type': 'integer',
                                          'default': 30,
                                          'minimum': 1,
                                          'maximum': 90,
                                          'description': 'Number of days to analyze'}},
                  'required': []}},
 {'name': 'snipara_query_trends',
  'description': 'Get query trends over time with configurable granularity.\n'
                 '\n'
                 'Returns time-bucketed query counts, success rates, and latency for trend '
                 'analysis.',
  'inputSchema': {'type': 'object',
                  'properties': {'days': {'type': 'integer',
                                          'default': 7,
                                          'minimum': 1,
                                          'maximum': 30,
                                          'description': 'Number of days to analyze'},
                                 'granularity': {'type': 'string',
                                                 'enum': ['hour', 'day'],
                                                 'default': 'hour',
                                                 'description': 'Time bucket granularity'}},
                  'required': []}},
 {'name': 'snipara_adaptive_routing_catalog',
  'description': 'Build a sanitized Adaptive Work Routing runtime catalog for the current '
                 'project.\n'
                 '\n'
                 'Returns provider-neutral worker candidates from project BYOM/local provider '
                 'configuration. Secrets, API keys, ciphertext, and endpoint credentials are never '
                 'returned; workers must use the server-side gateway for execution.',
  'inputSchema': {'type': 'object',
                  'properties': {'work_profile': {'type': 'object',
                                                  'description': 'Optional task profile from '
                                                                 'Adaptive Work Routing.'},
                                 'model_requirements': {'type': 'object',
                                                        'description': 'Optional provider-neutral '
                                                                       'worker requirements used '
                                                                       'to filter endpoint types.'},
                                 'include_disabled': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include disabled provider '
                                                                     'configs for diagnostics.'},
                                 'limit': {'type': 'integer',
                                           'default': 50,
                                           'minimum': 1,
                                           'maximum': 100,
                                           'description': 'Maximum number of sanitized candidates '
                                                          'to return.'}},
                  'required': []},
  'annotations': {'title': 'Build adaptive routing catalog',
                  'readOnlyHint': True,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False}},
 {'name': 'snipara_adaptive_routing_approve',
  'description': 'Approve or reject an Adaptive Work Routing recommendation through a direct MCP '
                 'coding-agent contract.\n'
                 '\n'
                 'Returns a project-scoped approval receipt that companion, orchestrator, and '
                 'gateway code can verify before treating delegated work as approved. This is not '
                 'a UI approval surface; it is intended for explicit coding-agent approval calls.',
  'inputSchema': {'type': 'object',
                  'properties': {'decision': {'type': 'string',
                                              'enum': ['approve', 'reject', 'needs_changes'],
                                              'default': 'approve',
                                              'description': 'Approval decision for the routed '
                                                             'work package.'},
                                 'idempotency_key': {'type': 'string',
                                                     'minLength': 8,
                                                     'maxLength': 160,
                                                     'description': 'Stable key supplied by the '
                                                                    'coding agent to make approval '
                                                                    'retries idempotent.'},
                                 'approval_subject': {'type': 'object',
                                                      'description': 'Optional structured routing '
                                                                     'recommendation, handoff, or '
                                                                     'task subject.'},
                                 'approval_subject_id': {'type': 'string',
                                                         'description': 'Optional stable subject '
                                                                        'identifier.'},
                                 'routing_recommendation_id': {'type': 'string',
                                                               'description': 'Optional routing '
                                                                              'recommendation '
                                                                              'identifier.'},
                                 'handoff_id': {'type': 'string',
                                                'description': 'Optional orchestrator or companion '
                                                               'handoff identifier.'},
                                 'routing_card': {'type': 'object',
                                                  'description': 'Optional routing card being '
                                                                 'approved.'},
                                 'approved_write_scope': {'type': 'array',
                                                          'items': {'type': 'string'},
                                                          'default': [],
                                                          'description': 'Exact write scopes '
                                                                         'approved for the worker. '
                                                                         'Empty means no writes '
                                                                         'approved.'},
                                 'approved_endpoint_types': {'type': 'array',
                                                             'items': {'type': 'string'},
                                                             'default': [],
                                                             'description': 'Endpoint types '
                                                                            'approved for this '
                                                                            'handoff, for example '
                                                                            'local or cloud.'},
                                 'max_cost_cents': {'type': 'integer',
                                                    'minimum': 0,
                                                    'maximum': 1000000,
                                                    'description': 'Optional per-approval cost '
                                                                   'ceiling in cents.'},
                                 'expires_at': {'type': 'string',
                                                'format': 'date-time',
                                                'description': 'Optional ISO timestamp after which '
                                                               'the approval must fail closed.'},
                                 'reason': {'type': 'string',
                                            'maxLength': 2000,
                                            'description': 'Short rationale for the approval '
                                                           'decision.'},
                                 'evidence_refs': {'type': 'array',
                                                   'items': {'type': 'string'},
                                                   'default': [],
                                                   'maxItems': 25,
                                                   'description': 'Evidence references used by the '
                                                                  'coding agent to approve or '
                                                                  'reject.'},
                                 'approver_agent_id': {'type': 'string',
                                                       'maxLength': 160,
                                                       'description': 'Stable coding-agent '
                                                                      'identifier supplied by the '
                                                                      'caller.'}},
                  'required': ['idempotency_key']},
  'annotations': {'title': 'Approve adaptive routing handoff',
                  'readOnlyHint': False,
                  'destructiveHint': False,
                  'idempotentHint': True,
                  'openWorldHint': False}},
 {'name': 'snipara_htask_create',
  'description': 'Create a hierarchical task at any level (N0-N3).\n'
                 '\n'
                 'Supports 4-level hierarchy: N0_INITIATIVE > N1_FEATURE > N2_WORKSTREAM > '
                 'N3_TASK.\n'
                 'Tasks have owners, priorities, acceptance criteria, and evidence requirements.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string',
                                              'description': 'Swarm ID. Optional when '
                                                             'auto_create_swarm is true.'},
                                 'auto_create_swarm': {'type': 'boolean',
                                                       'default': True,
                                                       'description': 'Create or reuse a default '
                                                                      'project swarm when swarm_id '
                                                                      'is omitted'},
                                 'swarm_name': {'type': 'string',
                                                'description': 'Project-scoped swarm name to '
                                                               'create or reuse when swarm_id is '
                                                               'omitted'},
                                 'swarm_description': {'type': 'string',
                                                       'description': 'Description for the '
                                                                      'auto-created swarm'},
                                 'swarm_max_agents': {'type': 'integer',
                                                      'default': 10,
                                                      'description': 'Max agents for the '
                                                                     'auto-created swarm'},
                                 'level': {'type': 'string',
                                           'enum': ['N0_INITIATIVE',
                                                    'N1_FEATURE',
                                                    'N2_WORKSTREAM',
                                                    'N3_TASK'],
                                           'default': 'N3_TASK',
                                           'description': 'Task hierarchy level'},
                                 'title': {'type': 'string', 'description': 'Task title'},
                                 'description': {'type': 'string',
                                                 'description': 'Task description'},
                                 'owner': {'type': 'string',
                                           'description': 'Task owner (required)'},
                                 'parent_id': {'type': 'string',
                                               'description': 'Parent task ID (required for '
                                                              'N1-N3)'},
                                 'priority': {'type': 'string',
                                              'enum': ['P0', 'P1', 'P2'],
                                              'default': 'P1',
                                              'description': 'Priority level'},
                                 'eta_target': {'type': 'string',
                                                'description': 'Target completion date (ISO '
                                                               'format)'},
                                 'execution_target': {'type': 'string',
                                                      'enum': ['LOCAL',
                                                               'CLOUD',
                                                               'HYBRID',
                                                               'EXTERNAL'],
                                                      'description': 'Where the task executes'},
                                 'workstream_type': {'type': 'string',
                                                     'enum': ['API',
                                                              'FRONTEND',
                                                              'QA',
                                                              'BUGFIX_HARDENING',
                                                              'DEPLOY_PROD_VERIFY',
                                                              'DATA',
                                                              'SECURITY',
                                                              'DOCUMENTATION',
                                                              'CUSTOM',
                                                              'OTHER'],
                                                     'description': 'Workstream type for N2 tasks'},
                                 'custom_workstream_type': {'type': 'string',
                                                            'description': 'Required label when '
                                                                           'workstream_type is '
                                                                           'CUSTOM'},
                                 'acceptance_criteria': {'type': 'array',
                                                         'items': {'type': 'object'},
                                                         'description': 'List of acceptance '
                                                                        'criteria [{id, text, '
                                                                        'checked}]'},
                                 'context_refs': {'type': 'array',
                                                  'items': {'type': 'string'},
                                                  'description': 'Context references (URLs, file '
                                                                 'paths)'},
                                 'context_query': {'type': 'string',
                                                   'description': 'Auto-fetch relevant docs via '
                                                                  'snipara_context_query and add '
                                                                  "to context_refs (e.g., 'JWT "
                                                                  "authentication patterns')"},
                                 'evidence_required': {'type': 'array',
                                                       'items': {'type': 'object'},
                                                       'description': 'Required evidence [{type, '
                                                                      'description}]'},
                                 'is_blocking': {'type': 'boolean',
                                                 'default': True,
                                                 'description': 'Whether task blocks parent '
                                                                'closure when failed/incomplete'}},
                  'required': ['title', 'description', 'owner']}},
 {'name': 'snipara_htask_create_feature',
  'description': 'Create a N1 feature with standard workstreams.\n'
                 '\n'
                 'Creates a feature (N1) with automatic N2 workstreams: API, FRONTEND, QA, '
                 'BUGFIX_HARDENING, DEPLOY_PROD_VERIFY.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string',
                                              'description': 'Swarm ID. Optional when '
                                                             'auto_create_swarm is true.'},
                                 'auto_create_swarm': {'type': 'boolean',
                                                       'default': True,
                                                       'description': 'Create or reuse a default '
                                                                      'project swarm when swarm_id '
                                                                      'is omitted'},
                                 'swarm_name': {'type': 'string',
                                                'description': 'Project-scoped swarm name to '
                                                               'create or reuse when swarm_id is '
                                                               'omitted'},
                                 'swarm_description': {'type': 'string',
                                                       'description': 'Description for the '
                                                                      'auto-created swarm'},
                                 'swarm_max_agents': {'type': 'integer',
                                                      'default': 10,
                                                      'description': 'Max agents for the '
                                                                     'auto-created swarm'},
                                 'title': {'type': 'string', 'description': 'Feature title'},
                                 'description': {'type': 'string',
                                                 'description': 'Feature description'},
                                 'owner': {'type': 'string', 'description': 'Feature owner'},
                                 'parent_id': {'type': 'string',
                                               'description': 'Optional N0 parent'},
                                 'create_initiative': {'type': 'boolean',
                                                       'default': False,
                                                       'description': 'Create an N0 initiative '
                                                                      'parent when parent_id is '
                                                                      'omitted'},
                                 'initiative_title': {'type': 'string',
                                                      'description': 'Optional title for the N0 '
                                                                     'initiative'},
                                 'initiative_description': {'type': 'string',
                                                            'description': 'Optional description '
                                                                           'for the N0 initiative'},
                                 'workstreams': {'type': 'array',
                                                 'items': {'type': 'string'},
                                                 'description': 'Standard workstream types or '
                                                                'custom labels to create (defaults '
                                                                'to standard set)'},
                                 'custom_workstreams': {'type': 'array',
                                                        'items': {'type': 'string'},
                                                        'description': 'Custom N2 workstream '
                                                                       'labels created as CUSTOM '
                                                                       'workstreams'},
                                 'workstream_owners': {'type': 'object',
                                                       'additionalProperties': {'type': 'string'},
                                                       'description': 'Map of workstream type or '
                                                                      'CUSTOM:<label> to owner'},
                                 'create_actionable_tasks': {'type': 'boolean',
                                                             'default': True,
                                                             'description': 'Create actionable N3 '
                                                                            'starter tasks under '
                                                                            'each N2 workstream'},
                                 'task_blueprints': {'type': 'object',
                                                     'description': 'Optional per-workstream N3 '
                                                                    'task blueprint overrides'}},
                  'required': ['title', 'description', 'owner']}},
 {'name': 'snipara_htask_get',
  'description': 'Get a hierarchical task with its children.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'include_children': {'type': 'boolean',
                                                      'default': True,
                                                      'description': 'Include direct children'}},
                  'required': ['swarm_id', 'task_id']}},
 {'name': 'snipara_htask_tree',
  'description': 'Get full hierarchical tree from a node.\n'
                 '\n'
                 'Returns recursive tree structure with all descendants up to max_depth.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string',
                                             'description': 'Root task ID (optional, defaults to '
                                                            'all roots)'},
                                 'max_depth': {'type': 'integer',
                                               'default': 4,
                                               'description': 'Maximum depth to traverse'},
                                 'include_archived': {'type': 'boolean',
                                                      'default': False,
                                                      'description': 'Include archived tasks'},
                                 'include_completed': {'type': 'boolean',
                                                       'default': True,
                                                       'description': 'Include completed and '
                                                                      'cancelled descendants in '
                                                                      'the tree'}},
                  'required': ['swarm_id']}},
 {'name': 'snipara_htask_update',
  'description': 'Update task fields (whitelist enforced by status).\n'
                 '\n'
                 'Different fields are updatable based on task status. Structural fields require '
                 'admin.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'updates': {'type': 'object', 'description': 'Fields to update'},
                                 'is_admin': {'type': 'boolean',
                                              'default': False,
                                              'description': 'Admin privileges for structural '
                                                             'updates'}},
                  'required': ['swarm_id', 'task_id', 'updates']}},
 {'name': 'snipara_htask_block',
  'description': 'Block a task with detailed payload.\n'
                 '\n'
                 'Requires blocker_type and blocker_reason. Automatically propagates to ancestors '
                 'if is_blocking=true.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'blocker_type': {'type': 'string',
                                                  'enum': ['TECH',
                                                           'DEPENDENCY',
                                                           'ACCESS',
                                                           'PRODUCT',
                                                           'INFRA',
                                                           'SECURITY',
                                                           'OTHER'],
                                                  'description': 'Type of blocker'},
                                 'blocker_reason': {'type': 'string',
                                                    'description': 'Detailed explanation'},
                                 'blocked_by_task_id': {'type': 'string',
                                                        'description': 'ID of blocking task'},
                                 'required_input': {'type': 'string',
                                                    'description': "What's needed to unblock"},
                                 'eta_recovery': {'type': 'string',
                                                  'description': 'Expected unblock date (ISO)'},
                                 'escalation_to': {'type': 'string',
                                                   'description': 'Who to escalate to'}},
                  'required': ['swarm_id', 'task_id', 'blocker_type', 'blocker_reason']}},
 {'name': 'snipara_htask_unblock',
  'description': 'Unblock a task and re-evaluate ancestor status.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'resolution': {'type': 'string',
                                                'description': 'How the blocker was resolved'}},
                  'required': ['swarm_id', 'task_id']}},
 {'name': 'snipara_htask_complete',
  'description': 'Complete an N3 task with evidence and optional memory creation.\n'
                 '\n'
                 'Evidence may be required based on policy. Use for leaf tasks (N3_TASK).\n'
                 'Automatically creates a linked memory with task outcome, learnings, and decision '
                 'impact.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'evidence': {'type': 'array',
                                              'items': {'type': 'object'},
                                              'description': 'Evidence list [{type, description, '
                                                             '...}]'},
                                 'result': {'type': 'object', 'description': 'Task result data'},
                                 'learnings': {'type': 'array',
                                               'items': {'type': 'string'},
                                               'description': 'Lessons learned from this task'},
                                 'decision_impact': {'type': 'string',
                                                     'description': 'How this task affects future '
                                                                    'decisions'},
                                 'work_profile': {'type': 'object',
                                                  'description': 'Optional Adaptive Work Routing '
                                                                 'work profile used for '
                                                                 'delegation.'},
                                 'model_requirements': {'type': 'object',
                                                        'description': 'Optional provider-neutral '
                                                                       'worker requirements used '
                                                                       'by routing.'},
                                 'routing_receipt': {'type': 'object',
                                                     'description': 'Optional worker cost/outcome '
                                                                    'receipt for quality-adjusted '
                                                                    'routing.'},
                                 'create_memory': {'type': 'boolean',
                                                   'default': True,
                                                   'description': 'Auto-create a memory with task '
                                                                  'outcome (default: true)'}},
                  'required': ['swarm_id', 'task_id']}},
 {'name': 'snipara_htask_verify_closure',
  'description': 'Verify if a parent task can be closed.\n'
                 '\n'
                 'Checks all children status against closure policy. Returns blockers and waiver '
                 'requirements.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'}},
                  'required': ['swarm_id', 'task_id']}},
 {'name': 'snipara_htask_close',
  'description': 'Close a parent task (with optional waiver).\n'
                 '\n'
                 'Use waiver_reason and waiver_approved_by when closing with exceptions (if policy '
                 'allows).',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'waiver_reason': {'type': 'string',
                                                   'description': 'Reason for waiver'},
                                 'waiver_approved_by': {'type': 'string',
                                                        'description': 'Who approved the waiver'}},
                  'required': ['swarm_id', 'task_id']}},
 {'name': 'snipara_htask_delete',
  'description': 'Delete a task (soft by default, hard with force flag).\n'
                 '\n'
                 'Soft delete archives the task. Hard delete removes permanently (requires policy '
                 '+ admin).',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'},
                                 'force': {'type': 'boolean',
                                           'default': False,
                                           'description': 'Hard delete (requires policy + admin)'},
                                 'cascade': {'type': 'boolean',
                                             'default': False,
                                             'description': 'Delete all descendants'},
                                 'is_admin': {'type': 'boolean',
                                              'default': False,
                                              'description': 'Admin privileges'}},
                  'required': ['swarm_id', 'task_id']}},
 {'name': 'snipara_htask_recommend_batch',
  'description': 'Get recommended batch of N3 tasks ready to work on.\n'
                 '\n'
                 'Returns prioritized list of unblocked, pending N3 tasks. Filter by feature_id or '
                 'workstream_type for focused recommendations.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'feature_id': {'type': 'string',
                                                'description': 'Filter to tasks under this N1 '
                                                               'feature'},
                                 'workstream_type': {'type': 'string',
                                                     'enum': ['API',
                                                              'FRONTEND',
                                                              'QA',
                                                              'BUGFIX_HARDENING',
                                                              'DEPLOY_PROD_VERIFY',
                                                              'DATA',
                                                              'SECURITY',
                                                              'DOCUMENTATION',
                                                              'CUSTOM',
                                                              'OTHER'],
                                                     'description': 'Filter to tasks in this '
                                                                    'workstream type'},
                                 'limit': {'type': 'integer',
                                           'default': 5,
                                           'description': 'Maximum tasks to return'},
                                 'owner': {'type': 'string', 'description': 'Filter by owner'},
                                 'exclude_blocked': {'type': 'boolean',
                                                     'default': True,
                                                     'description': 'Exclude blocked tasks'},
                                 'claim_for_agent': {'type': 'string',
                                                     'description': 'If set, atomically claim '
                                                                    'returned ready N3 tasks for '
                                                                    'this agent'}},
                  'required': ['swarm_id']}},
 {'name': 'snipara_htask_policy_get',
  'description': 'Get the htask policy configuration for a swarm.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'}},
                  'required': ['swarm_id']}},
 {'name': 'snipara_htask_policy_update',
  'description': 'Update the htask policy for a swarm.\n'
                 '\n'
                 'Admin-only fields: allowStructuralUpdate, allowHardDelete, compatMode.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'updates': {'type': 'object',
                                             'description': 'Policy fields to update'},
                                 'is_admin': {'type': 'boolean',
                                              'default': False,
                                              'description': 'Admin privileges'}},
                  'required': ['swarm_id', 'updates']}},
 {'name': 'snipara_htask_metrics',
  'description': 'Get comprehensive metrics for htasks in a swarm.\n'
                 '\n'
                 'Includes throughput, aging by level, blocked/recovered ratio, and top blockers.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'period_hours': {'type': 'integer',
                                                  'default': 24,
                                                  'description': 'Period for time-based metrics'}},
                  'required': ['swarm_id']}},
 {'name': 'snipara_htask_audit_trail',
  'description': 'Get complete audit trail for a specific task.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'task_id': {'type': 'string', 'description': 'Task ID'}},
                  'required': ['swarm_id', 'task_id']}},
 {'name': 'snipara_htask_checkpoint_delta',
  'description': 'Get delta report since last checkpoint.\n'
                 '\n'
                 'Returns events, closures, blocks since the specified timestamp.',
  'inputSchema': {'type': 'object',
                  'properties': {'swarm_id': {'type': 'string', 'description': 'Swarm ID'},
                                 'since': {'type': 'string',
                                           'description': 'ISO timestamp of last checkpoint'}},
                  'required': ['swarm_id', 'since']}}]

TOOL_DEFINITION_BY_NAME = {tool["name"]: tool for tool in TOOL_DEFINITIONS}


MCP_TOOL_NAMES = ['snipara_collaboration_status',
 'snipara_collaboration_start',
 'snipara_collaboration_claim',
 'snipara_collaboration_release',
 'snipara_collaboration_guard',
 'snipara_context_query',
 'snipara_ask',
 'snipara_search',
 'snipara_read',
 'snipara_code_callers',
 'snipara_code_imports',
 'snipara_code_neighbors',
 'snipara_code_shortest_path',
 'snipara_code_symbol_card',
 'snipara_code_impact',
 'snipara_local_code_overlay_upload',
 'snipara_local_code_overlay_status',
 'snipara_local_code_overlay_get',
 'snipara_local_code_overlay_retire',
 'snipara_decompose',
 'snipara_multi_query',
 'snipara_plan',
 'snipara_multi_project_query',
 'snipara_inject',
 'snipara_context',
 'snipara_clear_context',
 'snipara_stats',
 'snipara_sections',
 'snipara_settings',
 'snipara_help',
 'snipara_store_summary',
 'snipara_get_summaries',
 'snipara_delete_summary',
 'snipara_shared_context',
 'snipara_list_templates',
 'snipara_get_template',
 'snipara_list_collections',
 'snipara_create_collection',
 'snipara_get_collection_documents',
 'snipara_link_collection',
 'snipara_unlink_collection',
 'snipara_upload_shared_document',
 'snipara_list_business_collections',
 'snipara_ensure_business_collection',
 'snipara_upload_business_document',
 'snipara_list_client_projects',
 'snipara_create_client_project',
 'snipara_remember',
 'snipara_remember_if_novel',
 'snipara_end_of_task_commit',
 'snipara_remember_bulk',
 'snipara_recall',
 'snipara_resume_context',
 'snipara_memories',
 'snipara_forget',
 'snipara_memory_invalidate',
 'snipara_memory_attach_source',
 'snipara_memory_supersede',
 'snipara_memory_verify',
 'snipara_memory_review_queue',
 'snipara_memory_resolve_queue_item',
 'snipara_journal_append',
 'snipara_journal_get',
 'snipara_journal_summarize',
 'snipara_session_memories',
 'snipara_memory_compact',
 'snipara_session_bootstrap_status',
 'snipara_owner_profile_get',
 'snipara_owner_profile_update',
 'snipara_memory_health',
 'snipara_memory_duplicate_candidates',
 'snipara_memory_clean_candidates',
 'snipara_memory_daily_brief',
 'snipara_tenant_profile_create',
 'snipara_tenant_profile_get',
 'snipara_swarm_create',
 'snipara_swarm_delete',
 'snipara_swarm_join',
 'snipara_agent_profile_get',
 'snipara_agent_profile_update',
 'snipara_claim',
 'snipara_release',
 'snipara_state_get',
 'snipara_state_set',
 'snipara_state_poll',
 'snipara_broadcast',
 'snipara_swarm_events',
 'snipara_agent_status',
 'snipara_swarm_leave',
 'snipara_swarm_members',
 'snipara_swarm_update',
 'snipara_upload_document',
 'snipara_sync_documents',
 'snipara_document_tombstones',
 'snipara_svg_bundle_ingest',
 'snipara_request_access',
 'snipara_load_document',
 'snipara_load_project',
 'snipara_orchestrate',
 'snipara_repl_context',
 'snipara_get_chunk',
 'snipara_decision_create',
 'snipara_decision_query',
 'snipara_decision_supersede',
 'snipara_index_health',
 'snipara_index_recommendations',
 'snipara_reindex',
 'snipara_search_analytics',
 'snipara_query_trends',
 'snipara_adaptive_routing_catalog',
 'snipara_adaptive_routing_approve',
 'snipara_htask_create',
 'snipara_htask_create_feature',
 'snipara_htask_get',
 'snipara_htask_tree',
 'snipara_htask_update',
 'snipara_htask_block',
 'snipara_htask_unblock',
 'snipara_htask_complete',
 'snipara_htask_verify_closure',
 'snipara_htask_close',
 'snipara_htask_delete',
 'snipara_htask_recommend_batch',
 'snipara_htask_policy_get',
 'snipara_htask_policy_update',
 'snipara_htask_metrics',
 'snipara_htask_audit_trail',
 'snipara_htask_checkpoint_delta']

MCP_TOOL_NAME_SET = set(MCP_TOOL_NAMES)

MCP_TOOL_DEFINITIONS = [TOOL_DEFINITION_BY_NAME[name] for name in MCP_TOOL_NAMES if name in TOOL_DEFINITION_BY_NAME]

EXPOSED_TOOL_DEFINITIONS = [tool for tool in TOOL_DEFINITION_BY_NAME.values() if tool.get("exposed", True)]

EXPOSED_TOOL_NAMES = {tool["name"] for tool in EXPOSED_TOOL_DEFINITIONS}

TOOL_NAMES = {tool["name"] for tool in TOOL_DEFINITIONS}
