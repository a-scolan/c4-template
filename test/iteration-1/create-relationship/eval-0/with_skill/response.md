Relationship choice: `calls`.
Rule: In the system model, the relationship kind belongs in the arrow itself (`-[calls]->`). Protocol or medium details belong in the block as `technology '...'`, not as the relationship kind.
Example:
webApp -[calls]-> api 'Sends request' {
  technology 'HTTPS'
}
Anti-pattern:
webApp -> api {
  calls 'Sends request'
  technology 'HTTPS'
}
