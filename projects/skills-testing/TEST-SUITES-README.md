# Writing Test Suites for Skills Using TDD

This directory contains test scenarios for all 19 skills, organized by skill type and test phase.

## Organization

```
tests/
├── discipline/           # Skills enforcing rules under pressure
│   ├── SKILL-RED.md     # Baseline without skill
│   └── SKILL-GREEN.md   # Compliance with skill
├── technique/           # Skills teaching how-to
│   ├── SKILL-RED.md
│   └── SKILL-GREEN.md
└── reference/           # Skills providing lookup/reference
    ├── SKILL-RED.md
    └── SKILL-GREEN.md
```

## Test Methodology (TDD)

Each skill has paired RED/GREEN tests:

**RED (Baseline):** What happens WITHOUT the skill loaded?
- What shortcuts does agent take?
- Which rules are violated?
- What rationalizations are used?

**GREEN (Compliance):** What happens WITH the skill loaded?
- Does agent follow all rules?
- Are all guidelines applied?
- Pass/fail on 5-10 specific criteria

## Skills Tested

### Discipline Skills (5)
Rules-enforcing skills that require specific decisions under pressure:
- sync-with-template (confidentiality before pushing)
- create-element (PascalCase kinds, FQN references)
- create-relationship (specific kinds, proper arrow syntax)
- configure-project-includes (multi-file organization safety)
- write-rich-descriptions (metadata vs markdown tables)

### Technique Skills (10)
How-to skills teaching concrete methods:
- understand-project-structure (load context before changes)
- c4-modeling-process (C1→C2→C3 hierarchy)
- design-view (include patterns, categories)
- customize-view (styling, layout control)
- create-sequence-view (temporal flows, initiating actor)
- model-deployment-infrastructure (hierarchy, naming, tables)
- test-model (validation completeness)
- troubleshoot-errors (diagnosis accuracy)
- document-decision (ADR format)
- organize-multi-project (shared specs setup)

### Reference Skills (4)
Lookup/discovery skills:
- lookup-element-kinds (find valid kinds)
- implement-pattern (pattern recognition)
- name-deployment-nodes (naming formulas)
- structure-deployment-tiers (tier organization)

## Running Tests

```bash
# Test single skill
./test-skills-gh-cli.sh create-element

# Test all discipline skills
./test-skills-gh-cli.sh sync-with-template create-element create-relationship \
  configure-project-includes write-rich-descriptions

# Test all skills
./test-skills-gh-cli.sh
```

## Test Scenarios Created

**All test suites include:**
- Clear RED scenario (pressure situation)
- Expected baseline violations
- GREEN scenario (same situation WITH skill)
- Specific pass/fail criteria
- Scoring mechanism

## Next Steps

1. Run tests using hybrid approach (script + agent)
2. Collect RED and GREEN responses
3. Score compliance
4. Generate comprehensive report per skill
