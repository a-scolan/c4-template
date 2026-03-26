Push upstream:
- `.github/skills/create-relationship/SKILL.md`
- `projects/shared/spec-context.c4`

Keep local:
- `projects/payments/system-model.c4`
- `README.md`

Rule of thumb: sync upstream only reusable workspace assets (`.github`, `projects/shared`). Keep project/domain artifacts (`projects/<project>`, root docs) local. Do a final genericity + confidentiality check before opening PR.