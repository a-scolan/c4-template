Recover by cleaning the sync branch so it contains only the generic skill change.

Preferred recovery:
1. Inspect what differs from upstream:
   - `git fetch c4-template main`
   - `git diff --name-only c4-template/main...HEAD`
2. Remove the local-only files from the sync branch by restoring them from upstream:
   - `git checkout c4-template/main -- projects/acme/system-model.c4 README.md`
3. Commit that cleanup:
   - `git add projects/acme/system-model.c4 README.md`
   - `git commit -m 'chore: remove local-only files from sync branch'`
4. Verify the branch now contains only the generic file intended for upstream:
   - `git diff --name-only c4-template/main...HEAD`
5. Run the confidentiality review on `.github/skills/create-element/SKILL.md`, then push/update the PR:
   - `git push c4-template sync/spec-hardening --force-with-lease`

If the branch is too messy, the safer fallback is to recreate it from `c4-template/main` and bring over only `.github/skills/create-element/SKILL.md`. Any local edits to `projects/acme/system-model.c4` or `README.md` should live on a normal local branch, not on the upstream sync branch.
