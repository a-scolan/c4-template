## Full validation plan before commit

Given a new **worker container** and a dedicated **C2 view**, use a full integrity pass:

1. **Taxonomy check**: kinds and relationship types must come from shared specs.
2. **Reference check**: all new FQNs and view references resolve correctly.
3. **Relationship check**: verify kind/direction/label, keep protocol in `technology`.
4. **View check**: C2 must keep parent system context and expected neighbors.
5. **Scope check**: ensure includes are intentionally narrow, not broad wildcards.
6. **Diagnostics check**: ensure no unresolved references or typing errors remain.

## Completion checklist

- [ ] valid kinds
- [ ] valid FQNs
- [ ] correct relationship semantics
- [ ] protocol modeled in `technology`
- [ ] parent context visible in C2
- [ ] include scope controlled
- [ ] render matches intended architecture story
