No, that is not the right place for it.

A **C1** view must stay **static**. Its job is to show the **system boundary**, the main actors, and the external systems around it. It is about **context**, not step-by-step behavior.

If you want to show a user journey with temporal arrows between the user, the webapp, and the API, that belongs in **`views 'Use Cases'`** as a **dynamic view**.

Why:

- **C1** answers: *who interacts with the system and what is around it?*
- **Dynamic views** answer: *what happens first, next, and after that?*

So keep C1 static, and move the temporal flow to a dynamic use-case view.