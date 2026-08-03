## halal-graphify

This project has a knowledge graph at graphify-out/ with hub nodes, community structure, and cross-file relationships.

When the user types `/halal-graphify`, use the installed halal-graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `halal-graphify query "<question>"` when graphify-out/graph.json exists. Use `halal-graphify path "<A>" "<B>"` for relationships and `halal-graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip halal-graphify. Only skip halal-graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `halal-graphify update .` to keep the graph current (AST-only, no API cost).
