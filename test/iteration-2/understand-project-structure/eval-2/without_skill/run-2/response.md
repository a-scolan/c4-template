Structured diagnosis for unknown kind/relationship:

1) Check first (fast triage)
- Confirm active project id (`list-projects` + selected project)
- Read active project taxonomy (`read-project-summary`)

2) Compare
- Compare your used element kind vs `specification.elementKinds`
- Compare your used relationship kind vs `specification.relationshipKinds`
- Compare tags/metadata keys with project-defined conventions

3) Confirm sources of truth
- Validate that the edited `.c4` file is included by the active project's `likec4.config.json`
- Ensure you are not borrowing taxonomy from a different project/example

4) Confirm before fixing
- Find similar valid elements/relationships in same project (`search-element`, `read-element`)
- Reuse exact kind names and relationship kinds from those valid examples

5) Apply fix
- Replace unknown kind/relationship with a valid taxonomy item from active project
- Re-check related view/element references for consistency
