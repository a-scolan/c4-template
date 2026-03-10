# Discipline: write-rich-descriptions Testing - RED (Baseline WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** write-rich-descriptions  
**Test Type:** Discipline Skill - Metadata vs Markdown Tables  
**Status:** RED (baseline violations)

---

## Scenario: Document Complex Infrastructure Configuration

**Setup:** "Add rich descriptions to a deployment node: ProdDMZZone running 3 VMs with network settings"

**WITHOUT skill loading — what organization issues occur?**

---

## Expected Violations

### Violation 1: Metadata and Markdown Mixed Incorrectly
**Pressure:** "Just put everything in description, it's simpler"

**What happens WITHOUT skill:**
- [ ] Puts network specs in metadata instead of markdown table
- [ ] Mixes data structure with prose paragraphs
- [ ] No clear separation between queryable metadata and documentation

**Correct Behavior:**
- Metadata for queryable fields: owner, env, tier
- Markdown tables for specs: network interfaces, IP ranges, ports
- Prose for context and responsibilities

---

### Violation 2: Network Interfaces Not First in Tables
**Pressure:** "List them in any order"

**What happens WITHOUT skill:**
- [ ] Network interfaces somewhere in the middle
- [ ] Ports, IPs, services listed first
- [ ] Makes scanning difficult

**Correct Behavior:**
- Network interfaces ALWAYS first (eth0, eth1, etc.)
- Then IPs, ports, services
- Then capabilities and notes

---

## Test Execution

Run WITHOUT loading write-rich-descriptions skill:

1. **Prompt:** "Add rich description to ProdDMZZone with network config"
2. **Observe:** Where are network details placed?
3. **Document:** What's in metadata vs markdown table?
4. **Record:** Order of information

---

## Baseline Violations Found

| Violation | Occurs | Why | Fix |
|-----------|--------|-----|-----|
| Wrong field in metadata vs markdown | [ ] | Unclear boundary | Define rule |
| Network interfaces not first | [ ] | Unknown priority | Make explicit |
| No table structure | [ ] | Mixed with prose | Enforce markdown |

---

## Next Steps

→ Run baseline scenario  
→ Document agent's description structure  
→ Move to GREEN phase with skill loaded
