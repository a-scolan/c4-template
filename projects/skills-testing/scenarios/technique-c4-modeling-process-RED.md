# Technique: c4-modeling-process Testing - RED (WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** c4-modeling-process  
**Test Type:** Technique Skill - C4 Hierarchy Methodology  
**Status:** RED (baseline without skill)

---

## Scenario: Design System for New Architecture

**Setup:** "Create a system model from scratch. How should elements be organized? Is there a specific hierarchy?"

**WITHOUT skill loading — what violations occur?**

---

## Expected Violations

### Violation 1: Missing C1→C2→C3 Progression
**Without skill:**
- [ ] Creates elements at random levels
- [ ] Mixes system, container, component definitions
- [ ] No clear parent-child relationships
- [ ] Incomplete visibility of hierarchy

### Violation 2: Skipped Abstraction Levels
**Without skill:**
- [ ] Jumps directly to components
- [ ] Misses container layer
- [ ] No context-level diagram
- [ ] Incomplete modeling chain

### Violation 3: Poor Organization Pattern
**Without skill:**
- [ ] Elements not grouped by responsibility
- [ ] Relationships not scoped correctly
- [ ] No clear breakdown strategy
- [ ] Missing refinement patterns

### Violation 4: No Top-Down Method
**Without skill:**
- [ ] Starts detailed without context
- [ ] No systematic decomposition
- [ ] Relationships poorly defined
- [ ] Hard to see system cohesion

---

## Test Execution

Run WITHOUT loading c4-modeling-process skill:

1. **Prompt:** "I need to model a multi-tenant SaaS platform. Design the system."
2. **Observe:** How deep does it go immediately?
3. **Document:** What levels of detail emerge? 
4. **Record:** C4 coverage completeness

---

## Compliance Scoring (Violations)

| Violation | Found? |
|-----------|--------|
| Missing C1→C2→C3 progression | [ ] |
| Skipped abstraction levels | [ ] |
| Poor organization pattern | [ ] |
| No top-down method | [ ] |

**Baseline:** Expect 3-4 of these violations

---

## Expected Baseline

This is RED state: demonstrates need for skill guidance on C4 methodology.
