Dans `mySystem`, tu peux ajouter un backend minimal comme ceci :

```likec4
mySystem = System_Existing 'My System' {
  fileIngestionApi = Container_Api 'File Ingestion API' {
    technology 'Node.js, Express'
    description 'Receives files and performs initial ingestion.'
  }
}
```

Je reste sur la déclaration de l'élément uniquement.
