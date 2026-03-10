# Skills Testing

Fully automated RED-GREEN testing of all 19 LikeC4 skills. Just run the script.

## Quick Start

```bash
# Run complete test suite (one command does everything)
./test-skills.sh

# Manual cleanup if needed
./test-skills.sh reset
```

The script automatically:
1. Resets workspace to pristine state
  - Restores hidden skills without creating nested `skill/skill` folders
  - Auto-heals previously nested duplicate skill directories if found
2. Discovers all 19 skills from scenarios/
3. Prepares test environment (backup, hide skills)
4. Executes RED-GREEN tests for each skill
5. Generates insightful report with patterns
6. Restores all skills and cleans up

## What You Get

The script generates **SKILLS-TEST-REPORT.md** with:
- 🎯 **Key findings** - which categories work best, overall effectiveness
- 📊 **Pattern analysis** - common issues without skills, common improvements with skills  
- ✅ **Detailed results** - per-skill RED/GREEN comparison
- 💡 **Recommendations** - actionable next steps based on findings

Not just numbers - actual insights about what skills improve and how.

## Test Files

Located in `scenarios/` subfolder. Organized by skill type (38 total: RED/GREEN pairs for each of 19 skills):

- `scenarios/CATEGORY-SKILL-RED.md` → Baseline test (without skill)
- `scenarios/CATEGORY-SKILL-GREEN.md` → Compliance test (with skill)

**Test Coverage:**
- **5 Discipline skills** (enforce rules under pressure)
  - sync-with-template
  - create-element
  - create-relationship
  - configure-project-includes
  - write-rich-descriptions

- **10 Technique skills** (concrete how-to methods)
  - understand-project-structure
  - c4-modeling-process
  - design-view
  - customize-view
  - create-sequence-view
  - model-deployment-infrastructure
  - test-model
  - troubleshoot-errors
  - document-decision
  - organize-multi-project

- **4 Reference skills** (lookup/discovery)
  - lookup-element-kinds
  - implement-pattern
  - name-deployment-nodes
  - structure-deployment-tiers

## How It Works

**Single command runs the complete pipeline:**

1. **Prepare** - Auto-discovers skills, backs up, hides from context
2. **Execute** - For each skill:
   - RED phase: Simulates without skill (documents violations)
   - GREEN phase: Simulates with skill (documents improvements)
   - Compares RED vs GREEN baseline
3. **Analyze** - Finds patterns across all skills:
   - Most common violations without skills
   - Most impactful improvements with skills
   - Category-level effectiveness rates
4. **Report** - Generates insights (not just numbers)
5. **Cleanup** - Restores all skills, removes temp files

**Output:** Single `SKILLS-TEST-REPORT.md` with actionable insights

## Documentation

- **SKILLS-TEST-REPORT.md** — Insights and recommendations (generated after testing)
- [TEST-SUITES-README.md](TEST-SUITES-README.md) — All 19 skills test organization

## Safety

✅ Full backup before any skill movement  
✅ Zero git history pollution (no stash)  
✅ Atomic operations (all-or-nothing)  
✅ Error recovery with backup restoration  
✅ Cleanup of temporary files


