Prends le pattern queue + worker :

```likec4
jobQueue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
}

vault.api -[async]-> jobQueue 'Publishes jobs'
workerService -[async]-> jobQueue 'Consumes jobs'
```

N’ajoute pas de retour synchrone `workerService -> vault.api` : ce flux async est à sens unique ; le résultat passe par événement, stockage ou notification séparée.
