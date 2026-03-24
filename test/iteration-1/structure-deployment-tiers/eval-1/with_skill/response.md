Not as the main job of this skill.

This skill should primarily decide the tier layout, the purpose of each zone, and the firewall/network boundaries between them. It can show small examples, but exact VM names, detailed Markdown property tables, and full `Node_App` + `instanceOf` wiring are deployment-detail concerns rather than tier-structure concerns.

A clean handoff is:
- tier split, zone purpose, and allowed traffic: this skill
- exact VM naming: `name-deployment-nodes`
- full environment/zone/VM/`Node_App` hierarchy and `instanceOf` wiring: `model-deployment-infrastructure`
- rich Markdown spec tables in descriptions: `write-rich-descriptions`

So the right boundary is: use this skill to decide where `Dmz`, `AppTier`, `ProcTier`, `DataTier`, `SecZone`, and `InfraZone` belong; then switch to the more detailed deployment skills to name, table, and wire the nodes precisely.
