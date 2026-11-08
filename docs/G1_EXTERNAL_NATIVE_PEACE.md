# Intervention négociée du lige dans une guerre extérieure

Actualisation du même adaptateur PRIVATE0.0.10. G1_EXTERNAL_MEDIATION.md ajoute
une sollicitation du protecteur avec accord personnel du lige avant réutilisation
du worker ci-dessous. Les tentatives concurrentes sont désormais contrôlées.

Tranche du 8 novembre 2026. **Static-checked**, expérimentale et **non testée
dans CK3**. PRIVATE0.0.10. Baseline et résultat 80/80 source, 0/20 campagne,
delta 0. Les validations moteur restent regroupées dans la campagne finale.

## Capacité native et rôle

La source AGOT épinglée de `stop_attacker_vassal_war_interaction` exige que
l'attaquant soit le vassal direct de l'intervenant. Elle examine notamment la
guerre, la participation de l'intervenant, les ennemis, les délais d'une tentative
précédente et les hameçons. La source n'exige pas un suzerain commun aux deux
camps. Son acceptation ouvre la négociation native et ses événements suivants.

Le dossier extérieur expose désormais cette option au suzerain original du
déclarant. Dans l'exemple Leyton/Dayne, cette capacité revient à Mace. Le rôle
protecteur de Doran conserve les réactions et demandes politiques précédentes.
Une capacité d'intervention supplémentaire pour le protecteur ou un supérieur
nécessite son propre parcours. La proclamation générale de paix reste différée.

La négociation, les éventuelles contreparties d'or ou de faveur, le refus et la
résolution de la guerre restent ceux de CK3/AGOT. Cette inspection de source
justifie le raccordement expérimental. Son fonctionnement dans ce nouveau contexte
extérieur doit encore être observé dans CK3.

## Préparation et validation

Le choix initial de l'autorité doit être encore ouvert. L'identité personnelle,
le parent et son numéro, les chefs principaux, le titre d'autorité et le rôle de
lige doivent correspondre au dossier existant. L'intervenant doit être extérieur
à la guerre. L'attaquant ne peut avoir qu'une guerre dans sa liste locale, tous
CB confondus, pour conserver la garde de ciblage de l'interface native spéciale.

Le choix consomme sa fenêtre initiale et capture la guerre et le titre d'autorité
de la tentative. Il prépare un événement séparé pour le lendemain, avec une
fenêtre technique de deux jours. Cet événement revalide l'identité capturée,
le contexte actuel et les conditions natives avec
`is_character_interaction_valid`. La cible est vérifiée avant et après cette
validation. Une tentative devenue indisponible clôt le dossier et informe le lige.
Une fenêtre technique expirée devient inerte puis est nettoyée mensuellement.

Le choix d'intervention constitue une alternative initiale à la demande politique
simple. Les demandes déjà closes et les accusés de réception conservent leur
état. Les autres autorités conservent leurs propres dossiers.

## Envoi et cible exacte

Avant l'unique `run_interaction`, le dossier est clos avec le résultat
`native_requested` et sa date d'envoi. La fenêtre technique est consommée.
Deux marqueurs personnels de transport d'un jour portent le dossier et son numéro.
Le callback natif exige le contexte actuel, ce dossier consommé, le rôle de lige,
les mêmes acteur et destinataire et l'absence d'une liaison précédente.
Il restaure alors la guerre exacte dans `target` et consomme le transport.

Les transports de l'ancien parcours entre pairs et du nouveau parcours extérieur
s'excluent mutuellement dans leurs gardes d'envoi et de callback. Un envoi sans
callback consommateur nettoie ses propres marqueurs après l'appel. Les conditions
et conséquences natives restent dans le corps natif inchangé. Le statut d'envoi
et la date de liaison sont des faits de dispatch. Ils n'établissent aucun résultat
de paix, paiement, hameçon ou exécution de promesse.

## Adaptateur et vérifications

Le nouveau marqueur de disponibilité reste faux dans le socle. PRIVATE0.0.10 le
fournit avec son préfixe de callback. Un ancien adaptateur ne peut ainsi ouvrir
l'option extérieure. Le générateur vérifie que retirer ses ajouts restitue les
octets natifs. Les quatre sources épinglées et les quatre sorties natives restent
les mêmes familles. Vingt-deux fichiers originaux de runtime sont recensés.
Les sorties contenant le code AGOT restent privées et hors du dépôt.

Huit nouveaux tests de source et un test des fichiers livrés couvrent notamment
les rôles, l'ambiguïté multi-guerres, les dates et numéros, l'ancien adaptateur,
la validation native, les transports croisés, le ciblage et l'expiration. Les
mutations négatives vérifient aussi qu'aucun résultat natif ou coût n'est recopié
dans les nouveaux effets. Les chemins précédents conservent leurs propres tests.

La campagne finale doit vérifier l'événement natif et chacune de ses issues,
les coûts exacts, l'or ou la faveur, le refus, la paix effective, les callbacks
de fin, les rechargements et les changements de contexte pendant la tentative.
Elle doit couvrir les transports absents, périmés ou croisés, l'ancien adaptateur,
les multiples guerres et Mega Wars. L'IA utilise les mêmes gardes et effets.
Ses préférences contextuelles plus complètes restent à développer.
