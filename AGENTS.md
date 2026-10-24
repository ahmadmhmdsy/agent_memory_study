# agent_memory_study — scoped entry

## What this component is

**agent_memory_study** — the harness, task suites and run outputs for the memory
studies on multi-session coding agents: R-013 (five memory conditions, 24
tasks) and R-014 (8-session projects with many, changing facts). The agent is a
smolagents-ts CodeAgent running in a Docker Jupyter sandbox. The folder has no
git of its own; `runs/` and `node_modules/` are ignored by its `.gitignore`.

## Entry points

| entry point | path | notes |
|---|---|---|
| runner | `harness/run.mjs` | `node harness/run.mjs --out runs/<name> --tasks L01,L02 --conds C0,C2 --reps 1 --max-steps 30` |
| model client | `harness/model.mjs` | reads key names from `AI_Research/.env`; uses the library in `E:\python_projects\smolagents_ts` |
| conditions | `templates/notes`, `templates/pack`, `harness/prompts.mjs` | C0 none, C1 notes, C2 pack, C2g pack-given (the harness writes between sessions), C3 run-memory |
| task suites | `tasks/S01..S24` (R-013), `tasks/L01..L20` (R-014), `tasks/P1..P4` (pilots) | generators and checkers in `tasks/*.py` |
| analysis | `harness/analysis/scored014.py`, `pilot014.py`, `sig.py` | for example `python harness/analysis/scored014.py runs/r014_scored` |
| sandbox image | `docker/Dockerfile` | one container per session (1 CPU, 1 GB) |

## Smallest validation command

From `projects/agent_memory_study/`:

```powershell
node --check harness/run.mjs; python harness/analysis/scored014.py runs/r014_scored
```

Expected result: no syntax error, and the R-014 table (fact score C0 68, C1 95,
C2 97, C2g 97, C3 96).

## Boundaries

Owns the harness, tasks, templates and run outputs. It does not own the agent
library (`E:\python_projects\smolagents_ts`, read-only from here) or the
pre-registrations and verdicts (`research/experiments/R-013*`, `R-014*`).

## Hazards

- A scored run lasts hours and calls a remote model. Keep the machine awake for
  the whole run (see `docs/memory/agent_memory_study.md`).
- `.env` holds live keys. Code reads key names only; no value goes into a log,
  record or commit.
- Runs that are not used are moved to `runs/_aside/`, and tasks to
  `tasks/_aside/`.
- Absolute paths in `harness/model.mjs` and `harness/run.mjs` point at
  `smolagents_ts` and `AI_Research/.env`; a move of either breaks the harness.

## Pointers to root rules

Root policy lives in `rules/`, registered by `rules/00-index.md`; this file
restates none of it. This component's own rule file is
`rules/components/agent_memory_study.md`; the shared project rules are
`rules/components/projects.md`. Lessons: `docs/memory/agent_memory_study.md`.
