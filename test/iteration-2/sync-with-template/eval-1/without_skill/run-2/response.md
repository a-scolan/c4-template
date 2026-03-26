## What usually stays local vs what can be refreshed

### Usually project-owned
- Project model files that describe your real system
- Project views and layout choices
- ADRs and local architecture notes
- Project-specific aliases, naming decisions, and descriptions
- Local relationships, deployment topology, and business semantics

### Usually reasonable to refresh from the template
- Shared specification files that define reusable tags, colors, relationship kinds, and element kinds
- Common cheatsheets or reference material
- Generic config defaults that point to shared specs
- Template examples only if you still use them as examples and have not customized them

### Mixed ownership: review instead of overwrite
- Project config files
- Include lists and alias mappings
- Any file copied from the template and then edited locally

A good heuristic is simple: if a file encodes workspace-wide vocabulary, it is a template-refresh candidate; if it encodes your system truth, it is project-owned.