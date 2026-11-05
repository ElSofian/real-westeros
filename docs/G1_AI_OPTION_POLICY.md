# G1 — Préférence initiale de désobéissance pour l’IA

**Expérimental, vérifié statiquement ; aucun test CK3. W2/AI4 restent ouverts, +0.**

L’adaptateur privé 0.0.4 ajoute `starts_enabled` à son option de défi. Ce champ
existe dans les sources AGOT 0.5.2.1 fournies ; le reçu
G1_AI_OPTION_SOURCE_RECEIPT.json ne publie que chemin, empreinte et repères.
L’observation de ce champ dans des interactions de diarque ne démontre ni son
ordre d’évaluation dans la déclaration de guerre ni son usage par le planificateur IA.

Le trigger original `rw_uw_ai_default_defiance_trigger` initialise le choix si :

- le contexte partagé de pairs féodaux/interdit/helper natif est encore valide ;
- aucun hameçon n’est déjà sélectionné dans cette fenêtre ;
- l’acteur est IA, en paix, avec au moins 150 pièces d’or disponibles ;
- il n’a pas d’obligation personnelle de service/faveur actuellement marquée ;
- son opinion personnelle de son suzerain actuel est au plus −25.

Les 150 pièces constituent une préférence de réserve, pas un coût ou une dispense
du coût natif. Les trois facteurs sont moyens, engagements/charge militaire et
relation politique connue. Le seuil est un choix de conception prudent, à ajuster
après observation. Aucun tirage aléatoire réévalué, parcours global, événement
périodique, état persistant ou lecture du dossier privé d’autrui.

Le joueur commence sans défi présélectionné. Le test `is_ai` intervient seulement
dans cette préférence : visibilité, validité, autorisation du défi et conséquences
restent partagées. Un joueur peut choisir le défi avec moins d’or ou une autre
opinion ; l’IA n’obtient aucun droit supplémentaire. Les contrôles natifs du CB,
des coûts et des autres restrictions restent responsables de l’exécution.
Un hameçon acquis n’est ni consommé ni sélectionné par cette politique. Si le moteur
sélectionne ensuite hameçon et défi ensemble, les gardes existantes refusent le défi.

**Limite encore ouverte :** l’IA peut filtrer la guerre interdite avant de construire
les options de l’interaction. `starts_enabled` ne résout pas cette découverte.
Aucun `start_war`, appel forcé, faux CB ou champ IA inventé ne la contourne.
La préférence initiale n’est pas une preuve de décision, de guerre lancée, de coût
payé ou de réaction royale. Sans adaptateur privé, aucun chemin de guerre ne change.

## Vérifications disponibles

Tests de source : préférence séparée des trois gardes partagées, absence d’effets et
de hasard, hameçon incompatible, facteurs attachés à l’acteur, une seule insertion
`starts_enabled`, conservation exacte des octets natifs par inversion des trois
fragments d’origine. Le reçu privé nomme explicitement la découverte/envoi non vérifiés.
La génération privée teste toujours les quatre entrées épinglées ; le fichier diarque
sert de preuve de syntaxe, jamais d’entrée recopiée ou de dépendance d’installation.

## Campagne finale uniquement — tous NON EXÉCUTÉS

| Cas | Observation requise |
|---|---|
| AIDEFY-01 | Joueur : option décochée initialement, sélection/refus/fermeture sans effet anticipé. |
| AIDEFY-02 | IA hostile, en paix, solvable, sans engagement : observer la découverte native, puis la sélection, puis une vraie guerre de revendication et ses coûts. Distinguer chaque étape ; absence de découverte laisse W2/AI4 ouverts. |
| AIDEFY-03 | IA amicale, réserve insuffisante, guerre existante ou obligation : préférence fausse ; aucune nouvelle restriction mécanique du joueur. |
| AIDEFY-04 | Hameçon sélectionné avant/après construction, exemption contractuelle ou loi modifiée : aucun cumul ou permission persistante. |
| AIDEFY-05 | Changement de cible/suzerain, annulation et rechargement : contexte réévalué, aucun état global ; coûts et cycle natifs uniques. |
| AIDEFY-06 | Deux acteurs IA : initiative native puis réaction royale, négociation/refus natifs ; performance et Mega Wars selon les cas existants. |

Ne pas demander un test intermédiaire. G1CHOICE, DECLAW, G1ROYAL et NATIVEWAR restent
nécessaires ; ce changement ne les remplace pas et ne valide aucun point moteur.
