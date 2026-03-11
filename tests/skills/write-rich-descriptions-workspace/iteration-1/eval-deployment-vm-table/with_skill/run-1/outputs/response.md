Pour `ProdApiVm`, fais un tableau Markdown, pas un bloc metadata en premier.
Ordre conseillé :
1. Interfaces réseau d’abord (`eth0`, puis `eth1` si besoin)
2. OS
3. CPU / RAM / Disk
4. Port / runtime / health check / RTO si utile

Ne duplique pas le hostname déjà dans le titre. Le gateway vit plutôt au niveau de la zone, sauf cas multi-homed. La metadata reste optionnelle : ne la répète que si une automatisation en a besoin.
