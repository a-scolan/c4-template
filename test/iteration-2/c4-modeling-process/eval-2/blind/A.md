That is **not** the right use of a C1 view.

A **C1 context diagram should stay static**:
- who the users are,
- what the system boundary is,
- which external systems interact with it,
- and the main static relationships.

A user journey with **time-ordered arrows** between the user, web app, and API belongs in a **dynamic / use-case view**, not in C1.

Why:
- **C1** answers **“what surrounds the system?”**
- **Dynamic views** answer **“how does a scenario unfold over time?”**

So keep C1 clean and static, then create a separate dynamic scenario view for the nominal interaction sequence.