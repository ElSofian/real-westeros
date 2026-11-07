# Personnalité du décideur — revue des promesses

## Ce qui est examiné

Cette revue couvre les 39 traits de personnalité hors dragons du relevé installé.
Elle suit le prestataire lorsqu'il décide de tenir une promesse de soutien public
ou de rompre/renoncer. **Static-checked**. Validation moteur en attente.

Le relevé privé `--promise-review` donne les directions actuelles, trait par trait,
pour les quatre options et leurs branches de rémunération. Les questions
contextuelles ci-dessous identifient les règles encore à développer. Aucun poids
de gameplay n'est ajouté par cette revue.

## Parcours réellement consommés par les options

| Option du prestataire | Entrées actuelles | Effets après validation |
|---|---|---|
| Tenir contre or | Honneur, avidité, importance du revenu, opinion du client, dossier et capacité d'exécution | Paiement du client au prestataire, 50 prestige au client, mémoire de soutien public |
| Rompre contre or | Honneur, opinion du client, engagement courant actionnable | Reçu de rupture puis choix de réaction du client |
| Tenir dans la famille faveur | Honneur, opinion, dossier et capacité d'exécution. Avidité et revenu seulement pour le terme gold25 | Hameçon reçu par le prestataire ou paiement de 25 or, 50 prestige au client, mémoire de soutien public |
| Renoncer dans la famille faveur | Honneur et opinion si le client vit, engagement courant en attente | Reçu de renonciation et possibilité de réponse personnelle du client |

Après le décès du client, la renonciation conserve son poids neutre. L'exécution
reste soumise aux conditions de validité. Une rupture ne déclenche pas une
sanction judiciaire automatique. Une réaction future reste incertaine.

## Sens des influences actuelles

L'honneur augmente la préférence pour tenir et réduit celle pour rompre. L'avidité
augmente l'intérêt de recevoir un paiement dans les branches monétaires. Les
autres axes ne sont pas directement consommés par ces quatre nouveaux profils.

Le relevé indique hausse ou baisse possible avec neutralisation par les bornes.
Des contributions opposées à l'honneur et à l'avidité restent marquées mixtes.
Le résultat dépend du profil agrégé. Aucune probabilité n'est déduite d'une option
isolée, car attendre, amender et annuler peuvent également être proposés.

« 0 direct » est justifié uniquement pour les axes lus par l'option, à opinion,
moyens, parties et éligibilité constants. Les effets indirects restent distincts.
La couverture politique complète de chaque trait garde son état en cours.

## Revue des 39 traits

| Identifiant | Trait | Questions contextuelles et garde de conception |
|---|---|---|
| `ambitious` | Ambitieux | Examiner le gain personnel de pouvoir et l'utilité d'une faveur. Le prestige de cette exécution revient au client et ne constitue pas un gain propre du prestataire. |
| `diligent` | Appliqué | Examiner une charge de travail ou des devoirs concurrents réellement représentés. Le soutien actuel n'a aucun coût de travail explicite à inventer. |
| `arrogant` | Arrogant | Examiner rang, reconnaissance et affronts connus. Les contributions opposées d'honneur et d'avidité ne donnent pas un verdict unique sur l'exécution rémunérée. |
| `authoritative` | Autoritaire | Examiner le rôle et l'enjeu d'autorité. Une promesse privée entre dirigeants ne constitue pas automatiquement une soumission politique. |
| `brave` | Brave | Examiner un danger ou une intimidation crédible. Un service ordinaire sans danger représenté ne justifie pas de bonus universel de courage. |
| `calm` | Calme | Examiner stress réel et conséquences émotionnelles modélisées. Une exécution sans variation de stress explicite ne crée pas un coût supplémentaire. |
| `chaste` | Chaste | Aucun enjeu sexuel n'est attaché au service. Les contributions natives d'honneur restent actives, les relations pertinentes éventuelles doivent être établies. |
| `wrathful` | Colérique | Examiner affronts connus et colère envers cette personne. Le trait seul n'établit aucune offense commise par le client. |
| `compassionate` | Compatissant | Examiner aide réellement apportée et dommages prévisibles. Le nom du service ne suffit pas à établir un secours à une victime. |
| `trusting` | Confiant | Examiner la fiabilité attendue lorsqu'elle est pertinente. Le solde actuel du client et les conditions d'exécution restent vérifiés. |
| `content` | Content | Examiner engagements et intérêts présents. Un faible désir d'expansion n'annule pas l'intérêt de tenir un service déjà accepté. |
| `greedy` | Cupide | Le paiement est une recette du prestataire. L'utilité politique d'une faveur reçue reste à modéliser séparément de l'or. |
| `inquisitive` | Curieux | Examiner nouveauté et informations accessibles procurées par l'action. Le service courant ne promet aucune découverte. Distinguer cet identifiant du trait d'enfance curious. |
| `cynical` | Cynique | Examiner intérêt concret et enjeux religieux réellement présents. Le cynisme ne suffit pas à déduire un refus de toute promesse. |
| `stubborn` | Entêté | Examiner engagement pris et demande éventuelle de changement. Tenir sa promesse et refuser un nouvel accord sont deux situations différentes. |
| `eccentric` | Excentrique | Examiner préférences et circonstances connues. Aucun comportement aléatoire supplémentaire n'est introduit pour simuler ce trait. |
| `deceitful` | Fourbe | L'honneur natif influence déjà la rupture. Examiner opportunité et conséquences d'une tromperie. Le soutien est public et la rupture produit un reçu. |
| `gluttonous` | Gourmand | Aucun repas ni coût alimentaire n'est prévu. L'avidité native peut déjà agir sur la recette monétaire. |
| `rude` | Grossier | Examiner relations et portée sociale de l'acte. Le soutien ne contient aucune condition de politesse à inventer. |
| `generous` | Généreux | Le prestataire reçoit l'or. Faible avidité et honneur peuvent se contrarier. L'amendement de prix possède déjà un poids propre à revoir séparément. |
| `honest` | Honnête | La parole donnée passe par l'honneur. Confronter légitimité du soutien, devoirs concurrents et faits connus au contexte. |
| `humble` | Humble | Examiner statut et recherche de reconnaissance. Le prestige versé au client n'est pas une récompense personnelle du prestataire. |
| `impatient` | Impatient | Examiner temps restant et solutions d'attente. Renonciation anticipée et exécution devenue possible ont des calendriers différents. |
| `fickle` | Inconstant | L'honneur natif agit déjà. Examiner un objectif concurrent concret et les alternatives avant d'ajouter un motif de rupture. |
| `forgiving` | Indulgent | Examiner une faute connue à pardonner. Le prestataire qui exécute et le client qui pardonne une rupture ont des rôles différents. |
| `just` | Juste | Examiner légitimité de l'engagement et autres devoirs. Un bonus nommé supplémentaire risquerait de recompter l'honneur déjà lu. |
| `lustful` | Lubrique | Aucun objectif sexuel n'est prévu. Conserver les contributions natives et examiner seulement les relations réellement concernées et connues. |
| `craven` | Lâche | Examiner une menace crédible, sa portée et la capacité de son auteur. Le reçu de rupture ne prouve pas qu'une punition aura lieu. |
| `paranoid` | Paranoïaque | Distinguer savoir et soupçon. Une crainte ne devient pas une preuve et ne donne pas accès à un secret inconnu. |
| `lazy` | Paresseux | Examiner efforts ou contraintes représentés. Aucun coût de travail arbitraire n'est attribué à un soutien immédiat. |
| `arbitrary` | Partial | L'honneur natif agit déjà. Examiner intérêts et préférences du contexte, sans transformer le trait en rupture obligatoire. |
| `patient` | Patient | Examiner délais, urgence et option attendre. Le trait n'alimente actuellement aucun des deux axes directement lus par les quatre profils. |
| `sadistic` | Sadique | Examiner la souffrance réellement prévisible d'une personne concernée. Le soutien public ne produit pas une blessure ou une torture par lui-même. |
| `callous` | Sans cœur | Examiner dommages et intérêts d'autrui concernés. La faible compassion ne supprime pas l'intérêt personnel à tenir une promesse rentable. |
| `gregarious` | Sociable | Examiner liens et valeur sociale du soutien. L'opinion native peut déjà porter une partie de ces relations, à éviter de recompter. |
| `temperate` | Tempéré | Examiner pondération et gain réel. L'avidité native réduit l'intérêt du paiement sans établir une opposition générale au service. |
| `shy` | Timide | Examiner exposition publique et stress éventuel. Le soutien est public, un coût de stress supplémentaire reste à concevoir et à vérifier. |
| `vengeful` | Vindicatif | Examiner un grief connu envers cette personne et les réparations. Un grief envers un tiers n'est pas automatiquement un motif contre le client. |
| `zealous` | Zélé | Examiner foi, doctrine et légitimité religieuse lorsque le soutien les concerne. L'identité du client ne suffit pas à inventer un conflit religieux. |

## Influences indirectes et rôles

Les profils lisent l'opinion du prestataire envers le client. Les modificateurs
natifs des traits peuvent donc changer le résultat lorsque leurs conditions
s'appliquent à cette paire. Un effet envers le seigneur lige, les vassaux, un
trait opposé ou une culture ne s'applique pas automatiquement à tout client.
Le relevé des axes ne calcule pas ces opinions.

Les ressources sont les valeurs réelles au moment de décider. Une influence déjà
passée par les revenus ou dépenses ne doit pas être recomptée comme un transfert.
Ces profils ne lisent directement ni les six compétences, ni un âge numérique,
ni la santé, ni le stress. Leurs autres effets restent à examiner.

Le décideur est toujours le prestataire dans les quatre profils. Les réactions
du client, notamment pardonner, exprimer une rancune ou saisir un médiateur,
nécessitent une politique distincte. Les traits d'un conjoint ne remplacent pas
la personnalité du décideur.

## Âge, calendrier et suite

L'éligibilité du service emploie `is_adult`, sans fixer un âge adulte universel
dans ce profil. Elle vérifie aussi vie, terres et état de guerre. L'exécution de
la famille faveur vérifie en plus la liberté des deux parties. Rupture et
renonciation ont des conditions moins restrictives que l'exécution. Les rendre
identiques empêcherait de traiter certains engagements devenus impossibles.

Le prochain lot doit traiter le choix entre exécuter, attendre et renoncer avec
les délais réels. Conserver renégociation, engagements existants, gardes et
conséquences partagées joueur/IA. Peur, foi, stress et arbitrages globaux restent
ouverts. Les tests moteur demeurent regroupés dans la campagne finale.

Qualité AI3/O1. Baseline et résultat **74/80 source, 0/20 campagne**, delta **0**.
Cette revue apporte la traçabilité des influences actuelles et une revue de
conception de 39 traits. Leur couverture politique globale reste incomplète.
