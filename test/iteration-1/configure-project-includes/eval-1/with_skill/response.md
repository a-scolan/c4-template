Split it progressively, not all at once. Start with the smallest clean baseline:
- `likec4.config.json`
- `system-model.c4` for elements and relationships
- `system-views.c4` for static views

Then add focused files only when the project actually needs them:
- `system-sequences.c4` for dynamic views in `Use Cases`
- `deployment.c4` for deployment nodes and `instanceOf`
- `deployment-views.c4` for `Deployment` views
- `operations.c4` for operational topology
- `operations-views.c4` for `Operations` views

Keep C1/C2/C3 views in `system-views.c4`, grouped under `views 'C1'`, `views 'C2'`, and `views 'C3'`. Every view should be inside a category folder except the root `index` view, which stays directly under `views { }`. Also keep model files separate from view files once the project is larger than a small single-file setup.
