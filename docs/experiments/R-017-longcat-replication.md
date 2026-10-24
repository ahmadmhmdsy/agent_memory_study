# R-017 — Does R-015's answer hold on a second model? (LongCat replication)

Status: **pre-registered 2026-10-21 (owner approved; D1–D3 as recommended).** Pilot running.

Code: `projects/agent_memory_study/` (the R-013/R-014/R-015 harness). Agent harness: smolagents-ts, imported from its built `dist`, unmodified (R-C-agent_memory_study.4).
Parent: M4 in `docs/01-project.md`; replicates the confirm stage of R-015 (T-022). Task: T-023.

## Explainer

**Question.** R-015 asks which way of carrying context between sessions is the cheapest one that still succeeds, on one model (MiniMax M3.1 Flash). R-017 asks: **if we run the same projects and the same paths on a different model, do we get the same answer?** R-015 itself says it "does not deliver a result for other models". R-017 is the cheapest way to get one.

**Why it matters.**
- A rule like "replay is cheapest on short projects, a pack on long ones" is only useful if it is not just a habit of one model.
- R-013 (LongCat) and R-014 (MiniMax) already disagreed in places. LongCat was more expensive per session and had a failure mode MiniMax lacks. So a second model is a real test, not a formality.

**Why LongCat, and why now.**
- It is the only other free model our key can use. Probe of 2026-10-21: every other free model is unavailable, blocked by country, or allowed only inside the OpenCode app. We do not work around those blocks.
- The provider's daily quota is counted per model. MiniMax is blocked until 00:00 UTC, but LongCat's quota is untouched, so R-017 can use time that is otherwise idle.

**What it is not.**
- It is not part of R-015 and does not change R-015.
- The two models' results are **never pooled** (same rule as the R-014 backup). Each model gets its own table.
- Agreement is judged per pre-registered comparison, not by averaging the two models.

**Design in one paragraph.** Run R-015's four confirm-stage paths on all 48 confirm projects × 3 repeats at the standard budget, on `longcat-2.5-preview-free`: C0 (no memory), C2 (full pack), C2-h (pack without the handoff file) and C3 (full transcript replay). That is 576 units, the same as R-015's confirm stage. Rank them with R-015's rule (success first, then cost, then speed). Then compare each key result with MiniMax's and label it "replicates", "consistent" or "contradicts".

**Honest limits (read before approving).**
1. **It inherits MiniMax's screen.** R-015 dropped 8 of 12 paths using MiniMax data. A path that MiniMax dropped but LongCat would favour is invisible here. That matters most for C3c (compacted replay): it was a borderline drop on MiniMax, and it is built for long projects, where LongCat's large prompts hurt most. *Owner decision D1:* add C3c as a fifth path (+144 units).
2. **LongCat collapses.** In R-013, 20 of 360 units had a "collapsed" session: the model's replies are cut to 13–20 tokens with no code, and the session stalls until the step cap. In replay (C3), a collapse in session 1 carried into later sessions in 3 of 4 cases, because the model copies its own empty replies from the history. That is model behaviour, not a provider fault (R-013 correction, raw-endpoint probe). So it hits C3 hardest by design. *Owner decision D2:* how collapses are counted (proposal below).
3. **Model-specific adapter.** LongCat often writes its own tool-call markup instead of a python block. `normalizeLongcat` in `harness/model.mjs` rewrites it, applying the same rule on every path (R-013). It is part of "LongCat as we can use it", and the rewrite rate per path is reported.
4. **Shared machine.** While the MiniMax confirm stage finishes (66 units after the reset), both runs share the machine. Wall time is inflated, so speed is ranked on model time (summed call latency), as in R-015.
5. **Unknown limits.** We do not know whether LongCat's daily quota matches MiniMax's (about 50k calls or 500M tokens per UTC day), or whether there is also an account-wide limit. R-017 could hit MiniMax's quota or slow it down. Both runs are watched for 429s in `calls.json`.
6. **Price is a proxy.** LongCat is free here. Cost is priced at the LongCat-2.0 list price used in R-013 (input $0.30, output $1.20, cached $0.006 per 1M). The MiniMax M3 price is used as a sensitivity check, so cost differences that come only from the price list can be told apart from those that come from token use.
7. **Context window.** On the advanced tier, replay resends 20+ sessions of history. LongCat uses about 3× MiniMax's tokens on matched units, so C3 may reach LongCat's context window sooner. Calls rejected for length are counted and reported per path, and are scored as task failures. They are not infrastructure errors, because hitting the limit is the behaviour being tested.
8. **Blindness.** This pre-registration is written before any MiniMax confirm-stage result has been read (only pooled projections were looked at, never per path). If it is approved after MiniMax's confirm results are read, that is recorded in the stage log.

**Measured LongCat vs MiniMax ratio** (R-014 pilot; the 7 units both models ran, L01/L02 × C0–C3; steps.json): LongCat used **1.66× the steps** and **3.12× the tokens** (4.88M vs 1.57M).

**Projection.**
- *Calls and tokens.* R-015's confirm stage takes about 37k calls and about 410M tokens on MiniMax. On LongCat: about 60k calls and about 1.3B tokens. That is more than one day's quota if LongCat's matches MiniMax's, so plan for **2–3 UTC days**.
- *Machine time.* MiniMax's confirm stage takes about 126 h of model time. LongCat is slower per call; R-014 had one 1,222-s session. Estimate 3–4× MiniMax's model time, which is roughly 12–18 h wall at concurrency 32, not counting quota waits.
- *Cost.* About $400 priced at the list price. Nothing is billed.
- The pilot replaces these estimates with measured ones.

## Pilot (measured budget; not scored)

- **Units.** T01, T02, L05, L06f, A01, A02 × C0, C2, C2-h, C3 (+ C3c if D1 is approved) × 1 repeat at the standard arm. That is 24 units, or 30 with C3c.
- **Output.** `runs/r017_pilot`. These projects already ran in R-015's pilot, so no new project is tried before being scored.
- **What it measures.** Calls, tokens, model time and wall time per unit and tier, failed attempts, 429s, adapter rewrite rate, collapse rate, and context-length rejections.
- **Gates.** The scored run starts only if all of these hold:
  - (a) failed provider attempts are ≤ 5% in every path;
  - (b) at most 2 of the 6 units in any one path collapse;
  - (c) the measured projection fits the caps in "Stopping" below.
  If any gate fails, I stop and report.

## Pre-registration (approved by the owner 2026-10-21)

Everything below is fixed at approval. A change after approval is a dated amendment, with its reason, made before the stage it affects.

**Model and harness.**
- Model: `longcat-2.5-preview-free` via OpenCode Go, which is the harness default when `R013_MODEL` is unset. Run with `R013_MODEL=longcat-2.5-preview-free` set explicitly.
- Harness: the commit used by R-015's confirm stage. The key is read from `.env` by name only: OPENCODE_API_KEY.
- Containers: `harness/sweep.mjs` runs before and after each stage, and the count is logged.

**Paths.** C0, C2, C2-h and C3, as built for R-015 and unchanged. C3c is added if D1 is approved. All of them are references; none is dropped.

**Projects.** R-015's confirm set, frozen:
- simple: T01–T16;
- intermediate: L05, L06f, L07, L08, L09, L10f, L11–L20;
- advanced: A01–A16.

**Arm.** Standard only: step cap 20, no token budget, R-015's session timeout. The limited and near-unlimited arms are not part of R-017 (see "Deferred").

**Repeats.** 3, fixed. No adaptive repeats: the quota makes extra repeats cost a day each. If the CI of a key comparison is wider than δ, that is reported, not resolved by running more.

**Outcomes.** Same as R-015:
- *Primary:* success per unit (every hidden test except stale passes).
- *Cost:* priced cost per success at measured caching, using LongCat-2.0 list prices. Sensitivity checks: no caching, the prefix bound, and MiniMax M3 prices.
- *Speed:* model time per success.
- *Secondary, reported per path:* fact score, stale errors, step-cap sessions, collapse rate, adapter rewrite rate, and context-length rejections.

**Ranking.** R-015's owner rule, per tier:
1. A path is acceptable if its success is within δ = 5 points of the best.
2. The lowest cost per success among acceptable paths wins.
3. Costs within 10% are tied, and the tie is broken by model time.

The Pareto frontier and the raw table are also reported.

**Statistics.** Paired bootstrap over projects: units are paired by project × repeat, with 10,000 resamples, seed 17, and 95% percentile CIs. The analysis script is `harness/analysis/r015.py` with one addition: a `--price` option (`minimax` | `longcat`), with `minimax` as the default so R-015 is unchanged. The option is tested on the R-017 pilot before any scored result is read.

**Collapse handling (D2; proposal).**
- *Primary:* collapsed units are scored as they ran, as failures if they fail. Collapse is LongCat behaviour, and R-013 showed it is not a provider fault, so rerunning it away would hide a real cost of using this model, especially for replay.
- *Sensitivity:* the same analysis is run with collapsed units excluded, using `harness/collapsed.py` with R-013's definition: at least half of a session's action steps are cut replies (no code, ≤ 30 output tokens).
- Both are reported, with the collapse rate per path and tier.
- *Alternative for the owner:* rerun collapsed units once, as R-013 did, and keep the first attempts as the sensitivity check.

**Cross-model agreement (the replication result).** For each comparison below, I compute LongCat's paired bootstrap CI and give it a label:
- **replicates:** the CI excludes the null (0 points, or a ratio of 1) on the same side as MiniMax's point estimate;
- **consistent:** the point estimate is on the same side, but the CI includes the null;
- **contradicts:** the CI excludes the null on the opposite side.

If MiniMax's own CI includes the null, the label is "both null" when LongCat's also does, and otherwise it is reported as "LongCat-only effect".

Key comparisons, per tier (3 tiers × 5 = 15 labels; there is no correction for multiplicity, and the count is stated):
- K1: success, C2 − C0
- K2: success, C3 − C2
- K3: success, C2-h − C2
- K4: cost per success, C3 / C2
- K5: cost per success, C2-h / C2

There is also one winner label per tier:
- *same winner:* LongCat's winner is MiniMax's winner;
- *winner acceptable:* MiniMax's winner is acceptable on LongCat and within 10% of LongCat's winner on cost;
- *different:* anything else.

**Stopping, quota and reruns.**
- *Concurrency.* Containers from the two runs together stay at or below 48. R-017 runs at 16 while the MiniMax confirm stage is running and at 32 after it ends.
- *Quota.* A watcher reads every `s*.calls.json` (not `steps.json`, which misses 429s). On the first sustained 429s, which means more than 20 in 5 minutes:
  - the runner is stopped;
  - the affected units are moved aside;
  - the run resumes after the next 00:00 UTC reset.
  A quota stop is never scored as a task failure. The quota usage per day (calls and tokens) is recorded, since that is a new fact about LongCat.
- *Interaction with MiniMax.* If MiniMax starts getting 429s while R-017 runs and its own quota is not exhausted, R-017 pauses first. R-015 has priority.
- *Caps.* At most 30 h of machine time, not counting quota waits, and at most 4 UTC days. If the projection after the pilot exceeds either cap, I stop and report before the scored run.
- *Reruns.* A unit with a harness error or more than 5% failed provider attempts is rerun once (R-015's rule). Collapse is not an infrastructure failure (see D2).
- *Reading results.* No result is read for ranking until all 576 units are complete. MiniMax's per-path confirm results are not read for R-017 before R-017's run is complete, apart from what R-015 itself needs.

**Predictions** (from R-013 and R-014; for scoring, not gates):
- (Q1) Every memory path beats C0 by more than δ at every tier (K1 replicates).
- (Q2) C3's collapse rate is the highest of the four paths.
- (Q3) C3's cost per success relative to C2 (K4) is higher on LongCat than on MiniMax at the advanced tier, because LongCat's larger prompts are resent on every call.
- (Q4) K3 (dropping the handoff file) is "consistent" or "both null" at every tier: the handoff file carries little on either model.
- (Q5) At least one tier has a "different" winner.

**Deferred.** The limited and near-unlimited arms are not run on LongCat. That is decided after R-015's stage 3 and after R-017's standard arm, because it depends on R-015's finalists and on the measured LongCat quota.

**Owner decisions needed.**
- **D1:** add C3c? I recommend yes. It adds 144 units, or about 25% more quota and time.
- **D2:** collapse handling. I recommend scoring collapses as they ran, with exclusion as the sensitivity check. The alternative is R-013-style reruns.
- **D3:** approve the caps (30 h machine time, 4 UTC days) and running in parallel with the MiniMax confirm stage, with R-015 having priority.

**Stage log.**
- 2026-10-21: drafted. Blind to MiniMax's per-path confirm results. The LongCat/MiniMax ratio was measured on R-014 pilot units only.
- 2026-10-21: the owner approved R-017 ("also approve R-017") and asked that LongCat work go ahead while MiniMax is blocked, with MiniMax's pending units kept until it is callable again. The owner did not name D1–D3, so the recommended options apply: D1, C3c is added (5 paths, 720 scored units); D2, collapses are scored as they ran, with exclusion as the sensitivity check; D3, the caps and the parallel run with R-015 taking priority. Still blind to MiniMax's per-path confirm results.
- 2026-10-21: `harness/analysis/r015.py` gained `--price {minimax,longcat}` (default minimax) and `--seed`. Checked on `runs/r015_pilot_std`: the default output is unchanged, and `--price longcat` changes only the cost columns.
- 2026-10-21 11:05–13:06Z: the pilot (`runs/r017_pilot`, concurrency 30) was stopped by the quota watcher after 24 of 30 units, with 89 HTTP 429s, mostly on advanced units. A probe at 13:07Z returned 200, so this was rate limiting, not a daily quota block.
  - **Gate (a) failed.** Failed provider attempts were 15–25% per path (C0 17%, C2 15%, C2-h 16%, C3 18%, C3c 25%), against a limit of 5%. By status:
    - 503 "Upstream request failed: Endpoint is unavailable": 243;
    - no response ("fetch failed"): 271;
    - 429: 89.
  - Gate (b) passed: 0 collapsed units.
  - Measured per unit (calls / model-s / Mtok): simple 49 / 1,212 / 0.50, intermediate 92 / 1,589 / 1.03, advanced 204 / 3,354 / 3.07. Projected for 720 units: about 83k calls, 1.1B tokens and 410 h of model time, about 13 h wall at concurrency 32, if the failures go away.
  - Per the pre-registration, I stopped and reported. No scored run was started.
- 2026-10-21 ~13:15Z, **amendment (owner):** "Rerun the R-017 pilot at concurrency 8 into a new run dir; if failed attempts are under 5% per path, start the scored run at that concurrency." The pilot is rerun in `runs/r017_pilot_c8`; the first pilot run is kept. If gate (a) passes, the scored run uses concurrency 8 instead of 16/32. The caps are unchanged and still apply before the scored run starts.
- 2026-10-21 ~13:20Z, **the concurrency-8 pilot did not start.** Every unit failed at import with `ERR_MODULE_NOT_FOUND: @smolagents-ts/core`. At 13:01Z, during a review-remediation commit made in another session, `smolagents_ts/packages/*/node_modules` lost its pnpm workspace links. No model calls were made, and the log is kept at `runs/r017_pilot_c8.log`. The rerun waits until the library's install is restored. Per the standing rule, I did not touch the library.
- 2026-10-21, at the owner's request: `pnpm install --frozen-lockfile` in smolagents_ts restored the workspace links, with no tracked change. A lesson was added to `smolagents_ts/docs/memory/general.md`. The concurrency-8 pilot starts automatically once the imports load (job waits 5 min to settle).
- 2026-10-21 14:06–15:22Z, **concurrency-8 pilot (`runs/r017_pilot_c8`) failed gate (a) again.** The quota watcher stopped it at 11/30 units. Failed attempts per path: C0 13.0%, C2 12.4%, C2-h 16.0%, C3 20.4% and C3c 9.2%. The failures were 59 × 429 ("Upstream request failed: Endpoint is unavailable"), 37 fetch failures and 4 × 500. The 429s started at 14:11Z, five minutes into the run, and continued with successes in between, so this is upstream capacity rather than a hard daily block. A probe at 15:22Z also returned 429. Per the pre-registration I stopped and reported; no scored run was started.
- 2026-10-21 ~15:30Z, **owner decision:** "drop longcat (keep as last free model to use)". R-017 is parked: LongCat is the last-resort free model and no further LongCat runs will be made unless the owner reopens this study. The data from the two pilots is kept.
