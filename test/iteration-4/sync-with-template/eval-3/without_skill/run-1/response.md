Verify it is truly generic before upstreaming by using the shared-spec bar:
- The change should improve reusable shared vocabulary only, not one project model.
- It should stay consistent with the generic naming and taxonomy already used in the shared specs, such as Actor_*, System_*, and Container_* patterns.
- It must not introduce project names, customer terminology, local environments, confidential URLs, or assumptions tied to one derived repository.
- Another derived repository should be able to apply it unchanged; if it needs exceptions or local caveats, it is not upstream material.

A safe review flow is:

git fetch c4-template
git switch --create sync/shared-container-fix c4-template/main
git cherry-pick <commit-with-the-shared-fix>
git diff --stat c4-template/main...HEAD
git diff c4-template/main...HEAD -- projects/shared/spec-containers.c4

Only push upstream if the isolated diff is still clearly generic after that review.
