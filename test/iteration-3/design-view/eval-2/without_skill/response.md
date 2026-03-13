For an upload journey, I would use a two-layer approach rather than forcing step order into the main container view.

1. Keep the static structure in `views 'C2'`.
2. Add a dedicated `views 'Use Cases'` section for the upload flow and make it the drill-down target from the relevant container (`webapp` or `api`).
3. Show only the critical path elements in that journey view: user -> webapp -> api -> queue/scanner/storage -> email/notification.
4. Highlight important elements with existing workspace semantics instead of one-off colors: `#Security` for auth or scanning controls, `#Queue` for async steps, `#External` for third-party systems, and storage-shaped containers for persistence.
5. If you need strict step-by-step narration, use a sequence or dynamic-style use-case view; if you just need a guided drill-down, a focused C2/C3 view with numbered relationship labels is enough.

Short version: C2 for structure, a dedicated Use Cases/sequence view for the upload journey, and tags/colors to emphasize the critical parts.
