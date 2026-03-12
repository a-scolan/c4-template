That is **not** the correct place for it.

A **C1** view should stay **static**: it shows the **system boundary**, the surrounding actors, and the external dependencies. It is about **context**, not step-by-step behavior over time.

If you want to show a user journey with temporal arrows between the user, the webapp, and the API, put it in a **dynamic view** under **`views 'Use Cases'`** instead.

Why:

- **C1 = boundary and environment**
- **Dynamic / Use Cases = temporal flow and ordered interactions**

So keep C1 static, and move the time-ordered journey to a dynamic view where sequence actually belongs.