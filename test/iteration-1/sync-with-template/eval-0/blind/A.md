You can split these changes into two groups.

## Can be proposed back to the template

- `.github/skills/create-relationship/SKILL.md` — candidate for template sync, because it sits under the reusable `.github` guidance area.
- `projects/shared/spec-context.c4` — candidate for template sync, because `projects/shared` is shared specification material.

## Must stay local

- `projects/payments/system-model.c4` — project-specific model content, so keep it in the local repository.
- `README.md` — keep this local as written. Do not push it back as-is; if it contains a reusable idea, rewrite that idea separately for template documentation later.

## Before any push

- Generalize the change first: remove project names, domain-specific wording, customer/internal identifiers, and examples tied to one repository.
- Review the diff for confidentiality and make sure no sensitive architecture details leak into the template.
- Only push the generic part after that review passes.
