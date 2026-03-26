Use a **layered description**: concise core + referenced details.

### Core block (target: 8–12 lines)
- Mission of `ProdApiVm`
- `eth0` role (client/data plane)
- `eth1` role (monitoring/management plane)
- Baseline capacity (CPU/RAM/GPU in one compact line)
- Top 3 dependencies
- Top 3 SLO/SLA-relevant signals
- Recovery target (RTO/RPO or restore expectation)
- Owner + on-call

### Keep it rich, not encyclopedic
- Prioritize **decision-critical** facts (what changes ops behavior).
- Use numeric thresholds only for actionable alerts.
- Move long enumerations (all metrics, all ports, full hardware inventory) to runbooks.
- Add links/references for depth instead of inlining everything.
- Apply a “3-item rule”: for each section, keep max 3 high-value bullets.

Good heuristic: if a detail does not change triage, escalation, or recovery, it belongs outside the core description.