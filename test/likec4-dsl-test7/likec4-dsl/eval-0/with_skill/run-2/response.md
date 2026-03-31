`npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template`

- `filteredErrors`: erreurs dans le sous-ensemble filtré par `--file` uniquement.
- `totalErrors`: erreurs sur tout le projet.
- `filteredFiles`: nombre de fichiers source `.c4`/`.likec4` réellement pris en compte par les filtres `--file`.

Interprétation rapide : si `filteredErrors > 0`, ton fichier filtré a échoué ; si `filteredErrors = 0` mais `totalErrors > 0`, ton fichier est propre et c’est le reste du projet qui est cassé.