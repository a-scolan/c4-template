Once project context is established, the next skill should be **`c4-modeling-process`** to sequence C1 → C2 → C3 correctly.

What this first skill (`understand-project-structure`) must lock in before handoff:

1. Active project is explicitly confirmed.
2. Semantic source of truth is clear:
   - `projects/shared/spec-*.c4`
   - `projects/shared/SPEC_CHEATSHEET.md`
3. Workflow guidance vs taxonomy distinction is explicit:
   - `.github/skills/` guides process
   - shared spec files define valid kinds/relationships/tags
4. Project wiring is verified (`likec4.config.json` include paths).
5. Target boundary is identified (system/container parent chain).
6. Known valid relationship namespaces are separated (model vs deployment).

Handoff statement:

Active project and shared taxonomy are validated. The next step is `c4-modeling-process` because the remaining task is sequencing structural modeling from C1 to C3 without introducing hierarchy drift.