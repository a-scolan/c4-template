# Technique: create-sequence-view Testing - RED (WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** create-sequence-view  
**Test Type:** Technique Skill - Temporal Flow Modeling  
**Status:** RED (baseline without skill)

---

## Scenario: Model User Registration Flow

**Setup:** "Show the sequence of interactions when a user registers"

**WITHOUT skill loading — what violations occur?**

---

## Expected Violations

### Violation 1: Missing Initiating Actor
**Without skill:**
- [ ] No clear starting point
- [ ] Unclear who initiates flow
- [ ] Human context missing
- [ ] Sequence feels incomplete

### Violation 2: Incorrect Arrow Syntax
**Without skill:**
- [ ] Uses relationship kinds in sequence
- [ ] Complex relationship notation
- [ ] Not using plain arrows
- [ ] Labels unclear

### Violation 3: Missing Time Ordering
**Without skill:**
- [ ] Steps presented out of sequence
- [ ] Flow logic hard to follow
- [ ] No temporal progression
- [ ] Dependencies unclear

### Violation 4: Incomplete Coverage
**Without skill:**
- [ ] Missing key participants
- [ ] Error paths not shown
- [ ] Edge cases ignored
- [ ] Sequence feels thin

---

## Test Execution

Run WITHOUT create-sequence-view skill:

1. **Prompt:** "Create a sequence view for user registration flow"
2. **Observe:** How is the sequence structured?
3. **Document:** Arrow types and labels used
4. **Record:** Completeness of flow

---

## Compliance Scoring (Violations)

| Violation | Found? |
|-----------|--------|
| Missing initiating actor | [ ] |
| Incorrect arrow syntax | [ ] |
| Missing time ordering | [ ] |
| Incomplete coverage | [ ] |

**Baseline:** Expect 2-3 of these violations

---

## Expected Baseline

This is RED state: demonstrates need for sequence view guidance.
