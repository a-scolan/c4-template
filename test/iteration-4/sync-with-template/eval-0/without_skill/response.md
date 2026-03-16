Push upstream only the changes that are reusable template material:
- The generic .github improvement, if it changes reusable guidance only.
- The projects/shared/spec-context.c4 change, if it stays generic and reusable across repositories.

Keep local:
- projects/payments/system-model.c4, because it is project-specific.
- README.md by default, unless that edit is truly template-wide and contains no local onboarding, naming, or confidential details.

Rule of thumb: upstream gets reusable template assets (.github and projects/shared); derived-repo assets stay local (projects/<project>/... and local documentation).
