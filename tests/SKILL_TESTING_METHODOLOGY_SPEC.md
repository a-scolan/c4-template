# Skill Testing Methodology Hardening Specification

## Status

Draft specification with an MVP runner implemented in `tests/run_skill_evals.py`. This document defines the required testing methodology for repository-local Copilot skills and the constraints that the runner is expected to follow.

## Purpose

This specification exists to make skill evaluations trustworthy.

A benchmark is only meaningful if each configuration is executed against the exact skill version it claims to represent, and if the baseline configuration is not contaminated by repository-local skill discovery.

## Scope

This specification applies to:

- repository-local skills stored under `.github/skills/<skill-name>/`
- evaluation workspaces stored under `tests/skills/<skill-name>-workspace/`
- the three supported evaluation configurations:
  - `with_skill`
  - `old_skill`
  - `without_skill`

This specification does **not** yet guarantee isolation from globally installed or user-level skills outside the repository. That concern is explicitly deferred to a later hardening phase.

## Goals

The methodology MUST:

1. compare like-for-like runs using the same prompt, inputs, model, and grading criteria
2. prove which skill version was visible to each run
3. prevent evaluation workspaces from being discovered as active skills
4. support both first-iteration baselines and later version-to-version comparisons
5. leave a durable audit trail in `tests/skills/`

## Non-goals

This specification does not define:

- a production runner implementation
- container-level security isolation
- protection from global skills outside the repository
- the user interface of any future runner

## Terminology

### Live skill

The active repository version of a skill, stored under:

` .github/skills/<skill-name>/ `

### Evaluation workspace

The persisted evidence directory for one skill, stored under:

` tests/skills/<skill-name>-workspace/ `

### Iteration

A numbered evaluation pass stored under:

` tests/skills/<skill-name>-workspace/iteration-N/ `

### Baseline snapshot

A saved copy of the previous skill version used for `old_skill` runs. If a snapshot is needed, it MUST be stored under:

` tests/skills/<skill-name>-workspace/skill-snapshot/ `

The primary skill file in a snapshot MUST be named `BASELINE_SKILL.md`.

### Sandbox

A temporary execution workspace created for one eval and one configuration. A sandbox is not a security boundary in the operating-system sense; it is a discovery boundary controlling which repository-local skills are visible to the run.

## Repository Layout Requirements

The repository MUST preserve this separation:

- live skills: `.github/skills/`
- evaluation artefacts: `tests/skills/`

Evaluation workspaces MUST NOT remain under `.github/skills/`.

A test workspace MUST NOT contain an active `SKILL.md` file in a location where the repository skill discovery mechanism could treat it as a live skill.

If a snapshot of an older skill version is stored for later replay, the snapshot MUST use `BASELINE_SKILL.md`, not `SKILL.md`.

## Supported Evaluation Configurations

### `with_skill`

`with_skill` represents the current live skill under test.

The sandbox MUST expose the current repository version of the target skill and MUST NOT silently substitute a baseline snapshot.

### `old_skill`

`old_skill` represents the immediately preceding skill version captured before modification.

The sandbox MUST expose the snapshot materialised as the active skill for the run. The live version and the baseline version MUST be distinguishable by content hash.

### `without_skill`

`without_skill` represents a baseline where the target repository-local skill is unavailable.

The sandbox MUST NOT expose the target skill. For the first iteration of a skill, this is the default baseline unless a stricter comparison is explicitly required.

## Baseline Policy

### First iteration

For the first measured iteration of a skill, the baseline SHOULD be `without_skill`.

The purpose of this comparison is to measure whether the skill adds value relative to generic model behaviour.

### Later iterations

For later iterations, the preferred comparison SHOULD be `with_skill` versus `old_skill`.

The purpose of this comparison is to measure whether the updated skill improves on the previous repository version.

A later iteration MAY additionally include `without_skill` if both absolute value and relative improvement are required.

## Sandboxing Requirements

For each eval prompt and configuration, the runner MUST create a fresh temporary sandbox.

Each sandbox MUST:

1. start from a clean temporary directory
2. contain the repository material required for the eval prompt
3. materialise only the repository-local skill view allowed for that configuration
4. run the prompt with that sandbox as the effective workspace root
5. be disposable after the run completes

A sandbox MUST NOT be reused across configurations.

A sandbox MUST NOT be reused across eval IDs.

## Skill Visibility Rules

### `with_skill` sandbox

The sandbox MUST expose the target skill as the active skill implementation.

### `old_skill` sandbox

The sandbox MUST expose the snapshot version as the active skill implementation.

If the snapshot includes support files such as `REFERENCE.md`, `CHECKLIST.md`, `PATTERNS.md`, `EXAMPLES.md`, or equivalent, those files MUST be included in the sandbox alongside the baseline skill.

### `without_skill` sandbox

The sandbox MUST make the target repository-local skill unavailable.

At minimum, this means the sandbox MUST NOT contain `.github/skills/<skill-name>/`.

A stronger implementation MAY provide an empty `.github/skills/` directory or a neutralised `copilot-instructions.md` to make the absence of local skills explicit.

## What "disable skills" means

For the purpose of this specification, disabling a skill does **not** mean instructing the model to ignore it.

Disabling a repository-local skill means removing it from the sandbox so that it cannot be discovered through normal repository-local skill loading.

Any methodology that merely asks the model not to use a visible skill is insufficient for a trustworthy baseline.

## Version Evidence Requirements

Each run MUST write a machine-readable manifest proving the skill state used by that configuration.

Recommended filename:

`skill_manifest.json`

The manifest MUST include:

- `skill_name`
- `configuration`
- `sandbox_root`
- a list of visible skill files for the target skill
- a content hash for each visible skill file
- an explicit statement that no target skill was visible for `without_skill`

If support files are present for the target skill, they MUST be hashed as part of the manifest.

## Invariants Across Configurations

For a single eval ID, the following MUST remain identical across configurations:

- prompt text
- input files
- model identifier
- grading logic and assertions
- expected output criteria

Only the visible skill version MAY change.

## Output Requirements

Each run MUST persist enough evidence to reconstruct what happened.

At minimum, each configuration run SHOULD persist:

- `outputs/response.md` or equivalent user-visible output
- `grading.json`
- `timing.json`
- `skill_manifest.json`

Each iteration SHOULD persist:

- `benchmark.json`
- `benchmark.md`
- `review.html`

Each workspace SHOULD additionally persist iteration-aware history reports derived from all `iteration-N/benchmark.json` files, and the shared `tests/skills/` root SHOULD persist a repo-wide multi-skill overview report.

## Validation Rules

Before executing a run, the runner MUST validate sandbox state.

### Required validation for `with_skill`

- the target skill exists in the sandbox
- the active skill file is present as `SKILL.md`

### Required validation for `old_skill`

- the target skill exists in the sandbox
- the active skill file is present as `SKILL.md`
- the active file content hash differs from the current live version unless the content is intentionally unchanged

### Required validation for `without_skill`

- the target skill does not exist in the sandbox
- no active `SKILL.md` for the target skill is present in the sandbox

If these checks fail, the run MUST be aborted and marked invalid.

## Failure Conditions

A run MUST be treated as invalid if any of the following occurs:

- the wrong skill version was visible in the sandbox
- both `with_skill` and `old_skill` resolve to identical content unintentionally
- the `without_skill` sandbox still exposes the target repository-local skill
- prompts, inputs, or grading logic differ across configurations for the same eval
- the run has no version manifest

Invalid runs MUST NOT be included in benchmark aggregates.

## Recommended Phase 1 Implementation Shape

A minimal future runner SHOULD:

1. read `.github/skills/<skill-name>/evals/evals.json`
2. determine the next `iteration-N`
3. for each eval and configuration, create a temporary sandbox
4. materialise the allowed skill view in that sandbox
5. execute the prompt using the sandbox as the workspace root
6. write run artefacts into `tests/skills/<skill-name>-workspace/iteration-N/`
7. aggregate and grade after all runs finish

This repository now ships an MVP implementation at `tests/run_skill_evals.py` that follows this shape with `gh copilot -- -p ...`, per-run temporary home directories, and optional MCP reinjection from `~/.vscode/mcp.json`.

The runner also regenerates:

- per-workspace history reports at `tests/skills/<skill-name>-workspace/workspace-history.{json,md,html}`
- a global overview at `tests/skills/skills-overview.{json,md,html}`

This makes historical iteration numbers first-class in the persisted reporting, rather than only in the folder layout.

## Deferred Hardening

The following improvements are recommended later but are outside this specification's immediate implementation scope:

- isolation from globally installed or user-level skills
- dedicated execution profiles for `without_skill`
- containerised execution
- automatic detection of non-discriminating assertions
- multi-run variance measurement per configuration

## Decision Summary

A trustworthy skill benchmark requires physical isolation of repository-local skill visibility, not prompt-level persuasion.

In this repository, the authoritative rule is therefore:

- live skills belong in `.github/skills/`
- evaluation evidence belongs in `tests/skills/`
- each benchmark configuration must be executed in a fresh sandbox with an explicitly materialised skill view
