Use three separate steps, each with a clear responsibility.

1. **Use `design-view` for the companion structural view only.**
   Create a C2 or C3 view that shows the upload area in context: parent boundary, focused elements, and neighbors.

   ```likec4
   views 'C3' {
     view c3_uploadService {
       title 'Upload Service'

       include mySystem.uploadService
       include mySystem.uploadService.*
       include -> mySystem.uploadService
       include mySystem.uploadService ->
     }
   }
   ```

2. **Use `create-sequence-view` for the step-by-step upload journey.**
   Temporal behavior belongs in `views 'Use Cases'`, not in a structural folder.

   ```likec4
   views 'Use Cases' {
     dynamic view uploadFlow {
       title 'Upload Journey'

       user -> mySystem.webapp 'Select file'
       mySystem.webapp -> mySystem.api 'POST /upload'
       mySystem.api -> mySystem.uploadService 'Validate and queue'
       mySystem.uploadService -> mySystem.storage 'Store file'
     }
   }
   ```

3. **Use `customize-view` for colors and visual emphasis.**
   After the structural and dynamic views exist, hand styling off to `customize-view` to highlight critical elements. `design-view` should frame the structure, not own the visual treatment.

That split keeps structure, temporal flow, and styling cleanly separated.
