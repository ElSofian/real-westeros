# Suivi de la première version intégrée — v0.1-plan-1

**État courant : 49/100 (+2), dont 49/80 source et 0/20 moteur.**
I3 ajoute la propagation contrôlée des récits ; prochaine cible indépendante M5.
W1/W2 restent ouverts (+0), en attente des observations finales G1 avant voie de production.
Vitesse encore non mesurable : relevés du même jour.

Relevé initial : **1 novembre 2026, 38/100**, évalué sur le code de
`45c5e845597fcf291175308d2f0b6c31fecfd4bc` (après PR #62).
**38/80 points de développement source ; 0/20 points de validation CK3/AGOT.**
Aucun test en jeu exécuté. Cette grille remplace l’estimation orale « environ 30 % » :
la différence est une calibration, pas huit points de fonctionnalités nouvelles.
La création de ce suivi apporte **+0 point de développement**.

Ce score mesure la préparation d’une **première version intégrée couvrant les huit
systèmes**. Il ne mesure ni le pourcentage de la vision finale ouverte, ni les heures
restantes. Les poids sont des conventions de planification, pas des estimations de
coût. Les trois scénarios initiaux ne limitent pas le périmètre ; le catalogue de
126 actions candidates n’est pas une liste de 126 obligations.

## Tableau de bord

| Système | Points acquis | Poids |
|---|---:|---:|
| Liberté, légalité et guerres | 0 | 12 |
| Affaires politiques | 6 | 8 |
| Négociation | 6 | 10 |
| Promesses et obligations | 10 | 10 |
| Justice et sanctions | 5 | 12 |
| Information et preuves | 8 | 8 |
| Mémoire politique | 8 | 10 |
| IA politique | 6 | 10 |
| Validation finale CK3/AGOT | 0 | 20 |

Les critères « source » ci-dessous sont implémentés expérimentalement et vérifiés
statiquement, **pas démontrés dans CK3**. Les points moteur sont indépendants.
Un diagnostic privé, une fenêtre native ouverte ou une réhabilitation politique ne
valident respectivement ni une guerre illégale livrée, ni une sanction exécutée,
ni une restauration après confiscation. Les gardes et contrôles existants restent
à confirmer dans le moteur.

## Critères gelés et preuves

La source de calcul est [V01_PROGRESS.json](V01_PROGRESS.json). Chaque critère est
binaire et n’est compté qu’une fois. Les liens indiquent les pièces principales,
à lire avec les limites de leur guide ; leur existence seule ne prouve pas que
le critère est rempli. La qualification est une revue humaine explicite du code.

### W — Liberté, légalité et guerres

| ID | Points | Critère de fin | État / preuve principale |
|---|---:|---|---|
| W1 | 2 | Qualification de la loi au moment de l’acte et exceptions natives dans le mod livré | À développer / valider |
| W2 | 4 | Déclaration malgré l’interdit avec vrai CB, contexte exact, coûts, annulation et accès joueur/IA | À développer / valider |
| W3 | 2 | Réaction royale discrétionnaire : intervention, sanction ou abstention selon le contexte | À développer / valider |
| W4 | 2 | Intégration du nouveau chemin aux cycles guerre/Mega Wars et à leur clôture | À développer / valider |
| W5 | 2 | Gardes et tests négatifs du chemin livré, distinct du diagnostic privé | À développer / valider |

### P — Affaires politiques

| ID | Points | Critère de fin | État / preuve principale |
|---|---:|---|---|
| P1 | 2 | Deux familles d’incidents hors contrats : affront allégué et complot découvert | Source seulement : [RW010_ALLEGATIONS.md](RW010_ALLEGATIONS.md), [rw_allegation_effects.txt](../mod/real_westeros/common/scripted_effects/rw_allegation_effects.txt) |
| P2 | 2 | Dossiers versionnés : parties connues, déclarations, faits et résolution distincts | Source seulement : [RW010_RECORDS.md](RW010_RECORDS.md), [rw_political_cases.txt](../mod/real_westeros/common/story_cycles/rw_political_cases.txt) |
| P3 | 2 | Médiation, réparation volontaire, saisine et abstention explicites | Source seulement : [RW010_CASES.md](RW010_CASES.md), [rw_case_events.txt](../mod/real_westeros/events/rw_case_events.txt) |
| P4 | 2 | Menaces ou ultimatums structurés avec enjeu, réponse et escalade crédible | À développer / valider |

### N — Négociation

| ID | Points | Critère de fin | État / preuve principale |
|---|---:|---|---|
| N1 | 2 | Offre, contre-offre, consentement versionné et gardes de fonds/rejeu | Source seulement : [RW010_SERVICES.md](RW010_SERVICES.md), [rw_service_effects.txt](../mod/real_westeros/common/scripted_effects/rw_service_effects.txt) |
| N2 | 2 | Au moins deux clauses indépendantes négociables : prix et délai | Source seulement : [RW010_DELIVERY_TERMS.md](RW010_DELIVERY_TERMS.md), [rw_service_effects.txt](../mod/real_westeros/common/scripted_effects/rw_service_effects.txt) |
| N3 | 2 | Trois services distincts et contreparties or/faveur : soutien, retrait d’allégation, libération de charte | Source seulement : [RW010_ALLEGATION_SETTLEMENT.md](RW010_ALLEGATION_SETTLEMENT.md), [rw_allegation_settlement_effects.txt](../mod/real_westeros/common/scripted_effects/rw_allegation_settlement_effects.txt) |
| N4 | 2 | Modèle de contrat réutilisable partagé par au moins deux systèmes | À développer / valider |
| N5 | 2 | Accord combinant plusieurs actions, consentement commun et résultats par action | À développer / valider |

### O — Promesses et obligations

| ID | Points | Critère de fin | État / preuve principale |
|---|---:|---|---|
| O1 | 2 | Engagement personnel différé avec consentement et exécution volontaire | Source seulement : [RW010_DEFERRED_FAVOR.md](RW010_DEFERRED_FAVOR.md), [rw_deferred_favor_effects.txt](../mod/real_westeros/common/scripted_effects/rw_deferred_favor_effects.txt) |
| O2 | 2 | Engagement continu et conditionnel, observation séparée de la faute volontaire | Source seulement : [RW010_MILITARY_RESTRAINT.md](RW010_MILITARY_RESTRAINT.md), [rw_military_restraint_effects.txt](../mod/real_westeros/common/scripted_effects/rw_military_restraint_effects.txt) |
| O3 | 2 | Engagement territorial/institutionnel et reconnaissance explicite du successeur | Source seulement : [RW010_RESTITUTION_CHARTERS.md](RW010_RESTITUTION_CHARTERS.md), [rw_restitution_charter_effects.txt](../mod/real_westeros/common/scripted_effects/rw_restitution_charter_effects.txt) |
| O4 | 2 | Cycle d’engagement patrimonial ou dynastique explicite, sans dette bancaire ni culpabilité héritée | Source seulement : [RW010_DYNASTIC_ENDOWMENTS.md](RW010_DYNASTIC_ENDOWMENTS.md), [rw_dynastic_pledge_effects.txt](../mod/real_westeros/common/scripted_effects/rw_dynastic_pledge_effects.txt) |
| O5 | 2 | Renoncement, libération, expiration et exécution unique avec réponse discrétionnaire | Source seulement : [RW010_DEFERRED_FAVOR.md](RW010_DEFERRED_FAVOR.md), [rw_deferred_favor_effects.txt](../mod/real_westeros/common/scripted_effects/rw_deferred_favor_effects.txt) |

### J — Justice et sanctions

| ID | Points | Critère de fin | État / preuve principale |
|---|---:|---|---|
| J1 | 2 | Inspection des raisons natives et de la détention, sans fausse immunité ni verdict rétroactif | Source seulement : [RW010_SCHEME_JUSTICE.md](RW010_SCHEME_JUSTICE.md), [rw_scheme_justice_triggers.txt](../mod/real_westeros/common/scripted_triggers/rw_scheme_justice_triggers.txt) |
| J2 | 3 | Sanction individuelle réellement exécutée via chemin natif joueur/IA, avec refus et résistance | Source seulement : [RW010_NATIVE_JUSTICE_ACTIONS.md](RW010_NATIVE_JUSTICE_ACTIONS.md), [rw_justice_action_effects.txt](../mod/real_westeros/common/scripted_effects/rw_justice_action_effects.txt) |
| J3 | 3 | Pouvoir arbitraire/légal et sanctions discrétionnaires distinctes sans double peine native | À développer / valider |
| J4 | 2 | Mesures coercitives familiales/dynastiques de terres ou statut couvrant les routes G3 | À développer / valider |
| J5 | 2 | Restauration après sanction coercitive effective, au-delà de la réhabilitation politique | À développer / valider |

### I — Information et preuves

| ID | Points | Critère de fin | État / preuve principale |
|---|---:|---|---|
| I1 | 2 | Observation du complot découvert et participants connus séparés | Source seulement : [RW010_SCHEME_EVIDENCE.md](RW010_SCHEME_EVIDENCE.md), [rw_scheme_on_actions.txt](../mod/real_westeros/common/on_action/rw_scheme_on_actions.txt) |
| I2 | 2 | Allégation, aveu, contestation et silence distincts de la vérité | Source seulement : [RW010_ALLEGATIONS.md](RW010_ALLEGATIONS.md), [rw_allegation_effects.txt](../mod/real_westeros/common/scripted_effects/rw_allegation_effects.txt) |
| I3 | 2 | Rumeur et propagation contrôlée avec source, destinataire et provenance | Source seulement : [RW010_RUMOR_PROPAGATION.md](RW010_RUMOR_PROPAGATION.md), [rw_rumor_effects.txt](../mod/real_westeros/common/scripted_effects/rw_rumor_effects.txt) |
| I4 | 2 | Accès privé/public et provenance sans association causale ou preuve rétroactive dans les dossiers livrés | Source seulement : [RW010_RECORDS.md](RW010_RECORDS.md), [rw_case_triggers.txt](../mod/real_westeros/common/scripted_triggers/rw_case_triggers.txt) |

### M — Mémoire politique

| ID | Points | Critère de fin | État / preuve principale |
|---|---:|---|---|
| M1 | 2 | Historique personnel indépendant et rétention bornée | Source seulement : [RW010_RECORDS.md](RW010_RECORDS.md), [rw_political_cases.txt](../mod/real_westeros/common/story_cycles/rw_political_cases.txt) |
| M2 | 2 | Continuité institutionnelle et stockage séparés des rôles et du consentement | Source seulement : [RW010_LAND_REGISTER.md](RW010_LAND_REGISTER.md), [rw_land_register_effects.txt](../mod/real_westeros/common/scripted_effects/rw_land_register_effects.txt) |
| M3 | 2 | Disgrâce politique de maison et réhabilitation multigénérationnelle sans faute personnelle héritée | Source seulement : [RW010_HOUSE_AFFAIRS.md](RW010_HOUSE_AFFAIRS.md), [rw_house_affairs.txt](../mod/real_westeros/common/story_cycles/rw_house_affairs.txt) |
| M4 | 2 | Intégration pertinente des souvenirs ou relations de maison natifs, au-delà des journaux propres | Source seulement : [RW010_NATIVE_MEMORIES.md](RW010_NATIVE_MEMORIES.md), [rw_political_memories.txt](../mod/real_westeros/common/character_memory_types/rw_political_memories.txt) |
| M5 | 2 | Mémoire influençant des choix politiques futurs indépendants du dossier d’origine | À développer / valider |

### AI — IA politique

| ID | Points | Critère de fin | État / preuve principale |
|---|---:|---|---|
| AI1 | 2 | Actions implémentées : coûts et gardes partagés, raccourcis humains explicitement bornés | Source seulement : [RW010_FAVOR_SERVICE.md](RW010_FAVOR_SERVICE.md), [rw_favor_service_effects.txt](../mod/real_westeros/common/scripted_effects/rw_favor_service_effects.txt) |
| AI2 | 2 | Ciblage borné, occasions réactives et délais anti-spam sans parcours global des paires | Source seulement : [RW010_FAVOR_SERVICE.md](RW010_FAVOR_SERVICE.md), [rw_favor_service_interactions.txt](../mod/real_westeros/common/character_interactions/rw_favor_service_interactions.txt) |
| AI3 | 2 | Politique contextuelle partagée par deux familles avec au moins trois facteurs : enjeux, risques, moyens, savoir ou obligations | Source seulement : [RW010_CONTEXTUAL_AI.md](RW010_CONTEXTUAL_AI.md), [rw_political_ai_values.txt](../mod/real_westeros/common/script_values/rw_political_ai_values.txt) |
| AI4 | 2 | Chemins autonomes IA↔IA à travers guerre, justice et négociation | À développer / valider |
| AI5 | 2 | Instrumentation effective des décisions, abus et performances, prête pour la campagne finale | À développer / valider |

### V — Validation finale CK3/AGOT

| ID | Points | Critère de fin | État / preuve principale |
|---|---:|---|---|
| V1 | 4 | G1 : vrai CB, interdiction royale et cycles guerre/Mega Wars démontrés en jeu | À développer / valider |
| V2 | 4 | G2 : interface multi-clause, sauvegarde/rechargement, rejeu et obligations démontrés en jeu | À développer / valider |
| V3 | 4 | G3 : octroi, succession, élection, conquête, sanction/restauration et dettes natives démontrés en jeu | À développer / valider |
| V4 | 4 | G4 : IA↔IA, symétrie, spam, abus et performance effectivement mesurés en jeu | À développer / valider |
| V5 | 4 | G5 : régression AGOT, installation et distribution vérifiées, blocages de sortie corrigés | À développer / valider |

## Prochain ordre de travail

1. **AI3 — livré dans les sources, +2 points acquis** : politique contextuelle partagée
   par au moins deux familles d’actions, utilisant trois facteurs concrets parmi
   enjeux, risques, moyens, informations connues et obligations. Des poids aléatoires
   fondés uniquement sur les traits ou une nouvelle variante de dialogue ne suffisent pas.
2. **J2 — voie d’arrestation livrée dans les sources, +3 acquis** : chemin de sanction individuelle effectif, natif et accessible
   à l’IA ; préserver droit, coût, refus et résistance. Une simple fenêtre ne suffit pas.
3. **W1/W2 — ouverts, +2/+4 possibles après résolution des limites G1** : qualification au moment de l’acte et véritable guerre
   interdite intégrée. Réserver RW-004 séparément. Ne pas livrer le diagnostic privé
   comme solution ; si un point moteur empêche une implémentation sûre, conserver le
   manque visible et travailler sur un critère indépendant, sans demander un test intermédiaire.
4. **O4/I3 livrés dans les sources (+2 chacun) ; M5 cible suivante** : engagements patrimoniaux/dynastiques, propagation de rumeurs,
   effet de la mémoire sur des choix futurs. M4 est livré dans les sources (+2),
   avec souvenirs publics natifs ; cela ne termine pas M5. Les autres critères ouverts
   demeurent dans le périmètre, notamment J3/J4/J5, N4/N5, P4, W3/W4/W5 et AI4/AI5.
5. **V1…V5** : une campagne finale, selon [FINAL_ENGINE_TESTS.md](FINAL_ENGINE_TESTS.md).
   Corriger ses erreurs avant de revendiquer une version jouable/compatible.

Cet ordre privilégie les manques structurants. Une dépendance technique peut imposer
un travail préalable à **+0** ; l’annoncer et expliquer quel critère il débloque.
Ne plus prolonger indéfiniment une tranche déjà comptée par de petites variantes.

## Règles de mise à jour et vitesse

- Avant une tâche : annoncer le critère visé et le score de départ. Après : score,
  delta réellement acquis, preuve et manque suivant. Une PR peut légitimement faire +0.
- Documentation, audit, nouveaux tests, diagnostic ou variante ne donnent pas
  automatiquement de points. Ne jamais convertir le nombre de PR/tests en progression.
- Pour changer un état, mettre à jour les preuves et ajouter un relevé daté réel au
  journal JSON : version, critères terminés, score recalculé, référence PR/commit et raison.
  Un retour en arrière est enregistré comme régression ; ne pas réécrire l’historique.
- Les critères/poids sont gelés par empreinte. Une modification de périmètre ou de
  pondération est une **recalibration**, exige une nouvelle version explicitée et une
  copie conservée de l’ancien relevé. Elle ne compte jamais comme livraison. Une réduction
  majeure de vision reste une décision du propriétaire.
- **Vitesse initiale : non mesurée.** Le rapport exige au moins deux relevés de même
  grille espacés d’au moins sept jours calendaires, dans une fenêtre de trente jours.
  Il indique les points/semaine au dernier relevé, y compris zéro ou une régression.
  Ce n’est pas une mesure des heures actives. Pas d’ETA calculée à partir des PR.
- Les points moteur exigent des résultats reproductibles sous `docs/engine-results/`,
  sans données privées. Un plan de tests ou une source inspectée ne les remplace pas.
  Les gardes automatiques vérifient cohérence et liens ; la revue juge les preuves.

Commande de consultation, sans modification ni simulation du jeu :

```sh
python tools/report_progress.py
python tools/report_progress.py --json
```

Les actions continuent d’être écrites en scripts CK3. Python sert uniquement au
contrôle de ce tableau. Tous les critères moteur restent ouverts jusqu’à la campagne
finale ; aucune compatibilité CK3/AGOT n’est présumée.
