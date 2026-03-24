Candidates for upstream sync:
- `.github/skills/create-relationship/SKILL.md` — yes, if the improvement is reusable across derived repositories and contains no local/private context.
- `projects/shared/spec-context.c4` — yes, if it is a genuinely shared spec improvement rather than a workaround for one repo.

Must stay local:
- `projects/payments/system-model.c4` — no; anything under `projects/<project>/` is project-local.
- `README.md` — no; repository-level docs are usually local to this repo.

Before pushing the first two upstream, apply the decision test: would another derived repo use them without knowing your local domain, do they avoid project names/internal systems/private architecture, and can you explain them as reusable workspace improvements rather than one-off fixes?
