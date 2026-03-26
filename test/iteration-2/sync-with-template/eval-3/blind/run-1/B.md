Use a short **genericity gate** before upstream push:

1. **Cross-repo usefulness**
   - Confirm `projects/shared/spec-containers.c4` improvement benefits multiple derived repos, not only your current domain.
2. **Local-context scan**
   - Remove project names, customer/internal system references, one-off assumptions.
3. **Confidentiality scan**
   - Ensure no secrets, internal topology details, private identifiers, team/person names.
4. **Scope validation**
   - File is in `projects/shared/` (good sync surface), but still verify content is generic.
5. **Diff-only check on sync branch**
   - Create `sync/*` from `c4-template/main`, bring only this file, review diff, then PR.

If any check fails, keep it local or refactor the change into a generic subset + local remainder.