Because neither element exists yet, describe them only after you model them.

1. Create the processing service first as a system-model element.
2. Create the production VM first as a deployment node in the deployment model.
3. Then choose the description format based on where the thing lives:
   - System model element: keep the description short in the element block. Use `metadata {}` only for machine-readable facts that automation or filtering needs.
   - Deployment VM: use a richer Markdown table, because operators need scannable operational facts.

A practical rule:
- If the information explains what the software/service is, keep it in the system model description.
- If the information explains how a VM is operated, connected, sized, or supported, put it in the VM's Markdown table.

So the order is: create first, then describe; concise element description for the service, ops-oriented table for the VM.
