This skill should **not** detail everything itself.

`c4-modeling-process` is the **orchestration and sequencing** layer. Since you already have **C2**, use it to decide what comes next, then hand off the detailed work:

- For **production infrastructure**, use **`model-deployment-infrastructure`**.
- For the **nominal user scenario**, use **`create-sequence-view`**.

That order matters:

1. Keep the **C1/C2 structural core** as the foundation.
2. Add **Deployment** only if runtime topology really matters.
3. Add a **Dynamic** view only if the workflow needs time-ordered behavior.

So Deployment and Dynamic are targeted, optional follow-ups after the structural model, not work that this skill should fully implement by itself.