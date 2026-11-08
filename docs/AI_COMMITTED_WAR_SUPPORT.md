# Soutiens ayant rejoint la guerre et réponse politique

Tranche RW-004 du 8 novembre 2026. **Static-checked**, expérimentale,
**non testée dans CK3**. Départ et résultat 80/80 source et 0/20 campagne finale.
Delta réel 0.

## Fait utilisé et décideur

Le déclarant peut désormais tenir compte de la présence de participants secondaires
ayant rejoint sa guerre exacte lorsqu'il répond à une demande politique d'arrêt.
Le même signal est appliqué aux parcours entre pairs et extérieur, chacun avec
ses propres identités et son propre tour. La fenêtre active, les rôles natifs,
le CB et les autorités restent vérifiés par les prédicats de réponse existants.

Le calcul consulte les attaquants et défenseurs de cette seule guerre native.
Un participant contribue au signal de son camp s'il est vivant, distinct de son
principal dirigeant de camp et possède un effectif courant natif strictement
positif. Son statut d'allié diplomatique n'est pas requis. Une entrée effective
dans la guerre peut aussi provenir d'un autre chemin natif.

Les simples alliés qui n'ont pas rejoint cette guerre ne sont pas parcourus.
Les participants sans effectif positif, morts ou principaux dirigeants de camp
sont exclus du nouveau signal. Un allié impliqué dans une autre guerre ne devient
pas un participant de celle-ci. Les anciennes relations d'alliance conservent
leur portée relationnelle.

L'entrée dans la guerre est un engagement déclaré. La présence physique des
armées, leur mobilisation, leurs autres engagements, leur route, la qualité,
les dragons et les effectifs réellement disponibles sur ce front restent à
approfondir. Le signal porte ici sur la présence d'un soutien avec un effectif
courant positif. Il ne produit aucune somme de soldats et aucun pronostic de
force de coalition.

## Coefficients provisoires

Le facteur commence à 1 et n'est évalué que pendant le propre tour du déclarant.
Chaque camp utilise désormais le meilleur signal de disponibilité observé parmi
ses participants secondaires admissibles. Au moins un soutien sans autre guerre
donne 1.25. Lorsque tous ces soutiens participent également à une autre guerre,
le signal vaut 1.1. Un camp sans soutien admissible vaut 1. Le facteur global
multiplie le signal attaquant et divise par le signal défenseur. Les bornes
restent de 0.8 à 1.25. AI_SUPPORT_COMPETING_WARS.md détaille cette extension.

| Signal attaquant | Signal défenseur | Facteur |
|---|---|---|
| Aucun | Aucun | 1 |
| Sans autre guerre | Aucun | 1.25 |
| Tous dans d'autres guerres | Aucun | 1.1 |
| Aucun | Sans autre guerre | 0.8 |
| Aucun | Tous dans d'autres guerres | Environ 0.909 |
| Sans autre guerre | Sans autre guerre | 1 |
| Tous dans d'autres guerres | Tous dans d'autres guerres | 1 |
| Sans autre guerre | Tous dans d'autres guerres | Environ 1.136 |
| Tous dans d'autres guerres | Sans autre guerre | 0.88 |

Le refus est multiplié par ce facteur, l'accusé de réception est divisé par ce
facteur. Les autres motivations, relations, enjeux de titres et score réel de
la guerre restent applicables. Les poids admissibles gardent leurs bornes de
1 à 300. Les coefficients sont provisoires. L'accusé de réception conserve la
portée politique documentée dans les tranches précédentes.

La neutralité de deux camps ayant le même niveau de signal exprime sa limite.
Les différences d'effectifs ou de qualité entre leurs soutiens conservent leur
revue suivante. Les participants supplémentaires ne multiplient pas indéfiniment
ce bonus. Tous les participants du camp restent susceptibles de satisfaire la
recherche native, sans tronquer leur liste à un nombre arbitraire.

## Lecture, livraison et vérification

Les recherches restent dans les deux listes de participants de la guerre exacte.
La recherche des autres engagements consulte les guerres du participant, en
excluant explicitement la guerre examinée. Aucun état, participant ou interaction n'est créé. Le facteur hors tour reste
neutre à 1, tandis que les gardes originales des poids conservent leurs conditions.
Les soutiens peuvent rejoindre ou quitter la guerre et la préférence suit les
faits courants. Aucun engagement personnel n'est transmis à un héritier.

Les docs moteur générées décrivent `any_war_attacker` et `any_war_defender` en
scope de guerre, avec des personnages comme cibles. Elles décrivent aussi
`current_military_strength` en scope de personnage. Les valeurs AGOT inspectées
utilisent ces itérateurs dans des calculs de valeurs. Cette inspection confirme
les formes de source, sans démontrer leur évaluation dans ces profils.

Huit tests de source et un contrôle du kit livré couvrent tour exact, même guerre,
chaque camp, exclusion des principaux dirigeants, mort, effectif nul, neutralité,
facteurs opposés, absence de recherches d'alliés potentiels et lecture seule.
Les mutations négatives retirent les gardes ou changent les références. Une
inversion retire le facteur de chaque profil et ses deux appels pour comparer
l'intégralité du profil précédent. Les comparaisons historiques des enjeux de
titres réutilisent ce retrait séparément contrôlé. Le test entre pairs actualise
l'empreinte du fichier partagé. Les graphes d'actions et sources de gameplay
conservent leur contenu.

Les fichiers déjà livrés et attestés sont réutilisés. Le socle et PRIVATE0.0.10
correspondants conservent 35 sources de runtime. Les quatre sorties natives
restent identiques. La campagne finale doit observer poids et décisions avec
aucun soutien, soutien d'un camp ou des deux, allié non participant, autre guerre,
participant non allié, principal dirigeant seul, effectif nul ou mort. Tester
entrée et sortie de guerre, rôles changés, contexte étranger, rechargements,
fenêtres périmées, Mega Wars et coût de calcul avec de nombreuses participations.
Aucun lancement intermédiaire requis. La disponibilité et la force effective
des renforts, puis les soutiens anticipés avant déclaration et les capacités
politiques des autres décideurs restent ouverts.
