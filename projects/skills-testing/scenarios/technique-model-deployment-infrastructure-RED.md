# Technique: model-deployment-infrastructure Testing - RED (WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** model-deployment-infrastructure  
**Test Type:** Technique Skill - Deployment Hierarchy  
**Status:** RED (baseline without skill)

---

## Scenario: Model Multi-Zone Production Environment

**Setup:** "Design deployment hierarchy with DMZ, App, and Data zones containing VMs"

**WITHOUT skill loading — what violations occur?**

---

## Expected Violations

### Violation 1: Incorrect Zone Naming
**Without skill:**
- [ ] Zones not following tier naming conventions
- [ ] VM names inconsistent
- [ ] No {Environment}{Service} pattern
- [ ] Hard to scan infrastructure

### Violation 2: Missing VM Details
**Without skill:**
- [ ] Sparse descriptions
- [ ] Network configuration unclear
- [ ] No markdown tables for specs
- [ ] Infrastructure invisible

### Violation 3: Poor Hierarchy Structure
**Without skill:**
- [ ] Zones mixed with VMs without clear tiers
- [ ] No parent-child relationships
- [ ] instanceOf links missing
- [ ] Deployment model incomplete

### Violation 4: Incomplete Instances
**Without skill:**
- [ ] VMs not properly representing services
- [ ] No metadata for roles
- [ ] Instance relationships vague
- [ ] No deployment tracking

---

## Test Execution

Run WITHOUT model-deployment-infrastructure skill:

1. **Prompt:** "Model a three-tier deployment with zones and VMs"
2. **Observe:** How is hierarchy structured?
3. **Document:** Naming patterns used
4. **Record:** Completeness of deployment model

---

## Compliance Scoring (Violations)

| Violation | Found? |
|-----------|--------|
| Incorrect zone naming | [ ] |
| Missing VM details | [ ] |
| Poor hierarchy structure | [ ] |
| Incomplete instances | [ ] |

**Baseline:** Expect 3-4 of these violations

---

## Expected Baseline

This is RED state: demonstrates need for deployment modeling guidance.
