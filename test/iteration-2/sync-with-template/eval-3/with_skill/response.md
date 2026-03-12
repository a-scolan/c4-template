Treat “another derived repository wants the same fix” as a useful signal, not proof that the change is generic. Verify it explicitly before pushing upstream.

Start with a genericity audit:
1. Would another derived repository use this fix without knowing your local domain?
2. Does the change mention project names, internal systems, customer details, or local architecture?
3. Is this a workspace-level improvement to `projects/shared/spec-containers.c4`, or is it compensating for one project’s special case?
4. Can you describe it as a reusable improvement instead of a one-off workaround?

Then do a confidentiality review:
- remove local names and identifiers
- remove private architecture details
- remove team/person references
- make sure the wording and examples are template-safe

If it passes both checks, use a safe sync workflow:
1. Fetch upstream:
   - `git fetch c4-template main`
2. Create a dedicated branch from the upstream template, not from local `main`:
   - `git checkout -b sync/spec-containers-fix c4-template/main`
3. Bring over only the shared file:
   - `git checkout main -- projects/shared/spec-containers.c4`
4. Stage it:
   - `git add projects/shared/spec-containers.c4`
5. Review the exact diff before any push:
   - `git diff --cached`
6. If the diff is still generic and confidentiality-safe, commit and push the `sync/*` branch.

Simple rollback plan:
- if review shows the fix is too local, do **not** push it upstream
- remove the file from the sync branch or reset the branch back to `c4-template/main`
- keep the change only in this repository until it can be generalized

In short: audit first, review the diff carefully, sync from a dedicated `sync/*` branch off `c4-template/main`, and abandon/reset the sync branch if the fix turns out to be local or regressive.