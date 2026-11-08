# Bénéficiaire des réactions politiques entre pairs

Static-checked, expérimental, **non testé dans le moteur**. Cette tranche affine
RW-004. Départ et résultat 80/80 source, 0/20 campagne finale, delta réel 0.

## Identité et moment de lecture

Le callback natif de déclaration du CB de revendication fournit éventuellement
`scope:claimant`. Le reçu original conserve cette identité avec son état connu
ou manquant. Le nouveau lecteur utilise ce reçu à travers le dossier politique
exact du lige ou du déclarant. Il vérifie le type, propriétaire, guerre, parties,
autorité, phase et rétention via `rw_dl_match_response_trigger`, puis le numéro
lié, le schéma des parties, l'état connu et l'existence d'un bénéficiaire vivant.
Les gardes de tour assurent également la guerre active et l'autorité actuelle.

Une revendication propre garde un facteur neutre de 1. Cela évite de compter une
seconde fois la relation au déclarant. Un reçu ancien sans données de parties,
un lien absent, étranger ou périmé et un bénéficiaire mort restent aussi neutres.
Aucun remplaçant, héritier ou titulaire actuel ne devient le bénéficiaire capturé.
La lecture décrit l'identité enregistrée au début de cette guerre. Elle ne
reconstitue aucune intention et ne certifie pas l'évaluation du callback en jeu.

## Préférence personnelle

Le facteur vaut initialement 1. Si le décideur est lui-même le tiers bénéficiaire,
il vaut 1.5. Sinon, sa propre opinion du tiers multiplie par 1.25 à partir de 25
ou par 0.75 à -25 ou moins. Un lien de proche parent ou d'alliance multiplie
également par 1.25, une seule fois même si les deux liens existent. Le résultat
reste entre 0.5 et 2. Ces coefficients sont un choix de conception provisoire.

Pour le lige, ce facteur multiplie la préférence d'ignorer. Son inverse entre
dans la censure et la résolution utilisée par la demande et l'intervention
native. Pour le déclarant, il multiplie le refus et divise l'accusé de réception.
Les poids admissibles conservent leurs bornes de 1 à 300. L'accusé de réception
conserve la portée définie dans AI_PEER_WAR_RESPONSES.md.

Seules les relations du décideur sont consultées. Les traits, opinions privées,
consentement et soutien militaire du bénéficiaire ne sont pas déduits. Son
identité publique ne prouve pas qu'il veut cette guerre ou qu'il y participera.

## Limites et suite

L'initialisation de la case de défi précède ce reçu. L'inspection des définitions
natives locales distingue le contexte interaction acteur/destinataire du contexte
CB avec revendiquant et titres. Aucun accès fiable au CB sélectionné dans
`starts_enabled` n'est établi ici. Les données du reçu ne sont donc utilisées
que dans les réactions après déclaration. Aucun nouveau score natif de sélection
du CB n'est ajouté. Cette frontière reste à vérifier dans la campagne finale.

La valeur et le rang des titres, l'intérêt dynastique détaillé, les chances de
victoire, les soutiens, la foi et la culture restent ouverts. Le parcours extérieur
et sa médiation conservent leur profil actuel et nécessitent leur propre lecteur
de bénéficiaire. La couverture exhaustive des traits reste ouverte.

## Livraison et vérification

Un déclencheur original en lecture seule et le profil entre pairs sont livrés
ensemble dans le socle et l'attestation PRIVATE0.0.10. Le kit compte désormais
31 sources de runtime. Les quatre sorties natives restent identiques. Le graphe
d'actions, les effets, gardes de permission, coûts, reçus, captures et cycles de
vie conservent leur contenu. Sept tests de source et un test sur le kit livré
exercent raccordement, sens opposés, neutralité, identité exacte et mutations
négatives. Ils ne simulent aucune décision CK3.

La campagne finale doit observer les poids et décisions avec un revendiquant
propre, un tiers apprécié/détesté, parent/allié et le lige bénéficiaire lui-même.
Comparer les deux décideurs, les données manquantes ou étrangères, mort,
rechargement et changements de contexte. Vérifier les coûts et résultats natifs,
le profil extérieur et le coût de calcul. Aucun lancement intermédiaire requis.
