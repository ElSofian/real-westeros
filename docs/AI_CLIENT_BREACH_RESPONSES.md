# Promesse rompue — réaction du client

## Statut et choix couverts

**Static-checked. Not engine-tested.** Le lot pondère sept choix existants du
client, avec les conditions et effets partagés joueur/IA.

| Situation | Choix du client | Base conservée |
|---|---|---:|
| Reçu de rupture d'un service contre or | Rancune | 60 |
| Même reçu | Pardonner | 40 |
| Même reçu et médiateur compétent disponible | Saisir le médiateur | 20 |
| Renonciation explicite dans la famille faveur | Rancune | 30 |
| Même renonciation | Prendre acte | 40 |
| Geste de réparation déjà proposé dans un dossier conclu | Accepter le geste | 50 |
| Même geste | Refuser le geste | 50 |

Les options de négociation monétaire et leurs montants nécessitent une revue
distincte. Le médiateur, le prestataire et le client gardent des décisions
indépendantes. Les dossiers d'affront allégué peuvent employer le même choix de
réponse à une réparation, sous leurs propres gardes de dossier et de divulgation.

## Personnalité du personnage qui réagit

Les getters natifs sont évalués sur le client qui choisit. Ils combinent les
contributions de ses traits et modificateurs. Le propriétaire de la story, le
prestataire et les proches ne remplacent pas ce décideur.

| Facteur | Calcul | Bornes |
|---|---|---|
| Rancune | 1 + vengeance / 200 | 0,25 à 2 |
| Pardon ou prise d'acte | 1 − vengeance / 200 | 0,25 à 2 |
| Compassion | 1 + compassion / 400 | 0,5 à 1,5 |
| Procédure équitable | 1 + honneur / 200 | 0,5 à 1,5 |

La compassion multiplie les réponses apaisées et divise la rancune ou le refus
d'une réparation. Le facteur d'honneur favorise la saisine seulement lorsqu'une
capacité d'exécution est attestée. Cela donne un chemin aux tendances de Juste,
Vindicatif et Indulgent, en tenant compte de leurs autres contributions natives.
Tous ces facteurs restent positifs. Aucun trait n'impose une réponse unique.

Les avis favorables envers le prestataire renforcent les réponses apaisées et
freinent la rancune. Les avis hostiles font l'inverse. La saisine conserve son
facteur existant de 2 lorsque l'opinion est négative. L'acceptation du geste conserve
ses seuils antérieurs stricts, opinion supérieure à 25 ou inférieure à −25.

Ces valeurs sont une calibration initiale choisie pour le prototype. Les
comparaisons de poids et comportements restent à valider dans le moteur.

## Conditions au moment de la rupture

Le reçu contre or enregistre désormais la capacité d'exécution avant nettoyage
du contrat. Il emploie les mêmes conditions de parties et de paiement que le
service, indépendamment de la présence d'une fenêtre de décision. Le délai expiré
ne rend donc pas automatiquement cette capacité fausse.

La renonciation faveur enregistre une capacité inconnue par défaut. Pendant la
fenêtre d'exécution, elle enregistre disponible ou indisponible à partir du
validateur existant. Hors de cette fenêtre, l'absence de capacité présente ne
prouve pas ce qui aurait été possible au moment convenu.

| Fait attesté dans le reçu privé courant | Facteur de responsabilité formelle |
|---|---:|
| Impossibilité d'exécution constatée | 0,5 |
| Refus explicite malgré une capacité attestée | 1,25 |
| Expiration imputable au prestataire selon les gardes existantes | 1 |
| Reçu ancien, absent, inconnu ou non reconnu | 1 |

Ce facteur multiplie rancune et saisine, et divise pardon ou prise d'acte.
La capacité ne prouve ni intention malveillante ni infraction. Le client peut
toujours choisir une réaction ferme ou clémente lorsque l'option est valide.
La cause détaillée d'une incapacité et sa responsabilité éventuelle restent à
examiner. L'atténuation initiale est une préférence, sans verdict d'innocence.
L'expiration ordinaire sans parties éligibles ou fonds suffisants suit déjà le
chemin d'annulation du service, avec ses conditions existantes.

Les paiements du service sont exécutés au moment de la prestation. La somme
convenue ne devient pas une perte financière lors de la rupture. Ce lot prend en
compte le soutien promis manquant et les conditions attestées, sans inventer un
débit, un dommage supplémentaire ou une sanction judiciaire automatique.

## Informations et persistance

La capacité est un instantané des conditions partagées du contrat. Elle ne lit
aucun secret ni projet caché. Les montants actuels ou l'état de guerre ultérieur
du prestataire ne servent pas à réécrire ce qui était possible lors de la rupture.
Le reçu reste soumis aux contrôles existants de client, numéro, révision, terme,
date de fin et réponse encore disponible selon la famille.

Le reçu contre or retire une ancienne capacité lors de son invalidation. Chaque
nouvelle renonciation faveur écrase explicitement l'ancien état par inconnu avant
de l'évaluer. Une ancienne sauvegarde sans capacité conserve un facteur neutre.
Les lectures de variables sont précédées de contrôles de présence.

Le geste de réparation est évalué dans sa propre affaire conclue. Un nouveau
contrat peut avoir remplacé le dernier reçu personnel du prestataire. Cette
réponse ne consulte donc pas ce reçu plus récent pour juger l'ancienne affaire.

## Contrôles et lecture trait par trait

Douze régressions couvrent le client original, les cadres incomplets ou étrangers,
la capture historique, les capacités inconnues, la distinction offre/réponse,
les cas indépendants et les directions symboliques. Les trois événements
retrouvent leurs graphes d'actions précédents après retrait des seuls poids IA.
Deux transformations réversibles sont ajoutées au relevé historique des paiements.
Le contrôle antérieur des métadonnées temporelles les inverse avant sa propre
vérification. Les anciennes empreintes et tests négatifs sont conservés.

Le lecteur privé accepte `--client-review` pour les 39 traits de personnalité
hors dragons. Il tient fixes relation, responsabilité et éligibilité, distingue
effet direct nul et revue globale incomplète, et traite la saisine dans le cas
d'une capacité attestée. Le résumé 176/3/1 033 reste celui du profil prestataire
sur honneur/avidité/énergie, distinct du profil client honneur/compassion/vengeance.

## Campagne finale

1. Même dossier et opinion, comparer vengeance, compassion et honneur du client.
2. Modifier les traits du prestataire seul et vérifier l'identité du décideur.
3. Comparer refus exécutable, refus sans moyens et expiration imputable.
4. Changer les fonds après la rupture, puis recharger. Vérifier l'instantané.
5. Renoncer avant, pendant et hors fenêtre faveur. Vérifier inconnu/disponibilité.
6. Recharger un ancien reçu sans capacité, un reçu déjà traité ou un cadre étranger.
7. Ouvrir un dossier, proposer une réparation, puis créer un nouveau contrat.
   Vérifier que l'ancienne réparation conserve son propre contexte et consentement.
8. Vérifier les réactions joueur/IA, les coûts existants et l'absence de doublons.

Qualité AI3/O1. Baseline et résultat **74/80 source, 0/20 campagne**, delta **0**.
Évaluation complète du préjudice, peur, foi, stress et négociation restent ouvertes.
