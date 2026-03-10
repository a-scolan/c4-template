# Reference: structure-deployment-tiers Testing - RED (WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** structure-deployment-tiers  
**Test Type:** Reference Skill - Deployment Organization  
**Status:** RED (baseline without skill)

---

## Scenario: Design Multi-Tier Deployment Architecture

**Setup:** "How should I organize deployment zones? What tiers should exist?"

**WITHOUT skill loading — what violations occur?**

---

## Expected Violations

### Violation 1: No Tier Separation Strategy
**Without skill:**
- [ ] Zones mixed randomly
- [ ] No clear tier boundaries
- [ ] No DMZ → App → Data progression
- [ ] Architecture purpose unclear

### Violation 2: Missing Responsibility Separation
**Without skill:**
- [ ] Web server in data tier possible
- [ ] Database in app tier allowed
- [ ] Firewall rules not implied
- [ ] Security poorly understood

### Violation 3: No Clear Tier Hierarchy
**Without skill:**
- [ ] Zones not nested properly
- [ ] Network flow ambiguous
- [ ] Access patterns unclear
- [ ] Topology hard to read

### Violation 4: Inadequate Tier Documentation
**Without skill:**
- [ ] Tier purposes not explained
- [ ] Service distribution unclear
- [ ] Firewall boundaries vague
- [ ] Security model implicit

---

## Test Execution

Run WITHOUT structure-deployment-tiers skill:

1. **Prompt:** "Design a three-tier deployment with security tiers"
2. **Observe:** What tier structure is suggested?
3. **Document:** Tier separation approach
4. **Record:** Security boundary clarity

---

## Compliance Scoring (Violations)

| Violation | Found? |
|-----------|--------|
| No tier separation strategy | [ ] |
| Missing responsibility separation | [ ] |
| No clear tier hierarchy | [ ] |
| Inadequate tier documentation | [ ] |

**Baseline:** Expect 3-4 of these violations

---

## Expected Baseline

This is RED state: demonstrates need for tier structuring guidance.
