Once project context is established, the next skill for sequence modeling should be `create-sequence-view`.

Before that handoff, this first skill should lock in five things:
1. the active project folder and its `likec4.config.json`
2. the shared taxonomy actually in scope via `../shared`
3. the exact system/container/component IDs the sequence will reference
4. the source-of-truth model and view files for that project
5. the intended abstraction level of the sequence (system, container, or component)

If those are not fixed first, sequence modeling becomes guesswork and tends to fail in two boring but common ways: it targets the wrong project, or it invents IDs that do not exist in the active model.
