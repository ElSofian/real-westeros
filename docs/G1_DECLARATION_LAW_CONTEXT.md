# W1 — Relevé de contexte dans le callback natif de déclaration

**Actualisation du 7 novembre 2026.** [W1 est qualifié en source](G1_W1_QUALIFICATION.md),
+2 points, développement76/80 et campagne0/20. Les liens déjà observés lèvent le
doute de disponibilité avant liaison pour ces parcours. Les essais exceptionnels
restent groupés. La préparation ci-dessous conserve son état historique initial.

**Source expérimentale ; aucun test CK3. W1 reste ouvert, +0 point.**
Cette tranche prépare la qualification de la loi et des exceptions au bon endroit
scripté. Elle ne prétend pas avoir démontré l'ordre des callbacks du moteur ou
l'interdiction applicable à l'instant physique de déclaration. Développement 64/80,
validation en jeu 0/20, total 64/100 ; ni crime ni verdict rétroactif ajoutés.

## Point d'entrée et préservation d'AGOT

L'adaptateur privé ajoute un unique appel original en tout début de
`claim_cb.on_declaration`, avant le corps natif contenant `on_declared_war = yes`.
Le CB garde son **vrai identifiant**, ses cibles, coûts, invalidations et issues :
retirer cet appel retrouve exactement les octets de la définition d'origine.
Le script ne démarre, n'arrête et ne rejoue aucune guerre ni conséquence native.
Ce n'est pas un nouveau CB substitué à une revendication.

Le helper natif d'autorisation est copié **uniquement dans la sortie privée**, sous
un identifiant original de RW, en remplaçant seulement les références `scope:actor`
et `scope:recipient` par deux alias propres à la capture. L'inversion du nom et de
ces substitutions retrouve ses octets d'origine, commentaires et chaînes inclus.
Un helper contenant d'autres références de contexte, `root` ou `prev` est refusé.
Le helper partagé AGOT n'est jamais remplacé. Les alias natifs du CB ne sont pas
écrasés par la capture ; le corps natif s'exécute ensuite dans son contexte original.

Le mod public définit des fallbacks qui refusent la capture. L'adaptateur privé
fournit le clone et son marqueur de disponibilité. Ce marqueur signifie seulement
que les définitions sont fournies, **pas que l'ordre de chargement ou le moteur
ont été validés**. Une absence d'adaptateur ou un mauvais chargement ne doit pas
produire une fausse exemption. Sans adaptateur, le mod principal ne modifie aucune
déclaration ni aucun callback de CB natif.

G1_DECLARATION_LAW_SOURCE_RECEIPT.json publie seulement chemins relatifs, empreintes
et lignes des deux fichiers déjà fournis. Les quatre entrées AGOT strictement
vérifiées par le générateur restent les mêmes ; aucune nouvelle collecte demandée.
Version déclarée 0.5.2.1 / support 1.19.0.6, exécutable/DLC toujours non vérifiés.

## Données enregistrées, pas de condamnation

Il faut les scopes natifs de guerre/attaquant/défenseur, le vrai `claim_cb`, les rôles
principaux exacts et deux pairs féodaux vivants avec le même suzerain direct. Aucun
contexte manquant n'est reconstruit depuis une recherche de guerres ultérieure.
Le relevé personnel de l'attaquant fige schéma/numéro, guerre, parties, suzerain et
titre d'autorité, date de lecture et phase `claim_cb_on_declaration_prefix`.

Il conserve les drapeaux d'interdiction interne/totale observés (priorité à la totale)
et le résultat du helper natif complet, notamment ses exceptions contractuelles :

- `permission_required` : interdiction relevée et autorisation exigée par le helper.
- `native_exception` : interdiction relevée mais helper natif ne demandant pas d'autorisation.
- `no_ban` : ni interdiction relevée ni besoin d'autorisation dans ce contexte.
- `inconsistent` : besoin d'autorisation sans interdiction correspondante relevée.

Aucun de ces états ne prouve l'utilisation ou la consommation d'un hameçon, le
choix effectivement envoyé par l'interface, une infraction native ou une culpabilité.
Une exemption n'est pas un droit universel de déclarer n'importe quelle guerre.
Les restrictions indépendantes restent celles du vrai CB et de l'interaction native.

Un relevé existe au maximum une fois par guerre exacte chez son propriétaire,
y compris après expiration de sa lecture : un callback répété ne peut pas remplacer
le contexte initial par une loi modifiée plus tard. La lecture expire après 365
jours sans renouvellement. Le reçu expiré reste inerte tant que cette guerre est
active pour empêcher une reconstruction tardive ; l'entretien mensuel le termine
après expiration et disparition de cette guerre. La mort du propriétaire termine
l'histoire : pas de transfert de connaissance, autorité ou culpabilité.

## Liaison aux réponses du suzerain

Après initialisation du dossier W3 et avant sa notification, un lecteur cherche
un relevé **déjà existant**, retenu et unique, avec guerre, parties, suzerain et titre
exactement correspondants. Il attache pointeur et numéro ; il ne crée jamais de
relevé de remplacement. Zéro correspondance, plusieurs correspondances ou changement
d'autorité : aucune liaison, sans pénalité ni qualification par défaut.

Le suzerain initial, encore autorisé à lire ce dossier W3, peut voir une ligne
conditionnelle sur ce relevé. Le lecteur vérifie type, propriétaire, numéro, phase,
parties/guerre/autorité et rétention. Il ne relit pas les lois actuelles et ne rappelle
pas le helper pour réinterpréter le passé. Aucun journal, clause privée ou nouveau
motif de sanction native n'est donné à un tiers ou à un successeur. L'absence de ligne
ne signifie pas « guerre légale ». Ces données ne changent ni les gardes ni les effets
d'opinion/intervention déjà livrés dans W3.

## Limites temporelles et installation

La position **avant le corps scripté natif de ce callback** est vérifiée par les
octets. La position relative aux autres callbacks du moteur, à Mega Wars, à la
validation/consommation d'un hameçon et au `on_accept` de l'interaction reste inconnue.
Si le CB n'offre pas encore les scopes attendus ou si sa capture arrive après
l'acceptation, il peut n'y avoir aucun relevé ou aucune liaison. Ne pas déplacer
silencieusement la capture vers `on_accept` et ne pas requalifier le contexte courant
comme une loi historique pour faire apparaître une ligne.

L'adaptateur **0.0.3** dépend de Real Westeros et contrôle les empreintes de **douze**
sources originales. Sa sortie privée contient désormais trois fichiers de code :
déclaration native adaptée, vrai `claim_cb` avec son appel préalable, clone du helper
sous identifiant RW. Aucun de ces originaux/derivés propriétaires n'est dans le ZIP
public. Le mod public contient seulement les sources originales et le générateur.

Pour la campagne finale seulement : remplacer entièrement l'ancien dossier de
l'adaptateur par une génération neuve ; ne pas superposer les anciens fichiers.
Installer AGOT, Real Westeros du même ZIP/commit, puis l'adaptateur. N'activer aucun
autre diagnostic/override G1 ni mod concurrent remplaçant `declare_war_interaction`
ou `claim_cb`. Ne pas supposer compatible un playset non testé. Les fichiers de
l'installation AGOT ne sont jamais modifiés par le générateur.

Les tests inspectent les vrais scripts originaux et rejettent les mutations de
contexte, rétention, identité, reconstruction tardive ou mutation native. Ils
vérifient aussi les inversions byte pour byte du CB et du helper, UTF-8/CRLF,
les commentaires/chaînes préservés, sources ambiguës et double patch. Ce sont des
contrôles source, pas une simulation Python du droit ou des guerres.

## DECLAW-01…09 — tous différés à la campagne finale

1. Mod de base seul et ancien adaptateur : pas de fausse capture ou exemption ;
   disponibilité déclarée distincte du chargement effectivement observé.
2. Adaptateur neuf, réelle revendication entre pairs : scopes/CB/parties/autorité et
   lecture au callback exact ; établir l'ordre réel face aux callbacks AGOT/interaction.
3. Interdit interne/toutes guerres, aucune interdiction, exception contractuelle et
   hameçon sélectionné ou non : comparer au helper natif, sans inférer l'utilisation
   d'un hameçon à partir du simple besoin d'autorisation.
4. Changement de loi/contrat entre déclaration et lecture : le relevé initial ne change
   pas ; contexte incohérent ou non observé reste distinct d'une infraction.
5. Rejouer le callback avant/après expiration : pas de remplacement ou nouvelle date,
   y compris pendant une guerre de plus d'un an ; sauvegarde/rechargement aux deux étapes.
6. Liaison W3 : zéro/une/plusieurs correspondances, ancien numéro ou autre guerre,
   suzerain ou titre ; aucune association choisie arbitrairement, aucune capture tardive.
7. Lecture par autre personnage/successeur, rétention expirée, décès et nettoyage :
   pas d'héritage de connaissance ou d'autorité, aucune prolongation à la lecture.
8. Annulation, invalidation et absence de scopes : pas de capture inventée ; aucun coût,
   claim, peine ou guerre rejoué ; le corps natif fonctionne comme dans le témoin.
9. Victoire/paix/défaite, Mega Wars, autres CB/gouvernements et volume humain/IA :
   régression AGOT, trois fichiers privés isolés et absence de code propriétaire public.
