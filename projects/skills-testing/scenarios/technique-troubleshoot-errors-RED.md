# Technique: troubleshoot-errors Testing - RED (WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** troubleshoot-errors  
**Test Type:** Technique Skill - Error Diagnosis  
**Status:** RED (baseline without skill)

---

## Scenario: Debug Model Build Errors

**Setup:** "Get error message: 'Element not found: shop.unknown'. What went wrong?"

**WITHOUT skill loading — what violations occur?**

---

## Expected Violations

### Violation 1: No Root Cause Analysis
**Without skill:**
- [ ] Just restates error
- [ ] Doesn't explain why
- [ ] No systematic diagnosis
- [ ] User still confused

### Violation 2: Missing Context Checks
**Without skill:**
- [ ] Doesn't ask about element definition
- [ ] Relationship context not examined
- [ ] View include patterns not questioned
- [ ] Partial debugging

### Violation 3: No Solution Path
**Without skill:**
- [ ] Error noted but fix unclear
- [ ] Multiple possible causes not enumerated
- [ ] Verification steps missing
- [ ] User must guess

### Violation 4: Incomplete Information Gathering
**Without skill:**
- [ ] Doesn't check element kinds
- [ ] Relationship types not validated
- [ ] Similar element names not suggested
- [ ] Diagnostic depth limited

---

## Test Execution

Run WITHOUT troubleshoot-errors skill:

1. **Prompt:** "I get: 'Element not found: shop.unknown' but I defined it"
2. **Observe:** What diagnosis is offered?
3. **Document:** Root cause analysis depth
4. **Record:** Solution clarity

---

## Compliance Scoring (Violations)

| Violation | Found? |
|-----------|--------|
| No root cause analysis | [ ] |
| Missing context checks | [ ] |
| No solution path | [ ] |
| Incomplete information gathering | [ ] |

**Baseline:** Expect 3 of these violations

---

## Expected Baseline

This is RED state: demonstrates need for troubleshooting guidance.
