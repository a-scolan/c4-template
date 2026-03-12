Use a short audit first, then sync only if the change survives it.

## Verify it is truly generic

- Check whether the fix solves a shared modeling problem, not just one project's naming or structure.
- Confirm another project can use the same change without renaming elements, tags, relationships, or examples.
- Remove project names, business-domain wording, client references, internal IDs, and any sensitive details.
- Review the diff carefully: `git diff -- projects/shared/spec-containers.c4`
- If any part is specific to one repo, keep that part local and do not push it back.

## Safe push workflow

- `git fetch c4-template main`
- `git switch -c sync/spec-containers-generic-fix c4-template/main`
- `git checkout main -- projects/shared/spec-containers.c4`
- Review the diff again against the template base and do a confidentiality check.
- Commit only that shared file.
- Push the `sync/*` branch after the review passes.

Do not push from `main`.

## Simple rollback plan

- If the audit shows the fix is too local, stop and leave it only in the project repo.
- If you already committed it on the sync branch and then spot a regression or local-only assumption, revert that one commit or delete the sync branch and start over.
