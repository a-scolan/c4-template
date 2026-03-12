Le kind exact pour ton backend est `Container_Api` ; pas `Container_API`, et pas le générique `Container` si tu veux rester précis.
Pour les relations modèle valides, reste sur `calls`, `reads`, `writes`, `async` et `uses`.
Vérifie dans le dépôt actif avec `read-project-summary` ou les specs partagées.
Et n'invente pas de relation non déclarée : pas `query`, pas `invokes`.
