# Préférences IA des guerres entre vassaux du même lige

Tranche du 8 novembre 2026. **Static-checked**, **non testée dans CK3**.
Baseline et résultat 80/80 source, 0/20 campagne, delta 0.

## Six choix et identité

Les réponses du lige commun et du déclarant utilisent six poids nommés dans
`rw_peer_war_ai_values.txt`. Chaque poids commence à zéro et exige la garde
réelle du tour ou de l'intervention native. Celle-ci conserve l'identité du
dossier, son numéro, les parties, la guerre, l'autorité et les fenêtres existantes.
Les neuf facteurs communs de personnalité et de charge personnelle proviennent
du profil extérieur et lisent uniquement le personnage qui décide.

Toutes les références aux parties, au dossier et à la guerre restent dans le
contexte `rw_uw_*` du parcours entre pairs. Les relations contextuelles du
parcours extérieur ont leurs propres lecteurs. Le profil entre pairs ne crée
aucun alias de conversion entre les deux familles.

| Choix | Base conservée | Facteurs |
| --- | --- | --- |
| Laisser passer | 20 | Prudence, attachement à l'attaquant, préoccupation pour le défenseur en sens inverse, faible initiative et attention occupée |
| Censurer | 20 | Vengeance, fermeté, préoccupation pour le défenseur, attachement à l'attaquant en sens inverse, signal politique peu coûteux |
| Demander la fin de guerre | 30 | Honneur, compassion, initiative, relations aux deux vassaux, capacité d'attention |
| Intervention native | 20 | Même résolution, capacité d'attention, moyens propres |
| Accuser réception | 30 | Sociabilité, prudence, relation au lige, position de guerre en sens inverse |
| Refuser | 15 | Fermeté, vengeance, relation au lige en sens inverse, position de guerre |

## Coefficients et connaissances

Les facteurs natifs communs conservent les formules documentées dans
AI_EXTERNAL_WAR_RESPONSES.md, avec bornes positives. Le lige lit sa propre opinion
de l'attaquant et du défenseur. Le déclarant lit sa propre opinion du lige.
L'opinion d'au moins 25 multiplie l'affinité par 1.25, celle d'au plus -25 par
0.75. Un proche parent ou allié multiplie aussi par 1.25. Chaque affinité reste
entre 0.5 et 2. Les liens publics et l'opinion ont des contributions distinctes.

La recherche d'une résolution multiplie honneur, compassion, initiative et
préoccupation pour le défenseur, puis divise par l'affinité pour l'attaquant.
Le facteur commun de charge tient compte d'une guerre en cours, du stress,
de la santé et des engagements de service/faveur reconnus. Il réduit les actions
actives et favorise relativement la retenue ou la censure peu coûteuse.

Les fonds inférieurs à 50 réduisent de 0.75 la préférence pour tenter une
intervention native. Les messages gratuits conservent leur coût propre. La
réponse au lige reçoit un facteur de 1.25 pour l'accusé de réception et 0.8 pour
le refus, en cohérence avec le rôle d'autorité de cette demande.

Le déclarant lit le score attaquant de sa guerre exacte. À partir de 25, le facteur
de position du refus multiplie par le facteur de rationalité. À -25 ou moins,
il divise par celui-ci. L'accusé de réception utilise l'inverse. Le facteur de
position reste entre 0.5 et 1.5. La réponse politique garde sa portée existante.

Chaque choix admissible conserve un poids entre 1 et 300. Les choix hors contexte
restent à zéro. Les traits sont combinés dans les tendances natives du décideur.
Le profil ne consulte aucun trait ou opinion privé d'un autre personnage.

## Portée de cette tranche

Le graphe d'actions de l'événement, après retrait des seuls `ai_chance`, est
identique à celui de départ. Les quatre fichiers d'effets, gardes et cycle du
parcours entre pairs et le profil extérieur partagé ont les mêmes empreintes.
Les prérequis, coûts, conséquences et capacités natives conservent leurs gardes
communes joueur/IA. La préférence initiale de déclaration de guerre conserve sa
revue séparée. La politique ne transmet aucun dossier à un supérieur.

L'âge conserve ses gardes adultes et effets natifs indirects. La revue exhaustive
des traits, de la puissance, des soutiens, de la crainte, des enjeux dynastiques,+de la foi, de la culture et des intérêts de tous les titres reste ouverte.
Les coefficients directs nuls et limites du profil extérieur restent applicables
aux facteurs communs utilisés ici.

## Vérification et campagne finale

Huit régressions de source couvrent les six poids raccordés, les gardes de tour,
les relations, la séparation des contextes, la réutilisation des seuls facteurs
communs sans références aux parties et la lecture seule. Un contrôle des fichiers
livrés réutilise ces vérifications avec des mutations négatives. Les formes des
entrées natives sont celles déjà inspectées pour le profil extérieur.

Le kit PRIVATE0.0.10 recense désormais vingt-huit sources de runtime. Le nouveau
profil original est inclus dans le socle. Les sorties natives générées restent
identiques à la livraison précédente. Utiliser socle et adaptateurs du même commit.

La campagne groupée doit comparer poids et décisions avec le lige puis le
déclarant comme joueur et IA, des relations opposées aux deux vassaux, liens
familiaux/alliances, santé, stress, engagements, moyens et scores de guerre.
Vérifier fenêtres périmées, dossiers étrangers, rechargements, coûts et effets
natifs, ainsi que l'autre parcours extérieur. Mesurer le coût de calcul et
observer plusieurs décisions. Aucun résultat comportemental nouveau n'est établi.

## Extension du bénéficiaire

AI_PEER_BENEFICIARY.md documente le lecteur du revendiquant tiers enregistré au
début de la guerre. Les poids utilisent désormais l'affinité propre du décideur
avec ce tiers sous gardes exactes. Le socle et PRIVATE0.0.10 correspondants
recensent 31 sources de runtime. La préférence initiale de déclaration et le
profil extérieur conservent leur revue séparée. Source delta0, non testé moteur.

## Extension des enjeux de titres

AI_PEER_TITLE_STAKES.md relie les véritables titres du côté du défenseur à la
préoccupation du lige et à l'attachement du déclarant à la revendication connue.
Les détenteurs sous le défenseur conservent leur identité et autorité propres.
Le socle et PRIVATE0.0.10 attestent 34 sources de runtime. Coefficients
provisoires, delta0, non testé moteur.

## Extension des soutiens entrés en guerre

AI_COMMITTED_WAR_SUPPORT.md relie les participants secondaires vivants avec
un effectif natif positif aux réponses du déclarant. Les deux camps sont lus
dans la même guerre exacte. La présence de soutien reste distincte de sa force
effective ou de sa mobilisation sur ce front. Coefficient provisoire0.8..1.25,
delta0, non testé moteur. Runtime35 dans le kit correspondant.

## Extension du regroupement avec une armée propre

AI_OBSERVED_REINFORCEMENTS.md ajoute un signal de regroupement physique de deux
armées de propriétaires distincts, dont l'une appartient au déclarant. Le tour
propre et l'unique guerre du déclarant sont requis. La visibilité du regroupement
reste une hypothèse de campagne finale, avec coefficient provisoire1..1.1.
Delta0, non testé moteur. Runtime35 dans le kit correspondant.
