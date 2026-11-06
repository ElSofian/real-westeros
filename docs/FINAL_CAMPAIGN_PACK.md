# Préparer une seule version pour la campagne finale

Cet outil prépare **un dossier privé**, avec le mod et ses trois adaptateurs issus
du même ZIP public. Il ne lance pas CK3, n'installe rien, ne modifie ni sauvegarde
ni playset et n'ajoute aucun service payant. **Aucun point de développement ou de
validation moteur** : score inchangé68/80 source +0/20 moteur.

La revue de continuation RW-004 confirme la limite actuelle : `starts_enabled`
règle une préférence d'option ; les sources reçues ne montrent pas le planificateur
natif qui découvre une guerre interdite. W1/W2/W4/W5/AI4 restent ouverts. Cette
préparation aide à observer ensemble ces points et les nouvelles voies J4/J5,
sans nouveau contournement de guerre ni relancement intermédiaire demandé.

## Une commande de préparation, avant le lancement groupé

1. Récupérer le ZIP public et son fichier `.zip.sha256` depuis **la même exécution
   CI réussie**. Garder les deux côte à côte, sans renommer l'un indépendamment.
   Extraire ce ZIP dans un dossier de travail, distinct du dossier mod installé.
2. Python3.10 ou supérieur est nécessaire uniquement pour cette préparation,
   jamais pendant le jeu. Les bibliothèques utilisées sont toutes standard.
   Dans le dossier extrait, exécuter sous PowerShell (remplacer les trois chemins) :

```powershell
py -3 .\tools\prepare_final_campaign.py --distribution "<ZIP public>" --agot-root "<dossier AGOT>" --output "<nouveau dossier privé>"
```

Sous Linux/macOS, utiliser `python3 tools/prepare_final_campaign.py` avec les mêmes
arguments. Le dossier AGOT est celui qui contient `descriptor.mod` et `common/`.
L'outil réutilise les fichiers déjà recensés ; aucune nouvelle collecte n'est
nécessaire. Il attend les octets AGOT0.5.2.1 audités et les métadonnées déclarées
0.5.2.1 / support1.19.0.6 ; cela ne vérifie pas la version de l'exécutable CK3.

Le dossier de sortie doit être nouveau, avec un parent existant, en dehors du
checkout et de l'installation AGOT. Le ZIP, son checksum et les outils doivent
appartenir exactement à la même version. Un vieux script sur un ZIP récent est
refusé ; utiliser le script extrait de ce ZIP. Le checksum détecte une altération,
pas l'authenticité d'une provenance : conserver la source CI du téléchargement.

## Ce qui est assemblé

- Le mod public exact, ses guides et diagnostics séparés, sans remonter de fichiers
  locaux non suivis ou d'un autre checkout.
- L'adaptateur G1 privé : déclaration native et vrai claim_cb, capture de contexte
  et clôtures originales ; toujours expérimental, ordre moteur non vérifié.
- L'adaptateur privé de révocation, dont la campagne institutionnelle J4.
- L'adaptateur privé d'octroi pour les deux restitutions ducales RW, dont J5.
- Les trois reçus privés, les empreintes de tous les fichiers et le commit du ZIP
  dans `PRIVATE_CAMPAIGN.json`, écrit seulement en fin de préparation réussie.

Chaque générateur existant vérifie les empreintes de ses entrées natives ; l'outil
vérifie aussi ses sorties et les sources RW qu'il référence. Une entrée manquante,
un hash/version inattendu ou une différence entre outils et ZIP refuse la
préparation. Aucun dossier existant n'est remplacé. Les étapes intermédiaires
restent temporaires ; une erreur n'autorise pas un assemblage partiel prêt à jouer.

**La sortie contient du code AGOT généré : ne pas la publier, committer ou
redistribuer.** Le ZIP public de CI contient seulement les sources RW et les outils,
jamais ce dossier privé. Les reçus ne contiennent aucun chemin local d'installation.

## Installation lors de la campagne finale

À ce moment seulement, sauvegarder les anciennes versions RW puis copier le
contenu de `mod/` dans le dossier `mod` des données utilisateur CK3. Remplacer
entièrement les anciens dossiers d'adaptateurs, sans superposition. Le programme
ne le fait pas automatiquement. Les descripteurs conservent leurs chemins relatifs.

Dans le launcher, vérifier l'ordre : **AGOT → Real Westeros → adaptateur G1 →
adaptateur de révocation → adaptateur de restitution**. N'activer aucun ancien
probe/diagnostic G1 ou autre override concurrent de ces définitions. Les diagnostics
G3 sous `diagnostics/` restent séparés et inactifs par défaut. Aucune modification
automatique de la base du launcher n'est tentée.

Ouvrir [FINAL_ENGINE_TESTS.md](FINAL_ENGINE_TESTS.md) avant le démarrage de7–10minutes.
Grouper G1CHOICE/DECLAW/AIDEFY/WARLIFE et les cas J4/J5/AGOT sur une sauvegarde jetable,
en réutilisant la session et les sauvegardes de contrôle autant que possible.
Un témoin AGOT seul reste un autre playset nécessaire à la comparaison ; l'outil
ne promet ni rechargement à chaud des scripts ni une campagne exhaustive sans
aucun changement de playset. Zéro cas est exécuté par cette préparation.
