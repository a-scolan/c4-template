where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match

Deployment-instance tags are cumulative with the logical element's tags — the instance inherits all tags from its `instanceOf` target and merges them with any tags declared directly on the instance, so both `#next` (from the logical element) and `#gamma` (from the instance) are visible to `where source.tag is` filters.
