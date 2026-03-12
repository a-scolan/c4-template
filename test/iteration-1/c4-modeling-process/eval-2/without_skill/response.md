That is **not** the right place for it.

A **C1 view must stay static**. Its job is to show the system boundary, the main actors, and the neighboring systems. It is about context, not step-by-step behavior.

If you want to show a user journey with temporal arrows between the user, the web app, and the API, put that in a **dynamic / use-case view** instead. That is the right place to show sequence, order, and interaction flow.

A good split is:
- **C1**: user, web app, API, and their static relationships
- **Dynamic / use-case view**: the ordered journey between them

Why: C1 answers **“what is in scope and how it connects?”** while a dynamic view answers **“what happens over time?”**