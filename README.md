> ### This is halal-graphify — an unofficial fork of [Graphify](https://github.com/Graphify-Labs/graphify)
>
> **The only change: what the original calls "god nodes" are called "hub nodes"
> here.** Nothing else differs — same analysis, same maths, same output, same
> commands. "Hub" is the standard graph-theory term for a highly connected
> vertex, so the name is arguably the more correct one anyway.
>
> Made for Muslims, and for anyone else who would rather their tools did not
> describe a piece of code that way. Everything else is upstream, tracked
> automatically and released in step with it.
>
> Not affiliated with or endorsed by Graphify Labs.
> Licensed under Apache-2.0. This is a modified version of the original work.

## Coming from the original Graphify?

**Your existing graphs keep working — you do not need to re-extract anything.**
Run this once inside a project you had already graphed:

```bash
halal-graphify migrate .
```

That rewrites the stale key inside `graphify-out/` so the reports read
correctly. It is offline, uses no AI and costs nothing, writes a `.bak` backup
beside every file it touches, and is safe to run twice — the second run just
says there is nothing to do.

If your own notes, READMEs or agent rules also mention the old wording, add
`--docs`:

```bash
halal-graphify migrate . --docs
```

That one **shows you every proposed change first and writes nothing until you
type `y`.** There is deliberately no flag to skip that confirmation: the tool
cannot tell your prose apart from a document that uses the word for entirely
unrelated and legitimate reasons, so you get the final say. Words that merely
contain the same letters — the Polish *tygodnie*, "Godot", "pagoda" — are
recognised and never touched.

On Windows you can also just double-click `migrate.bat` inside the project.

**What is *not* renamed, on purpose:** `graphify-out/`, `GRAPHIFY_OUT`,
`.graphifyignore` and `.graphifyinclude`. Those live in *your* project, so
leaving them alone means both tools read the same data and nothing you already
set up breaks.

<p align="center">
  <a href="https://graphify.com"><img src="https://raw.githubusercontent.com/Graphify-Labs/graphify/v8/docs/logo.png" width="300" height="140" alt="Graphify"/></a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/25296?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-25296" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/25296" alt="Graphify-Labs%2Fgraphify | Trendshift" width="250" height="55"/></a>
</p>

<div align="center">
<details><summary><b>Read this in other languages</b></summary>

🇺🇸 <a href="README.md">English</a> | 🇨🇳 <a href="docs/translations/README.zh-CN.md">简体中文</a> | 🇯🇵 <a href="docs/translations/README.ja-JP.md">日本語</a> | 🇰🇷 <a href="docs/translations/README.ko-KR.md">한국어</a> | 🇩🇪 <a href="docs/translations/README.de-DE.md">Deutsch</a> | 🇫🇷 <a href="docs/translations/README.fr-FR.md">Français</a> | 🇪🇸 <a href="docs/translations/README.es-ES.md">Español</a> | 🇮🇳 <a href="docs/translations/README.hi-IN.md">हिन्दी</a> | 🇧🇷 <a href="docs/translations/README.pt-BR.md">Português</a> | 🇷🇺 <a href="docs/translations/README.ru-RU.md">Русский</a> | 🇸🇦 <a href="docs/translations/README.ar-SA.md">العربية</a> | 🇮🇷 <a href="docs/translations/README.fa-IR.md">فارسی</a> | 🇮🇹 <a href="docs/translations/README.it-IT.md">Italiano</a> | 🇵🇱 <a href="docs/translations/README.pl-PL.md">Polski</a> | 🇳🇱 <a href="docs/translations/README.nl-NL.md">Nederlands</a> | 🇹🇷 <a href="docs/translations/README.tr-TR.md">Türkçe</a> | 🇺🇦 <a href="docs/translations/README.uk-UA.md">Українська</a> | 🇻🇳 <a href="docs/translations/README.vi-VN.md">Tiếng Việt</a> | 🇮🇩 <a href="docs/translations/README.id-ID.md">Bahasa Indonesia</a> | 🇸🇪 <a href="docs/translations/README.sv-SE.md">Svenska</a> | 🇬🇷 <a href="docs/translations/README.el-GR.md">Ελληνικά</a> | 🇷🇴 <a href="docs/translations/README.ro-RO.md">Română</a> | 🇨🇿 <a href="docs/translations/README.cs-CZ.md">Čeština</a> | 🇫🇮 <a href="docs/translations/README.fi-FI.md">Suomi</a> | 🇩🇰 <a href="docs/translations/README.da-DK.md">Dansk</a> | 🇳🇴 <a href="docs/translations/README.no-NO.md">Norsk</a> | 🇭🇺 <a href="docs/translations/README.hu-HU.md">Magyar</a> | 🇹🇭 <a href="docs/translations/README.th-TH.md">ภาษาไทย</a> | 🇺🇿 <a href="docs/translations/README.uz-UZ.md">Oʻzbekcha</a> | 🇹🇼 <a href="docs/translations/README.zh-TW.md">繁體中文</a> | 🇵🇭 <a href="docs/translations/README.fil-PH.md">Filipino</a> | 🇮🇱 <a href="docs/translations/README.he-IL.md">עברית</a>

</details>
</div>

<p align="center">
  <a href="https://pypi.org/project/halal-halal_graphify/"><img src="https://img.shields.io/pypi/v/halal-graphify" alt="PyPI"/></a>
  <a href="https://pepy.tech/project/halal-graphify"><img src="https://img.shields.io/pepy/dt/halal-graphify?color=blue&label=downloads" alt="Downloads"/></a>
  <a href="https://discord.gg/598Ad9zQZ"><img src="https://img.shields.io/badge/Discord-Join-5865F2?style=flat&logo=discord&logoColor=white" alt="Discord"/></a>
  <a href="https://www.linkedin.com/company/graphify-labs"><img src="https://img.shields.io/badge/LinkedIn-Graphify%20Labs-0077B5?logo=linkedin" alt="LinkedIn"/></a>
  <a href="https://www.ycombinator.com/companies/graphify-labs"><img src="https://img.shields.io/badge/Y%20Combinator-S26-F0652F?style=flat&logo=ycombinator&logoColor=white" alt="YC S26"/></a>
</p>

<p align="center">
  <b>Early access to the halal-graphify platform is open before the public v1 launch: <a href="https://app.graphify.com/login">app.graphify.com</a></b>
</p>

Type `/halal-graphify` in your AI coding assistant and it maps your entire project (code, docs, PDFs, images, videos) into a **knowledge graph** you can **query instead of grepping** through files.

- **Code maps for free, fully local.** Code is parsed with tree-sitter AST: deterministic, no LLM, nothing leaves your machine. (Docs, PDFs, images and video use your assistant's model, or a configured API key, for a semantic pass.)
- **Every edge is explained.** Each connection is tagged `EXTRACTED` (explicit in the source) or `INFERRED` (resolved by halal-graphify), so you can tell what was read directly from what was inferred.
- **Not a vector index.** No embeddings, no vector store: a real graph you traverse. Ask a question, trace the path between two things, or explain one concept.

> Want this always-on, updating in the background across your code, docs, and meetings rather than only on demand? That is what we are building at **[graphify.com](https://graphify.com)**, and early access is open now at **[app.graphify.com](https://app.graphify.com/login)**.

<p align="center">
  <img src="https://raw.githubusercontent.com/Graphify-Labs/graphify/v8/docs/graph-hero.png" alt="halal-graphify's interactive graph.html showing the FastAPI codebase as a force-directed knowledge graph with a legend of detected communities" width="900">
</p>
<p align="center">
  <em>The FastAPI codebase mapped by halal-graphify. Every node is a concept, colors are detected communities, and the whole thing is clickable in graph.html.</em>
</p>

**Get started** (30 seconds):

```bash
uv tool install halal-graphify      # install the CLI (or: pipx install halal-graphify)
halal-graphify install               # register the skill with your AI assistant
```

Then, in your AI assistant:

```
/halal-graphify .
```

That's it. You get **three files**:

```
graphify-out/
├── graph.html       open in any browser — click nodes, filter, search
├── GRAPH_REPORT.md  the highlights: key concepts, surprising connections, suggested questions
└── graph.json       the full graph — query it anytime without re-reading your files
```

**Works in** Claude Code, Cursor, Codex, Gemini CLI, GitHub Copilot, and 15+ more — [pick your platform](#install).

---

## See it in action

<p align="center">
  <img src="https://raw.githubusercontent.com/Graphify-Labs/graphify/v8/docs/demo-path.svg" alt="halal-graphify path query: a terminal asks for the shortest path between FastAPI and ModelField, and the answer lights up hop by hop across the knowledge graph" width="900">
</p>

Once the graph is built you query it instead of reading files. Real output, halal-graphify run on the FastAPI codebase shown above:

```text
$ halal-graphify explain "APIRouter"
Node: APIRouter
  Source:    routing.py L2210
  Community: 2
  Degree:    47

Connections (47):
  --> RequestValidationError [uses] [INFERRED]
  --> Dependant [uses] [INFERRED]
  --> .get() [method] [EXTRACTED]
  <-- __init__.py [imports] [EXTRACTED]
  ...

$ halal-graphify path "FastAPI" "ModelField"
Shortest path (3 hops):
  FastAPI --uses--> DefaultPlaceholder <--references-- get_request_handler() --references--> ModelField
```

Every edge carries a **confidence tag** (`EXTRACTED` = explicit in the source, `INFERRED` = derived by resolution), so you can tell what was read directly from what was inferred. `halal-graphify query "<question>"` returns a scoped subgraph for a plain-language question, and `halal-graphify path A B` traces how any two things connect.

---

## What it does

What you get out of the box:

| Capability | What you get |
|---|---|
| **Hub nodes** | The most-connected concepts, so you see what everything flows through |
| **Communities** | The graph split into subsystems (Leiden), with LLM-free labels |
| **Cross-file links** | `calls` / `imports` / `inherits` / `mixes_in` resolved across ~40 languages via tree-sitter AST |
| **Query, path, explain** | Ask a question, trace the path between two things, or explain one concept, all against `graph.json` |
| **Rationale + doc refs** | `# NOTE:` / `# WHY:` comments and ADR/RFC citations become first-class nodes linked to the code |
| **Beyond code** | Docs, PDFs, images, and video/audio all map into the same graph |
| **Local-first** | Code is parsed locally with tree-sitter (no LLM, nothing leaves your machine); only the semantic pass over docs/media calls a backend, and only if you configure one |

---

## Benchmarks

| Benchmark | Metric | halal-graphify | Field |
|---|---|---|---|
| LOCOMO (n=300) | recall@10 | **0.497** | mem0 0.048, supermemory 0.149 |
| LOCOMO (n=300) | QA accuracy | 45.3% | supermemory 49.7%, mem0 27.3% |
| LongMemEval-S (n=50) | QA accuracy | **76%** | tied with dense RAG |
| Graph build | LLM credits | **0** | per-token for most systems |

Every system ran on the same harness with the same model and budgets, scored by a judge blind-validated against a second judge (90.6% agreement, Cohen's kappa 0.81). Full per-system tables, the code-intelligence result, and reproduction commands: **[BENCHMARKS.md](./BENCHMARKS.md)**.

---

## Prerequisites

| Requirement | Minimum | Check | Install |
|---|---|---|---|
| Python | 3.10+ | `python --version` | [python.org](https://www.python.org/downloads/) |
| uv *(recommended)* | any | `uv --version` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| pipx *(alternative)* | any | `pipx --version` | `pip install pipx` |

**macOS quick install (Homebrew):**
```bash
brew install python@3.12 uv
```

**Windows quick install:**
```powershell
winget install astral-sh.uv
```

**Ubuntu/Debian:**
```bash
sudo apt install python3.12 python3-pip pipx
# or install uv:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Install

> **Official package:** The PyPI package is `halal-graphify` (double-y). Other `halal-graphify*` packages on PyPI are not affiliated. The CLI command is still `halal-graphify`.

**Step 1 — install the package:**

```bash
# Recommended (isolated env; if 'halal-graphify' isn't found after, run: uv tool update-shell):
uv tool install halal-graphify

# Alternatives:
pipx install halal-graphify
pip install halal-graphify  # may need PATH setup — see note below
```

**Step 2 — register the skill with your AI assistant:**

```bash
halal-graphify install
```

That's it. Open your AI assistant and type `/halal-graphify .`

To install the assistant skill into the current repository instead of your user
profile, add `--project`:

```bash
halal-graphify install --project
halal-graphify install --project --platform codex
```

Project-scoped installs write under the current directory, for example
`.claude/skills/halal-halal_graphify/SKILL.md` or `.agents/skills/halal-halal_graphify/SKILL.md` (plus a
`references/` sidecar the skill loads on demand), and
print a `git add` hint for files that can be committed.
Per-platform commands that support project-scoped installs accept the same flag,
for example `halal-graphify claude install --project` or `halal-graphify codex install --project`.

> **PowerShell note:** Use `halal-graphify .` not `/halal-graphify .` — the leading slash is a path separator in PowerShell.

> **`halal-graphify: command not found`?** `uv tool install` / `pipx install` put the `halal-graphify` command in their tool bin dir (`~/.local/bin`). If your shell can't find it right after install — common on a fresh macOS + zsh setup — that dir isn't on your `PATH` yet: run `uv tool update-shell` (or `pipx ensurepath`), then open a new terminal. With plain `pip`, add `~/.local/bin` (Linux) or `~/Library/Python/3.x/bin` (Mac) to your PATH, or run `python -m halal_graphify`.

> **Running with `uvx` / `uv tool run` instead of installing?** Name the package, not the command: `uvx --from halal-graphify halal-graphify install`. Plain `uvx halal-graphify …` fails (`No solution found … no versions of halal-graphify`) because `uv tool run` reads the first word as a *package*, and the package is `halal-graphify` — the `halal-graphify` command lives inside it.

> **Avoid `pip install` on Mac/Windows** if possible. The skill resolves Python at runtime from `graphify-out/.graphify_python`; if that points to a different environment than where `pip` installed the package, you'll get `ModuleNotFoundError: No module named 'halal-graphify'`. `uv tool install` and `pipx install` isolate the package in their own env and avoid this entirely.

> **Git hooks and uv tool / pipx:** `halal-graphify hook install` embeds the current interpreter path directly into the hook scripts at install time, so the post-commit hook fires correctly even in GUI git clients and CI runners where `~/.local/bin` is not on PATH. If you reinstall or upgrade halal-graphify, re-run `halal-graphify hook install` to refresh the embedded path.

> **Strict mode (Claude Code):** `halal-graphify install --project --strict` makes the assistant actually use the graph. The default install *nudges* it to run `halal-graphify query` before reading files; strict mode *blocks* the first raw source read of a session and redirects it to the graph, then reverts to the nudge (so it fires at most once per session and never gets stuck). Toggle at runtime with `GRAPHIFY_HOOK_STRICT=1`/`0`; the default install is unchanged (soft nudge).

<details>
<summary><b>Pick your platform</b> (20+ assistants, click to expand)</summary>

| Platform | Install command |
|----------|----------------|
| Claude Code (Linux/Mac) | `halal-graphify install` |
| Claude Code (Windows) | `halal-graphify install` (auto-detected) or `halal-graphify install --platform windows` |
| CodeBuddy | `halal-graphify install --platform codebuddy` |
| Codex | `halal-graphify install --platform codex` |
| OpenCode | `halal-graphify install --platform opencode` |
| Kilo Code | `halal-graphify install --platform kilo` |
| GitHub Copilot CLI | `halal-graphify install --platform copilot` |
| VS Code Copilot Chat | `halal-graphify vscode install` |
| Aider | `halal-graphify install --platform aider` |
| OpenClaw | `halal-graphify install --platform claw` |
| Factory Droid | `halal-graphify install --platform droid` |
| Trae | `halal-graphify install --platform trae` |
| Trae CN | `halal-graphify install --platform trae-cn` |
| Gemini CLI | `halal-graphify install --platform gemini` |
| Hermes | `halal-graphify install --platform hermes` |
| Kimi Code | `halal-graphify install --platform kimi` |
| Amp | `halal-graphify amp install` |
| Agent Skills (cross-framework) | `halal-graphify install --platform agents` (alias `--platform skills`) |
| Kiro IDE/CLI | `halal-graphify kiro install` |
| Pi coding agent | `halal-graphify install --platform pi` |
| Cursor | `halal-graphify cursor install` |
| Devin CLI | `halal-graphify devin install` |
| Google Antigravity | `halal-graphify antigravity install` |

Codex users also need `multi_agent = true` under `[features]` in `~/.codex/config.toml` for parallel extraction. CodeBuddy uses the same Agent tool and PreToolUse hook mechanism as Claude Code. Factory Droid uses the `Task` tool for parallel subagent dispatch. OpenClaw and Aider use sequential extraction (parallel agent support is still early on those platforms). Trae uses the Agent tool for parallel subagent dispatch and does **not** support `PreToolUse` hooks, so AGENTS.md is the always-on mechanism.

`--platform agents` (alias `--platform skills`) targets the generic cross-framework [Agent-Skills](https://github.com/anthropics/skills) locations: the spec's user-global `~/.agents/skills/` (read by `npx skills` and spec-compliant frameworks) for a global install, and `./.agents/skills/` for a project (`--project`) install. The bare `halal-graphify install` stays single-platform (Claude Code) by design — use the named `agents` platform when you want the skill discoverable by any framework that reads `.agents/skills`.

> Codex uses `$halal-graphify` instead of `/halal-graphify`.

</details>

<details>
<summary><b>Optional extras</b> (install only what you need)</summary>

| Extra | What it adds | Install |
|---|---|---|
| `pdf` | PDF extraction | `uv tool install "halal-graphify[pdf]"` |
| `office` | `.docx` and `.xlsx` support | `uv tool install "halal-graphify[office]"` |
| `google` | Google Sheets rendering | `uv tool install "halal-graphify[google]"` |
| `video` | Video/audio transcription (faster-whisper + yt-dlp) | `uv tool install "halal-graphify[video]"` |
| `mcp` | MCP stdio server | `uv tool install "halal-graphify[mcp]"` |
| `neo4j` | Neo4j push support | `uv tool install "halal-graphify[neo4j]"` |
| `falkordb` | FalkorDB push support | `uv tool install "halal-graphify[falkordb]"` |
| `svg` | SVG graph export | `uv tool install "halal-graphify[svg]"` |
| `leiden` | Leiden community detection (Python < 3.13 only) | `uv tool install "halal-graphify[leiden]"` |
| `ollama` | Ollama local inference | `uv tool install "halal-graphify[ollama]"` |
| `openai` | OpenAI / OpenAI-compatible APIs | `uv tool install "halal-graphify[openai]"` |
| `gemini` | Google Gemini API | `uv tool install "halal-graphify[gemini]"` |
| `anthropic` | Anthropic Claude API (`--backend claude`, uses `ANTHROPIC_API_KEY`) | `uv tool install "halal-graphify[anthropic]"` |
| `bedrock` | AWS Bedrock (uses IAM, no API key) | `uv tool install "halal-graphify[bedrock]"` |
| `azure` | Azure OpenAI Service (`--backend azure`, uses `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT`) | `uv tool install "halal-graphify[openai]"` |
| `sql` | SQL schema extraction | `uv tool install "halal-graphify[sql]"` |
| `postgres` | Live PostgreSQL introspection (`--postgres DSN`) | `uv tool install "halal-graphify[postgres]"` |
| `dm` | BYOND DreamMaker `.dm`/`.dme` AST extraction (may need a C compiler + `python3-dev` if no wheel matches your platform) | `uv tool install "halal-graphify[dm]"` |
| `terraform` | Terraform / HCL `.tf`/`.tfvars`/`.hcl` AST extraction | `uv tool install "halal-graphify[terraform]"` |
| `pascal` | Pascal / Delphi `.pas`/`.dpr`/`.dpk`/`.inc` AST extraction (more accurate `calls`/`inherits` edges; falls back to a regex extractor when absent) | `uv tool install "halal-graphify[pascal]"` |
| `godot` | Godot GDScript `.gd` AST extraction (`.tscn`/`.tres` scene files are parsed without it) | `uv tool install "halal-graphify[godot]"` |
| `chinese` | Chinese query segmentation (jieba) | `uv tool install "halal-graphify[chinese]"` |
| `all` | Everything above | `uv tool install "halal-graphify[all]"` |

</details>

---

## Make your assistant always use the graph

Run this once in your project after building a graph:

| Platform | Command |
|----------|---------|
| Claude Code | `halal-graphify claude install` |
| CodeBuddy | `halal-graphify codebuddy install` |
| Codex | `halal-graphify codex install` |
| OpenCode | `halal-graphify opencode install` |
| Kilo Code | `halal-graphify kilo install` |
| GitHub Copilot CLI | `halal-graphify copilot install` |
| VS Code Copilot Chat | `halal-graphify vscode install` |
| Aider | `halal-graphify aider install` |
| OpenClaw | `halal-graphify claw install` |
| Factory Droid | `halal-graphify droid install` |
| Trae | `halal-graphify trae install` |
| Trae CN | `halal-graphify trae-cn install` |
| Cursor | `halal-graphify cursor install` |
| Gemini CLI | `halal-graphify gemini install` |
| Hermes | `halal-graphify hermes install` |
| Kimi Code | `halal-graphify install --platform kimi` |
| Amp | `halal-graphify amp install` |
| Agent Skills (cross-framework) | `halal-graphify agents install` (alias `halal-graphify skills install`) |
| Kiro IDE/CLI | `halal-graphify kiro install` |
| Pi coding agent | `halal-graphify pi install` |
| Devin CLI | `halal-graphify devin install` |
| Google Antigravity | `halal-graphify antigravity install` |

This writes a small config file that tells your assistant to consult the knowledge graph for codebase questions, preferring scoped queries like `halal-graphify query "<question>"` over reading the full report or grepping raw files.

- **Hook platforms** (Claude Code, Gemini CLI): a hook fires automatically before search-style tool calls (and, on Claude Code, before reading source files one by one via the Read/Glob tools) and nudges your assistant toward the graph path.
- **Instruction-file platforms** (Codex, OpenCode, Cursor, etc.): persistent instruction files (`AGENTS.md`, `.cursor/rules/`, etc.) provide the same query-first guidance.

`GRAPH_REPORT.md` is still available for broad architecture review.

**CodeBuddy** does the same two things as Claude Code: writes a `CODEBUDDY.md` section telling CodeBuddy to read `graphify-out/GRAPH_REPORT.md` before answering architecture questions, and installs `PreToolUse` hooks (`.codebuddy/settings.json`) that fire before Bash search commands and file reads, nudging toward `halal-graphify query` instead.

**Codex** writes to `AGENTS.md`, which is what actually carries the always-on graph guidance on this platform. `halal-graphify codex install` also registers a `PreToolUse` hook in `.codex/hooks.json` (`halal-graphify hook-check`), but that entry is deliberately a **no-op**: Codex Desktop rejects `hookSpecificOutput.additionalContext` on `PreToolUse`, so emitting a nudge there would break Bash tool calls. Unlike Claude Code, where the hook (`halal-graphify hook-guard`) does the nudging, on Codex the hook fires and intentionally does nothing, and `AGENTS.md` is the always-on mechanism.

**Kilo Code** installs the Graphify skill to `~/.config/kilo/skills/halal-halal_graphify/SKILL.md` and a native `/halal-graphify` command to `~/.config/kilo/command/graphify.md`. `halal-graphify kilo install` also writes `AGENTS.md` plus a native `tool.execute.before` plugin (`.kilo/plugins/graphify.js` + `.kilo/kilo.json` or `.kilo/kilo.jsonc` registration) so Kilo gets the same always-on graph reminder behavior through native `.kilo` config.

**Cursor** writes `.cursor/rules/halal-graphify.mdc` with `alwaysApply: true`, so Cursor includes it in every conversation automatically, no hook needed.

To remove halal-graphify from all platforms at once: `halal-graphify uninstall` (add `--purge` to also delete `graphify-out/`). Or use the per-platform command (e.g. `halal-graphify claude uninstall`).

---

## What's in the report

- **Hub nodes** — the most-connected concepts in your project. Everything flows through these.
- **Surprising connections** — links between things that live in different files or modules. Ranked by how unexpected they are.
- **The "why"** — inline comments (`# NOTE:`, `# WHY:`, `# HACK:`), docstrings, and design rationale from docs are extracted as separate nodes linked to the code they explain.
- **Suggested questions** — 4–5 questions the graph is uniquely positioned to answer.
- **Confidence tags** — every inferred relationship is marked `EXTRACTED`, `INFERRED`, or `AMBIGUOUS`. You always know what was found vs guessed.

---

## What files it handles

| Type | Extensions |
|------|-----------|
| Code (36 tree-sitter grammars) | `.py .ts .mts .cts .js .jsx .tsx .mjs .go .rs .java .c .cpp .cc .cxx .h .hpp .cu .cuh .metal .rb .cs .kt .kts .scala .php .swift .lua .luau .toc .zig .ps1 .psm1 .psd1 .ex .exs .m .mm .jl .vue .svelte .astro .groovy .gradle .dart .v .sv .svh .sql .f .f90 .f95 .f03 .f08 .pas .pp .dpr .dpk .lpr .inc .dfm .lfm .lpk .sh .bash .json .dm .dme .dmi .dmm .dmf .sln .slnx .csproj .fsproj .vbproj .xaml .razor .cshtml` (`.dm`/`.dme` requires `uv tool install halal-graphify[dm]`; `.mts`/`.cts` reuse the TypeScript grammar, `.cc`/`.cxx` and CUDA `.cu`/`.cuh` and Metal `.metal` reuse the C++ grammar) |
| Salesforce Apex | `.cls .trigger` (regex-based; classes, interfaces, enums, methods, triggers, SOQL/DML edges) |
| Terraform / HCL | `.tf .tfvars .hcl` (requires `uv tool install halal-graphify[terraform]`) |
| Godot / GDScript | `.gd` (classes, functions, signals, `extends`, `preload`/`load`, `emit`/`connect`; requires `uv tool install halal-graphify[godot]`) and `.tscn .tres` scene/resource files (script bindings and instanced scenes, no extra needed) |
| MCP configs | `.mcp.json` `mcp.json` `mcp_servers.json` `claude_desktop_config.json` — extracts server nodes, package refs, env var requirements |
| Package manifests | `apm.yml` `pyproject.toml` `go.mod` `pom.xml` — one canonical package node per package (by name) plus `depends_on` edges, so a package referenced from many manifests is a single hub |
| Docs | `.md .mdx .qmd .html .txt .rst .yaml .yml` (markdown `[text](./other.md)` links and `[[wikilinks]]` become `references` edges between docs) |
| Office | `.docx .xlsx` (requires `uv tool install halal-graphify[office]`) |
| Google Workspace | `.gdoc .gsheet .gslides` (opt-in; requires `gws` auth and `--google-workspace`; Sheets need `uv tool install halal-graphify[google]`) |
| PDFs | `.pdf` |
| Images | `.png .jpg .webp .gif` |
| Video / Audio | `.mp4 .mov .mp3 .wav` and more (requires `uv tool install halal-graphify[video]`) |
| YouTube / URLs | any video URL (requires `uv tool install halal-graphify[video]`) |

Code is extracted **locally with no API calls** (AST via tree-sitter). Everything else goes through your AI assistant's model API.

Google Drive for desktop `.gdoc`, `.gsheet`, and `.gslides` files are shortcut
pointers, not document content. To include native Google Docs, Sheets, and Slides
in a headless extraction, install and authenticate the
[`gws` CLI](https://github.com/googleworkspace/cli), then run:

```bash
uv tool install "halal-graphify[google]"  # needed for Google Sheets table rendering
gws auth login -s drive
halal-graphify extract ./docs --google-workspace
```

You can also set `GRAPHIFY_GOOGLE_WORKSPACE=1`. Graphify exports shortcuts into
`graphify-out/converted/` as Markdown sidecars, then extracts those files.

---

## Common commands

```bash
/halal-graphify .                        # build graph for current folder
/halal-graphify ./docs --update          # re-extract only changed files
/halal-graphify . --cluster-only         # rerun clustering without re-extracting
/halal-graphify . --cluster-only --resolution 1.5      # more granular communities
/halal-graphify . --cluster-only --exclude-hubs 99     # suppress utility super-hubs from hub-node rankings
/halal-graphify . --no-viz               # skip the HTML, just the report + JSON
/halal-graphify . --wiki                 # build a markdown wiki from the graph
halal-graphify export callflow-html      # Mermaid architecture/call-flow HTML (auto-regenerates on every git commit if hook is installed)

/halal-graphify query "what connects auth to the database?"
/halal-graphify path "UserService" "DatabasePool"
/halal-graphify explain "RateLimiter"

/halal-graphify add https://arxiv.org/abs/1706.03762   # fetch a paper and add it
/halal-graphify add <youtube-url>                       # transcribe and add a video

halal-graphify hook install              # auto-rebuild on git commit
halal-graphify merge-graphs a.json b.json              # combine two graphs

halal-graphify prs                       # PR dashboard: CI state, review status, worktree mapping
halal-graphify prs 42                    # deep dive on PR #42 with graph impact
halal-graphify prs --triage              # AI ranks your review queue (uses whatever backend is configured)
halal-graphify prs --conflicts           # PRs sharing graph communities — merge-order risk
```

See the [full command reference](#full-command-reference) below.

---

## Ignoring files

Create a `.graphifyignore` in your project root — same syntax as `.gitignore`, including `!` negation.

**`.gitignore` is respected automatically.** halal-graphify reads the `.gitignore` in each directory. If a `.graphifyignore` is also present, the two are **merged** — `.graphifyignore` patterns are evaluated last, so they win on conflicts (including `!` negations). Adding a `.graphifyignore` only ever excludes more; it never re-includes a file your `.gitignore` already excluded. Subdirectory scoping works the same way as git — an ignore file only affects its own subtree.

Pass `--no-gitignore` to `halal-graphify extract` when git-ignored generated or transpiled code belongs in the graph. This disables `.gitignore` and `.git/info/exclude`; `.graphifyignore` still applies.

```
# .graphifyignore
node_modules/
dist/
*.generated.py

# only index src/, ignore everything else
*
!src/
!src/**
```

---

## Team setup

`graphify-out/` is meant to be committed to git so everyone on the team starts with a map.

**Recommended `.gitignore` additions:**
```
graphify-out/cost.json        # local only
# graphify-out/cache/         # optional: commit for speed, skip to keep repo small
```

> `manifest.json` is now portable — keys are stored as relative paths and re-anchored on load, so committing it is safe and avoids a full rebuild on first checkout.

**Workflow:**
1. One person runs `/halal-graphify .` and commits `graphify-out/`.
2. Everyone pulls — their assistant reads the graph immediately.
3. Run `halal-graphify hook install` to auto-rebuild after each commit (AST only, no API cost). This also sets up a git merge driver so `graph.json` is never left with conflict markers — two devs committing in parallel get their graphs union-merged automatically.
4. When docs or papers change, run `/halal-graphify --update` to refresh those nodes.

---

## Using the graph directly

```bash
# query the graph from the terminal
halal-graphify query "show the auth flow"
halal-graphify query "what connects DigestAuth to Response?" --graph graphify-out/graph.json

# expose the graph as an MCP server (for repeated tool-call access)
python -m halal_graphify.serve graphify-out/graph.json
python -m halal_graphify.serve --graph graphify-out/graph.json  # --graph flag also accepted

# register with Kimi Code:
kimi mcp add --transport stdio halal-graphify -- python -m halal_graphify.serve graphify-out/graph.json

# or serve over HTTP so a whole team points at one URL (no local halal-graphify needed):
python -m halal_graphify.serve graphify-out/graph.json --transport http --port 8080
python -m halal_graphify.serve graphify-out/graph.json --transport http --host 0.0.0.0 --api-key "$SECRET"
```

The MCP server gives your assistant structured access: `query_graph`, `get_node`, `get_neighbors`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`.

### Shared HTTP server

`--transport stdio` (the default) spawns one local server per developer. `--transport http` serves the same tools over the MCP Streamable HTTP transport, so a single shared process can serve the graph for the whole team — clients point their IDE MCP config at `http://<host>:8080/mcp` instead of running halal-graphify locally.

| Flag | Default | Purpose |
|---|---|---|
| `--transport {stdio,http}` | `stdio` | Transport to serve on |
| `--host` | `127.0.0.1` | HTTP bind host (use `0.0.0.0` to expose beyond localhost) |
| `--port` | `8080` | HTTP bind port |
| `--api-key` | env `GRAPHIFY_API_KEY` | Require `Authorization: Bearer <key>` (or `X-API-Key`) |
| `--path` | `/mcp` | HTTP mount path |
| `--json-response` | off | Return plain JSON instead of SSE streams |
| `--stateless` | off | No per-session state (for load-balanced / CI deployments) |
| `--session-timeout` | `3600` | Reap idle stateful sessions after N seconds (`0` disables) |

The default `127.0.0.1` bind is loopback-only. Set `--host 0.0.0.0` **and** `--api-key` together when exposing on a shared host. Run it in a container:

```bash
docker build -t halal-graphify .
docker run -p 8080:8080 -v "$(pwd)/graphify-out:/data" halal-graphify \
  /data/graph.json --transport http --host 0.0.0.0 --api-key "$SECRET"
```

> **WSL / Linux note:** Ubuntu ships `python3`, not `python`. Use a venv to avoid conflicts:
> ```bash
> python3 -m venv .venv && .venv/bin/pip install "halal-graphify[mcp]"
> ```

---

## Environment variables

These are only needed for **headless / CI extraction** (`halal-graphify extract`). When running via the `/halal-graphify` skill inside your IDE, the model API is provided by your IDE session — no extra keys needed.

| Variable | Used for | When required |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude (Anthropic) backend | `--backend claude` |
| `ANTHROPIC_BASE_URL` | Anthropic-compatible endpoint URL (LiteLLM proxy, gateways, ...) | `--backend claude` (default: `https://api.anthropic.com`) |
| `ANTHROPIC_MODEL` | Model name for the Claude backend — for custom endpoints, use the model name/alias your server exposes | `--backend claude` (default: `claude-sonnet-4-6`) |
| `GEMINI_API_KEY` or `GOOGLE_API_KEY` | Google Gemini backend | `--backend gemini` |
| `OPENAI_API_KEY` | OpenAI or OpenAI-compatible APIs | `--backend openai` (local servers accept any non-empty value) |
| `OPENAI_BASE_URL` | OpenAI-compatible server URL (llama.cpp, vLLM, LM Studio, ...) | `--backend openai` (default: `https://api.openai.com/v1`) |
| `OPENAI_MODEL` | Model name for the OpenAI backend — for self-hosted servers, use the model name/alias your server exposes (check its `/v1/models` endpoint), e.g. `LFM2.5-8B-A1B-UD-Q4_K_XL` for llama.cpp | `--backend openai` (default: `gpt-4.1-mini`) |
| `DEEPSEEK_API_KEY` | DeepSeek backend | `--backend deepseek` |
| `MOONSHOT_API_KEY` | Kimi Code backend | `--backend kimi` |
| `OLLAMA_BASE_URL` | Ollama local inference URL | `--backend ollama` (default: `http://localhost:11434`) |
| `OLLAMA_MODEL` | Ollama model name | `--backend ollama` (default: auto-detect) |
| `GRAPHIFY_OLLAMA_NUM_CTX` | Override Ollama KV-cache window size | optional — auto-sized by default |
| `GRAPHIFY_OLLAMA_KEEP_ALIVE` | Minutes to keep Ollama model loaded | optional — set `0` to unload after each chunk |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI Service backend | `--backend azure` |
| `AZURE_OPENAI_ENDPOINT` | Azure resource endpoint URL | `--backend azure` (required alongside API key) |
| `AZURE_OPENAI_API_VERSION` | Azure API version override | optional — default `2024-12-01-preview` |
| `AZURE_OPENAI_DEPLOYMENT` or `GRAPHIFY_AZURE_MODEL` | Azure deployment name | optional — default `gpt-4o` |
| `AWS_*` / `~/.aws/credentials` | AWS Bedrock — standard credential chain | `--backend bedrock` (no API key, uses IAM) |
| `GRAPHIFY_MAX_WORKERS` | AST parallelism thread count | optional — also `--max-workers` flag |
| `GRAPHIFY_MAX_OUTPUT_TOKENS` | Raise output cap for dense corpora | optional — e.g. `32768` for large files |
| `GRAPHIFY_API_TIMEOUT` | Per-call timeout in seconds for HTTP, claude-cli, Anthropic SDK, and Bedrock backends (default: 600) | optional — also `--api-timeout` flag |
| `GRAPHIFY_MAX_RETRIES` | How many times to retry a rate-limited (429) request before giving up (default: 6; honors `Retry-After`) | optional — raise for strict per-org limits (e.g. kimi); `0` disables |
| `GRAPHIFY_FORCE` | Force graph rebuild even with fewer nodes | optional — also `--force` flag |
| `GRAPHIFY_GOOGLE_WORKSPACE` | Auto-enable Google Workspace export | optional — set to `1` |
| `GRAPHIFY_TRIAGE_BACKEND` | Backend for `halal-graphify prs --triage` | optional — auto-detected from available keys |
| `GRAPHIFY_TRIAGE_MODEL` | Model override for triage | optional — e.g. `claude-opus-4-7` |
| `GRAPHIFY_QUERY_LOG_ENABLE` | Set to `1` to turn on the local query log at `~/.cache/graphify-queries.log` (records each query/path/explain question + corpus path). Off by default — nothing is written unless you opt in (#1797) | optional |
| `GRAPHIFY_QUERY_LOG` | Enable the query log and write it to this path instead of the default | optional — off unless this or `_ENABLE` is set |
| `GRAPHIFY_QUERY_LOG_DISABLE` | Set to `1` to force the query log off (wins over the enable vars) | optional |
| `GRAPHIFY_QUERY_LOG_RESPONSES` | When the log is enabled, also record full subgraph responses (off by default) | optional |
| `GRAPHIFY_MAX_GRAPH_BYTES` | Override the 512 MiB graph.json size cap — e.g. `700MB`, `2GB`, or plain bytes | optional — useful for very large corpora |
| `GRAPHIFY_MAX_CONTEXTS` | Maximum number of non-default project graphs retained by one multi-project MCP server | optional — default: `8`; invalid values use `8`, and values below `1` use `1` |
| `GRAPHIFY_LLM_TEMPERATURE` | Override LLM temperature for semantic extraction — e.g. `0.7`, or `none` to omit | optional — auto-omitted for o1/o3/o4/gpt-5 reasoning models |

---

## Privacy

- **Code files** — processed locally via tree-sitter. Nothing leaves your machine. A code-only corpus requires no API key — `halal-graphify extract` runs fully offline. On a mixed repo, add `--code-only` to index just the code and skip the docs/PDFs/images that would otherwise need an LLM.
- **Video / audio** — transcribed locally with faster-whisper. Nothing leaves your machine.
- **Docs, PDFs, images** — sent to your AI assistant for semantic extraction (via the `/halal-graphify` skill, using whatever model your IDE session runs). Headless `halal-graphify extract` requires `GEMINI_API_KEY` / `GOOGLE_API_KEY` (Gemini), `MOONSHOT_API_KEY` (Kimi), `ANTHROPIC_API_KEY` (Claude), `OPENAI_API_KEY` (OpenAI), `DEEPSEEK_API_KEY` (DeepSeek), a running Ollama instance (`OLLAMA_BASE_URL`), AWS credentials via the standard provider chain (Bedrock - no API key needed, uses IAM), or the `claude` CLI binary (Claude Code - no API key needed, uses your Claude subscription). The `--dedup-llm` flag uses the same key.
- **Data residency** — `halal-graphify extract` auto-detects which provider to use based on which API key is set (priority: Gemini → Kimi → Claude → OpenAI → DeepSeek → Azure → Bedrock → Ollama). For code with data-residency requirements, use `--backend ollama` (fully local) or pass an explicit `--backend` flag. Kimi (`MOONSHOT_API_KEY`) routes to Moonshot AI servers in China.
- **No telemetry**, no usage tracking, no analytics.
- **Query logging** — every `halal-graphify query`, `halal-graphify path`, `halal-graphify explain`, and MCP `query_graph` call is logged to `~/.cache/graphify-queries.log` in JSON Lines format (timestamp, question, corpus, nodes returned, duration). Full subgraph responses are **not** stored by default. Set `GRAPHIFY_QUERY_LOG_DISABLE=1` to opt out, or `GRAPHIFY_QUERY_LOG=/dev/null` to silence without disabling the code path.

---

## Troubleshooting

**`halal-graphify: command not found` after installing**
The CLI is installed but its bin directory isn't on your shell's `PATH`. Pick the fix for how you installed:
- **uv** (`uv tool install halal-graphify`): the command lands in uv's tool bin dir (`~/.local/bin`), which a fresh macOS/zsh setup often doesn't have on `PATH`. Run `uv tool update-shell`, then open a new terminal. (Find the dir with `uv tool dir --bin`.)
- **pipx** (`pipx install halal-graphify`): run `pipx ensurepath`, then open a new terminal.
- **pip** (`pip install halal-graphify`): pip installs scripts to a user bin dir that may not be on `PATH` — add `~/Library/Python/3.x/bin` (macOS) or `~/.local/bin` (Linux) to your `PATH` in `~/.zshrc`/`~/.bashrc`, or just run `python -m halal_graphify`.

**`uvx halal-graphify …` or `uv tool run halal-graphify …` fails to resolve `halal-graphify`**
The PyPI package is `halal-graphify`; `halal-graphify` is only the command it provides. `uv tool run` treats the first word as a *package name*, so it looks for a package called `halal-graphify` and reports `No solution found … no versions of halal-graphify`. Name the package explicitly: `uvx --from halal-graphify halal-graphify install` (same as `uv tool run --from halal-graphify halal-graphify install`). Or `uv tool install halal-graphify` once and then call `halal-graphify` directly.

**`uv run --with halal-graphify python -m halal_graphify` silently runs an older install**
`uv run` uses your *system* Python, so if an older `halal-graphify` also lives there (e.g. a past `pip install halal-graphify`), Python can find that copy first on `sys.path` and `--with halal-graphify` won't override it. It runs with no error, but you get the *old* version's behavior — e.g. env overrides like `OPENAI_BASE_URL` are silently ignored, so requests hit the default endpoint and fail with a 401 that looks like a bad key. The fingerprint is a `warning: skill is from halal_graphify <newer>, package is <older>` line — that means a different install was loaded, not just a stale skill. Check which copy actually loaded:
```bash
python -c "import halal_graphify; print(halal_graphify.__file__)"
```
Then run the installed command directly (it uses the uv-managed copy), or drop the stale system copy:
```bash
uvx --from halal-graphify halal-graphify extract . --backend openai   # names the package explicitly
pip uninstall halal-graphify                                    # or remove the old system install
```

**`python -m halal_graphify` works but `halal-graphify` command doesn't**
Your shell's `PATH` doesn't include the bin directory the command was installed to. Prefer `uv tool install` / `pipx install` over plain `pip`, then run `uv tool update-shell` / `pipx ensurepath` and open a new terminal (see the install notes above).

**`/halal-graphify .` causes "path not recognized" in PowerShell**
PowerShell treats a leading `/` as a path separator. Use `halal-graphify .` (no slash) on Windows.

**Graph has fewer nodes after `--update` or rebuild**
If a refactor deleted files, the old nodes linger. Pass `--force` (or set `GRAPHIFY_FORCE=1`) to overwrite even when the rebuild has fewer nodes.

**`extract` exits with "extraction was incomplete ... refusing to overwrite"**
When an extraction pass crashes or a walk can't fully read the corpus, the run would be smaller than a complete one, so `halal-graphify extract` refuses to overwrite a larger existing graph with the partial result (protecting your `graph.json`). Fix the underlying failure and re-run, or pass `--allow-partial` to overwrite anyway.

**Graph has duplicate nodes for the same entity (ghost duplicates)**
Ghost duplicates (same symbol appearing twice — once from AST extraction with a source location, once from semantic extraction without) are now automatically merged at build time. If you see this in a graph built before v0.8.33, run a full re-extract to clean up:
```bash
halal-graphify extract . --force
```

**Ollama runs out of VRAM / context window exceeded**
The KV-cache window is auto-sized but may be too large for your GPU. Reduce it:
```bash
GRAPHIFY_OLLAMA_NUM_CTX=8192 halal-graphify extract ./docs --backend ollama --token-budget 4000
```

**`LLM returned invalid JSON` / `Unterminated string` warnings**
The model's JSON response hit its output-token limit and was cut off mid-string. halal-graphify auto-recovers (it splits the chunk and re-extracts the halves, and an oversized single document is first sliced at heading/paragraph boundaries so the whole file is still covered), so these warnings are noisy but not data loss. To reduce the churn, raise the output cap or shrink each chunk's output:
```bash
GRAPHIFY_MAX_OUTPUT_TOKENS=16384 halal-graphify extract . --mode deep   # lift the cap
halal-graphify extract . --mode deep --token-budget 4000                # smaller input chunks -> smaller output
```
With a cloud gateway like OpenRouter, prefer `--backend openai` (set `OPENAI_BASE_URL`) over the Ollama shim — it's a cleaner OpenAI-compatible path. If the model has its own max-output ceiling, lowering `--token-budget` is the reliable lever.

**Graph HTML is too large to open in a browser (>5000 nodes)**
Skip HTML generation and use the JSON directly:
```bash
halal-graphify cluster-only ./my-project --no-viz
halal-graphify query "..."
```

**`graph.json` has conflict markers after two devs commit at once**
Run `halal-graphify hook install` — it sets up a git merge driver that union-merges `graph.json` automatically so conflicts never happen.

**Extraction returns empty nodes/edges for docs or PDFs**
Docs, PDFs, and images require an LLM call — code-only corpora need no key. Check that your API key is set and the backend is correct:
```bash
ANTHROPIC_API_KEY=sk-... halal-graphify extract ./docs --backend claude
```

**Skill version mismatch warning in your IDE**
Your installed halal-graphify version is different from the skill file. Update:
```bash
uv tool upgrade halal-graphify
halal-graphify install  # overwrites the skill file
```

**Claude Code prompt cache invalidated after every `halal-graphify extract`**
Graphify writes output files (`graph.json`, `graphify-out/`) into the workspace. If those paths aren't ignored, every write invalidates Claude Code's prompt cache, forcing a full re-upload at cache-write rates on the next turn. Add them to `.claudeignore`:
```text
# .claudeignore
graph.json
graphify-out/
```

---

## Full command reference

```
/halal-graphify                          # run on current directory
/halal-graphify ./raw                    # run on a specific folder
/halal-graphify ./raw --mode deep        # more aggressive relationship extraction
halal-graphify extract ./raw --code-only # index code only — local AST, no API key (skips docs/PDFs/images); an `extract` flag, not a skill flag
/halal-graphify ./raw --update           # re-extract only changed files
/halal-graphify ./raw --directed         # preserve edge direction
/halal-graphify ./raw --cluster-only     # rerun clustering on existing graph
/halal-graphify ./raw --no-viz           # skip HTML visualization
/halal-graphify ./raw --obsidian         # generate Obsidian vault
/halal-graphify ./raw --obsidian --obsidian-dir ~/vault  # write into an existing vault (never overwrites your own notes or .obsidian config)
/halal-graphify ./raw --wiki             # build agent-crawlable markdown wiki
/halal-graphify ./raw --svg              # export graph.svg
/halal-graphify ./raw --graphml          # export for Gephi / yEd
/halal-graphify ./raw --neo4j            # generate cypher.txt for Neo4j
/halal-graphify ./raw --neo4j-push bolt://localhost:7687
/halal-graphify ./raw --falkordb         # generate cypher.txt for FalkorDB
/halal-graphify ./raw --falkordb-push falkordb://localhost:6379
/halal-graphify ./raw --watch            # auto-sync as files change
/halal-graphify ./raw --mcp              # start MCP stdio server

/halal-graphify add https://arxiv.org/abs/1706.03762
/halal-graphify add <video-url>
/halal-graphify add https://... --author "Name" --contributor "Name"

/halal-graphify query "what connects attention to the optimizer?"
/halal-graphify query "..." --dfs --budget 1500
/halal-graphify path "DigestAuth" "Response"
/halal-graphify explain "SwinTransformer"

halal-graphify save-result --question "Q" --answer "A" --nodes Foo Bar --outcome useful   # record how a Q&A turned out (work memory; outcome ∈ useful|dead_end|corrected)
halal-graphify reflect                   # aggregate graphify-out/memory/ outcomes into reflections/LESSONS.md
halal-graphify reflect --if-stale        # no-op when LESSONS.md is already newer than every input (cheap to run each session)
halal-graphify reflect --out docs/LESSONS.md    # write the lessons doc somewhere else
halal-graphify reflect --graph graphify-out/graph.json  # group lessons by community + write the work-memory overlay (.graphify_learning.json)
                                   # the overlay tags nodes preferred/tentative/contested (recency-weighted, with provenance);
                                   # halal-graphify explain / query then show a "Lesson:" hint, flagged "code changed — re-verify" when the source moved on

halal-graphify uninstall                 # remove from all platforms in one shot
halal-graphify uninstall --purge         # also delete graphify-out/
halal-graphify uninstall --project --platform codex  # remove project-scoped install files only

halal-graphify hook install              # post-commit + post-checkout hooks
halal-graphify hook uninstall
halal-graphify hook status

# always-on assistant instructions - platform-specific
halal-graphify claude install            # CLAUDE.md + PreToolUse hook (Claude Code)
halal-graphify claude uninstall
halal-graphify codebuddy install         # CODEBUDDY.md + PreToolUse hook (CodeBuddy)
halal-graphify codebuddy uninstall
halal-graphify codex install             # AGENTS.md + PreToolUse hook in .codex/hooks.json (Codex)
halal-graphify opencode install          # AGENTS.md + tool.execute.before plugin (OpenCode)
halal-graphify kilo install              # native Kilo skill + /halal-graphify command + AGENTS.md + .kilo plugin
halal-graphify kilo uninstall
halal-graphify cursor install            # .cursor/rules/halal-graphify.mdc (Cursor)
halal-graphify cursor uninstall
halal-graphify gemini install            # GEMINI.md + BeforeTool hook (Gemini CLI)
halal-graphify gemini uninstall
halal-graphify copilot install           # skill file (GitHub Copilot CLI)
halal-graphify copilot uninstall
halal-graphify aider install             # AGENTS.md (Aider)
halal-graphify aider uninstall
halal-graphify claw install              # AGENTS.md (OpenClaw)
halal-graphify claw uninstall
halal-graphify droid install             # AGENTS.md (Factory Droid)
halal-graphify droid uninstall
halal-graphify trae install              # AGENTS.md (Trae)
halal-graphify trae uninstall
halal-graphify trae-cn install           # AGENTS.md (Trae CN)
halal-graphify trae-cn uninstall
halal-graphify hermes install             # AGENTS.md + ~/.hermes/skills/ (Hermes)
halal-graphify hermes uninstall
halal-graphify amp install               # skill file (Amp)
halal-graphify amp uninstall
halal-graphify agents install            # ~/.agents/skills/ + AGENTS.md (cross-framework; alias: halal-graphify skills)
halal-graphify agents uninstall
halal-graphify kiro install               # .kiro/skills/ + .kiro/steering/graphify.md (Kiro IDE/CLI)
halal-graphify kiro uninstall
halal-graphify pi install                # skill file (Pi coding agent)
halal-graphify pi uninstall
halal-graphify devin install             # skill file + .windsurf/rules/graphify.md (Devin CLI)
halal-graphify devin uninstall
halal-graphify antigravity install       # .agents/rules + .agents/workflows (Google Antigravity)
halal-graphify antigravity uninstall

halal-graphify extract ./docs                        # headless LLM extraction for CI (no IDE needed)
halal-graphify extract ./docs --backend gemini       # explicit backend: gemini, kimi, claude, openai, deepseek, ollama, bedrock, or claude-cli
halal-graphify extract ./docs --backend gemini --model gemini-3.1-pro-preview
halal-graphify extract ./docs --backend ollama       # local Ollama (set OLLAMA_BASE_URL / OLLAMA_MODEL) - no API key needed for loopback
OPENAI_BASE_URL=http://localhost:8080/v1 OPENAI_MODEL=my-model halal-graphify extract ./docs --backend openai   # any OpenAI-compatible server (llama.cpp, vLLM, LM Studio)
ANTHROPIC_BASE_URL=http://localhost:4000 ANTHROPIC_MODEL=my-model halal-graphify extract ./docs --backend claude   # any Anthropic-compatible endpoint (LiteLLM proxy, gateways)
GRAPHIFY_OLLAMA_NUM_CTX=32768 halal-graphify extract ./docs --backend ollama   # override KV-cache window (auto-sized by default)
GRAPHIFY_OLLAMA_KEEP_ALIVE=0 halal-graphify extract ./docs --backend ollama    # unload model after each chunk (saves VRAM on small GPUs)
halal-graphify extract ./docs --backend bedrock      # AWS Bedrock via IAM - no API key, uses AWS credential chain
halal-graphify extract ./docs --backend claude-cli   # route through Claude Code CLI - no API key, uses your Claude subscription
halal-graphify extract ./docs --backend azure        # Azure OpenAI (set AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT)
halal-graphify extract ./docs --max-workers 16       # AST parallelism (also GRAPHIFY_MAX_WORKERS)
halal-graphify extract --postgres "postgresql://user:pass@host/db"   # introspect live PostgreSQL schema directly
halal-graphify extract ./my-workspace --cargo        # introspect Rust Cargo workspace dependencies directly
halal-graphify extract ./docs --token-budget 30000   # smaller semantic chunks for local/small models
halal-graphify extract ./docs --max-concurrency 2    # fewer parallel LLM calls (useful for local inference)
halal-graphify extract ./docs --api-timeout 900      # longer HTTP timeout for slow local models (default 600s)
halal-graphify extract ./docs --google-workspace     # export .gdoc/.gsheet/.gslides via gws before extraction
halal-graphify extract ./src --no-gitignore          # include git-ignored source; still honor .graphifyignore
halal-graphify extract ./docs --mode deep            # richer semantic extraction via extended system prompt
halal-graphify extract ./docs --no-cluster           # raw extraction only, skip clustering
halal-graphify extract ./docs --timing               # print per-stage wall-clock timings to stderr (also works on cluster-only)
halal-graphify extract ./docs --force                # overwrite graph.json even if new graph has fewer nodes (use after refactors or to clear ghost duplicates)
halal-graphify extract ./docs --dedup-llm            # LLM tiebreaker for ambiguous entity pairs (uses same API key)
halal-graphify extract ./docs --global --as myrepo   # extract and register into the cross-project global graph
GRAPHIFY_MAX_OUTPUT_TOKENS=32768 halal-graphify extract ./docs --backend claude  # raise output cap for dense corpora

halal-graphify export callflow-html                       # graphify-out/<project>-callflow.html
halal-graphify export callflow-html --max-sections 8      # cap generated architecture sections
halal-graphify export callflow-html --output docs/arch.html
halal-graphify export callflow-html ./some-repo/graphify-out

halal-graphify global add graphify-out/graph.json --as myrepo   # register a project graph into ~/.graphify/global-graph.json
halal-graphify global remove myrepo                         # remove a project from the global graph
halal-graphify global list                                  # show all registered repos + node/edge counts
halal-graphify global path                                  # print path to the global graph file

halal-graphify prs                              # PR dashboard: CI, review, worktree, graph impact
halal-graphify prs 42                           # deep dive on PR #42
halal-graphify prs --triage                     # AI triage ranking (auto-detects backend from env)
halal-graphify prs --worktrees                  # worktree → branch → PR mapping
halal-graphify prs --conflicts                  # PRs sharing graph communities (merge-order risk)
halal-graphify prs --base main                  # filter to PRs targeting a specific base branch
halal-graphify prs --repo owner/repo            # run against a different GitHub repo
GRAPHIFY_TRIAGE_BACKEND=kimi halal-graphify prs --triage   # use a specific backend for triage

halal-graphify clone https://github.com/karpathy/nanoGPT
halal-graphify merge-graphs a.json b.json --out merged.json
halal-graphify --version                                    # print installed version
halal-graphify watch ./src
halal-graphify check-update ./src
halal-graphify update ./src
halal-graphify update ./src --no-cluster  # skip reclustering, write raw AST graph only
halal-graphify update ./src --force       # overwrite even if new graph has fewer nodes
halal-graphify cluster-only ./my-project
halal-graphify cluster-only ./my-project --graph path/to/graph.json  # custom graph location
halal-graphify cluster-only ./my-project --max-concurrency 16 --batch-size 200  # parallel community labeling (large graphs)
halal-graphify cluster-only ./my-project --resolution 1.5            # more, smaller communities
halal-graphify cluster-only ./my-project --exclude-hubs 99           # exclude p99 degree nodes from partitioning
halal-graphify cluster-only ./my-project --no-label                  # keep "Community N" placeholders
halal-graphify cluster-only ./my-project --backend=gemini            # backend for community naming
halal-graphify cluster-only ./my-project --backend=gemini --model gemini-2.5-pro  # specific model
halal-graphify label ./my-project                                    # (re)name communities with the configured backend
halal-graphify label ./my-project --backend=openai --model gpt-4o   # force a specific backend and model
```

> **Community names:** inside an agent (Claude Code, Gemini CLI) the agent names communities itself. When you run the bare CLI, `cluster-only` auto-names them with the configured backend (built-in or custom OpenAI-compatible provider) — pass `--no-label` to keep `Community N`, or run `halal-graphify label` to (re)generate names on demand.

---

## Learn more

- [How it works](docs/how-it-works.md) — the extraction pipeline, community detection, confidence scoring, benchmarks
- [ARCHITECTURE.md](ARCHITECTURE.md) — module breakdown, how to add a language
- [Optional integrations](docs/docker-mcp-sqlite.md) — Docker MCP Toolkit + SQLite
- [The Memory Layer](https://safishamsi.gumroad.com/l/qetvlo) — the book on the ideas behind halal-graphify, the architecture end to end

---

## halal-graphify Enterprise

[**halal-graphify Enterprise**](https://graphify.com) is the always-on layer built on top of halal-graphify — it applies the same graph approach to your entire working context: meetings, files, docs, and code, updating continuously in the background.

Built for people and teams whose work lives across hundreds of conversations and documents they can never fully reconstruct.

**[Join the waitlist at graphify.com](https://graphify.com).** Free trial launching soon.

---

<details>
<summary>Contributing</summary>

### Development setup

The project uses [uv](https://docs.astral.sh/uv/) for dev workflow. Install it once, then:

```bash
git clone https://github.com/safishamsi/graphify.git
cd halal-graphify
git checkout v8                        # active development branch

# Create the project venv and install halal-graphify + all extras + the dev group
# (pytest). uv installs the dev dependency group by default; pass --no-dev to
# skip it.
uv sync --all-extras
```

Verify the editable install:
```bash
uv run halal-graphify --version
uv run python -c "import halal_graphify; print(halal_graphify.__file__)"
```

### Running tests

```bash
uv run pytest tests/ -q                # run the full suite
uv run pytest tests/test_extract.py -q # one module
uv run pytest tests/ -q -k "python"    # filter by name
```

> macOS note: the test suite includes both `sample.f90` and `sample.F90` fixtures. These collide on case-insensitive HFS+ / APFS file systems. Run on Linux or in a Docker container if you need to test both Fortran variants simultaneously.

### Git workflow

- Active development happens on the `v8` branch.
- Commit style: `fix: <description>` / `feat: <description>` / `docs: <description>`
- Before opening a PR, run `uv run pytest tests/ -q` and confirm it passes.
- Add a fixture file to `tests/fixtures/` and tests to `tests/test_languages.py` for any new language extractor.

### What to contribute

**Worked examples** are the most useful contribution. Run `/halal-graphify` on a real corpus, save the output to `worked/{slug}/`, write an honest `review.md` covering what the graph got right and wrong, and open a PR.

**Extraction bugs** — open an issue with the input file, the cache entry (`graphify-out/cache/`), and what was missed or wrong.

See [ARCHITECTURE.md](ARCHITECTURE.md) for module responsibilities and how to add a language.

</details>

---

## Community and links

<p align="center">
  <a href="https://graphify.com"><img src="https://img.shields.io/badge/Website-graphify.com-4c1?style=flat&logo=googlechrome&logoColor=white" alt="Website"/></a>
  <a href="https://discord.gg/598Ad9zQZ"><img src="https://img.shields.io/badge/Discord-Join-5865F2?style=flat&logo=discord&logoColor=white" alt="Discord"/></a>
  <a href="https://x.com/halal-graphify"><img src="https://img.shields.io/badge/X-graphify-000000?logo=x&logoColor=white" alt="X"/></a>
  <a href="https://github.com/sponsors/safishamsi"><img src="https://img.shields.io/badge/sponsor-safishamsi-ea4aaa?logo=github-sponsors" alt="Sponsor"/></a>
  <a href="https://safishamsi.gumroad.com/l/qetvlo"><img src="https://img.shields.io/badge/Book-The%20Memory%20Layer-2ea44f?style=flat&logo=gitbook&logoColor=white" alt="The Memory Layer"/></a>
</p>
