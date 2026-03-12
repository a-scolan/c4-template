Create the elements first, then document them.

1. Add the processing service as a system-model element.
2. Add the production VM as a deployment node in the deployment model.
3. Once they exist, choose the description format by model type:
   - System model element: keep the description concise. Use `metadata {}` only for structured facts that automation or filtering will actually query.
   - Deployment VM: use a richer Markdown table, because operators need scannable operational details.

A practical split:
- If the information explains what the software is or why it exists, keep it with the system element.
- If the information explains how the VM is connected, sized, operated, or recovered, put it in the VM table.

So the order is: model first, then describe; concise system description plus optional `metadata {}` when machines need it, and an ops-oriented Markdown table for the VM.
