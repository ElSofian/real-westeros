# Restitution volontaire effective — titre ducal

**Mise à jour :** la [chaîne après confiscation](POST_CONFISCATION_RESTITUTION.md)
complète désormais J5 dans son périmètre personnel ducal (+2 source,66/80+0/20).
Le chemin de promesse décrit ci-dessous reste distinct et ne suffit pas seul à
ce critère ; sa description/évaluation initiale à64 est conservée comme historique.

**Candidat source expérimental ; aucun test CK3. J5 reste ouvert, +0 :
64/80 développement, 0/20 moteur, 64/100 total.** Ce changement écrit un véritable
appel de transfert, pas seulement une intention ou une ouverture de fenêtre.
Il ne termine pas la restauration après une sanction coercitive effective.

## Décision et portée

Dans le panneau d'une promesse personnelle de restitution déjà acceptée et encore
à échéance, le détenteur peut choisir « Rendre ce titre ducal ». Joueur et IA
utilisent la même option, les mêmes gardes et le même effet. L'IA préfère honorer
la promesse, avec une pondération selon honnêteté/tromperie ; elle peut aussi
renoncer ou ne rien faire via les choix existants. Pas de recherche mondiale.

Le premier domaine couvre une dignité ducale actuellement possédée par un roi ou
empereur féodal indépendant, rendue à son vassal direct féodal de rang comtal,
déjà établi, de même foi/culture. Les deux doivent être vivants, adultes, libres,
en paix et sans diarchie ; partition et héritier du donateur exclus. Le titre
ne doit être ni primaire, ni foncier abstrait, ni familial, ni chef de foi, loué,
misé ou bloqué à l'attribution par AGOT. Les gardes originales de la promesse
conservent son identité privée et sa version. Une histoire archivée justifie une
demande ; elle ne crée aucun droit automatique sur le détenteur actuel.

**Seul le titre ducal change de détenteur.** Aucun comté, aucune baronnie ni aucun
vassal d'un autre personnage n'est inclus. Aucun statut nobiliaire, droit futur,
crime, revendication, hook ou loi de succession n'est modifié par le code RW.
Les conséquences scriptées natives applicables sont déléguées à l'adaptateur.
Les comtés et bénéficiaires non établis restent sur la voie native habituelle.

## Exécution et preuve

Le choix consomme définitivement la possibilité d'essayer pour cette promesse,
avec révision exacte et ticket de deux jours. Un événement caché distinct,
programmé le lendemain, revérifie l'identité, l'échéance, le détenteur courant,
les capacités et la disponibilité de l'adaptateur. Il nettoie les seules listes
locales `target_titles` et `titles_to_grant`, et lie un seul titre, l'acteur et le
bénéficiaire dans son propre contexte. Il ne réutilise pas le contexte d'une
interaction native ouverte. Les alias temporaires que les callbacks ne lient que
conditionnellement sont également effacés, notamment `recipient_is_independent`,
pour ne pas réutiliser une ancienne indépendance.

Avant toute mutation : les quatre prédicats natifs copiés (`is_shown`, validité,
sélecteur de titre, `can_send`) doivent réussir. Le ticket est consommé avant
`create_title_and_vassal_change` de type `granted`, puis `change_title_holder`
sans baronnies et `resolve_title_and_vassal_change`. Ce motif d'API existe dans
les sources AGOT reçues. L'interaction administrative dont il provient n'est
ni appelée ni débridée : les conditions féodales de cette décision sont originales.

Un résultat `transferred` n'est inscrit qu'après vérification du détenteur réel.
Alors seulement sont exécutés une fois les corps natifs d'acceptation et de
notification. En cas de refus des gardes ou d'absence de transfert observé :
pas de récompense RW, de nouvelle tentative automatique, de rollback supposé
atomique ou de faux succès. Une tentative consommée ne peut pas être relancée
par un ancien panneau ou un second callback. Les dons ordinaires restent possibles.

La promesse reste dans son état existant : la constatation native `on_title_gain`
peut observer le transfert et le bénéficiaire peut ensuite l'accuser réception.
Le nouvel effet ne fabrique pas de reçu de révocation, ne réécrit aucun fait
canonique et ne prétend pas qu'une confiscation précédente était légale.
Les lecteurs voient résultat et limites dans le panneau privé existant.

## Adaptateur privé

```sh
python tools/build_native_restitution.py --agot-root <AGOT> --output <nouveau-dossier-prive>
```

Le mod public refuse ce choix sans adaptateur. Le générateur vérifie le hash exact
du fichier AGOT reçu et les versions déclarées 0.5.2.1 / support1.19.0.6. Il clone
six blocs sous des noms RW : quatre prédicats et deux callbacks. **Les six corps
restent octet pour octet identiques**, seuls les noms des définitions changent.
Il ne remplace aucune interaction native. Les sorties privées remplacent seulement
les fallbacks RW, après le mod de base. Le reçu épingle tous les fichiers du mod
nécessaire et les deux sorties privées. Un dépôt, une destination existante,
une entrée symbolique, un hash ou des versions différents sont refusés.

**La sortie contient du code AGOT : ne jamais publier, committer ou redistribuer.**
Le ZIP public ne contient que le générateur original, les scripts RW et les reçus
d'empreintes. Installer AGOT, Real Westeros du même commit, puis cet adaptateur.
Il peut être préparé avec les autres candidats pour la campagne finale ; aucun
lancement intermédiaire ni nouveau fichier utilisateur n'est demandé.

L'alias natif `dummy_gender`, non lié visiblement dans la définition reçue mais
passé au paramètre `TITLE` de relation de maisons, est lié explicitement au titre
choisi. C'est une adaptation du contexte, pas une preuve de sa sémantique moteur.
Les corps restent inchangés ; cette liaison et leur ordre doivent être testés.
Le don générique comporte aussi du code moteur invisible : **ce candidat n'est
pas une preuve d'équivalence complète avec son interface native**. Timing,
coûts cachés éventuels, historique, succession, vassalité, notifications, load order
et callbacks AGOT doivent être observés avant toute annonce de compatibilité.
Aucune écriture des fichiers du jeu ou des installations n'est effectuée.

## Vérifications et campagne finale groupée

Tests adversariaux : gardes supprimées, capacité changée, acteur/titre courant,
révision/ticket/rejeu, listes isolées, effets après transfert vérifié et jamais
avant, transfert de vassaux interdit, égalité joueur/IA ; génération synthétique,
inversion des six corps, versions/hash/layout/symlinks/destination et empreintes.
La génération sur les vrais octets reçus utilise un descripteur de **fixture**
aux versions rapportées ; ce n'est pas une installation CK3 vérifiée.

| Cas final | Observation requise — aucun cas exécuté |
|---|---|
| RESTORE-01 | Roi/duc déchu resté comte : demande et promesse, choix explicite, titre précis rendu ; autres titres, comtés, vassaux et suzerainetés inchangés. |
| RESTORE-02 | Même parcours IA↔IA ; aucune aide/validation réservée au joueur, possibilité de ne pas restituer. |
| RESTORE-03 | Décès, guerre, prison, diarchie, bénéficiaire déplacé ou titre perdu entre choix et lendemain : aucun transfert. |
| RESTORE-04 | Titre bloqué, loué, misé, spécial ; restrictions natives de bénéficiaire/titre : garde négative sans conséquence. |
| RESTORE-05 | Ancien panneau, callback répété, sauvegarde/rechargement, ticket expiré, adaptateur absent/retiré : aucune répétition ni faux succès. |
| RESTORE-06 | Comparer au don ducal natif sans transfert de vassaux : historique, opinions, prestige/stress, relations de maisons, notifications et callbacks ; vérifier alias TITLE. |
| RESTORE-07 | Chaîne révocation native réelle → reçu canonique → dépôt facultatif → demande/promesse → restitution ; pas de double effet ou preuve causale inventée. |
| RESTORE-08 | Autres attributions/successions, institutions AGOT et Mega Wars inchangées avec le playset complet ; ne pas utiliser le candidat pendant une guerre. |

Ces cas partagent les sessions finales HCONF/HCRECEIPT/G3. Un lancement prend
7–10 minutes : charger les candidats une fois, puis utiliser les sauvegardes
et scénarios préparés sans relancer CK3 pour chaque cas.

## Suite

J5 exige une restauration après une sanction coercitive effective. La chaîne
reste dépendante des révocations réelles, de leur qualification et de leur
couverture J4/G3 ; une promesse et un appel de transfert étroit ne suffisent pas
à créditer tout le critère. Prochaine étape : couverture des routes coercitives
restantes et intégration de la chaîne, sans multiplier les variantes de journal.
