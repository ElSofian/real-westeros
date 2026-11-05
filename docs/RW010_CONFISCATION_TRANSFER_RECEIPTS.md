# Demande native et transfert de titre observé

**Source expérimentale, aucun test CK3. Préparation J4/J5, +0 :64/80 source,
0/20 moteur, total64/100. Ce chemin ne restaure aucun titre et ne valide pas J5.**

Le score IA de confiscation n’est pas un résultat. Ce chemin associe une demande
native concrète à un changement de détenteur effectivement observé par le callback
de titre. Il ne rejoue aucune révocation et ne fabrique aucun motif de sanction.

## Capture et observation

L’adaptateur privé **0.0.2** conserve le bonus IA et ajoute deux appels metadata-only :
au début de `on_send`, capture du titre sélectionné encore détenu par le destinataire ;
au début de `on_decline`, fermeture de l’association avant le corps scripté natif du refus.
Si le titre manque au refus, toutes les associations de cette paire d’acteurs
sont fermées conservativement ; aucun titre n’est deviné. Le corps de `on_accept`
reste intégralement inchangé. Le helper de révocation inspecté
gère notamment peines et relations ; il ne fournit pas la position du transfert moteur.
Encadrer ce helper par deux lectures n’aurait donc pas établi un point fiable.

La capture exige un ordre actif de maison unique et les gardes du candidat natif.
Elle mémorise émetteur, ancien détenteur, titre, maison, autorité actuelle et date
sur une histoire personnelle de demande, **30 jours fixes** sans renouvellement.
Une demande exacte déjà active n’est pas dupliquée ; elle n’empêche aucun acte natif.
Expiration ou mort du propriétaire : nettoyage, sans héritage ni peine. Retirer
l’ordre de priorité ne rappelle pas une demande déjà envoyée au moteur.

Un troisième enfant nommé s’ajoute à `on_title_gain`, après les deux lecteurs existants,
sans remplacer leurs effets. Il n’exige pas que les alias natifs actor/recipient/
landed_title ou un marqueur de révocation survivent au callback. Il utilise le nouveau
détenteur natif root, le titre et l’ancien détenteur natifs. Le nouveau détenteur doit
encore posséder ce titre comtal ou supérieur ; l’ancien détenteur doit être vivant,
avec la maison capturée. Une seule demande typée, non expirée, de ce propriétaire,
ce titre, cet ancien détenteur et cette autorité encore détenue doit correspondre.

La demande est consommée **avant** l’écriture d’un fait ou toute proposition UI.
La correspondance n’est pas un identifiant d’opération du moteur : un autre transfert
compatible pendant une demande pendante ne peut pas être exclu par ce seul sous-ensemble.
Le fait décrit donc un **transfert observé associé à une demande**, sans verdict sur
sa cause exclusive, un complot, une condamnation ou une confiscation universelle.
Les héritages d’un ancien détenteur mort et les résultats ultérieurs d’une guerre
après refus ne sont pas associés par ce chemin.

## Un journal, pas un deuxième registre de faits

Le lecteur emploie le journal `story_rw_title_provenance`, son compteur et ses gardes
privées existants : schéma1, titre/parties/date immuables, coalescence d’un jour,
rétention cinq ans et fin au décès. Une entrée équivalente sous sa fenêtre d’un jour
est laissée **entièrement inchangée** : ni duplication, ni association rétroactive,
ni nouvelle date ou prolongation, même si le lecteur ancien l’a créée dans ce callback.
La coalescence peut fusionner deux transitions réelles de même tuple dans la journée ;
ce journal n’est pas exhaustif et ne fournit pas un identifiant de transaction.

Une nouvelle entrée porte une origine explicite `pending_native_revocation_transfer`.
Elle ne crée aucune observation de participant exposé et n’appelle pas le lieur de
dossier privé. L’ancien lecteur de complot conserve toutes ses gardes. Aucun droit
foncier, culpabilité héritée ou consentement de descendant n’est déduit de la note.

Si l’émetteur était souverain à l’envoi et l’est encore, une nouvelle note peut
proposer le **dépôt facultatif existant** au registre foncier. Autorité et maison sont
celles capturées avant le transfert, jamais reconstruites plus tard. Un événement
isolé le lendemain lie les alias du journal, avec numéro/titre/parties/maison/autorité
exacts et un ticket UI sept jours consommé avant ouverture. Les alias natifs ne sont
pas écrasés. Le lecteur de dépôt, les accès/custodies, la rétention centenaire et
les dialogues de restitution existants restent inchangés ; seul un dépôt effectivement
choisi copie leurs faits publics habituels, sans pointeur de demande, dossier ou crime.

## Construction et limites

Même commande que RW010_NATIVE_HOUSE_CONFISCATION.md. Remplacer complètement l’ancien
adaptateur, utiliser Real Westeros du même commit. **19 sources runtime** originales
contrôlées, un fichier AGOT épinglé inchangé, deux sorties privées. Retirer les trois
fragments originaux retrouve tous les octets de la définition native, UTF-8/CRLF et
commentaires compris. Le ZIP public contient le générateur et les bibliothèques
originales ; les définitions natives générées restent privées, non redistribuables.

L’existence de landed_title à l’envoi, l’ordre/composition des callbacks et la
persistance des tickets doivent être confirmés dans le moteur. Une absence ou
ambiguïté produit aucune association ; pas de scan ultérieur, reconstruction tardive,
transfert forcé ou privilège ajouté pour faire fonctionner la capture. J4/J5 restent
ouverts, sans cinquante ans d’interdiction, suppression de noblesse ou restauration.

## HCRECEIPT-01…08 — tous NON EXÉCUTÉS, campagne finale uniquement

1. Joueur/IA, vrai envoi accepté : vérifier les scopes d’envoi, puis l’observation
   de gain, le journal canonique et ses dates ; distinguer association et cause.
2. Refus/résistance : fermeture avant corps natif, aucune entrée imputant la guerre
   ultérieure à une révocation acceptée ; comparer coûts/peines/guerre au témoin AGOT.
3. Autre titre/ancien détenteur/maison/autorité, ancien détenteur mort ou demandes
   multiples : pas d’association choisie arbitrairement ni d’héritage qualifié.
4. Callback répété, demande expirée, ancien adaptateur ou alias absent : aucun fait
   fabriqué, renouvellement ou nouvel envoi ; une nouvelle demande reste distincte.
5. Ancien lecteur TP actif/inactif, entrée équivalente existante : un fait canonique,
   aucune réécriture ou liaison rétrospective au nouvel ordre de maison.
6. Dépôt humain/IA ou abstention, ticket expiré/ancien numéro : accès exact, une seule
   proposition, aucun pointeur privé copié au registre, aucune restauration automatique.
7. Sauvegarde/rechargement aux étapes demande/observation/dépôt, décès et succession :
   demandes et notes personnelles non héritées ; garde institutionnelle seulement après dépôt.
8. Titres issus d’octroi/élection/conquête, Mega Wars et charge : protections natives,
   fenêtres et coût des recherches locales ; pas de veto d’acquisition implicite.

Grouper avec HCONF et les autres tests du même playset. Le lancement propriétaire
prend7–10minutes : aucun lancement intermédiaire ou par scénario n’est demandé.
