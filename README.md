# agent_memory_study

**How should a coding agent remember a project across sessions, and what is the cheapest way to do it that still works?**

This repo holds the harness, about 1,000 task files and the analysis code behind three pre-registered studies of multi-session coding agents. Together they ran about 1,750 scored agent units (one project, all its sessions) in Docker sandboxes. The agent is a smolagents-ts `CodeAgent`. It works on a project over many sessions, and between sessions it keeps memory in one of 12 ways: none, a notes file, a structured "context pack", full transcript replay, and others. Hidden tests then check whether the code works and whether the agent remembered the facts from earlier sessions.

## Headline results

| study | question | answer |
|---|---|---|
| **R-013**: 24 short tasks × 5 conditions × 3 repeats | Does memory help at all? | **Yes, by a lot.** The pack beats no memory by **+56.9 points** of success (Holm-adjusted p = 0.0002). On short tasks every memory condition sits near the ceiling (86–96%). |
| **R-014**: 8-session projects with 12 changing facts | Does a pack beat plain notes over a long project? | Memory vs none: **+26 to +29 points** of fact score (C0 68 → C1 95, C2 97, C2g 97, C3 96). Pack and notes tie, so the long project did not separate them. |
| **R-015**: 12 memory paths, 3 project sizes, 48 projects | Which memory path is **cheapest per success**? | **Full transcript replay (C3) wins at every tier.** Overall it reaches **93.1% success at $0.181 per success**, vs $0.224 for the full pack. At the advanced tier, replay leads on success by +20 points (95.0% vs 75.0%). |

A likely reason replay is cheap: the provider caches the replayed prefix, and the agent spends fewer steps rebuilding context. Under a hard *token* budget the trade flips. In the partial limited arm, replay stays ahead on simple and intermediate projects, but on advanced projects it runs out of budget first.

## The memory paths (R-015)

| path | memory between sessions |
|---|---|
| C0 | none (floor) |
| C1 / C1t | free-form `NOTES.md` / notes with a fixed template |
| C2 | full context pack (`AGENTS.md`, tasks, handoff, decisions) |
| C2−t / C2−h / C2−d | pack minus tasks / handoff / decisions (ablations) |
| C2a | `AGENTS.md` only |
| C2x | pack plus an irrelevant distractor file |
| C3 | full transcript replay |
| C3c | replay with compaction past a size threshold |
| C4 | ACE-style delta notes |

The study ran in three stages:
1. **Screen:** 12 paths × 8 projects × 2 repeats. Survivors were C0, C2, C3 and C2-h. Distractor files cost more and gained nothing. Dropping the task file cost 19 points.
2. **Confirm:** 4 paths × 48 projects × 3 repeats, or 5 repeats where the CI was still wide.
3. **Budget arms:** cut short when the free model was retired, so they are reported as partial and unranked.

## How it works

```
harness/run.mjs ─┬─ one Docker Jupyter sandbox per session (1 CPU, 1 GB)
                 ├─ harness/model.mjs   OpenAI-compatible client, retries, per-call usage log
                 ├─ harness/prompts.mjs session prompts and memory conditions
                 └─ templates/          notes, pack and ablation templates
tasks/            project generators + hidden tests (simple T*, intermediate L*, advanced A*)
harness/analysis/ paired bootstrap, ranking rule, drop rule, cost pricing (r015.py, scored014.py, sig.py)
docs/experiments/ the pre-registrations, stage logs and results (R-013, R-014, R-015, R-017)
```

**Rigour:**
- Each study was pre-registered before any scored result was read. Changes are dated amendments.
- Statistics use a paired bootstrap over projects (10,000 resamples, fixed seed) with 95% CIs.
- Cost is priced per call, with input, output and cached tokens priced separately. Totals cover failed sessions too.
- Infrastructure failures (rate limits, Docker errors) are rerun once and never scored as task failures.
- New projects pass static checks (`tasks/check_facts.py`, `check_long.py`) so that no hidden test asks for a fact no prompt states.

## Running it

You need Node 20+, Python 3.11+ with numpy, Docker, and a build of the smolagents-ts library. The harness currently points at local paths: `harness/model.mjs` holds the library path and the location of the `.env` file with `OPENCODE_API_KEY`. Adjust both to your setup.

```bash
docker build -t r013-sandbox:1 docker/
node harness/run.mjs --out runs/demo --tasks L05 --conds C0,C2,C3 --reps 1 --max-steps 20
python harness/analysis/r015.py runs/demo
node harness/sweep.mjs   # removes any leftover sandbox containers
```

Run outputs (`runs/`, about 2 GB) are not in the repo.

## Limits

- Each study used one free model: LongCat for R-013 and MiniMax M3.1 Flash for R-014/R-015. Results may not carry over to other models.
- Dollar costs use the paid sibling model's list price.
- At the advanced tier, the spread between projects kept the deciding CI wider than the 5-point margin, even after 5 repeats.

See `docs/experiments/` for the full records.
