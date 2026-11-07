# Promesses — agir, attendre et échéances

## Statut et périmètre

**Static-checked. Not engine-tested.** Cette extension ajoute l'énergie native
et un repère temporel propre à chaque engagement aux préférences du prestataire.
Elle couvre les services contre or et les promesses contre faveur ou gold25.
Les cas CK3 sont regroupés dans la campagne finale.

Le décideur conserve ses possibilités d'exécuter, attendre, renoncer, amender ou
demander une libération selon les gardes existantes. L'IA et le joueur utilisent
les mêmes conditions et effets. Les poids concernent les préférences de l'IA.

## Personnalité et choix

L'énergie est une tendance native agrégée du personnage. Les traits qui la
modifient peuvent ainsi influencer ces choix, au-delà de Patient et Impatient.

| Préférence | Calcul | Bornes |
|---|---|---|
| Agir maintenant | 1 + énergie / 200 | 0,5 à 1,5 |
| Différer | 1 − énergie / 200 | 0,5 à 1,5 |

Ces facteurs sont des choix de conception modérés, à confronter au moteur et à
la campagne de validation. L'honneur, l'avidité dans les branches monétaires,
l'opinion du client et les moyens continuent d'intervenir.

Dans le relevé installé, Patient apporte −10 à l'énergie et Impatient +10.
En tenant les autres entrées fixes, cela donne respectivement 0,95/1,05 pour
agir/différer et 1,05/0,95. Le profil agrégé du personnage peut modifier ou
neutraliser ces influences. Aucune probabilité d'action n'en est déduite.

## Échéances et occasions réelles

| Famille | Calendrier existant | Nouveau repère de préférence |
|---|---|---|
| Or, délai de 14 jours | Première décision au jour 8, attente de 7 jours, échéance au jour 14 | Réserve d'attente jusqu'au jour 7. Dès sa disparition, un nouveau rappel de 7 jours atteindrait ou dépasserait la limite |
| Or, délai de 30 jours | Première décision au jour 8, attentes de 7 jours, échéance au jour 30 | Réserve d'attente jusqu'au jour 23, puis même avertissement |
| Faveur/gold25 différé | Deux occasions fixes aux jours 8 et 22, exécution avant le jour 30 | Repère de prochaine occasion jusqu'au jour 22. Au dernier rappel, laisser le dossier en attente ne programme aucune nouvelle occasion |

Quand l'occasion est urgente et le service actuellement exécutable, le poids
d'exécution reçoit un facteur 1,5 et celui d'attente un facteur 0,25. L'urgence
n'ajoute aucun facteur à la rupture ou à la renonciation. Ces choix restent
pondérés par l'honneur et les relations, avec leurs conditions existantes.

Si le service est inexécutable, aucune pénalisation temporelle de l'attente n'est
appliquée. L'exécution garde son poids nul. Un client sans fonds, un hameçon
indisponible ou une partie inéligible ne devient pas éligible par préférence.

L'option laisser de la famille faveur garde un poids de sortie de 30 hors promesse
courante du prestataire. Dans une promesse courante, son facteur de délai est
appliqué. Cela préserve la sortie des offres et des vues anciennes ou terminales.

## Persistance et anciennes sauvegardes

À l'acceptation, chaque famille enregistre le numéro du contrat et un indicateur
temporaire de réserve d'attente ou de prochaine occasion. Les profils vérifient
le dossier complet, l'identité courante, l'état actionnable et ce numéro avant
d'interpréter l'expiration de l'indicateur comme une urgence.

Une ancienne sauvegarde sans numéro temporel conserve une urgence neutre.
Aucun calendrier n'est reconstruit depuis une consultation tardive. Un numéro
étranger échoue au contrôle. Une renégociation de prix garde la date d'origine
et son numéro de contrat. Toute future modification de délai devra actualiser
explicitement cette horloge.

La clôture retire ces métadonnées. La création d'une nouvelle offre faveur retire
aussi les restes éventuels d'un ancien créneau expiré. Les numéros sont lus
seulement après vérification de leur présence. Aucun nouveau rappel, événement
périodique ou parcours de toutes les paires de personnages n'est ajouté.

## Traçabilité et contrôles

Le lecteur privé est actualisé pour les trois axes consommés et les six choix.
Sur les mêmes 1 212 définitions installées, 176 ont une contribution directe
non nulle, 3 une contribution conditionnelle/non résolue et 1 033 une entrée
directe nulle sur ces trois axes. Les anciens comptes 84/2/1 126 décrivent le
premier profil honneur/avidité. La revue politique complète demeure en cours.

Sept nouvelles régressions vérifient les facteurs opposés, les gardes contre les
dossiers périmés ou étrangers, les horloges 7/23/22 jours, l'exécution impossible,
la sortie sûre et le nettoyage. Un contrôle inverse retire les seules métadonnées
et retrouve les empreintes des quatre fichiers d'effets précédents. Les graphes
d'actions des événements, après retrait des seuls poids IA, gardent leurs preuves
existantes. Ces contrôles n'émulent pas le moteur.

Les sources natives privées inspectées confirment le getter `ai_energy`, son
emploi dans les script values et les indicateurs de personnage temporaires.
Leur existence ne prouve pas le comportement temporel de cette extension.

## Scénarios pour la campagne finale

1. Comparer deux profils d'énergie à dossier, moyens, opinion et calendrier égaux.
2. Or14, jour8. Vérifier le poids urgent, puis la possibilité de choisir attendre.
3. Or30, jours8/22/23/29. Vérifier le passage du repère et la limite finale.
4. Faveur/gold25, jours8/21/22. Comparer prochaine occasion et dernier rappel.
5. Retirer les fonds ou rendre la faveur indisponible. Vérifier exécution nulle
   et absence de réduction temporelle de l'attente.
6. Recharger une sauvegarde antérieure sans métadonnées, un vieux dossier, une
   autre partie ou un engagement remplacé. Vérifier l'urgence neutre.
7. Amender le prix, recharger, exécuter, renoncer et laisser expirer. Contrôler
   le calendrier d'origine, le nettoyage et l'unicité des effets natifs.

Cible AI3/O1. Baseline et résultat **74/80 source, 0/20 campagne**, delta **0**.
La validation des durées exactes et de l'ordre expiration/rappel reste moteur.
