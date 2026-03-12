When you switch projects in a multi-project LikeC4 workspace, treat the old context as invalid until you re-establish it.

## Revalidation sequence before editing a C3 view

1. **Re-identify the active project.**
   - Check which project folder you are editing.
   - In this repository, the visible project ids are `template-project` and `spec-showcase`.

2. **Re-run `list-projects`.**
   - This confirms the available project ids instead of assuming the current one.

3. **Re-run `read-project-summary` for the explicit project id.**
   - Use the project you just switched to, not a remembered default.
   - This refreshes the loaded elements, views, kinds, tags, and current model shape.

4. **Re-read the project `likec4.config.json`.**
   - Confirm that the active project still includes `../shared` and that you are using the right local config.
   - This avoids carrying includes or aliases from the previous project.

5. **Re-read shared specs before any C3 edit.**
   - `spec-context.c4`
   - `spec-containers.c4`
   - `spec-components.c4`
   - `spec-global.c4`
   - `spec-deployment.c4` only if the target edit crosses into deployment concerns

6. **Confirm the C3 parent container exists in the new project.**
   - Use `read-element` or `search-element` on the intended parent container.
   - Make sure the parent is the right C2 container in the switched project, not just a same-named element from the old one.

7. **Read the existing model/view files for the target project.**
   - Confirm current C1/C2 structure, existing view folders, and whether a `C3` folder already exists.

8. **Only then edit the C3 view.**
   - Add internal `Component` detail selectively.
   - Keep the C3 scope anchored to the confirmed parent container.

## Risks this avoids

- **Stale context:** editing with the previous project's loaded elements or views still in mind.
- **Invalid kind or relationship usage:** using taxonomy that is not actually loaded for the current project.
- **Wrong C3 parent:** attaching components to the wrong container, or to a container that belongs to another project.
- **Wrong file target:** updating a view that looks familiar but is not the active project's source file.

## Rule of thumb

After a project switch, rerun `list-projects` + `read-project-summary`, reread shared specs, and re-confirm the parent container before touching any C3 view.