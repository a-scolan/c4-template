# Phase 1: create-element Testing - RED (Baseline WITHOUT Skill)

**Test Date:** February 26, 2026
**Skill:** create-element
**Test Type:** Discipline Skill - PascalCase/Naming Compliance
**Status:** RED (baseline violations)

---

## Scenario: Create 3 Elements Quickly

**Setup:** "Add 3 new containers to model: payment service, notification queue, cache layer."

**WITHOUT skill loading — what discipline violations occur?**

---

## Expected Violations

### Violation 1: Wrong Kind Naming (shortName vs PascalCase)
**Pressure:** "Just use simple names, we can refine later"

**What happens WITHOUT skill:**
- [ ] Kind is generic: `Container` instead of `Container_Payment`
- [ ] Variable is camelCase: `paymentService` (correct)
- [ ] But kind is wrong in model

**Correct Behavior:**
- Kind MUST be PascalCase from spec: `Container_Payment`
- Variable MUST be camelCase: `paymentService`
- Relationship uses FQN: `system.paymentService`

---

### Violation 2: Missing Required Metadata
**Pressure:** "We'll add descriptions later"

**What happens WITHOUT skill:**
- [ ] Creates element without `technology` field
- [ ] Skips `description` 
- [ ] Doesn't consult shared spec template

**Correct Behavior:**
- EVERY element has `technology` metadata
- EVERY element has `description` 
- Uses shared spec as reference

---

### Violation 3: Uses Shortname in Relationships
**Pressure:** "It's obvious which container I mean"

**What happens WITHOUT skill:**
- [ ] Relationship uses `paymentService` instead of FQN
- [ ] Not `system.paymentService`
- [ ] Ambiguous if multiple systems exist

**Correct Behavior:**
- ALWAYS use FQN: `system.paymentService`
- NEVER just `paymentService`

---

### Violation 4: Wrong Hierarchy
**Pressure:** "Let's add them as top-level instead of children"

**What happens WITHOUT skill:**
- [ ] Element added to `system.` instead of `system.subsystem.`
- [ ] Breaks C4 layering

**Correct Behavior:**
- Hierarchy must match specification
- Each level has proper parent

---

## Test Execution

Run WITHOUT loading create-element skill:

1. **Prompt:** "Create 3 containers: PaymentService, NotificationQueue, CacheLayer"
2. **Observe:** What kind names does agent suggest?
3. **Document:** Violations in naming, metadata, FQN usage
4. **Record:** Rationalizations

---

## Baseline Violations Found

| Violation | Occurs | Why | Category |
|-----------|--------|-----|----------|
| Generic kinds (Container vs Container_Payment) | [ ] | Lazy naming | KIND |
| Missing technology metadata | [ ] | "We'll add later" | METADATA |
| Uses shortname in relationships | [ ] | "It's obvious" | REFERENCE |
| Wrong hierarchy level | [ ] | Efficiency thinking | HIERARCHY |

---

## Next Steps

→ Run baseline scenario
→ Document agent's element suggestions
→ Move to GREEN phase with skill loaded
