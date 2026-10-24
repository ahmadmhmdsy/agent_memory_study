// The pinned model, wrapped so that transient provider errors are retried and every call is counted.
// The wrapper answers generateStream with one chunk from a non-streaming call, so a retry never
// replays half a stream into the agent.
import { randomUUID } from "node:crypto";
import { readFileSync } from "node:fs";

const MODELS = "file:///E:/python_projects/smolagents_ts/packages/models/dist/index.js";
const { OpenAICompatibleModel } = await import(MODELS);

// R013_MODEL picks another OpenCode Go model (e.g. deepseek-v4.1-flash); the scored run used longcat.
export const MODEL_ID = process.env.R013_MODEL || "longcat-2.5-preview-free";
const BASE_URL = "https://opencode.ai/inference/go/openai/v1";

/** Reads one key by name from the AI_Research .env. The value is never logged. */
function envKey(name) {
  const text = readFileSync("E:/python_projects/AI_Research/.env", "utf8");
  for (const line of text.split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m && m[1] === name) return m[2].replace(/^["']|["']$/g, "");
  }
  throw new Error(`${name} not found in .env`);
}

const API_KEY = envKey("OPENCODE_API_KEY");

export function scrub(text) {
  return String(text).split(API_KEY).join("<key>");
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/**
 * Model adapter (R-013 pilot finding). longcat often writes its native tool-call markup instead of
 * a ```python block, e.g. `<longcat_tool_call>python\n<code>\n```</longcat_arg_value>\n</longcat_tool_call>`.
 * When that markup comes before any fenced block, the first call's code is rewritten into one
 * ```python block, with the text before it kept as the thought. Same rule in every condition.
 * Returns null when nothing needs rewriting.
 */
export function normalizeLongcat(text) {
  const tag = text.indexOf("<longcat_tool_call>");
  if (tag === -1) return null;
  const fence = text.indexOf("```");
  if (fence !== -1 && fence < tag && /^```[a-z]*\s*\n/.test(text.slice(fence))) return null;
  const end = text.indexOf("</longcat_tool_call>", tag);
  let body = text.slice(tag + "<longcat_tool_call>".length, end === -1 ? undefined : end);
  body = body
    .replace(/<longcat_arg_key>[\s\S]*?<\/longcat_arg_key>/g, "")
    .replace(/<\/?longcat_[a-z_]+>/g, "")
    .replace(/^[ \t]*(python|py|code|bash|sh)?[ \t]*\n/, "")
    .replace(/^[ \t]*```[a-z]*[ \t]*$/gm, "");
  const code = body.replace(/^\s*\n/, "").replace(/\s+$/, "");
  return `${text.slice(0, tag).trimEnd()}\n\`\`\`python\n${code}\n\`\`\``;
}

/**
 * The provider's raw usage for one HTTP attempt. The library keeps only prompt and completion
 * counts, so the harness reads the response body itself (rule R-C-agent_memory_study.5): cached
 * and cache-write tokens, reasoning tokens, finish reason, the model id served, and timing.
 */
function rawUsage(status, body, startedAt, ms) {
  const u = body?.usage ?? {};
  const pd = u.prompt_tokens_details ?? {};
  const cd = u.completion_tokens_details ?? {};
  return {
    t: new Date(startedAt).toISOString(),
    ms,
    status,
    model: body?.model ?? null,
    finish: body?.choices?.[0]?.finish_reason ?? null,
    prompt: u.prompt_tokens ?? null,
    completion: u.completion_tokens ?? null,
    cached: pd.cached_tokens ?? u.cached_tokens ?? null,
    cacheWrite: pd.cache_write_tokens ?? u.cache_write_tokens ?? u.cache_creation_input_tokens ?? null,
    reasoning: cd.reasoning_tokens ?? u.reasoning_tokens ?? null,
    cost: u.cost ?? body?.cost ?? null,
    usage: body?.usage ?? null,
  };
}

/** One wrapped model per agent session (one x-opencode-session id per conversation). */
export function makeModel(stats) {
  stats.callLog ??= [];
  let pending = null;
  async function recordingFetch(url, init) {
    const startedAt = Date.now();
    const res = await fetch(url, init);
    let body = null;
    try { body = await res.clone().json(); } catch {}
    pending = rawUsage(res.status, body, startedAt, Date.now() - startedAt);
    return res;
  }
  const inner = new OpenAICompatibleModel({
    model: MODEL_ID,
    baseUrl: BASE_URL,
    apiKey: API_KEY,
    fetch: recordingFetch,
    headers: { "x-opencode-session": randomUUID() },
    provider: "opencode-go",
    maxTokens: 8192,
  });

  async function generate(messages, options) {
    const waits = [5, 15, 30, 60, 120, 240];
    for (let attempt = 0; ; attempt++) {
      const started = Date.now();
      pending = null;
      try {
        const out = await inner.generate(messages, options);
        stats.calls += 1;
        stats.callMs += Date.now() - started;
        stats.callLog.push({ ...(pending ?? {}), attempt, wallMs: Date.now() - started, ok: true });
        // R-015 limited arm: once this session's prompt + completion tokens reach the budget, the
        // session is aborted; the agent sees the abort before its next model call.
        if (stats.tokenBudget > 0 && !stats.budgetHit) {
          const used = stats.callLog.reduce((n, c) => n + (c.ok ? (c.prompt ?? 0) + (c.completion ?? 0) : 0), 0);
          if (used >= stats.tokenBudget) { stats.budgetHit = true; stats.onBudget?.(); }
        }
        const fixed = typeof out.content === "string" ? normalizeLongcat(out.content) : null;
        if (fixed === null) return out;
        stats.rewrites = (stats.rewrites ?? 0) + 1;
        return { ...out, content: fixed };
      } catch (err) {
        stats.errors.push({ attempt, message: scrub(err?.message ?? err).slice(0, 500) });
        stats.callLog.push({ ...(pending ?? {}), attempt, wallMs: Date.now() - started, ok: false });
        if (options?.signal?.aborted || attempt >= waits.length) throw err;
        await sleep(waits[attempt] * 1000);
      }
    }
  }

  return {
    id: inner.id,
    provider: inner.provider,
    capabilities: inner.capabilities,
    generate,
    async *generateStream(messages, options) {
      const out = await generate(messages, options);
      yield { delta: out.content, finishReason: out.finishReason, usage: out.usage };
    },
  };
}
