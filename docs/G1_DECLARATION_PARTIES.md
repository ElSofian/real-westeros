# Parties et titres d'une guerre de revendication

Tranche de la revue de fond du 7 novembre 2026. **Static-checked** et expérimentale,
**non testée dans CK3**. Baseline et résultat80/80 source,0/20 campagne, delta0.

## Rôles conservés

Dans le cas Leyton–Dayne, la future réponse politique doit connaître les rôles
effectifs de la guerre et des titres visés. La source native distingue déjà le
défenseur principal des vassaux dont les titres sont ciblés. Le bénéficiaire
d'une revendication peut également être une autre personne que l'attaquant.

Le relevé précoce du vrai `claim_cb` conserve désormais des faits supplémentaires.

| Fait | Source de la capture |
|---|---|
| Attaquant et défenseur principaux | Scopes natifs du callback, déjà enregistrés |
| Autorité directe de l'attaquant | Suzerain et titre d'autorité, déjà enregistrés |
| Suzerain direct du défenseur | Référence observée si elle existe |
| Bénéficiaire de la revendication | `scope:claimant` si le moteur le fournit |
| Chaque titre ciblé | Itérateur `every_target_title` du CB de la guerre exacte |
| Détenteur du titre | Détenteur observé à la capture, ou état manquant |
| Suzerain du détenteur | Référence observée, accompagnée de son titre principal s'il existe |

Le parcours source utilise la relation guerre → CB → titres ciblés documentée
par le moteur et les scripts natifs inspectés. Il conserve tous les titres
fournis. Il crée un fait personnel par titre, lié au relevé de loi parent par
propriétaire, numéro et guerre. Le titre conserve ainsi son propre détenteur.

Ces références permettent de distinguer un défenseur principal Doran d'un
détenteur Dayne, si ce sont les rôles réellement fournis par le moteur. La
capture n'attribue aucun de ces rôles à partir d'un nom, d'un lien familial ou
du seul titre principal du défenseur.

## Données absentes et capture partielle

`rw_dl_party_schema=1` identifie la nouvelle capture de parties. Le bénéficiaire
possède un état `known` ou `missing`. Chaque fait de titre conserve également
l'état de son détenteur. Les alias de détenteur, suzerain et titre d'autorité
sont effacés avant chaque titre pour éviter de réutiliser une valeur précédente.

Le relevé parent compte les titres parcourus et les faits effectivement créés.
L'état de la liste peut être `unavailable`, `partial` ou `all_titles_recorded`.
Ce dernier décrit l'enregistrement des titres. Un détenteur ou bénéficiaire
peut toujours être manquant et conserver cet état explicite.

Le marqueur de début est consommé avant le parcours. Une nouvelle invocation
ne remplace aucun fait par un détenteur apparu plus tard. Le travailleur exige
un relevé personnel de même schéma, numéro positif, guerre, attaquant, défenseur,
phase précoce et date courante. Les anciens parents dépourvus de ce nouveau
schéma de parties restent sans cette capture. La déduplication du relevé de loi
empêche également une nouvelle capture par un callback répété.

## Conservation et couverture actuelle

Les faits de titres appartiennent à l'attaquant initial. Ils se terminent à son
décès. Leur entretien mensuel exige un parent encore existant, de même type,
propriétaire, numéro et guerre. La fin du parent entraîne donc leur nettoyage
au prochain entretien. Le parent garde sa politique de rétention actuelle.

Ces données constituent la première liaison des rôles nécessaire au parcours
inter-seigneuries. La liaison à l'initiateur de l'interaction native, l'ouverture
du défi extérieur et les réponses de Mace/Doran restent des tranches suivantes.
L'option de défi et les réponses existantes conservent leur périmètre actuel.
Le nouveau travailleur intervient dans la capture du callback et conserve les
définitions natives du CB. La disponibilité et les valeurs effectives des
références dans ce callback restent à valider dans CK3.

## Vérifications et campagne groupée

Huit régressions source couvrent le parent exact, les données manquantes,
l'absence de substitution du bénéficiaire par l'attaquant, le rejeu, les alias
périmés entre titres, la capture partielle et la durée de vie des enfants.
Les tests de loi et des premiers compteurs restent applicables.

Dans CK3, comparer revendication personnelle et pour un tiers, un ou plusieurs
titres, détenteurs différents et défenseur principal supérieur au détenteur.
Inspecter les identités, compteurs et états manquants, puis changer un détenteur
et recharger pour vérifier l'immuabilité. Tester parent supprimé, décès et guerre
longue. Mesurer le coût avec de nombreuses cibles et guerres IA. Aucun résultat
de performance ou d'exécution moteur n'est établi par les tests source.

Les sources primaires inspectées sont AGOT `common/character_interactions/00_war.txt`,
`common/casus_belli_types/00_claim.txt` et le fichier moteur généré `effects.log`.
Ce dernier documente `every_target_title` depuis un scope `casus_belli` vers des
`landed_title`. Les entrées natives du générateur restent les quatre sources
épinglées existantes. Les treize fichiers runtime originaux restent les mêmes.

| Primary source | SHA256 |
|---|---|
| AGOT war interaction | `07c93240045371d3ede417e59607a08e36e331ca995bf448a439cff76233147e` |
| AGOT claim CB | `deb9a27936f27fbb930de372d146122192612ec7e2479df9ba080382e3faf7b2` |
| Engine-generated effects.log, every_target_title at12271 | `83bec80303576bc4b3bc3180ce23044a64f16215da4f604081cebedf81fcd05b` |
