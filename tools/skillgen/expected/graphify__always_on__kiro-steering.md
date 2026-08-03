---
inclusion: always
---

halal-graphify: A knowledge graph of this project lives in `graphify-out/`. For codebase, architecture, or dependency questions, when `graphify-out/graph.json` exists, first run `halal-graphify query "<question>"` (or `halal-graphify path "<A>" "<B>"` / `halal-graphify explain "<concept>"`). These return a scoped subgraph, usually much smaller than `GRAPH_REPORT.md` or raw grep output. Read `GRAPH_REPORT.md` only for broad architecture review or when those commands do not surface enough context.
