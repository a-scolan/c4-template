Split it progressively instead of doing a big-bang refactor.

Start with the template baseline:
- `system-model.c4` — elements and relationships
- `system-views.c4` — C1/C2/C3 views and the index view

Recommended progression:
1. Move all structural declarations from `system.c4` into `system-model.c4`.
2. Move the C1, C2, and C3 views into `system-views.c4`.
3. If dynamic flows become numerous, extract them into `system-sequences.c4` under the `Use Cases` folder.
4. If deployment modeling is substantial, split it into:
   - `deployment.c4` — deployment nodes and `instanceOf`
   - `deployment-views.c4` — deployment views
5. If operations topology becomes large enough, split it into:
   - `operations.c4` — operations structure
   - `operations-views.c4` — operations views

Placement rules:
- C1/C2/C3 views stay in `system-views.c4`
- Use Cases go in `system-sequences.c4` when they justify a dedicated file
- Deployment definitions and deployment views should not be mixed into the main model/view files once they are meaningful enough to stand alone
- Operations definitions and operations views should also live in their own paired files when that concern exists

One important convention: keep the index view at the root `views {}` block, and place all other views inside their category folders (`C1`, `C2`, `C3`, `Use Cases`, `Deployment`, `Operations`).