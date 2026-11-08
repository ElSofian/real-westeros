# Titres menacés et préférence du protecteur

Tranche RW-004 de la revue de fond du 8 novembre 2026. **Static-checked**,
expérimentale et **non testée dans CK3**. Départ et résultat 80/80 source,
0/20 campagne finale. Delta réel 0.

## Périmètre retenu

Le protecteur adverse apprécie désormais les titres ciblés de ses propres
vassaux directs. Dans l'exemple Leyton–Dayne, Doran utilise les véritables faits
de titres du CB, même si le défenseur principal est une autre personne.
Le calcul peut reconnaître plusieurs détenteurs sous sa même autorité. Le titre
représentatif continue de déterminer la validité du dossier existant.

Ce premier lecteur des enjeux concerne les réactions du protecteur. L'intérêt
des titres pour le déclarant, son bénéficiaire, son lige, le médiateur et le
parcours entre pairs garde sa revue suivante. La richesse des terres, les
bâtiments, le développement, les droits de jure, les chances de victoire et le
soutien attendu restent ouverts. Le rang fournit ici un signal politique.

## Données historiques et situation actuelle

Le lecteur exige le tour actif du protecteur, sa source originale et son numéro,
le propriétaire, schéma des parties, phase, rétention, date, guerre et parties.
La capture doit indiquer tous les titres enregistrés, avec un nombre positif
et des compteurs concordants. Une capture partielle ou ancienne sans ces données
conserve un facteur neutre de 1.

Chaque fait utilisé doit avoir le bon type, propriétaire, parent, numéro parent,
guerre et date. Son détenteur connu doit être vivant et détenir encore le titre.
Son suzerain et son autorité capturés doivent toujours correspondre au protecteur
actuel et à l'autorité du dossier. Les références requises doivent exister.
Les titres d'un autre protecteur, étrangers ou dont le détenteur a changé sont
exclus, sans substitution. Les autres faits valides restent utilisables.

Le rang est lu sur le titre réellement ciblé. Le caractère principal du titre
est apprécié au moment de cette décision chez son détenteur enregistré. Un
changement de titre principal peut donc changer ce signal. Aucun relevé historique
n'est réécrit. Les liens au déclarant, bénéficiaire et défenseur principal restent
distincts de l'identité du détenteur.

## Coefficients provisoires

Le facteur commence à 1. Le plus haut rang présent parmi les faits valides ajoute
une seule des valeurs suivantes.

| Rang du titre ciblé | Ajout |
|---|---|
| Comté | 0.1 |
| Duché | 0.2 |
| Royaume | 0.3 |
| Empire ou rang supérieur | 0.4 |

Une baronnie seule conserve l'ajout de rang nul. Les rangs inférieurs ne se
cumulent pas. La présence du titre principal d'au moins un détenteur ajoute 0.2.
Au moins deux faits de titres valides ajoutent 0.1, une seule fois. Tous les faits
correspondants peuvent satisfaire les recherches, sans tronquer la liste à un
nombre arbitraire. Le facteur reste entre 1 et 1.7.

Ce facteur multiplie la préoccupation du protecteur pour les terres attaquées.
Les bornes existantes de cette préoccupation restent de 0.5 à 2. Cela renforce
relativement la désapprobation, la demande et la sollicitation de médiation,
et réduit relativement l'ignorance de la guerre. Les autres motivations et les
bornes finales de poids restent applicables. Ces coefficients sont des choix
de conception provisoires à observer en campagne finale.

## Vérification et limites moteur

Le lecteur recherche uniquement dans les dossiers possédés par l'attaquant
initial et filtre chaque fait par son identité exacte. Il n'écrit aucun état,
ne lance aucune interaction et ne recherche aucun personnage globalement.
Le coût effectif des recherches répétées reste à mesurer dans CK3.

Les docs moteur générées décrivent les comparaisons `tier` en scope de titre,
`primary_title` depuis un personnage et `any_owned_story`. Une valeur AGOT
inspectée utilise déjà des histoires possédées dans un calcul numérique.
Cette inspection établit les formes utilisées, sans prouver leur évaluation ici.

Huit régressions de source et un contrôle du kit livré couvrent les contextes
périmés ou étrangers, la capture partielle, les détenteurs changés, les recherches
exactes, les rangs exclusifs, le titre principal du véritable détenteur, la
pluralité et les bornes. Les mutations négatives détectent les gardes retirées.
Une inversion retire le seul nouveau facteur et son appel pour comparer tout
le profil antérieur. Le contrôle de la tranche bénéficiaire retire explicitement
cette extension séparément vérifiée avant sa comparaison historique. Le test
entre pairs actualise l'empreinte du fichier partagé. Les graphes d'actions et
les sept empreintes d'effets, gardes et cycle extérieurs restent identiques.

Le socle et PRIVATE0.0.10 correspondants attestent 33 sources de runtime. Les
quatre sorties natives restent identiques. La campagne finale doit comparer
baronnie/comté/duché/royaume/empire, titre principal ou secondaire, un ou plusieurs
titres, plusieurs détenteurs et plusieurs protecteurs. Vérifier les identités,
les poids, les décisions et les coûts natifs, données absentes, changements de
détenteur/autorité/titre principal, fenêtres périmées et rechargements. Mesurer
le coût avec beaucoup de faits locaux. Aucun test manuel intermédiaire requis.
