# Expressions de localisation corrigées

**6 novembre 2026 — source vérifiée, aucun test CK3.** Correction transversale
RW-010/RW-004, sans nouveau critère achevé : **+0, développement64/80,
validation en jeu0/20, total64/100**.

Le passage de [ck3-tiger v1.19.0](https://github.com/amtep/tiger/releases/tag/v1.19.0)
sur les sources privées partielles signalait 14 erreurs `datafunctions` et trois
avertissements `markup` dans les textes RW. Ces erreurs sont indépendantes des
définitions/ressources manquantes dans cette collecte.

- Les 14 textes français/anglais d'allégation, de retenue militaire et de réaction
  royale contenaient 22 préfixes `[scope:…]`. La localisation attend `[nom_du_scope…]`.
  Seul le préfixe est retiré ; mêmes personnages, méthodes, clés et textes.
- Trois textes anglais d'intention de révocation préfixaient un numéro dynamique
  par un `#` seul. Ce caractère ouvre du balisage. Le doubler (`##`) conserve un
  dièse littéral devant le même numéro, avec sa même expression et son format.

Sept fichiers de localisation sont corrigés, avec leur BOM UTF-8 conservé. Aucune
interaction, condition, pondération IA, mutation de titre, dépense ou conséquence
n'est modifiée. Les scopes de script conservent leur syntaxe `scope:` ; seule leur
référence dans le texte change. Ce correctif ne démontre pas que tous les scopes
seront disponibles au bon moment dans le moteur.

`tools/validate_mod.py` ajoute deux contrôles ciblés sur les valeurs entre guillemets :
préfixe de script dans une expression et nombre impair de dièses immédiatement
suivis d'un crochet d'expression. Les commentaires extérieurs sont ignorés, y
compris après une valeur contenant des guillemets échappés. Les dièses littéraux
échappés, balises ordinaires et tooltips dynamiques restent acceptés. Ce contrôle
ne remplace ni le parseur complet Jomini, ni la résolution des fonctions/scopes.
Ne pas étendre ses conclusions aux expressions qu'il ne reconnaît pas.

Neuf tests couvrent les régressions, formes correctes, échappements, commentaires,
numéros de ligne, intégration du validateur et préservation des références dans
les deux langues. Le validateur autonome inclus dans le ZIP applique aussi ces
règles. Aucun téléchargement de Tiger ou service n'est requis par la CI.

Le même binaire Tiger épinglé dans GOLD_DEBIT_SOURCE_RECEIPT.json a été utilisé
(archive SHA-256 `6d72d276c2b2a953f63221ff8050d1276a085b5a2ffe74977675fdf6e17e9ff3`).
Après correction : **datafunctions14→0, markup3→0** dans ce passage. La collecte
reste partielle, avec des éléments de fixture explicitement synthétiques ; ce
n'est ni une installation CK3, ni une validation sémantique complète. Les autres
diagnostics restent à trier. Aucun binaire, source native ou rapport privé brut
n'est publié. Les sources propres du projet restent dans le dépôt et le ZIP.

Lors de la campagne finale déjà prévue, lire les noms des deux parties dans les
panneaux d'allégation/retenue militaire, les réactions royales du candidat privé,
et les numéros d'observations dans le journal de révocation, en français et en
anglais. Vérifier les logs de localisation et les scopes absents. Grouper ces
lectures avec les scénarios existants : aucun lancement CK3 intermédiaire ou
relancement par texte (démarrage7–10minutes).

Suite : examiner les alertes de scope restantes dans leur contexte d'appel,
confirmer les erreurs avant de changer le code ; garder J4/J5 et les critères de
guerre ouverts. Ne pas masquer les diagnostics par des suppressions générales.
