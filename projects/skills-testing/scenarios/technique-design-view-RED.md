# Technique: design-view Testing - RED (WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** design-view  
**Test Type:** Technique Skill - View Design & Organization  
**Status:** RED (baseline without skill)

---

## Scenario: Create System Overview View

**Setup:** "Design a view showing all containers in a system with neighbors"

**WITHOUT skill loading — what violations occur?**

---

## Expected Violations

### Violation 1: Missing Parent Context
**Without skill:**
- [ ] Shows containers without system scope
- [ ] Missing context container inclusions
- [ ] Views disconnected from parents
- [ ] Incomplete architectural picture

### Violation 2: No Neighbor Relationships
**Without skill:**
- [ ] Includes containers but not connections
- [ ] Missing "→ element" patterns
- [ ] Relationship includes forgotten
- [ ] Dependencies unclear

### Violation 3: Poor Include Patterns
**Without skill:**
- [ ] Manual element listing instead of patterns
- [ ] No tag filtering mentioned
- [ ] Wildcards used inefficiently
- [ ] Hard to maintain view definitions

### Violation 4: Flat Organization
**Without skill:**
- [ ] No distinction between view types
- [ ] Mixed C1/C2/C3 levels
- [ ] No category separation
- [ ] Views not grouped logically

---

## Test Execution

Run WITHOUT design-view skill:

1. **Prompt:** "Design a view of system containers with their neighbors"
2. **Observe:** What gets included?
3. **Document:** Include/exclude patterns used
4. **Record:** Relationship completeness

---

## Compliance Scoring (Violations)

| Violation | Found? |
|-----------|--------|
| Missing parent context | [ ] |
| No neighbor relationships | [ ] |
| Poor include patterns | [ ] |
| Flat organization | [ ] |

**Baseline:** Expect 2-3 of these violations

---

## Expected Baseline

This is RED state: demonstrates need for view design guidance.
