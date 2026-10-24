# R-014 — Does a context pack beat a notes file over a long project?

Status: **done 2026-10-20 (scored run complete; P1a–d pass, P2 and P3 fail; see "Scored run"). Pre-registered 2026-10-19; model changed to minimax-m3.1-flash-free (backup longcat-2.5-preview-free) on 2026-10-19, see the amendment; project v2 on 2026-10-20 (no "record it" wording, 9 facts); C0 leak gone; v3 (8 sessions, 12 facts) on 2026-10-20; ceiling rule dropped and primary comparisons changed on 2026-10-20 before the scored run, see the last amendment.** Owner approved the design on 2026-10-19 ("pre-register R-014 as described and build the pilot on DeepSeek Flash. Report the pilot's measured cost before the scored run."). The scored run waits for the owner's OK on the pilot's measured cost.

Code: `E:\python_projects\agent_memory_study` (the R-013 harness; new tasks `L01`–`L20`). Agent harness: smolagents-ts, imported from its built `dist`, unmodified.
Parent: M4 in `docs/01-project.md`; follows R-013, which hit the ceiling (every memory condition at 86–96% success).

## Pre-registration

    ## R-014 — memory conditions over long projects with many, changing facts
    - Question: when a project runs for 6 sessions and its facts pile up and
      change, does a context pack keep a coding agent correct better than a
      free-form NOTES.md, and how close does it get to full-history replay
      at what token cost?
    - Projects: 16 scored projects (plus 4 pilot projects, dropped from the
      scored suite), each worked over 6 sessions; each session is a fresh
      agent and a fresh sandbox. Each project has a repo of 4-6 Python files
      and 5 facts stated only in session prompts 1-4:
        constraint  — a rule later code can break;
        decision    — a design choice no code shows yet;
        unfinished  — a step left for later, named only in the session
                      that defers it;
        superseded  — a fact stated in session 1 or 2 and changed in
                      session 3 or 4 (1-2 per project).
      Sessions 5 and 6 ask for work that must apply the facts; their prompts
      never restate them. Hidden tests are never shown to the agent; tasks
      and tests are frozen before any scored run.
    - Conditions: C0 none, C1 notes, C2 pack, C2g pack-given, C3 run memory,
      defined and prompted exactly as in R-013.
    - Agent: as in R-013 (smolagents-ts CodeAgent, Docker Jupyter sandbox,
      only tool final_answer, one system prompt plus the condition note).
    - Model, pinned for the whole study: deepseek-v4.1-flash via OpenCode Go
      (paid; owner-approved 2026-10-19). Key from .env by name only:
      OPENCODE_API_KEY. If the model fails or is withdrawn, stop and ask.
    - Repeats: 3 per (project, condition). 16 x 5 x 3 = 240 units,
      1,440 sessions.
    - Primary metric: fact score = share of a project's hidden fact tests
      (test_fact*) that pass after session 6, per unit.
    - Secondary: task success (every hidden test except test_stale* passes);
      stale-fact errors (test_stale* tests, which pass when the code follows
      the old version of a superseded fact); tokens per unit; C0's
      self-written note rate (the R-013 leak check).
    - Hypotheses (differences in mean fact score, in points):
        H1 C2 - C1 >= 10;
        H2 C2 stale-fact errors < C1 (per-project mean count);
        H3 C3 - C2 <= 5 and C2 tokens < 0.6 x C3 tokens (both must hold;
           the score part is a one-sided non-inferiority test of
           C2 - C3 > -5);
        H4 C2g - C2 > 0.
      Reported, not gated: C0 against every condition; results by fact kind;
      tokens per condition; memory-skip rate.
    - Test: per-project means over repeats, paired by project (n = 16).
      One-sided Wilcoxon signed-rank for H1, H2, H4 and the H3 score part;
      Holm over H1-H4. A hypothesis passes if p_holm < 0.05 and the observed
      difference meets its threshold. Paired bootstrap 95% CIs.
    - Prior: H1 uncertain (R-013 found +5.6 at the ceiling); H2 plausible
      (a pack has a decisions log); H3 plausible on tokens, uncertain on
      score; H4 likely passes.
    - Pilot (not scored): 4 projects x 5 conditions x 1 repeat, step cap 30.
      Rules:
        ceiling       — if C1 or C2 mean fact score exceeds 80%, add facts
                        or sessions to the projects and repeat the pilot;
        step cap      — the smallest of 20/30/40 at or above the 90th
                        percentile of steps in sessions that finished;
        format        — at least 90% of steps carry a code block, else stop
                        and ask;
        cost          — measured tokens per unit, scaled to 240 units, are
                        reported to the owner; the scored run starts only on
                        the owner's OK.
    - Budget: no GPU. DeepSeek Flash spend set from the pilot. Wall time:
      about 1 day of task writing, 2-4 h scored run at concurrency 20.
    - Stop condition: the pinned model is withdrawn or changes behaviour
      mid-study; a harness bug that affects one condition more than another
      (fix, then re-run every condition). C3 context overflow is logged and
      counted as that unit's outcome, not a stop.
    - Known limitations: one model; toy-sized projects; C0 can still write
      its own notes into code (measured, not prevented).
    - Owner: Ahmad Mahmoud (approval); Claude (runs).
    - Date: approved 2026-10-19.

## Pilot 2026-10-19 (not scored)

- Run: 4 projects (L01–L04) × 5 conditions × 1 repeat on deepseek-v4.1-flash, step cap 30, concurrency 20. Out: `runs/r014_pilot`; summary `python harness/analysis/pilot014.py runs/r014_pilot`.
- Harness change before the run: `harness/run.mjs` records `factScore` and `staleErrors`, and leaves `test_stale*` out of success. Projects come from `tasks/make_long_tasks.py`; `tasks/check_long.py` confirms every hidden test passes on the reference code and every stale test fails.
- Health: 120/120 sessions ended in success; 0 collapses; 0 provider errors; 97.6% of steps carry code; p90 steps 12, max 24.
- Fact score: C0 90.0, C1 100, C2 95.0, C2g 100, C3 100. Stale-fact errors: 0 in every condition. Success: C0 2/4, C1 4/4, C2 3/4, C2g 4/4, C3 4/4.
- Tokens per unit (k in / k out): C0 144/15.8, C1 232/23.1, C2 283/29.0, C2g 230/26.6, C3 262/12.9. Pilot total 4.60M in, 0.43M out.
- Cost: at $0.30 / $1.20 per 1M tokens (the higher, uncached rate on opencode.ai's DeepSeek V4.1 Flash page), the pilot cost about $1.90 and 240 scored units about $23. Caching or off-peak rates would lower this.
- Ceiling rule triggered: C1 and C2 exceed 80% fact score, so the projects must get harder before any scored run.
- Cause: all four C0 agents wrote the stated facts into files (README.md in L01 and L02, a new NOTES.md in L03, DESIGN.md in L04), as in R-013. The session prompts say "record it for later work", which invites this. More facts or sessions alone may not break the ceiling while that wording stays.

## Free-model check 2026-10-19 (not scored)

- The owner asked to try `deepseek-v4.1-flash-free` and `glm-5.3-flash-free` because they are free. Neither can be used from this harness.
- On the OpenCode Go endpoint both IDs return HTTP 400 "Upstream request failed: Model is unavailable." on every call; in the same minute `deepseek-v4.1-flash` (paid) answered.
- On the OpenCode Zen endpoint both return `FreeTierError`: the free tier can only be used from within the OpenCode client. The harness does not pretend to be that client.
- The two started pilots made 0 model calls; their outputs are moved to `runs/_aside/`. The pinned model stays `deepseek-v4.1-flash`.

## Free-model pilots and model amendment 2026-10-19 (not scored)

- The owner asked to try `longcat-2.5-preview-free` and `minimax-m3.1-flash-free`. Both answer on the OpenCode Go endpoint.
- MiniMax pilot (`runs/r014_pilot_minimax`, L01–L04 x 5 conditions x 1 repeat, step cap 30, concurrency 10): 120/120 sessions ended in success; 0 collapses; 1 provider error (retried); 95.8% of steps carry code; p90 steps 10, max 17.
  - Fact score: C0 80.0, C1 100, C2 100, C2g 100, C3 100. Stale-fact errors 0 everywhere. Success: C0 1/4, all others 4/4.
  - Tokens per unit (k in / k out): C0 127/30.9, C1 81/25.7, C2 142/35.8, C2g 155/43.8, C3 163/22.8. Scaled to 240 units: about 32M in, 7.6M out; the model is free.
  - C0 misses: L01 low_stock_sorted, L03 truncate, L04 due and tags.
- LongCat pilot (`runs/_aside/r014_pilot_longcat`) was stopped by the owner's instruction after 7 of 20 units (slow: one session took 1,222 s). Partial: 42/42 sessions succeeded, every finished unit scored 90-100, 0 provider errors.
- Owner decision (2026-10-19, "use minimax-m3.1-flash-free and make the backup model longcat-2.5-preview-free"): the pinned model becomes `minimax-m3.1-flash-free` via OpenCode Go, replacing `deepseek-v4.1-flash`; the backup is `longcat-2.5-preview-free`. No scored unit has run, so this is a design change before data, not a mid-study switch.
- Backup rule: if MiniMax fails or is withdrawn, the study moves to LongCat as a whole: a LongCat pilot on the frozen projects first, then every scored unit re-run on LongCat. Results from the two models are never pooled.
- Cost rule: the model is free, so the cost gate falls away; the scored run still waits on the ceiling fix and the owner's OK.
- The ceiling rule is still triggered (C1 and C2 at 100). The projects must get harder before any scored run; how (drop the "record it for later work" wording, or only add facts/sessions) is the owner's open decision.

## Project v2 and pilot 2026-10-20 (not scored)

- Owner instruction (2026-10-19): "Drop the 'record it for later work' wording and add more facts per project, then rerun the pilot on minimax-m3.1-flash-free."
- Projects v2 (`tasks/make_long_tasks.py`; v1 moved to `tasks/_aside/v1_5facts/`):
  - Decision prompts now read "Design decision for this project: " and change prompts read "Change to an earlier decision (it replaces the old one): "; "record it for later work" and "nothing implements it yet" are gone.
  - Each project has 9 facts instead of 5: 2 superseded, 2 unfinished, the rest constraints and decisions. Each project has 2 stale tests.
  - `check_long.py L01 L02 L03 L04`: the reference passes all 9 fact tests and fails both stale tests; no hidden test passes on the start repo.
- Pilot (`runs/r014_pilot_v2`, L01–L04 x 5 conditions x 1 repeat, step cap 30, concurrency 10): 120/120 sessions ended in success; 0 collapses; 1 provider error; 98.0% of steps carry code; p90 steps 13, max 26.
  - Fact score: C0 11.1, C1 94.4, C2 100, C2g 100, C3 100. Stale-fact errors: C0 1 (L02 overlap), all others 0. Success: C0 0/4, C1 3/4, the others 4/4.
  - C1 misses: L04 done_key and sorted.
  - Tokens per unit (k in / k out): C0 279/71.6, C1 255/63.2, C2 212/51.5, C2g 177/47.8, C3 153/21.6. Scaled to 240 units: about 52M in, 12M out; the model is free.
- The C0 leak is gone: no C0 repo holds a notes file, and C0 falls from 80 to 11.
- The ceiling rule is still triggered (C1 94.4, C2 100 exceed 80%). The step cap stays at 30 (p90 13). Whether to make the projects harder again, or to change the ceiling rule before any scored run, is the owner's decision.

## Project v3 and pilot 2026-10-20 (not scored)

- Owner instruction (2026-10-20): "Make the projects harder again (more sessions and facts, e.g. 8 sessions with 12 facts) and rerun the pilot on minimax-m3.1-flash-free."
- Projects v3 (`tasks/make_long_tasks.py`; v2 in `tasks/_aside/v2_9facts/`): 8 sessions and 12 facts per project (3 superseded, 3 unfinished, 6 constraints or decisions). Sessions 5 and 6 are new: each does a small task and states facts. The old sessions 5 and 6 are now 7 and 8. Each project has 3 stale tests. `check_long.py` passes on all four projects.
- Owner decision (2026-10-20): use minimax-m3.1-flash-free for the rest of R-014.
- Pilot (`runs/r014_pilot_v3`, L01–L04 x 5 conditions x 1 repeat, step cap 30, concurrency 10): 159 of 160 sessions ended in success, and 1 hit the step cap. 1 provider error. 96.7% of steps carry code; p90 steps 15, max 30.
  - Fact score: C0 39.6, C1 95.8, C2 97.9, C2g 100, C3 100.
  - Stale-fact errors: C0 1 (L03 id_8); all others 0.
  - Success: C0 0/4, C1 3/4, C2 3/4, C2g 4/4, C3 4/4.
  - Misses: C1 missed L01 csv_footer and overdraw; C2 missed L04 done_key.
  - Tokens per unit (k in / k out): C0 464/118, C1 530/87, C2 483/91, C2g 458/93, C3 392/38. Scaled to 240 units: about 112M in, 20M out; the model is free.
- The ceiling rule is still triggered: C1 and C2 stay above 80%. Over three project versions (5, 9 and 12 facts), C1 and C2 stayed at 94–100 while C0 moved. More facts do not lower the ceiling for a model that keeps a notes file. Whether to change the rule or the projects is the owner's decision.

## Amendment before the scored run 2026-10-20

Owner decision (2026-10-20, verbatim): "Amend the ceiling rule: accept that C1/C2 are near the ceiling and make the primary comparisons C0 vs memory, stale errors and tokens. Freeze v3, build L05–L20 and run the 240 scored units on MiniMax."

No scored unit has run. Every change below is fixed before any scored data exists.

- Projects: v3 is frozen, with 8 sessions and 12 facts per project (3 superseded, 3 unfinished, 6 constraints or decisions). Sessions 1–6 state the facts; sessions 7 and 8 must apply them. The scored suite is L05–L20 (16 projects), built in the same form; L01–L04 stay pilot-only. Each project passes `check_long.py` before the run: the reference code passes every fact test and fails every stale test, and the start repo passes no hidden test.
- Model: minimax-m3.1-flash-free via OpenCode Go, under the backup rule above.
- Units: 16 x 5 x 3 = 240 units, 1,920 sessions. Concurrency 10.
- Step cap: 20. The pilot rule picks the smallest of 20/30/40 at or above the v3 p90 of 15.
- Ceiling rule: dropped. C1 and C2 are expected near 100 and are reported as found.
- Primary comparisons (one-sided Wilcoxon signed-rank on per-project means over repeats, paired by project, n = 16; Holm over all six tests; a test passes if p_holm < 0.05 and the observed difference meets its threshold):
    P1a-d  memory vs none: C1 - C0, C2 - C0, C2g - C0 and C3 - C0 fact
           score each >= 20 points;
    P2     stale-fact errors: C2 < C1 (per-project mean count);
    P3     tokens: C2 total tokens per unit < C1.
- The old hypotheses are reported but do not gate any claim: H1 (C2 - C1 >= 10), H3 (C3 - C2 <= 5 with C2 tokens < 0.6 x C3) and H4 (C2g - C2 > 0). The old H2 is P2. Each comes with a paired bootstrap 95% CI.
- Also reported: stale errors for each memory condition vs C0, results by fact kind, tokens and steps per condition, and C0's self-note rate.
- Prior: P1 likely passes (the v3 pilot gap is 56–60 points). P2 is uncertain, since stale errors are rare everywhere (pilot: 0 in C1 and C2), so a tie is the likely result. P3 is uncertain (pilot C2 574k vs C1 617k total).

## Scored run 2026-10-20

Run: `runs/r014_scored` in the harness repo. 16 projects (L05–L20) x 5 conditions x 3 repeats = 240 units, 1,920 sessions, step cap 20, model minimax-m3.1-flash-free. Analysis: `harness/analysis/scored014.py`, output in `runs/r014_scored.analysis.txt`.

How the run went (deviations from the amendment):
- Concurrency: 10 for the first 70 units (log `runs/r014_scored.part1.log`, config `config.part1.json`). The model takes about 15–17 s per call, so 10 parallel sessions gave about 4 sessions a minute. On the owner's instruction (2026-10-20: "go to 50 or 100 or more see what the machine can handle") the rest ran at concurrency 100: about 40 sessions a minute, 17.4 s per step, no throttling and no zero-call sessions. Each session still runs in its own container (1 CPU, 1 GB). Units are queued interleaved across tasks and conditions, so a change in concurrency does not favour any condition. The run settings are otherwise unchanged.
- Sleep incident: in the first 100-way attempt the machine went to idle sleep. 95 sessions ended with 0 model calls and about 20,000 s of wall time. That attempt's 100 units are moved aside to `runs/_aside/r014_scored_part2_sleep`, and the 10 partial units from the stop to `runs/_aside/r014_scored_partial_1107`. All of them were rerun from scratch, and no data from them is used. For the rerun a keep-awake script called SetThreadExecutionState while `run.mjs` was alive; it changed no system settings.
- Final run: 240/240 units, no zero-call sessions, empty stderr. 1,848 sessions ended in success and 72 hit the step cap; step-cap sessions are real outcomes and are scored. 16 provider errors were retried. 97.7% of steps carry code; p90 steps 13. 119M tokens in total. *(superseded: see Correction 2026-10-20)*

Per condition (48 units each):

| cond | fact % | stale / unit | success % | tokens k / unit (superseded) | steps / unit |
|---|---|---|---|---|---|
| C0 | 68.4 | 0.06 | 0.0 | 396 | 78.2 |
| C1 | 94.6 | 0.08 | 62.5 | 455 | 75.4 |
| C2 | 96.7 | 0.00 | 79.2 | 511 | 79.2 |
| C2g | 97.4 | 0.00 | 77.1 | 524 | 80.6 |
| C3 | 96.0 | 0.00 | 77.1 | 593 | 39.7 |

Primary tests (one-sided Wilcoxon on per-project means, n = 16, Holm over 6; bootstrap 95% CI):

| test | diff | CI95 | p_holm | result |
|---|---|---|---|---|
| P1a C1 − C0 fact ≥ 20 | +26.2 | [+21.7, +30.7] | 0.0013 | **pass** |
| P1b C2 − C0 fact ≥ 20 | +28.3 | [+22.9, +33.2] | 0.0013 | **pass** |
| P1c C2g − C0 fact ≥ 20 | +29.0 | [+25.2, +33.0] | 0.0013 | **pass** |
| P1d C3 − C0 fact ≥ 20 | +27.6 | [+20.8, +33.2] | 0.0013 | **pass** |
| P2 C2 stale < C1 | −0.08 | [−0.17, −0.02] | 0.125 | fail (direction right, not significant) |
| P3 C2 tokens < C1 | +56k | [+20k, +91k] | 0.995 | fail (C2 uses more tokens) *(superseded: see Correction 2026-10-20)* |

Reported, not gated:
- H1, C2 − C1 fact: +2.1 [−1.7, +5.7]. Not supported; C1 is at the ceiling.
- H3, C2 vs C3: fact +0.7 [−4.5, +7.3], so C2 is within 5 points of C3 (p = 0.004). But C2 uses 0.86 of C3's tokens, above the 0.6 bound, so H3 fails. *(superseded: see Correction 2026-10-20)*
- H4, C2g − C2 fact: +0.7 [−2.4, +4.3]. Not supported.
- Stale errors vs C0: C1 +0.02; C2, C2g and C3 each −0.06 [−0.12, 0.00]; none significant. Only C0 (3 units) and C1 (4 units) made stale-fact errors at all.
- Tokens vs C0, k per unit: C1 +59, C2 +115, C2g +128, C3 +197. Every memory condition costs more than none. *(superseded: see Correction 2026-10-20)*
- Fact pass % by kind:

| cond | superseded | unfinished | constraint | decision | stale tests passing |
|---|---|---|---|---|---|
| C0 | 91.7 | 22.2 | 64.8 | 88.9 | 2.1 |
| C1 | 94.4 | 97.2 | 92.6 | 93.9 | 2.8 |
| C2 | 97.2 | 97.2 | 98.1 | 95.0 | 0.0 |
| C2g | 98.6 | 97.2 | 97.2 | 96.7 | 0.0 |
| C3 | 100.0 | 95.1 | 90.7 | 96.7 | 0.0 |

- C0 self-note rate (heuristic: sessions 1–7 write a non-.py file): 8/48 units.

Findings:
1. Any memory beats none by 26–29 fact points (P1a–d pass). Most of the gap is unfinished work (C0 22% vs 95–97%) and constraints (C0 65% vs 91–98%). Superseded facts and decisions mostly survive in the code itself, even without memory.
2. Among memory conditions, the differences are small and not significant on fact score. A notes file (C1) is already near the ceiling on this model. The context pack (C2) has fewer stale errors (0 vs 4 units) and higher success (79% vs 63%), but the stale test is close to its floor: only 4 projects differ, so Wilcoxon cannot reach p < 0.05 even after Holm. As the prior predicted, P2 is underpowered rather than refuted.
3. The context pack does not save tokens. C2 uses about 12% more tokens than C1 (P3 fails), and its token share vs full replay (0.86) is far above the 0.6 target. Full replay (C3) halves the steps but pays for it in input tokens. *(superseded: see Correction 2026-10-20)*
4. Success, which needs every hidden test to pass, separates the conditions more than fact score does: C0 0%, C1 63%, C2 79%, C2g 77%, C3 77%. It is not a pre-registered primary measure, so it is reported only.

Verdict: R-014 supports "memory vs none" strongly. On this model and these projects it does not show that a context pack beats a notes file on correctness, stale errors or tokens. A test of C2 vs C1 needs projects where stale errors are common, or a weaker model that does not keep NOTES.md well. The token part of this verdict is corrected below.

## Correction 2026-10-20: token counts and cost

**What was wrong.** The token figures above summed `tokenUsage` from `sessions.jsonl`. A session that hits the step cap ends in state `error`, and the library then returns `tokenUsage: null`, so all 72 step-cap sessions counted as 0 tokens. They are the longest sessions, and they are not spread evenly: error sessions per unit were C0 0.83, C1 0.29, C2g 0.25, C2 0.12, C3 0. The step logs (`s<k>.steps.json`) keep every call's usage; on sessions that do have a total, the logs match it at 100.00%. The analysis now counts tokens from the logs (`harness/analysis/usage.py`; corrected output `runs/r014_scored.analysis.v2.txt`, the old output kept). Fact score, stale errors, success and P1/P2 do not change.

Corrected tokens (k per unit, logs): C0 625, C1 542, C2 540, C2g 600, C3 593 (was 396, 455, 511, 524, 593). Run total 139.2M (was 119.0M).

| test | was | corrected |
|---|---|---|
| P3 C2 tokens < C1 | +56k [+20k, +91k], p_holm 0.995, fail (C2 costs more) | −2k [−70k, +60k], p_holm 0.666, fail (tie) |
| H3 token ratio C2/C3 | 0.86 | 0.91 (still above 0.6, H3 still fails) |
| tokens vs C0, k/unit | C1 +59, C2 +115, C2g +128, C3 +197 | C1 −83 [−157, −15], C2 −85 [−182, +12], C2g −25 [−112, +63], C3 −32 [−144, +79] |

So finding 3 changes: the context pack costs the same as a notes file, not more, and **memory is cheaper than no memory** (C1 significantly), because without memory the agent re-explores and runs into the step cap.

**Cost and time** (`harness/analysis/cost.py`). The run used the free model, and the provider returns no cost field, so dollars are computed from per-call tokens at the list price of the paid sibling, MiniMax M3 on OpenCode Go (2026-10-20 docs table, per 1M tokens): input $0.30, output $1.20, cached read $0.06. Caching is bounded two ways: "none" pays every input token in full; "prefix" assumes each call reuses the previous call's whole prompt in the same session (the best a prefix cache can do).

| cond | success % | $ / unit, no cache / prefix | $ / success, prefix | cache saving | wall s / unit (median) | wall s / success | error sessions / unit |
|---|---|---|---|---|---|---|---|
| C0 | 0.0 | 0.278 / 0.170 | – | 39% | 1,444 (1,478) | – | 0.83 |
| C1 | 62.5 | 0.243 / 0.151 | 0.242 | 38% | 1,359 (1,295) | 2,175 | 0.29 |
| C2 | 79.2 | 0.244 / 0.153 | 0.194 | 37% | 1,296 (1,239) | 1,637 | 0.12 |
| C2g | 77.1 | 0.266 / 0.163 | 0.212 | 39% | 1,376 (1,291) | 1,785 | 0.25 |
| C3 | 77.1 | 0.215 / 0.110 | 0.143 | 49% | 669 (658) | 868 | 0.00 |

Full replay (C3) is the cheapest and fastest per success on these 8-session projects: it takes half the steps, so it writes far fewer output tokens (output costs 4× input), and its growing prompt is exactly what a prefix cache serves. Wall times include queueing at concurrency 100; units were interleaved across conditions, so the comparison holds, but the absolute seconds do not transfer.

**Cache probe.** A 9.4k-token prompt sent twice to the free endpoint: the response carries `usage.prompt_tokens_details.cached_tokens` and `completion_tokens_details.reasoning_tokens`, but only 128–186 tokens came back as cached on MiniMax free (0 on LongCat free, which also reports `cache_write_tokens`). Real cache behaviour on the paid model was not probed (it costs money; not approved). The harness did not record `cached_tokens` during the run because the library's model class drops it. Since then the harness records each call's raw usage (`s<k>.calls.json`, and `usage` in every session record). Its smoke test (`runs/smoke_usage`, L05 C3, 2 sessions) found the free endpoint does cache inside a real session: 44% and 69% of prompt tokens, in 256-token blocks, so the 2-call probe understated it. Lesson and rule: `docs/memory/agent_memory_study.md`, R-C-agent_memory_study.5.

## Correction 2026-10-20: L06 cannot succeed

**What was wrong.** Found in the R-015 pilot. L06 (sensor log) has a hidden fact test, `test_fact_report_count` (kind decision), that checks that the summary's last line is "sensors: N". None of L06's 8 session prompts states that decision (`tasks/scored_a.py`, L06 block), so no unit could pass it: 0 of L06's 15 units succeeded here (all 5 conditions), and 0 of 12 in the R-015 pilot. The project checker did not catch it, because it only checks that the reference solution passes and the start repo fails.

**Effect.** The defect lowers every condition by the same amount, so no comparison between conditions changes, and P1–P3 and H1–H4 stand. It caps success at 15/16 projects:

| cond | success %, as run (48 units) | success %, without L06 (45 units) |
|---|---|---|
| C0 | 0.0 | 0.0 |
| C1 | 62.5 | 66.7 |
| C2 | 79.2 | 84.4 |
| C2g | 77.1 | 82.2 |
| C3 | 77.1 | 82.2 |

Fact score loses at most 0.5 points per condition (1 of 12 facts on 1 of 16 projects). L06 itself stays frozen as run. R-015 uses a fixed copy, L06f (`tasks/r015_l06f.py`), that states the decision in session 2; otherwise it is identical.

## Correction 2026-10-20: L10 asks for an unstated step

**What was wrong.** Found by the R-015 audit of hidden tests that no prompt supports. L10 (event booking) has a hidden fact test, `test_fact_slug_clean` (kind unfinished), that checks `slug("Rock & Roll!") == "rock-roll"` and `slug("  Jazz   Night ") == "jazz-night"`. Session 5's deferred step asks to remove punctuation and collapse runs of hyphens, but no prompt says that leading and trailing spaces are dropped, so a correct reading of the prompts can still fail it. 1 of the 12 memory-condition units passed it. In 11 of those 12, it was the only failing fact or basic test, so it alone cost the unit its success.

**Effect.** Nearly even across conditions (C1 3, C2 2, C2g 3, C3 3 units lost), so no conclusion changes. It narrows C2's lead over C2g and C3 to a tie:

| cond | success %, as run (48 units) | success %, L10 slug test counted as passed |
|---|---|---|
| C0 | 0.0 | 0.0 |
| C1 | 62.5 | 68.8 |
| C2 | 79.2 | 83.3 |
| C2g | 77.1 | 83.3 |
| C3 | 77.1 | 83.3 |

L10 stays frozen as run. R-015 uses a fixed copy, L10f (`tasks/r015_l10f.py`), whose session-5 deferred step also states the trimming; otherwise it is identical.
