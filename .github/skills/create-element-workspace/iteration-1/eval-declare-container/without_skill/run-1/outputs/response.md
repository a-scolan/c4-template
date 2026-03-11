Tu peux ajouter quelque chose comme ça :

```likec4
model {
  mySystem = System_Existing 'My System' {
    fileIngestion = Container 'File Ingestion API' {
      technology 'Node.js'
    }
  }
}
```

Ensuite tu pourras le relier à la base et faire une vue C2.