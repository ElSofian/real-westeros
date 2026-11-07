# W1 — Qualification source de la loi à la déclaration

**Extension ultérieure de la lecture territoriale.**
[G1_TERRITORIAL_LAW.md](G1_TERRITORIAL_LAW.md) décrit les nouveaux contextes de
capture, encore non testés dans CK3. La qualification et les empreintes ci-dessous
correspondent à la version antérieure observée. Les anciennes archives sont
conservées. Le score courant reste80/80 source et0/20 campagne, delta0.

Revue du 7 novembre 2026 sur le code de `15fcec34204377a9c930a392f13460d1b3f7dcc9`.
W1 est qualifié en source pour le chemin livré de revendication entre pairs
féodaux. Développement **74 → 76/80**, campagne finale **0/20**, delta **+2**.
Cette qualification porte sur l'implémentation existante et les observations
déjà réalisées. Les nouveaux contrôles et ce document rapportent ces preuves.

## Loi applicable dans le chemin livré

Le générateur insère la capture en première instruction du vrai
`claim_cb.on_declaration`, avant le corps AGOT et son appel `on_declared_war`.
Le relevé conserve la guerre exacte, les parties, le suzerain direct, son titre,
la date et la phase de capture. L'interdiction totale a priorité sur l'interne.
Les conditions de capture limitent ce chemin aux parties et au CB pris en charge.

Le résultat d'autorisation vient du helper natif complet, cloné sous des alias
propres. Le générateur exige les empreintes natives revues puis vérifie que
l'inversion de ses substitutions restitue les octets originaux. L'exception
contractuelle reste dans ce helper. Les situations de souverain indépendant,
de cible suzeraine et d'administration conservent leur traitement natif. Le
motif lié à la loi bureaucratique japonaise reste également dans le helper.
Le domaine féodal entre pairs est plus étroit que l'ensemble de ces situations.
Les règles indépendantes du CB et de l'interaction continuent leur exécution.

La lecture classe la condition d'autorisation observée en quatre états.

| État | Lecture conservée |
|---|---|
| `permission_required` | Interdiction relevée et autorisation demandée par le helper |
| `native_exception` | Interdiction relevée avec exception reconnue par le helper |
| `no_ban` | Aucune interdiction relevée et aucune autorisation demandée |
| `inconsistent` | Autorisation demandée sans interdiction correspondante relevée |

Le relevé exprime la loi et la condition d'autorisation dans ce callback.
La consommation d'un hameçon reste une opération native à observer séparément.
Les infractions, preuves judiciaires et sanctions ont leurs propres conditions.

## Ce que les observations existantes lèvent

Les essais joueur corrigés et les deux déclarations autonomes de Dorne ont
produit un relevé de déclaration lié au dossier royal de la même guerre.
La liaison exige un relevé déjà présent, unique, de même propriétaire, numéro,
guerre, parties, suzerain et titre. Elle est appelée une fois à l'initialisation
du dossier, avant sa notification. Elle ne possède aucun chemin de capture.
Ces liens établissent que la capture avait précédé cette liaison dans les cas
observés. Le déplacement vers une lecture tardive n'est donc pas nécessaire
pour ces parcours. Les étapes et empreintes des sauvegardes figurent dans
[l'essai joueur](G1_FIRST_ENGINE_TRIAL.md) et
[l'observation autonome](G1_AI_AUTONOMY.md).

Les trois fichiers de loi courants correspondent exactement au reçu privé
utilisé pour l'observation autonome PRIVATE0.0.6.

| Fichier original RW | SHA256 observé et courant |
|---|---|
| `common/scripted_triggers/rw_declaration_law_triggers.txt` | `43328188ead386ea2a3360126e381b4e729cfa2637ed0a055368df5241139de5` |
| `common/scripted_effects/rw_declaration_law_effects.txt` | `3899d1b320007a9c180f8d06c2c37a6e5f1c7c512dea7179204c13cf252c537c` |
| `common/story_cycles/rw_declaration_law.txt` | `349e83d4afd9ba19900b4aa7ff9a35435e28578eb36fb00ea912d5bfefbc178a` |

## Conservation et contrôles négatifs

La capture est dédupliquée par guerre exacte. Son résultat est archivé une fois.
La liaison et la lecture utilisent le relevé historique, avec contrôle de numéro
et d'identité. Elles ne consultent pas une nouvelle loi ou un nouveau contrat.
L'absence d'adaptateur empêche la capture. Une liaison absente, ambiguë, expirée
ou étrangère ne fournit aucune qualification par défaut. La mort termine le
relevé personnel. La rétention et la référence exacte empêchent sa reconstruction
pendant la guerre après expiration de sa fenêtre de lecture.

Les tests existants couvrent ces gardes et les inversions du générateur. Deux
régressions supplémentaires fixent l'association exacte des quatre états à leurs
branches et l'unique copie du résultat précoce vers l'archive. Elles détectent
notamment une inversion des états qui passerait un simple contrôle de présence.

## Validation restante

Les cas DECLAW-01…09 restent à exécuter dans la campagne groupée pour les
exceptions contractuelles, hameçons, changements de loi, rechargements et autres
contextes. La preuve d'ordre ci-dessus se limite aux parcours observés. Les
transitions et clôtures Mega Wars appartiennent à W4, qui reste ouvert avec W5.
La couverture moteur générale et les critères V1–V5 restent ouverts.

L'adaptateur privé courant est PRIVATE0.0.6. Il fournit quatre fichiers dérivés
natifs et vérifie treize fichiers runtime RW ainsi que quatre entrées AGOT.
Le ZIP public livre les scripts originaux et le générateur. L'assemblage privé
est réalisé depuis une même version vérifiée pour la campagne.
