# J4 — campagne institutionnelle de confiscation

**Source expérimentale, aucun test CK3.** Cette mesure familiale porte sur les
titres actuels des membres d'une maison dans un royaume féodal. Elle complète le
critère source J4 de la v0.1 sur une voie de confiscation réactive : **+2,
développement68/80, moteur0/20, total68/100**. Elle ne constitue ni un veto
universel aux acquisitions ni une garantie d'absence de terres pendant50ans.
Le texte du critère, ses points et l'historique restent inchangés.

## Décision et institution

Une disgrâce politique seule ne déclenche rien. Le souverain indépendant féodal,
adulte et libre, peut explicitement activer les confiscations sous un décret
existant visant une autre maison. Il doit disposer du droit natif de révocation
et de l'adaptateur privé correspondant. Deux décrets concurrents pour la même
maison/autorité empêchent l'activation ambiguë. Les choix sont communs au joueur
et à l'IA ; l'IA préfère armer en présence d'un motif natif contre le représentant
et d'une opinion négative, et désarmer si elle est indulgente et favorable.
Ces préférences ne créent aucun motif contre les autres membres de la maison.

L'ordre est enregistré dans l'histoire institutionnelle existante, avec numéro
de version, auteur et date. **L'échéance originale du décret n'est jamais
renouvelée** par activation, retrait, réactivation ou changement de souverain.
La garde actuelle de l'histoire ne donne aucun pouvoir politique supplémentaire.
Le mécanisme existant de succession de garde est conservé ; les permissions
dépendent du détenteur actuel de l'autorité enregistrée.

L'ordre peut survivre à son auteur. Il devient inapplicable lorsque cette autorité
n'est plus le titre principal du souverain indépendant féodal, lorsque la loi
change ou lorsque sa propre maison devient celle visée. Il n'est pas étendu à
un nouvel empire par promotion. Une guerre suspend la préférence de révocation.
Les branches cadettes sont des maisons distinctes ; aucun élargissement à toute
une dynastie, aucune culpabilité personnelle héréditaire et aucun retrait de
noblesse ne sont déduits.

## Couverture des routes G3

Le point commun est le **titre actuellement détenu**, après acquisition. Aucune
condition de provenance ne réserve le traitement à la première génération.

| Route | Traitement source | Ce qui reste natif / à observer |
|---|---|---|
| Octroi | Si le bénéficiaire appartient à la maison et reste dans le royaume, le titre peut entrer dans la campagne. | L'octroi lui-même reste libre ; aucune annulation ou confiscation instantanée. |
| Héritage | Même contrôle du nouveau titulaire et de sa maison actuelle, même après décès du premier sanctionné. | Transmission, partition, sortie du royaume et succession AGOT inchangées. |
| Élection | Même contrôle après attribution effective à un titulaire admissible. | Électeurs, candidatures et institutions spéciales ne sont pas remplacés. |
| Conquête | Même contrôle du titre gagné et de la juridiction actuelle. | Vrai CB, résolution de guerre et Mega Wars demeurent natifs ; aucune préférence pendant la guerre. |

Pour chaque révocation, l'acteur est le **seigneur lige direct** admissible du
titulaire, dans le royaume actuel de cette Couronne. Acteur et cible sont
féodaux, vivants, détenteurs de terres et en paix ; l'acteur est adulte, libre,
au moins duc et autorisé à révoquer. Le titre choisi par l'interaction native
appartient encore à la cible, est au moins comtal, ni titre de famille noble ni
titre sans terre. La maison propre du seigneur n'est pas ciblée. Les protections
et limites natives supplémentaires restent applicables ; les terres hors royaume
et les gouvernements spéciaux ne sont pas aspirés dans la mesure.

L'adaptateur ajoute **une seule préférence IA**,2500 pour l'institution, sinon1500
pour l'ordre personnel antérieur, sinon0. Le bonus institutionnel dépasse le
socle natif négatif et sa pénalité féodale LP observée, sans supprimer les autres
pénalités ni facteurs nuls natifs. Il ne prouve pas que le moteur découvrira,
enverra ou acceptera une demande. Le joueur utilise la révocation native habituelle.
Coûts, tyrannie éventuelle, protections, refus/résistance et conséquences restent
ceux d'AGOT. Aucun transfert forcé, motif criminel ou paiement n'est ajouté ici.

## Information, retrait et restitution

La consultation expose uniquement maison, autorité et état de l'ordre, avec
identité/numéro/version revérifiés. Les membres du royaume et les membres de la
maison visée, y compris sans terres ou exilés, disposent de cette information
publique ; aucun dossier privé de complot n'est exporté. Aucun adaptateur n'est
nécessaire pour lire ou arrêter une campagne existante.

Le détenteur actuel peut arrêter la campagne, même si la maison visée est devenue
la sienne ou a quitté son royaume. Cela retire également ses propres ordres
personnels correspondants. La réhabilitation ou le retrait explicite d'un décret
armé retire son autorisation et les intentions personnelles correspondantes du
détenteur actuel de la Couronne. L'expiration automatique n'efface pas des ordres
personnels indépendants ; les demandes natives déjà envoyées ne sont pas annulées.

Les deux voies RW de retour ducal, après confiscation ou sur promesse, exigent
l'arrêt des campagnes institutionnelles actives et des intentions personnelles
correspondantes de l'émetteur. Ceci évite une restitution automatiquement reprise
par la même politique. Réhabiliter un décret déjà désarmé n'arrête pas un nouvel
ordre personnel indépendant : il faut le retirer séparément. Un autre lige peut
avoir sa propre politique. La fenêtre native d'octroi reste accessible ; cette
garde ne prétend pas réglementer tous les dons du jeu.

## Construction et portée des preuves

Le ZIP public contient uniquement le code RW et les générateurs originaux.
Générer de nouveau les adaptateurs depuis **le même checkout** ; ordre de
chargement : AGOT → Real Westeros → adaptateurs correspondants.

```sh
python tools/build_g3_native_confiscation.py --agot-root <AGOT> --output <nouveau-dossier-prive-revocation>
python tools/build_native_restitution.py --agot-root <AGOT> --output <nouveau-dossier-prive-octroi>
```

Révocation0.0.4 :38 sources runtime épinglées, deux sorties privées. Les quatre
insertions restent les mêmes ; leur retrait restitue les octets de la définition
native. Octroi0.0.1 : les six corps natifs restent inchangés, toutes les sources
du mod sont épinglées. Les entrées sont les octets reçus et vérifiés par empreinte,
avec descripteur de fixture rapportant AGOT0.5.2.1 / CK3support1.19.0.6 ; aucune
installation ou version de l'exécutable n'est attestée. **Sorties privées : ne
pas publier le code AGOT généré.**

Tests de contrats source et mutations négatives : décret non armé/ambigu,
mauvaise maison/autorité/titre/lige, perte de loi ou guerre, échéance renouvelée,
ancien panneau, privilège moteur inventé, fuite de preuves et boucle de retour.
La couverture source commune aux quatre routes n'est pas une preuve d'exécution
sur ces quatre routes. G3/G4/G5 et tous les tests moteur restent ouverts.

## Campagne finale — HFORFEIT-01…10, aucun cas exécuté

1. Activer puis vraie révocation native après octroi : coûts, tyrannie, refus,
   résistance, acceptation et titre effectif, avec témoin AGOT.
2. Héritage et partition : membres successifs, changement de maison et sortie
   du royaume ; aucun effet contre un titulaire désormais hors juridiction.
3. Élection ordinaire puis institution protégée : même filtre actuel dans le
   premier cas, règles natives conservées dans le second.
4. Conquête puis paix, contre-test guerre/Mega Wars et sortie de royaume.
5. IA↔IA : découverte, choix du titre, envoi et conséquences ; absence de double
   bonus personnel/institutionnel, pas de garantie artificielle d'acceptation.
6. Mort du souverain et du gardien de l'histoire, changement de chef de maison,
   sauvegarde/rechargement : même décret, même échéance, pouvoirs actuels seulement.
7. Promotion impériale, gouvernement/loi modifiés, Couronne passée à la maison
   visée : suspension sans extension ; rétablissement des conditions avant échéance.
8. Retrait, réactivation tardive, échéance originale, ancien panneau : aucun
   renouvellement ; retrait possible sans adaptateur et sans vassal encore présent.
9. Consultation souverain/vassal/membre sans terre ou exilé et tiers extérieur :
   connaissance publique partagée, preuves privées jamais révélées.
10. Stopper campagne et intentions personnelles, puis J5/retour sur promesse :
    aucun cycle automatique ; demandes natives pendantes, octroi manuel et
    nouvelles politiques indépendantes conservés.

Grouper ces cas avec G3/HCONF/HCRECEIPT/POSTRESTORE/RESTORE dans la campagne finale,
sans lancement intermédiaire (7–10minutes par démarrage). Prochain manque source :
W1/W2/W4/W5 et AI4 ; pas une nouvelle variante de journal ou de cette mesure.
