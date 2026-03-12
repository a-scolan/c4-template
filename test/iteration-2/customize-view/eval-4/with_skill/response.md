```likec4
view existing_c2_view {
  autoLayout TopBottom

  include user with {
    rank source
  }
}
```

Start with `autoLayout` and a single obvious anchor for the user.
I would avoid stacking extra `rank same`, `rank source`, or `rank sink` directives unless the preview is still genuinely unclear.