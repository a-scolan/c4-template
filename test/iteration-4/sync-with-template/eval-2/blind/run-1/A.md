A safe path is to fetch upstream, create a sync branch, copy only .github and projects/shared from the upstream reference, and commit that as one sync change. Replace main if needed.

git switch main
git pull --ff-only
git fetch c4-template
git switch --create sync/template-refresh
git restore --source=c4-template/main --staged --worktree .github projects/shared
git diff --stat
git commit -m "Sync .github and projects/shared from c4-template"

Why squash: one sync commit is easier to review, easier to revert, keeps the derived repository history clean, and avoids importing a long chain of upstream commits when all you want is the current upstream state for those shared paths.
