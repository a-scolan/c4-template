Pour un `ProdApiVm`, pars sur un tableau Markdown dans la description.
Ordre utile :
1. Interfaces réseau d’abord (`eth0`, puis `eth1` si besoin).
2. OS.
3. CPU / RAM / Disk.
4. Détails de service utiles aux ops (port, healthcheck, RTO).
À ne pas dupliquer : le gateway standard vit plutôt au niveau de la zone, pas du VM ; et la `metadata` reste optionnelle, seulement si une automatisation doit requêter ces champs.
