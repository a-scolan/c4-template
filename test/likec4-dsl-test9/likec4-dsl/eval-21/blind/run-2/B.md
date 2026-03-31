# Isolation failure

Execution is blocked in strict baseline mode because the repository context exposed `.github/copilot-instructions.md`, which means the required precondition that `.github/skills/` be physically emptied before the session is not satisfied. Per the isolation rules, I must stop instead of answering the eval prompt under these conditions.
