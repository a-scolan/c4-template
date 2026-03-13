For a C2 detail view, the parent system must stay explicit. The user, web application, and API can be in the view, but the containing system boundary should still be visible so the view keeps correct parent context.

To validate it:
- Check the include rules first: prefer explicit elements or a scoped pattern such as `mySystem.*`; avoid broad includes like `include **` that can silently pull in unrelated containers.
- Preview the actual rendered view with `open-view`: confirm the parent system is present, the user is shown as external context, and only the intended containers and close neighbors appear.
- Check for hidden scope problems: if the view renders extra siblings or unexpected systems, the include is too broad even if the file still parses.
- Check the Problems panel for unresolved references or include/exclude interactions.

For deeper rules about what a C2 should contain and how to shape the view itself, hand off to `design-view`; this skill's job is to validate that the current view keeps proper context and safe include boundaries.
