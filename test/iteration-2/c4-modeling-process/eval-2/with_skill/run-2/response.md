Not quite—**C1 is not the right place for temporal flow**.

- **C1 (System Context)** should stay static: boundary, actors, external systems, key dependencies.
- A user journey with ordered steps belongs in a **dynamic view** under `views 'Use Cases'`.

Why: C1 answers *who/what is in scope*; dynamic views answer *what happens over time, in what order*.