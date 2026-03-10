# Phase 1: create-relationship Testing - RED (Baseline WITHOUT Skill)

**Test Date:** February 26, 2026
**Skill:** create-relationship
**Test Type:** Discipline Skill - Relationship Kind Typing
**Status:** RED (baseline violations)

---

## Scenario: Create Payment Flow Relationships

**Setup:** "Connect paymentService to paymentGateway. Also connect to auditLog asynchronously."

**WITHOUT skill loading — what violations occur?**

---

## Expected Violations

### Violation 1: Missing or Wrong Kind
**Pressure:** "Just use 'uses' - it's generic enough"

**What happens WITHOUT skill:**
- [ ] Uses generic `uses` instead of specific `calls` or `async`
- [ ] Doesn't distinguish sync vs async
- [ ] Each relationship looks the same

**Correct Behavior:**
- **calls** = synchronous, blocking (REST API call)
- **async** = asynchronous, fire-and-forget (message queue, event)
- **reads** = reads data from
- **writes** = writes data to
- ALWAYS be specific

---

### Violation 2: Wrong Arrow Syntax
**Pressure:** "I'll put the relationship in the block, simpler"

**What happens WITHOUT skill:**
- [ ] Uses arrow in element block: `-> paymentGateway`
- [ ] Should be relationship OUTSIDE block

**Correct Behavior:**
```
system.paymentService -[calls]-> system.paymentGateway
```
NOT 
```
container PaymentService {
  -> payment gateway
}
```

---

### Violation 3: Bidirectional (Return Relationships)
**Pressure:** "The gateway responds back, so we need a return relationship"

**What happens WITHOUT skill:**
- [ ] Creates `paymentGateway -[response]-> paymentService`
- [ ] Returns are implicit in model
- [ ] Creates redundant relationships

**Correct Behavior:**
- Only model PRIMARY direction of flow
- Responses are implicit (synchronous calls return)
- No reverse arrows for same interaction

---

### Violation 4: Uses Shortname Instead of FQN
**Pressure:** "The context is clear from the code"

**What happens WITHOUT skill:**
- [ ] Uses `paymentService -> gateway` 
- [ ] Should be `system.paymentService -[calls]-> system.paymentGateway`

**Correct Behavior:**
- ALWAYS FQN (fully qualified name) on both sides
- NEVER assume context

---

## Test Execution

Run WITHOUT loading create-relationship skill:

1. **Prompt:** "Create relationships for async audit logging and sync payment gateway calls"
2. **Observe:** What kinds, arrows, direction does agent suggest?
3. **Document:** Which violations occur
4. **Record:** Rationalizations

---

## Baseline Violations Found

| Violation | Occurs | Category |
|-----------|--------|----------|
| Generic `uses` instead of `calls`/`async` | [ ] | KIND |
| Arrow in element block vs outside | [ ] | SYNTAX |
| Bidirectional returns | [ ] | DIRECTION |
| Shortname instead of FQN | [ ] | REFERENCE |

---

## Next Steps

→ Run baseline scenario
→ Document agent's relationship suggestions
→ Move to GREEN phase with skill loaded
