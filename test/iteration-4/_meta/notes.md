# Iteration 4 launch notes

- Protocol preflight completed and `protocol-lock.json` was written.
- Workspace hooks are now enabled by default through `.vscode/settings.json`.
- A first launch attempt exposed a live isolation failure: the strict baseline worker could read forbidden files when hooks were not yet enabled at the workspace level.
- After adding `.vscode/settings.json`, a targeted blocked-file probe succeeded for one forbidden test artifact, but a second probe still showed that runtime isolation via the current subagent path is not trustworthy enough for a scored campaign.
- After a full restart, live probes were run again through the current execution path and both still leaked forbidden files: `README.md` and `test/iteration-3/_meta/c4-modeling-process-with_skill.json`.
- Result: the full iteration-4 benchmark launch was aborted intentionally. Do not score or aggregate iteration 4 until a live worker probe blocks both `README.md` and prior-iteration/test artifacts consistently.

## Runtime hook fix — 2026-03-13 (follow-up)

- Root cause identified: live custom-agent hook payloads reached `enforce-test-access.py` without `hookEventName`, so the script fell through to the default allow path.
- Fix applied: `enforce-test-access.py` now infers `PreToolUse` when a live payload contains a tool invocation but omits `hookEventName`.
- Live verification now blocks forbidden baseline reads again.
- Strict `without_skill` iteration-4 execution has started for real and the following skills have already been materialized:
	- `create-element`
	- `c4-modeling-process`
	- `configure-project-includes`
	- `create-relationship`
	- `create-sequence-view`
	- `customize-view`
	- `design-view`
	- `document-decision`
	- `implement-pattern`
	- `name-deployment-nodes`
	- `test-model`
	- `troubleshoot-errors`
	- `write-rich-descriptions`

## Baseline prompt reload note — 2026-03-13

- Strict baseline workers cannot read `test/iteration-4/_disabled-skills/**` by design, so the manager temporarily restored `.github/skills/` only long enough to re-read the remaining `evals/evals-public.json` files.
- No baseline worker session was started while skills were restored.
- After the public prompt definitions were loaded, the manager immediately re-ran `disable-workspace-skills` and continued strict `without_skill` execution with fresh worker sessions.
- Interim per-skill `without_skill-summary.json` files have been refreshed for all currently completed baseline skills.