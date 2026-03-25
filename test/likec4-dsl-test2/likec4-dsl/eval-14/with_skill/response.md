`styles { theme dark }` fails for two reasons. First, `styles` is not a valid top-level statement. SKILL.md rule 2 states that only `import`, `specification`, `model`, `deployment`, `views`, and `global` are allowed at the top level. Second, `theme` is not a recognized property in any LikeC4 DSL block — light/dark theme is a project-level configuration concern, not a model-file property, and cannot be expressed in a `.c4` file at all. The intent must be handled in the project config file (`likec4.config.json`). Because no top-level DSL statement expresses a theme toggle, the closest minimal valid `.c4` file that satisfies the parser while documenting the intent is:

```likec4
// Theme preference (e.g. dark) belongs in likec4.config.json, not in model files.
views {
}
```

This file is syntactically valid (it contains one allowed top-level block) but one must understand that the dark-theme intent cannot be expressed inside a `.c4` file — it requires a `likec4.config.json` entry instead.
