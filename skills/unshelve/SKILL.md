---
name: unshelve
description: Resume a previously shelved scientific experiment or code project. Read the handoff and manifest, restore only required verified files or data, reconstruct the environment and next steps, and avoid overwriting active work. Invoke manually with /unshelve.
disable-model-invocation: true
---

# Unshelve a project

Use the current project root (`${CLAUDE_PROJECT_DIR}`) unless the user names another path. This skill is independently installable and does not depend on the shelve skill being installed.

1. Read `SHELVED.md`, if present, and discover `archive/*/HANDOFF.md` and `manifest.yaml`. If multiple snapshots exist, ask which to resume when the choice matters. Read the recorded objective, outcomes, limitations, next steps, Git commit, and any available session provenance.
2. Compare the recorded Git commit and environment with the working tree. Show meaningful changes before restoring or modifying files; never reset, checkout, or overwrite existing edits without approval.
3. Inspect the manifest and identify which source files, consolidated intermediates, or external datasets are actually required for the user's next task. Prefer restoring a minimal working subset rather than all large outputs. Explain estimated transfer size and storage needed.
4. For a compressed bundle, verify its checksum and member paths before extracting. Reject absolute paths, parent traversal, symlink escapes, and overwrites. Extract into a staging directory and compare recorded file hashes before moving verified artifacts into the project.
5. For externalized datasets, use the saved immutable object/version and retrieval command, e.g. `dvc pull` when DVC was configured. Verify SHA-256 against `manifest.yaml` after retrieval. If credentials or the backend are unavailable, report the missing dependency rather than guessing a replacement URL.
6. For regenerable artifacts, follow the precise recorded command and parameters. Restore the environment using the project's lockfile, e.g. `uv sync` when `uv.lock` is available. Do not assume a package version or a random seed not recorded in the handoff.
7. Reproduce one representative command or analysis where practical; distinguish successful checks from untested steps.

Finish with a concise status: restored artifacts and locations, verification outcomes, outstanding blockers, current scientific understanding, and the next concrete experiment. Never claim the original session context has been completely restored when the transcript was incomplete.
