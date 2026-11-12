# Contributions financières entre maisons

## Barème du 12 novembre 2026

**Static-checked. Not engine-tested.** Baseline et résultat80/80 source,0/20
campagne, delta réel+0. Les contributions institutionnelles de réhabilitation
négociée et de dotation dynastique utilisent un montant fixé lors de l'offre.

| Plus haut rang CK3 du payeur initial | Contribution |
|---|---:|
| Sans terre, baron ou comte | 50 or |
| Duc | 100 or |
| Roi | 200 or |
| Empereur | 400 or |

La réhabilitation utilise le chef pétitionnaire comme payeur initial. La dotation
utilise le contributeur qui propose l'engagement. Le rang interne de CK3 détermine
le montant, avec les intitulés propres à AGOT dans l'interface.

Le montant est stocké dans le dossier avant la présentation de l'offre. Il figure
dans la fenêtre avant acceptation. La validation des fonds, le débit et le crédit
utilisent tous ce même nombre. Une reconnaissance ultérieure, un changement de
rang ou l'intervention d'un successeur conservent le montant accepté. Les anciennes
offres de50or gardent leur validité sous leurs gardes de parties et d'échéance.
Chaque règlement consomme l'offre ou la promesse avant le transfert.

Les quatre valeurs admises sont50/100/200/400. Une valeur altérée à zéro, négative
ou extérieure à ce barème échoue sur la validité du dossier. Les parties gardent
leurs choix explicites d'acceptation, refus, renonciation et libération.

Les services et compensations personnels utilisent leurs montants négociés25/50or.
Le présent barème porte sur la réhabilitation d'une maison et la dotation entre
maisons. Il reste une première calibration à confronter à l'économie d'AGOT.

## Contrôles et campagne

Huit tests supplémentaires vérifient le rang du payeur, le gel de la somme,
la prise en charge des anciens montants, les valeurs invalides, les fonds,
l'égalité débit/crédit, l'absence de nouveau calcul au paiement et les quatre
présentations FR/EN. Les contrats existants conservent les contrôles d'identité,
consentement, succession, échéance et rejet des anciennes fenêtres.

Les corrections enregistrées du débit d'or restent vérifiables par inversion
exacte des changements ajoutés au reçu historique. Les tests de métadonnées
antérieures inversent les ajouts ultérieurs avant leur comparaison.

En campagne, proposer et accepter chaque montant chez joueur et IA. Tester un
ancien dossier50or, des fonds inférieurs à la somme, un changement de rang entre
proposition et acceptation, le remplacement d'un chef, l'accord personnel d'un
successeur, le paiement effectif, son rejeu et le rechargement. Relever les deux
trésoreries et l'offre affichée avant/après. Évaluer aussi le poids de400or chez
les grands seigneurs pour calibrer cette première version.
