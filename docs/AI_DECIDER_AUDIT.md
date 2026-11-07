# Le personnage qui décide — premier inventaire

## État et périmètre

Relevé du 7 novembre 2026 sur les sources installées CK3 1.19.0.6 et
AGOT 0.5.2.1. **Static-checked**. L'évaluation en moteur des nouveaux poids de
promesses reste à valider pendant la campagne finale.

L'inventaire compte 1 212 définitions après remplacement des fichiers de même
chemin relatif par AGOT. Il conserve les traits cachés, techniques, d'apparence
et de dragons. Ce nombre ne désigne pas 1 212 traits accessibles à un dirigeant
humain. Le relevé ne filtre ni les DLC actifs ni l'accessibilité à un personnage.
Il ne décrit aucun autre mod du playset. Un même nom français peut correspondre
à plusieurs identifiants, notamment Curieux.

| Entrées dans le profil actuel des quatre promesses | Nombre |
|---|---:|
| Contribution directe non nulle à l'honneur ou à l'avidité | 84 |
| Contribution conditionnelle ou non résolue sur ces axes | 2 |
| Aucune contribution directe non nulle déclarée sur ces deux axes | 1 126 |
| Total des définitions recensées | 1 212 |

Le dernier groupe ne constitue pas une liste de traits politiquement sans effet.
Les traits peuvent modifier les opinions, compétences, ressources, conditions ou
autres tendances natives utilisées ailleurs. Ces chemins restent à examiner.
Les deux contributions conditionnelles sont conservées comme telles. Le lecteur
ne substitue jamais zéro à une expression qu'il ne sait pas résoudre.

Tous les traits gardent le statut `context_review = pending` pour la revue
politique complète. Un futur statut « examiné, effet nul » exige une justification
pour la décision considérée. L'inventaire seul n'établit pas cette justification.

## Ce que signifie une contribution

Le profil actuel lit l'honneur et l'avidité agrégés du personnage. Il ne lit pas
une liste exclusive de noms de traits. Les contributions natives des traits et
modificateurs peuvent donc parvenir au profil par ces axes.

Une contribution native n'est pas un bonus final à une option. Les autres traits,
modificateurs, bornes du profil et conditions du dossier interviennent encore.
L'avidité concerne ici la réception du paiement par le prestataire. Le même
coefficient ne convient pas automatiquement à un personnage qui doit payer.
AI_DECISION_CONTEXT.md décrit les quatre options et leurs limites exactes.

Pour chaque trait et chaque décision, la revue doit consigner les éléments suivants.

| Élément | Vérification attendue |
|---|---|
| Identité | Identifiant exact, source effective, catégorie et éventuel caractère technique |
| Personnalité | Axes natifs modifiés et effet réel des axes effectivement lus par l'option |
| Capacités et moyens | Effets pertinents sur compétences, santé, ressources et possibilités |
| Relations | Effets sur les opinions ou réactions déjà calculées par le moteur |
| Conditions | Pistes, niveaux, culture, foi, déclencheurs et autres expressions contextuelles |
| Combinaison | Contradictions avec les autres traits, bornes et risques de double comptage |
| Résultat | Positif, négatif, contextuel, nul justifié ou encore non évalué pour cette option |
| Preuve | Lecture source, contrôle statique, puis scénario moteur séparé |

Les axes recensés sont audace, compassion, énergie, avidité, honneur, rationalité,
sociabilité, vengeance et zèle. Leur présence dans l'inventaire ne signifie pas
qu'ils sont tous consommés par le profil de promesses actuel.

## Autres composantes du décideur

| Composante | Revue prévue | Couverture de ce lot |
|---|---|---|
| Âge | Capacité légale par action, minorité/régence, durée de l'engagement et enjeux de transmission | Bornes d'âge littérales des traits recensées dans le JSON privé, aucun nouveau coefficient d'âge |
| Compétences | Diplomatie, martialité, intendance, intrigue, érudition et prouesse selon l'action | Modifications directes littérales recensées, effets conditionnels à examiner |
| Éducation | Orientation et capacités effectivement apportées | Traits inclus, aucun nouveau poids par éducation |
| Expérience | Pistes, modes de vie et souvenirs pertinents connus du personnage | Traits inclus, pistes et souvenirs à examiner |
| Santé et stress | Capacité, coût personnel prévisible et incompatibilités avec l'action | Quelques modificateurs directs recensés, revue fonctionnelle à poursuivre |
| Rôle | Autorité, responsabilités et devoirs concurrents du souverain, vassal, régent ou conseiller | Hors inventaire des traits, aucune nouvelle règle livrée |
| Objectifs et convictions | Intérêts et convictions représentés dans le jeu, reliés au but de l'option | Revue contextuelle à poursuivre |

L'âge n'attribue ici aucun bonus général de prudence ou d'impulsivité. Aucune
espérance de vie individuelle n'est déduite d'un âge seul. La lecture doit suivre
les règles natives de chaque action et les informations accessibles au décideur.

## Reproduction privée et contrôles

Exécuter `python tools/audit_trait_context.py --help` pour les arguments. Fournir
les deux racines locales CK3/AGOT et une destination privée hors des fichiers
suivis. `--markdown` produit la liste lisible des noms français et identifiants.
Le JSON conserve les chemins relatifs, empreintes, lignes, champs directs et
contributions non résolues. Aucun corps de définition n'est exporté. Les rapports
complets restent privés et ne font pas partie de la distribution du mod.

Le lecteur superpose les fichiers par chemin relatif, résout uniquement les
script values numériques littérales non ambiguës et garde les expressions
dynamiques non résolues. Une définition dupliquée dans des fichiers de traits
survivants, une source absente ou une structure non supportée font échouer le
relevé. Ce lecteur borné n'émule ni le moteur ni son préprocesseur.

Les fixtures originales couvrent le remplacement complet d'un fichier, les
doublons, commentaires/chaînes, constantes, valeurs symboliques, expressions,
pistes, données manquantes, zéro explicite et noms français homonymes.

Cible de qualité AI3/O1. Baseline et résultat **74/80 source, 0/20 campagne**.
Delta **0**. La grille gelée et ses checkpoints restent inchangés. Prochaine
étape du chantier demandé par le propriétaire, examiner les traits de personnalité
et leurs chemins contextuels par option avant d'étendre les coefficients.
