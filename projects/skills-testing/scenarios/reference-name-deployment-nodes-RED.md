# Reference: name-deployment-nodes Testing - RED (WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** name-deployment-nodes  
**Test Type:** Reference Skill - Naming Conventions  
**Status:** RED (baseline without skill)

---

## Scenario: Name VMs and Zones Consistently

**Setup:** "I'm creating deployment nodes. What naming pattern should I use?"

**WITHOUT skill loading — what violations occur?**

---

## Expected Violations

### Violation 1: No Naming Convention Standard
**Without skill:**
- [ ] Naming arbitrary
- [ ] Inconsistent across environment
- [ ] No pattern guidance
- [ ] Hard to scan infrastructure

### Violation 2: Unclear VM Naming Formula
**Without skill:**
- [ ] Doesn't explain {Environment}{Service}Vm
- [ ] No systematic approach
- [ ] Different nodes named inconsistently
- [ ] Convention must be guessed

### Violation 3: Zone Naming Not Addressed
**Without skill:**
- [ ] Zones have unclear names
- [ ] Tier relationships invisible
- [ ] No {Tier}Zone pattern
- [ ] Hard to understand topology

### Violation 4: No Self-Documenting Infrastructure
**Without skill:**
- [ ] Names don't reveal purpose
- [ ] Infrastructure scanning difficult
- [ ] Onboarding confusion
- [ ] Manual documentation needed

---

## Test Execution

Run WITHOUT name-deployment-nodes skill:

1. **Prompt:** "How should I name production VMs and zones?"
2. **Observe:** Does it suggest naming formulas?
3. **Document:** Pattern explanation
4. **Record:** Self-documentation level

---

## Compliance Scoring (Violations)

| Violation | Found? |
|-----------|--------|
| No naming convention standard | [ ] |
| Unclear VM naming formula | [ ] |
| Zone naming not addressed | [ ] |
| No self-documenting infrastructure | [ ] |

**Baseline:** Expect 3-4 of these violations

---

## Expected Baseline

This is RED state: demonstrates need for deployment naming guidance.
