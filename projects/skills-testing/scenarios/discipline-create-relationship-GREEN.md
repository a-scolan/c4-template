# Phase 1: create-relationship Testing - GREEN (WITH Skill Loaded)

**Test Date:** February 26, 2026
**Skill:** create-relationship
**Test Type:** Discipline Skill - Relationship Kind Typing
**Status:** GREEN (compliance check)

---

## Scenario: Create Payment Flow Relationships

**Setup:** "Connect paymentService to paymentGateway. Also connect to auditLog asynchronously."

**WITH skill loaded — did agent use correct kinds and syntax?**

---

## Compliance Checklist

### Rule 1: Specific Kind for Sync
**Requirement:** Synchronous call uses `calls` (or `syncs`, NOT generic `uses`)

```
Expected: paymentService -[calls]-> paymentGateway
NOT: paymentService -[uses]-> paymentGateway
```

**Actual Relationship:**
[COPY AGENT'S SYNC RELATIONSHIP HERE]

**Compliance:** ✅ YES / ❌ NO

---

### Rule 2: Specific Kind for Async
**Requirement:** Asynchronous uses `async` (NOT `sends`, NOT `publishes`)

```
Expected: paymentService -[async]-> auditLog
NOT: paymentService -[sends]-> auditLog
```

**Actual Relationship:**
[COPY AGENT'S ASYNC RELATIONSHIP HERE]

**Compliance:** ✅ YES / ❌ NO

---

### Rule 3: Correct Syntax (Outside Block)
**Requirement:** Relationship defined OUTSIDE element block with arrow

```
Correct:
  system.paymentService -[calls]-> system.paymentGateway

NOT:
  container PaymentService {
    -> gateway
  }
```

**Actual Definition:**
[COPY AGENT'S RELATIONSHIP DEFINITION HERE]

**Compliance:** ✅ YES / ❌ NO

---

### Rule 4: FQN on Both Sides
**Requirement:** Source and target are fully qualified names

```
Correct: system.paymentService -[calls]-> system.paymentGateway
NOT: paymentService -[calls]-> gateway
```

**Actual Relationship:**
[COPY AGENT'S NAMES HERE]

**Compliance:** ✅ YES / ❌ NO

---

### Rule 5: No Bidirectional Returns
**Requirement:** Does NOT create reverse relationship for same interaction

```
Should be ONE direction:
  paymentService -[calls]-> gateway

NOT both:
  paymentService -[calls]-> gateway
  gateway -[response]-> paymentService  ❌
```

**Actual Relationships Suggested:**
[COPY ALL RELATIONSHIPS AGENT CREATED]
Count: ____ relationships for 1 interaction (should be 1)

**Compliance:** ✅ YES / ❌ NO

---

## Compliance Score

```
Total Rules: 5
Passed: __/5
Failed: __/5

Pass Rate: __%
```

**Threshold:** Must pass 5/5 (100%) - This is a discipline skill with modeling impact.

---

## Violations Found

| Rule | Violation | Severity | Fix |
|------|-----------|----------|-----|
| | | | |
| | | | |

---

## Time Pressure Test (Optional Future)

**Pressure:** "Quick, just add the relationships, don't worry about kinds"

Does agent still apply the 5 rules under time pressure?

---

## Notes

**Common Rationalizations to Watch For:**
- "The gateway responds, so we need a return relationship"
- "It doesn't matter which specific kind, they're all relationships"
- "Generic 'uses' is simpler"
