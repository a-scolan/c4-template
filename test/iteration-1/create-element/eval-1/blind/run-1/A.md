No. In this workspace, new kinds are a last resort, so `Container_UploadOrchestrator` is not a good idea for one service. Reuse an existing shared kind first—most likely `Container_Api` for an upload/orchestration API.

Before adding any new kind, check in this order: 1) the active project summary or model when available, 2) `projects/shared/SPEC_CHEATSHEET.md`, 3) the shared spec files such as `projects/shared/spec-context.c4` and `projects/shared/spec-containers.c4`, and 4) existing project model files for naming and placement.

Only introduce a new kind if none of the shared kinds fits, and ask before adding it. A better start here is:

ingestionApi = Container_Api 'Upload Orchestrator API' {
  technology 'Node.js, Fastify'
  description 'Coordinates upload requests and starts the ingestion workflow.'
}
