Modélise le flux de cette façon :

```likec4
uploadService -[async]-> jobQueue 'Queue le job'
jobQueue -[async]-> worker 'Livre le job'
worker -[writes]-> database 'Persiste le statut'
```

Il n'y a pas de relation retour du worker vers le producteur : pas de relation retour.
Garde le pattern asynchrone one-way, sans ACK modélisé comme appel retour.
