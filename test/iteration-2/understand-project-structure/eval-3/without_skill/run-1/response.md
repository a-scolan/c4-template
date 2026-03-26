After project context is established, hand off to `create-sequence-view` for sequence modeling.

What this first skill must lock in before handoff:
- Active project id and boundaries
- Authoritative taxonomy (element kinds, relationship kinds, tags)
- Source-of-truth files (`likec4.config.json` includes + target `.c4` files)
- Stable element ids/names that sequence steps will reference
- Clear scenario scope (participants, trigger, success/failure path)

Handoff only after these are stable, so sequence modeling does not drift across projects or invalid kinds.
