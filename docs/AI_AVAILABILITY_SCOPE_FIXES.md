# Scope des filtres de disponibilité IA

**6 novembre 2026 — correction source, aucun test moteur.** RW-010/RW-009,
**+0 : développement64/80, validation CK3 0/20, total64/100**. AI4 reste ouvert :
ce correctif n'ajoute pas l'initiative de guerre autonome encore manquante.

Neuf filtres `ai_potential`, dans sept fichiers d'interactions, entouraient leurs
conditions par `scope:actor`. Ce filtre est évalué sur le personnage candidat,
avant la sélection du destinataire ; l'alias nommé n'y est pas fourni d'office.
Les conditions évaluent maintenant directement ce personnage courant.

Cela concerne réconciliation, services immédiat/différé, services contre faveur
immédiat/différé, allégation, retenue militaire, engagement dynastique et relais
de rumeur. Les conditions de capacité, engagements actifs et cooldowns gardent
exactement leur contenu. Les helpers concernés n'exigent pas d'alias acteur ou
destinataire. La comparaison complète des fichiers au baseline confirme que
seuls les neuf entourages de scope sont retirés.

Cibles du suzerain direct, fréquence12, poids, visibilité, validité à l'envoi,
consentement et effets restent identiques. Le champ IA existant est conservé ;
aucune condition IA n'est déplacée dans la visibilité du joueur. Aucune recherche
mondiale, dépense, revendication, sanction ou action native n'est ajoutée.

Le contexte est déclaré explicitement dans la source du validateur libre
[ck3-tiger v1.19.0](https://github.com/amtep/tiger/tree/v1.19.0),
`src/ck3/data/interactions.rs`, autour des lignes280–293 : les filtres sont enracinés
sur un personnage sans autres scopes nommés prédéfinis. Les sources AGOT reçues
utilisent aussi des conditions directes dans `ai_potential`, notamment
`common/character_interactions/00_vassal_interactions.txt`, autour de la ligne859.
Aucune condition native de ce fichier n'est copiée dans le projet.

Le validateur RW ajoute un contrôle ciblé de la forme fautive : un filtre qui
commence directement par un entourage `scope:actor` ou `scope:recipient`. Les
commentaires/chaînes sont ignorés et le numéro de ligne est signalé. Les références
aux acteurs dans les autres phases de l'interaction restent autorisées. Ce
contrôle ne résout pas les dépendances de scopes générales ou les liaisons
conditionnelles ; une forme qu'il accepte n'est pas une preuve de validité moteur.

Sept tests supplémentaires couvrent les neuf conditions attendues, les helpers,
les cibles/fréquences, la réintroduction du défaut, les commentaires/chaînes,
les phases d'interaction ordinaires et le validateur intégré. L'ancien test de
bypass de réconciliation mute désormais le nouveau filtre, toujours avec le
même contrôle d'éligibilité partagée.

Même binaire Tiger épinglé par GOLD_DEBIT_SOURCE_RECEIPT.json, mêmes sources
privées partielles et fixtures explicitement synthétiques : **les neuf alertes
de scope IA passent à zéro**. Il reste une alerte stricte dans l'intake des
complots et d'autres diagnostics ; aucun acquittement global. Le binaire, les
sources natives et le rapport privé restent hors dépôt/distribution. Ni
installation réelle, ni déclenchement du planificateur, ni performance démontrés.

Dans la campagne finale, observer les neuf initiatives IA↔IA existantes, les
exclusions d'âge/guerre/prison/engagements/cooldowns selon chaque action, leur
fréquence et leur résolution. Vérifier les actions du joueur et l'absence de
nouveau spam. Grouper avec les scénarios prévus, sans lancement intermédiaire
ou relancement par interaction (démarrage CK3 7–10minutes).

Suite : examiner l'alerte restante de participant dans l'intake des complots,
en distinguant scope facultatif et obligatoire ; corriger un défaut démontré,
sans suppression générale. Les dépendances J4/J5 et G1 restent visibles.
