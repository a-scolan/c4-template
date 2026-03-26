For a **very simple API container**, a C3 view is usually **not required**.

Use this decision rule:
- Create C3 only if the container is **complex**, **risky**, or **architecturally central**.
- Skip C3 if C2 already explains it clearly and its internals are straightforward.

So the default is: **stop at C2 unless extra internal detail improves understanding or decisions**.