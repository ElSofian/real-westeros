# Légitimité et stress des décisions politiques

## Barème initial du 12 novembre 2026

**Static-checked. Not engine-tested.** Baseline et résultat80/80 source,0/20
campagne, delta réel+0. Les API natives `has_legitimacy`, `add_legitimacy` et
`stress_impact` figurent dans la documentation générée de l'installation examinée.
Les effets sont partagés entre joueur et IA.

## Légitimité

| Acte propre à Real Westeros | Personne concernée | Variation |
|---|---|---:|
| Déclarer une nouvelle disgrâce publique de maison | Souverain émetteur | −10 |
| Lever gratuitement le décret d'un prédécesseur | Nouveau souverain décidant cette clémence | +10 |
| Lever gratuitement son propre décret | Auteur du décret | 0 |
| Réhabilitation négociée contre or | Souverain et pétitionnaire | 0 |
| Reconnaissance explicite d'une charte par la couronne | Chef de maison reconnu | +10, bonus annuel |
| Répudier une charte personnellement reconnue | Souverain répudiant sa propre parole | −10 |
| Répudier la charte d'un prédécesseur sans l'avoir reconnue | Successeur | 0 |
| Services, compensations et autres promesses privées | Parties | 0 |

Chaque variation exige un personnage qui utilise la légitimité native.
Les deux conséquences du décret possèdent des repères distincts dans le dossier,
consommés avant leurs effets. L'émetteur et la date de déclaration, puis l'auteur
et la date de clôture, rattachent le coût ou la récompense à son acte réel.
Le bonus de clémence exige un autre souverain que l'émetteur initial, ce qui
empêche de fabriquer un gain en alternant ses propres sanctions et retraits.

La reconnaissance utilise la couronne, la maison, le chef et la révision actuels
de la charte. Elle s'applique après acceptation explicite ou reprise volontaire
par un souverain. Son repère personnel chez le chef reconnu dure365jours et est
consommé avant le gain. La répudiation vérifie la reconnaissance personnelle du
souverain qui agit, sa clôture datée et un repère unique de conséquence.

## Stress d'une rupture personnelle

| Trait | Base de stress |
|---|---:|
| Honnête | +15 |
| Juste | +10 |
| Compatissant | +5 |
| Autres traits | 0 dans ce barème direct |

Les contributions des traits présents s'additionnent. Les modificateurs natifs
s'appliquent ensuite. Ces bases concernent les parcours suivants.

- Soutien contre or, refus explicite ou échéance manquée avec capacité d'exécution
  positivement constatée. L'impossibilité constatée utilise une base0.
- Soutien contre faveur/or, renonciation volontaire. Avant échéance, la capacité
  future reste inconnue. Une impossibilité déjà constatée au moment dû utilise0.
- Restitution personnelle promise, renonciation avec parties actuellement capables
  de participer. Cette capacité est observée avant de consommer l'engagement.
- Dotation dynastique, renonciation d'un chef ayant personnellement reconnu le pacte.
  Un successeur qui décline la parole de son prédécesseur utilise0.
- Retenue militaire, renonciation explicite après consommation de l'engagement.
- Charte institutionnelle, répudiation de sa propre reconnaissance personnelle,
  en plus de la variation de légitimité correspondante.
- Accord multiple, refus volontaire d'une clause actuellement exécutable. La
  capacité de la clause est observée avant son refus. Le coût de stress est
  appliqué une fois par personne et par accord, même si elle refuse plusieurs
  clauses de cet accord. Les personnes originales signataires restent déterminantes.

Les annulations pour incapacité, les contre-offres, le refus d'une offre encore
non acceptée et la libération consentie par le bénéficiaire utilisent0 dans ce
barème. La violation de retenue observée par un callback de guerre conserve sa
réponse politique facultative. Les conséquences de l'acte de guerre sont prises
en charge par les mécanismes natifs.

## Stress des décisions publiques

La disgrâce de maison ajoute une base+10 pour juste et+10 pour compatissant.
La clémence gratuite ajoute une base+10 pour vindicatif. Les autres traits
contribuent0 à ces deux barèmes directs. Les modificateurs natifs de stress
s'appliquent et les repères du décret protègent ces coûts contre le rejeu.

## Couverture et contexte

Les décisions de guerre et les actes judiciaires natifs emploient leurs propres
conséquences de stress, légitimité, tyrannie et opinion. Le barème ajouté porte
sur les actes originaux décrits ici. Les mémoires, sanctions familiales et droits
sur les titres gardent leurs données de domaine. Les réactions de négociation,
information et promesse restent distinctes de la preuve et de la culpabilité.

Les anciens dossiers continuent avec leurs rôles et consentements enregistrés.
Un nouvel acte reçoit ses nouvelles conséquences. Lire un dossier clos,
changer de représentant ou hériter d'une fonction conserve un coût direct0.

## Vérification et session groupée

Treize tests supplémentaires vérifient les API et bases, les actes frais, les
marqueurs avant effet, la disponibilité native de la légitimité, le destinataire
d'une reconnaissance, la clémence d'un prédécesseur, le consentement personnel
avant rupture, les capacités connues et le coût unique d'un accord multiple.
Les tests antérieurs et l'inversion des reçus de débit restent exécutés.

Dans CK3, comparer les personnages avec/sans légitimité et avec/sans les traits
cités. Relever les compteurs avant/après chaque acte et rejouer ses anciennes
fenêtres après sauvegarde. Tester le dirigeant original, un successeur sans
reconnaissance et un successeur ayant accepté personnellement la promesse.
Tester les trois refus d'un accord chez la même personne, une incapacité de payer,
un délai expiré, une révocation du décret par son auteur et par son successeur,
une réhabilitation payante et deux reconnaissances rapprochées du même chef.

## Candidat du premier jour

Les corrections de la revue sont couvertes en source par
[le suivi de paix](PEACE_DEMAND_REVIEW.md),
[le soutien et les promesses](SUPPORT_REWARD_BALANCE.md),
[les contributions institutionnelles](INSTITUTIONAL_CONTRIBUTIONS.md)
et le présent barème. Les montants constituent la première calibration du candidat.
La session groupée du deuxième jour confronte les huit systèmes à leurs entrées
réelles dans CK3 selon [FINAL_ENGINE_TESTS.md](FINAL_ENGINE_TESTS.md). Les résultats
orientent les corrections du troisième jour et la partie jouable visée. Les
critères moteur V1–V5 conservent leurs exigences de preuve reproductible.
