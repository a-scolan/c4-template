where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match

Deployment-instance tags are **cumulative**: the effective tag set for `source.tag` filtering is the union of the logical element's own tags and any tags declared directly on the `instanceOf` deployment instance, so both `#next` (from the logical `frontend`) and `#gamma` (added on `prod.eu.frontend`) match.
