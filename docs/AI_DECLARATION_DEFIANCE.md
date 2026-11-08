# Préférence IA de défi à la déclaration

Tranche du 8 novembre 2026. **Static-checked**, **non testée dans CK3**.
Baseline et résultat 80/80 source, 0/20 campagne, delta 0.

## Point d'entrée et portée

Le champ natif `starts_enabled` attend un booléen pour présélectionner la case de
défi. La préférence utilise désormais une comparaison déterministe entre motivation
et prudence. Les mêmes entrées produisent la même réponse lors des réévaluations.
Le profil ne stocke aucun choix et ne lance aucun tirage aléatoire.

La garde partagée de loi applicable reste requise, avec acteur et destinataire
féodaux, adultes, vivants, possessionnés et libres dans ce périmètre. Le helper
natif conserve les exceptions de loi et de contrat. Le hameçon sélectionné exclut
la préférence de défi. L'initialisation exige toujours un acteur IA. Le joueur
conserve la case initialement décochée et son choix explicite.

Les valeurs sont calculées en scope du déclarant original. Les seules identités
lues sont l'acteur, le destinataire et le lige actuel de l'acteur, avec le booléen
natif du hameçon sélectionné. Le bénéficiaire d'une revendication, le conjoint,
les titres exacts et leurs enjeux ne sont pas déduits d'identités supposées.
Ce contexte de case initiale ne démontre pas ces informations de CB sélectionné.

## Motivation

La motivation commence à 50. Les composantes natives réutilisent les facteurs
bornés du décideur dans le profil de réponses extérieures. Les contributions
ci-dessous utilisent donc des axes effectifs limités à l'intervalle -100 à 100
par ces facteurs partagés.

| Entrée | Contribution |
| --- | --- |
| Audace | De -25 à +25 |
| Honneur | De +20 à -20 quand l'honneur augmente |
| Énergie | De -10 à +10 |
| Compassion | De +10 à -10 quand la compassion augmente |
| Opinion du lige au plus -25 | +15 |
| Opinion du lige au moins 25 | -15 |
| Opinion du destinataire au plus -25 | +10 et contribution de vengeance entre -10 et +10 |

La vengeance s'applique seulement à cette hostilité connue du déclarant.
La motivation est bornée entre 0 et 100. Un contexte absent ou invalide lui
conserve sa valeur de zéro.

## Prudence

La prudence commence à 60 dans un contexte valide. La charge matérielle suivante
est additionnée, puis multipliée par le facteur positif de rationalité du décideur,
borné entre 0.5 et 1.5. Les tranches de trésorerie sont exclusives.

| Charge propre | Ajout avant rationalité |
| --- | --- |
| Trésorerie négative | 25 |
| Sinon moins de 50 pièces | 20 |
| Sinon moins de 150 pièces | 10 |
| Déjà en guerre | 20 |
| Engagement personnel de service/faveur reconnu | 10 |
| Niveau de stress d'au moins 2 | 10 |
| Santé inférieure à 3 | 15 |

La prudence ajoute ensuite les facteurs politiques suivants.

| Situation connue | Ajout |
| --- | --- |
| Lige interdisant toutes les guerres | 5 |
| Crainte native du lige de niveau 2 | 25 |
| Sinon crainte de niveau 1 | 10 |
| Lige proche parent ou allié | 10 |
| Destinataire proche parent ou allié | 15 |
| Hameçon utilisable sur le lige | 10 |

L'or représente ici une réserve et une appréciation du risque. Le profil ne prélève
aucune somme. Un hameçon utilisable est une alternative politique connue. Le
profil ne le sélectionne ni ne le consomme. Les deux niveaux de crainte sont
exclusifs. La prudence valide est bornée entre 0 et 250. Hors contexte, sa valeur
reste à 1000, au-dessus de toute motivation admissible.

## Comparaison et exécution native

La préférence devient vraie si la motivation atteint ou dépasse la prudence,
après la garde partagée et le contrôle de l'acteur IA. Une guerre existante,
une obligation ou une faible réserve augmentent donc la prudence. Elles conservent
leurs effets propres dans les conditions natives de déclaration.

Le booléen concerne la présélection de la case. La découverte du candidat,
le choix du CB, la décision d'envoi, les coûts réels et la résolution restent
au moteur. G1_AI_AUTONOMY.md conserve les deux observations de déclarations IA
de PRIVATE0.0.6. Ces observations ne constituent pas une validation moteur de
la nouvelle comparaison et de ses nouveaux facteurs.

## Traitement des traits et limites

Les traits et modificateurs se combinent d'abord dans les tendances natives du
déclarant. Les opinions, moyens, santé, stress, crainte, famille et alliances
apportent des chemins contextuels supplémentaires. L'âge conserve les gardes
adultes et ses effets indirects. Avidité, zèle, sociabilité, martialité et prouesse
n'ont pas de coefficient direct ajouté dans cette comparaison politique.

Les objectifs précis du CB, son bénéficiaire, les intérêts du conjoint, les enjeux
de chaque titre, les puissances et soutiens anticipés, la foi et la culture dans
la cause de guerre restent à approfondir. La revue exhaustive de chaque trait
reste ouverte. Les autres conditions CK3/AGOT continuent de décider de l'action
réellement admissible.

## Vérification et campagne finale

Les docs moteur générées décrivent `has_dread_level_towards`, ses niveaux, et
`has_usable_hook`. Les sources AGOT utilisent les comparaisons de valeurs scriptées
et les soustractions dynamiques. Ce sont des références de syntaxe inspectées.
L'évaluation de cette combinaison dans la fenêtre native reste à observer.

Huit nouvelles régressions de source et une vérification des fichiers livrés
couvrent identité, score hors contexte, garde native, hameçon, directions des
composantes, charge, peur, lecture seule et absence de hasard. L'empreinte de
tout le fichier de gardes hors préférence initiale est conservée. L'option native
et ses insertions générées gardent leurs octets. PRIVATE0.0.10 recense désormais
trente sources de runtime. Utiliser le socle et les adaptateurs du même commit.

La campagne groupée doit distinguer découverte, présélection, option finalement
retenue et envoi natif. Comparer profils, relations, crainte, trésorerie, charges,
stress, santé, contrat et hameçons, puis cibles/liges modifiés, annulation et
rechargement. Contrôler le joueur, les cas hors contexte, plusieurs réévaluations,
les coûts réels, les réactions et Mega Wars. Aucun nouveau résultat moteur ou
de performance n'est revendiqué.
