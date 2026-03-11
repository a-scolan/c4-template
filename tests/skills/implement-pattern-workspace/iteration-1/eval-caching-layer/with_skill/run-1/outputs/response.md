Modélise explicitement le cache comme un composant d’accès, pas comme la nouvelle base :

```likec4
cache = Container_Cache 'Cache' {
  technology 'Redis'
}

vault.api -[reads]-> cache 'Read-through cache'
vault.api -[writes]-> cache 'Cache updates'
vault.api -[reads]-> database 'Fetch on cache miss'
```

Précise que Postgres reste la source de vérité ; Redis accélère les lectures mais ne remplace pas la base.
