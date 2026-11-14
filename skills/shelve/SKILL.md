---
name: shelve
description: Shelve a paused or completed scientific experiment or code project. Capture session decisions, results, failed approaches and restart instructions; inventory and consolidate files; externalize verified large datasets; request explicit approval before any removal. Invoke manually with /shelve.
disable-model-invocation: true
---

# Shelve a project

Work within `${CLAUDE_PROJECT_DIR}` by default. If the user explicitly supplies another project path, confirm the path is the intended root before making changes. Never alter unrelated projects. Do not run destructive operations without explicit approval.

Session ID: `${CLAUDE_SESSION_ID}`

## 1. Record the scientific and computational state

Inspect available conversation context, relevant project documentation, `git status`, `git rev-parse HEAD`, environment files (including `pyproject.toml` and `uv.lock` where present), source code, and experiment outputs. Do not imply that the entire session history was captured if part is unavailable.

Create a timestamped directory `archive/YYYY-MM-DD-HHMMSS/` and write `HANDOFF.md` covering:

- Objectives, hypotheses, dataset provenance, and scientific questions.
- Experiments actually performed, important commands, parameters, random seeds, and environment.
- Quantitative results with paths to supporting figures, tables, and scripts.
- What worked, what failed, what was learned, and remaining uncertainties; separate observations from interpretations.
- Git commit and status, Claude session ID, known missing context, and unfinished work.
- Minimal steps to resume and reproduce one representative result.

Never fabricate results or reconstruct an unobserved experiment as if it happened.

## 2. Inventory before modifying files

Run `python3 "${CLAUDE_SKILL_DIR}/scripts/inventory.py" --root "${CLAUDE_PROJECT_DIR}" --output archive/YYYY-MM-DD-HHMMSS/inventory.csv`, replacing the date directory with the one actually created. The inventory includes ignored/untracked regular files but excludes the generated directories documented in the script; inspect important excluded directories separately.

Review file counts and sizes. Classify paths as KEEP, CONSOLIDATE, EXTERNALIZE, REGENERATE, or UNKNOWN. Size alone never implies disposability. Preserve irreplaceable raw measurements, source code, configuration, and final research results.

## 3. Produce a reviewable plan

Write `PLAN.md` in the snapshot directory. List exact paths or safe directory patterns, the proposed action, size reduction, scientific rationale, risk, and restoration method. Identify imports or scripts that would break if files move. Do not reorganize the source tree merely for neatness.

Write `manifest.yaml` with `schema_version: 1`, project path, snapshot time, Git commit, and one record for each externalized, consolidated, or regenerable artifact. Record at least the relative path, disposition, SHA-256 when the bytes are available, and either (a) an external storage URI plus immutable version/object ID and retrieval command, (b) a verified bundle path and member name, or (c) precise regeneration instructions with software/parameters. Do not record unverified locations as available.

Show the proposed operations and explicitly ask approval. If external storage is unspecified, request its location/configuration; do not delete large data while waiting for an answer.

## 4. Apply only approved operations

After explicit approval for the listed paths:

1. Consolidate selected small intermediates into a compressed archive using standard tooling. Preserve relative paths and a member-level manifest. Verify archive readability and SHA-256, and test restoration into a temporary directory before deleting any originals.
2. Externalize selected large datasets only through an already configured storage backend (such as DVC). Verify that the remote object exists, is retrievable with the documented command, and matches the checksum. Never treat `dvc add` as proof of remote backup; verify `dvc push` and the remote data.
3. Remove an original only if it appears in the approved plan and its alternate copy or regeneration process has been verified. Do not delete the only known copy. Avoid broad glob deletions and avoid changing Git-tracked work without separate consent.
4. Leave readable pointers in `manifest.yaml`, record the resulting commands in `HANDOFF.md`, and update a root-level `SHELVED.md` pointing to this snapshot (without overwriting substantive content without consent).

Do not claim clean-up, backup, or successful restoration if a verification step failed. Keep originals in place and report the blocker instead.

## 5. Verify and report

Check that the source tree still has the files needed to reopen it, that manifest paths resolve, and that at least one representative archived artifact can be restored. Report before/after size, archived and deleted file counts, any irreproducible or unverified data, and the location of `HANDOFF.md`.
