No—do not keep normal browser-to-application traffic as a deployment relationship.

Put that relationship in the system model between the logical elements, and use the technology value there:

```likec4
user -[calls]-> mySystem.webapp 'Interacts with' {
  technology 'Manual'
}

mySystem.webapp -[calls]-> mySystem.api 'Makes API requests' {
  technology 'HTTPS'
}
```

Use this rule:
- `technology 'Manual'` for human interaction
- `technology 'HTTPS'` for normal browser or service traffic
- `technology 'HTTP/8080'` only when the port is relevant and non-default

Deployment instances should inherit those logical relationships via `instanceOf`. Keep deployment relationships for rare infrastructure-specific exceptions only, such as an explicit node-level hop, port-specific routing, or another environment-only connection that does not exist in the logical system model.
