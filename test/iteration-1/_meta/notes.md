# Iteration 1 Notes

- Scope: all workspace skills under `.github/skills/*` with `evals/evals.json`
- Skill count: 19
- Eval count: 73
- Mode: blind comparison (`with_skill` vs `without_skill`)
- Output language: English
- MCP usage: forbidden
- Repository writes outside `/test`: forbidden
- Anonymization: no absolute workspace paths in saved artifacts or reports
- Previous iteration: none found

## Critical baseline isolation

- Prompt-only restrictions were judged insufficient after the first contaminated pilot.
- The corrected procedure physically moves every directory from `.github/skills/` into `test/iteration-1/_disabled-skills/` before any baseline run.
- All `without_skill` runs must complete while `.github/skills/` is empty.
- Skills are restored only after the full baseline batch completes.
- `with_skill` runs start only after restoration, in fresh sessions or fresh workers.

## Baseline rerun status

- The clean baseline batch was executed only after relocating all 19 skills out of `.github/skills/`.
- A targeted isolation probe that had leaked before came back clean after the relocation step.
- A global scan across `without_skill` outputs found no unexpected skill-name or MCP leakage.
- The only scan hits were expected references inside `sync-with-template` outputs, where a skill file path was itself the subject of the eval prompt.
- Baseline isolation is accepted for this iteration, subject to the relocation and restoration manifests in `_meta/`.
