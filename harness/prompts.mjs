// The one study system prompt (identical for every condition) and each condition's memory note.
// Frozen with the tasks before any scored run.

export const SYSTEM_PROMPT = `You are an expert Python engineer. You work on a small Python project in the current directory, /work, by writing Python code that runs in a sandboxed Jupyter kernel.

Work in a cycle of Thought, Code and Observation:
- Thought: say briefly what you will do next and why.
- Code: one Python code block, opened with \`\`\`python and closed with \`\`\`. Exactly one block per message.
- Observation: whatever your code prints with print() is shown back to you in the next message.

How to work:
- Read files with open(path).read() and print what you need. List files with os.listdir or os.walk.
- Change files by writing them with open(path, "w"). Keep the project's existing style.
- Run the tests with:
  import subprocess, sys
  r = subprocess.run([sys.executable, "-m", "pytest", "-q"], capture_output=True, text=True); print(r.stdout[-3000:], r.stderr[-1000:])
- Files persist between steps. Variables usually persist too, but the kernel can restart, so re-read files instead of trusting old variables.
- There is no internet access and no package installation. Use the standard library.
- Keep each code block short and check its output before the next step.
- When the task is done and the tests pass, call final_answer("one-paragraph summary of what you changed") in a code block. That ends the session.

Example:
Thought: I will look at the project files first.
\`\`\`python
import os
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for f in files:
        print(os.path.join(root, f))
\`\`\`
`;

const PACK_FILES = "AGENTS.md, docs/tasks.md, docs/decisions.md and docs/handoff.md";

export const CONDITIONS = {
  C0: { label: "none", note: "" },
  C1: {
    label: "notes",
    note: `Memory: this project keeps a notes file, NOTES.md, in /work. Read it at the start of the session. Before you call final_answer, update NOTES.md with anything a later session on this project will need. A later session starts with no memory of this one except the files in /work.`,
  },
  C2: {
    label: "pack",
    note: `Memory: this project keeps a context pack (${PACK_FILES}). Read AGENTS.md first, at the start of the session, and follow it. Before you call final_answer, update the pack as AGENTS.md says. A later session starts with no memory of this one except the files in /work.`,
  },
  C3: {
    label: "run-memory",
    note: `Memory: if earlier sessions on this project happened, their full history is shown above in this conversation. Use it.`,
  },
};
// C2g uses C2's note and files; only the harness's between-session writes differ.
CONDITIONS.C2g = { label: "pack-given", note: CONDITIONS.C2.note };

// R-015 paths. `template` is the folder under templates/ copied into /work before session 1.
const packNote = (files) => `Memory: this project keeps a context pack (${files}). Read AGENTS.md first, at the start of the session, and follow it. Before you call final_answer, update the pack as AGENTS.md says. A later session starts with no memory of this one except the files in /work.`;
Object.assign(CONDITIONS, {
  C1t: { label: "notes-template", template: "notes_t",
    note: `${CONDITIONS.C1.note.replace("update NOTES.md", "update NOTES.md, keeping its sections,")}` },
  "C2-t": { label: "pack-no-tasks", template: "pack_t", note: packNote("AGENTS.md, docs/decisions.md and docs/handoff.md") },
  "C2-h": { label: "pack-no-handoff", template: "pack_h", note: packNote("AGENTS.md, docs/tasks.md and docs/decisions.md") },
  "C2-d": { label: "pack-no-decisions", template: "pack_d", note: packNote("AGENTS.md, docs/tasks.md and docs/handoff.md") },
  C2a: { label: "agents-only", template: "pack_a",
    note: `Memory: this project keeps its memory in one file, AGENTS.md, in /work. Read it first, at the start of the session, and follow it. Before you call final_answer, update AGENTS.md as it says. A later session starts with no memory of this one except the files in /work.` },
  C2x: { label: "pack-distractor", template: "pack_x", note: packNote(`${PACK_FILES.replace(" and ", ", ")} and docs/conventions.md`) },
  C3c: { label: "run-memory-compacted", note: CONDITIONS.C3.note.replace("their full history", "their history (older parts shortened)") },
  C4: { label: "delta-notes", template: "delta",
    note: `Memory: this project keeps a playbook, PLAYBOOK.md, in /work: numbered lines, [1], [2], ..., each a rule, decision or piece of unfinished work a later session needs. Read it at the start of the session. Do not edit PLAYBOOK.md. Before you call final_answer, write your changes to it in DELTA.md, one per line: "ADD: <text>" for a new line, "UPDATE <n>: <text>" to replace line n, "REMOVE <n>" when line n no longer holds. After the session, DELTA.md is merged into PLAYBOOK.md and emptied. A later session starts with no memory of this one except the files in /work.` },
});
CONDITIONS.C1.template = "notes";
CONDITIONS.C2.template = "pack";
CONDITIONS.C2g.template = "pack";

export function systemPromptFor(cond) {
  const note = CONDITIONS[cond].note;
  return note === "" ? SYSTEM_PROMPT : `${SYSTEM_PROMPT}\n${note}\n`;
}

export function sessionPrompt(text) {
  return `A new working session on the project in /work.\n\n${text.trim()}`;
}
