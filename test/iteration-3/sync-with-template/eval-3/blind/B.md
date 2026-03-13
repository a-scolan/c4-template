To verify the fix is truly generic before pushing it upstream via `c4-template`, check all of these:
1. Scope: it improves reusable container vocabulary in `projects/shared/spec-containers.c4`, not a payments- or acme-specific model.
2. Neutrality: no customer names, internal acronyms, private URLs, or local infrastructure assumptions.
3. Reuse: another derived repo can adopt it unchanged. If consumers need renaming, exceptions, or local caveats, it is probably not upstream material.
4. Template fit: the change should still make sense against the generic example in `projects/template/system-model.c4`.
5. Showcase fit: it should also remain compatible with the broader examples in `projects/spec-showcase/containers.c4`.
6. Shared-spec contract: `projects/shared/` is where reusable element kinds, tags, styles, and relationships live, so only push changes you would want inherited broadly.
7. Clean branch: the upstream PR should contain only the shared spec change (and matching shared docs if needed), never local `projects/<domain>/...` files.

Practical test: ask, `Would I want every derived repository to inherit this by default?` If the answer is not a clear yes, keep it local.
