Pas entièrement.

Ce skill sert surtout à **verrouiller les noms** : `Prod`, `ProdUploadVm`, `ProdWorkerVm`, `AppTier`, `ProcTier`, `DataTier`, `SecZone`.

Pour la **modélisation complète** — hiérarchie **Environment → Zone → VM → Node_App**, tables Markdown avec IP/CPU/RAM et liens `instanceOf` vers les containers — passe à **`model-deployment-infrastructure`**.

Donc :
- **ici** tu fixes les patterns `{Env}{Service}Vm`, `{Tier}Tier` et `{Function}Zone` ;
- **là-bas** tu détailles la structure, les descriptions et les `instanceOf`.
