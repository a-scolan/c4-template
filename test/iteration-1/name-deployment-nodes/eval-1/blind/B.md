Not for the full modeling scope.

This guidance is mainly for naming deployment environments, zones, and VMs. If you only need naming, keep patterns like:

- VMs: `{Env}{Service}Vm`
- Tier names: `AppTier`, `ProcTier`, `DataTier`
- Functional zones: `SecZone`, `InfraZone`

For the full Environment → Zone → VM → Node_App hierarchy, Markdown descriptions with IP/CPU/RAM, and `instanceOf` links, use a separate deployment-modeling workflow rather than trying to solve all of that in the naming step.