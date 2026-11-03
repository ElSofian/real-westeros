# G1 — Réponses du suzerain au défi déclaré

**Sources CK3 expérimentales, module privé isolé, aucun test moteur.** Cette tranche
RW-004 relie le choix natif de défi à une véritable décision du suzerain : ignorer,
censurer ou demander la fin des hostilités. Elle ne force aucune paix, confiscation,
révocation ou sanction familiale. **W1…W5 et AI4 restent ouverts, +0 point** : pas de
qualification historique de légalité, de chemin autonome d'initiation IA ou de résultat
G1 prouvé. Développement 62/80, validation moteur 0/20, total 62/100.

## Entrée depuis la déclaration native

Le générateur de G1_NATIVE_CHOICE.md ajoute désormais trois fragments originaux :
une alternative de garde, un send_option, puis un appel à `rw_uw_notice_effect` à
la toute fin du `on_accept` natif. Leur retrait retrouve les octets exacts de la
définition d'origine, y compris UTF-8/CRLF internes. Le corps natif d'acceptation,
les CB/coûts/autres restrictions et tous les callbacks AGOT de guerre restent intacts.
Le générateur n'ajoute pas d'on_action global et ne réexécute aucune conséquence native.
La sortie générée contenant le code AGOT reste strictement privée.

L'appel exige toujours le choix explicite et aucun hameçon sélectionné, le contexte
courant des deux pairs féodaux et le helper natif de l'interdiction. Il recherche
**exactement une guerre native active de type claim_cb**, avec cet acteur comme
attaquant principal et ce destinataire comme défenseur principal. Zéro guerre,
plusieurs correspondances, autre CB ou rôles modifiés : aucune réaction n'est créée.
Les autres CB proposés par la fenêtre gardent le choix expérimental de défi mais
ne sont pas couverts par cette première réponse.

C'est l'observation d'un **choix de défi et du contexte au callback d'acceptation**.
Ce n'est pas une preuve de la loi à l'instant moteur où la guerre commence. Si les
callbacks changent la hiérarchie ou démarrent la guerre après cet appel, la réaction
peut ne pas être créée. Ne pas reconstruire une infraction à partir de cet échec,
d'une loi consultée plus tard ou d'une guerre simplement présente dans l'itérateur.
Aucun crime, raison d'emprisonnement, aveu ou culpabilité héréditaire n'est créé.

## Un dossier personnel, une réaction par guerre

Une StoryScope originale appartient à l'attaquant. Elle fige le schéma/numéro local,
la référence de guerre, les parties, la personne du suzerain, son titre d'autorité,
la date d'observation et la provenance `native_choice_accept`. Les événements
conservent ces mêmes identités ; chaque effet revérifie numéro, propriétaire, guerre,
parties principales, suzerain direct et détenteur du titre. Un héritier, nouveau
suzerain, autre guerre entre les mêmes personnages ou CB modifié ne remplace jamais
silencieusement ce contexte. Les acteurs doivent encore être qualifiés/libres pour
agir ; le suzerain mort, dépossédé ou emprisonné n'exerce pas cette autorité.

La création recherche d'abord les histoires déjà possédées par cet attaquant pour
cette guerre exacte, y compris les reçus fermés et les fenêtres expirées. Un deuxième
callback ne peut pas répéter la réaction ou l'opinion. Aucun index global, drapeau
sur la guerre, balayage de tous les personnages ou plafond d'interactions utiles.
Le numéro augmente uniquement après vérification de la création de l'histoire.

Le dossier a une fenêtre totale fixe de quatorze jours, dont sept jours pour la
première décision. Demander un arrêt ouvre au maximum sept jours de réponse sans
renouveler les quatorze jours d'origine. Les gardes ferment les actions dès expiration,
même avant l'entretien mensuel. Celui-ci ferme les fenêtres périmées **sans peine**
et supprime les dossiers dont la guerre exacte n'est plus active. Un reçu fermé
reste inerte tant que sa guerre est active, pour dédupliquer après rechargement,
changement de suzerain ou longue guerre ; ce n'est pas un nouveau droit d'action.
La mort du propriétaire termine l'histoire, sans transmission de connaissance ou
culpabilité. La persistance des WarScope, les bornes temporelles et cette suppression
restent à démontrer dans CK3. Aucun journal historique permanent n'est ajouté.

## Décisions et conséquences réelles dans les sources

Le suzerain, humain ou IA, a trois choix utilisant les mêmes gardes et effets :

- **Ignorer** : ferme la réaction sans coût, opinion ni changement de guerre.
- **Censurer** : ferme d'abord la réaction, puis ajoute son opinion de désapprobation
  envers cet attaquant, −10 pendant deux ans, et lui envoie une notification personnelle.
  Ce n'est ni une publicité à tout le royaume ni un motif de sanction native.
- **Exiger la fin des hostilités** : consomme sa décision et adresse un événement
  à l'attaquant. L'ordre seul ne change ni la guerre ni un droit natif.

L'attaquant peut **accuser réception**, sans promesse, aveu, soumission ou paix,
ou **refuser ouvertement** : fermeture du dossier avant une opinion de désapprobation
du suzerain de −15 pendant deux ans. Le suzerain reçoit une notification distincte.
Le silence ne produit aucune peine automatique. Les règles de paix natives restent
à la disposition des belligérants ; cette tranche n'envoie pas de proposition native
et ne prétend pas avoir obtenu leur accord. Refus et censure sont des alternatives
dans un même dossier, pas une double peine pour la même réponse. Plusieurs guerres
restent des affaires différentes ; les règles natives d'empilement des opinions
ne sont pas réécrites.

L'IA du suzerain pondère ses choix par sa charge de guerre, sa réserve d'or et son
opinion personnelle de l'attaquant, avec des traits secondaires. Les traits modifient
seulement les poids, jamais les gardes ou conséquences. Elle peut tolérer le défi,
exprimer un désaccord ou faire une demande ; rien n'impose toujours la même réaction.
Les choix du vassal utilisent aussi les mêmes effets humain/IA. **Cela ne fournit
pas l'initiative autonome d'une guerre interdite**, dont le send_option natif reste
non démontré pour l'IA. G4 et AI4 ne sont pas validés par ces événements.

## Distribution et vérifications hors jeu

Les sept templates originaux et le générateur sont inclus dans le ZIP sous
`experiments/` et `tools/`, sans activation dans le mod principal. Le générateur
vérifie toujours les trois mêmes empreintes AGOT. G1_ROYAL_RESPONSE_SOURCE_RECEIPT.json
contient seulement chemins relatifs, empreintes et positions de marqueurs pour le
contexte de guerre de l'acceptation native et le stockage natif de référence de guerre.
Aucun original AGOT, sauvegarde, chemin personnel ou service payant n'est ajouté.

Les tests vérifient la préservation des octets natifs, la position unique de l'appel
après le corps natif, la structure et les localisations du module original, l'exacte
guerre/parties/autorité, les fenêtres et tours, la consommation avant opinion, les
répétitions et les chemins négatifs. Des mutations de cible, suzerain, numéro,
garde d'ambiguïté, délai et opérations natives interdites sont rejetées. Ce sont
des vérifications des vrais fichiers CK3, pas une simulation Python des réactions.

## G1ROYAL-01…10 — tous différés à la campagne finale

1. Déclaration avec défi d'une vraie revendication, témoin sans candidat et voie
   normale/hameçon : réaction seulement dans le chemin explicitement sélectionné.
2. Ordre des callbacks, contexte réel du `on_accept`, rôles principaux et CB ;
   aucune réaction sur échec/annulation/autre CB ou correspondance absente/ambiguë.
3. Ignorer, censurer et demander l'arrêt : opinion exacte, notification personnelle,
   aucune fin de guerre ou peine native, aucune publicité ajoutée à d'autres personnages.
4. Réception de l'ordre : distinguer accusé de réception, refus et silence ; aucune
   paix ou promesse inventée, absence de peine sur silence, refus une seule fois.
5. Même décision/callback répété, rechargement et dossier fermé pendant guerre longue :
   jamais seconde opinion ou nouvelle décision pour cette même guerre.
6. Changement de suzerain/titre/parties principales, décès et captivité : pas de
   transfert automatique d'autorité ni de culpabilité, anciennes fenêtres inertes.
7. Jour limite des sept/quatorze jours, notification perdue et entretien mensuel :
   pas de renouvellement des délais ni action après expiration.
8. Fin native puis autre guerre entre les mêmes personnes : pas de confusion de
   WarScope, suppression du vieux dossier et nouveau dossier seulement si nouvelle
   déclaration admissible ; victoire/paix/défaite ne signifient pas obéissance à l'ordre.
9. Décisions IA↔IA/IA→humain avec différentes réserves, opinions et charges : accès
   identique, décisions variables, aucun scan global ; mesurer le volume en campagne.
10. Régression CB/coûts/hooks/Mega Wars/prisonniers et source privée/distribution :
    corps natif toujours préservé, candidat seul activé, mod principal inchangé.
