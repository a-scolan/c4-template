Je réutiliserais un kind déjà présent du shared spec : `Container_Api`.

```likec4
model {
  mySystem = System_Existing 'My System' {
    ingestionApi = Container_Api 'File Ingestion API' {
      technology 'Node.js, Express'
      description 'Expose l’ingestion de fichiers et déclenche les traitements associés'
    }
  }
}
```

Ici je reste volontairement sur **la déclaration d’élément** : pas de flèches, pas de vue C2, juste le bon kind, la bonne hiérarchie et les champs utiles.