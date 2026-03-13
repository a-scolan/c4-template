Validation plan:
1. Check the worker kind against `projects/shared/spec-containers.c4`. If it is a background processor, `Container_ProcessingServer` is usually a better fit than `Container_Webapp`; if it is a broker, use `Container_Queue`.
2. Check FQNs in `projects/template/system-model.c4`: the worker should be nested under `mySystem`, so its canonical reference is `mySystem.worker`. In `projects/template/system-views.c4`, use that FQN consistently in `include` statements and any `navigateTo` wiring.
3. Check relationships against `projects/shared/spec-global.c4`: the shared business relationships here are `uses`, `calls`, `async`, `reads`, and `writes`. Make sure the direction and the `technology` value match the real interaction.
4. Check view scope in `projects/template/system-views.c4`: keep the new dedicated view under `views 'C2'` and prefer explicit includes for a focused detail view instead of `include mySystem.*`.
5. Check rendering: the view should show only the intended actor/containers, with no unresolved references, no unknown kinds, and no stray elements such as `database` or `emailService` unless you intentionally included them.
6. If you added drill-down, verify that the source container's `navigateTo` points to the new view name exactly.
If all six pass, the change is very likely model-correct rather than only parser-acceptable.
