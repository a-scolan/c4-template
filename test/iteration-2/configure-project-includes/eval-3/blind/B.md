If the immediate job is only `likec4.config.json`—shared includes and image aliases—that narrow configuration work is enough.

If you are adding a true second LikeC4 project to the workspace, that is broader than a config tweak. You will usually also need a dedicated multi-project organization pass for:

- folder layout
- per-project model/view files
- shared vs project-local assets
- naming boundaries
- documentation boundaries

So the short answer is:

- config-only change: enough
- full second-project setup: not enough by itself

In both cases, keep shared references project-relative, for example `../shared` and `../shared/images/`, rather than using absolute paths.