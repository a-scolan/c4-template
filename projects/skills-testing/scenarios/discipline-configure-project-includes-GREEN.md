# Discipline: configure-project-includes Testing - GREEN (WITH Skill)

**Test Date:** February 26, 2026  
**Skill:** configure-project-includes  
**Test Type:** Discipline Skill - Multi-file Include Safety  
**Status:** GREEN (compliance verification)

---

## Scenario: Add New Project to Multi-Project Workspace

**Setup:** "I have a new project 'microservices' - add it to likec4.config.ts with shared specs"

**WITH skill loading — what compliance improvements occur?**

---

## Expected Compliance

### Rule 1: Verify Shared vs Project-Specific Files
**With skill:**
- [ ] Identifies which files are shared (`spec-*.c4`)
- [ ] Separates shared specs from project-specific models
- [ ] Documents the include strategy
- [ ] Only includes necessary files

### Rule 2: Verify Image Paths Before Adding
**With skill:**
- [ ] Checks that all custom image paths exist
- [ ] Verifies lucide icons are available
- [ ] Documents image sources (custom, lucide-static)
- [ ] Uses correct path format

### Rule 3: Use Consistent Relative Paths
**With skill:**
- [ ] All paths use same style (relative from config)
- [ ] No mixing of absolute and relative paths
- [ ] Clear path structure documentation
- [ ] Works from any subdirectory

### Rule 4: Document Include Strategy
**With skill:**
- [ ] Comments explain why files are included
- [ ] Shared spec comment section present
- [ ] Project-specific files documented
- [ ] Why others are excluded documented

---

## Test Execution

Run WITH loading configure-project-includes skill:

1. **Prompt:** "Add new project configuration with includes and image aliases"
2. **Observe:** What verification is done?
3. **Document:** Which compliance rules are followed
4. **Record:** How agent explains choices

---

## Compliance Scoring

| Rule | Score |
|------|-------|
| Shared vs project-specific separation | [ ] / 5 |
| Image path verification | [ ] / 5 |
| Consistent relative paths | [ ] / 5 |
| Include strategy documentation | [ ] / 5 |

**Pass Threshold:** 16/20 (80%)

---

## Next Steps

→ Score against RED baseline  
→ Compare compliance improvements  
→ Generate final report
