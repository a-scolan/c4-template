Sous `mySystem`, ajoute directement la déclaration d'élément suivante et reste sur l'élément uniquement :

```likec4
mySystem = System_Existing 'My System' {
  fileIngestionApi = Container_API 'File Ingestion API' {
    technology 'Node.js, Express'
    description 'Ingests uploaded files and validates input before processing.'
  }
}
```

Je me limite à la déclaration de l'élément uniquement, sans relations ni vues.
