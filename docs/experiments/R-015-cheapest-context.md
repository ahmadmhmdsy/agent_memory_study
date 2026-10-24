# R-015 — The cheapest context that still succeeds, at three project sizes

Status: **done 2026-10-24 (closed on the confirm stage; stage 3 partial and unranked, see "Result"). Pre-registered 2026-10-20 (owner approved as drafted).** Owner approved the study on 2026-10-20 ("approve R-015 ... 1-model: keep MiniMax").

Code: `projects/agent_memory_study/` (the R-013/R-014 harness). Agent harness: smolagents-ts, imported from its built `dist`, unmodified (R-C-agent_memory_study.4).
Parent: M4 in `docs/01-project.md`; follows R-014.

## Explainer

**Question.** For a coding agent that works on a project over many sessions, which way of carrying context forward is the cheapest one that still gets the work right, and does the answer change with project size and with how much budget the agent gets?

**Why it matters.** R-013 and R-014 showed that any memory beats none, but the memory paths tie on correctness at this model's ceiling. Once success ties, the choice is decided by cost and speed, and the corrected R-014 numbers (Correction 2026-10-20) already flip two earlier conclusions: memory is cheaper than no memory, and full replay (C3) is the cheapest and fastest per success on 8-session projects. R-015 asks where that stops being true, and which parts of a context pack carry the value.

**Ranking rule (owner, 2026-10-20).** Success first, then cost, then speed:
1. A path is *acceptable* if its success is within δ points of the best path at that size and budget (δ to be set; proposal 5 points, with the CI reported).
2. Among acceptable paths, the lowest priced cost per success wins.
3. Ties on cost (within 10%) are broken by speed.
Because other readers weigh these differently, every result also gets the Pareto frontier (success × cost × time), a cost-first ranking, a speed-first ranking, and the raw table.

**Project sizes (tiers).** New projects, built and frozen before any scored run, in the R-014 style (facts stated only in session prompts; hidden tests).
- **Simple:** 4 sessions, about 5 facts. Expected ceiling for every memory path, so it measures the cheapest.
- **Intermediate:** 8 sessions, 12 facts, as R-014.
- **Advanced:** 20+ sessions, chains of superseded facts (a fact replaced 2–3 times), more stale tests, and a full history that nears the model's context window, so raw replay must break or be compacted.

**Paths (conditions).**

| id | path | what it tests |
|---|---|---|
| C0 | none | floor |
| C1 | free-form NOTES.md | the cheap baseline |
| C1t | NOTES.md with a fixed template | can cheap notes match the pack? |
| C2 | full context pack | R-014's pack |
| C2−t / C2−h / C2−d | pack minus tasks / handoff / decisions | which file carries the value (ablation) |
| C2a | AGENTS.md only | the leanest pack |
| C2x | pack plus a plausible but irrelevant distractor file | does extra context hurt? |
| C3 | full transcript replay | R-014's cheapest |
| C3c | replay with compaction past a size threshold | replay that survives long projects |
| C4 | ACE-style delta notes (append small edits only) | incremental memory |

C2g (pack-given) is dropped: R-013 and R-014 both found it equal to C2.

**Budget arms.** Each tier runs at a *standard* budget (step cap 20, as R-014). Finalists also run at a *limited* budget (step cap about half the standard p90, so roughly 8) and a *near-unlimited* one (step cap 60, long session timeout), to see how each path behaves when the agent is squeezed or free.

**Adaptive budget (measured, not guessed).** The model is free, so the binding limit is machine time and run size, not money. The study runs in stages, each with its rule fixed in advance:
1. *Pilot* (2 projects per tier × all paths × 1 repeat): measures tokens, calls, wall time and error rate per path, and checks the tasks are neither trivial nor impossible.
2. *Screen* (intermediate tier, all paths, 8 projects × 2 repeats): drop a path only when it is clearly dominated (success CI entirely below the best by more than δ, or cost per success CI entirely above an acceptable path's).
3. *Confirm* (survivors, all three tiers, 16 projects × 3 repeats, standard budget), then the limited and near-unlimited arms on the confirm set's finalists.
Each stage's size is set from the stage before it: repeats are added (up to a cap fixed in the pre-registration) only when the key comparison's CI is still wider than δ. Every stage's projected sessions and hours are reported before it starts.

**Measures** (all per call, from every session including failures; R-C-agent_memory_study.5):
- success (every hidden test except stale passes), fact score, stale-fact errors;
- prompt, completion, cached, cache-write and reasoning tokens; peak prompt size; calls; failed attempts and retries;
- finish reason, HTTP status, model id served, per-call latency and timestamps;
- steps, step-cap sessions, wall time and model time per session and unit;
- priced cost: per call, at the dated list price of the paid sibling (MiniMax M3: input $0.30, output $1.20, cached $0.06 per 1M, 2026-10-20), three ways: measured caching (as the free endpoint reports it), no caching, and the prefix-cache bound.

**Model.** minimax-m3.1-flash-free via OpenCode Go, pinned, as R-014 (owner, 2026-10-20). Key from `.env` by name only: OPENCODE_API_KEY.

**What it delivers.** For each tier and budget: the cheapest acceptable path, the Pareto frontier, which pack files matter, whether a distractor hurts, and where replay stops being cheapest. It does not deliver a result for other models: the ceiling and the caching behaviour are model-specific, and the free endpoint's caching may differ from the paid model's, so real cached cost needs a paid check later. (Smoke test 2026-10-20, `runs/smoke_usage`, L05 C3: the free endpoint served 44% and 69% of prompt tokens from cache in sessions 1–2, in 256-token blocks, unlike the 2-call probe's 128–186 of 9.4k.)

**Risks.**
- Ceiling again on simple and intermediate tiers: mitigated by ranking on cost once success ties, which is the point of the study.
- Advanced projects are costly to build and may be too hard for every path: the pilot checks this before scoring.
- Too many paths: the screen stage prunes them.
- Wall time is inflated by concurrency: conditions stay interleaved (R-C-agent_memory_study.2); speed ranks by model time and steps, wall time is reported.
- Compaction (C3c) and delta notes (C4) are new harness code; the library stays unmodified, so they live in the harness and are smoke-tested first.

## Pilot 2026-10-20 (measured budget; not scored)

Runs: `projects/agent_memory_study/runs/r015_pilot_std` (step cap 20), `runs/r015_pilot_lim` (step cap 8 + token budget 78k), and `runs/r015_pilot_cap8_nobudget` (step cap 8 only: the budget step of `harness/r015_pilot.sh` crashed on a file-encoding error, since fixed, so this run went ahead without the budget and is kept as a cap-only arm). Projects T01, T02 (simple), L05, L06 (intermediate) and A01, A02 (advanced) × 12 paths × 1 repeat = 72 units and 792 sessions per arm. Machine time: about 75 min wall per arm for the standard arm and 41 min for the limited arm, at 72 units in parallel. Provider failed attempts were 0–0.4% per path.

**Measured budget.** Standard arm, per-session prompt + completion tokens: p50 54k, p75 96k, p90 156k. Limited token budget = half the p90 = **78k per session**. At step cap 8 the cap binds first for the file paths (1–4 budget hits in 66 sessions); the budget binds for replay (C3 38/66, C3c 34/66), because the replayed history counts as prompt.

Standard arm by path (6 units each; priced at measured caching):

| path | success | fact | tokens | cached | calls | cost |
|---|---|---|---|---|---|---|
| C0 | 0 | 0.70 | 3.7M | 79% | 549 | $1.03 |
| C1 | 4 | 0.96 | 4.3M | 81% | 584 | $1.16 |
| C1t | 3 | 0.94 | 4.2M | 79% | 567 | $1.06 |
| C2 | 4 | 0.97 | 4.5M | 80% | 627 | $1.15 |
| C2-t | 3 | 0.94 | 4.4M | 81% | 606 | $1.11 |
| C2-h | 4 | 0.95 | 4.6M | 80% | 624 | $1.17 |
| C2-d | 4 | 0.97 | 4.8M | 83% | 658 | $1.20 |
| C2a | 3 | 0.81 | 5.4M | 83% | 659 | $1.30 |
| C2x | 4 | 0.97 | 6.6M | 84% | 742 | $1.57 |
| C3 | 5 | 0.99 | 13.0M | 97% | 322 | $1.20 |
| C3c | 5 | 0.99 | 5.3M | 88% | 290 | $0.78 |
| C4 | 3 | 0.96 | 4.2M | 82% | 597 | $1.09 |

By tier: success, standard / limited arm, out of 24 units: simple 21 / 18, intermediate 11 / 3, advanced 10 / 4. Mean priced cost per session (standard): simple $0.016, intermediate $0.017, advanced $0.018. Limited arm by path: success C3 4, C3c 4, C2-d 3, C2-h 3, all others 0–2; C0's fact score falls to 0.13.

**Task checks.** No tier is trivial. Advanced is hard but not impossible (A01 2/12, A02 8/12 standard). **L06 is defective:** its hidden test `test_fact_report_count` (the last summary line is "sensors: N") checks a decision that none of its 8 prompts states, so L06 cannot succeed. It scored 0/12 here and 0/15 in R-014 `runs/r014_scored`, in every condition. In R-014 the defect lowers every condition equally but caps intermediate success. Owner decision (2026-10-20): fix the prompt. R-015 uses **L06f** (`tasks/r015_l06f.py`): L06 with the decision stated in session 2, otherwise identical; it passes the project checker. L06 stays frozen as R-014 ran it, and the R-014 record has a correction note.

**Projection** (from the standard arm's per-session cost and time, concurrency 100):
- Screen (12 paths × 8 intermediate projects × 2 repeats): 1,536 sessions, about 92M tokens, $27 priced, about 1 h wall.
- Confirm, if 6 paths survive (16 projects × 3 repeats × 3 tiers): 9,504 sessions, about 780M tokens, $166 priced, about 340 session-hours, about 4–5 h wall. Then the limited and near-unlimited arms on about 2 finalists: about 1.5 h each.
- Total: about 9–10 h, within the 24 h cap.
- The confirm stage needs 14 more simple and 14 more advanced projects; only 2 of each exist.

## Pre-registration (approved by the owner 2026-10-20, as drafted)

Everything below is fixed before the screen starts. A change after approval is a dated amendment in this section, with its reason, made before the stage it affects.

**Model and harness.** minimax-m3.1-flash-free via OpenCode Go; harness at the commit that starts the screen (smolagents-ts `dist`, unmodified). Containers: `docker ps` must show no `r013=1` containers before a stage. `harness/sweep.mjs` runs before every stage, and the run sweeps again at the end and logs the count. A stage that leaves containers behind is reported.

**Paths.** All 12: C0, C1, C1t, C2, C2-t, C2-h, C2-d, C2a, C2x, C3, C3c, C4, as built in the pilot and unchanged. C0 (floor), C2 (R-014's pack) and C3 (R-014's cheapest) are references and are never dropped.

**Projects.**
- Simple: T01, T02 + 14 new.
- Intermediate: L05, L06f, L07, L08, L09, L10f, L11–L20.
- Advanced: A01, A02 + 14 new.

Every project passes `tasks/check_long.py` and `tasks/check_facts.py` (each flag read by hand, and the reading recorded). It is then frozen before the stage that uses it. New projects are not tried with the agent before they are scored.

**Budget arms.**
- *Standard:* step cap 20, no token budget.
- *Limited:* step cap 8 and a per-session token budget of 78,000. The budget is the sum of prompt + completion tokens over the session's calls, with cached tokens counted in full. It is half the pilot's standard-arm p90.
- *Near-unlimited:* step cap 60, no token budget, session timeout ×3.

The budget counts tokens as sent, not as billed, so it **penalises replay**: C3 and C3c resend their history on every call. Their budget hits are reported separately (pilot: C3 38/66, C3c 34/66 sessions).

**Outcomes.**
- Primary: success per unit (every hidden test except stale passes).
- Cost: priced cost per success at measured caching. The no-cache and prefix-bound prices are sensitivity checks.
- Speed: model time per success (summed call latency). Wall time is reported but not ranked.
- Secondary: fact score, stale errors, step-cap and budget-hit sessions, and the cost of failed units.

**Ranking (owner rule).**
1. *Acceptable:* success within δ = 5 points of the best path at that tier and arm.
2. The lowest cost per success among acceptable paths wins.
3. Costs within 10% are tied, and the tie is broken by speed.

The Pareto frontier, a cost-first ranking, a speed-first ranking and the raw table are also reported.

**Statistics.** Paired bootstrap over projects: units are paired by project × repeat, with 10,000 resamples, seed 15, and 95% percentile CIs. Success differences are in points. Cost per success is compared as a ratio of totals. Analysis script: `harness/analysis/r015.py`, written and run on the pilot runs before the screen's results are read.

**Stage 1, screen.**
- Intermediate L05, L06f, L07, L08, L09, L10f, L11, L12 (the first 8 by id) × 12 paths × 2 repeats, standard arm. That is 192 units, 1,536 sessions, about 1 h.
- Drop rule: a non-reference path P is dropped only if
  - (a) the CI of success(P) − success(best) lies entirely below −δ, or
  - (b) the CI of cost-per-success ratio P / Q lies entirely above 1 for some path Q whose success point estimate is ≥ P's.
- *Survivor cap:* if more than 8 paths survive, the 3 references and the 5 non-reference survivors with the lowest point cost per success go on. The rest are reported as "not dropped, not confirmed".

**Stage 2, confirm.**
- Survivors × 3 tiers × 16 projects × 3 repeats, standard arm.
- Projected before the start from the screen's measured per-session cost and time (about 4–5 h for 6 paths).
- *Repeat rule:* after 3 repeats, if the CI half-width of the deciding comparison is > δ in a tier, that tier gets one more repeat, up to a cap of **5**. The deciding comparison is the winner vs the runner-up on success, or on the cost ratio if both are acceptable.

**Stage 3, limited and near-unlimited arms.**
- Finalists: in each tier, the winner and runner-up from the confirm stage, plus C2 and C3. That is at most 6 paths.
- They run on all 3 tiers × 16 projects × 3 repeats in each arm, ranked by the same rule.

**Stopping and reruns.**
- The whole study stays within 24 h machine time (raised to 45 h by the owner on 2026-10-21, after the screen showed the provider rate limit caps throughput at concurrency 16). If a stage's projection would exceed what is left, I stop and report before starting it.
- A unit with a harness error or more than 5% failed provider attempts is rerun once. Reruns are listed, and an infrastructure failure is never scored as a task failure.
- No result is read for ranking until its stage is complete.

**Predictions** (from the pilot; for scoring how well the pilot predicted, not gates):
- (P1) C3c is the cheapest acceptable path at the intermediate tier.
- (P2) At the advanced tier, C3's cost per success exceeds C3c's by more than 10%.
- (P3) In the limited arm, the replay paths keep the most success despite the budget penalty.
- (P4) C2x costs more than C2 with no gain in success.
- (P5) No single pack file's removal (C2-t, C2-h, C2-d) drops success by more than δ.

**Stage log.**
- 2026-10-20: the owner approved the pre-registration as drafted ("Approve the R-015 pre-registration as drafted; start the screen and build the 28 new projects in parallel").
- 2026-10-20: the screen started: `runs/r015_screen`, 192 units, concurrency 100. Harness at de7cdc7 plus the uncommitted container-leak fix (session labels and end sweep). That fix was smoke-tested in `runs/_smoke_leak`: 12 budget aborts, 0 containers left.
- 2026-10-20: `harness/analysis/r015.py` was written and run on `runs/r015_pilot_std` and `runs/r015_pilot_lim` before any screen result was read. It covers:
  - priced cost three ways: measured caching, no caching, and the prefix bound, which assumes each call reuses the previous call's prompt;
  - the bootstrap, which resamples projects and keeps all their repeats;
  - the ranking, the Pareto frontier, the drop rule and the survivor cap;
  - rerun detection: a session that ended in an error other than the step cap or a cancellation, or a unit with more than 5% failed provider attempts.

  A resample with no successes keeps an infinite cost per success, using nearest-rank percentiles. On the pilot, the rule kept C0, C2, C3 and C3c in both arms. That is a check of the code, not a result: the pilot has 5–6 projects × 1 repeat.

## Tunings proposed from R-013/R-014 (for owner review)

1. **Primary measure = success, not fact score.** Fact score sat at 94–97% for every memory path in R-014; success (all tests) separated the paths (63–79%).
2. **Keep C3 as a strong baseline.** On 8 sessions it was cheapest and fastest; the advanced tier exists to find where it breaks.
3. **Count failure cost.** Step-cap sessions are the most expensive and were uneven across paths (C0 0.83 per unit, C3 0). Report cost per success *and* cost of failed sessions.
4. **Price three ways.** Measured caching on the free endpoint (44–69% in the smoke test) need not match the paid model; report measured, none and prefix bound.
5. **Power the stale test.** Stale errors were near the floor (4 of 16 projects differed); the advanced tier's fact chains should raise them.
6. **Drop C2g** (no difference in two studies).

## Debugging our own pack: separate study (proposed R-016)

Recommendation: a separate R-016 that reuses R-015's ablation method on the real AI_Research pack with a set of real repository tasks. The subject (our own files), the tasks (real repo work, not synthetic projects) and the measures (rule compliance, routing) differ, so mixing them would blur both answers. R-016 starts after R-015's screen stage, when we know which ablations are informative.

## Owner decisions 2026-10-20

1. Acceptable success: within **5 points** of the best path at that tier and budget (CI reported).
2. Intermediate tier: **reuse R-014's L05–L20**, so results compare directly with R-014.
3. Limited arm: **both** a step cap (about 8) and a per-session token budget (new harness code, smoke-tested first).
4. Machine time: **24 h maximum** for the whole study ("approve 24 h as max, but speed up as much as possible"); each stage reports its projection, and the run uses the highest concurrency the machine holds (R-014 ran clean at 100).
5. After the pilot (2026-10-20): the token budget stays as raw prompt + completion tokens, cached counted in full, and the pre-registration states that this penalises replay; every path goes into the screen, with C3c as the leading candidate only.
6. Audit for hidden tests no prompt supports (R-014 + pilot runs, memory paths, stale tests excluded): L06 `report_count` 0/45 (fixed as L06f); **L10 `test_fact_slug_clean` 1/12**: the test needs leading and trailing spaces dropped (`"  Jazz   Night "` → `"jazz-night"`), which no prompt states; it alone cost 11 of 12 memory units their success in R-014. Owner approved the fix: L10f (`tasks/r015_l10f.py`) adds the trimming to session 5's deferred step; R-014 note added. A static screen, `tasks/check_facts.py` (each fact test's expected strings, not its input data, must appear in some prompt), was then run on all 26 projects with facts: it flags L06 and L10, passes L06f and L10f, and its 28 other flags were each read by hand and are stated in a prompt (the test uses other example data, or the value is computed from stated rules), so no further defects. New projects must pass it before they are run. A01 is valid (A01 C3 passed every fact test); its `test_basic` (0.20) depends on SKU facts, so it is not a pure basic test.
- 2026-10-20: **the screen was stopped and restarted (infrastructure failure, not scored).**
  - About 30 min into the first attempt, Docker Desktop's engine began answering every API call with HTTP 500. Sessions then failed with "The Docker sandbox could not start" and ran to the step cap, and 0 of 192 units had finished.
  - I stopped the run, restarted Docker Desktop and swept the 271 containers that the kill had left. The attempt is kept unscored in `runs/_aside/r015_screen_dockerfail`.
  - The screen was relaunched in a fresh `runs/r015_screen` at concurrency 48 instead of 100. Concurrency is an operational setting, not part of the design. A watcher now stops waiting if Docker fails two health checks 2 min apart.
- 2026-10-21: the relaunched screen finished all 192 units, but r015.py flagged 111 of them for rerun. The cause was 688 sessions that ended on HTTP 429 from OpenCode Go ("Upstream request failed"). These are provider rate-limit failures, not task results. They hit nearly every repeat-2 unit plus the late sessions of some repeat-1 units.
  - Under the pre-registered rerun rule, the 111 units were moved unscored to `runs/_aside/r015_screen_429` and rerun once in `runs/r015_screen` at concurrency 16.
  - Before the cause was found, r015.py had printed a partial analysis. It rested on only 4 paired projects. It is discarded and not used for any decision.
  - In the rerun, 110 units ran at concurrency 16 in about 2.5 h, plus L12_C4_r2 separately. No 429s occurred, and 0 containers were left.

**Screen result** (2026-10-21; `runs/r015_screen`; 192 units; all 8 projects paired; no reruns pending; full output in `runs/r015_screen.analysis.txt`). The table gives success (95% CI), priced $ per success (95% CI) and model-seconds per success:

| path | success | $/succ | s/succ | screen decision |
|---|---|---|---|---|
| C3 | 93.8% [81.2, 100] | 0.0907 [0.079, 0.102] | 612 | reference, kept |
| C3c | 81.2% [56.2, 100] | 0.1093 [0.088, 0.153] | 801 | dropped (b) vs C3, ratio CI [1.00, 1.59] |
| C2-h | 100% [100, 100] | 0.1366 [0.117, 0.155] | 1105 | survives (best success) |
| C2a | 93.8% [81.2, 100] | 0.1442 [0.130, 0.161] | 1158 | dropped (b) vs C3 [1.43, 1.76] |
| C1t | 87.5% [62.5, 100] | 0.1594 [0.125, 0.221] | 1347 | dropped (b) vs C3 [1.39, 2.37] |
| C2-d | 87.5% [68.8, 100] | 0.1676 [0.142, 0.211] | 1404 | dropped (b) vs C3 [1.51, 2.33] |
| C2 | 87.5% [68.8, 100] | 0.1785 [0.148, 0.226] | 1468 | reference, kept |
| C1 | 81.2% [56.2, 100] | 0.1888 [0.131, 0.313] | 1490 | dropped (b) vs C3 [1.34, 3.57] |
| C2x | 87.5% [68.8, 100] | 0.2365 [0.190, 0.305] | 1663 | dropped (b) vs C3 [1.95, 3.63] |
| C2-t | 68.8% [43.8, 93.8] | 0.2409 [0.174, 0.375] | 1833 | dropped (a) vs C2-h [−56.2, −6.2] |
| C4 | 62.5% [31.2, 87.5] | 0.2542 [0.173, 0.454] | 2062 | dropped (a) vs C2-h [−68.8, −12.5] |
| C0 | 0% | inf | inf | reference, kept |

- **Survivors (4):** C0, C2, C3 and C2-h. The survivor cap does not bind.
- **C3c:** its ratio CI's lower bound is 1.00 to two places. It lies strictly above 1, so the rule drops it, but only just.
- **Screen ranking:** the screen ranking is not the study's ranking. The point estimates have C2-h as the most successful path and C3 as the cheapest. C3 is within δ of C2-h, so it is the cheapest acceptable path.
- **Projected confirm stage:** 4 paths × 3 tiers × 16 projects × 3 repeats = 576 units.
  - Throughput: measured at about 44 units/h, at concurrency 16, the highest setting that ran with no 429s.
  - Wall time: about 13 h. The pre-registration estimated 4–5 h, assuming 72-way parallelism with no rate limit.
  - Machine time used so far: about 9 h (pilot about 2.6, Docker failure 0.5, screen 3.4, 429 rerun 2.5). About 15 h is left.
  - The confirm stage fits within that. Stage 3 (two arms on up to 4 finalists, about 1,150 units, about 26 h) does not. Under the stopping rule, I report this at a gate before starting the confirm stage.
- 2026-10-20: the 28 new projects are built and frozen, and none has been tried with the agent:
  - simple T03–T16, from `tasks/r015_simple2.py`, documented in `tasks/R015_NEW_SIMPLE.md`;
  - advanced A03–A16, 21 sessions and 13–14 facts each, from `tasks/r015_advanced2.py`, documented in `tasks/R015_NEW_ADVANCED.md`.

  All 28 pass check_long. check_facts flags T05, T16 and A04. I read the T16 and A04 flags by hand: in both, the fact is stated in a prompt and the flagged strings are test inputs. A04's name trimming and its ids starting at 1 are both stated in session 1. The T05 flag was read by the build session and reported as the same kind (test inputs echoed back).
- 2026-10-21: the owner raised the machine-time cap to 45 h. The confirm stage started at 04:20Z.
  - Output: `runs/r015_confirm`.
  - Paths: the 4 survivors, C0, C2, C3 and C2-h.
  - Projects: T01–T16, L05, L06f, L07–L09, L10f, L11–L20 and A01–A16.
  - Settings: 3 repeats, step cap 20, concurrency 16.
- 2026-10-21 05:22Z: the owner asked for more speed. The machine can take about 50 containers; the limit is the provider. At concurrency 16, 6 of 4,078 calls failed (0.15%).
  - I stopped the run at 98 finished units. I moved the 16 unfinished units, unscored, to `runs/_aside/r015_confirm_partial`, along with the c16 log, and swept the 16 containers they left.
  - I relaunched at concurrency 32. If provider failures climb, it drops back.
  - Concurrency is operational. It does not change the design.

- 2026-10-21 10:15Z — Confirm stage paused on a provider daily quota. From 09:34Z every call got HTTP 429 ("Rate limit exceeded", `retry-after` ≈ 49,700 s, so the reset is about 00:00Z). The runner kept going and failed units, so it was stopped at 10:12Z. 510/576 units are complete and clean. 37 units hit by the quota (34 incomplete, 3 complete with >5% failed attempts, per the rerun rule) were moved to `runs/_aside/r015_confirm_quota429/` and are not scored. They and the 29 units not yet started (66 in all) will run after the reset at concurrency 32. Lesson: the limit is a daily call quota, so concurrency changes how fast we reach it, not how much fits into a day. Stage 3 and any extra repeats will need to be planned in daily quota blocks. The 429 watcher missed this because it searched steps files while the 429s are recorded in the calls files.
- 2026-10-22 01:46Z, **confirm stage complete:** 576/576 units, 0 reruns, no 429s after the 00:00Z resume. Ten sessions hit the 20-step cap; they are scored as task outcomes. Analysis is in `runs/r015_confirm_analysis.txt`, seed 15.
  - Overall success: C3 93.1%, C2 82.6%, C2-h 79.2%, C0 4.2%. $/success: C3 0.181, C2-h 0.219, C2 0.224.
  - C3 wins every tier (cheapest-acceptable, by speed, Pareto):
    - T: C3, C2 and C2-h are all at 87.5%; C3/C2 $/succ ratio CI [0.54, 0.63].
    - L: C3 93.8% vs C2-h 89.6%; ratio CI [0.50, 0.65].
    - A: C3 97.9% vs C2 72.9%; success diff CI [+12.5, +39.6].
  - Repeat rule: T and L are decided, since both runner-ups are acceptable and their cost-ratio CIs lie below 1. In A, the success-diff half-width is 13.5 > δ, so A gets a 4th repeat (64 units, about 1 h). This follows the rule as written, even though the winner is already clear.
  - Machine time used: about 16 h of 45 h.
- 2026-10-22, **tier A, repeat 4:** 64/64 units, with no 429s.
  - Tier A with 4 repeats: C3 96.9% at $0.395/succ; C2 75.0% at $0.474; C2-h 60.9%; C0 0%.
  - The runner-up, C2, is still not acceptable. The success-diff CI is [+9.4, +35.9], with half-width 13.3 > δ, so tier A gets a 5th repeat. That is the cap.
  - The half-width barely moved. The spread comes from differences between projects, which more repeats cannot shrink. Output is in `runs/r015_confirm_analysis_r4.txt`.
- 2026-10-22 ~05:00Z, **tier A, repeat 5 (cap reached):** 64/64 units, with no 429s.
  - Tier A over 5 repeats (320 units): C3 95.0% at $0.399/succ and 968 s/succ; C2 75.0% at $0.472; C2-h 63.7%; C0 0%.
  - The success-diff CI for C3 − C2 is [+6.2, +36.2], half-width 15.0, still > δ at the cap. The rule allows no more repeats, so tier A is reported as is. C3 wins on success, because the CI excludes 0. The $/succ ratio CI [0.67, 1.01] does not separate the two on cost.
  - Output is in `runs/r015_confirm_analysis_r5.txt`.
- 2026-10-22 05:02Z, **stage 3 started:**
  - **Finalists:** each tier's winner and runner-up (T: C3, C2; L: C3, C2-h; A: C3, C2), plus C2 and C3, which gives C3, C2 and C2-h.
  - **Size:** 3 paths × 48 projects × 3 repeats × 2 arms = 864 units.
  - **Projection:** about 14–20 h. That fits the cap, since about 19 h of 45 are used. The calls are estimated from confirm-stage calls per unit (T 30, L 64, A 164, standard arm): about 30–70k, which spans about 2 UTC days of quota.
  - **Run order:** the limited arm first (`runs/r015_lim`: step cap 8, token budget 78k), then the near-unlimited arm (`runs/r015_unlim`: step cap 60, session 135 min). Both run at concurrency 32 with the 429 quota watcher. Runner: `harness/r015_arms.sh`.
- 2026-10-22 07:48Z, **stage 3 paused on the daily quota:**
  - From about 07:39Z, every call returned HTTP 429. The watcher stopped the run, by which point the limited arm had 268 of 432 results.
  - The two units it flagged for harness errors (A01_C2-h_r2 and A02_C2-h_r2) and the 32 unfinished units were moved to `runs/_aside/r015_lim_quota429`. They are not scored.
  - The remainder resumes automatically at 00:05Z on 2026-10-23.
  - Today's quota covered about 260 limited-arm units plus 194 confirm-stage units. Quota, not machine time, is now the binding limit.
- 2026-10-23 00:05–00:20Z, **resume:**
  - Docker Desktop was not running at 00:05Z, so the first resume died at the container sweep. I started Docker again.
  - The second launch began while the engine was still answering HTTP 500. I stopped it and moved its 32 unfinished units to `runs/_aside/r015_lim_restart` (not scored).
  - I relaunched cleanly from 266 limited-arm results. This was infrastructure only; nothing was scored from these attempts.
- 2026-10-23 00:25Z, **stage 3 halted: model deprecated.**
  - OpenCode Go now answers `minimax-m3.1-flash-free` with HTTP 410, `ModelDeprecated`.
  - The resumed runner had stalled. I stopped it and moved its 32 unfinished units to `runs/_aside/r015_lim_deprecated`.
  - The limited arm keeps 266/432 results, all from 2026-10-22. The near-unlimited arm never started.
  - The screen and the confirm stage are complete and stand. Stage 3 cannot be finished on the same model. Owner gate: decide how to treat stage 3.
- 2026-10-24, **closed by the owner on the confirm results.** A probe of OpenCode's 12 free models found none callable from the harness:
  - Go endpoint: every `*-free` id answers 400 "Model is unavailable", and longcat-2.5-preview-free answers 429 "Endpoint is unavailable".
  - Zen endpoint: 403 `FreeTierError` ("free tier can only be used from within OpenCode"); beam-free answers 403 `RegionError`.

  The owner ruled out paid models ("No paid models. Close R-015 on the confirm results and report stage 3 as a partial."). Stage 3 is therefore reported below as a partial, unranked arm.

## Result (2026-10-24)

**Answer.** On minimax-m3.1-flash-free at the standard budget, **C3 (full transcript replay) is the cheapest path that still succeeds at every tier.** Overall it reaches 93.1% success at $0.181 per success, against C2-h at $0.219 and C2 at $0.224. Confirm stage, 576 units plus tier A repeats 4–5; seed 15.

| tier | winner | runner-up | deciding comparison | decided? |
|---|---|---|---|---|
| T (simple) | C3 87.5% | C2 87.5% (acceptable) | $/succ ratio CI [0.54, 0.63] | yes, at 3 repeats |
| L (intermediate) | C3 93.8% | C2-h 89.6% (acceptable) | $/succ ratio CI [0.50, 0.65] | yes, at 3 repeats |
| A (advanced) | C3 95.0% | C2 75.0% (not acceptable) | success diff CI [+6.2, +36.2], half-width 15.0 | at the 5-repeat cap; C3 wins on success, cost not separated (ratio CI [0.67, 1.01]) |

C0 (no memory) reached 4.2% overall, so memory is needed at every tier.

**Stage 3, partial and unranked.** The limited arm (step cap 8, 78k-token budget) kept 266 of its 432 units before the model was retired. The near-unlimited arm never ran.
- Coverage: T has repeats 1–2 complete, L has repeats 1–2 complete, and A has repeat 1 complete with repeat 2 half done. Paths are unequally covered in A (C3 30 units, C2 22, C2-h 20).
- The pre-registered ranking needs complete, paired stages, so no ranking, CI or prediction verdict is drawn from these units. The descriptive counts are in `runs/r015_lim_partial_summary.txt`:

| tier | path | units | success | $/succ | budget-hit / step-capped sessions |
|---|---|---|---|---|---|
| T | C3 | 34 | 88.2% | 0.032 | 9 / 4 of 136 |
| T | C2-h | 32 | 68.8% | 0.059 | 0 / 58 of 128 |
| T | C2 | 32 | 43.8% | 0.098 | 0 / 69 of 128 |
| L | C3 | 32 | 68.8% | 0.106 | 64 / 1 of 256 |
| L | C2-h | 32 | 37.5% | 0.270 | 1 / 137 of 256 |
| L | C2 | 32 | 25.0% | 0.446 | 5 / 168 of 256 |
| A | C2 | 22 | 27.3% | 0.992 | 28 / 296 of 462 |
| A | C2-h | 20 | 20.0% | 1.293 | 27 / 222 of 420 |
| A | C3 | 30 | 13.3% | 1.395 | 436 / 4 of 630 |

  Read descriptively:
  - The pack paths fail mainly on the 8-step cap.
  - C3 fails mainly on the token budget, which counts replayed history in full. That is the penalty the pre-registration named.
  - C3 leads in T and L, but in A, where the replayed history is longest, it is last.

  A follow-up on another model would have to rerun the whole arm. These units are never pooled with it.

**Predictions** (from the pilot; scored from the screen and confirm stages):
- P1 (C3c cheapest acceptable at L): **not supported.** C3c was dropped at the screen against C3.
- P2 (C3's $/succ over C3c's by >10% at A): **not testable.** C3c did not reach the confirm stage.
- P3 (replay paths keep the most success in the limited arm): **not scored.** Stage 3 is incomplete.
- P4 (C2x costs more than C2 with no gain): **supported at the screen.** $0.237 vs $0.179 per success, both at 87.5%.
- P5 (no single pack-file removal drops success by >δ): **not supported.** C2-t was 68.8% vs C2's 87.5% at the screen and was dropped under rule (a). C2-h and C2-d stayed within δ.

**Limits.**
- One model, which has now been retired.
- Tier A's deciding success CI stayed wider than δ at the repeat cap, because the spread comes from between-project variance.
- Costs use the paid sibling's list price.
- Machine time used: about 19 h of the 45 h cap.

