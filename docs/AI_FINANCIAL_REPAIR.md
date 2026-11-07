# Réparation financière — négocier et recevoir

## Statut et périmètre

**Static-checked. Not engine-tested.** Sept choix existants reçoivent des poids
contextuels dans le dossier privé de compensation d'un service. Les moyens de
proposer 25/50 or, accepter, contre-proposer, clôturer et réagir après paiement
restent ceux du même parcours partagé joueur/IA. Le prestataire est toujours le
payeur, même lorsque le client propose le montant.

Les bases sont conservées, proposition 25 à 2, proposition 50 à 1, acceptation à 60,
contre-offre à 10, clôture à 10, appréciation et prise d'acte à 50. Laisser reste une
sortie de poids 50. La calibration doit être confrontée aux choix et performances
réels dans la campagne finale.

## Valeur de l'offre selon le rôle

| Entrée | Payeur | Bénéficiaire |
|---|---|---|
| Avidité, montant 25 | 1 − avidité/400 | 1 + avidité/400 |
| Avidité, montant 50 | 1 − avidité/200 | 1 + avidité/200 |
| Honneur et compassion | 1 + (honneur + compassion)/400 | Aucun facteur direct sur la réception du paiement |
| Relations et coopération | Facteur partagé existant, opinion propre, souvenirs publics propres et engagements concurrents | Relations sur la demande initiale et les concessions |
| Liquidités | Fonds suffisants pour le montant, puis facteur 0,5 si trésor inférieur au double du montant | Facteur 1,25 si le montant reçu dépasse le trésor propre |

Les facteurs de personnalité sont bornés de 0,5 à 1,5. La réserve dépend donc du
montant réellement discuté, soit 50 pour 25 et 100 pour 50. Elle n'interdit aucun
paiement par elle-même. Les critères d'exécution financière restent ceux du
validateur courant, notamment le consentement du répondant et les fonds du payeur.

Le montant 50 reçoit aussi un facteur 0,75 côté payeur et 1,25 côté bénéficiaire.
Une offre impossible à financer reçoit un poids IA nul. L'acceptation utilise
le montant de la version affichée. L'or du bénéficiaire ne peut pas financer la
promesse du payeur.

## Contre-offres et concessions

Le code existant alterne 25 et 50. Le profil évalue le montant qui résulterait de
cette contre-offre, après validation de la version et du tour courant.

| Répondant | Montant affiché | Montant proposé ensuite | Sens financier propre |
|---|---:|---:|---|
| Payeur | 50 | 25 | Réduction du paiement |
| Payeur | 25 | 50 | Geste plus généreux |
| Bénéficiaire | 25 | 50 | Demande plus élevée |
| Bénéficiaire | 50 | 25 | Concession |

Une direction financièrement favorable reçoit un facteur 1,5, une concession 0,5.
La concession du bénéficiaire emploie aussi sa moindre avidité, sa compassion et
sa coopération. Une alternative qui devient finançable alors que le montant
courant ne l'est pas reçoit un facteur 2. Par exemple, un payeur possédant 30 or
peut envisager 25 face à une demande de 50. La contre-offre 50 reste sans poids si ce
payeur ne peut pas la financer.

Les révisions, réponses différées d'un jour et délai initial de sept jours
proviennent du parcours existant. Aucun nouveau rappel, renouvellement du délai
ou compteur de négociations n'est ajouté.

## Réparations antérieures et connaissance

Seul le résultat `repaired` du même dossier conclu sert d'indicateur de geste
déjà effectué. Il applique un facteur 0,75 au payeur, favorise
l'acceptabilité du montant 25 côté bénéficiaire par un facteur 1,25 et freine
par un facteur 0,5 une demande initiale ou une contre-offre du bénéficiaire vers 50. Les autres facteurs peuvent
se combiner ou se contrarier.

Les relations favorables orientent la demande initiale du bénéficiaire vers25,
les relations hostiles vers50. Une mémoire publique propre au décideur peut déjà
favoriser la coopération via le facteur partagé. Le dernier reçu personnel du
prestataire et son prix d'origine ne remplacent pas les faits du dossier actuel.
Le paiement est un geste volontaire. Le prix d'un service impayé ne devient pas
une dette ou une mesure du préjudice réel.

## Accepter le paiement et réagir ensuite

Le bénéficiaire peut accepter l'or sans facteur de pardon ou de vengeance dans
ce choix financier. Après le paiement effectif, les deux choix personnels
emploient ses tendances de vengeance et de compassion dans leur propre fenêtre.
Une relation hostile peut freiner l'appréciation. Prendre acte reste possible.

Ces réponses utilisent le reçu exact de paiement, son montant, sa révision et
sa date. Le payeur ne répond pas à sa propre générosité. Un ancien panneau ou
un dossier étranger ne peut créer une seconde transaction ou une nouvelle réponse.
Les effets de paiement et d'opinion conservent leurs preuves séparées.

## Contrôles et suite

Douze régressions couvrent les rôles, les deux montants, les sens de contre-offre,
les liquidités limites, les dossiers incomplets/périmés, les gardes de clôture,
l'indépendance de la reconnaissance et les directions par trait. Les empreintes
des deux bibliothèques d'effets sont identiques à celles d'avant ce lot. Le graphe
d'actions de l'événement retrouve aussi son empreinte après retrait des poids IA.
Les contrôles adversariaux existants sur consentement, délais et reçus restent actifs.

`--compensation-review` dans le lecteur privé donne les 39 traits de personnalité
hors dragons, séparant payeur, bénéficiaire et réaction après paiement. Montant,
moyens, relations, souvenirs et gestes antérieurs sont tenus fixes. Les contre-
offres, dont le sens dépend du rôle et du prix, demandent leur propre contexte.

Campagne finale prévue, tester les deux proposants, les deux répondants et les
deux montants. Vérifier les frontières 24/25/49/50/99/100 or, une contre-offre
moins chère devenue finançable, la guerre/détention après l'offre, une ancienne
révision, une offre expirée, un paiement déjà consommé et un bénéficiaire qui
reçoit l'or puis choisit de prendre acte. Comparer un geste antérieur réel dans
la même affaire et un geste dans une autre affaire.

Qualité AI3/N1. Baseline et résultat **74/80 source, 0/20 campagne**, delta **0**.
L'évaluation complète des enjeux, de l'urgence, de la peur et du préjudice reste ouverte.
