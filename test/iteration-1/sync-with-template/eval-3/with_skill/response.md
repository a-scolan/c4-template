Treat this as a short audit before you push anything.

## 1. Verify the fix is truly generic

Ask these questions against `projects/shared/spec-containers.c4`:

- Would any project using the template benefit from this change?
- Does the fix work without renaming project-specific elements?
- Does it avoid project names, local architecture details, and local business rules?
- Would another project use it as-is, not as a starting point for more edits?

If the answer is "no" to any of those, keep it local.

## 2. Review the diff for confidentiality

Before pushing, inspect the diff and confirm it does **not** contain:

- project names or customer names
- internal architecture details
- security-sensitive configuration
- internal APIs or infrastructure details
- employee or team names

If anything looks uncertain, stop and ask before pushing to a public template.

## 3. Push it safely from a template-based branch

If the audit passes:

```bash
git fetch c4-template main
git checkout -b sync/shared-spec-template c4-template/main
git checkout main -- projects/shared/spec-containers.c4
git add projects/shared/spec-containers.c4
git diff --cached
```

Then do one final genericity/confidentiality review, commit, and push the `sync/*` branch.

## 4. Simple rollback plan

If the fix turns out to be too local or causes regressions:

- **Before push**: do not commit it on the sync branch; restore the file or delete the branch.
- **After commit but before push**: reset the sync branch back one commit or recreate the branch from `c4-template/main`.
- **Best fallback**: keep the change only in your local project and split out a smaller generic version later.

That gives you a safe gate: audit first, review diff, push only from `sync/*`, and abandon the sync branch if the change is not truly template-grade.
