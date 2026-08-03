<p align="center">
  <a href="https://graphify.com"><img src="https://raw.githubusercontent.com/safishamsi/graphify/v4/docs/logo-text.svg" width="260" height="64" alt="Graphify"/></a>
</p>

<p align="center">
  🇺🇸 <a href="../../README.md">English</a> | 🇨🇳 <a href="README.zh-CN.md">简体中文</a> | 🇯🇵 <a href="README.ja-JP.md">日本語</a> | 🇰🇷 <a href="README.ko-KR.md">한국어</a> | 🇩🇪 <a href="README.de-DE.md">Deutsch</a> | 🇫🇷 <a href="README.fr-FR.md">Français</a> | 🇪🇸 <a href="README.es-ES.md">Español</a> | 🇮🇳 <a href="README.hi-IN.md">हिन्दी</a> | 🇧🇷 <a href="README.pt-BR.md">Português</a> | 🇷🇺 <a href="README.ru-RU.md">Русский</a> | 🇸🇦 <a href="README.ar-SA.md">العربية</a> | 🇮🇹 <a href="README.it-IT.md">Italiano</a> | 🇵🇱 <a href="README.pl-PL.md">Polski</a> | 🇳🇱 <a href="README.nl-NL.md">Nederlands</a> | 🇹🇷 <a href="README.tr-TR.md">Türkçe</a> | 🇺🇦 <a href="README.uk-UA.md">Українська</a> | 🇻🇳 <a href="README.vi-VN.md">Tiếng Việt</a> | 🇮🇩 <a href="README.id-ID.md">Bahasa Indonesia</a> | 🇸🇪 <a href="README.sv-SE.md">Svenska</a> | 🇬🇷 <a href="README.el-GR.md">Ελληνικά</a> | 🇷🇴 <a href="README.ro-RO.md">Română</a> | 🇨🇿 <a href="README.cs-CZ.md">Čeština</a> | 🇫🇮 <a href="README.fi-FI.md">Suomi</a> | 🇩🇰 <a href="README.da-DK.md">Dansk</a> | 🇳🇴 <a href="README.no-NO.md">Norsk</a> | 🇭🇺 <a href="README.hu-HU.md">Magyar</a> | 🇹🇭 <a href="README.th-TH.md">ภาษาไทย</a> | 🇺🇿 <a href="README.uz-UZ.md">Oʻzbekcha</a> | 🇹🇼 <a href="README.zh-TW.md">繁體中文</a>
</p>

<p align="center">
  <a href="https://www.ycombinator.com/companies/halal-graphify"><img src="https://img.shields.io/badge/Y%20Combinator-S26-F0652F?style=flat&logo=ycombinator&logoColor=white" alt="YC S26"/></a>
  <a href="https://safishamsi.gumroad.com/l/qetvlo"><img src="https://img.shields.io/badge/Book-The%20Memory%20Layer-2ea44f?style=flat&logo=gitbook&logoColor=white" alt="The Memory Layer"/></a>
  <a href="https://github.com/safishamsi/graphify/actions/workflows/ci.yml"><img src="https://github.com/safishamsi/graphify/actions/workflows/ci.yml/badge.svg?branch=v8" alt="CI"/></a>
  <a href="https://pypi.org/project/halal-halal_graphify/"><img src="https://img.shields.io/pypi/v/halal-graphify" alt="PyPI"/></a>
  <a href="https://clickpy.clickhouse.com/dashboard/halal-graphify"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsql-clickhouse.clickhouse.com%2F%3Fquery%3DSELECT%2520concat%2528toString%2528round%2528sum%2528count%2529%2F1000%2529%2529%2C%2520%2527k%2527%2529%2520AS%2520c%2520FROM%2520pypi.pypi_downloads%2520WHERE%2520project%253D%2527graphifyy%2527%2520FORMAT%2520JSON%26user%3Ddemo&query=%24.data%5B0%5D.c&label=downloads&color=blue" alt="Downloads"/></a>
  <a href="https://github.com/sponsors/safishamsi"><img src="https://img.shields.io/badge/sponsor-safishamsi-ea4aaa?logo=github-sponsors" alt="Sponsor"/></a>
  <a href="https://www.linkedin.com/company/graphify-labs"><img src="https://img.shields.io/badge/LinkedIn-Graphify%20Labs-0077B5?logo=linkedin" alt="LinkedIn"/></a>
  <a href="https://x.com/halal-graphify"><img src="https://img.shields.io/badge/X-halal-graphify-000000?logo=x&logoColor=white" alt="X"/></a>
</p>

<p align="center">
  <a href="https://star-history.com/#safishamsi/graphify&Date">
    <img src="https://api.star-history.com/svg?repos=safishamsi/graphify&type=Date" alt="Star History Chart" width="370"/>
  </a>
</p>

Введіть `/halal-graphify` у своєму ШІ-асистенті для кодингу, і він нанесе весь ваш проект — код, документи, PDF, зображення, відео — на граф знань, який можна запитувати замість того, щоб шукати по файлах.

Працює в Claude Code, Codex, OpenCode, Cursor, Gemini CLI, GitHub Copilot CLI, VS Code Copilot Chat, Aider, OpenClaw, Factory Droid, Trae, Hermes, Kimi Code, Kiro, Pi та Google Antigravity.

```
/halal-graphify .
```

Це все. Ви отримуєте три файли:

```
graphify-out/
├── graph.html       відкрийте в будь-якому браузері — клікайте по вузлах, фільтруйте, шукайте
├── GRAPH_REPORT.md  основне: ключові концепції, неочікувані зв’язки, запропоновані запитання
└── graph.json       повний граф — запитуйте його будь-коли без повторного перечитування ваших файлів
```

Для читабельної сторінки архітектури з діаграмами викликів Mermaid виконайте:

```bash
halal-graphify export callflow-html
```

---

## Вимоги

| Вимога | Мінімум | Перевірка | Встановлення |
|---|---|---|---|
| Python | 3.10+ | `python --version` | [python.org](https://www.python.org/downloads/) |
| uv *(рекомендовано)* | будь-яка | `uv --version` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| pipx *(альтернатива)* | будь-яка | `pipx --version` | `pip install pipx` |

**Швидке встановлення на macOS (Homebrew):**
```bash
brew install python@3.12 uv
```

**Швидке встановлення на Windows:**
```powershell
winget install astral-sh.uv
```

**Ubuntu/Debian:**
```bash
sudo apt install python3.12 python3-pip pipx
# або встановити uv:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Встановлення

> **Офіційний пакет:** Пакет PyPI — `halal-graphify` (подвійна y). Інші пакети `halal-graphify*` на PyPI не є афілійованими. Команда CLI залишається `halal-graphify`.

**Крок 1 — встановити пакет:**

```bash
# Рекомендовано (uv автоматично додає halal-graphify до PATH):
uv tool install halal-graphify

# Альтернативи:
pipx install halal-graphify
pip install halal-graphify
```

**Крок 2 — зареєструвати навичку у вашому ШІ-асистенті:**

```bash
halal-graphify install
```

Це все. Відкрийте асистента і введіть `/halal-graphify .`

Щоб встановити навичку в поточний репозиторій замість профілю користувача, додайте `--project`:

```bash
halal-graphify install --project
halal-graphify install --project --platform codex
```

Встановлення на рівні проєкту записуються в поточну директорію, наприклад .claude/skills/halal-halal_graphify/SKILL.md або .agents/skills/halal-halal_graphify/SKILL.md, і виводять підказку git add для файлів, які можна закомітити. Команди для окремих платформ, що підтримують інсталяції на рівні проєкту, приймають той самий прапорець, наприклад halal-graphify claude install --project або halal-graphify codex install --project.

> **Примітка для PowerShell:** Використовуйте `halal-graphify .` замість `/halal-graphify .` — ведучий слеш є роздільником шляху в PowerShell.

> **`halal-graphify: command not found`?** Використовуйте `uv tool install halal-graphify` або `pipx install halal-graphify` — обидва автоматично додають CLI до PATH. При використанні звичайного `pip` додайте `~/.local/bin` (Linux) або `~/Library/Python/3.x/bin` (Mac) до вашого PATH, або запустіть `python -m halal_graphify`.

### Оберіть платформу

| Платформа | Команда встановлення |
|----------|----------------|
| Claude Code (Linux/Mac) | `halal-graphify install` |
| Claude Code (Windows) | `halal-graphify install --platform windows` |
| Codex | `halal-graphify install --platform codex` |
| OpenCode | `halal-graphify install --platform opencode` |
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
| Kiro IDE/CLI | `halal-graphify kiro install` |
| Pi coding agent | `halal-graphify install --platform pi` |
| Cursor | `halal-graphify cursor install` |
| Google Antigravity | `halal-graphify antigravity install` |

> Користувачам Codex: також додайте `multi_agent = true` під `[features]` у `~/.codex/config.toml`.
> Codex використовує `$halal-graphify` замість `/halal-graphify`.

### Додаткові пакети (опціонально)

Встановіть лише те, що потрібно:

| Пакет | Що додає | Встановлення |
|---|---|---|
| `pdf` | Вилучення PDF | `pip install "halal-graphify[pdf]"` |
| `office` | Підтримка `.docx` та `.xlsx` | `pip install "halal-graphify[office]"` |
| `google` | Рендеринг Google Sheets | `pip install "halal-graphify[google]"` |
| `video` | Транскрипція відео/аудіо (faster-whisper + yt-dlp) | `pip install "halal-graphify[video]"` |
| `mcp` | MCP stdio-сервер | `pip install "halal-graphify[mcp]"` |
| `neo4j` | Підтримка надсилання до Neo4j | `pip install "halal-graphify[neo4j]"` |
| `svg` | Експорт графу в SVG | `pip install "halal-graphify[svg]"` |
| `leiden` | Виявлення спільнот Leiden (лише Python < 3.13) | `pip install "halal-graphify[leiden]"` |
| `ollama` | Локальний вивід Ollama | `pip install "halal-graphify[ollama]"` |
| `openai` | OpenAI / OpenAI-сумісні API | `pip install "halal-graphify[openai]"` |
| `gemini` | Google Gemini API | `pip install "halal-graphify[gemini]"` |
| `bedrock` | AWS Bedrock (використовує IAM, без API-ключа) | `pip install "halal-graphify[bedrock]"` |
| `sql` | Вилучення SQL схем | `pip install "halal-graphify[sql]"` |
| `all` | Все вищезазначене | `pip install "halal-graphify[all]"` |

---

## Змусьте асистента завжди використовувати граф

Виконайте один раз у своєму проекті після побудови графу:

| Платформа | Команда |
|----------|---------|
| Claude Code | `halal-graphify claude install` |
| Codex | `halal-graphify codex install` |
| OpenCode | `halal-graphify opencode install` |
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
| Kiro IDE/CLI | `halal-graphify kiro install` |
| Pi coding agent | `halal-graphify pi install` |
| Google Antigravity | `halal-graphify antigravity install` |

Це записує невеликий конфігураційний файл, який каже асистенту звертатися до графу знань для питань про кодову базу — надаючи перевагу локалізованим запитам на кшталт `halal-graphify query "<питання>"` замість читання повного звіту або пошуку по сирих файлах. На платформах, що підтримують хуки з корисним навантаженням (Claude Code, Gemini CLI), хук спрацьовує автоматично перед пошуковими викликами інструментів і спрямовує асистента до графу. На інших (Codex, OpenCode, Cursor тощо) постійні файли інструкцій (`AGENTS.md`, `.cursor/rules/` тощо) забезпечують таке саме керівництво. `GRAPH_REPORT.md` все ще доступний для загального огляду архітектури.

Щоб видалити halal-graphify з усіх платформ одразу: `halal-graphify uninstall` (додайте `--purge`, щоб також видалити `graphify-out/`). Або скористайтеся командою для конкретної платформи (напр. `halal-graphify claude uninstall`).

---

## Що є у звіті

- **Вузли-боги** — найбільш пов'язані концепції у вашому проекті. Через них проходить все.
- **Несподівані зв'язки** — зв'язки між речами з різних файлів або модулів. Відсортовані за ступенем несподіваності.
- **«Чому»** — рядкові коментарі (`# NOTE:`, `# WHY:`, `# HACK:`), рядки документації та обґрунтування дизайну з документів витягуються як окремі вузли, пов'язані з кодом, який вони пояснюють.
- **Запропоновані питання** — 4–5 питань, на які граф унікально здатний відповісти.
- **Теги впевненості** — кожен виведений зв'язок позначений як `EXTRACTED`, `INFERRED` або `AMBIGUOUS`. Ви завжди знаєте, що знайдено, а що виведено.

---

## Які файли підтримуються

| Тип | Розширення |
|------|-----------|
| Код (31 мова) | `.py .ts .js .jsx .tsx .mjs .go .rs .java .c .cpp .h .hpp .rb .cs .kt .scala .php .swift .lua .luau .zig .ps1 .ex .exs .m .mm .jl .vue .svelte .astro .groovy .gradle .dart .v .sv .sql .f .f90 .f95 .f03 .f08 .pas .pp .dpr .dpk .lpr .inc .dfm .lfm .lpk .sh .bash .json` |
| Документи | `.md .mdx .qmd .html .txt .rst .yaml .yml` |
| Office | `.docx .xlsx` (потрібен `pip install halal-graphify[office]`) |
| Google Workspace | `.gdoc .gsheet .gslides` (опціонально; потрібна автентифікація `gws` та `--google-workspace`; Sheets потребує `pip install halal-graphify[google]`) |
| PDF | `.pdf` |
| Зображення | `.png .jpg .webp .gif` |
| Відео / Аудіо | `.mp4 .mov .mp3 .wav` та інші (потрібен `pip install halal-graphify[video]`) |
| YouTube / URL | будь-який URL відео (потрібен `pip install halal-graphify[video]`) |

Код витягується локально без API-викликів (AST через tree-sitter). Все інше обробляється через API моделі вашого ШІ-асистента.

Файли `.gdoc`, `.gsheet` та `.gslides` з Google Drive for desktop — це ярлики-посилання, а не вміст документів. Щоб включити нативні Google Docs, Sheets та Slides у безголове витягування, встановіть та автентифікуйте [`gws` CLI](https://github.com/googleworkspace/cli), потім запустіть:

```bash
pip install "halal-graphify[google]"  # потрібен для рендерингу таблиць Google Sheets
gws auth login -s drive
halal-graphify extract ./docs --google-workspace
```

Також можна встановити `GRAPHIFY_GOOGLE_WORKSPACE=1`. Graphify експортує ярлики в `graphify-out/converted/` як Markdown-сайдкари, а потім витягує ці файли.

---

## Часті команди

```bash
/halal-graphify .                        # побудувати граф для поточної папки
/halal-graphify ./docs --update          # повторно витягнути лише змінені файли
/halal-graphify . --cluster-only         # перезапустити кластеризацію без повторного витягування
/halal-graphify . --cluster-only --resolution 1.5      # більш дрібні спільноти
/halal-graphify . --cluster-only --exclude-hubs 99     # виключити утилітарні суперхаби з рейтингів “hub-node” вузлів-богів
/halal-graphify . --no-viz               # пропустити HTML, лише звіт + JSON
/halal-graphify . --wiki                 # побудувати markdown-вікі з графу
halal-graphify export callflow-html      # Mermaid архітектура/flow-викликів HTML (автоматично регенерується на кожен git-коміт, якщо встановлений hook)

/halal-graphify query "що пов'язує auth з базою даних?"
/halal-graphify path "UserService" "DatabasePool"
/halal-graphify explain "RateLimiter"

/halal-graphify add https://arxiv.org/abs/1706.03762   # завантажити статтю і додати її
/halal-graphify add <youtube-url>                       # транскрибувати і додати відео

halal-graphify hook install              # автоматичне перебудування при git-коміті
halal-graphify merge-graphs a.json b.json              # об'єднати два графи

halal-graphify prs                       # дашборд PR: стан CI, статус рев’ю, мапінг worktree
halal-graphify prs 42                    # детальний огляд PR #42 з впливом на граф
halal-graphify prs --triage              # ШІ оцінює вашу чергу рев’ю (використовує будь-який налаштований бекенд)
halal-graphify prs --conflicts           # PR-и, що ділять спільні графові спільноти — ризик порядку злиття
```

Дивіться [повний довідник команд](#повний-довідник-команд) нижче.

---

## Ігнорування файлів

Створіть `.graphifyignore` у кореневій директорії проекту — той самий синтаксис, що й `.gitignore`, включно з запереченням `!`:

```
# .graphifyignore
node_modules/
dist/
*.generated.py

# індексувати лише src/, ігнорувати все інше
*
!src/
!src/**
```

---

## Налаштування для команди

`graphify-out/` призначений для коміту в git, щоб кожен у команді починав із картою.

**Рекомендовані доповнення до `.gitignore`:**
```
graphify-out/manifest.json    # базується на mtime, ламається після git clone
graphify-out/cost.json        # лише локальний
# graphify-out/cache/         # опціонально: комітьте для швидкості, пропустіть для меншого репо
```

**Робочий процес:**
1. Одна людина запускає `/halal-graphify .` і комітить `graphify-out/`.
2. Усі виконують pull — їхній асистент одразу читає граф.
3. Запустіть `halal-graphify hook install` для автоматичного перебудування після кожного коміту (лише AST, без витрат API). Це також налаштовує git merge driver, щоб `graph.json` ніколи не залишався з маркерами конфліктів — два розробники, що комітять одночасно, отримають автоматично об'єднані графи.
4. Коли документи або статті змінюються, запустіть `/halal-graphify --update`, щоб оновити ці вузли.

---

## Використання графу напряму

```bash
# запит до графу з терміналу
halal-graphify query "покажи потік автентифікації"
halal-graphify query "що пов'язує DigestAuth з Response?" --graph graphify-out/graph.json

# відкрити граф як MCP-сервер (для повторного доступу через інструменти)
python -m halal_graphify.serve graphify-out/graph.json

# зареєструвати в Kimi Code:
kimi mcp add --transport stdio halal-graphify -- python -m halal_graphify.serve graphify-out/graph.json
```

MCP-сервер надає асистенту структурований доступ: `query_graph`, `get_node`, `get_neighbors`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`.

> **Примітка для WSL / Linux:** Ubuntu постачає `python3`, а не `python`. Використовуйте venv, щоб уникнути конфліктів:
> ```bash
> python3 -m venv .venv && .venv/bin/pip install "halal-graphify[mcp]"
> ```

---

## Змінні середовища

Потрібні лише для **headless / CI витягування** (`halal-graphify extract`). При запуску через навичку `/halal-graphify` у вашому IDE API моделі надається сесією IDE — додаткових ключів не потрібно.

| Змінна | Використання | Коли потрібна |
|---|---|---|
| `ANTHROPIC_API_KEY` | Backend Claude (Anthropic) | `--backend claude` |
| `ANTHROPIC_BASE_URL` | URL Anthropic-сумісного endpoint (LiteLLM proxy, шлюзи, ...) | `--backend claude` (типово: `https://api.anthropic.com`) |
| `ANTHROPIC_MODEL` | Назва моделі для backend Claude — для власних endpoint використовуйте назву/псевдонім моделі вашого сервера | `--backend claude` (типово: `claude-sonnet-4-6`) |
| `GEMINI_API_KEY` або `GOOGLE_API_KEY` | Backend Google Gemini | `--backend gemini` |
| `OPENAI_API_KEY` | OpenAI або OpenAI-сумісні API | `--backend openai` (локальні сервери приймають будь-яке непорожнє значення) |
| `OPENAI_BASE_URL` | URL OpenAI-сумісного сервера (llama.cpp, vLLM, LM Studio, ...) | `--backend openai` (типово: `https://api.openai.com/v1`) |
| `OPENAI_MODEL` | Назва моделі для backend OpenAI — для self-hosted серверів використовуйте назву/псевдонім моделі, яку надає ваш сервер (див. його endpoint `/v1/models`), напр. `LFM2.5-8B-A1B-UD-Q4_K_XL` для llama.cpp | `--backend openai` (типово: `gpt-4.1-mini`) |
| `DEEPSEEK_API_KEY` | Backend DeepSeek | `--backend deepseek` |
| `MOONSHOT_API_KEY` | Backend Kimi Code | `--backend kimi` |
| `OLLAMA_BASE_URL` | URL локального виводу Ollama | `--backend ollama` (типово: `http://localhost:11434`) |
| `OLLAMA_MODEL` | Назва моделі Ollama | `--backend ollama` (типово: автовизначення) |
| `GRAPHIFY_OLLAMA_NUM_CTX` | Перевизначити розмір KV-кеш вікна Ollama | опціонально — автоматично за замовчуванням |
| `GRAPHIFY_OLLAMA_KEEP_ALIVE` | Хвилини утримання моделі Ollama завантаженою | опціонально — встановіть `0` для вивантаження після кожного шматка |
| `AWS_*` / `~/.aws/credentials` | AWS Bedrock — стандартний ланцюг облікових даних | `--backend bedrock` (без API-ключа, використовує IAM) |
| `GRAPHIFY_MAX_WORKERS` | Кількість потоків паралелізму AST | опціонально — також прапор `--max-workers` |
| `GRAPHIFY_MAX_OUTPUT_TOKENS` | Підвищити ліміт виводу для щільних корпусів | опціонально — напр. `32768` для великих файлів |
| `GRAPHIFY_API_TIMEOUT` | HTTP тайм-аут у секундах (типово: 600) | опціонально — також прапор `--api-timeout` |
| `GRAPHIFY_FORCE` | Примусове перебудування графу навіть із меншою кількістю вузлів | опціонально — також прапор `--force` |
| `GRAPHIFY_GOOGLE_WORKSPACE` | Автоввімкнення експорту Google Workspace | опціонально — встановіть в `1` |
| `GRAPHIFY_TRIAGE_BACKEND` | Backend для `halal-graphify prs --triage` | опціонально — автовизначення з наявних ключів |
| `GRAPHIFY_TRIAGE_MODEL` | Перевизначення моделі для triage | опціонально — напр. `claude-opus-4-7` |

---

## Конфіденційність

- **Файли коду** — обробляються локально через tree-sitter. Нічого не покидає ваш комп'ютер.
- **Відео / аудіо** — транскрибуються локально за допомогою faster-whisper. Нічого не покидає ваш комп'ютер.
- **Документи, PDF, зображення** — надсилаються до вашого ШІ-асистента для семантичного витягування (через навичку `/halal-graphify`, використовуючи модель, що запущена у вашому IDE). Безголове `halal-graphify extract` потребує `GEMINI_API_KEY` / `GOOGLE_API_KEY` (Gemini), `MOONSHOT_API_KEY` (Kimi), `ANTHROPIC_API_KEY` (Claude), `OPENAI_API_KEY` (OpenAI), `DEEPSEEK_API_KEY` (DeepSeek), запущеного екземпляра Ollama (`OLLAMA_BASE_URL`), AWS-облікових даних через стандартний ланцюг провайдерів (Bedrock — без API-ключа, використовує IAM) або бінарного файлу `claude` CLI (Claude Code — без API-ключа, використовує вашу підписку Claude). Прапор `--dedup-llm` використовує той самий ключ.
- Без телеметрії, без відстеження використання, без аналітики.

---

## Вирішення проблем

**`halal-graphify: command not found` після `pip install halal-graphify`**
pip встановлює скрипти в директорію bin для користувача, яка може не бути в PATH. Виправлення:
- macOS: додайте `~/Library/Python/3.x/bin` до PATH у `~/.zshrc`
- Linux: додайте `~/.local/bin` до PATH у `~/.bashrc`
- Або використовуйте `uv tool install halal-graphify` / `pipx install halal-graphify` — обидва автоматично керують PATH.

**`python -m halal_graphify` працює, але команда `halal-graphify` — ні**
PATH вашої оболонки не включає директорію скриптів Python. Використовуйте `uv` або `pipx` замість звичайного `pip`.

**`/halal-graphify .` викликає "path not recognized" в PowerShell**
PowerShell трактує ведучий `/` як роздільник шляху. Використовуйте `halal-graphify .` (без слеша) на Windows.

**Граф має менше вузлів після `--update` або перебудови**
Якщо рефакторинг видалив файли, старі вузли залишаються. Передайте `--force` (або встановіть `GRAPHIFY_FORCE=1`), щоб перезаписати навіть якщо перебудова має менше вузлів.

**Граф має дублікати вузлів для однієї сутності (фантомні дублікати)**
Це трапляється, коли семантичне та AST-витягування не погодилось щодо формату ID вузла. Запустіть повне повторне витягування для очищення:
```bash
halal-graphify extract . --force
```

**Ollama вичерпує VRAM / перевищено вікно контексту**
KV-кеш вікно автоматично розраховується, але може бути завеликим для вашого GPU. Зменшіть його:
```bash
GRAPHIFY_OLLAMA_NUM_CTX=8192 halal-graphify extract ./docs --backend ollama --token-budget 4000
```

**HTML графу занадто великий для відкриття в браузері (>5000 вузлів)**
Пропустіть генерацію HTML і використовуйте JSON напряму:
```bash
halal-graphify cluster-only ./my-project --no-viz
halal-graphify query "..."
```

**`graph.json` має маркери конфліктів після одночасного коміту двох розробників**
Запустіть `halal-graphify hook install` — це налаштовує git merge driver, який автоматично об'єднує `graph.json`, щоб конфліктів ніколи не виникало.

**Вилучення повертає порожні вузли/ребра для документів або PDF**
Документи та PDF потребують LLM-виклику. Перевірте, що API-ключ встановлено і backend правильний:
```bash
ANTHROPIC_API_KEY=sk-... halal-graphify extract ./docs --backend claude
```

**Попередження про невідповідність версій навички у вашому IDE**
Встановлена версія halal-graphify відрізняється від файлу навички. Оновіть:
```bash
uv tool upgrade halal-graphify
halal-graphify install  # перезаписує файл навички
```

---

## Повний довідник команд

```
/halal-graphify                          # запустити в поточному каталозі
/halal-graphify ./raw                    # запустити у конкретній папці
/halal-graphify ./raw --mode deep        # більш агресивне витягування зв'язків
/halal-graphify ./raw --update           # повторно витягнути лише змінені файли
/halal-graphify ./raw --directed         # зберегти напрямок ребер
/halal-graphify ./raw --cluster-only     # повторна кластеризація існуючого графу
/halal-graphify ./raw --no-viz           # пропустити HTML-візуалізацію
/halal-graphify ./raw --obsidian         # згенерувати сховище Obsidian
/halal-graphify ./raw --wiki             # побудувати markdown-вікі для обходу агентами
/halal-graphify ./raw --svg              # експортувати graph.svg
/halal-graphify ./raw --graphml          # експортувати для Gephi / yEd
/halal-graphify ./raw --neo4j            # згенерувати cypher.txt для Neo4j
/halal-graphify ./raw --neo4j-push bolt://localhost:7687
/halal-graphify ./raw --watch            # автосинхронізація при зміні файлів
/halal-graphify ./raw --mcp              # запустити MCP stdio-сервер

/halal-graphify add https://arxiv.org/abs/1706.03762
/halal-graphify add <video-url>
/halal-graphify add https://... --author "Name" --contributor "Name"

/halal-graphify query "що пов'язує attention з optimizer?"
/halal-graphify query "..." --dfs --budget 1500
/halal-graphify path "DigestAuth" "Response"
/halal-graphify explain "SwinTransformer"

halal-graphify uninstall                 # видалити з усіх платформ одразу
halal-graphify uninstall --purge         # також видалити graphify-out/
halal-graphify uninstall --project --platform codex  # видалити лише файли проектного встановлення

halal-graphify hook install              # хуки post-commit + post-checkout
halal-graphify hook uninstall
halal-graphify hook status

halal-graphify claude install / uninstall
halal-graphify codex install / uninstall
halal-graphify opencode install
halal-graphify cursor install / uninstall
halal-graphify gemini install / uninstall
halal-graphify copilot install / uninstall
halal-graphify aider install / uninstall
halal-graphify claw install / uninstall
halal-graphify droid install / uninstall
halal-graphify trae install / uninstall
halal-graphify trae-cn install / uninstall
halal-graphify hermes install / uninstall
halal-graphify kiro install / uninstall
halal-graphify antigravity install / uninstall

halal-graphify extract ./docs                        # headless LLM-витягування для CI (без IDE)
halal-graphify extract ./docs --backend gemini       # явний backend: gemini, kimi, claude, openai, deepseek, ollama, bedrock або claude-cli
halal-graphify extract ./docs --backend gemini --model gemini-3.1-pro-preview
halal-graphify extract ./docs --backend ollama       # локальний Ollama (встановіть OLLAMA_BASE_URL / OLLAMA_MODEL) — без API-ключа для loopback
OPENAI_BASE_URL=http://localhost:8080/v1 OPENAI_MODEL=my-model halal-graphify extract ./docs --backend openai   # будь-який OpenAI-сумісний сервер (llama.cpp, vLLM, LM Studio)
ANTHROPIC_BASE_URL=http://localhost:4000 ANTHROPIC_MODEL=my-model halal-graphify extract ./docs --backend claude   # будь-який Anthropic-сумісний endpoint (LiteLLM proxy, шлюзи)
GRAPHIFY_OLLAMA_NUM_CTX=32768 halal-graphify extract ./docs --backend ollama   # перевизначити KV-кеш вікно (автоматично за замовчуванням)
GRAPHIFY_OLLAMA_KEEP_ALIVE=0 halal-graphify extract ./docs --backend ollama    # вивантажити модель після кожного шматка (економить VRAM на малих GPU)
halal-graphify extract ./docs --backend bedrock      # AWS Bedrock через IAM — без API-ключа, використовує ланцюг облікових даних AWS
halal-graphify extract ./docs --backend claude-cli   # маршрутизація через Claude Code CLI — без API-ключа, використовує вашу підписку Claude
halal-graphify extract ./docs --max-workers 16       # паралелізм AST (також GRAPHIFY_MAX_WORKERS)
halal-graphify extract ./docs --token-budget 30000   # менші семантичні шматки для локальних/малих моделей
halal-graphify extract ./docs --max-concurrency 2    # менше паралельних LLM-викликів (корисно для локального виводу)
halal-graphify extract ./docs --api-timeout 900      # довший HTTP тайм-аут для повільних локальних моделей (типово 600с)
halal-graphify extract ./docs --google-workspace     # експортувати .gdoc/.gsheet/.gslides через gws перед витягуванням
halal-graphify extract ./docs --no-cluster           # лише сире витягування, пропустити кластеризацію
halal-graphify extract ./docs --force                # перезаписати graph.json навіть якщо новий граф має менше вузлів (використовуйте після рефакторингу або для очищення фантомних дублікатів)
halal-graphify extract ./docs --dedup-llm            # LLM-арбітр для неоднозначних пар сутностей (використовує той самий API-ключ)
halal-graphify extract ./docs --global --as myrepo   # витягнути і зареєструвати в крос-проектний глобальний граф
GRAPHIFY_MAX_OUTPUT_TOKENS=32768 halal-graphify extract ./docs --backend claude  # підвищити ліміт виводу для щільних корпусів

halal-graphify export callflow-html                       # graphify-out/<project>-callflow.html
halal-graphify export callflow-html --max-sections 8      # обмежити кількість згенерованих секцій архітектури
halal-graphify export callflow-html --output docs/arch.html
halal-graphify export callflow-html ./some-repo/graphify-out

halal-graphify global add graphify-out/graph.json myrepo   # зареєструвати граф проекту в ~/.graphify/global.json
halal-graphify global remove myrepo                         # видалити проект з глобального графу
halal-graphify global list                                  # показати всі зареєстровані репо + кількість вузлів/ребер
halal-graphify global path                                  # вивести шлях до файлу глобального графу

halal-graphify prs                              # дашборд PR: CI, рев’ю, worktree, вплив на граф
halal-graphify prs 42                           # детальний огляд PR #42
halal-graphify prs --triage                     # AI ранжування пріоритизації (автоматично визначає бекенд з середовища)
halal-graphify prs --worktrees                  # worktree → гілка → PR зіставлення
halal-graphify prs --conflicts                  # PR-и, що ділять спільні графові спільноти (ризик порядку злиття)
halal-graphify prs --base main                  # фільтр PR-ів за цільовою базовою гілкою
halal-graphify prs --repo owner/repo            # запустити для іншого GitHub-репо
GRAPHIFY_TRIAGE_BACKEND=kimi halal-graphify prs --triage   # використовувати конкретний backend для triage

halal-graphify clone https://github.com/karpathy/nanoGPT
halal-graphify merge-graphs a.json b.json --out merged.json
halal-graphify --version                                    # вивести встановлену версію
halal-graphify watch ./src
halal-graphify check-update ./src
halal-graphify update ./src
halal-graphify update ./src --no-cluster  # пропустити рекластеризацію, записати лише сирий AST граф
halal-graphify update ./src --force       # перезаписати навіть якщо новий граф має менше вузлів
halal-graphify cluster-only ./my-project
halal-graphify cluster-only ./my-project --graph path/to/graph.json  # власне розташування графу
halal-graphify cluster-only ./my-project --resolution 1.5            # більше, менших спільнот
halal-graphify cluster-only ./my-project --exclude-hubs 99           # виключити вузли p99 ступеня з розбиття
```

---

## Дізнатися більше

- [Як це працює](../how-it-works.md) — пайплайн витягування, виявлення спільнот, оцінка впевненості, бенчмарки
- [ARCHITECTURE.md](../../ARCHITECTURE.md) — опис модулів, як додати мову
- [Опціональні інтеграції](../docker-mcp-sqlite.md) — Docker MCP Toolkit + SQLite

---

## Побудовано на halal-graphify — Penpax

[**Penpax**](https://graphify.com) — це завжди активний шар поверх halal-graphify, він застосовує той самий графовий підхід до всього робочого життя: зустрічей, історії браузера, email-ів, файлів і коду, постійно оновлюючись у фоновому режимі.

Створений для людей, чия робота розкидана по сотнях розмов і документів, які неможливо повністю відтворити. Без хмари, повністю на пристрої.

**Безкоштовна пробна версія незабаром.** [Приєднайтесь до списку очікування →](https://graphify.com)

---

<details>
<summary>Участь у розробці</summary>

### Налаштування розробки

Клонуйте репо і встановіть у редагованому режимі:

```bash
git clone https://github.com/safishamsi/graphify.git
cd halal-graphify
git checkout v8                        # гілка активної розробки

# Створіть віртуальне середовище (потрібен Python 3.10+):
python3 -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate

# Встановіть у редагованому режимі з усіма опціональними пакетами:
pip install -e ".[all]"
```

Перевірте редаговане встановлення:
```bash
halal-graphify --version
python -c "import halal_graphify; print(halal_graphify.__file__)"
```

### Запуск тестів

```bash
pip install pytest
pytest tests/ -q                       # запустити весь набір тестів
pytest tests/test_extract.py -q        # один модуль
pytest tests/ -q -k "python"           # фільтрація за назвою
```

> Примітка для macOS: набір тестів включає обидва файли `sample.f90` та `sample.F90`. Вони конфліктують на файлових системах HFS+ / APFS без урахування регістру. Запускайте на Linux або в Docker-контейнері, якщо потрібно тестувати обидва варіанти Fortran одночасно.

### Робочий процес з git

- Активна розробка відбувається в гілці `v8`.
- Стиль комітів: `fix: <опис>` / `feat: <опис>` / `docs: <опис>`
- Перед відкриттям PR запустіть `pytest tests/ -q` і переконайтесь, що він проходить.
- Додайте файл-фікстуру до `tests/fixtures/` і тести до `tests/test_languages.py` для будь-якого нового екстрактора мови.

### Що варто додати

Найкорисніший внесок — це **опрацьовані приклади**. Запустіть `/halal-graphify` на реальному корпусі, збережіть результат у `worked/{slug}/`, напишіть чесний `review.md` про те, що граф зробив правильно і неправильно, і відкрийте PR.

**Помилки витягування** — відкрийте issue з вхідним файлом, записом кешу (`graphify-out/cache/`) і тим, що було пропущено або неправильно.

Дивіться [ARCHITECTURE.md](../../ARCHITECTURE.md) щодо відповідальностей модулів і того, як додати мову.

</details>
