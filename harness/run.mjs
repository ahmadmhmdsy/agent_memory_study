// R-013 harness: runs (task, condition, repeat) units of three sessions each, then the hidden tests.
// Usage: node harness/run.mjs --out runs/pilot --tasks P1,P2 --conds C0,C2 --reps 1 --max-steps 30
// A unit whose result.json exists is skipped, so a stopped run resumes where it left off.
import { cpSync, existsSync, mkdirSync, readFileSync, writeFileSync, appendFileSync, rmSync } from "node:fs";
import { basename, join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

import { CONDITIONS, sessionPrompt, systemPromptFor } from "./prompts.mjs";
import { makeModel, MODEL_ID, scrub } from "./model.mjs";
import { cliRuntime, runHiddenTests, sweepContainers } from "./runtime.mjs";

const LIB = "file:///E:/python_projects/smolagents_ts/packages";
const { CodeAgent, noopLogger, stepToJSON } = await import(`${LIB}/core/dist/index.js`);
const { createDockerExecutor } = await import(`${LIB}/exec-remote/dist/docker.js`);

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

function parseArgs(argv) {
  const a = { out: "runs/pilot", tasks: "P1,P2,P3,P4", conds: "C0,C1,C2,C2g,C3", reps: "1",
    "max-steps": "30", "exec-timeout": "60000", "session-minutes": "45", concurrency: "1",
    "token-budget": "0", "compact-tokens": "24000" };
  for (let i = 0; i < argv.length; i += 2) a[argv[i].replace(/^--/, "")] = argv[i + 1];
  return {
    out: resolve(ROOT, a.out),
    tasks: a.tasks.split(","),
    conds: a.conds.split(","),
    reps: Number(a.reps),
    maxSteps: Number(a["max-steps"]),
    execTimeout: Number(a["exec-timeout"]),
    sessionMs: Number(a["session-minutes"]) * 60_000,
    concurrency: Number(a.concurrency),
    // R-015 limited arm: a session ends once its prompt + completion tokens reach this (0 = off).
    tokenBudget: Number(a["token-budget"]),
    // C3c: the replayed history is shortened once it is estimated above this many tokens.
    compactTokens: Number(a["compact-tokens"]),
  };
}

/** C3's checkpoint store: one JSON file per checkpoint name, kept with the run. */
class FileRunStore {
  constructor(dir) { this.dir = dir; mkdirSync(dir, { recursive: true }); }
  path(name) { return join(this.dir, `${name}.json`); }
  async save(name, snapshot) { writeFileSync(this.path(name), JSON.stringify(snapshot)); }
  async load(name) { return existsSync(this.path(name)) ? JSON.parse(readFileSync(this.path(name), "utf8")) : undefined; }
}

/**
 * C3c's store: C3's checkpoint, shortened on load once its estimated size (characters / 4) is
 * above `limit` tokens. The latest session is always kept whole. Stage 1 cuts the observations of
 * older sessions to 300 characters; stage 2 then drops older sessions' steps, oldest first, keeping
 * each session's task and final answer. Deterministic, no model call; the library is unchanged.
 */
class CompactingStore extends FileRunStore {
  constructor(dir, limit, logPath) { super(dir); this.limit = limit; this.logPath = logPath; }
  static size(steps) {
    let n = 0;
    for (const s of steps) n += (s.task?.length ?? 0) + (s.modelOutput?.length ?? 0) + (s.observations?.length ?? 0);
    return Math.round(n / 4);
  }
  async load(name) {
    const steps = await super.load(name);
    if (!steps) return steps;
    const before = CompactingStore.size(steps);
    if (before <= this.limit) return steps;
    const starts = steps.map((s, i) => (s.kind === "task" ? i : -1)).filter((i) => i >= 0);
    const lastStart = starts[starts.length - 1];
    let out = steps.map((s, i) => (i < lastStart && s.kind === "action" && (s.observations?.length ?? 0) > 300
      ? { ...s, observations: `${s.observations.slice(0, 300)}\n[... shortened]` } : s));
    let stage = 1;
    for (let k = 0; k < starts.length - 1 && CompactingStore.size(out.filter(Boolean)) > this.limit; k++) {
      stage = 2;
      const [a, b] = [starts[k], starts[k + 1]];
      out = out.map((s, i) => (s && i > a && i < b && s.kind === "action" && !s.isFinalAnswer ? null : s));
    }
    out = out.filter(Boolean);
    appendFileSync(this.logPath, JSON.stringify({ t: new Date().toISOString(), before, after: CompactingStore.size(out),
      stepsBefore: steps.length, stepsAfter: out.length, stage }) + "\n");
    return out;
  }
}

/** C4: merges the session's DELTA.md lines into the harness-owned playbook, then rewrites both files. */
function mergeDelta(ws, unitDir, sessionNo) {
  const book = join(unitDir, "playbook.json");
  const lines = existsSync(book) ? JSON.parse(readFileSync(book, "utf8")) : [];
  const deltaPath = join(ws, "DELTA.md");
  const delta = existsSync(deltaPath) ? readFileSync(deltaPath, "utf8") : "";
  const applied = { add: 0, update: 0, remove: 0, bad: 0 };
  for (const raw of delta.split(/\r?\n/)) {
    const l = raw.replace(/^\s*[-*]\s*/, "").replace(/^`|`$/g, "").trim();
    if (!l || l.startsWith("#")) continue;
    let m;
    if ((m = l.match(/^ADD:\s*(.+)$/i))) { lines.push({ n: lines.length + 1, text: m[1].trim(), live: true }); applied.add++; }
    else if ((m = l.match(/^UPDATE\s*\[?(\d+)\]?:\s*(.+)$/i)) && lines[m[1] - 1]) { lines[m[1] - 1] = { ...lines[m[1] - 1], text: m[2].trim(), live: true }; applied.update++; }
    else if ((m = l.match(/^REMOVE\s*\[?(\d+)\]?\s*$/i)) && lines[m[1] - 1]) { lines[m[1] - 1].live = false; applied.remove++; }
    else applied.bad++;
  }
  writeFileSync(book, JSON.stringify(lines, null, 1));
  const live = lines.filter((x) => x.live);
  // Numbers stay stable across sessions, so a removed line leaves a gap.
  writeFileSync(join(ws, "PLAYBOOK.md"), `# Playbook\n\n${live.length ? live.map((x) => `[${x.n}] ${x.text}`).join("\n") : "(empty)"}\n`);
  writeFileSync(deltaPath, "");
  appendFileSync(join(unitDir, "delta.jsonl"), JSON.stringify({ session: sessionNo, ...applied, live: live.length }) + "\n");
  return applied;
}

const NETWORK_RE = /\b(socket|urllib|requests|http\.client|httpx|aiohttp|pip\s+install|curl|wget)\b/;

/** C2g: the harness writes a session's facts into the pack before the next session starts. */
function writeGivenFacts(ws, facts, sessionNo) {
  if (!facts) return;
  const tag = `(session ${sessionNo})`;
  for (const d of facts.decisions ?? []) appendFileSync(join(ws, "docs/decisions.md"), `- ${d} ${tag}\n`);
  for (const t of facts.tasks ?? []) appendFileSync(join(ws, "docs/tasks.md"), `| ${t.task} | ${t.status} | ${sessionNo} |\n`);
  if (facts.handoff) appendFileSync(join(ws, "docs/handoff.md"), `\n## After session ${sessionNo}\n\n${facts.handoff}\n`);
}

function summarizeSteps(allSteps) {
  // C3 carries earlier sessions' steps; count only this session's (after its task step).
  let lastTask = -1;
  allSteps.forEach((s, i) => { if (s.kind === "task") lastTask = i; });
  const actions = allSteps.slice(lastTask + 1).filter((s) => s.kind === "action");
  const withCode = actions.filter((s) => typeof s.codeAction === "string" && s.codeAction.trim() !== "");
  const firstWrite = actions.findIndex((s) => /open\([^)]*['"][wa]['"]|write_text\(|\.write\(/.test(s.codeAction ?? ""));
  return {
    actionSteps: actions.length,
    stepsWithCode: withCode.length,
    stepErrors: actions.filter((s) => s.error).length,
    networkTouch: withCode.some((s) => NETWORK_RE.test(s.codeAction)),
    firstWriteStep: firstWrite === -1 ? null : firstWrite + 1,
  };
}

/** Totals over a session's successful calls; null fields count as 0, and `missing` counts them. */
function sumUsage(log) {
  const tot = { calls: 0, prompt: 0, completion: 0, cached: 0, cacheWrite: 0, reasoning: 0, maxPrompt: 0, missing: 0, failedAttempts: 0 };
  for (const c of log) {
    if (!c.ok) { tot.failedAttempts += 1; continue; }
    tot.calls += 1;
    if (c.prompt == null) tot.missing += 1;
    for (const k of ["prompt", "completion", "cached", "cacheWrite", "reasoning"]) tot[k] += c[k] ?? 0;
    tot.maxPrompt = Math.max(tot.maxPrompt, c.prompt ?? 0);
  }
  return tot;
}

async function runSession({ ws, cond, prompt, cfg, store, checkpoint, sessionIndex, unitDir }) {
  const replay = cond === "C3" || cond === "C3c";
  const stats = { calls: 0, callMs: 0, errors: [], tokenBudget: cfg.tokenBudget, budgetHit: false };
  const created = [], pending = [];
  const session = `${process.pid}-${basename(unitDir)}-s${sessionIndex + 1}`;
  const executor = createDockerExecutor({
    runtime: cliRuntime({ workspace: ws, created, pending, session }),
    readyAttempts: 120,
    readyIntervalMs: 500,
  });
  const agent = new CodeAgent({
    model: makeModel(stats),
    tools: [],
    executor,
    maxSteps: cfg.maxSteps,
    executionTimeoutMs: cfg.execTimeout,
    systemPrompt: systemPromptFor(cond),
    logger: noopLogger,
    ...(replay ? { store } : {}),
  });
  const controller = new AbortController();
  stats.onBudget = () => controller.abort();
  const timer = setTimeout(() => controller.abort(), cfg.sessionMs);
  const started = Date.now();
  let result, failure;
  try {
    result = await agent.run(prompt, {
      signal: controller.signal,
      ...(replay ? { checkpoint, reset: sessionIndex === 0 } : {}),
    });
  } catch (err) {
    failure = { name: err?.name, message: scrub(err?.message ?? err).slice(0, 2000) };
  } finally {
    clearTimeout(timer);
    await executor.dispose?.().catch(() => {});
    for (const id of created) await cliRuntime({ workspace: ws }).removeContainer(id).catch(() => {});
    // A create still running when the session was aborted: wait for it, then remove by label.
    await Promise.allSettled(pending);
    await sweepContainers(session).catch(() => {});
  }
  const steps = (result?.steps ?? agent.memory?.steps ?? []).map((s) => {
    try { return stepToJSON(s); } catch { return { kind: s.kind }; }
  });
  writeFileSync(join(unitDir, `s${sessionIndex + 1}.steps.json`), scrub(JSON.stringify(steps, null, 1)));
  // Every HTTP attempt with the provider's raw usage, kept for sessions that end in error too.
  writeFileSync(join(unitDir, `s${sessionIndex + 1}.calls.json`), scrub(JSON.stringify(stats.callLog, null, 1)));
  return {
    session: sessionIndex + 1,
    state: result?.state ?? "error",
    failure,
    output: result ? scrub(String(result.output ?? "")).slice(0, 2000) : null,
    tokenUsage: result?.tokenUsage ?? null,
    // From the call log, so it is never null (tokenUsage is null when the session errors).
    usage: sumUsage(stats.callLog),
    modelCalls: stats.calls,
    modelMs: stats.callMs,
    adapterRewrites: stats.rewrites ?? 0,
    providerErrors: stats.errors,
    wallMs: Date.now() - started,
    budgetHit: stats.budgetHit,
    ...summarizeSteps(steps),
  };
}

async function runUnit(task, cond, rep, cfg) {
  const unitId = `${task}_${cond}_r${rep}`;
  const unitDir = join(cfg.out, "units", unitId);
  if (existsSync(join(unitDir, "result.json"))) return "skipped";
  const ws = join(cfg.out, "ws", unitId);
  rmSync(ws, { recursive: true, force: true });
  rmSync(unitDir, { recursive: true, force: true });
  mkdirSync(unitDir, { recursive: true });

  const taskDir = join(ROOT, "tasks", task);
  const spec = JSON.parse(readFileSync(join(taskDir, "sessions.json"), "utf8"));
  cpSync(join(taskDir, "repo"), ws, { recursive: true });
  const tpl = CONDITIONS[cond].template;
  if (tpl) cpSync(join(ROOT, "templates", tpl), ws, { recursive: true });

  const store = cond === "C3c"
    ? new CompactingStore(join(unitDir, "c3store"), cfg.compactTokens, join(unitDir, "compaction.jsonl"))
    : new FileRunStore(join(unitDir, "c3store"));
  const sessions = [];
  for (let i = 0; i < spec.sessions.length; i++) {
    if (cond === "C2g" && i > 0) writeGivenFacts(ws, spec.sessions[i - 1].given, i);
    const rec = await runSession({
      ws, cond, cfg, store, unitDir, sessionIndex: i, checkpoint: unitId,
      prompt: sessionPrompt(spec.sessions[i].prompt),
    });
    if (cond === "C4") rec.delta = mergeDelta(ws, unitDir, i + 1);
    sessions.push(rec);
    appendFileSync(join(cfg.out, "sessions.jsonl"), JSON.stringify({ unit: unitId, task, cond, rep, ...rec }) + "\n");
    console.log(`${unitId} s${rec.session}: ${rec.state} steps=${rec.actionSteps} calls=${rec.modelCalls} ${Math.round(rec.wallMs / 1000)}s`);
  }

  const hidden = await runHiddenTests(ws, join(taskDir, "hidden"));
  const all = Object.entries(hidden.results);
  // R-014: test_stale* tests pass when the code follows the old version of a superseded fact.
  // They count stale-fact errors and are left out of success.
  const stale = all.filter(([n]) => n.startsWith("test_stale"));
  const tests = all.filter(([n]) => !n.startsWith("test_stale"));
  const facts = tests.filter(([n]) => n.startsWith("test_fact"));
  const result = {
    unit: unitId, task, kind: spec.kind, tier: spec.tier ?? "intermediate", cond, rep, model: MODEL_ID,
    maxSteps: cfg.maxSteps, tokenBudget: cfg.tokenBudget,
    // R-013 tasks have no stale tests, so their exit code still decides; with stale tests pytest's exit code is not usable.
    success: tests.length > 0 && tests.every(([, v]) => v === "PASSED") && (stale.length > 0 || hidden.exitCode === 0),
    // At least one fact test must run: a collection error leaves no results, and every() on [] is true.
    factPassed: facts.length > 0 && facts.every(([, v]) => v === "PASSED"),
    factScore: facts.length > 0 ? facts.filter(([, v]) => v === "PASSED").length / facts.length : 0,
    staleErrors: stale.filter(([, v]) => v === "PASSED").length,
    hidden,
    sessions,
  };
  writeFileSync(join(unitDir, "result.json"), JSON.stringify(result, null, 1));
  console.log(`${unitId}: success=${result.success} factScore=${result.factScore.toFixed(2)} stale=${result.staleErrors}`);
  return result;
}

const cfg = parseArgs(process.argv.slice(2));
for (const c of cfg.conds) if (!CONDITIONS[c]) throw new Error(`unknown condition ${c}`);
mkdirSync(cfg.out, { recursive: true });
const swept = await sweepContainers();
if (swept) console.log(`removed ${swept} leftover containers`);
writeFileSync(join(cfg.out, "config.json"), JSON.stringify({ ...cfg, model: MODEL_ID, started: new Date().toISOString() }, null, 1));

// Units in interleaved order (repeat, task, condition), so provider drift hits all conditions alike.
// --concurrency N runs up to N units at once; a unit's own sessions always run in order.
const queue = [];
for (let rep = 1; rep <= cfg.reps; rep++)
  for (const task of cfg.tasks)
    for (const cond of cfg.conds) queue.push([task, cond, rep]);

async function worker() {
  while (queue.length) {
    const [task, cond, rep] = queue.shift();
    try {
      await runUnit(task, cond, rep, cfg);
    } catch (err) {
      console.error(`${task}_${cond}_r${rep} harness error: ${scrub(err?.stack ?? err)}`);
      appendFileSync(join(cfg.out, "harness_errors.log"), `${new Date().toISOString()} ${task}_${cond}_r${rep} ${scrub(err?.stack ?? err)}
`);
    }
  }
}
await Promise.all(Array.from({ length: Math.max(1, cfg.concurrency) }, worker));
console.log(`end sweep: removed ${await sweepContainers().catch(() => "?")} leftover container(s)`);
console.log("done");
