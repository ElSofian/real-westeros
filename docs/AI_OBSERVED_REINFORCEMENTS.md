# Regroupement observé avec les armées du déclarant

Tranche RW-004 du 8 novembre 2026. **Static-checked**, expérimentale,
**non testée dans CK3**. Départ et résultat 80/80 source et 0/20 campagne finale.
Delta réel 0.

## Données disponibles et limite de connaissance

L'audit local établit des points d'entrée de script vers les armées, leurs
propriétaires et leurs provinces. Les docs moteur générées donnent les relations
suivantes.

| Entrée | Scope de départ | Donnée obtenue |
|---|---|---|
| `any_army` | Personnage | Armées parcourues |
| `army_owner` | Armée | Personnage propriétaire |
| `location` | Armée | Province courante |
| `any_army_in_location` | Province | Armées de cette province |
| `army_size` | Armée | Taille courante |
| `is_raid_army` | Armée | Statut de raid |
| `squared_distance` | Province ou titre | Distance cartographique au carré |

Les sources AGOT inspectées utilisent déjà `any_army` et les comparaisons du
propriétaire d'armée. Un filtre de visibilité des positions lointaines utilisable
en script n'est pas établi par cet audit. Le premier signal s'appuie donc sur
un regroupement avec une armée propre au déclarant, dans la même province.
L'hypothèse d'observation de ce regroupement fait partie de la campagne finale.

Le calcul de temps d'arrivée exige encore l'audit des itinéraires, passages et
transports, indépendamment de la distance cartographique exprimée en pixels au
carré. L'affectation d'une armée à une mission dans un CB reste également à établir.

## Cas retenu

Le lecteur agit seulement dans le propre tour de réponse politique du déclarant,
pour les parcours entre pairs et extérieur. La guerre exacte, ses rôles, son CB,
les identités et fenêtres restent vérifiés par les prédicats existants.

Le déclarant doit être impliqué dans cette seule guerre native. Le contrôle des
autres guerres exclut explicitement celle-ci par identité. Il permet de rattacher
prudemment ce signal au conflit discuté, sans inventer une attribution native
d'armée à ce CB. Un contexte de plusieurs guerres conserve le facteur neutre.

Un participant secondaire vivant du camp attaquant doit posséder une armée de
taille positive, avec une province courante et un statut hors raid. Le propriétaire
est comparé au personnage de ce participant lors de la recherche de ses armées.
La province doit aussi contenir une armée du déclarant, de taille positive et
hors raid. Les deux propriétaires sont distincts puisque le participant principal
est exclu de la recherche des soutiens.

Ce regroupement peut être observé au lieu de rassemblement, en marche ou à une
position de combat. Sa présence sur l'objectif du CB et sa capacité réelle à
combattre restent à examiner. Un soutien dans une autre province ne produit pas
ce nouveau signal. Les positions du camp défenseur ne sont pas interrogées.

## Pondération provisoire

Le facteur commence à 1. Lorsque le regroupement admissible est trouvé, il est
multiplié par 1.1. Les bornes restent 1..1.1. Le refus multiplie ce facteur et
l'accusé de réception le divise. Il se combine aux signaux précédents de soutien
entré en guerre et d'autres engagements. Un seul regroupement suffit, sans somme
de soldats ni multiplication par le nombre d'armées.

Aucun regroupement observé, aucune armée propre, aucune armée admissible du
soutien, contexte périmé ou plusieurs guerres du déclarant conservent 1. Les
coefficients sont provisoires. Les motivations et les bornes finales des poids
restent applicables. Les prérequis, coûts et conséquences des actions conservent
leurs gardes communes joueur et IA.

## Vérification et campagne finale

Huit régressions de source et un contrôle du kit livré couvrent le propre tour,
la seule guerre exacte, participant secondaire vivant, propriétaires distincts,
tailles positives des deux armées, exclusions de raid, province courante et
ancrage dans une armée propre. Les mutations négatives retirent ces gardes ou
changent la guerre, le camp ou le propriétaire. La lecture reste locale aux
participants, à leurs armées et à la province retenue, sans écriture ni recherche
globale de personnages ou d'armées.

Une inversion retire le seul nouveau facteur et ses deux appels de chaque profil
pour comparer les profils complets précédents. Les invariants historiques des
soutiens et titres réutilisent ce retrait séparément contrôlé. Le test entre
pairs actualise l'empreinte du fichier partagé. Les trois graphes d'événements,
les effets, gardes, cycles et sorties natives conservent leur contenu. Le socle
et PRIVATE0.0.10 correspondants conservent 35 sources de runtime.

La campagne finale doit confronter les propriétaires, positions et tailles
réellement renvoyés à l'affichage du joueur. Tester soutien seul et renfort
regroupé, autre province, armée du déclarant seule, raids, unités vides, mort,
armée attachée ou regroupée sous un autre commandement, province terrestre et
maritime, marche, siège et combat. Inclure plusieurs guerres, frontières de
visibilité, identités étrangères, rechargements, fenêtres périmées et Mega Wars.
Observer valeurs, choix, coûts et effets natifs, ainsi que le coût de calcul.
Aucun lancement intermédiaire requis. Visibilité lointaine, rattachement au front,
itinéraires, délais d'arrivée, force effective et qualité restent ouverts.
