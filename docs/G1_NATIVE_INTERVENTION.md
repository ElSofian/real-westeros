# W3 — Réaction discrétionnaire et demande native d'intervention

**6 novembre : premier essai moteur en échec sur la cible native.** Guerre réelle
et refus observés, mais `run_interaction` perd `target` et la lettre perd défenseur/
guerre. [G1_FIRST_ENGINE_TRIAL.md](G1_FIRST_ENGINE_TRIAL.md) décrit les preuves et
le correctif privé0.0.6, non testé dans CK3 : préfixe dans le vrai `on_accept`,
marqueurs personnels éphémères/exacts, aucun argument moteur inventé. Préparation
historique ci-dessous ; +0,score68/100. Ne pas confondre demande et paix exécutée.

**Scripts CK3 originaux intégrés ; vérification statique seulement, aucun test moteur.**
Le suzerain peut désormais choisir une tentative native de négociation pour arrêter
la guerre de revendication du dossier. Ce chemin complète la décision de tolérer,
censurer ou adresser une demande politique sans action native. Une demande envoyée
n'est ni une négociation confirmée, ni une paix acceptée, ni une sanction exécutée.
**W3 : source seulement, +2 points ; développement 64/80, moteur 0/20, total 64/100.**
G1, W1/W2, W4/W5, l'initiative autonome de guerre AI4 et G3 restent ouverts.

## Intégration et activation

Les douze fichiers originaux (triggers, effets, histoires, événements et EN/FR) sont
maintenant dans `mod/real_westeros`. Leur présence n'ajoute aucun on_action global,
aucune politique de déclaration automatique et aucun override natif. L'entrée reste
l'appel gardé du `on_accept` du candidat privé de G1_NATIVE_CHOICE.md. Sans cet
adaptateur, les déclarations ordinaires ne créent aucun de ces dossiers.

Le générateur privé valide les douze sources publiques, mais ne les recopie plus :
sa sortie 0.0.3 contient les overrides privés de déclaration et du callback de
claim_cb, un clone de helper en lecture seule et le descripteur dépendant de
**Real Westeros**. Voir G1_DECLARATION_LAW_CONTEXT.md pour cette extension W1 à +0. Installer AGOT, puis Real Westeros, puis cet
adaptateur privé pendant la campagne finale. Il reste mutuellement exclusif avec
les anciens diagnostics G1 et tout autre override de déclaration. Le ZIP public
ne contient jamais la définition AGOT générée ; aucun changement des fichiers
installés n'est automatique. Les empreintes des sources publiques attendues sont
consignées dans le reçu privé pour vérifier la bonne version du mod au test.

Le générateur exige désormais quatre fichiers AGOT aux empreintes exactes :
interaction de déclaration, helper de l'interdiction, CB de revendication et
`common/character_interactions/00_vassal_interactions.txt`. Le dernier est vérifié
comme dépendance native ; il n'est ni modifié ni copié dans la sortie. Le reçu
G1_NATIVE_INTERVENTION_SOURCE_RECEIPT.json contient uniquement chemins relatifs,
empreintes et lignes. L'événement de suivi localisé dans la collection CK3 n'établit
pas à lui seul la résolution effective de tous les fichiers du playset AGOT.
Version déclarée AGOT 0.5.2.1 / support 1.19.0.6 ; exécutable CK3 non vérifié.

## Voie native choisie

`stop_attacker_vassal_war_interaction` est l'interaction native du suzerain envers
l'attaquant, avec interface spéciale `interfere_in_war`. Elle utilise un destinataire
vassal direct, un acteur non participant, les protections de hameçon fort et le
délai d'opinion natifs. Son `can_be_picked` vise une guerre dont le destinataire
est attaquant principal. Son acceptation démarre `vassal_interaction.0001` ; le
`auto_accept` de l'interaction **ne signifie pas acceptation de la paix**.
Les suites natives prévoient acceptation, contrepartie et refus. Les opinions,
faveurs, paiements, réactions du joueur, délais et éventuelle paix restent natifs.

Cette tranche ne copie ni l'interaction ni ses événements. Elle ne déclenche pas
directement leurs événements et n'appelle pas `end_war`, `start_war` ou leurs
helpers. Aucun prix, opinion native, consommation de hameçon, résultat ou peine
n'est reproduit. `run_interaction` utilise uniquement les arguments source-localisés
`interaction`, `actor` (le suzerain exact), `recipient`, `send_threshold = decline`, sans
`execute_threshold` ni argument `target` inventé.

## Contexte exact et garde d'ambiguïté

Le dossier existant doit correspondre à la guerre de revendication native encore
active, au numéro, au propriétaire initial, aux parties principales, à la personne
du suzerain et au détenteur du titre d'autorité. La fenêtre initiale du suzerain
et la durée totale de quatorze jours restent applicables. Humain et IA ont les mêmes
conditions ; les poids IA utilisent moyens, charge de guerre et opinion personnelle.

Pour ce raccourci automatisé, l'attaquant doit participer à **une seule guerre au
total**, qui doit être celle du dossier. Filtrer seulement les guerres de revendication
laisserait une autre guerre sélectionnable par l'interface spéciale. Cette restriction
conservatrice est une garde de cible, pas un quota d'interactions : le menu natif
habituel reste disponible dans les situations plus complexes. Aucun choix automatique
entre plusieurs guerres, aucune redirection vers le défenseur.

Le choix consomme le tour `pending` en `native_queued`, sans renouveler les quatorze
jours ni appliquer la censure de l'autre branche. Il programme un événement caché
le lendemain. Les rôles natifs `actor`/`recipient` et `target` ne sont liés que dans
ce **nouveau contexte d'événement**, pour ne pas remplacer la cible de revendication
de la déclaration encore en cours. À cette étape, les identités, autorité, guerre,
unicité et non-participation du suzerain sont revérifiées, puis
`is_character_interaction_valid` interroge la véritable interaction native.
La cible de contexte doit toujours correspondre à la guerre exacte après validation.

Si le contrôle réussit, le reçu devient fermé/`native_requested`, avec date d'envoi,
et perd sa fenêtre d'action **avant** l'unique appel natif. L'appel peut ne rien
déclencher ; aucun succès n'est déduit de son retour. Si les gardes échouent alors
que le ticket personnel reste identifiable, il devient `native_blocked`, sans
opinion, coût ou appel natif, avec une notification personnelle. Les tickets devenus
illisibles ou dont le propriétaire meurt suivent le nettoyage normal sans peine.
Les reçus inertes sont conservés pour leur guerre active, comme les autres réactions,
empêchant une répétition même après rechargement. Aucune relance aveugle après un
retour natif sans résultat. Un nouveau souverain n'hérite pas de ce ticket personnel.

## Limites à démontrer dans CK3

La propagation de `scope:target` vers l'interface spéciale n'est **pas démontrée**
par les sources de `run_interaction`. La garde d'unicité exclut une autre guerre
candidate, mais ne prouve pas que l'API accepte une cible déjà liée ou que sa
validité sans sélection de fenêtre réussit. Un rejet reste un rejet : ne pas
supprimer les contrôles pour faire fonctionner le bouton. La campagne finale doit
observer séparément validation, envoi, négociation, contrepartie/refus et issue.

Le droit applicable à l'instant de déclaration n'est toujours pas établi par ce
callback : la réaction répond au défi explicitement choisi et au contexte connu,
pas à une condamnation native. Aucun nouveau crime ou pouvoir de confiscation.
L'IA du suzerain peut choisir l'intervention ; cela ne donne toujours pas à l'IA
la capacité autonome de sélectionner le send_option de déclaration interdite.
Aucune compatibilité G1/G4/G5, performance ou sauvegarde n'est déclarée validée.

## NATIVEWAR-01…09 — tous différés à la campagne finale

1. Installation correcte : les sources originales sont dans Real Westeros, seul
   l'adaptateur privé remplace la déclaration ; base seul sans nouveau comportement.
2. Défi d'une vraie revendication, unique guerre, suzerain qualifié non participant :
   choix facultatif, événement du lendemain et **guerre exacte** dans la négociation.
3. Contrôle négatif sans adaptateur, sans défi, autre CB, autre suzerain/titre ou
   autre dossier/numéro : aucune nouvelle tentative native.
4. Ajouter une guerre d'allié ou changer les rôles/la cible entre choix et envoi :
   aucune sélection d'une autre guerre ; blocage sans coût ni censure ajoutée.
5. Hameçon fort du vassal, délai natif d'une précédente intervention, captivité,
   souverain participant ou dépossédé : protections natives préservées.
6. Suite native d'acceptation, contrepartie/faveur/or, refus et réponse joueur :
   comparer au menu AGOT normal, sans paiement ou opinion exécuté deux fois.
7. Répéter le choix, l'événement caché et recharger aux deux étapes : un seul appel,
   reçu préalable, pas de paix annoncée sur un simple retour de fonction.
8. Expiration, décès, remplacement de souverain, guerre terminée ou fenêtre native
   rejetée : pas de succession du ticket, nouveau crime, relance ou peine automatique.
9. Régression victoire/paix/défaite/invalidation/Mega Wars et volume humain/IA :
   comparer au témoin AGOT, mesurer en campagne finale, conserver les limites visibles.

## Migration de l'ancien adaptateur

L'adaptateur privé porte désormais la version **0.0.3**. À la campagne finale,
remplacer entièrement son ancien dossier `rw_g1_native_choice` par le nouveau
dossier généré ; ne pas simplement superposer les fichiers. Les versions précédentes
contenaient leurs propres bibliothèques, qui pourraient sinon masquer celles du
mod principal. Mettre à jour Real Westeros avec le même ZIP/commit et comparer les
douze empreintes du reçu privé aux sources installées. Le générateur ne supprime ni
ne remplace automatiquement aucun dossier d'installation.

### Relevé de déclaration — adaptateur 0.0.3

G1_DECLARATION_LAW_CONTEXT.md documente la capture au début de `claim_cb.on_declaration`.
La version privée 0.0.3 vérifie douze sources originales et produit trois fichiers
privés (déclaration, vrai CB de revendication préservé, clone natif en lecture seule).
Le helper partagé n’est pas remplacé ; seul un identifiant RW est fourni au-dessus
d’un fallback public qui refuse la capture. Ne pas cumuler avec un autre override
de `claim_cb`. Aucun coût ni effet de guerre rejoué ; W1 reste ouvert tant que
l’ordre réel des callbacks n’est pas démontré. Remplacer entièrement l’ancien
adaptateur et mettre à jour Real Westeros avec le même ZIP/commit.
