In an unfamiliar LikeC4 workspace, start by rebuilding context before drawing anything new.

1. **Identify the active project and its shared inputs**
   - Confirm which project you are editing.
   - In this workspace, project configs such as `projects/template/likec4.config.json` and `projects/spec-showcase/likec4.config.json` include `../shared`, so shared specs influence the valid kinds, tags, and conventions.

2. **Re-establish the C1 picture**
   - Understand the system boundary, actors, external systems, and the purpose of the product.
   - If the C1 picture is unclear, fix that understanding first.

3. **Define the purpose of the new C2 view**
   - Decide the audience and question the view must answer.
   - Choose the containers that matter for that specific view instead of trying to show everything.

4. **Map the containers and their relationships**
   - Identify the main applications, stores, queues, and integrations.
   - Keep the relationships static and architectural.

5. **Only then design the C2 view**
   - Include the relevant containers.
   - Organize the layout for readability.
   - Keep it aligned with the C1 story.

6. **Use separate focused follow-up passes if needed**
   - one pass for structure and conventions,
   - one for missing elements,
   - one for missing relationships,
   - one for polishing the view itself.

The key is to move **C1 → C2**, not jump straight into detailed edits before the project structure and shared conventions are clear.