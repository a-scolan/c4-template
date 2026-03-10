# Discipline: configure-project-includes Testing - RED (Baseline WITHOUT Skill)

**Test Date:** February 26, 2026  
**Skill:** configure-project-includes  
**Test Type:** Discipline Skill - Multi-file Include Safety  
**Status:** RED (baseline violations may occur)

---

## Scenario: Add New Project to Multi-Project Workspace

**Setup:** "I have a new project 'microservices' - add it to likec4.config.ts with shared specs"

**WITHOUT skill loading — what safety shortcuts might occur?**

---

## Expected Violations

### Violation 1: Include All Files Without Review
**Pressure:** "Just add everything to includes, we'll clean up later"

**What happens WITHOUT skill:**
- [ ] Adds all *.c4 files to includes (including project-specific ones)
- [ ] Doesn't verify shared vs project-specific separation
- [ ] Mixes local paths with relative paths

**Correct Behavior:**
- Only include shared specs and project files
- Exclude project-specific context files
- Use consistent relative paths
- Document the include strategy

---

### Violation 2: No Verification of Image Aliases
**Pressure:** "Image paths look fine to me"

**What happens WITHOUT skill:**
- [ ] Adds image aliases without checking if paths exist
- [ ] Doesn't verify lucide icons are available
- [ ] References custom images that don't exist

**Correct Behavior:**
- Verify all image paths exist before adding to config
- Document image source locations
- Use lucide-static for universal icons

---

## Test Execution

Run WITHOUT loading configure-project-includes skill:

1. **Prompt:** "Add new project configuration with includes and image aliases"
2. **Observe:** What paths are suggested? Are they verified?
3. **Document:** Which file organization violations occur
4. **Record:** Rationalizations used

---

## Baseline Violations Found

| Violation | Occurs | Why | Fix |
|-----------|--------|-----|-----|
| No shared spec verification | [ ] | "Obvious which are shared" | Document strategy |
| Unverified image paths | [ ] | "Looks correct" | Add verification step |
| Mixed path styles | [ ] | "Both work" | Enforce consistency |
| No config documentation | [ ] | "Self-explanatory" | Add comments |

---

## Next Steps

→ Run baseline scenario  
→ Document agent's configuration suggestions  
→ Move to GREEN phase with skill loaded
