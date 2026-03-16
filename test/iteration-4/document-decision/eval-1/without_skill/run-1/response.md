Usually no. A GitHub Actions workflow change is not automatically an ADR.
Write an ADR only if the workflow change captures a long-lived architectural or governance decision, such as a repository-wide release strategy, deployment topology, security/compliance gate, artifact promotion model, or platform standard that other systems must follow.
If it is just CI mechanics—job steps, caching, trigger tweaks, naming, or test sequencing—document it in the pull request, workflow comments, or engineering docs instead of an ADR.
