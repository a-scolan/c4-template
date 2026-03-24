Run:
`git fetch c4-template`
`git switch -c sync/github-shared`
`git merge --squash --no-commit c4-template/main`
`git restore --source=HEAD --staged --worktree -- . ':(exclude).github' ':(exclude)projects/shared'`
`git diff -- .github projects/shared`
`git add .github projects/shared`
`git commit -m "sync: import upstream .github and shared updates"`
Use `--squash` because you usually want one curated sync commit, not a real merge commit that drags upstream history into the derived repo. It makes review easier, keeps rollback simple, and lets you accept only the reusable paths while dropping everything else.
