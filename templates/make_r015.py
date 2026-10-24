"""Builds the R-015 memory templates from templates/pack and templates/notes, so every variant
shares the same wording. Run once; the outputs are frozen with the tasks.

    python templates/make_r015.py

notes_t    C1t   NOTES.md with fixed sections
pack_t     C2-t  pack without docs/tasks.md
pack_h     C2-h  pack without docs/handoff.md
pack_d     C2-d  pack without docs/decisions.md
pack_a     C2a   AGENTS.md only, holding the tasks, decisions and handoff itself
pack_x     C2x   pack plus docs/conventions.md, a plausible file that has nothing the tasks need
delta      C4    PLAYBOOK.md (harness-owned) and an empty DELTA.md
"""
import os
import shutil

T = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "t": ("docs/tasks.md", "every task with its status: todo, doing, done or later."),
    "h": ("docs/handoff.md", "what the last session did and what the next session must do first."),
    "d": ("docs/decisions.md", "rules and design decisions that the code must follow. One line each, with the session that made it."),
}
START = {"t": None, "h": None, "d": "Follow every rule and decision in `docs/decisions.md`, even when the request does not repeat it."}
FINISH = {
    "t": "`docs/tasks.md`: update the status of each task you touched; add any task left for later.",
    "d": "`docs/decisions.md`: add every new rule or decision you were given or made. Never delete one; mark it superseded instead.",
    "h": "`docs/handoff.md`: rewrite it for the next session: what you did, what is unfinished, what to do first.",
}
X = ("docs/conventions.md", "release, commit and review conventions of the team.")


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf8", newline="\n") as f:
        f.write(text)


def agents(keep, extra=None):
    files = [FILES[k] for k in "tdh" if k in keep] + ([extra] if extra else [])
    lines = ["# AGENTS.md", "", "Read this file first in every session. It is the entry point to the project's memory.", "", "## Files", ""]
    lines += [f"- `{p}`: {d}" for p, d in files]
    reads = [f"`{FILES[k][0]}`" for k in "hdt" if k in keep] + ([f"`{extra[0]}`"] if extra else [])
    lines += ["", "## At the start of a session", "", f"1. Read {', '.join(reads[:-1]) + ' and ' + reads[-1] if len(reads) > 1 else reads[0]}."]
    if "d" in keep:
        lines.append(f"2. {START['d']}")
    lines += ["", "## Before you finish a session", ""]
    for i, k in enumerate([k for k in "tdh" if k in keep], 1):
        lines.append(f"{i}. {FINISH[k]}")
    return "\n".join(lines) + "\n"


def pack(name, keep, extra=None):
    out = os.path.join(T, name)
    shutil.rmtree(out, ignore_errors=True)
    w(os.path.join(out, "AGENTS.md"), agents(keep, extra))
    os.makedirs(os.path.join(out, "docs"), exist_ok=True)
    for k in keep:
        shutil.copy(os.path.join(T, "pack", FILES[k][0]), os.path.join(out, FILES[k][0]))
    return out


pack("pack_t", "hd")
pack("pack_h", "td")
pack("pack_d", "th")
out = pack("pack_x", "thd", X)
w(os.path.join(out, X[0]), """# Conventions

How the team works on this repository. None of this changes what the code does.

## Commits

- One logical change per commit. The subject line is at most 60 characters, in the imperative ("Add cart totals", not "Added cart totals").
- The body says why the change was made, wrapped at 72 characters.
- Reference the ticket at the end of the body as `Refs: ABC-123` when there is one.

## Branches

- Work on a branch named `<initials>/<short-topic>`, for example `al/export-fix`.
- Rebase on the main branch before asking for review; do not merge the main branch into a work branch.

## Review

- Every change is reviewed by one other person before it is merged.
- A reviewer checks that tests were added for new behaviour and that the change log entry is present.
- Review comments that are only style suggestions start with "nit:" and do not block the merge.

## Releases

- Versions follow semantic versioning: MAJOR.MINOR.PATCH.
- The change log, CHANGELOG.md, has an "Unreleased" section at the top; each merged change adds one line there.
- A release moves the "Unreleased" lines under a new version heading with the release date.
- Releases are cut on Tuesdays; urgent fixes may be released on any day as a PATCH version.

## Style

- Line length is at most 100 characters.
- Imports are grouped: standard library, third-party, local, with one blank line between groups.
- Public functions have a one-line docstring.
""")

out = os.path.join(T, "pack_a")
shutil.rmtree(out, ignore_errors=True)
w(os.path.join(out, "AGENTS.md"), """# AGENTS.md

Read this file first in every session. It is the project's whole memory: keep everything a later session needs here.

## At the start of a session

1. Read this whole file.
2. Follow every rule and decision under Decisions, even when the request does not repeat it.

## Before you finish a session

1. Tasks: update the status of each task you touched; add any task left for later.
2. Decisions: add every new rule or decision you were given or made. Never delete one; mark it superseded instead.
3. Handoff: rewrite it for the next session: what you did, what is unfinished, what to do first.

## Tasks

| task | status | session |
|---|---|---|

## Decisions

Rules and design decisions the code must follow.

## Handoff

(no earlier session)
""")

out = os.path.join(T, "notes_t")
shutil.rmtree(out, ignore_errors=True)
w(os.path.join(out, "NOTES.md"), """# Notes

Keep these four sections. A later session reads only this file.

## Rules

Constraints the code must always follow, one per line.

## Decisions

Current design decisions and values, one per line. When one is changed, mark the old line superseded and add the new one.

## Unfinished

Work left for a later session, with what it is waiting for.

## Last session

What the last session did.
""")

out = os.path.join(T, "delta")
shutil.rmtree(out, ignore_errors=True)
w(os.path.join(out, "PLAYBOOK.md"), "# Playbook\n\n(empty)\n")
w(os.path.join(out, "DELTA.md"), "")
print("built notes_t, pack_t, pack_h, pack_d, pack_a, pack_x, delta")
