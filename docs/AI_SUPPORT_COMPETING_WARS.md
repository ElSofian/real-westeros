# Autres guerres des soutiens déjà engagés

Tranche RW-004 du 8 novembre 2026. **Static-checked**, expérimentale,
**non testée dans CK3**. Départ et résultat 80/80 source et 0/20 campagne finale.
Delta réel 0.

## Fait observé et portée

Le signal de soutien des réponses du déclarant tient désormais compte des autres
guerres de ses participants secondaires, dans les parcours entre pairs et
extérieur. Les gardes du tour, de la guerre exacte et des participants vivants
avec effectif courant positif restent requises. Les principaux dirigeants de
chaque camp restent exclus de ce signal.

Pour chaque camp, le lecteur cherche si au moins un de ces participants n'est
impliqué dans aucune autre guerre. La guerre examinée est explicitement exclue
par identité de la recherche des autres guerres du personnage. La présence d'un
seul soutien admissible sans autre conflit suffit au signal plein, même si ses
compagnons sont occupés ailleurs.

Si tous les soutiens admissibles du camp participent aussi à une autre guerre,
le signal est réduit. Il reste positif. Une autre guerre exprime un risque de
dispersion et ne prouve pas que toutes les forces du personnage sont indisponibles.
Les autres guerres peuvent notamment concerner des fronts proches ou des conflits
liés par Mega Wars. Cette interprétation reste à observer en campagne finale.

## Coefficients provisoires

Le signal d'un camp vaut 1 sans soutien admissible, 1.25 avec au moins un soutien
sans autre guerre et 1.1 lorsque tous ses soutiens ont un autre engagement natif.
Le facteur global vaut signal attaquant / signal défenseur, borné à 0.8..1.25.
Le refus du déclarant multiplie ce facteur et l'accusé de réception le divise.
Le tableau complet est actualisé dans AI_COMMITTED_WAR_SUPPORT.md.

Deux camps de même niveau de signal donnent 1. Un camp attaquant sans autre guerre
face à des défenseurs tous impliqués ailleurs donne environ 1.136. Le cas inverse
donne 0.88. Ces coefficients sont provisoires. Les autres motivations, le score
de guerre et les enjeux des titres restent applicables. La portée politique de
l'accusé de réception et les bornes des poids restent celles du parcours existant.

Ce signal reste une appréciation de participation et de concurrence entre guerres.
La mobilisation des armées, leur position, leurs itinéraires, le rapport réel
d'effectifs sur ce front, les transports, ravitaillement, qualité et dragons
restent à approfondir. L'absence d'une autre guerre ne suffit pas à prouver
l'arrivée immédiate des renforts.

## Source et vérifications

Les docs moteur générées décrivent `any_character_war` depuis un personnage vers
des guerres. Ce même itérateur sert déjà aux gardes d'une guerre exacte dans le
parcours natif privé. Les recherches restent dans les participants de la guerre
examinée et dans leurs propres guerres. Aucun état, participation ou interaction
n'est modifié. Le coût de ces recherches imbriquées reste à mesurer dans CK3.

Les huit régressions de présence sont adaptées au raffinement de disponibilité.
Quatre régressions supplémentaires couvrent l'exclusion de la guerre examinée,
le signal réduit conservé pour les soutiens occupés, la répétition des gardes
d'admissibilité et le fait qu'un seul soutien sans autre guerre suffit. Le test
du kit livré ajoute une mutation de l'identité de la guerre exclue. Les profils
historiques hors facteur de soutien et ses deux appels gardent leur comparaison
inchangée. Les invariants de titres et la copie du fichier partagé sont vérifiés.

Les deux facteurs de soutien existants seuls sont affinés. Les autres poids,
graphes d'actions, effets, permissions, cycles et sorties natives conservent leur
contenu. Les fichiers attestés sont réutilisés. Le socle et PRIVATE0.0.10
correspondants conservent 35 sources de runtime.

La campagne finale doit comparer aucun soutien, soutien sans autre guerre, tous
occupés, mélange avec un seul soutien sans autre conflit et camps asymétriques.
Inclure autre guerre du principal dirigeant seul, soutien mort ou sans effectif,
allié non participant et engagement dans une autre guerre sans participation à
celle-ci. Faire rejoindre ou quitter une autre guerre, puis recharger et vérifier
les poids, décisions et coûts natifs. Contrôler Mega Wars, fenêtres périmées,
identités étrangères et coût sur de grandes listes de participants et guerres.
Aucun lancement intermédiaire requis. Le déploiement et la force effective des
renforts, puis les soutiens anticipés et les capacités des autres décideurs
restent ouverts.
