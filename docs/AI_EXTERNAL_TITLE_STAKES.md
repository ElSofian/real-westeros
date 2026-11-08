# Enjeux des titres pour les autres décideurs extérieurs

Tranche RW-004 du 8 novembre 2026. **Static-checked**, expérimentale,
**non testée dans CK3**. Départ et résultat 80/80 source et 0/20 campagne finale.
Delta réel 0.

## Périmètre et rôles

Le seigneur lige du déclarant apprécie désormais l'importance des titres ciblés
lorsqu'il répond à la guerre extérieure de son vassal. Le médiateur retrouve
ce même enjeu dans son propre tour de réponse à une demande. Le déclarant peut
s'attacher davantage à la revendication lorsqu'il répond à son lige ou au
protecteur et que son bénéficiaire original est connu et vivant.

Le protecteur conserve le lecteur des titres de ses propres vassaux décrit dans
AI_PROTECTED_TITLE_STAKES.md. Les autres décideurs utilisent l'importance du
conflit entier qu'une intervention native chercherait à interrompre. Un dossier
de médiation reste celui de son protecteur demandeur, avec sa fenêtre, ses
identités et ses gardes de consentement propres. Le lecteur ne crée aucun droit
sur les titres d'un autre protecteur.

L'enjeu politique de la revendication ne calcule pas encore les gains attendus,
la richesse, les transferts ou la vassalité d'après-guerre. Les effets natifs et
les autres motivations restent déterminants. Aucun consentement, personnalité
ou soutien du bénéficiaire n'est déduit de son identité.

## Source et détenteurs réels

Le lecteur exige le tour actif du lige du déclarant, du déclarant lui-même ou
du médiateur. Le rôle de lige déclarant est requis pour la première entrée.
Les prédicats existants conservent les identités, guerre, autorités, titres
représentatifs et fenêtres propres à chaque dossier.

La source doit conserver son type, propriétaire, schéma, numéro lié positif,
phase, rétention, date, guerre et parties exacts. Le schéma des parties, l'état
de capture complète, un nombre positif et des compteurs concordants sont requis.
Les données partielles ou anciennes sans ces faits gardent un facteur neutre.

Chaque fait de titre doit avoir le bon type, propriétaire, parent, numéro parent,
guerre, date et détenteur connu. Ce détenteur doit être vivant et posséder encore
le titre. S'il est le défenseur principal exact de la guerre, cette identité
suffit pour le rattacher au côté attaqué. Cela inclut un défenseur indépendant,
sans lui inventer un suzerain à partir d'un champ absent.

Pour tout autre détenteur, le lecteur exige son suzerain direct et son autorité
capturés encore concordants, ainsi que sa position actuelle sous le défenseur.
Les vassaux de niveaux inférieurs sont donc admissibles avec leur véritable
identité. Une référence manquante, un détenteur remplacé, une guerre étrangère
ou une hiérarchie devenue incompatible excluent ce fait. Les autres faits
valides restent utilisables.

L'attachement du déclarant exige en plus son propre tour et le bénéficiaire
original connu, existant et vivant. Celui-ci peut être le déclarant ou un tiers,
y compris sans terres. Une donnée absente ou un bénéficiaire mort laisse cette
pondération neutre.

## Coefficients provisoires

La formule reprend les tranches de titres précédentes. Le facteur commence à 1.
Seul le plus haut rang présent ajoute 0.1 pour un comté, 0.2 pour un duché,
0.3 pour un royaume et 0.4 pour un empire ou rang supérieur. Une baronnie seule
conserve l'ajout de rang nul. Le titre principal actuel d'au moins un détenteur
ajoute 0.2. Au moins deux faits valides ajoutent 0.1 une seule fois. Les facteurs
restent entre 1 et 1.7. Les recherches utilisent les dossiers de l'attaquant initial.

Pour le lige du déclarant, ce facteur multiplie la préoccupation existante,
qui garde ses bornes de 0.5 à 2. Cela favorise relativement désapprobation,
demande et tentative d'intervention, et réduit relativement l'ignorance de la
guerre. Pour le médiateur, il multiplie l'acceptation et divise le refus.
Le signalement d'une tentative déjà présente conserve son poids factuel sous
sa garde existante. Pour le déclarant, l'attachement à l'objectif multiplie le
refus et divise l'accusé de réception. Les autres motivations et les bornes
finales des choix admissibles restent applicables. Ces coefficients sont
provisoires et leur effet comportemental reste à observer.

## Vérifications et suite

Huit tests de source et un contrôle du kit livré couvrent les tours distincts,
la source complète, les faits exacts, défenseur principal indépendant et vassaux
imbriqués, bénéficiaire propre ou tiers, données absentes ou mortes, rangs
exclusifs, titre principal du véritable détenteur, pluralité, sens des réponses
et lecture seule locale. Les mutations négatives retirent les gardes.

Une inversion retire les deux facteurs et leurs cinq appels pour comparer
l'ensemble du profil précédent, y compris le lecteur du protecteur et les
facteurs communs aux autres parcours. Les vérifications historiques du
bénéficiaire et du protecteur réutilisent ce retrait séparément contrôlé.
L'empreinte du fichier partagé du test entre pairs est actualisée. Les graphes
d'actions et les sept empreintes d'effets, gardes et cycle extérieurs restent
identiques. Le socle et PRIVATE0.0.10 attestent 35 sources de runtime. Les quatre
sorties natives restent identiques.

Les docs moteur générées décrivent les entrées de rang, titre principal,
hiérarchie de vassalité et histoires possédées déjà inspectées. Leur combinaison
reste à observer dans CK3. La campagne groupée doit varier les trois décideurs,
les rangs, titres principaux, pluralité, défenseur indépendant, détenteur sous
le défenseur, plusieurs protecteurs, bénéficiaire propre/tiers/sans terres,
données manquantes, mort, changements de détenteur ou d'autorité, rechargements
et fenêtres périmées. Vérifier poids, choix, consentement et coûts natifs, ainsi
que le coût de calcul. Aucun lancement intermédiaire requis. La prochaine
revue porte sur la puissance et les soutiens connus. Gains économiques,
droits de jure et couverture exhaustive du contexte restent ouverts.
