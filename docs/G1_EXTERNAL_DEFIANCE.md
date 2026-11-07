# Défi d'une interdiction de guerre extérieure

Tranche du 8 novembre 2026. **Static-checked**, expérimentale et **non testée dans
CK3**. Baseline et résultat 80/80 source, 0/20 campagne, delta 0.

## Portée de PRIVATE0.0.8

L'option native de défi examine désormais l'interdiction applicable au déclarant.
Le périmètre pris en charge reste deux personnages adultes, vivants, libres,
possessionnés et féodaux. Le déclarant doit avoir un suzerain direct vivant.
Le destinataire peut dépendre d'un autre suzerain ou être indépendant.

| Loi du suzerain direct du déclarant | Même suzerain direct | Autre branche ou indépendant |
| --- | --- | --- |
| Aucune interdiction | Option absente | Option absente |
| Guerres internes interdites | Défi proposé si permission native requise | Option absente |
| Toutes les guerres interdites | Défi proposé si permission native requise | Défi proposé si permission native requise |

Le helper natif `war_declarer_needs_hook_on_liege` reste requis. Les exceptions
contractuelles et légales qu'il reconnaît conservent donc leur effet. La loi du
roi ou du défenseur ne remplace pas celle du suzerain direct du déclarant.

Le défi doit être explicitement sélectionné et ne peut être combiné avec le
hameçon sélectionné. Il ouvre uniquement la branche native d'interdiction de
guerre concernée. Les autres conditions de déclaration, les coûts et le vrai CB
restent ceux de CK3/AGOT. Le générateur vérifie l'inversion exacte de ses ajouts.

Joueur et IA utilisent les mêmes conditions d'éligibilité et d'exécution.
Le joueur commence avec la case décochée. La préférence IA existante utilise
désormais ce périmètre élargi, avec ses mêmes conditions d'opinion, moyens et
engagements. L'initiative du planificateur natif contre une cible extérieure et
la prise en compte complète de la personnalité restent à vérifier ou améliorer.

## Dossier et réponses

Le relevé précoce conserve la loi, les parties et les titres d'un `claim_cb`.
La liaison d'acceptation expérimentale conserve acteur, destinataire et choix
seulement avec une correspondance fraîche et unique à cette guerre exacte.
Les autres CB natifs gardent leur comportement, sans nouveau relevé RW ici.

Le parcours politique existant exige explicitement un suzerain direct commun.
Une déclaration extérieure n'entre donc pas dans ce parcours. Le routage des
réponses distinctes de Mace et Doran, puis une éventuelle demande à un supérieur,
reste la prochaine tranche. La proclamation générale de paix demeure différée.

## Vérifications et campagne groupée

Cinq tests de source contrôlent la table de lois, l'autorité du déclarant,
les exceptions natives, la séparation hameçon/défi et la limite du parcours
politique. Les mutations négatives retirent ou inversent ces gardes.
La préparation privée utilise les sources natives locales sans les distribuer.

La campagne finale doit observer les cases cochée/décochée, les exceptions et
coûts, les cibles d'une autre branche et indépendantes, le vrai CB et ses rôles,
la liaison au relevé exact, les déclarations IA, les sauvegardes/rechargements,
les anciens événements entre pairs et les contraintes Mega Wars. Aucun résultat
de ces nouveaux cas moteur n'est revendiqué dans cette tranche.
