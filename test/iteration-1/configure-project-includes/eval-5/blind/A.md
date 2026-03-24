Keep every unrelated field as-is and make the smallest safe edit to the include and alias sections:

`{
  "include": {
    "paths": ["../shared", "../platform-shared"]
  },
  "imageAliases": {
    "@": "../shared/images/",
    "@platform": "../platform-shared/images/"
  }
}`

This appends `../platform-shared` after `../shared`, keeps the existing shared icon alias working, and avoids collisions by giving the platform image source its own alias.
