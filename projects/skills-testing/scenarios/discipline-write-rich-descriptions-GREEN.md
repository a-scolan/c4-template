# Discipline: write-rich-descriptions Testing - GREEN (WITH Skill)

**Test Date:** February 26, 2026  
**Skill:** write-rich-descriptions  
**Test Type:** Discipline Skill - Metadata vs Markdown Tables  
**Status:** GREEN (compliance verification)

---

## Scenario: Document Complex Infrastructure Configuration

**Setup:** "Add rich descriptions to a deployment node: ProdDMZZone running 3 VMs with network settings"

**WITH skill loading — what compliance improvements occur?**

---

## Expected Compliance

### Rule 1: Correct Metadata vs Markdown Tables Separation
**With skill:**
- [ ] Metadata for queryable fields (owner, environment, tier)
- [ ] Markdown tables for infrastructure specs
- [ ] Clear boundary between queryable and documentation
- [ ] Follows shared spec patterns

### Rule 2: Network Interfaces First in Tables
**With skill:**
- [ ] Network interfaces (eth0, eth1) listed first in markdown table
- [ ] Easy to scan for networking topology
- [ ] IPs, ports, services follow interfaces
- [ ] Makes infrastructure self-documenting

### Rule 3: Rich But Structured Descriptions
**With skill:**
- [ ] Markdown formatting (bold, italic, bullet lists)
- [ ] Responsibilities section
- [ ] Capability notes
- [ ] Security or performance context

### Rule 4: Queryable Metadata Used Correctly
**With skill:**
- [ ] owner, environment, tier in metadata
- [ ] Enables filtering and searching
- [ ] Avoids duplicating prose in metadata
- [ ] Consistent with write-rich-descriptions approach

---

## Test Execution

Run WITH loading write-rich-descriptions skill:

1. **Prompt:** "Add rich description to ProdDMZZone with network config"
2. **Observe:** How is description structured?
3. **Document:** Metadata vs markdown separation
4. **Record:** Order and organization of information

---

## Compliance Scoring

| Rule | Score |
|------|-------|
| Metadata vs markdown separation | [ ] / 5 |
| Network interfaces priority | [ ] / 5 |
| Markdown structure and richness | [ ] / 5 |
| Queryable metadata usage | [ ] / 5 |

**Pass Threshold:** 16/20 (80%)

---

## Next Steps

→ Score against RED baseline  
→ Compare structure improvements  
→ Generate final report
