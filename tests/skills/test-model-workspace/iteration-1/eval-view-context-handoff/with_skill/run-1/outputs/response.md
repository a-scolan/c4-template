Pour `c2_webapp_details`, valide trois choses :
- Contexte parent : la vue doit rester lisible dans le cadre du système parent, pas comme un fragment isolé.
- Include patterns : évite les wildcards trop larges ; vérifie exactement ce qui entre dans la vue.
- Rendu réel : prévisualise la vue et contrôle aussi le panneau Problems.

Pour les règles détaillées parent + focus + neighbors, le bon handoff est `design-view`.
