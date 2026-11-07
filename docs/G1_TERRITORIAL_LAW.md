# Portée territoriale des interdictions de guerre

**Extension de contexte du 7 novembre 2026.**
[G1_DECLARATION_PARTIES.md](G1_DECLARATION_PARTIES.md) ajoute la capture du
bénéficiaire natif et des détenteurs de tous les titres ciblés, avec leur suzerain
observé. Ces nouvelles références sont non testées dans CK3. La liaison à
l'initiateur de l'interaction et les réactions inter-seigneuries restent à développer.
Baseline/résultat80/80 source,0/20 campagne, delta0.

Première tranche de la revue de fond du 7 novembre 2026. Baseline et résultat
**80/80 source, 0/20 campagne**, delta **0**. Extension expérimentale du relevé
de loi, **non testée dans CK3**.

## Règle retenue avec le propriétaire

Chaque échelon applique ses règles à son propre périmètre. Les interdictions du
roi concernent les actes relevant de son autorité directe. Mace possède ses
propres règles pour ses vassaux. Les compétences d'intervention, demandes d'aide
et arbitrages constituent un autre volet du dossier politique. Le propriétaire
a écarté la proclamation royale de paix générale du périmètre actuel.

Le helper natif inspecté distingue l'interdiction interne entre personnages de
même suzerain direct et l'interdiction de toutes les guerres du déclarant. Il
conserve notamment l'exception contractuelle et les autres conditions natives.
La capture RW conserve le résultat de ce helper intégral sous ses alias propres.

| Règle du suzerain du déclarant | Même suzerain direct pour les deux chefs de guerre | Suzerains directs différents |
|---|---|---|
| Aucune de ces interdictions | Aucune interdiction relevée par RW | Aucune interdiction relevée par RW |
| Guerres internes interdites | Interdiction interne applicable | Interdiction interne hors de ce périmètre |
| Toutes les guerres interdites | Interdiction totale applicable | Interdiction totale applicable |

Ces lignes décrivent les drapeaux d'interdiction observés. Le helper natif fournit
ensuite son résultat d'autorisation avec ses exceptions. Les autres conditions
de déclaration et du vrai CB continuent leur traitement natif.

Pour l'exemple Leyton–Dayne, les règles du suzerain du déclarant servent à examiner
sa déclaration. Les règles de Doran prennent leur sens pour les déclarations de
ses propres vassaux. Son rôle de protecteur du seigneur attaqué sera examiné dans
la réponse politique. Une sollicitation du roi aura son propre contexte.

## Adaptation du relevé

La capture reste dans le préfixe du vrai `claim_cb.on_declaration`. Elle accepte
désormais des chefs de guerre féodaux de suzerains différents, ainsi qu'un
défenseur indépendant. L'attaquant doit toujours être un vassal féodal avec un
suzerain direct vivant, titré et un titre d'autorité existant. Les autres gardes
du callback et des identités sont conservées.

Le champ optionnel `rw_dl_peer_relation` fige la relation reçue dans ce callback.

- `same_liege` exige un suzerain du défenseur présent et égal à celui de l'attaquant.
- `different_liege` décrit les autres cas pris en charge.

Ce champ décrit une relation de suzeraineté entre les chefs de guerre observés.
Les frontières géographiques, le détenteur du titre visé, le bénéficiaire de la
revendication et l'initiateur d'une demande sont des informations distinctes.
Si le moteur attribue d'autres rôles, le relevé suit les scopes réellement reçus.
Une association supplémentaire à Leyton, aux Dayne ou aux titres visés exige une
liaison démontrée dans la future intégration inter-seigneuries.

Le champ optionnel `rw_dl_rule` conserve la règle du suzerain observée, avec
les valeurs `none`, `internal` ou `all`. Le champ `rw_dl_ban` conserve ensuite
l'interdiction applicable à cette guerre. Les anciennes archives peuvent avoir
ces nouvelles métadonnées absentes.

La lecture conserve sa priorité pour l'interdiction totale. Elle relève une
interdiction interne seulement avec `same_liege`. Ainsi une interdiction interne
hors périmètre conduit à `ban=none` et, si le helper ne demande aucune autorisation,
à `gate=no_ban`. Le relevé évite de présenter cette situation comme une exception
à une interdiction applicable. Les branches d'incohérence restent conservatrices.

La seule autorité de loi lue par RW est le suzerain direct de l'attaquant observé.
Les conditions de capture n'interrogent aucune chaîne de seigneurs supérieurs ni
la loi du défenseur pour qualifier la déclaration. Le helper natif reste conservé
par inversion de ses octets et s'exécute dans ses propres règles.

## Compatibilité et limites

Les anciens relevés conservent leur schéma et leur contenu. Leur champ de relation
peut être absent. La liaison et la lecture des dossiers existants gardent leurs
gardes historiques, sans nouvelle exigence sur ce champ. La déduplication interdit
une capture de remplacement pour une guerre déjà enregistrée.

L'option de défi et l'entrée des réponses royales conservent leur périmètre de
deux vassaux du même suzerain direct. Le nouveau relevé prépare la qualification
des autres guerres natives effectivement déclarées. La voie complète de défi
extérieur, les réponses de Mace et Doran et le recours à un supérieur commun
restent les prochaines tranches à développer. La génération et la lecture source
ne démontrent aucun nouveau comportement moteur.

## Vérifications et campagne

Cinq régressions source couvrent le contexte de capture élargi, l'unique archive
de la relation, le retrait ou l'inversion du périmètre interne, la priorité de
l'interdiction totale et le maintien du périmètre des réponses existantes.
Les cas à exécuter dans CK3 compareront même suzerain, branches différentes et
défenseur indépendant, sous chaque combinaison d'interdictions. Vérifier les
exceptions natives, les rôles effectifs, une loi royale différente de celle de
Mace, l'absence du nouveau champ sur un ancien relevé et le rechargement.
