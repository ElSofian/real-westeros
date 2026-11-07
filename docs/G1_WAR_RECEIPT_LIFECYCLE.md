# W4 — Clôture des choix et conservation du reçu de guerre

## Qualification source du 7 novembre 2026

W4 est qualifié en source après correction du chemin de fin lors d'un transfert
de commandement. Développement **76 → 78/80**, campagne finale **0/20**, delta
**+2**. Le code évalué est `f5f91d722b47c6102e796bb2b85b2d580e468970`.
La nouvelle recherche de participants est expérimentale, **non testée dans CK3**.

### Correction du dossier du déclarant initial

Le callback visitait uniquement les histoires de l'attaquant principal courant.
Un déclarant initial encore présent comme participant après transfert pouvait
ainsi être absent de cette visite. La fermeture garde sa visite directe de
l'attaquant du callback, puis visite les autres participants de la même guerre.
L'itérateur natif `every_war_participant`, documenté depuis un scope de guerre
vers des personnages, couvre les deux camps. La recherche reste locale à cette
guerre et aux histoires possédées par ses participants.

Un effet interne partagé conserve toutes les opérations de fermeture antérieures.
Le contrôle du type, schéma, numéro présent, propriétaire initial, attaquant initial
et référence exacte de guerre reste obligatoire. Le premier callback garde sa
priorité et les résultats de censure, refus ou envoi déjà clos sont conservés.
Le retrait des fenêtres et la clôture rendent les tickets différés inutilisables
après ce callback.
La comparaison des opérations normalisées avant/après confirme cette conservation.

| Contexte rencontré | Traitement du chemin source |
|---|---|
| Déclarant toujours attaquant principal | Visite directe, fermeture personnelle identique |
| Déclarant devenu participant secondaire ou passé dans l'autre camp | Recherche parmi les participants de la guerre exacte |
| Autre guerre ou dossier d'un autre propriétaire initial | Comparaisons d'identité et de référence refusent l'écriture |
| Déclarant sorti de la guerre ou décédé | Entretien local ou fin de l'histoire personnelle, sans suivi d'un successeur |
| Rôles, CB ou autorité devenus inadmissibles | Effets refusés immédiatement par leurs gardes, fenêtres closes au constat mensuel |
| Guerre remplacée ou callback absent | Référence initiale conservée jusqu'au nettoyage local, aucune liaison à la remplaçante |
| Callback répété ou résultat déjà clos | Premier reçu conservé, aucune nouvelle conséquence native |

### Frontière avec le cycle Mega Wars natif

L'audit des sources installées relève le contrôle Mega Wars dans
`claim_cb.allowed_against_character`, les actions natives de début, transfert et
invalidation, et la maintenance quotidienne des histoires Mega Wars. Ces parties
restent exécutées dans leur contexte AGOT. Le générateur ne remplace aucune de
ces actions, histoires ou définitions de triggers Mega Wars.

Les quatre préfixes RW se limitent aux callbacks du vrai `claim_cb`. L'inversion
complète, vérifiée sur le fichier AGOT réel épinglé, restitue tous ses octets après
retrait de la capture et des quatre préfixes de fin. Les alias natifs restent
intacts. Le reçu source associé contient uniquement empreintes et repères des
sources primaires et de la documentation moteur de l'itérateur.

La [paix blanche déjà observée](G1_FIRST_ENGINE_TRIAL.md) établit un reçu terminal
`on_white_peace` avec une paix réelle, tout en conservant `native_requested`.
Le contre-test de refus conserve la guerre active sans reçu terminal. Ces essais
portent sur la version précédente du corps de fermeture. La nouvelle visite des
participants et les transitions Mega Wars conservent leur validation en campagne.

Deux nouvelles régressions fixent la visite du déclarant courant et des autres
participants, ainsi que les gardes personnelles de l'effet partagé. Les tests
antérieurs continuent de couvrir mauvais dossier, rejeu, retrait des fenêtres,
non-transfert d'autorité et préservation native. Le crédit W4 porte sur cette
intégration source corrigée. Le barème moteur et W5 restent ouverts.

### Complément à la campagne groupée

Ajouter à WARLIFE-04/06 un transfert où le déclarant initial reste secondaire,
puis un changement de camp s'il est possible dans le scénario natif. Vérifier
la fermeture de son dossier à la fin, le label du callback, l'absence d'écriture
dans un dossier étranger et de nouvel envoi royal. Comparer au témoin AGOT.
Tester séparément la sortie complète du déclarant, un callback manquant et la
conservation des références après rechargement. Mesurer le coût sur une guerre
avec de nombreux participants. L'itérateur documenté ne prouve aucune performance.

## Préparation historique du 5 novembre

La section suivante conserve les limites et le score de la première préparation.

**Source expérimentale, contrôles statiques seulement. W4 ouvert, +0 :
développement 64/80, validation en jeu 0/20, total 64/100.**

## Correction dans le mod original

Le nettoyage W3 utilisait le même test pour « guerre encore admissible aux actions »
et « reçu à conserver ». Un changement de CB ou de rôles pouvait donc supprimer
le reçu lors de l’entretien mensuel alors que sa guerre exacte existait encore.
Une nouvelle observation du même contexte aurait alors perdu la protection anti-rejeu.

`rw_uw_exact_war_present_trigger` sépare cette conservation des autorisations :
schéma/type/propriétaire initial et guerre exacte dans la liste locale du propriétaire.
Il ne dépend pas du CB, des rôles actuels, du suzerain ou des fenêtres d’action.
Il ne suit pas une guerre remplaçante, un héritier ou un nouveau chef de guerre.
Le reçu se termine lorsque cette guerre quitte la liste locale, ou au décès du
propriétaire. Ce n’est pas une preuve de disparition globale de la guerre.

L’entretien ferme les choix encore ouverts si le contexte d’action est perdu :
CB/rôles, parties vivantes, juridiction ou détenteur du titre d’autorité. Le résultat
est `context_lost`, sans sanction, nouvelle qualification juridique ou événement.
Les contrôles partagés existants s’appliquent toujours avant chaque effet ; l’entretien
mensuel ne remplace pas ces contrôles et n’observe pas toutes les transitions entre
deux passages. Une clôture observée ne rouvre jamais les fenêtres.

## Préfixes privés de fin de revendication

L’adaptateur **0.0.5** insère un appel original avant le corps de chacun des quatre
callbacks natifs : `on_invalidated`, `on_victory`, `on_white_peace`, `on_defeat`.
L’effet ne fait rien sans les scopes de guerre et d’attaquant du callback. Il cherche
uniquement les histoires personnelles de cet attaquant, avec schéma/type/propriétaire,
numéro et guerre exactement correspondants. Aucun parcours global des personnages
ou histoires, aucun ciblage reconstruit depuis les guerres ultérieures.

Le premier appel correspondant enregistre date et **nom du callback observé**, ferme
les choix encore ouverts et retire les fenêtres suzerain/réponse/durée totale.
Une censure, un refus ou un envoi natif déjà enregistré garde son résultat original.
Les callbacks répétés ne réécrivent pas le premier reçu ; l’histoire reste conservée
pour l’anti-rejeu tant que sa guerre exacte est dans la liste locale du propriétaire.
Un événement d’intervention différé ne retrouve donc plus un ticket `native_queued`.
Les événements natifs déjà envoyés restent entièrement sous contrôle natif.

Ce préfixe n’est pas l’observation d’une paix effectivement exécutée : il précède
le corps natif et ne garantit ni sa résolution ni l’ordre des callbacks moteur.
Il n’interrompt, ne recrée et ne termine aucune guerre ; aucun coût, hameçon,
titre, claim, opinion, crime ou état Mega Wars n’est écrit. Les alias natifs
`war`/`attacker`/`defender` restent inchangés. Retirer LAW_PREFIX et les quatre
TERMINAL_PREFIXES restaure exactement la définition claim_cb native, UTF-8/CRLF,
commentaires et autres branches compris. Toute entrée/layout inattendue est refusée.

## Limites Mega Wars et installation

Le reçu source ne publie que chemins relatifs, hashes et repères. Le helper AGOT
`agot_mw_is_in_realm_at_megawar` inspecté dépend de `root` et parcourt les dirigeants
et histoires : ce changement ne l’appelle pas dans un contexte de story différent.
La qualification, la rupture/réunification des royaumes, les rôles et les issues
restent gérés par AGOT. Un changement de contexte ferme notre dossier lors de son
observation, sans changer la guerre, transférer l’autorité ou considérer le retour
d’un personnage comme un nouveau consentement. Une guerre remplacée n’est jamais liée.

La disponibilité des scopes dans chaque callback, leur ordre face à Mega Wars,
la conservation des références et les retours natifs restent à démontrer dans CK3.
**Ce changement ne termine donc pas W4**, ni G1/W1/W2/W5/AI4. Aucun test intermédiaire
ou nouveau fichier utilisateur demandé ; les cas ci-dessous rejoignent la campagne finale.

Treize fichiers originaux runtime sont dans le ZIP public, avec le générateur ;
les trois fichiers natifs générés restent PRIVÉS. Quatre entrées AGOT épinglées
inchangées. Le fichier de triggers Mega Wars est une référence d’audit, jamais copié,
modifié ou requis comme cinquième entrée. Remplacer complètement l’ancien adaptateur
privé et installer Real Westeros du même commit ; ne pas superposer ses anciennes
bibliothèques ou cumuler les diagnostics/overrides de déclaration/claim_cb.

## WARLIFE-01…08 — tous NON EXÉCUTÉS

| Cas | Vérifier dans la campagne finale |
|---|---|
| 01 | Victoire/défaite/paix blanche/invalidation : scopes présents, reçu avant corps natif, choix clos ; résultats natifs identiques au témoin. |
| 02 | Fin entre mise en file et événement du lendemain : aucun nouvel envoi natif, aucune opinion ou dépense originale. |
| 03 | Callback répété, autre guerre, autre propriétaire/numéro/schéma : aucune réécriture ou clôture d’un dossier étranger. |
| 04 | Rôles/CB modifiés pendant la même guerre : reçu conservé, choix fermés au constat ; pas de recréation ni substitution de guerre. |
| 05 | Changement de suzerain/détenteur, décès/captivité : contrôles immédiats refusent les effets, entretien ne transfère aucune autorité ; pas d’héritage personnel. |
| 06 | Mega Wars : rupture/réunification, remplacement de guerre et changement de camp ; comparer rôles, titres, fin et nettoyage au témoin AGOT, sans écrire ses variables. |
| 07 | Censure/refus/envoi natif préalable : résultat conservé ; clôture callback ne signifie pas peine supplémentaire, paix acceptée ou négociation confirmée. |
| 08 | Guerre longue, sauvegarde/rechargement, disparition de la liste locale et volume IA : rétention bornée au contexte connu, absence de double envoi et coût de maintenance mesuré. |
