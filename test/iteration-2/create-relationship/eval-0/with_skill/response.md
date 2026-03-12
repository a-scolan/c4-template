Use a typed relationship in the system model, with the relationship kind in the arrow:

```likec4
webApp -[calls]-> api 'Sends request' {
  technology 'HTTPS'
}
```

The relationship type belongs in the arrow as `-[calls]->`, not in the properties block. Keep the action label inline (`'Sends request'`), and keep protocol or medium details such as `technology 'HTTPS'` inside the block.

So `webApp -> api { calls 'Sends request' }` is the wrong pattern; `webApp -[calls]-> api ...` is the correct one.
