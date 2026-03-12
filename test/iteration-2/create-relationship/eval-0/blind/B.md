Use a **typed relationship arrow** in the system model:

```likec4
webApp -[calls]-> api 'Requests API operations' {
  technology 'HTTPS'
}
```

Key rule:
- Put the relationship type in the arrow: `-[calls]->`
- Keep the human-readable label inline: `'Requests API operations'`
- Put the transport/protocol in the properties block: `technology 'HTTPS'`

So the relationship **type belongs in the arrow**, not in the block.

Avoid patterns like:
- `webApp -> api { calls ... }`
- `webApp -> api { technology 'HTTPS' kind 'calls' }`
- `webApp -> api { calls 'Requests API operations' }`

If this is normal application traffic, model it in the **system model**, not in deployment.