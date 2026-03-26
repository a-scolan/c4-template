Yes for both predicates.

`source.tag is #next` matches because deployment instances inherit tags from their referenced logical element (`frontend`).

`source.tag is #gamma` also matches because `#gamma` is an instance-local tag on `prod.eu.frontend`.

So deployment-instance tag matching sees both inherited and instance-specific tags.