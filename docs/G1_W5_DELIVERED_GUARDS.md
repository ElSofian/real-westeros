# W5 — Gardes du parcours intégré livré

Revue du 7 novembre 2026. W5 qualifie les gardes et contrôles négatifs du parcours
intégré après W1/W2/W4. Développement **78 → 80/80**, campagne finale **0/20**,
delta **+2**. Le barème et ses checkpoints antérieurs sont conservés.

## Chemin évalué

Le ZIP public contient le mod original et ses générateurs. L'assemblage de campagne
vérifie ce ZIP puis lit les sources AGOT locales épinglées pour générer les trois
adaptateurs privés. La voie guerre utilise `rw_g1_native_choice`, avec le vrai
`declare_war_interaction`, le vrai `claim_cb`, le helper natif conservé et la
réponse native du suzerain. Les commandes console et anciens probes demeurent
des diagnostics séparés. Le dossier préparé déclare son ordre de chargement.

Les tests d'assemblage utilisent les trois vrais générateurs et les fichiers RW
issus d'un ZIP construit depuis un commit de fixture. Leurs entrées natives sont
des fixtures synthétiques originales, avec empreintes substituées uniquement
dans le test. La génération avec les sources natives installées est vérifiée
séparément. Ces opérations préparent des fichiers pour la campagne CK3.

## Matrice de couverture source

| Partie du chemin | Refus et conservation contrôlés | Tests principaux |
|---|---|---|
| Option native | Défi explicite, hameçon exclu, même admissibilité joueur/IA, aucun bypass persistant | `test_g1_native_choice.py` |
| Exceptions et autres règles | Helper natif complet, CB/coûts/corps d'acceptation préservés par inversion des octets | `test_declaration_law_context.py`, `test_g1_native_choice.py` |
| Annulation | Enregistrement limité à la fin de l'acceptation native, conditions et autres branches natives conservées | `test_g1_royal_response.py`, `test_g1_native_choice.py` |
| Capture de loi | Adaptateur absent refusé, scopes/phase exacts, états conditionnels distincts, aucune reconstruction tardive | `test_declaration_law_context.py` |
| Dossier royal | Guerre et parties exactes, propriétaire initial, numéro, titre et juridiction actuels | `test_g1_royal_response.py` |
| Rejeu et échéance | Déduplication, état consommé avant effet, fenêtres bornées, vieux événement refusé | `test_g1_royal_response.py`, `test_native_war_intervention.py` |
| Intervention native | Ticket exact, guerre unique, cible recontrôlée, validation native, consommation avant envoi | `test_native_war_intervention.py`, `test_g1_native_target_binding.py` |
| Transport de cible | Marqueurs temporaires liés au reçu consommé, usage unique, nettoyage d'un envoi sans suite | `test_g1_native_target_binding.py` |
| Clôture | Même guerre, propriétaire initial parmi ses participants, premier callback, fenêtres retirées, résultat antérieur conservé | `test_war_receipt_lifecycle.py` |
| Livraison | Sources/versions natives épinglées, empreintes runtime/sorties, défaut de module refusé avant ZIP, kit cohérent | `test_distribution.py`, `test_final_campaign_pack.py` |

Les tests existants portent sur les sources réellement utilisées par les
générateurs. W5 ajoute leur vérification sur les fichiers du dossier privé
effectivement assemblé depuis le ZIP. Ce contrôle réutilise les validateurs
des dossiers royaux, de la loi, de l'intervention et du cycle de guerre.

Le test positif vérifie aussi que retirer les ajouts RW de l'adaptateur généré
restitue exactement les définitions natives synthétiques fournies, en conservant
`claim_cb`. Il retire seulement le BOM et l'unique fin de ligne ajoutée au fichier.

## Neuf mutations négatives du dossier assemblé

Chaque mutation travaille sur les octets de source lus après assemblage, en
mémoire. Le validateur concerné doit signaler l'écart.

1. Retirer le contrôle du choix explicite de défi à l'acceptation.
2. Remplacer la comparaison du numéro de dossier par sa seule présence.
3. Comparer la référence de guerre au titre d'autorité.
4. Retirer le contrôle du détenteur du titre d'autorité.
5. Retirer la validation de l'interaction native.
6. Réintroduire une capture tardive dans la liaison au dossier royal.
7. Limiter la clôture aux attaquants, en perdant les participants de l'autre camp.
8. Conserver une fenêtre d'action après clôture.
9. Retirer le contrôle du premier callback et permettre sa réécriture.

Le nouveau test vérifie des invariants source. Son résultat ne constitue pas
l'exécution des neuf situations dans le moteur. Les refus de version, sources,
chemins, empreintes, sortie préexistante et copie partielle restent exercés par
les tests d'assemblage existants.

## Qualification et validation restante

W5 termine le critère source des gardes du chemin intégré retenu. Son crédit
porte sur les gardes livrées et leur couverture du parcours construit, avec les
cas négatifs correspondants. La compilation sémantique, les refus effectifs
dans CK3, les coûts réellement débités, le rechargement, les transitions Mega Wars
et la performance conservent leurs scénarios de campagne. Les anciennes
observations joueur/IA sont détaillées dans les rapports G1 associés.

Les critères V1–V5 restent ouverts. La revue de fond des huit systèmes prévue
par le propriétaire reprend à partir de ce socle et peut accompagner les essais
groupés. Les variantes simplifiées et complètes gardent leurs propres résultats.
