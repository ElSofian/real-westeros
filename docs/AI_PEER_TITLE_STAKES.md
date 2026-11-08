# Enjeux des titres dans les réponses entre pairs

Tranche RW-004 du 8 novembre 2026. **Static-checked**, expérimentale,
**non testée dans CK3**. Départ et résultat 80/80 source et 0/20 campagne finale.
Delta réel 0.

## Deux décideurs et un objectif contesté

Dans une guerre entre vassaux d'un même lige, le lige apprécie l'importance des
titres effectivement menacés du côté du défenseur. Le déclarant peut accorder
plus d'importance à la poursuite de la revendication lorsque son bénéficiaire
original est connu et vivant. Cette identité peut être celle du déclarant ou
d'un tiers, y compris un bénéficiaire sans terres.

Les relations propres du décideur au déclarant, au défenseur et au bénéficiaire
conservent leurs facteurs précédents. La personnalité du bénéficiaire, son accord
et ses moyens ne sont pas inférés. L'attachement à la revendication décrit ici
l'enjeu politique de l'objectif. Le résultat, les transferts et la situation de
vassalité d'après-guerre restent déterminés par le CB natif. Cette tranche ne
calcule pas encore un gain territorial ou financier attendu.

## Identités et titres utilisés

Le lecteur exige un tour actif du lige ou du déclarant, le lien exact vers le
relevé précoce, son numéro, son schéma de parties et sa date. Le prédicat existant
`rw_dl_match_response_trigger` vérifie type, propriétaire, guerre, parties,
autorité, phase et rétention. La capture doit indiquer tous les titres enregistrés
avec un nombre positif et des compteurs concordants. Une capture partielle ou
ancienne sans ces données conserve le facteur neutre de 1.

Chaque fait utilisé conserve son type, propriétaire, parent, numéro parent,
guerre, date, titre, détenteur connu, suzerain direct et autorité. Le détenteur
doit être vivant et posséder encore le titre. Son suzerain direct et son autorité
capturés doivent toujours correspondre à leur situation actuelle.

Les faits admissibles concernent le défenseur principal ou ses propres vassaux,
y compris les niveaux inférieurs. Un comté détenu sous un duc défenseur peut
donc contribuer à l'enjeu. Le lecteur conserve le véritable détenteur et sa
propre autorité directe. Il ne remplace aucun de ces rôles par le défenseur ou
le lige commun. Les titres étrangers à ce côté de la guerre, les références
absentes, détenteurs morts ou contextes modifiés sont exclus. Les autres faits
valides restent utilisables.

L'attachement du déclarant exige en plus son propre tour et le bénéficiaire
original connu, existant et vivant. L'absence de ce fait laisse ce coefficient
neutre, tout en conservant la lecture des titres pour le lige.

## Coefficients provisoires et effets sur les préférences

La formule reprend les valeurs de AI_PROTECTED_TITLE_STAKES.md. Le facteur de
base vaut 1. Seul le plus haut rang présent ajoute 0.1 pour un comté, 0.2 pour un
duché, 0.3 pour un royaume et 0.4 pour un empire ou rang supérieur. Une baronnie
seule apporte un ajout de rang nul. La présence du titre principal actuel d'un
détenteur ajoute 0.2. Au moins deux faits valides ajoutent 0.1 une seule fois.
Les deux facteurs restent entre 1 et 1.7. Les recherches considèrent les faits
correspondants dans les dossiers locaux de l'attaquant initial.

Pour le lige, ce facteur multiplie sa préoccupation pour le défenseur, qui garde
ses bornes de 0.5 à 2. Cela renforce relativement la censure, la demande et la
tentative d'intervention native, et réduit relativement l'ignorance de la guerre.
Pour le déclarant, l'attachement à l'objectif multiplie le refus et divise l'accusé
de réception. Les bornes finales de 1 à 300 des choix admissibles restent en place.
L'accusé de réception conserve sa portée définie dans les documents précédents.
Les autres motivations et la position réelle de la guerre restent applicables.

## Vérification et campagne finale

Huit tests de source et un contrôle du kit livré couvrent les liens exacts,
capture partielle, titres du défenseur et de ses vassaux, détenteur et autorité
modifiés, bénéficiaire absent ou mort, revendication propre, sens opposés des
réponses, rangs exclusifs, titre principal du véritable détenteur, pluralité,
lecture seule et recherches locales. Les mutations négatives retirent ces
gardes. Une inversion retire les deux nouveaux facteurs et leurs trois appels
pour comparer l'ensemble du profil précédent. Le graphe d'actions et les effets,
gardes, cycles et autres profils conservent leur contenu.

Les docs moteur générées décrivent `is_vassal_or_below_of` depuis un personnage,
les comparaisons `tier`, `primary_title` et `any_owned_story`. Leur combinaison
avec les faits reste à observer en jeu. Le socle et PRIVATE0.0.10 correspondants
attestent 34 sources de runtime. Les quatre sorties natives restent identiques.

La campagne groupée doit comparer les deux décideurs avec un titre direct et un
titre détenu sous le défenseur, tous les rangs, titre principal ou secondaire,
un ou plusieurs faits, bénéficiaire propre ou tiers, sans terres, absent ou mort.
Tester les faits étrangers et contextes modifiés, fenêtres périmées, rechargements,
poids et décisions réelles, coûts natifs et coût de calcul avec de nombreux dossiers
locaux. Aucun lancement intermédiaire requis. Les intérêts des titres dans les
autres réponses extérieures et la médiation restent à approfondir, puis puissance
et soutiens attendus. Richesse, droits de jure et couverture exhaustive du contexte
restent ouverts.
