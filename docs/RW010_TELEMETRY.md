# AI5 — Instrumentation opt-in pour la campagne finale

**Source expérimentale, vérifiée statiquement ; aucun lancement CK3 ni résultat de
performance.** Cette instrumentation observe des chemins effectivement livrés de
justice et de négociation. Elle ne débloque pas G1/G3 et ne crédite aucun point moteur.

## Activation et confidentialité

Dans une copie de sauvegarde réservée à la campagne finale, démarrer CK3 en mode
débogage. Depuis la console, dans le contexte du personnage joué :

```text
effect rw_tm_start_effect = yes
```

Arrêter avec `effect rw_tm_stop_effect = yes`. Aucun démarrage automatique, bouton
joueur ou modification d'un on_action natif. Le marqueur global expire après
90 jours de jeu ; il reste au maximum 5 000 observations par activation, puis un
marqueur `truncated`. Relancer explicitement crée une nouvelle fenêtre et réinitialise
ce budget. Ce plafond concerne les traces, jamais les interactions ou leurs coûts.
Les contrôles start/stop sont hors budget. Sans trace stop (expiration, fermeture,
rotation du journal), la fin reste « non observée ». Sauvegarder/recharger ne remet
pas le budget à zéro. Le débogage CK3 et les globals restent à confirmer en jeu.

Les lignes originales sont des constantes ASCII `RW_TM1 family=… action=… stage=…
control=…`. Aucun nom, identifiant personnage, titre, prix, secret ou terme privé.
Les journaux CK3 complets peuvent contenir d'autres données privées : les conserver
localement. L'outil n'exporte que les compteurs autorisés, jamais les lignes brutes,
les en-têtes, les noms de fichiers ou les chemins. Aucun réseau ou service externe.

## Couverture effective et limites

Le registre [TELEMETRY_HOOKS.json](TELEMETRY_HOOKS.json) énumère les points branchés :

- Arrestation et sentence natives : entrée, garde acceptée/rejetée, demande juste
  avant `run_interaction`, retour du gestionnaire ; choix explicite de non-intervention.
- Accord multi-action : contre-offre, signature, clôture, refus de chaque clause,
  paiement, soutien, libération de charte et choix de quitter.
- Opportunité judiciaire connue : visite dans le contexte du véritable observateur,
  avant évaluation d'éligibilité. Aucun balayage supplémentaire de personnages.

`evaluated` signifie entrée de l'effet ; `authorized` uniquement garde extérieure
passée ; `denied` garde rejetée, **pas preuve de triche**. `selected` est un choix
réel de ne pas intervenir ; `visit` n'est pas une décision. `complete` signifie
**retour du gestionnaire**, jamais succès natif, mort, arrestation ou libération
vérifiée. Des gardes internes peuvent encore éviter une opération après `authorized`.

Avant chaque opération irréversible instrumentée, le reçu métier est déjà consommé.
Une marque auxiliaire `rw_tm_<clé>_committed` sur le même dossier observe une
réentrée : `commit` la première fois, `duplicate` les suivantes. Clés distinctes
pour arrestation, sentence, or, soutien et charte : trois clauses d'un accord ne
sont pas trois doublons. Ces marques n'autorisent, ne bloquent et ne rejouent aucun
effet de jeu ; elles ne sont écrites que pendant une fenêtre active avec budget.
`missing_context` signale un contexte d'audit absent. Cette observation se produit
juste avant la demande, elle ne garantit pas son exécution moteur. Une opération
antérieure non tracée, une autre copie du dossier ou une fenêtre tronquée ne peut
pas être dédupliquée par ce diagnostic. Les marques persistent avec leur dossier
pour observer une réentrée après recharge/réactivation ; aucune migration métier.

Les chemins anciens et les guerres non livrées ne sont pas instrumentés par magie.
La couverture est une tranche représentative, extensible lors de leur développement.
`is_ai` sert seulement à classer la ligne dans le logger commun : mêmes conditions,
coûts, poids, délais et conséquences qu'avant. Les appels n'exposent pas de dossier
privé dans une interface de jeu. Aucune déclaration de compatibilité G4/G5.

## Lecture locale et mesure réelle du processus

À la campagne finale, relever le journal de débogage produit par CK3 (souvent
`debug.log`, selon sa configuration). Vérifier les marqueurs start/stop avant toute
interprétation. Conserver chaque fichier tournant distinct : l'analyse n'en invente
pas l'ordre ni des sessions manquantes.

```sh
python tools/report_telemetry.py debug.log --output traces-agregees.json
```

Un marqueur invalide donne un code de sortie non nul et un compteur sans recopier
son contenu. Une session sans fin observée, tronquée ou des marqueurs orphelins
ne constituent pas une couverture complète. Une ligne `duplicate` appelle une
inspection du scénario et des effets natifs ; zéro doublon dans une fenêtre ne
prouve pas l'absence universelle d'abus. Le rapport ne calcule aucune durée d'effet
à partir des dates de journal.

Sur Windows, sampler **en lecture seule**, depuis le dossier extrait :

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\Measure-RealWesteros-Process.ps1 -DurationSeconds 60 -OutputPath .\process.csv
```

Le script cherche exactement un processus `ck3`, sinon demander explicitement son
PID via `-TargetProcessId 1234`. Il mesure le CPU cumulé natif, le temps mural au
chronomètre, la mémoire résidente/privée et les threads ; aucun chemin, argument,
nom d'utilisateur ou injection. Il refuse d'écraser un fichier existant et cesse
si le processus devient indisponible ou si le PID est réutilisé. Ne pas modifier
le script pour contourner les permissions système ; utiliser le même utilisateur
que CK3. `DurationSeconds` 0,1…3 600 ; intervalle 100…10 000 ms. La fenêtre
commence au premier relevé CPU réel, après l’initialisation des API. Si le processus
reste accessible, au moins deux relevés CPU couvrent la durée demandée ; le coût de
collecte peut prolonger le temps mural. Aucun second relevé n’est fabriqué si le
processus disparaît. CSV invariant même
sur un Windows français, UTF-8 avec BOM.

```sh
python tools/report_telemetry.py debug.log --samples process.csv --output bilan.json
```

Les deltas de CPU sont divisés par le temps **réel entre échantillons** ; un cœur
équivalent peut dépasser 1 pour un processus multithread. Le pourcentage machine
est rapporté au nombre de processeurs logiques observé par PowerShell. Ce nombre
peut être limité par l'environnement ; documenter cette limite. Le pic mémoire
est seulement le maximum échantillonné. Ces mesures portent sur **tout CK3** :
ni FPS, ni latence d'effet, ni surcoût attribuable à RW sans comparaison contrôlée.

## Preuves statiques et distribution

`python tools/verify_telemetry.py` retire seulement les appels d'observation et les
branches else devenues vides, puis compare les six fichiers métier aux empreintes
normalisées prises avant instrumentation. Les gardes, ordre, coûts et effets natifs
restent identiques. Le logger est audité avec un vocabulaire de métadonnées restreint.
Ce contrôle n'est pas une preuve de non-interférence du moteur ou de performance.
Tests négatifs : garde/dispatch modifié, coût ajouté au logger, diagnostic utilisé
comme condition de jeu, entrées malformées, CPU régressif, sortie existante.
Les tests du sampler exécutent un vrai processus PowerShell, **pas CK3** ; Windows
PowerShell 5.1 et PowerShell Linux sont exigés en CI. Les références de syntaxe
natives sont seulement chemins relatifs/empreintes/lignes dans
[TELEMETRY_SOURCE_RECEIPT.json](TELEMETRY_SOURCE_RECEIPT.json), sans code AGOT recopié.
Le ZIP intégré contient les scripts d'observation, ce guide, le registre et les deux
outils autonomes de collecte/rapport ; le vérificateur source reste dans le dépôt.

## Cas finaux TM-01…08 — tous non exécutés

1. **TM-01** : sans activation, aucun marqueur ni variable auxiliaire nouvelle ;
   vérifier les mêmes actions et issues que sans instrumentation.
2. **TM-02** : start/stop, expiration 90 jours, rechargement et rotation de journal ;
   observer le budget conservé, les fenêtres incomplètes correctement signalées.
3. **TM-03** : scénario volume >5 000 observations ; exactement une troncature à
   l'épuisement, plus de trace ni marque auxiliaire, interactions toujours disponibles.
4. **TM-04** : humain/IA, abstention, refus, garde devenue invalide et opportunité ;
   vérifier les lignes contre les choix réellement observés et aucune donnée privée.
5. **TM-05** : trois ordres de clauses, répétition d'options et rechargement ; compter
   les transferts réels séparément des marqueurs, zéro double paiement attendu.
6. **TM-06** : arrestation/sentence, refus ou fenêtre native en attente ; `commit` et
   `complete` ne doivent jamais être interprétés comme une mort/emprisonnement acquis.
7. **TM-07** : sur copies d'une même sauvegarde, comparer AGOT seul, AGOT+RW traces
   désactivées, puis activées. Même vitesse/date/caméra/machine, mêmes échauffements
   et sauvegardes automatiques, plusieurs fenêtres de 60 s au calme et en charge.
   Consigner écarts/dispersion CPU et mémoire sans seuil inventé ni causalité abusive.
8. **TM-08** : après arrêt/reprise et forte charge, régression G2/G4/G5, confidentialité,
   budget et rétention des dossiers ; conserver uniquement un résultat anonymisé
   reproductible sous `docs/engine-results/` après la campagne finale.
