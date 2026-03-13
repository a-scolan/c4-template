Split it explicitly:
- Safe upstream candidates: `.github/skills/create-relationship/SKILL.md` and `projects/shared/spec-context.c4`, because they are reusable workspace assets.
- Must stay local: `projects/payments/system-model.c4` and `README.md`, because `projects/<project>/` content and the repository README are project-local.

Before pushing the two upstream candidates, do two checks:
1. Genericity review: confirm another derived repository could use the change without knowing your local domain.
2. Confidentiality review: remove project names, internal system names, customer details, private architecture notes, employee/team names, secrets, or anything else that should not travel upstream.

Only if the diff still contains generic workspace assets after that review should it be pushed to the upstream reference repo.
