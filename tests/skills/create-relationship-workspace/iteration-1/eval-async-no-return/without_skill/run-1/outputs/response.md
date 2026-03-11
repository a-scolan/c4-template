Tu peux faire :

```likec4
uploadService -[calls]-> jobQueue 'Envoie le job'
worker -[calls]-> uploadService 'Ack'
worker -[calls]-> database 'Sauve le statut'
```
