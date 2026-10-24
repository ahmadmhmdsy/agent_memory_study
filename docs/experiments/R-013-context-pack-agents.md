# R-013 — Does a context pack help coding agents across sessions?

Status: **closed 2026-10-19. H1 passes (C2 − C0 +56.9 pts, p_holm = 0.0002); H2, H3 and H5 fail; H4 shows no difference.** Any memory beats none, but on these short tasks the pack is not shown to beat a plain NOTES.md or transcript replay, and every memory condition sits near the ceiling (86–96% success). The run used the approved design (24 tasks × 5 conditions × 3 repeats, longcat); deviations and corrections are dated notes under "Scored run 2026-10-19". Follow-up: a harder study on DeepSeek Flash, not yet approved.

Code: `E:\python_projects\agent_memory_study` (new folder; harness in Node, tasks in Python). Agent harness: smolagents-ts (`E:\python_projects\smolagents_ts`, https://github.com/ahmadmhmdsy/smolagents-ts), imported from its built `dist`, unmodified.
Parent: M4 in `docs/01-project.md`. This pack itself is the treatment being tested.

## Pre-registration

    ## R-013 — multi-session coding-agent success under five memory conditions
    - Question: does a structured context pack raise a coding agent's
      success on tasks that span several sessions, compared with no memory,
      a free-form notes file and smolagents-ts's own run memory?
    - Tasks: about 24 small Python tasks (final count set by the pilot), each
      worked over 3 sessions; each session is a fresh agent and a fresh
      sandbox. Each task hides one fact that only one session prompt states:
        constraint  — session 1 states a rule (e.g. money in integer cents,
                      rounded half-up) that session 3's work can break;
        decision    — session 1 records a design choice that the code does
                      not yet show (e.g. time values in milliseconds) and
                      session 3 must follow;
        unfinished  — session 2 is told to leave one listed step for later;
                      session 3 is told only to "finish the remaining work".
      One third of the tasks per kind. Hidden tests are never shown to the
      agent; tasks and tests are frozen before any scored run.
    - Conditions (only the memory differs; model, prompt, step cap, tools
      and task text are identical):
        C0 none        — the repo only;
        C1 notes       — told to read NOTES.md at start and update it before
                         finishing;
        C2 pack        — a minimal context pack (AGENTS.md, tasks, handoff,
                         decisions), told to read AGENTS.md first and update
                         the pack before finishing;
        C2g pack-given — the C2 pack, but the harness writes each session's
                         facts into it correctly before the next session
                         (the best case a pack can reach);
        C3 run memory  — no files; each session resumes the previous
                         session's full step history through smolagents-ts
                         RunStore checkpoints (reset: false).
    - Agent: smolagents-ts CodeAgent. The model writes Python; it runs in a
      Docker container (Jupyter kernel, Python 3.12, pytest) with the task
      repo mounted at /work. The only tool is final_answer: the agent reads,
      edits and tests files with its own code. One study system prompt for
      Python, the same for every condition, with the condition's memory
      instruction appended.
    - Model, pinned for the whole study: longcat-2.5-preview-free via
      OpenCode Go (owner's choice 2026-10-19; Gemini's free limits are too
      low for this size). Key from .env by name only: OPENCODE_API_KEY. If
      the model fails or is withdrawn, stop and ask the owner (paid
      deepseek-v4.1-flash is the owner's named fallback).
    - Repeats: 3 per (task, condition). 24 x 5 x 3 x 3 = 1,080 sessions.
    - Primary metric: task success = every hidden test passes after session 3.
    - Secondary: hidden-fact test passes; constraint violations
      (constraint tasks); tokens and model calls per task; steps before the
      first file write in sessions 2 and 3.
    - Hypotheses (difference in mean task success, in points):
        H1 C2 - C0 >= 15;
        H2 C2 - C1 >= 10;
        H3 C2 constraint violations < C1;
        H4 C2 - C3 >= 0 is reported two-sided: does a file pack match full
           run-history replay?
        H5 C2g - C2 > 0: how much the agent loses by keeping its own pack.
    - Test: per-task success rate averaged over repeats, paired by task.
      One-sided Wilcoxon signed-rank for H1-H3 and H5, two-sided for H4;
      Holm over H1-H5. A directional hypothesis passes if p_holm < 0.05 and
      the observed difference meets its threshold. Paired bootstrap 95% CIs
      for every difference.
    - Reported, not gated: results by hidden-fact kind; cost per success;
      how often C1/C2 agents skip writing their memory; all other pairs.
    - Prior: H1 likely passes; H2 uncertain (a good NOTES.md may carry most
      of the benefit); H3 uncertain; C3 strong on these short tasks; H5
      passes.
    - Pilot (not scored; its tasks are dropped from the scored suite):
      4 tasks x 5 conditions x 1 repeat, step cap 30, visible tests shown.
      Settings it picks, by these rules only:
        step cap      — the smallest of 10/20/30 at or above the 90th
                        percentile of steps used in sessions that finished;
        visible tests — shown, unless C0 task success exceeds 80% (then
                        hidden, and the pilot repeats);
        format        — the pinned model must produce a runnable code block
                        in at least 90% of steps, or stop and ask the owner;
        task count    — 24, cut to 15 if the pilot's calls per session make
                        24 take more than 4 weeks of wall time.
      Language: Python only. The smolagents-ts JavaScript sandbox (QuickJS)
      has no file system, so it cannot do these tasks.
    - Budget: no GPU. About 20-30k model calls on the free tier, $0. Docker
      image about 0.3 GB. Wall time about 5-7 weeks including task writing.
    - Stop condition: the pinned model is withdrawn or changes behaviour
      mid-study (then inconclusive, or restart all conditions on a new pin);
      a harness bug that affects one condition more than another (fix, then
      re-run every condition).
    - Known limitation: the container keeps a bridge network, because the
      host talks to the kernel through a published port. Agent code that
      touches the network is logged and reported.
    - Owner: Ahmad Mahmoud (approval); Claude (runs).
    - Date: approved 2026-10-19.

## Readiness check 2026-10-19

- OpenCode Go, from Python: `longcat-2.5-preview-free` answers on `https://opencode.ai/inference/go/openai/v1/chat/completions` with a Bearer key and a per-conversation `x-opencode-session` header. Cloudflare rejects the default Python User-Agent (403, error 1010); a custom User-Agent fixes it. About 3.5 s per short call. It is a reasoning model: reasoning tokens count toward `max_tokens`.
- Google, from Python: `gemini-3.5-flash-lite` and `gemini-3.1-flash-lite` answer via `generateContent` in about 1 s.
- smolagents-ts, from Node (built `dist`): `OpenAICompatibleModel` (longcat, session id via `headers`) and `GeminiModel` both returned a correct tool call for a two-integer `add` tool. Node's default User-Agent was not blocked.
- smolagents-ts findings (reported to the owner, not fixed; the study works around them without editing the library):
  1. The CodeAgent system prompt is written for JavaScript even with a Python executor (it says to use `console.log` and that the code cannot import or read files). The study passes its own `systemPrompt`.
  2. The Docker backend cannot mount a folder, change the image or turn off the network. The study injects its own `ContainerRuntime` through the `runtime` option.
  3. The process backend puts its own arguments first (`-u -c <prelude>`), so it cannot be wrapped in `docker run`.
  4. `reasoning_content` from OpenAI-compatible replies is dropped, so the model's reasoning is not logged.
  5. `extractCodeBlock` (`core/src/utils/parse-code-blocks.ts`) treats the first fence it meets as an opener, even a closing one. With no opening fence in the output it runs the text after a stray closing fence as code. The resulting `SyntaxError: line 1` observation does not show the code that ran, so the model cannot see what went wrong.

## Smoke test 2026-10-19

- Sandbox image `r013-sandbox:1` built from `docker/Dockerfile`. Package versions are in `agent_memory_study/docker/pip-freeze.txt` (pytest 9.1.1, ipykernel 7.4.0, jupyter-kernel-gateway 3.0.1, jupyter_client 8.10.0).
- First run, P1 under C2: the harness, containers, workspace mount and kernel all worked. Session 1 hit the 30-step cap with 29 of 30 steps failing. longcat wrote its native tool-call markup (`<longcat_tool_call>python … ```</longcat_arg_value></longcat_tool_call>`) instead of a ```python block, even though the prompt shows an example. Finding 5 then turned each step into a syntax error. The model blamed the environment and retried. The one step with a real ```python block ran correctly. Run stopped after session 1.
- **Model adapter (owner-approved deviation, 2026-10-19):** `normalizeLongcat` in `harness/model.mjs` rewrites a reply whose first code-like content is longcat markup into one ```python block holding the first call's code, keeping the text before it as the thought. Replies that already open with a fenced block are untouched. The rule is the same in every condition, and each session records `adapterRewrites`. Replaying it over the 30 recorded session-1 outputs gave 30 clean code blocks. It changes only the format of model output, never its content; it is part of the model interface, not of any memory condition.
- Rerun with the adapter, P1 under C2 (`runs/smoke`): all 3 sessions ended with `final_answer` (4, 10 and 22 steps; 508, 225 and 255 s). Hidden tests passed 7/7, including both fact tests (`success=true`). The adapter fired once in 36 calls. The agent recorded the int-cents and half-up rule in `docs/decisions.md` in session 1. longcat is slow: about 125 s per call in session 1, with about 6.8k output tokens per call, mostly reasoning. The first, failed run is kept as `runs/smoke_v0_no_adapter`.

## Pilot 2026-10-19 (not scored)

4 tasks × 5 conditions × 1 repeat, 60 sessions, step cap 30, visible tests shown, `agent_memory_study/runs/pilot`. 4.28 h of wall time; mean 4.3 min per session.

| task (kind) | C0 | C1 | C2 | C2g | C3 |
|---|---|---|---|---|---|
| P1 constraint | pass | pass | pass | pass | pass |
| P2 decision | pass | pass | fail (no `get_duration`; fact test not reached) | pass | pass |
| P3 unfinished | fail (no `reading_time`) | pass | pass | pass | pass |
| P4 decision | fail (no `todos.jsonl`) | fail (extra `{"next_id": 3}` line) | pass | fail (s3 hit the cap before `save`) | pass |

Unit success: C0 2/4, C1 3/4, C2 3/4, C2g 3/4, C3 4/4.

Pilot rules applied:
- Steps: p90 is 26, so the step cap stays at 30. 5 of 60 sessions hit it.
- C0 success is 50%, not above 80%, so visible tests stay shown.
- 98.3% of steps had a runnable code block, above the 90% bar, so no owner decision is needed.
- 1,080 sessions × 4.3 min ≈ 77 h sequential, under 4 weeks, so the study keeps 24 tasks.

Other observations:
- 18 provider errors (15 × HTTP 429, 3 × fetch failed). All were recovered by the retry wrapper.
- The adapter fired 20 times.
- One session touched a network name, which was blocked.

Task-design lessons for the 24 scored tasks:
- C0 passed both fact tests in P1 and P2. Half-up rounding via `Decimal` and integer milliseconds are choices a model makes without being told. Hidden facts must go against the default choice, as P3's deferred work and P4's file format did.
- P4 under C1 shows partial recall: JSON Lines was kept, but a header line was added. The fact tests should check the exact shape.

## Scored run 2026-10-19

- Tasks S01–S24 are generated by `agent_memory_study/tasks/make_scored_{constraint,decision,unfinished}.py` and listed in `tasks/SCORED_TASKS.md`. `check_scored.py` passes for all 24: the reference passes the visible and hidden tests, and a default variant, written without the fact, fails every `test_fact*` while passing the plain tests. The owner approved the list.
- Run: `runs/scored`, 24 tasks × 5 conditions × 3 repeats, step cap 30. Started 2026-10-19 as a detached process.
- **Provider fault at start.** The first session (S01_C0_r1 s1) used all 30 steps. Every reply was cut to about 20 output tokens, just before the code fence, and there was one HTTP 500 response. A raw request minutes later returned a normal reply, and smolagents-ts sends no stop sequences. This was treated as a provider fault, not model behaviour. The session's records were moved to `runs/scored/aside_provider_fault_1/`, and the unit was rerun from scratch. After the restart, the first two sessions ran cleanly: every step had code, with 0 errors.
- **Parallel units.** The 77 h serial estimate was cut by adding `--concurrency N` to `harness/run.mjs`: a pool of N workers takes units from the same interleaved (repeat, task, condition) queue, and each unit still runs its 3 sessions in order. Results do not depend on N; only wall time changes. The run was restarted twice, at N = 8 and then N = 24. Records of units cut off mid-way were moved to `runs/scored/aside_partial_serial_stop/` and `aside_partial_conc8_stop/`, and those units rerun from scratch. At N = 24: 55 sessions in 9.5 min (about 3 h for all 1,080), 2 HTTP 429 in 575 calls (both recovered), containers near 0% CPU.
- **Collapsed sessions recur.** 4 of the first 55 sessions at N = 24 show the start-of-run fault: replies cut to 13–20 tokens before the code fence on nearly every step, until the 30-step cap (S03_C0_r1 s1, all 3 sessions of S05_C3_r1). Single cut replies in 5 other sessions recovered on the next step. In S05_C3_r1 the fault carried into s2 and s3, a risk specific to conditions that carry earlier transcript. Whether to rerun collapsed units after the run is an owner decision.
- **Collapsed units rerun (owner decision 2026-10-19).** The main run ended at 19:45 AST with all 1,080 sessions and no harness errors. `harness/collapsed.py` marks a session as collapsed when at least half of its action steps are cut replies (no code, ≤ 30 output tokens); a unit is collapsed when any of its sessions is. It found 20 of 360 units spread across all five conditions. In C3, a collapse in s1 carried into s2 and s3 in 3 of the 4 collapsed C3 units. These units were moved to `runs/scored/aside_collapsed_1/` and rerun at N = 20. Two collapsed again (S03_C0_r1, S08_C3_r3), were moved to `aside_collapsed_2/`, and were rerun once more. Final state: 360/360 units, 1,080 sessions, 0 collapsed. The set-aside records are kept for a later look at fault rate by condition.
- **Correction: the cut replies are model behaviour, not a provider fault.** Probe 2026-10-19: the first turn of S03_C0_r1 s1 was sent 30 times in parallel to the raw endpoint, with no smolagents-ts and no harness. Results: 6/30 ended with `finish_reason: "stop"` after 13–17 tokens of preamble and no code ("I'll start by exploring the project structure."); 3/30 ran to the 8,192-token cap (`length`); 2/30 leaked `<longcat_tool_call>` markup. The model ends its turn as if it were handing off to a native tool call. A session collapses when the model then copies its own no-code replies from the history. The cause is neither smolagents-ts, the task design, nor parallelism; the serial run's first session collapsed the same way. The earlier "provider fault" wording above is superseded. Because the reruns resample a failure mode of the model, results are reported both with the reruns and with the first attempts.
- **Scored results (fact = hidden `test_fact*` pass; success = all hidden tests; 72 units per condition).** C0 success 34.7% / fact 56.9%; C1 86.1 / 88.9; C2 91.7 / 94.4; C2g 95.8 / 98.6; C3 90.3 / 93.1. Fact by kind (constraint / decision / unfinished): C0 33.3 / 75.0 / 62.5; C1 87.5 / 91.7 / 87.5; C2 95.8 / 95.8 / 91.7; C2g 95.8 / 100 / 100; C3 95.8 / 83.3 / 100. Paired by task against C0 (mean of 3 repeats), every memory condition is better on 12–15 of 24 tasks and worse on at most 1. The C0 fact rates for decision and unfinished tasks are higher than the failing defaults predict; this needs a check for facts leaking through code the agent wrote in sessions 1–2.
- **Sensitivity, first attempts of collapsed units instead of reruns (success / fact):** C0 33.3 / 55.6; C1 81.9 / 88.9; C2 86.1 / 94.4; C2g 94.4 / 98.6; C3 86.1 / 93.1. Fact rates move by at most 1.4 points, and the ordering of conditions is unchanged.
- **Scoring bug: vacuous fact passes (fixed 2026-10-19).** `factPassed` was `every()` over the `test_fact*` results. When the hidden tests failed at collection (for example `ImportError: cannot import name 'letter'`), there were no results, and `every()` on an empty list is true. 21 of 360 units had this: 15 C0 unfinished, 1 each in C0 decision, C1 decision, C2 unfinished, C2g constraint, C2g decision, and C3 constraint. `harness/run.mjs` now requires at least one fact test to run. `harness/rescore.py` writes the corrected values to `runs/scored/rescored.jsonl`; `result.json` stays as recorded. Every number below uses the rescored values, and the results bullet above is superseded.
- **Rescored results (fact %, 72 units per condition):** C0 34.7, C1 87.5, C2 93.1, C2g 95.8, C3 91.7. By kind (constraint / decision / unfinished): C0 33.3 / 70.8 / 0.0; C1 87.5 / 87.5 / 87.5; C2 95.8 / 95.8 / 87.5; C2g 91.7 / 95.8 / 100; C3 91.7 / 83.3 / 100. Success % is unchanged: C0 34.7, C1 86.1, C2 91.7, C2g 95.8, C3 90.3. With the first attempts of collapsed units in place of the reruns, fact % is C0 33.3, C1 86.1, C2 88.9, C2g 95.8, C3 87.5, and the ordering of conditions is the same.
- **C0 facts come from notes the agent wrote itself.** `harness/analysis/leak2.py` looks for a fact-specific marker in the code that sessions 1–2 used to write files. It counts a marker in a comment, docstring or prose line as a note, and one only in executable code as code. Lines in `final_answer`, `print` and grep calls are ignored. C0's fact rate is 21/32 in units with a note, 3/5 with code, and 1/35 with neither; the one exception is S15 r1, where case-insensitive lookup can be a guess. Examples: a README line "URL slugs in this project join words with `_`" (S11), the CSV-delimiter decision as a module docstring (S12), and the UTC format rule in a docstring (S13). Unfinished tasks in C0 score 0/24, because the agent never wrote the deferred item (c) down. So no fact leaks from the harness or the task repos. The C0 agent carries memory in the repo when a session-1 rule fits naturally into a docstring. C0 is therefore an "agent's own notes" baseline, not a true no-memory one.
- **Significance (`harness/analysis/sig.py`; per-task mean of 3 repeats, n = 24 tasks; exact sign test, Wilcoxon signed-rank, 10,000-resample bootstrap 95% CI over tasks).** Fact rate against C0: C1 +0.53 [0.38, 0.68], 18 tasks better / 0 worse, Wilcoxon p = 2e-4; C2 +0.58 [0.43, 0.72], 21/1, p = 6e-5; C2g +0.61 [0.44, 0.76], 19/0, p = 9e-5; C3 +0.57 [0.39, 0.74], 18/1, p = 1e-4. Success shows the same pattern (every p ≤ 2.3e-4). If C0 units with self-written carriers count as fails, the gains are +0.86 to +0.94 (p ≤ 1e-5). Between memory conditions, nothing is significant: the largest gap is C2g − C1 at +0.08 [−0.01, 0.18], p = 0.17, and Holm-adjusted p = 1 for all 6 pairs. Conclusion: every memory condition clearly beats C0. With 24 tasks and pass rates of 88–96%, this run cannot tell the memory conditions apart, because of a ceiling effect.
- **Model for later runs (owner decision 2026-10-19):** later runs use the paid DeepSeek Flash model in place of `longcat-2.5-preview-free`. This scored run stays on longcat.
- **Pre-registered test (`harness/analysis/prereg.py`, task success, rescored; n = 24 tasks, Holm over H1–H5).**
  - H1, C2 − C0: +56.9 pts [41.7, 70.8], 21 tasks better / 1 worse, p_holm = 0.0002. **PASS.**
  - H2, C2 − C1: +5.6 pts [−2.8, 15.3], p_holm = 0.85. **Fail** (threshold 10).
  - H3, constraint violations C1 − C2: +8.3 pts [0.0, 20.8], only 2 of 8 constraint tasks differ, p_holm = 0.85. **Fail.**
  - H4, C2 − C3: +1.4 pts [−9.7, 13.9], p = 1. Reported only: the file pack matches full history replay.
  - H5, C2g − C2: +4.2 pts [−4.2, 12.5], p_holm = 0.85. **Fail.**
  - Reported only:
    - Tokens per success (k in / k out): C0 161/27.5, C1 179/22.3, C2 225/22.1, C2g 148/15.9, C3 416/25.5. C3 costs about 1.9× C2 for the same success. *(superseded: see Correction 2026-10-20)*
    - Sessions 1–2 that never write memory: C1 9/144, C2 7/144, C2g 7/144.
  - Verdict: any memory beats none. On these short tasks, the pack is not shown to beat a plain NOTES.md, its curated (given) version, or full transcript replay. Every memory condition sits at 86–96% success, so a ceiling limits H2 and H5. The prior expected H2 and H3 to be uncertain and H5 to pass; H5 did not pass.
- **DeepSeek Flash check (owner request 2026-10-19; not scored, a model check only).** `R013_MODEL=deepseek-v4.1-flash` (the `harness/model.mjs` default stays longcat) was run on S03, S08, S15 and S17 × 5 conditions × repeat 1, giving 20 units and 60 sessions in `runs/deepseek_check/`. Results:
  - 0 collapsed units. 410/417 action steps carry code, with 0 provider errors and all 60 sessions ending in success.
  - About 17.6k input / 2.3k output tokens per session, against 62k / 5.8k on longcat.
  - Success: C0 3/4, and every memory condition 4/4. On the same units, longcat had C0 2/4, C1 3/4, C2 4/4, C2g 4/4 and C3 2/4.
  - S17 C0 still fails, since the deferred item is never written down. S08 C0 passes because the session-1 agent wrote the "Kelvin-return rule" into the code, the same self-written-note channel seen with longcat.
  - So DeepSeek fixes longcat's collapse failure mode and confirms the direction of the results. With 4 tasks it cannot test H2–H5. It also scores closer to the ceiling, so a DeepSeek rerun of this suite would compress the differences between memory conditions further.

## Correction 2026-10-20: token counts and cost

**What was wrong.** Tokens per success summed `tokenUsage` from `sessions.jsonl`, which is null for the 26 sessions that ended in error (step cap), so their calls counted as 0 (C0 3 sessions / 0.15M tokens, C1 3 / 1.49M, C2 7 / 3.78M, C2g 6 / 2.36M, C3 7 / 3.97M). `harness/analysis/prereg.py` now counts from the step logs via `harness/analysis/usage.py`. Success and fact results do not change.

Corrected tokens per success (k in / k out): C0 166/28.3, C1 201/24.4, C2 276/28.5, C2g 179/19.1, C3 472/30.8 (was C0 161/27.5, C1 179/22.3, C2 225/22.1, C2g 148/15.9, C3 416/25.5). C3 costs about 1.7× C2 for the same success (was 1.9×).

**Cost and time** (`harness/analysis/cost.py`), at the list price of LongCat-2.0 on OpenCode Go (2026-10-20, per 1M: input $0.30, output $1.20, cached read $0.006); the run used the free variant and the provider returns no cost. "Prefix" is the best case for a prefix cache (each call reuses the previous call's prompt in the same session).

| cond | success % | $ / unit, no cache / prefix | $ / success, prefix | cache saving | tokens k / unit | wall s / unit (median) | wall s / success |
|---|---|---|---|---|---|---|---|
| C0 | 34.7 | 0.029 / 0.016 | 0.045 | 46% | 68 | 477 (364) | 1,375 |
| C1 | 86.1 | 0.077 / 0.033 | 0.039 | 57% | 194 | 806 (632) | 936 |
| C2 | 91.7 | 0.107 / 0.042 | 0.046 | 61% | 279 | 1,016 (720) | 1,108 |
| C2g | 95.8 | 0.073 / 0.030 | 0.031 | 59% | 190 | 779 (531) | 813 |
| C3 | 90.3 | 0.161 / 0.056 | 0.062 | 65% | 454 | 956 (631) | 1,059 |

On these short 3-session tasks, C2g is the cheapest and fastest per success, and full replay (C3) the most expensive, the reverse of R-014's long projects. Lesson and rule: `docs/memory/agent_memory_study.md`, R-C-agent_memory_study.5.

