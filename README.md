# AIluminode

AIluminode is a wieldable AI cognitive-orientation EEG instrument.

It helps AI tools check contextual posture before acting.

It uses NodAIity doctrine, but this repo is standalone.

```text
prompt/task
→ cognitive posture trace
→ route polarity
→ next safe action
```

## Use

Install locally:

```powershell
python -m pip install -e .
```

Run:

```powershell
ailuminode scan "Refactor Paula EPUB source handling without touching memory save logic"
```

Or without installation:

```powershell
python -m ailuminode scan "Read airframe.epub section 5 without saving it as memory"
```

## Output

```text
AIluminode TRACE ailuminode_0000

ACTIVE_TERRAIN:
- source_terrain

STANCE:
bounded_source_reader

COMPASS_GUIDANCE:
- none

ROUTE_POLARITY:
- OPEN: current_prompt (declared task is the active entry point)
- OPEN: bounded_source_index (source terrain is active; use bounded source access)
- PROTECT: saved_memory (saved_memory is named under a protection/avoidance phrase)
- DEFER: vector_memory (vector_memory is not needed for this task)
- BLOCK: autonomous_crawling (AIluminode stays declared-task only)

DRIFT_RISK:
- source_terrain_mistaken_for_memory
- section_numbers_mistaken_for_chapters

NEXT_SAFE_ACTION:
List source sections or search source text before summarizing.
```

## Route Polarity

```text
OPEN    = enter this route now
PROTECT = preserve this route; do not alter it
AUDIT   = inspect as evidence before acting
DEFER   = leave dormant unless explicitly reopened
BLOCK   = keep closed for this task
```

## Doctrine

Compass determines corridor truth.

AIluminode determines cognitive and retrieval posture.

AIluminode does not:

- read repositories
- store prompts
- own memory
- crawl systems
- ingest telemetry
- build dashboards
- run agents

It is wielded, read, and released.

```text
illuminate
orient
release
```
