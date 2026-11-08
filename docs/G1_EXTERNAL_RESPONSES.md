# Réactions distinctes aux guerres entre branches

Tranche du 8 novembre 2026, **Static-checked**, expérimentale et **non testée
dans CK3**. PRIVATE0.0.9. Baseline et résultat 80/80 source, 0/20 campagne,
delta 0. Les essais moteur restent regroupés dans la campagne finale.

## Déclaration admissible

Le point d'entrée natif appelle le nouveau routage après la liaison d'acceptation
et avant l'ancien parcours entre pairs. Il exige un relevé précoce unique d'un
`claim_cb` actif, accepté aujourd'hui, avec acteur et destinataire correspondant
aux chefs principaux natifs. Les guerres multiples de cette même paire, même
avec un autre CB, sont refusées. Le relevé doit constater une autre branche,
l'interdiction de toutes les guerres et la permission native requise, avec le
défi sélectionné. Les autres déclarations gardent leur parcours existant.

La liaison d'acceptation pose un marqueur frais après avoir consommé son propre
marqueur d'écriture. Le routage consomme ce nouveau marqueur avant allocation et
enregistre sa date. Les anciens relevés et les acceptations rejouées ne créent
pas de réactions. Cette date atteste une tentative de routage. Une allocation
partielle conserve les décisions déjà créées et ne relance pas les envois.

## Deux rôles

- Le suzerain du déclarant provient du suzerain et du titre d'autorité enregistrés
  lors de la déclaration. Dans l'exemple envisagé, il s'agit de Mace.
- Chaque suzerain des détenteurs des titres visés provient des relevés de titres
  du vrai CB. Dans l'exemple où Dayne détient le titre et relève directement de
  Doran, ce rôle revient à Doran, même si le défenseur principal est différent.

Les titres doivent avoir tous été enregistrés avant le routage protecteur.
Chaque fait exige le parent exact, son numéro, la guerre, la date et les identités
enregistrées. Le détenteur, son suzerain et le titre d'autorité sont revalidés.
Le suzerain du déclarant et le déclarant lui-même sont exclus du rôle protecteur.
Un détenteur indépendant sans suzerain ne produit pas ce second rôle.

Chaque autorité distincte reçoit une décision par guerre et par rôle. La recherche
visite seulement les relevés personnels des titres du CB. Plusieurs titres avec
le même suzerain sont dédupliqués. Le premier fait admissible sert de référence
à sa décision. Si son titre change ensuite de détenteur ou de suzerain, ce choix
devient indisponible, même si un autre titre concerné pourrait encore relever de
cette autorité. Aucun nouveau protecteur n'est reconstruit après coup.

## Choix et conséquences

Chaque autorité dispose de sept jours pour laisser passer ou désapprouver
l'attaque. Les décisions sont personnelles et indépendantes. Désapprouver ferme
d'abord le choix, puis applique le modificateur politique existant de -10
d'opinion envers l'attaquant pendant deux ans et lui envoie une notification.
Les deux autorités peuvent donc chacune manifester leur propre désapprobation.

Les conditions d'exécution sont communes aux joueurs et à l'IA. Une préférence
initiale utilise les axes natifs d'honneur et d'audace, l'opinion de l'attaquant,
les moyens et les guerres de l'autorité. Cette tranche n'achève pas la revue de
tous les traits et détails contextuels demandée par le propriétaire.

La guerre, ses coûts, le CB et sa résolution restent gérés par CK3/AGOT. La
désapprobation protectrice est une position politique. Le parcours n'ajoute ni
motif de crime, ni confiscation, ni hameçon, ni demande de paix native. Les
demandes, négociations et aides d'un supérieur restent les tranches suivantes.
La proclamation générale de paix demeure différée.

## Identité, nettoyage et livraison

Chaque décision conserve son parent, numéro, guerre, rôle, autorité et titre.
Les choix revalident ces données, les chefs principaux et la situation actuelle
du détenteur et du suzerain. Les changements d'autorité, de chef de guerre ou de
contexte invalident le choix. La fenêtre expirée refuse immédiatement ses effets.
Le nettoyage mensuel ferme les décisions périmées. Les décisions fermées restent
inertes tant que leur guerre exacte figure dans la liste du propriétaire initial.
Sa mort ou la disparition de cette guerre termine le relevé. Aucun héritier
ne reçoit le choix ou la faute personnelle.

L'adaptateur privé recense les six nouveaux fichiers de source et garde les
quatre entrées natives épinglées. L'inversion des ajouts restaure exactement la
déclaration native. Le ZIP public contient uniquement les sources originales et
les générateurs. Les tests portent sur ces sources et les fichiers livrés.

La campagne moteur doit vérifier l'ordre réel des callbacks, l'identité du
destinataire et du défenseur principal, la disponibilité des titres du CB,
les notifications et préférences IA, la persistance après rechargement, les
transferts, la déduplication multi-titres et le coût de nombreux titres. Une
liaison native absente ou ambiguë laisse cette réaction indisponible.
