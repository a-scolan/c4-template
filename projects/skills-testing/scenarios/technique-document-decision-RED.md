# Technique: document-decision Testing - RED (WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** document-decision  
**Test Type:** Technique Skill - ADR Documentation  
**Status:** RED (baseline without skill)

---

## Scenario: Record Technology Selection Decision

**Setup:** "We're choosing between Docker and Podman for deployment. Document the decision."

**WITHOUT skill loading — what violations occur?**

---

## Expected Violations

### Violation 1: Informal Documentation
**Without skill:**
- [ ] No structured format
- [ ] Context missing
- [ ] Rationale not recorded
- [ ] Future reference unclear

### Violation 2: Missing Context Section
**Without skill:**
- [ ] Problem statement vague
- [ ] Constraints not documented
- [ ] Requirements not listed
- [ ] Decision drivers unclear

### Violation 3: Incomplete Trade-offs
**Without skill:**
- [ ] Only benefits mentioned
- [ ] Drawbacks not documented
- [ ] Not vs Then alternatives missing
- [ ] Trade-off analysis shallow

### Violation 4: No Consequences Recorded
**Without skill:**
- [ ] Outcomes not anticipated
- [ ] Impact not documented
- [ ] Follow-up actions missing
- [ ] Decision reversibility unclear

---

## Test Execution

Run WITHOUT document-decision skill:

1. **Prompt:** "Document our decision to use Podman instead of Docker"
2. **Observe:** What documentation structure emerges?
3. **Document:** Format and completeness
4. **Record:** Context and rationale depth

---

## Compliance Scoring (Violations)

| Violation | Found? |
|-----------|--------|
| Informal documentation | [ ] |
| Missing context section | [ ] |
| Incomplete trade-offs | [ ] |
| No consequences recorded | [ ] |

**Baseline:** Expect 3-4 of these violations

---

## Expected Baseline

This is RED state: demonstrates need for ADR documentation guidance.
