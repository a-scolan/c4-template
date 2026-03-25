`styles { theme dark }` fails because `styles` is not a valid top-level statement for selecting a theme. In LikeC4, `theme` belongs in a `global` block, while `styles` is used for defining style rules, not for activating a built-in theme. So the parser rejects this file at the top level.

Minimal valid file with the same intent:

global {
  theme dark
}

This keeps the intent ('use the dark theme') and uses an allowed top-level statement only.
