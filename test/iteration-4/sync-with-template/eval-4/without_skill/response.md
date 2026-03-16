Safest recovery: do not open the PR from the contaminated branch. Create a new clean sync branch from the upstream default branch and carry over only the generic .github change.

If the generic change is already in its own commit:

git branch backup/sync-spec-hardening
git fetch c4-template
git switch --create sync/spec-hardening-clean c4-template/main
git cherry-pick <good-generic-commit>
git diff --name-only c4-template/main...HEAD
git push c4-template HEAD:sync/spec-hardening-clean

If the generic change and the local projects/acme/system-model.c4 and README.md edits were mixed into one commit, split it first:

git branch backup/sync-spec-hardening
git fetch c4-template
git reset --soft c4-template/main
git restore --source=c4-template/main --staged --worktree projects/acme/system-model.c4 README.md
git commit -m "Isolate generic .github improvement"
git diff --name-only c4-template/main...HEAD

Open the PR only when the diff contains the generic .github change and nothing from projects/acme or README.md.
