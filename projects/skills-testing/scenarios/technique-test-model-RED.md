# Technique: test-model Testing - RED (WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** test-model  
**Test Type:** Technique Skill - Model Validation  
**Status:** RED (baseline without skill)

---

## Scenario: Validate Complex Project Model

**Setup:** "Check if all relationships are valid, no undefined elements, syntax correct"

**WITHOUT skill loading — what violations occur?**

---

## Expected Violations

### Violation 1: Incomplete Validation Checklist
**Without skill:**
- [ ] Spot checks only
- [ ] No systematic verification approach
- [ ] Some error types missed
- [ ] Partial confidence in model

### Violation 2: Missing Syntax Verification
**Without skill:**
- [ ] Elements not checked for proper definition
- [ ] Relationships not validated
- [ ] Syntax errors possible
- [ ] Model might not render

### Violation 3: No Element Reference Checking
**Without skill:**
- [ ] Relationships to undefined elements possible
- [ ] FQN validity not verified
- [ ] Dead links in views
- [ ] Orphan elements not caught

### Violation 4: Type Mismatches Not Caught
**Without skill:**
- [ ] Relationship kinds not validated
- [ ] Element kinds inconsistent
- [ ] No schema enforcement
- [ ] Type errors remain hidden

---

## Test Execution

Run WITHOUT test-model skill:

1. **Prompt:** "Check if this model is valid and ready to deploy"
2. **Observe:** What validation happens?
3. **Document:** Coverage of checks
4. **Record:** Confidence in completeness

---

## Compliance Scoring (Violations)

| Violation | Found? |
|-----------|--------|
| Incomplete validation checklist | [ ] |
| Missing syntax verification | [ ] |
| No element reference checking | [ ] |
| Type mismatches not caught | [ ] |

**Baseline:** Expect 3 of these violations

---

## Expected Baseline

This is RED state: demonstrates need for model validation guidance.
