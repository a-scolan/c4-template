Relationship choice: `calls`.
Short rule: In this repository, the relationship kind belongs in the arrow (`-[calls]->`), the action label stays inline after the target, and protocol/medium goes in the properties block.
Minimal example:
webApp -[calls]-> api 'Sends request' {
  technology 'HTTPS'
}
Counter-example / anti-pattern:
webApp -> api {
  calls 'Sends request'
  technology 'HTTPS'
}
That form is wrong because the type must not live inside the block.
