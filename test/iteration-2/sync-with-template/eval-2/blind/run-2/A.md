## First comparisons to re-sync includes and aliases safely

Start with the project configuration, not the diagrams.

1. Compare the include paths that pull shared specs into the project.
2. Compare alias names or namespace shortcuts used by the project.
3. Check whether the order of included shared files changed.
4. Verify whether shared spec file names changed or split into new files.
5. After config matches, scan project model files for references to shared element kinds, tags, and relationship kinds.

The highest-risk drift points are:
- `spec-global` changes that rename tags, colors, or relationship kinds
- context/container/component/deployment spec changes that rename element kinds
- config drift that points at the wrong shared files or wrong relative paths

Practical re-sync order:
1. config includes and aliases
2. shared global definitions
3. shared context/container/component/deployment definitions
4. project model files that reference them
5. project views and filters

If includes and aliases are wrong, everything downstream lies with confidence. Classic config behavior.