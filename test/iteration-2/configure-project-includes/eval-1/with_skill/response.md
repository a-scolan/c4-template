Do not do a big-bang split. Start with the smallest clean baseline, then extract only the topics that are actually dense.

Recommended baseline:
- `likec4.config.json`
- `system-model.c4` — elements and relationships
- `system-views.c4` — index plus C1/C2/C3 views

Then grow progressively only when needed:
- `system-sequences.c4` — dynamic flows / Use Cases
- `deployment.c4` — deployment nodes and `instanceOf` links
- `deployment-views.c4` — deployment views
- `operations.c4` — operations topology / operational structure
- `operations-views.c4` — operations views

Placement rules:
- Put C1/C2/C3 views in `system-views.c4`.
- Put Use Cases in `system-sequences.c4` once the dynamic flows justify extraction.
- Put deployment definitions in `deployment.c4` and deployment views in `deployment-views.c4`.
- Put operations definitions in `operations.c4` and operations views in `operations-views.c4`.

View organization:
- Keep the index view at the root `views { }` block.
- Put all other views inside category folders such as `views 'C1'`, `views 'C2'`, `views 'C3'`, `views 'Use Cases'`, `views 'Deployment'`, and `views 'Operations'`.

That gives you a clean project baseline without exploding one `system.c4` into too many files too early.
