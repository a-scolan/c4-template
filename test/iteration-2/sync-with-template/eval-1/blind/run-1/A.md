Use a clean `sync/*` branch from upstream and gate push with a confidentiality review.

1. Prepare remotes and latest refs:
   - `git fetch --all --prune`
2. Start a dedicated sync branch from upstream main:
   - `git switch -c sync/skill-create-relationship-improvement c4-template/main`
3. Bring your improvement commit(s) only:
   - `git cherry-pick <commit_sha>`
   - (repeat for each relevant commit)
4. Verify scope is exactly what you intend:
   - `git diff --name-only c4-template/main...HEAD`
   - Expect only `.github/skills/create-relationship/SKILL.md`.
5. Confidentiality review before push:
   - Ensure no internal names, secrets, private URLs, customer identifiers, or FOUND_LOCAL-only policy text.
   - If needed, amend commit: `git commit --amend`.
6. Push branch to upstream remote:
   - `git push -u c4-template sync/skill-create-relationship-improvement`
7. Open PR against `c4-template/main` and request review.

This sequence keeps history clean, limits blast radius, and enforces review before publication.