1) Clarify scope and outcomes (business goals, primary users, success criteria).  
2) Model C1 first: identify actors and external systems; define system boundary.  
3) Model C2 next: split the system into containers (web app, API, DB, queues, etc.) and define key relationships/technologies.  
4) Validate C2 against real flows and ownership (who uses what, data direction, trust boundaries).  
5) Add C3 only where needed: decompose only complex/critical containers.  
6) Add deployment views for runtime/infrastructure mapping (environments, nodes, instances, network zones).  
7) Add dynamic views for scenarios (nominal flow, error flow, async timing).  
8) Refine incrementally: tags, metadata, descriptions, view filters, and consistency checks.

Optional items:
- C3 views for simple containers with low internal complexity.  
- Dynamic views if interaction timing is not important for the current audience.  
- Detailed deployment modeling early on (can be postponed until infrastructure decisions stabilize).  
- Advanced styling/manual layout while the model is still changing quickly.