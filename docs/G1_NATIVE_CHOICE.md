# G1 — Candidat isolé : défi explicite dans la fenêtre native

**Implémentation source expérimentale et privée ; aucun test moteur.** Cette tranche
RW-004 développe une voie de déclaration, pas un nouveau journal de diagnostic.
Elle reste extérieure au mod principal. **W1…W5 et AI4 restent ouverts, +0 point.**
Ni G1 résolu, ni guerre interdite fonctionnelle, ni compatibilité AGOT démontrée.

## Choix technique

Le candidat ajoute « Défier l’interdiction de mon suzerain » à la fenêtre native de
déclaration de guerre. Il ajoute une seule alternative au contrôle natif exigeant
l'absence de besoin de hameçon ou l'option hameçon. L'alternative demande le nouveau
choix explicite, l'absence d'option hameçon sélectionnée et le contexte courant :
acteur/cible adultes vivants, libres, titrés et féodaux, distincts, même suzerain
direct vivant, interdiction interne/totale et helper natif exigeant réellement
l'autorisation. Une exemption contractuelle que reconnaît déjà ce helper conserve
sa voie normale. Posséder un hameçon n'impose pas de l'utiliser.

Le contrôle du contexte est présent à la visibilité, à la validité de l'option et
au contrôle final de cible. Le moteur doit encore démontrer ces réévaluations.
Cocher défi et hameçon ensemble invalide l'option de défi ; aucune consommation
simultanée n'est ajoutée. Le helper partagé reste **inchangé**, sans récursion.
Les options natives et leurs conditions restent byte pour byte identiques.

Contrairement au ticket préalable du diagnostic G1INT, l'intention est ici un
`send_option` de l'interaction native : aucune variable, autorisation d'un jour,
flag personnage, réservation d'un autre personnage ou effet sur ouverture. Fermer
ou changer de fenêtre devrait abandonner ce choix local ; c'est un contrat moteur
à vérifier, pas un résultat observé. Le candidat n'appelle ni `start_war`, ni
`run_interaction`, ni un CB de remplacement. La fenêtre native conserve le choix du
CB/titre, toutes les restrictions étrangères à cette unique garde, les coûts,
l'emploi éventuel d'un hameçon dans la voie normale et tout son `on_accept`.
Le choix n'est pas restreint artificiellement au seul `claim_cb` : les CB réellement
proposés par le moteur restent natifs, sans nouvel octroi de revendication.

Aucun callback de guerre/Mega Wars, law, coût ou état de guerre n'est recopié ni
rejoué. Aucune qualification d'infraction, réaction royale, sanction ou restitution
n'est encore attachée au choix : le contexte et l'ordre des callbacks natifs doivent
être établis avant de créer un verdict historique. Ne pas présenter un snapshot
postérieur ou l'ouverture de la fenêtre comme la loi au moment de l'acte.

Les mêmes triggers n'excluent ni humain ni IA. **La sélection autonome du nouveau
choix par l'IA native n'est pas démontrée et aucune politique d'initiation IA n'est
implémentée.** Aucun paramètre AI de send_option n'est inventé pour le prétendre.
Il ne s'agit donc pas d'une livraison complète W2 ou AI4.

## Génération locale privée pour la campagne finale

Le dépôt/ZIP public contient uniquement le générateur et trois fichiers originaux
(triggers et EN/FR), jamais la définition AGOT. Sur la copie de sources installées :

```sh
python tools/build_g1_native_choice.py --agot-root <dossier-AGOT> --output <nouveau-dossier-prive>
```

Le dossier doit être nouveau, extérieur au dépôt et à l'installation AGOT. Il n'est
jamais installé automatiquement. Le générateur exige la version déclarée AGOT
0.5.2.1 / support 1.19.0.6 et les trois empreintes privées déjà auditées : interaction
de guerre/helper dans G1_SOURCE_RECEIPT.json, claim dans G1_COMPLEMENT_RECEIPT.json.
Ces métadonnées ne vérifient pas l'exécutable CK3. Aucun changement de version/hash
n'est accepté sans nouvel examen ; aucune nouvelle source à transmettre maintenant.

Il extrait uniquement la définition native `declare_war_interaction`, ajoute les
deux fragments originaux, et démontre que leur retrait retrouve exactement les
octets de la définition d'entrée (UTF-8, y compris CRLF internes). Tout autre bloc
du fichier AGOT reste absent de l'override généré et demeure fourni par AGOT.
Le manifeste privé contient des chemins relatifs et empreintes, jamais de chemin
personnel. Un fichier modifié, lien symbolique, layout inattendu, version différente
ou destination existante provoque un refus avant création de sortie.

**La sortie contient une définition propriétaire AGOT : ne pas la publier, committer
ou redistribuer.** Son unique override est `zz_rw_native_war_choice.txt`, chargé dans
un mod séparé `rw_g1_native_choice`. Pour la campagne finale seulement, installer ce
mod après AGOT et, le cas échéant, Real Westeros ; vérifier que sa définition gagne
réellement la résolution du playset. N'activer qu'un candidat G1 à la fois : il est
**incompatible avec les deux diagnostics G1 et tout autre override de déclaration**.
Le mod de base et son installation normale ne le chargent jamais. Désactivation et
retour à une sauvegarde jetable restent le moyen de revenir au témoin AGOT seul.

## Vérifications disponibles et limites

18 tests couvrent la construction réelle sur fixtures synthétiques originales, les
sources manquantes/modifiées, version, symlinks, destinations, layout, double patch,
préservation des octets UTF-8/CRLF, isolation, manifeste, gardes natives et textes.
Une construction privée supplémentaire sur les trois fichiers reçus a réussi avec
empreintes exactes et une fixture du descripteur déclaré. Cela n'exécute aucun moteur
et ne démontre pas l'installation réelle, le load order, l'IA, le CB ou les coûts.

Les fichiers originaux et le générateur autonome sont inclus dans le ZIP public,
sous `experiments/` et `tools/`, sans mod optionnel installé ni source propriétaire.
Le contrôle structurel principal ne transforme pas ces sources en gameplay validé.
Un autre contrôle caché du moteur peut encore bloquer la guerre malgré cette garde.

## Cas G1CHOICE-01…08 — tous différés à la campagne finale

1. Témoin AGOT seul, puis candidat isolé : comparer l'interface et vérifier la bonne
   définition chargée, sans perte d'option ni autre interaction du fichier natif.
2. Interdiction actuelle, deux pairs féodaux, vraie revendication sur le titre choisi :
   refus sans choix, tentative avec défi, identité exacte du CB/titre/parties et coûts
   réellement dépensés. Vérifier absence d'autorisation native hameçon.
3. Hameçon seul, exemption contractuelle et absence d'interdiction : comportement
   natif inchangé ; défi masqué/invalide. Défi+hameçon ensemble doit refuser l'envoi.
4. Autre cible, suzerain changé, loi/exemption changée pendant l'interface, acteur/cible
   invalides : pas de réutilisation du choix hors de son contexte admissible.
5. Annuler/fermer/recharger/changer de cible ou de CB : aucun coût, infraction,
   autorisation persistante ou nouveau choix précoché attribué par le candidat.
6. Restrictions indépendantes (armée levée, dette, trêve/allié culturel, captivité,
   foi, diarchie, Braavos/Pentos, institutions AGOT) : comparaison stricte au témoin.
7. Victoire/défaite/paix blanche/invalidation et guerre Mega Wars appropriée :
   callbacks/coûts/titres/nettoyage natifs, sans nouveau callback ni effet rejoué.
8. IA↔IA et IA→joueur : constater séparément l'accès/choix natif et les limites
   d'initiation. Sans chemin autonome réel, W2/AI4 restent ouverts. Aucune guerre
   constatée ne suffit seule à attribuer une infraction ou à valider la réaction royale.
