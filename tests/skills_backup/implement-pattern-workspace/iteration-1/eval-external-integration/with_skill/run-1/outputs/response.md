Utilise le pattern d’intégration externe :

```likec4
paymentProvider = System_External 'Payment Provider' {
  technology 'REST API'
  #External
}

vault.api -[calls]-> paymentProvider 'Process payment'
```

Garde un libellé d’action précis (`Process payment`, `Create charge`) plutôt qu’un label flou comme `Uses external API`.
