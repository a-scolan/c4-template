The repo README gives two valid ways.

Simpler recommended method:
1. `git fetch c4-template main`
2. `git checkout c4-template/main -- .github/copilot-instructions.md .github/skills/`
3. `git checkout c4-template/main -- projects/shared/`
4. `git add .github/ projects/shared/`
5. `git commit -m 'sync: update template files (copilot instructions, skills, specs)'`

If you are using subtree sync instead:
1. `git fetch c4-template main`
2. `git subtree pull --prefix=.github c4-template main --squash`
3. `git subtree pull --prefix=projects/shared c4-template main --squash`

Why `--squash`: it collapses all upstream template commits into one local sync commit per pull, which keeps the derived repo history readable and makes review, audit, and rollback easier.
