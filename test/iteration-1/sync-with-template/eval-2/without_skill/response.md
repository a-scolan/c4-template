Run these commands:

- `git fetch c4-template main`
- `git subtree pull --prefix=.github c4-template main --squash`
- `git subtree pull --prefix=projects/shared c4-template main --squash`

Why `--squash`:

- It collapses the imported template history into one commit per pull.
- That keeps your local history cleaner and easier to review.
- It avoids dragging the full upstream commit graph into everyday project history.

Keep this limited to `.github` and `projects/shared`; do not use the same pull for project-specific files.
