## Recommended LikeC4 modeling order (top-down)

1. **Start with workspace context (Stage 0)**  
   First align on project structure, valid kinds, relationship taxonomy, and existing view organization.

2. **Model C1 (System Context)**  
   Define the system boundary, actors, and external systems/dependencies.

3. **Model C2 (Containers)**  
   Split the system into runtime/deployable building blocks and connect them with meaningful relationships.

4. **Add C3 selectively (Components)**  
   Only for containers that are complex, risky, or architecturally central.

5. **Add Dynamic views when sequence matters**  
   Put user flows/use cases in `views 'Use Cases'`.

6. **Add Deployment views when topology matters**  
   Model environments/zones/VMs/instances only after structure is stable.

7. **Validate model integrity**  
   Run model checks before finishing.

## What is optional

- **C3 views are optional** (create only where extra internal detail adds value).  
- **Dynamic views are optional** (only if temporal behavior needs explanation).  
- **Deployment views are optional** (only if runtime topology/infrastructure matters).

In short: stabilize **C1 → C2** first, then add only the extra depth that is justified.