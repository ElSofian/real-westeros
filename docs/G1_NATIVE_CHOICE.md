# G1 — Choix explicite dans la fenêtre native

**Source expérimentale ; aucun test moteur.** Le choix de défi ajoute une alternative
locale au contrôle d'autorisation native dans un adaptateur privé séparé. Le mod
principal ne remplace aucune interaction, loi, CB ou callback de guerre.
G1, W1/W2, W4/W5 et l'initiative autonome de guerre restent ouverts.
La réaction W3 et l'intervention native sont décrites dans G1_NATIVE_INTERVENTION.md.
Leur qualification source ne valide pas le moteur ou la déclaration interdite.

## Chemin et périmètre

« Défier l'interdiction de mon suzerain » est un send_option de la fenêtre native,
pas un ticket extérieur d'une journée. Il exige deux pairs féodaux adultes, vivants,
libres, titrés, distincts, avec le même suzerain direct vivant et son interdiction
courante ; le helper natif inchangé doit encore exiger l'autorisation. L'exemption
contractuelle reconnue par ce helper conserve sa voie native. Le défi est incompatible
avec la sélection simultanée d'un hameçon. Posséder un hameçon ne force pas à l'utiliser.

Les gardes sont réévaluées à la visibilité, validité de l'option et contrôle de cible.
La sélection du CB/titre, les autres restrictions, les coûts et le corps original
d'acceptation restent natifs. Aucun CB artificiel, claim accordé ou appel `start_war`.
Le choix peut accompagner les CB proposés par le moteur ; la première réaction
originale est limitée à une guerre de revendication exacte et univoque.

En fin de `on_accept`, un appel original gardé peut créer ce dossier de réaction.
Il constate le défi choisi et le contexte au callback, **pas la loi à l'instant
moteur de déclaration**. Un callback sans guerre admissible ne crée rien ; aucune
infraction native ou culpabilité héritée n'est inventée. La sélection autonome de
ce send_option par l'IA native n'est ni fournie ni démontrée. Les négociations
royales IA ne résolvent pas cette limite d'initiation de guerre.

## Génération et installation privées, pour la campagne finale

```sh
python tools/build_g1_native_choice.py --agot-root <dossier-AGOT> --output <nouveau-dossier-prive>
```

Le dossier doit être nouveau, extérieur au dépôt/ZIP extrait et à l'installation.
Le générateur refuse une version déclarée différente de AGOT 0.5.2.1 / support
1.19.0.6, un hash inattendu, source symbolique ou layout non reconnu. Les quatre
fichiers AGOT requis sont les interactions de guerre et de vassaux, le helper
war-and-peace et le CB de revendication. Les douze sources originales dans
`mod/real_westeros` sont aussi contrôlées. Aucun besoin d'un nouvel envoi de fichiers.

La sortie contient les définitions privées de déclaration et de claim_cb adaptées,
le clone du helper en lecture seule, des descripteurs, un reçu et l'avertissement privé. Elle ne recopie plus les bibliothèques originales.
La suppression des trois fragments (garde, option, appel final) retrouve exactement
les octets de la définition de déclaration d'origine, y compris UTF-8/CRLF internes.
Aucun autre bloc du fichier de guerre natif n'est copié dans l'override et le fichier
natifs d'interactions de vassaux n'est jamais modifié. Les références sont dans
G1_SOURCE_RECEIPT.json, G1_COMPLEMENT_RECEIPT.json et
G1_NATIVE_INTERVENTION_SOURCE_RECEIPT.json, sans code propriétaire publié.

**Cette sortie contient du code AGOT : ne jamais publier, committer ou redistribuer.**
Installer AGOT, puis Real Westeros, puis l'adaptateur `rw_g1_native_choice`, dont
le descripteur dépend explicitement de Real Westeros. Ne pas activer en même temps
les anciens diagnostics G1 ni un autre override de déclaration. Vérifier le load
order effectif ; les métadonnées ne démontrent pas l'exécutable, les DLC ou le playset.
Le ZIP public contient le mod original et le générateur, jamais cet override natif.
Sans adaptateur, aucune déclaration ordinaire n'alimente le nouveau dossier.

## Vérification et campagne finale

Les tests positifs/négatifs du générateur couvrent les entrées privées synthétiques,
la préservation des octets, les sources/destinations/versions refusées, la dépendance
au mod de base et l'absence de bibliothèques dupliquées dans l'adaptateur. Une
construction locale sur les quatre sources reçues et une fixture des métadonnées
rapportées ne constitue ni une installation vérifiée ni un lancement CK3.

Les cas **G1CHOICE-01…08** restent tous non exécutés : témoin/load order ; vraie
revendication et coûts exacts ; hameçon/exemptions/absence d'interdit ; contexte
modifié pendant la fenêtre ; fermeture/annulation/rechargement/retargeting ; autres
restrictions natives ; victoire/défaite/paix/invalidation/Mega Wars ; initiation IA.
Ils s'ajoutent aux cas G1ROYAL et NATIVEWAR de leurs guides respectifs. Une guerre
constatée ou une simple demande ne démontre ni illégalité, paix ou sanction exécutée.

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
