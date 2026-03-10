# Reference: lookup-element-kinds Testing - RED (WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** lookup-element-kinds  
**Test Type:** Reference Skill - Kind Discovery  
**Status:** RED (baseline without skill)

---

## Scenario: Validate Element Kind Names

**Setup:** "What are valid element kinds? Is 'apigateway' a valid kind or should it be 'ApiGateway'?"

**WITHOUT skill loading — what violations occur?**

---

## Expected Violations

### Violation 1: Guessing About Conventions
**Without skill:**
- [ ] No reference to naming standards
- [ ] Assumes conventions
- [ ] May suggest wrong kind
- [ ] User unsure of answer

### Violation 2: Missing Kind Validation Approach
**Without skill:**
- [ ] Doesn't explain how to check
- [ ] No lookup methodology
- [ ] User can't verify independently
- [ ] One-off answers only

### Violation 3: Incomplete Kind Coverage
**Without skill:**
- [ ] Lists obvious kinds only
- [ ] Misses custom kinds
- [ ] No system or container distinctions
- [ ] Partial knowledge

### Violation 4: No Specification Reference
**Without skill:**
- [ ] Doesn't point to authoritative source
- [ ] No spec-code.c4 reference
- [ ] User can't learn pattern
- [ ] Knowledge not transferable

---

## Test Execution

Run WITHOUT lookup-element-kinds skill:

1. **Prompt:** "Is 'apigateway' valid? What kinds exist?"
2. **Observe:** Does it explain naming conventions?
3. **Document:** Approach to validation
4. **Record:** Completeness of kind list

---

## Compliance Scoring (Violations)

| Violation | Found? |
|-----------|--------|
| Guessing about conventions | [ ] |
| Missing kind validation approach | [ ] |
| Incomplete kind coverage | [ ] |
| No specification reference | [ ] |

**Baseline:** Expect 3 of these violations

---

## Expected Baseline

This is RED state: demonstrates need for element kind lookup guidance.
