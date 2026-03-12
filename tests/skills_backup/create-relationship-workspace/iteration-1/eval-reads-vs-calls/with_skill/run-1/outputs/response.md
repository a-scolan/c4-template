Règle : `-[reads]->` pour les lectures de cache/base, `-[writes]->` pour la persistance, et `-[calls]->` seulement pour du service-à-service.

Exemple court :

```likec4
retrievalService -[reads]-> cache 'Check cache'
retrievalService -[reads]-> database 'Fetch metadata'
retrievalService -[writes]-> database 'Store access log'
```
