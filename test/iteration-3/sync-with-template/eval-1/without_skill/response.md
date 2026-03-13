Safe sequence:
1. `git fetch c4-template main`
2. `git switch -c sync/create-relationship-skill c4-template/main`
3. Bring over only the generic file from your working branch:
   `git checkout <your-working-branch> -- .github/skills/create-relationship/SKILL.md`
4. Review exactly that file:
   `git diff -- .github/skills/create-relationship/SKILL.md`
5. Run confidentiality review before any push. Confirm the diff contains no customer names, internal URLs, repo-specific examples, secrets, screenshots, or local-path references.
6. Commit only that file:
   `git add .github/skills/create-relationship/SKILL.md`
   `git commit -m 'sync: improve create-relationship skill'`
7. Re-check the final patch:
   `git show --stat --name-only HEAD`
8. Only after approval, push the sync branch to the upstream reference repo:
   `git push c4-template HEAD:refs/heads/sync/create-relationship-skill`
9. Open a PR from `sync/create-relationship-skill` to `c4-template/main`.

Why this is safe: the branch starts from upstream `main`, contains one generic file, and inserts a human confidentiality review before the first push.
