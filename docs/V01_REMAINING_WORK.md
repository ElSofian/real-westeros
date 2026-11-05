# Ce qui reste avant la première version intégrée

Revue du **5 novembre 2026**, après PR #81 (`e0d9121b04e33316a0a3c1c5eb0a248904263109`).
**Développement qualifié : 64/80 ; validation en jeu : 0/20 ; total : 64/100.**
Cette revue ne livre pas de fonctionnalité et ne modifie ni la grille, ni les points,
ni les critères ouverts de [V01_PROGRESS.json](V01_PROGRESS.json).

## Lecture du score

Les 16 points source restants ne représentent pas 16 points de code indépendant
à écrire avant de pouvoir lancer CK3. Certains critères ont du code expérimental,
mais une observation du moteur peut déterminer quel code est réellement nécessaire
pour terminer leur implémentation. Les 20 points moteur couvrent ensuite la campagne
de validation complète ; du code présent n’est jamais une preuve de compatibilité.

Les dernières PR ont écrit la capture du contexte de déclaration, une préférence
initiale IA et la clôture des choix de guerre. Elles apportent de la préparation et
une correction de conservation anti-rejeu, sans achever un nouveau critère entier.
Il reste aussi des fonctionnalités absentes : le développement n’est pas terminé.
Les huit systèmes restent le périmètre ; les trois scénarios sont des exemples.

## Les sept critères source ouverts

| Critère | Écrit dans le dépôt | Ce qui manque réellement | Dépendance / prochaine décision |
|---|---|---|---|
| **W1 — 2 pts** | Capture dans le préfixe natif claim_cb, helper sous alias propres, reçu immuable et liaison au dossier royal. | Établir que la capture permet bien de qualifier la loi au moment de l’acte ; adapter le point d’entrée si son ordre réel ne convient pas. | Observation de l’ordre des callbacks dans DECLAW-01…09. Une nouvelle capture tardive ne résout pas le manque. |
| **W2 — 4 pts** | Option privée de défi dans la fenêtre native, vrai CB conservé, gardes partagées et préférence initiale IA. | Voie intégrée de déclaration interdite joueur/IA avec contexte exact, coûts et annulation préservés. La découverte native de cette guerre par l’IA reste non résolue. | Distinguer découverte, construction de l’option, sélection et envoi dans G1CHOICE/AIDEFY. Le champ starts_enabled n’établit pas la première étape. |
| **W4 — 2 pts** | Conservation du reçu exact indépendante des rôles/CB, clôture des choix dans quatre callbacks natifs et gardes de contexte. | Intégration effective aux transitions/clôtures guerre et Mega Wars ; adaptations éventuelles selon les scopes, l’ordre et les remplacements observés. | WARLIFE-01…08 et témoin AGOT. Ne pas réécrire les cycles natifs pour contourner l’absence d’observation. |
| **W5 — 2 pts** | Tests négatifs de source/générateur, gardes de cible/numéro/autorité, préservation des octets natifs. | Couverture du chemin de jeu effectivement retenu et livré, distinct des diagnostics ; corriger les lacunes identifiées après choix du chemin W2/W4. | Dépend du chemin final. Ajouter des tests répétant les mêmes gardes ne suffit pas à terminer le critère. |
| **J4 — 2 pts** | Disgrâce politique, archives et diagnostic de transferts ; sanctions personnelles séparées. | Mesure coercitive familiale/dynastique effective sur terres ou statut, couvrant les routes G3 et l’autorité qui l’impose. L’interdiction universelle de terres pendant 50 ans n’est pas implémentée. | Développement réel manquant et mécanisme de couverture non établi. Les sources d’octroi/succession/élection/conquête sont déjà reçues ; un callback après transfert n’est pas un veto. |
| **J5 — 2 pts** | Réhabilitation politique et discussions de restitution, sans restauration coercitive démontrée. | Restauration après la sanction effective J4, avec identité, autorité et état réellement sanctionné ; aucun octroi automatique supposé. | Dépend de J4. Une réhabilitation politique supplémentaire ne remplace pas la restauration de terres/statut. |
| **AI4 — 2 pts** | Voies originales IA de justice/négociation et réactions royales ; préférence initiale de défi. | Parcours autonome IA↔IA traversant aussi l’initiative de guerre, avec mêmes gardes/coûts/conséquences. | Travail de guerre partagé avec W2 puis observation AIDEFY/G4 ; ne pas compter deux fois la même modification comme deux mécanismes livrés. |

Preuves et limites : [contexte W1](G1_DECLARATION_LAW_CONTEXT.md),
[choix natif W2](G1_NATIVE_CHOICE.md), [préférence IA](G1_AI_OPTION_POLICY.md),
[cycle du reçu W4](G1_WAR_RECEIPT_LIFECYCLE.md),
[frontière G3](G3_HOUSE_SANCTIONS.md) et [audit des routes](TITLE_ROUTE_AUDIT.md).

## Décision J4 après examen ciblé — 5 novembre 2026

**J4 mis en attente, pas livré.** Trois voies natives ont été confrontées au besoin :

- L’extinction de famille noble (`celestial_extinguish_noble_family_interaction`)
  exige un souverain céleste humain joueur et un destinataire IA avec titre de famille
  noble. Ces conditions ne fournissent pas une sanction féodale AGOT symétrique.
- Le déshéritement natif vise une personne avec ses conditions dynastiques/culturelles ;
  il ne couvre pas octroi et conquête, ni une interdiction de maison de cinquante ans.
- La confiscation actuelle via `revoke_title_interaction` serait une mesure distincte
  et réelle, mais son interface spéciale sélectionne un titre. La transmission sûre
  de ce titre dans un appel automatisé conservant coûts, refus/résistance et choix IA
  n’est pas établie par les sources reçues. Lier un scope ou ouvrir la fenêtre n’en
  constitue pas la preuve. Ne pas inventer un argument de run_interaction, copier
  directement le helper de confiscation ou effectuer un transfert forcé de remplacement.

Références : [frontière G3](G3_HOUSE_SANCTIONS.md),
[audit des routes](TITLE_ROUTE_AUDIT.md), interaction AGOT de révocation (sélection
vers ligne215, acceptation408, refus570), sources déjà reçues. Aucun nouvel envoi requis.
Ce constat porte sur les voies examinées ; il ne prouve pas une impossibilité générale.

J5 reste dépendant d’une sanction effective. Reprendre J4 avec une capacité native
précise documentée ou des observations de la campagne finale G3 ; celles-ci peuvent
nécessiter une nouvelle investigation/implémentation, elles ne garantissent pas une
solution. Ne pas relire les mêmes voies à chaque « continue » ni produire une autre
PR de diagnostic/variante pour masquer le blocage. Le prochain travail moteur utile
est l’investigation de faisabilité G1/G3 au début de la **campagne finale déjà prévue**,
avec corrections/retests selon résultats. Aucun test intermédiaire demandé ici.
Le code de jeu et le score restent inchangés :64/80 +0/20, total64/100.

## Ordre de continuation

1. **Cible substantielle J4, actuellement en attente selon la décision ci-dessus**, puis J5 lorsqu’une sanction
   effective existe. Partir des routes déjà auditées et d’une hypothèse technique
   précise : quel mécanisme natif peut imposer la mesure, à qui, avec quelle autorité,
   quels refus/coûts et quelles routes couvertes ? Développer seulement une voie
   étayée ; garder visibles les routes non couvertes. Les définitions natives reçues
   ne démontrent ni un point d’extension universel ni une impossibilité universelle.
2. **W1/W2/W4/AI4 : préserver le candidat actuel**, reprendre leur code pour un défaut
   concret ou une preuve de source levant un manque précis. Ne pas produire une autre
   variante de dialogue, un diagnostic supplémentaire ou un préfixe de métadonnées
   comme substitut à la découverte IA ou à la compatibilité Mega Wars.
3. **Si la voie sûre n’est pas établie dans les sources disponibles**, enregistrer
   la dépendance et mettre ce morceau en attente. Ne pas remplir les tours par des
   PR à +0 sans défaut concret ou déblocage identifié. Ne pas changer discrètement
   le périmètre, les conditions d’AGOT ou le barème pour obtenir des points.
4. **Campagne CK3 finale maintenue**, selon [FINAL_ENGINE_TESTS.md](FINAL_ENGINE_TESTS.md).
   Elle sert aussi à lever les questions de faisabilité encore ouvertes : prévoir
   des corrections et nouvelles vérifications après ses premiers résultats.
   On ne promet donc pas 80/80 avant toute observation, ni une seule passe de tests
   sans reprise du développement. Aucun lancement intermédiaire demandé au propriétaire.

## Rapports à fournir

À chaque livraison : fonctionnalité réellement ajoutée ou défaut corrigé, critère
achevé ou encore ouvert, point précis débloqué, tests disponibles et delta réel.
Dire explicitement si l’étape suivante est du code, une preuve de source ou une
observation CK3. Le nombre de PR/tests et le volume de scripts ne mesurent ni le
pourcentage global de la vision finale ni une vitesse de développement.
