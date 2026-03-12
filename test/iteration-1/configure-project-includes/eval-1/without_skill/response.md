Split it progressively rather than doing a big-bang rewrite.

Start with the minimal template-aligned split:

1. Move the model structure into `system-model.c4`.
   - Actors
   - systems
   - containers
   - components
   - relationships

2. Move the architecture views into `system-views.c4`.
   - C1 views
   - C2 views
   - C3 views

That gives you a clean first step without changing the whole model organization at once.

Then extract only when the file grows enough to justify it:

3. Put use-case or interaction flows into `system-sequences.c4`.
   - Keep this for dynamic scenarios and narrative flows
   - Do not scatter use cases across model and view files

4. When runtime topology matters, add dedicated deployment files.
   - `deployment-model.c4` for deployment structure
   - `deployment-views.c4` for deployment views
   - If you prefer one file at first, `deployment.c4` is also fine

5. When operational concerns exist, separate them too.
   - `operations-model.c4` for operations-oriented definitions
   - `operations-views.c4` for operations views
   - Or start with a single `operations.c4` and split later

A practical migration order is:

- first: `system-model.c4` + `system-views.c4`
- next: `system-sequences.c4` if flows are getting noisy
- later: `deployment*.c4` when infrastructure matters
- later: `operations*.c4` when runbooks, support views, or ops-specific concerns appear

This keeps C1/C2/C3 in `system-views.c4`, gives use cases a dedicated home, and lets deployment and operations evolve separately only when they are real concerns.