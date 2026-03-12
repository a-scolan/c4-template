Run these commands:

- `git fetch c4-template main`
- `git subtree pull --prefix=.github c4-template main --squash`
- `git subtree pull --prefix=projects/shared c4-template main --squash`

Why `--squash`:

- It keeps the history cleaner and more compact.
- It records each upstream sync as a smaller, easier-to-review change in your repo.
- It avoids importing the full upstream commit graph for these shared template assets.

That scope is intentionally limited to `.github` and `projects/shared`; do not use this pull for project-specific files or folders.