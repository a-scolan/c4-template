To verify `projects/shared/spec-containers.c4` is truly generic before upstream push:

- Check portability: would another derived repo use this unchanged?
- Remove local context: no domain/project/customer-specific references.
- Confidentiality review: no secrets, private topology, internal-only identifiers.
- Scope check: it lives in `projects/shared/` (good), but content still must be generic.
- Sync branch hygiene: create `sync/*` from `c4-template/main`, bring only this file, inspect diff, then PR.

If not fully generic, split the change: upstream-safe subset vs local-only remainder.