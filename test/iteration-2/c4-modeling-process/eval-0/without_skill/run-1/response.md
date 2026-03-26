Start in this order:

1. **Frame the problem (required)**
   - Define product scope, business goals, key actors, and boundaries.
2. **Model C1 first (required)**
   - Add people/systems and the main external interactions.
3. **Model C2 next (required)**
   - Break the system into containers and define responsibilities + interfaces.
4. **Refine relationships and naming (required)**
   - Use clear, consistent relation labels and technology hints where useful.
5. **Create core views for C1/C2 (required)**
   - Ensure each view answers a concrete stakeholder question.
6. **Validate and iterate (required)**
   - Check for missing actors, unclear boundaries, and overloaded containers.

What is optional (depends on complexity/risk):

- **C3 views** for specific containers (optional unless internals are non-trivial).
- **Deployment modeling** (optional until runtime/infrastructure concerns matter).
- **Dynamic/sequence views** (optional unless behavior over time must be explained).
- **Advanced styling/tags/customization** (optional; useful for governance, scale, and readability).

Short rule: **C1 -> C2 is mandatory baseline; C3/deployment/dynamic are added only when they answer real decisions.**1. Define scope and outcomes (required)
   - Name the SaaS product, target users, core business capabilities, and boundaries (what is in vs out).
   - Capture key non-functional constraints early (security, compliance, availability, latency, data residency).

2. Model C1 first: actors and systems (required)
   - Create people/staff/admin actors and internal/external systems.
   - Add high-level relationships with purpose and technology where meaningful.
   - Outcome: a context map that answers “who interacts with the product and with which surrounding systems?”.

3. Decompose into C2 containers (required)
   - Split the SaaS into major runtime/building blocks (web app, API, queue, database, storage, IAM, etc.).
   - Model key data and control flows (sync vs async, reads vs writes).
   - Outcome: a container architecture showing responsibilities and integration paths.

4. Drill down to C3 components only where complexity justifies it (optional, but recommended for critical containers)
   - For complex/high-risk containers, model internal components and their interactions.
   - Skip simple containers to avoid over-modeling.

5. Add deployment model after logical model is stable (required for production planning)
   - Define environments and infrastructure nodes/zones (internet, DMZ/app/data tiers, VMs/clusters, shared infra).
   - Link deployed instances back to logical elements (`instanceOf`) and add infra-specific relationships only when needed.

6. Define views for each stakeholder question (required)
   - Create focused context/container/component/deployment views.
   - Use includes/filters/tags so each view answers one clear question.
   - Keep labels and relationship text concise and action-oriented.

7. Standardize naming, tags, and relationship vocabulary (required)
   - Apply consistent PascalCase naming and a stable tag taxonomy.
   - Reuse a small set of relationship kinds (`uses`, `calls`, `async`, `reads`, `writes`) to keep diagrams predictable.

8. Validate and iterate (required)
   - Check completeness: every critical capability has an owner container, data path, and deployment target.
   - Check quality: no ambiguous boundaries, no orphan elements, no duplicated responsibilities.
   - Iterate with architecture and product stakeholders.

Optional additions (use when useful)
- Decision records (ADR) for major trade-offs.
- Advanced style customization (colors/shapes/themes).
- Scenario/dynamic views for key user journeys.
- Extra environment slices (dev/staging/prod, DR/backup, CI/CD).
- Traceability metadata (owner, domain, criticality, compliance tags).