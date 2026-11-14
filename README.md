# Claude Code research skills

A monorepo of independently installable Claude Code skills. Each skill is a standalone directory under `skills/`.

## Available skills

| Skill | Purpose |
| --- | --- |
| [shelve](skills/shelve/SKILL.md) | Capture research context, inventory files, and perform a reviewed, recoverable project cleanup. |
| [unshelve](skills/unshelve/SKILL.md) | Review a shelved project, retrieve required data, and resume work. |

## Install an individual skill

Clone this repository once:

```bash
git clone https://github.com/williamgilpin/skills.git ~/claude-skills
mkdir -p ~/.claude/skills
```

Install only the skills you need:

```bash
ln -s ~/claude-skills/skills/shelve ~/.claude/skills/shelve
ln -s ~/claude-skills/skills/unshelve ~/.claude/skills/unshelve
```

Launch Claude Code in the **research project's directory** and invoke `/shelve` or `/unshelve`.

Updates: `git -C ~/claude-skills pull`. To uninstall a skill, remove its symlink from `~/.claude/skills/` (not the source directory). If a destination exists already, inspect it before replacing it.

For per-project installation, link a single skill under that project's `.claude/skills/` instead.

## Shelving behavior and safety

- `shelve` writes a scientific handoff and a file inventory, then presents a cleanup plan.
- No large data are deleted unless an independently retrievable, checksum-verified copy or reproducible regeneration process is documented and the user explicitly approves the exact deletion.
- Remote data storage is **not included**. Configure an external backend (for example DVC with suitable remote storage) before using externalization.
- `unshelve` reconstructs context and restores only the data needed for the task, without overwriting existing files without approval.

The bundled inventory script uses Python's standard library. Large-file classifications are **review hints**, not deletion decisions. It excludes `.git`, virtual environments, common generated caches, `node_modules`, and past `archive/` snapshots.

See [Claude Code skills documentation](https://code.claude.com/docs/en/skills).
