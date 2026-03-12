This skill should **not** try to detail everything itself.

`c4-modeling-process` is the **orchestration and sequencing** skill: it decides what level comes next and when optional work is justified. The detailed editing should be delegated to the more specific skills.

Because you already have **C2**, you can now add targeted follow-up views:

- For **production infrastructure**, hand off to **`model-deployment-infrastructure`**.
- For the **nominal user scenario**, hand off to **`create-sequence-view`**.

Both of those come **after** the core structural model is stable, and both are **optional / targeted** additions:

- **Dynamic** views are for time-ordered behavior.
- **Deployment** views are for runtime topology.

So use this skill to decide the order, then let the specialized skills do the detailed work. One skill to rule the sequence, not to micromanage every diagram.