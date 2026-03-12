Treat this as a template-candidate audit first, not a push-first change.

1. Verify the fix is actually generic.
   - Check that it solves a reusable modeling problem, not a repo-specific one.
   - Remove any project names, domain terms, local tags, paths, or assumptions tied to one system.
   - Ask whether the change would still make sense in at least one unrelated derived repository.

2. Do a confidentiality review on the diff.
   - Look for internal names, proprietary examples, architecture details, or identifiers that should not leave the local repo.
   - Do not push anything upstream until that review passes.

3. Isolate the candidate change on a template sync branch.
   - `git fetch c4-template main`
   - `git switch -c sync/spec-containers-generic-fix c4-template/main`
   - `git checkout main -- projects/shared/spec-containers.c4`

4. Review the exact upstream proposal.
   - `git diff -- projects/shared/spec-containers.c4`
   - Confirm it improves the shared spec without encoding local needs or breaking existing generic usage.

5. Only then commit and push the `sync/*` branch.
   - `git add projects/shared/spec-containers.c4`
   - `git commit -m "sync: refine shared container spec"`
   - `git push -u c4-template sync/spec-containers-generic-fix`

Simple rollback plan:

- If it turns out to be too local or regressive before push, abandon the branch: `git switch main` then `git branch -D sync/spec-containers-generic-fix`.
- If you already committed on the sync branch but have not pushed, reset it back to `c4-template/main` or recreate the branch from that base.

Same fix wanted elsewhere is a good signal, but not proof — the audit still decides whether it is truly template-grade.