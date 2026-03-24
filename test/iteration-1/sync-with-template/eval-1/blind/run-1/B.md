Safe sequence:
1) Make sure local-only work is out of the way: `git status` and, if needed, `git stash push -u -m "local-only before upstream sync"`.
2) Fetch the reference repo: `git fetch c4-template`.
3) Create a clean branch from upstream main: `git switch -c sync/create-relationship c4-template/main`.
4) Copy only the generic file from the branch or commit that contains your improvement: `git restore --source=<your-local-branch-or-commit> -- .github/skills/create-relationship/SKILL.md`.
5) Review only that file: `git diff -- .github/skills/create-relationship/SKILL.md`.
6) Do the confidentiality review before any push: check for internal customer names, repo-local examples, private URLs, secrets, screenshots, or process language that should not leave the derived repo.
7) Commit only the reviewed file: `git add .github/skills/create-relationship/SKILL.md && git commit -m "sync: improve create-relationship skill"`.
8) Push the sync branch: `git push -u c4-template sync/create-relationship`.
9) Open the PR against the upstream reference repo only after the confidentiality review is complete.
