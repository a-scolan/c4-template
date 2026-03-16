Use a clean sync branch from the upstream default branch so only the generic .github improvement is carried. Replace main if the upstream default branch is different.

git fetch c4-template
git switch --create sync/github-improvement c4-template/main
git cherry-pick <commit-with-the-generic-.github-change>
git diff --stat c4-template/main...HEAD
git diff c4-template/main...HEAD -- .github
git diff --name-only c4-template/main...HEAD

Do the confidentiality review before any push: confirm the diff contains only the intended generic .github file(s), with no customer names, project models, local docs, secrets, or internal URLs.

Then push the sync branch:

git push c4-template HEAD:sync/github-improvement

If the improvement is not committed yet, commit it locally first, then cherry-pick that commit onto the clean sync branch.
