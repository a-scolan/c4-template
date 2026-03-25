Yes—`where source.tag is #next` can match the relation from `prod.eu.frontend`.

Reason: for deployed instances (`instanceOf frontend`), the instance’s effective tags include:
- tags defined on the logical element (`frontend` has `#next`), and
- tags defined on the deployment instance itself (here `#gamma`).

So for the same relation source (`prod.eu.frontend`):
- `where source.tag is #next` → **matches** (inherited from logical `frontend`)
- `where source.tag is #gamma` → **also matches** (tag set directly on the deployment instance)

In short, deployment instances use a merged tag set: **logical element tags + instance tags**.