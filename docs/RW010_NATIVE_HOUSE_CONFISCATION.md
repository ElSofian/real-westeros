# Confiscations de maison — politique dans l’IA native de révocation

**Extension courante :** [POST_CONFISCATION_RESTITUTION.md](POST_CONFISCATION_RESTITUTION.md)
ajoute le cas opératif de retour après révocation acceptée et perte constatée.
Adaptateur0.0.3 : quatre insertions inversibles,29 sources runtime/deux sorties
privées. Le corps natif d'acceptation est conservé avec un suffixe RW ; aucun
coût/effet de révocation rejoué. Le présent guide conserve la description de
l'association canonique/ordre IA initial, qui ne constitue pas à elle seule
une restitution ou un verdict. J4 reste ouvert ; J5 source+2,66/80+0/20.

**Source expérimentale, pas de lancement CK3. Préparation J4, +0 :
développement 64/80, validation en jeu 0/20, total 64/100.**

## Voie implémentée

La révocation AGOT calcule déjà son score IA sur un titre précis : sa préférence
active de rang lit `scope:landed_title.tier`. Le nouveau chemin ne transmet donc
aucun titre à `run_interaction`. Il laisse le moteur sélectionner les candidats,
valider et envoyer son interaction native, payer ses coûts et résoudre le refus,
la résistance ou l’acceptation.

Un dirigeant féodal adulte, libre, au moins roi, disposant de la loi de révocation
peut engager une politique envers la maison exacte d’un vassal direct adulte féodal.
Sa propre maison est exclue. L’ordre est gratuit et peut être arbitraire : aucune
raison native, culpabilité personnelle ou condamnation héritée n’est créée.
L’IA préfère commencer en paix avec des réserves, une opinion hostile et un motif
personnel natif de révocation contre le représentant ; ce choix ne donne pas de
motif contre les autres membres. Les conditions d’exécution restent partagées.

L’histoire personnelle fige maison, dirigeant, titre d’autorité et date. Sa fenêtre
initiale est de **180 jours**, sans renouvellement à la lecture ou au choix répété.
Un seul ordre actif par même dirigeant/maison, sans plafond global de maisons.
La mort du propriétaire termine l’histoire ; le bonus vérifie à chaque lecture
son autorité, sa situation, sa loi et la fenêtre. Entretien mensuel des histoires
invalides. Changement de maison/cadet ou de juridiction : aucun suivi des anciens
membres, aucune poursuite dans une autre maison ou chez un autre suzerain.

Le retrait gratuit passe par un membre de la maison visée et termine seulement
l’intention personnelle. Il ne répare pas les révocations déjà faites, ne rembourse
rien et ne protège pas des initiatives natives indépendantes. Expiration/retrait
ne sont ni restitution ni restauration J5.

## Adaptateur privé et gardes

```sh
python tools/build_g3_native_confiscation.py --agot-root <AGOT> --output <nouveau-dossier-prive>
```

Le générateur vérifie le fichier AGOT de révocation épinglé par hash et les versions
déclarées 0.5.2.1 / support1.19.0.6. Il émet sa définition native adaptée et un marqueur
RW de disponibilité. Le mod public contient **22 sources runtime originales**, non dupliquées
dans l’adaptateur ; leurs empreintes figurent au reçu. Sans adaptateur, le fallback
refuse la création d’ordres et le nouveau bonus reste nul.

Une seule insertion originale ajoute `rw_hc_native_priority_value` après la base et
avant les modificateurs IA natifs. Valeur **0 sans ordre exact/contexte valide**, sinon
**+1500** : une priorité, pas une obligation d’agir ni une garantie de score final positif.
Les modificateurs natifs, dont facteurs nuls, relations, risques et réticences régionales,
restent présents, sans réécriture. Leur calcul effectif doit être vérifié dans CK3.
Les corps natifs originaux de validité, sélection du titre, coûts, acceptation et
refus sont préservés. La version0.0.2 ajoute aussi un préfixe metadata-only à l’envoi
et au refus ; retirer PREFIX/BEFORE/AFTER restaure toute la définition native.
[RW010_CONFISCATION_TRANSFER_RECEIPTS.md](RW010_CONFISCATION_TRANSFER_RECEIPTS.md)
décrit la demande et son association au transfert observé, sans verdict causal.

Le candidat doit être un titre actuellement détenu par le destinataire, comtal ou
supérieur, non titre foncier abstrait ni titre de famille noble ; destinataire
féodal, vivant et vassal direct de l’émetteur, maison exacte. Aucune recherche mondiale,
aucun transfert direct, crime, trait, hook ou appel d’interaction forcé. Les recherches
de politique visitent seulement les histoires de l’acteur proposé par l’IA native.

**La sortie contient du code AGOT : PRIVÉ, ne jamais publier/committer/redistribuer.**
Installer AGOT, puis Real Westeros du même commit, puis cet adaptateur. Le marqueur
ne démontre pas le load order. Ne pas cumuler avec un autre override de
`revoke_title_interaction`. L’adaptateur de guerre vise d’autres définitions, mais
leur combinaison reste à vérifier avec tout le playset lors de la campagne finale.
Le générateur ne modifie aucune installation et refuse une destination existante,
interne au dépôt/source ou des entrées symboliques/modifiées.

## Accès joueur et IA ; limites J4/G3

L’ordre et son retrait sont accessibles aux deux. Le joueur choisit les titres et
envoie les révocations par la fenêtre native habituelle ; l’ordre ne joue pas à sa
place. L’IA utilise son propre choix natif, dont seule la priorité conditionnelle
change. Les droits, coûts et conséquences de chaque révocation restent natifs.
La création d’un ordre n’atteste aucun envoi ou titre confisqué ; aucun reçu de
sanction exécutée n’est fabriqué à partir d’un score IA.

| Route G3 | Portée de cette mesure |
|---|---|
| Octroi | Un titre déjà octroyé peut être candidat natif ; aucun veto sur les octrois futurs. |
| Héritage | Un titre déjà hérité peut être candidat natif ; aucune modification de la succession. |
| Élection | Le titre d’un élu reste soumis aux gardes natives et aux exclusions du candidat ; aucune modification des listes électorales. |
| Conquête | Un titre déjà acquis peut être candidat natif dans la juridiction actuelle ; aucune modification des CB, conquêtes ou changements de guerre. |

Les voies spéciales d’AGOT, les gouvernements exclus, les titres non admissibles,
la suppression de noblesse et l’interdiction de possession pendant cinquante ans
ne sont pas couverts. **J4 reste ouvert**, de même que J5. La source lève la nécessité
supposée d’une sélection externe de titre pour cette approche IA ; elle n’établit
ni son déclenchement effectif, ni une couverture universelle des routes G3.

## Vérifications et campagne finale uniquement

Tests d’inversion UTF-8/CRLF, natives synthétiques, hashes/versions/entrées/sorties
refusées ; gardes de maison/propriétaire/titre/autorité, expiration/non-renouvellement,
retrait sans restitution, bonus nul hors ordre et absence de mutations natives.
Une génération sur les vrais octets reçus avec un descripteur de fixture des versions
rapportées n’est ni une installation vérifiée ni un test moteur.

**HCONF-01…08, tous NON EXÉCUTÉS**, à grouper dans la campagne finale, sans lancement
intermédiaire demandé (coût propriétaire :7–10min par lancement) :

1. Base seule, adaptateur correct et témoin AGOT : activation/load order et absence
   de différence de priorité sans ordre, avec les autres tests du même playset.
2. Ordre joueur et IA, vassaux de même maison : native AI proposée avec titre réel,
   choix/envoi natifs ; distinguer chaque étape d’un transfert effectivement exécuté.
3. Mauvaise maison/cadet, autre suzerain, titre sans bon détenteur/baronnie/titre
   spécial, autre numéro de schéma : bonus nul, protections natives intactes.
4. Refus/révolte/acceptation, coût/tyrannie/relations et choix d’hameçon natifs :
   comparer au menu normal ; aucune pénalité, dépense ou révocation dupliquée.
5. Expiration180j, retrait, décès, captivité, changement de loi/détenteur d’autorité,
   sauvegarde/rechargement : pas de succession, renouvellement ou poursuite illégitime.
6. Origines octroi/héritage/élection/conquête et institutions protégées : gardes natives,
   absence de veto futur et de récupération automatique des terres.
7. Relation amie, moyens insuffisants, guerre/activité et facteurs nuls natifs :
   vérifier le score effectif, le refus d’agir et les fréquences ; rien n’est forcé.
8. Plusieurs ordres/vassaux, volume IA et Mega Wars : mesurer coût des recherches
   locales, spam/résistance et régression AGOT dans cette même campagne.
