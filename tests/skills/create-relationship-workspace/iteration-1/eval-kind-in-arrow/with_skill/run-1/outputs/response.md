Utilise une relation typée avec le type de relation dans la flèche :

```likec4
mySystem.webapp -[calls]-> mySystem.api 'Appelle l’API' {
  technology 'HTTPS'
}
```

Le type de relation va dans la flèche, pas dans le bloc de propriétés.
Garde le label inline. Et jamais une forme invalide comme `-> { calls ... }`.
