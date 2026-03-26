Before pushing `projects/shared/spec-containers.c4` upstream, prove it is generic with this checklist:

1. **Scope check**
   - Diff contains only `projects/shared/spec-containers.c4`.
   - No references to tenant names, local paths, internal IDs, or private systems.

2. **Template relevance check**
   - Change improves baseline modeling guidance/structure used by multiple repos.
   - It does not depend on `projects/<tenant>/...` artifacts.

3. **Cross-repo applicability check**
   - Apply the patch in at least one other derived repo.
   - Confirm it works without adaptation.

4. **Confidentiality check**
   - No secrets, internal URLs, customer data, or organization-only process details.

5. **History hygiene**
   - Put the change on a dedicated `sync/*` branch.
   - Keep commit message generic (problem + reusable fix).

6. **Upstream verification**
   - Compare against `c4-template/main` and ensure change is self-contained.

If all six pass, it is a valid upstream candidate for `c4-template`.