Use a dedicated `sync/*` branch that starts from `c4-template/main`, then bring over only the generic file.

1. Make sure your local improvement exists on `main`.
2. Fetch the template upstream:

```bash
git fetch c4-template main
```

3. Create a sync branch from the template, not from your local `main`:

```bash
git checkout -b sync/skills-template c4-template/main
```

4. Copy only the generic skill file from your local `main` onto that branch:

```bash
git checkout main -- .github/skills/create-relationship/SKILL.md
```

5. Stage it and review exactly what will be pushed:

```bash
git add .github/skills/create-relationship/SKILL.md
git diff --cached
```

6. Do a confidentiality and genericity review **before any push**:
   - no project names
   - no internal architecture details
   - no security-sensitive content
   - no employee or team names

7. Commit only after that review passes:

```bash
git commit -m "sync: improve create-relationship skill"
```

8. Push the `sync/*` branch to the template remote:

```bash
git push c4-template sync/skills-template --set-upstream
```

This keeps the template update isolated, pushes only the generic file, and avoids pushing directly from `main`.
