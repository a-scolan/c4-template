Keep the same minimal shape as the workspace baseline in `projects/template/likec4.config.json`: `$schema`, `name`, `title`, `include.paths`, and `imageAliases`. From `projects/payments`, shared specs should be referenced with `../shared`, and shared icons should keep `"@": "../shared/images/"`. Use paths relative to the project folder, not workspace-root or absolute paths.

Safe minimal file: {"$schema":"https://likec4.dev/schemas/config.json","name":"payments","title":"Payments Architecture","include":{"paths":["../shared"]},"imageAliases":{"@":"../shared/images/"}}
