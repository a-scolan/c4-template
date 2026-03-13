The smallest safe JSON edit is to change only these sections and leave `$schema`, `name`, and `title` untouched:

{"include":{"paths":["../shared","../platform-shared"]},"imageAliases":{"@":"../shared/images/","@platform":"../platform-shared/images/"}}

This appends `../platform-shared` after `../shared` instead of replacing the array, keeps the shared `@` alias working exactly as before, and avoids collisions by giving the platform images their own alias key rather than overloading `@`. That keeps the scope limited to config editing, with all paths still relative to the project folder.
