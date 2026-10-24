# Conventions

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
