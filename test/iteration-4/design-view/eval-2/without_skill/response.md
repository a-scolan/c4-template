I would not put the whole upload journey into one crowded diagram. The clean LikeC4 approach is a small view set built from one stable model.

Recommended approach:
1. Keep one C2 overview for the upload platform structure.
2. Add a short series of focused journey views, one per step: submit, validate, persist, process, notify.
3. Model the flow with the shared relationship types: `calls`, `async`, `writes`, and `reads`.
4. Highlight critical elements with existing semantic tags instead of inventing new ad-hoc colors: use `#Security` for sensitive checks, `#Async` or `#Queue` for handoffs, and `#Persistence` or `#Data` for storage-heavy steps.
5. Keep the layout consistent across the step views so the reader can see what changes from one step to the next.

A practical naming pattern is `upload_01_submit`, `upload_02_validate`, `upload_03_store`, `upload_04_process`, `upload_05_notify`. That keeps the narrative readable, and the colors stay aligned with the workspace conventions already defined in the shared specs.
