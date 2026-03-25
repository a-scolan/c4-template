Yes—`where source.tag is #next` **will match** the relation from `prod.eu.frontend`.

It will also match with `where source.tag is #gamma`.

Reason: a deployed instance created with `instanceOf frontend` has an effective tag set that includes:
- tags from the referenced logical element (`frontend`, so `#next`), and
- tags declared on the deployment instance itself (here `#gamma`).

So in deployment-view predicates, `source.tag` can match either inherited logical tags or deployment-instance-local tags.