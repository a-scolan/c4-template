Not in C1.

In LikeC4/C4, **C1 is a static context diagram** (who/what interacts with the system), not a temporal behavior diagram.

Your user journey with time-ordered arrows should go to a **dynamic (sequence-like) view**, typically anchored at:

- **C2 level** if the journey is between containers (user -> webapp -> API), or
- **C3 level** if you must show component-level behavior inside a container.

Why: this separation keeps C1 readable for scope/boundary understanding, while dynamic views capture ordering, causality, and runtime flow.