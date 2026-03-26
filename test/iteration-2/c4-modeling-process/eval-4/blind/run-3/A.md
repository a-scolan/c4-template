This skill should **not** detail everything itself.

It should orchestrate the sequence, then hand off:

1. You already have C2 (good baseline).
2. For production infrastructure, hand off to **`model-deployment-infrastructure`**.
3. For a nominal user scenario (time-ordered), hand off to **`create-sequence-view`**.
4. Optionally use **`design-view`** for static view adjustments and **`test-model`** for validation.

So: this skill defines *what comes next*; specialized skills perform the detailed edits.