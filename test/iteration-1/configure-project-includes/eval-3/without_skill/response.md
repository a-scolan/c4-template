It is enough for the `likec4.config.json` part of the job, especially:

- adding or preserving `include.paths`
- keeping `imageAliases` stable
- referencing shared specs with relative paths such as `../shared`

It is not enough by itself for the full workspace-level design of a second project.

For that larger task, combine it with a separate project-organization step that decides:

- where the second project lives
- what is shared vs project-specific
- how shared sources are named and reused
- how multiple projects stay consistent over time

So use this for configuration details inside `likec4.config.json`, but use a broader workspace-structure approach for the overall multi-project layout.