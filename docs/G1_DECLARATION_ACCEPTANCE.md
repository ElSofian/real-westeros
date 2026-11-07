# Liaison de l'acceptation native à la guerre observée

Tranche du 8 novembre 2026. **Static-checked**, expérimentale et **non testée dans
CK3**. Baseline et résultat80/80 source,0/20 campagne, delta0.

## Point d'entrée

L'adaptateur privé0.0.7 ajoute une liaison de métadonnées à la fin du
`declare_war_interaction.on_accept` natif, avant l'appel RW de réponse existant.
Le générateur conserve son inversion des trois blocs ajoutés. Le corps natif,
ses coûts, ses autres conditions et les CB gardent leurs octets d'origine.

La capture précoce conserve les parties et titres du vrai `claim_cb`. Cette
nouvelle liaison examine les `scope:actor` et `scope:recipient` fournis par
l'interaction acceptée. Elle les enregistre seulement lorsqu'ils correspondent
aux rôles principaux d'une guerre active et à son relevé précoce exact.

## Conditions et historique

Le candidat doit appartenir à l'acteur, avec schémas de loi et de parties,
numéro positif, rétention présente, phase précoce et date du jour. Ses parties
doivent être l'acteur et le destinataire de l'interaction. Son suzerain enregistré
doit toujours être le suzerain direct de l'acteur, détenteur du titre d'autorité.
La guerre référencée doit être un `claim_cb` actif de ces mêmes chefs de guerre.

La recherche exige un seul relevé correspondant et refuse plusieurs guerres
actives entre cette paire de chefs principaux, quel que soit leur CB. Les guerres
contre d'autres personnages restent hors de ce contrôle d'ambiguïté. Les relevés
déjà liés sont inclus dans le comptage afin de préserver cette vérification.

Les nouveaux relevés reçoivent un marqueur `rw_dl_acceptance_ready` à leur
création. L'écriture exige ce marqueur et l'absence d'une liaison précédente.
Elle revalide le relevé sélectionné, consomme le marqueur, puis écrit la date,
le schéma de liaison, l'acteur et le destinataire acceptés. Les anciens relevés
sans marqueur gardent leurs données. Un rejeu ne remplace aucune liaison et
n'étend aucune durée de conservation.

La sélection du relevé est locale aux histoires possédées par l'acteur. Les
identités, la phase, le titre d'autorité et les références de guerre restent
contrôlés. Une association absente ou ambiguë garde son état non lié.

## Choix envoyé

Le champ `rw_dl_accepted_choice` conserve l'état des drapeaux de l'interaction.

| Valeur | Observation |
|---|---|
| `ordinary` | Aucun des deux drapeaux sélectionné |
| `defy_selected` | Défi sélectionné avec hameçon non sélectionné |
| `hook_selected` | Hameçon sélectionné avec défi non sélectionné |
| `ambiguous` | Les deux drapeaux présents |

Ces valeurs décrivent la sélection lue à l'acceptation. La consommation effective
d'un hameçon, la dépense native et la qualification juridique ont leurs preuves
propres. La loi et les détenteurs de titres restent ceux du relevé précoce.

## Couverture et suite

La liaison peut examiner les relevés de branches différentes déjà capturés.
L'admissibilité de l'option de défi et des réponses existantes conserve son
périmètre entre pairs. Le prochain travail portera sur le chemin de défi
extérieur, puis les réactions de Mace/Doran à partir des rôles vérifiés.
Un changement de chefs principaux ou une association non démontrée conserve
l'absence de liaison. Les essais moteur devront confirmer les contextes reçus.

Six régressions source couvrent les identités étrangères, les anciennes archives,
la fraîcheur, l'autorité, les guerres/relevés ambigus, le rejeu, les quatre choix,
la place de l'appel et la conservation native. La campagne groupée comparera
revendications ordinaires, avec hameçon et avec défi, entre pairs puis entre
branches. Ajouter un autre CB entre les mêmes chefs, un rechargement, un changement
de rôles ou d'autorité et un callback répété. Inspecter les marqueurs et les
identités réellement reçues avant toute qualification moteur de ce chemin.

L'assemblage exige la base et les adaptateurs issus d'un même ZIP vérifié.
La version0.0.7 conserve les quatre entrées natives épinglées et vérifie les
empreintes des treize fichiers runtime originaux. La disponibilité des scopes et le coût du nouveau lecteur restent
à observer dans CK3.
