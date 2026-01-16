---
name: understand-project-structure
description: Load project context before making changes. Use when starting work to check available element kinds, relationship types, and tags.
---

# Understand Project Structure

Use this skill when starting work on a LikeC4 project or before making significant changes.

## Workspace Structure

- **Shared specifications:** `projects/shared/spec-*.c4` - Source of truth for element kinds, relationship types, and tags
- **MCP servers (REQUIRED):** Use LikeC4 MCP and Context7 MCP for context gathering
- **ADR documentation:** `ADR/` directory - System architecture decisions using standard ADR format

## Steps

1. **Use LikeC4 MCP (REQUIRED):** `list-projects` or `read-project-summary` to get project overview
2. Read `likec4.config.json` to understand includes and image aliases
3. Check `projects/shared/spec-*.c4` for available element kinds, relationship types, and tags
4. Review existing model files to understand architecture patterns
5. **Use Context7 MCP:** Query LikeC4 documentation if uncertain about syntax or features

## Output

Complete understanding of project structure, available element kinds, and current architecture.
