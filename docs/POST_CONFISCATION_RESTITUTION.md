# J5 — restitution effective après révocation native

**État courant après J4 :** voir [INSTITUTIONAL_HOUSE_FORFEITURE.md](INSTITUTIONAL_HOUSE_FORFEITURE.md).
La campagne institutionnelle complète la voie personnelle antérieure, sans veto
universel. Les deux retours RW exigent l'arrêt des ordres correspondants avant
transfert. Régénérer les adaptateurs depuis le même checkout ; révocation0.0.4,
38 sources runtime/deux sorties privées, quatre insertions inchangées. Les scores
et comptes plus bas décrivent la livraison historique de ce guide, pas le score
courant68/80 source +0/20 moteur. Aucun test CK3.


**Source expérimentale vérifiée, aucun test CK3.** La voie livrée relie une
révocation native acceptée et une perte de titre constatée à un véritable octroi
du titre perdu. Elle complète J5 dans les sources de la première v0.1 : **+2,
développement66/80, moteur0/20, total66/100**, sous réserve des contrôles requis.
Le barème, le texte du critère et les précédents checkpoints restent gelés.

## Parcours livré

1. Un souverain indépendant féodal engage sa politique envers la maison d'un
   vassal. La révocation ordinaire conserve ses droits, coûts, acceptation,
   refus/résistance et conséquences. L'adaptateur existant aide sa sélection IA ;
   le joueur utilise la fenêtre native habituelle.
2. Pour le duché principal d'un duc féodal, l'envoi fige les parties, titre,
   maison et autorité. **L'envoi seul n'ouvre aucun droit de restitution.**
3. La fin de `on_accept` atteste l'acceptation native. Le callback de gain constate
   le titre exact quitté par cet ancien détenteur et désormais détenu par le
   souverain. Les deux preuves sont nécessaires. Leur rapprochement accepte
   les deux ordres de callbacks et refuse un rapprochement tardif après deux jours.
4. Le souverain peut examiner ses restitutions auprès de l'ancien titulaire,
   joueur ou IA. Un panneau par duché admissible, sans plafond arbitraire. Il peut
   garder le titre ou choisir de le rendre. Aucune promesse ou publication dans
   les archives n'est nécessaire ; aucun personnage n'hérite d'une culpabilité.
5. Le choix consomme une tentative et programme le retour le lendemain. Après
   revalidation du cas et des gardes natives d'octroi, le vrai contexte de changement
   de titre `granted` est créé et résolu. Le succès est enregistré seulement si
   l'ancien titulaire détient réellement ce titre. Les conséquences et la
   notification natives sont alors exécutées une seule fois.

Ce mécanisme rend une dignité ducale réellement retirée, au-delà d'une réhabilitation
politique, d'un reçu ou de l'ouverture d'une fenêtre. J4 reste ouvert : couverture
des sanctions familiales sur les routes G3, bannissement foncier universel et
suppression/restauration générale de noblesse ne sont pas ajoutés ici. La voie
native de confiscation déjà présente fournit l'entrée de J5 ; clôturer toutes
les mesures J4 n'est pas requis pour ce chemin de restitution après perte effective.

## Périmètre et liberté

L'ancien duc doit être resté comte, vassal direct du même souverain, dans la maison
figée. Tous deux sont adultes, vivants, libres, en paix, féodaux et sans diarchie,
de même foi/culture. Le souverain détient toujours son autorité initiale et le
duché ; partition et son héritier sont exclus. Les quatre prédicats du don natif
sont conservés et revérifiés dans l'adaptateur privé. Titres loués, familiaux,
fonciers abstraits, chefs de foi, misés ou bloqués par AGOT sont exclus.

**Seul ce duché est rendu : aucun comté, baronnie ou vassal d'autrui n'est pris.**
Les conditions d'exécution sont identiques pour joueur et IA. L'IA peut revoir
ses cas via son pool de vassaux et une fréquence6, selon opinion/pardon, puis
choisir séparément de rendre ou conserver. Pas de recherche mondiale. Il ne
s'agit pas d'une obligation d'agir ni d'une preuve que le planificateur le fera.

La possibilité est personnelle pendant cinq ans. La mort de l'une des parties
ferme ce chemin ; les descendants ne récupèrent pas automatiquement ce titre.
Rendre des comtés, relever une maison entièrement sans terre, gérer les héritiers
institutionnels ou restaurer une noblesse supprimée reste hors de cette voie.
Ce sont des extensions de la vision ; le critère source J5 de cette v0.1 est
qualifié sur cette chaîne complète, avec ces limites explicites, pas comme une
restauration universelle de toutes les sanctions possibles.

## Rejeu, origine et perte de capacité

Le cas opératif n'est pas un second journal foncier. Il est créé uniquement depuis
la demande native exacte consommée au gain du titre. Les faits TP et les archives
canoniques restent inchangés et ne sont pas reconstruits. La confirmation ne
prouve ni le motif criminel d'un complot ni la légalité de la révocation : elle
rapproche l'acceptation native et le transfert exact, sans verdict rétroactif.

Identité/numéro immuables, preuve d'acceptation consommée sans renouvellement,
fenêtres fixes, propriétaire courant et autorité revérifiés. Refus natif : clôture
des seules preuves non confirmées. Toute cession ultérieure du duché ferme le
cas ; une réacquisition ne le réactive pas. Un callback sans changement réel de
détenteur ne ferme rien. Le titre rendu ferme aussi le cas ; un nouveau cycle
nécessite une nouvelle révocation et de nouvelles preuves. Ancien panneau,
expiration, mort, changement de maison/suzerain/autorité ou capacités devenues
invalides n'autorisent pas de transfert. Une tentative consommée n'est jamais
relancée automatiquement, y compris après échec ambigu. L'octroi ordinaire reste
possible. Entretien des seules histoires personnelles, pas de scan global.

## Adaptateurs et vérifications

Générer les deux adaptateurs depuis **le même checkout livré** :

```sh
python tools/build_g3_native_confiscation.py --agot-root <AGOT> --output <nouveau-dossier-prive-revocation>
python tools/build_native_restitution.py --agot-root <AGOT> --output <nouveau-dossier-prive-octroi>
```

AGOT → Real Westeros → ces deux adaptateurs. Version de révocation0.0.3 : quatrième
insertion originale, suffixe d'acceptation. Retirer les quatre insertions restaure
la définition native octet pour octet ; aucun effet/coût natif n'est rejoué.
Un input natif épinglé,29 sources runtime originales, deux sorties privées. Le
builder d'octroi conserve ses six corps natifs sous des noms RW et épingle toutes
les sources du mod. Références : HOUSE_CONFISCATION_SOURCE_RECEIPT.json et
NATIVE_RESTITUTION_SOURCE_RECEIPT.json. Sans les preuves ou l'adaptateur d'octroi,
aucun retour n'est offert. Les anciennes demandes ne sont pas reconstituées.

**Les sorties contiennent du code AGOT : PRIVÉ, ne pas publier ou redistribuer.**
Le ZIP public contient seulement les sources RW et les générateurs originaux.
Les générations sur octets reçus utilisent les versions rapportées dans un
descripteur de fixture : ce n'est pas une installation CK3 vérifiée.

Les tests adversariaux couvrent les deux ordres, absence de l'une des preuves,
mauvaise paire/titre/autorité, acceptation répétée, refus, identité du panneau,
consommation avant transfert, revalidation native, vérification du détenteur avant
conséquences, absence de transfert de vassaux, réacquisition et égalité joueur/IA.
La source n'établit pas l'ordre réel des callbacks, l'équivalence des effets
hardcodés du don, la composition des on_actions, le load order ou la performance.
Tous restent à observer dans CK3 ; aucun point moteur n'est attribué.

## Campagne finale groupée — POSTRESTORE-01…08, aucun cas exécuté

1. Ordre envers une maison → vraie révocation acceptée du duché principal, duc
   resté comte → choix de restitution → vrai retour du même duché ; constater
   soldes/coûts natifs, historique, comtés, vassaux et hiérarchie avant/après.
2. Même chaîne IA↔IA ; observer découverte, choix de conserver/rendre et effets.
3. Demande seule, refus/résistance et gain sans acceptation : aucun cas confirmé.
4. Observer l'ordre effectif acceptation/gain ; confirmer sans doublon dans les
   deux ordres supportés, avec sauvegarde/rechargement et callback répété.
5. Mort, guerre, prison, changement de maison/suzerain/autorité, titre perdu entre
   choix et lendemain ou garde native négative : aucun retour automatique.
6. Rejeu/ancien panneau, tentative échouée, cession puis réacquisition : aucun
   réveil ou double transfert ; nouveau cycle seulement après nouvelle révocation.
7. Les faits/archives/promesses anciens restent indépendants ; pas de crime,
   pardon, succession, sanction familiale ou droit hérité fabriqué.
8. Comparer le don natif ducal sans transfert de vassaux : callbacks, opinions,
   relations de maisons, prestige/stress, alias TITLE, notifications et AGOT/Mega Wars.

Grouper avec HCONF/HCRECEIPT/RESTORE/G3, sans lancement intermédiaire et sans
relancement par cas (CK3 démarre en7–10minutes). Prochaine cible substantielle :
J4 et sa couverture G3 ; les critères de guerre et AI4 restent également ouverts.
