Verify it with a genericity and confidentiality review before you sync anything upstream:
1. Reusability test: would another derived repository benefit from this change without knowing your local domain?
2. Local-context test: does it mention project names, internal systems, customer details, private architecture, or one-off assumptions from this repo?
3. Scope test: is it truly a workspace-level improvement to `projects/shared`, not a hidden fix for one project?
4. Explanation test: can you describe it as a reusable improvement to shared container modeling guidance rather than a local workaround?
5. Confidentiality audit: remove secrets, internal architecture notes, employee/team names, and other private context.
6. Separation check: keep this file in its own commit and do not mix it with project-local files.

If it passes those checks, branch from `c4-template/main`, bring over only `projects/shared/spec-containers.c4`, review the diff, and open a PR. If any answer points to local context, keep the change in the current repo.
