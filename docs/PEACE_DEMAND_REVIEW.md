# Suivi d'une demande politique de paix

## Correctif du 12 novembre 2026

**Static-checked. Not engine-tested.** Le choix de réception d'une demande de paix
conserve désormais une dernière décision discrétionnaire de son autorité.
Baseline et résultat 80/80 source, 0/20 campagne, delta réel +0.

Le parcours concerne les pairs d'un même seigneur direct et les réponses
extérieures d'une déclaration sous interdiction territoriale. Après réception
courtoise ou refus, une décision de l'autorité est proposée le lendemain. Après
sept jours sans réponse, un callback unique propose cette même revue. Elle utilise
le dossier, les rôles et la guerre d'origine.

La réponse originale est conservée dans le dossier. L'autorité peut tolérer,
censurer ou choisir une voie d'intervention disponible. Le suzerain déclarant
conserve la demande native d'arrêt de guerre sous ses gardes existantes. Le
protecteur extérieur conserve la médiation consentie. Les coûts, réponses et
résultats de ces voies sont ceux de leurs mécanismes respectifs.

## Limites et durée

Une seule demande est permise dans ce dossier. Une fois le dernier choix proposé,
les possibilités de renvoyer la demande sont fermées. La dernière fenêtre est de
sept jours, sous le plafond initial de quatorze jours. Une guerre terminée, une
autorité remplacée ou un rôle devenu invalide ferme les possibilités d'action.
Les callbacks périmés et les anciennes fenêtres échouent sur les mêmes gardes.

Les réponses du premier tour conservent leurs effets d'opinion. Un refus coûte
−15 auprès du suzerain déclarant et −10 auprès du protecteur extérieur. Une
censure décidée ensuite ajoute sa désapprobation de −10. L'autorité peut aussi
tolérer la conduite. Le traitement natif peut produire ses propres conséquences.
Ces cumuls sont à observer dans la campagne groupée.

Les anciens dossiers de pairs encore répondables utilisent leur délai total
existant. Les anciens dossiers extérieurs reçoivent, à leur première demande ou
réponse après mise à jour, une fenêtre de revue unique de sept jours. Un numéro
de schéma distingue cette migration d'un délai moderne expiré. Les dossiers déjà
fermés restent des reçus historiques.

## Vérification

Huit tests ciblés supplémentaires couvrent identité, échéance, non-renouvellement,
réponse consommée avant revue, silence, absence d'exécution automatique, conservation
des gardes natives et migration des dossiers extérieurs. Le contrôle du chemin
assemblé réutilise les contrats de réponse étendus. Les instantanés des actions et
gardes sont actualisés pour cette modification explicite. Les fonctions natives
d'intervention gardent leurs instantanés existants.

En campagne, exécuter réception/refus/silence avec guerre active, accepter ou
refuser le dernier choix, vérifier la clôture sans boucle, puis tenter une ancienne
fenêtre après paix, succession et rechargement. Contrôler les coûts natifs et les
opinions avant/après chaque étape chez joueur et IA. Inclure un protecteur extérieur
et un ancien dossier encore en attente.
