# Sync with Template Upstream

Manage bidirectional improvements between a derived project and its upstream template (c4-template) using git subtree.

## 🎯 Concept

A derived project (e.g., `<foobar-project>`) has two types of files:

| Type | Examples | Sync to Template? | Reason |
|------|----------|-------------------|--------|
| **Generic** | `.github/skills/`, `projects/shared/spec-*.c4`, `.github/copilot-instructions.md` | ✅ YES | Reusable by all projects |
| **Project-Specific** | `projects/your-project/ADR/`, `projects/your-project/docs/`, `README.md`, `PROJECT_CHECKLIST.md` | ❌ NO | Unique project context |

**Golden Rule**: Before pushing to template, remove ALL mentions of the local project and generalize.

---

## 👉 Identify What Should Go to Template

### Files to Always Push

```bash
.github/skills/**/*.md          # Skill improvements & new skills
.github/copilot-instructions.md # Enhanced guidance & workspace instructions
projects/shared/spec-*.c4       # Reusable specifications (spec-code, spec-components, etc.)
projects/shared/images/         # Shared icons & diagrams
```

### Files to NEVER Push

```bash
projects/<foobar-project>/      # Project-specific code & models
README.md (root)                # Project navigation & introduction
PROJECT_CHECKLIST.md            # Project checklist
ADR/ (root of project)          # Project architecture decisions
docs/ (root)                    # Project documentation
likec4.config.json (root)       # Project configuration
```

### Process: Abstraction Before Push

Before pushing any improvement to template:

**Abstraction Checklist:**

- [ ] No mentions of project names (your-project, project-name, etc.)
- [ ] No absolute or context-specific paths
- [ ] No links to project-specific README.md or docs
- [ ] Generic language ("a derived project" vs "your-project")
- [ ] Generic examples (not domain-specific)
- [ ] "Do" vs "Don't" patterns instead of "dev-forge does/doesn't"

**Example - ❌ Avoid (Project-Specific):**
```markdown
# Create Relationship Skill for <FoobarProject>

Used in <foobar-project> for modeling payment systems...
See projects/<foobar-project>/ADR/0002-...
<FoobarProject> uses: `api -[calls]-> service`
```

**Example - ✅ Do (Generic):**
```markdown
# Create Relationship Skill

Used in architecture models to define system interactions...
Standard patterns include:
- Synchronous: `component -[calls]-> service`
- Asynchronous: `producer -[async]-> queue`
```

---

## 📤 Push Improvements to Template

### Step 1: Verify Content Purity

```bash
# Ensure c4-template remote exists
git remote -v | grep c4-template

# If missing:
git remote add c4-template https://github.com/a-scolan/c4-template.git
```

### Step 2: Create a Sync Branch

```bash
# Create branch FROM c4-template/main (IMPORTANT: not from local main)
git fetch c4-template main
git checkout -b sync/skills-template c4-template/main

# Or for specs (use consistent naming):
git checkout -b sync/spec-template c4-template/main
```

### Step 3: Cherry-Pick Generic Files

```bash
# Copy from local main (checkout from main branch into sync branch)
git checkout main -- .github/skills/create-element/SKILL.md

# OR copy multiple skills
git checkout main -- .github/skills/{create-relationship,create-sequence-view}/

# OR copy specs and instructions
git checkout main -- projects/shared/spec-*.c4 .github/copilot-instructions.md
```

### Step 4: Verify No Local Context

```bash
# Search for any project name mention
grep -r "<foobar-project>\|your-project\|myproject" .github/skills/ projects/shared/

# Search for local paths
grep -r "projects/<foobar-project>" .github/ projects/shared/

# Search for project-specific ADRs
grep -r "ADR-000[0-9]" .github/skills/  # Should only reference template ADRs
```

If local context found → **STOP and clean up before continuing**

⚠️ **CONFIDENTIALITY CHECK:** If you're unsure whether specific content contains confidential information (internal architecture, API schemas, security details, internal naming conventions, employee/team names, etc.), **STOP and ask your team or manager before pushing to the remote template repository**. Leaking confidential information to a public repository is a serious security risk.

### Step 5: Verify Final Checklist

Before committing, run this validation:

```bash
# Check all modified files for context leaks
git status
echo "=== Files to be committed ==="
git diff --cached --name-only

# Verify generic content
echo "=== Checking for project names ==="
git diff --cached | grep -E "<foobar-project>|your-project|myproject|confidential" || echo "✅ Clean"

echo "=== Checking for absolute paths ==="
git diff --cached | grep -E "C:|/home/|/Users/" || echo "✅ Clean"

echo "=== Checking for secrets (API keys, tokens, etc.) ==="
git diff --cached | grep -E "SECRET|TOKEN|PASSWORD|CREDENTIAL" || echo "✅ Clean"

echo "=== Checking for internal/confidential terms ==="
git diff --cached | grep -E "internal|confidential|proprietary|restricted" || echo "✅ Clean"

echo "=== Ready to commit ==="
```

**⚠️ MANUAL REVIEW REQUIRED:** If any checks fail or if you're uncertain about whether content should be public, **ask your team or manager BEFORE pushing**. It's better to be cautious than to accidentally leak confidential information.

### Step 6: Commit and Push

```bash
# Stage files to commit
git add .github/skills/ projects/shared/spec-*.c4 .github/copilot-instructions.md

# Commit with descriptive, generic message
git commit -m "sync: improve create-relationship skill with better examples

- Add detail about sync vs async relationships
- Include common patterns from successful projects
- Clarify best practices for relationship typing"

# Push branch (never push main directly!)
# ⚠️  BEFORE PUSHING: Review the changes one more time
echo "Review changes carefully before pushing:"
git diff --cached | less
echo ""
echo "⚠️  CONFIDENTIALITY CHECK - Does this contain ANY:"
echo "  - Internal paths or credentials?"
echo "  - Project-specific secrets or API details?"
echo "  - Security-sensitive architecture?"
echo "  - Internal naming (teams, projects, services)?"
echo "  - Employee/team member names?"
echo ""
echo "If ANY YES: Run 'git reset HEAD' and clean up, then ask your team"
echo "If ALL NO: Proceed with push"
echo ""
echo "UNCERTAIN? Ask your manager/team before proceeding!"

git push c4-template sync/skills-template --set-upstream
```

**Commit Message Examples:**

```
sync: add sync-with-template skill for bidirectional improvements
sync: enhance spec-containers with deployment patterns
sync: update copilot-instructions with documentation guidance
sync: improve create-element skill with metadata examples
```

### Step 7: Create PR on c4-template

1. Go to: https://github.com/a-scolan/c4-template/pulls
2. Click **New Pull Request**
3. Base: `main`
4. Compare: `sync/skills-template` (or `sync/spec-template` for specs)
5. Description: List improvements and why they matter
6. **⚠️ REVIEW ONCE MORE:** Check the diff carefully for ANY confidential information
7. Request reviewers and wait for approval before merge

---

## 📥 Pull Improvements from Template

### Recommended Sync Frequency

- **Automatic**: After a PR is merged into c4-template/main (if another project improved skills)
- **Scheduled**: Once per quarter (maintenance sync)
- **Event-driven**: When a new feature lands in template

### Pull Process

```bash
# On derived project's main branch
git fetch c4-template main

# Pull the three subtrees
git subtree pull --prefix=.github c4-template main --squash
git subtree pull --prefix=projects/shared c4-template main --squash
git subtree pull --prefix=projects/spec-showcase c4-template main --squash

# Resolve conflicts if needed (rare)
# Then push
git push origin main
```

### Resolve Conflicts (If Needed)

Occurs only if you modified subtree files locally AFTER sending updates to template:

```bash
# See conflicts
git status

# For each conflict, choose:
# Option 1: Keep local (your improvements)
git checkout --ours .github/skills/create-element/SKILL.md

# Option 2: Take template (their improvements)
git checkout --theirs .github/skills/create-element/SKILL.md

# Mark as resolved
git add .

# Finalize the merge
git commit -m "merge: resolve template sync conflicts"
git push origin main
```

**Note:** Conflicts are rare if you follow the rule: **Don't modify subtree files locally**. Send improvements TO TEMPLATE, then pull changes back.

---

## 🔄 Complete Cycle: Improvement → Template → Back

```
1. Derived project improves a skill
   ↓
2. Abstract content (remove project-specific references)
   ↓
3. Create sync/... branch from c4-template/main
   ↓
4. Cherry-pick generic files
   ↓
5. Push to c4-template and create PR
   ↓
6. Reviewer approves PR on c4-template
   ↓
7. Merge into c4-template/main
   ↓
8. Other projects pull via subtree pull
   ↓
9. Derived project also pulls changes (+ improvements from other projects)
   ↓
10. Cycle continues...
```

---

## Best Practices

### ✅ Do

- ✅ Remove ALL project names before pushing to template
- ✅ Test generic files locally before pushing
- ✅ Write descriptive PRs explaining why the change matters
- ✅ Wait for approval before merging (if you have permissions)
- ✅ Use `--squash` for subtree pulls (clean history)
- ✅ Push from `sync/*` branches (never push main directly to template)
- ✅ Group changes logically (skills vs specs vs instructions)
- ✅ Verify purity before committing (Step 5 validation)

### ❌ Don't

- ❌ Mention the derived project in template skills
- ❌ Push project-specific files (ADRs, docs, README)
- ❌ Push confidential information (internal paths, API keys, security details)
- ❌ Force-push without reason (except rare emergencies)
- ❌ Leave `sync/*` branches long-lived (clean up after merge)
- ❌ Modify subtree files locally then pull (conflicts)
- ❌ Commit template changes mixed with project-specific changes
- ❌ Push to remote WITHOUT reviewing diffs first (risk of leaking secrets)

---

## Troubleshooting

### "I'm unsure if something is generic or project-specific"

**Quick Checklist:**

- Does it make sense for ANY project using c4-template? → ✅ Generic
- Does it need adaptation to be reusable? → ❌ Too specific
- Does it apply to ALL projects? → ✅ Generic
- Does it apply to my project ONLY? → ❌ Specific

**🔐 CONFIDENTIALITY WARNING:** If you're uncertain whether content contains confidential information (internal names, API schemas, security details, internal architecture, employee names, etc.), **STOP and ask your team or manager before pushing to the template**. Better safe than sorry. Confidential information in a public repository cannot be easily removed.

### "My subtree pull says 'Already up to date' but there are changes"

```bash
# Force a refetch
git fetch c4-template --prune
git subtree pull --prefix=.github c4-template main --squash --force
```

### "How do I cherry-pick only one skill?"

```bash
# From sync/* branch
git checkout main -- .github/skills/create-element/SKILL.md

# Commit just that one
git add .github/skills/create-element/
git commit -m "sync: update create-element skill with new patterns"
```

### "Template merged my PR but I have other local changes"

```bash
# No problem!
# 1. Pull template changes
git fetch c4-template main
git subtree pull --prefix=.github c4-template main --squash

# 2. Your local changes stay in projects/your-project/ (unaffected)
# Verify:
git status  # Should be clean or only show projects/your-project/

# 3. Push local with template changes
git push origin main
```

---

## Real-World Example: Improve and Push a Skill

**Scenario:** You fix a bug in `create-relationship/SKILL.md` and want to push it to template.

```bash
# 1. On main, make the fix
vim .github/skills/create-relationship/SKILL.md
git add .
git commit -m "fix: improve relationship syntax examples"

# 2. Verify no local context
grep -r "<foobar-project>\|your-project\|internal\|confidential" .github/skills/create-relationship/SKILL.md  # Should be empty

# 3. Create branch from template (use consistent naming)
git fetch c4-template main
git checkout -b sync/skills-template c4-template/main

# 4. Cherry-pick the change
git checkout main -- .github/skills/create-relationship/SKILL.md

# 5. Commit cleanly
git add .github/skills/create-relationship/SKILL.md
git commit -m "sync: improve relationship syntax examples

- Add clarity on calls vs async patterns
- Clarify when to use each kind
- Include real-world examples"

# 6. ⚠️ REVIEW BEFORE PUSHING
echo "Review changes:"
git diff --cached
echo ""
echo "🔐 CONFIDENTIALITY CHECK - Does this contain ANY:"
echo "  - Project-specific paths?"
echo "  - Internal API details?"
echo "  - Confidential architecture?"
echo "  - Security credentials?"
echo "  - Employee or team names?"
echo ""
echo "If UNCERTAIN or ANY yes: run 'git reset HEAD', clean up, and ask your team"
echo "If all no: proceed:"

# 7. Push and create PR
git push c4-template sync/skills-template --set-upstream
# Then create PR via GitHub UI
```

---

## Future: CI/CD Automated Sync

Future improvements could include GitHub Actions for:

1. **Quarterly Updates**: Auto-pull from c4-template and create PR
2. **Context Detection**: Scan files to push for local context
3. **Validation**: Verify generic files load correctly

For now: execute manually following this workflow.
