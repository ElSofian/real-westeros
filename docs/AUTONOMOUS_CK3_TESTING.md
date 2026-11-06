# Ce qui peut être vérifié sans lancer CK3 manuellement

Recherche et exécution du **6 novembre2026**, après PR#93. Résultats détaillés et
empreintes : [AUTONOMOUS_CK3_TESTING_RECEIPT.json](AUTONOMOUS_CK3_TESTING_RECEIPT.json).
**Aucun test moteur. +0 :68/80 source,0/20 moteur,total68/100.**

## Résultat concret exécuté dans le cloud

[Tiger1.19.0](https://github.com/amtep/tiger/tree/v1.19.0) accepte plusieurs
`load_mod` ordonnés. L'analyse a donc été étendue du mod de base à **l'assemblage
privé complet** produit depuis le ZIP du commit9364817db27dff786299fa438bbcda809a656de8 :
base, adaptateur de guerre, de révocation et d'octroi. Aucun original AGOT n'est
ajouté au dépôt ou à l'archive publique.

Deux profils ont été réellement exécutés avec le même binaire, les mêmes données
CK3/AGOT partielles et les mêmes six entrées natives auditées :

| Profil | Ordre ajouté aux données partielles | Diagnostics dont le premier emplacement est le code RW de base |
|---|---|---|
| Témoin | Six entrées natives originales → RW de base |370|
| Assemblé | Mêmes entrées → RW de base → guerre → révocation → octroi |370|

La comparaison par clé, message, chemin relatif, ligne primaire, gravité et
confiance donne **0 ajout,0 retrait** pour le code RW de base. Cela montre que
l'activation des adaptateurs n'introduit pas de nouveau diagnostic primaire sur
ces fichiers dans cette analyse. Ce n'est ni une exécution des effets ni une
preuve d'absence de défaut.

Le profil assemblé compte676 diagnostics ayant leur premier emplacement dans RW
ou ses fichiers privés générés. Ce nombre inclut les corps natifs recopiés. Le
problème de scope du callback de revendication apparaît également dans le CB
original ; la double priorité d'interface et les trois alertes de scope de guerre
de révocation apparaissent également dans l'interaction originale. Aucun corps
natif n'a été « corrigé » pour faire taire l'analyse ; les preuves d'inversion et
les six corps d'octroi restent celles des générateurs existants.

**Les données sont partielles**, avec les fixtures de signatures/répertoires déjà
utilisées auparavant. Avec `show_loaded_mods=yes`, le témoin émet301226 diagnostics
et l'assemblage250003, principalement des références natives absentes. Ces totaux
ne mesurent ni qualité du mod ni progrès : déplacer une définition dans un fichier
surchargé ou un helper cloné change aussi la façon dont Tiger émet les alertes.
Les rapports complets restent privés car ils contiennent des extraits natifs.
Aucun filtre ou suppression n'a masqué les diagnostics ; **un code de sortie0
n'est pas un verdict de validation**. L'avertissement conditionnel de participant
au complot reste présent et qualifié, sans identité fabriquée.

## Reproduire l'analyse sur une vraie installation, sans démarrer le jeu

Le modèle suivant est tiré du
[fichier de configuration Tiger épinglé](https://github.com/amtep/tiger/blob/v1.19.0/ck3-tiger.conf).
Remplacer les chemins, en utilisant des slashs `/`. Dans un fichier privé :

```text
languages = { check = "english" check = "french" }
filter = { show_loaded_mods = yes }
load_mod = { label = "AGOT" modfile = "<AGOT>/descriptor.mod" }
load_mod = { label = "RW-base" modfile = "<pack>/mod/real_westeros/descriptor.mod" }
load_mod = { label = "RW-war" modfile = "<pack>/mod/rw_g1_native_choice/descriptor.mod" }
load_mod = { label = "RW-revoke" modfile = "<pack>/mod/rw_g3_native_confiscation/descriptor.mod" }
```

```text
ck3-tiger --game "<CK3>" --paradox "<répertoire utilisateur isolé>" --config "<configuration privée>" --json "<pack>/mod/rw_native_restitution/descriptor.mod"
```

Pour le témoin, garder uniquement AGOT dans `load_mod`, et cibler le descripteur
RW de base. Dans notre collection partielle, une couche privée des six originaux
reçus a aussi été chargée dans **les deux** profils, avant RW, pour assurer la
comparaison des mêmes originaux. Une installation complète n'a pas besoin de cette
couche de collection. Ne pas ajouter de fausses définitions pour faire disparaître
les références manquantes. L'analyse de sources complètes permettrait davantage
de vérifications statiques, toujours sans moteur.

## Automatisation moteur : piste réelle, disponibilité non démontrée ici

Un [exemple public meckt](https://github.com/Xorrad/meckt/blob/ba27da2431ce92f96c6e9b8a1db7b6e0235f8142/src/tests/workflows/monitor.py)
lance un exécutable CK3 avec `-nographics` et observe un journal de chargement.
Son [workflow](https://github.com/Xorrad/meckt/blob/ba27da2431ce92f96c6e9b8a1db7b6e0235f8142/.github/workflows/run.yml)
charge une image Docker CK3 depuis un dépôt LFS privé nécessitant un token. Il
faut donc **déjà disposer du jeu exécutable et de ses données**, ce n'est pas un
moteur de remplacement téléchargeable avec les scripts du mod.

Le [run public consulté](https://github.com/Xorrad/meckt/actions/runs/41043934161)
termine en échec à l'étape Run CK3 ; les deux autres runs récents consultés sont
aussi en échec. Cela ne prouve pas que cette option est impossible, mais ne
valide ni le fonctionnement de cet exemple ni sa compatibilité1.19.* / AGOT0.5.2.1.
Aucun exécutable CK3, SteamCMD, Wine ou Xvfb n'a été repéré par les vérifications
d'environnement effectuées ici. Les fichiers reçus sont des scripts, pas une
installation exécutable. Aucun binaire privé tiers, image de jeu ou identifiant
Steam n'a été récupéré ou demandé.

Une ligne de chargement réussie, l'absence de crash ou un délai écoulé ne suffiraient
pas à valider l'initiative IA, les coûts, la capture de loi ou les Mega Wars. Un
futur banc moteur doit enregistrer des observations précises et distinguer refus,
absence de découverte, succès et scénario non exécuté ; il ne doit pas décider
« succès » sur un marqueur de démarrage. Les options de lancement et capacités
de contrôle doivent être vérifiées sur notre véritable exécutable.

## Autres pistes et décision

- [CWTools](https://github.com/cwtools/cwtools-ck3-config) propose des schémas et
  contrôles d'éditeur. C'est une autre analyse statique ; sa documentation ne
  fournit pas une simulation de l'IA ou des callbacks. Non exécuté dans cette revue.
- [meckt](https://github.com/Xorrad/meckt) est un éditeur de cartes ; ses tests
  d'éditeur ne sont pas des tests de nos guerres. Son exemple de lancement moteur
  est distinct de ces tests.
- Une installation autorisée sur une machine accessible, éventuellement un
  runner local, pourrait ensuite permettre des exécutions moteur répétées avec
  moins de manipulations. Elle exigerait une configuration initiale et la
  vérification de l'exécutable ; elle n'est ni installée ni disponible aujourd'hui.
  Aucun service payant ou runner supplémentaire n'a été créé.

**Décision :** continuer les vérifications statiques autonomes de l'assemblage,
qualifier leurs alertes et corriger seulement les défauts établis. Garder la piste
sans interface comme recherche, sans promettre son fonctionnement ou demander
maintenant un lancement intermédiaire. Les points W1/W2/W4/W5/AI4 et les20points
moteur restent ouverts. Les inconnues du planificateur natif ne sont pas résolues
par cette analyse, mais il existe bien davantage de contrôles autonomes que les
seuls tests Python du dépôt. Aucun nouveau prototype de simulation n'est ajouté.
