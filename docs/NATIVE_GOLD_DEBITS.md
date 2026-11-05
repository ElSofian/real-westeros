# Correction des débits d'or natifs

**5 novembre 2026 — source corrigée, aucun test moteur.** Développement64/80,
validation CK3 0/20, total64/100, **+0** : correction de fonctionnalités déjà
créditées, pas achèvement de J4/J5 ou d'un autre critère ouvert.

## Défaut et correction

Onze chemins de paiement utilisaient une addition négative pour débiter le payeur.
Cinq étaient des littéraux (`add_gold` négatif), six des blocs de prix négativés.
Le validateur libre [ck3-tiger v1.19.0](https://github.com/amtep/tiger/releases/tag/v1.19.0),
qui annonce CK3 1.19.0 comme cible, exige une valeur non négative pour `add_gold`.
Les sources AGOT reçues utilisent `remove_short_term_gold` pour le débit puis
`add_gold` pour le crédit, notamment dans `events/single_combat_events.txt`.
Les empreintes et positions sont dans GOLD_DEBIT_SOURCE_RECEIPT.json.

La correction remplace chaque débit par `remove_short_term_gold` avec **le même
montant positif**. Les crédits au bénéficiaire restent inchangés. Ni la proposition,
ni la contre-offre, ni l'acceptation d'une promesse différée ne paient à l'avance.
Les conditions de consentement, les versions, les fonds actuels, la consommation
avant paiement, les hooks alternatifs et les destinataires restent identiques.
Les onze fichiers se restaurent octet pour octet en inversant le seul débit :
le reçu conserve leurs empreintes avant/après et la substitution exacte.

| Chemin | Débit corrigé |
|---|---|
| Service immédiat et promesse de service | Prix accepté de l'instantané ; deux chemins |
| Service contre faveur, immédiat et différé | 25 or, uniquement dans la branche or ; deux chemins |
| Compensation privée d'affaire | Prix accepté |
| Retrait négocié d'allégation | Prix accepté |
| Compensation de charte de restitution | Prix accepté |
| Accord à plusieurs actions | Prix accepté de la clause financière |
| Engagement dynastique | 50 or au bénéficiaire actuel reconnu |
| Conditions de réhabilitation politique | 50 or au souverain ayant proposé les conditions |
| Réponse personnelle au complot | 25 or au demandeur désigné |

Le reçu de télémétrie du paiement multi-action doit aussi avancer : son hash
normalisé change à cause de cette correction de gameplay, pas à cause du logger.
`TELEMETRY_HOOKS.json` conserve le commit initial, l'ancienne empreinte et une
révision explicite de ce seul fichier. Les appels d'observation et le logger
restent identiques ; la vérification de non-interférence reste obligatoire.

## Contrôles sans CK3

`python tools/validate_mod.py` refuse désormais les montants littéraux négatifs
pour les effets d'ajout/retrait, les blocs négatifs simples et le motif simple
`value = prix ; multiply = -1` utilisé pour ces débits. Commentaires et chaînes
sont ignorés ; les numéros de ligne sont conservés. **Ce n'est pas un évaluateur
général d'expressions** : les valeurs référencées et les formules complexes
restent à vérifier avec les définitions réelles. Le contrôle s'applique aussi au
ZIP extrait grâce au validateur autonome déjà distribué ; aucun binaire ou
service externe n'est requis dans la CI.

Les tests conservent les mutations de consentement/fonds/version/rejeu/direction,
contrôlent explicitement le débit avant le crédit et les deux opérations exactement,
et reconnaissent le retrait comme opération d'argent interdite aux propositions,
refus, lectures et entretiens. Dix tests supplémentaires couvrent les formes
négatives, les exclusions lexicales, les emplacements, la validation intégrée,
l'inversion des onze corrections et l'avance auditable du reçu de télémétrie.

Le binaire Tiger reste hors dépôt ; son archive correspond au digest publié par
GitHub, épinglé dans le reçu. Le passage utilise **des sources privées partielles**,
pas une installation : fichiers manquants, répertoires/signature de fixture et
métadonnées synthétiques sont explicitement identifiés. Les cinq alertes ciblées
sur les littéraux passent de cinq à zéro. Les six prix calculés ont été trouvés
par examen du code RW, pas par cette sortie du validateur. Les autres alertes de
ce passage restent à trier ; aucune déclaration de validation sémantique complète.
Ni les sources CK3/AGOT, ni leur rapport brut privé, ni Tiger ne sont distribués.

## Campagne finale maintenue

Vérifier dans les scénarios de paiement existants : solde du payeur avant/après,
solde du bénéficiaire, montant convenu 25/50, insuffisance de fonds, branche hook
sans or, callback répété/rechargement et parcours IA↔IA. Vérifier aussi les budgets
natifs à court terme et l'absence de dette introduite. Grouper avec les scénarios
existants, sans relancement par paiement (démarrage CK3 7–10 minutes).
Le correctif ne démontre ni les soldes réels, ni une transaction moteur atomique.

Suite utile : trier les alertes de localisation/scopes dans leur contexte réel,
puis corriger uniquement les erreurs confirmées ; conserver les dépendances de
sanction/restauration et les critères de guerre ouverts, sans variantes de journal.
