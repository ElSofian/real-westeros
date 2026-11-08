# Préférences IA des réponses aux guerres extérieures

Actualisation. AI_PEER_WAR_RESPONSES.md applique les facteurs communs sans
références aux parties à six choix du parcours entre pairs. Les relations et
identités de ce parcours disposent de leurs propres lecteurs.

Tranche du 8 novembre 2026. **Static-checked**, **non testée dans CK3**.
Baseline et résultat 80/80 source, 0/20 campagne, delta 0.

## Périmètre et identité

Les dix choix des réponses extérieures et de leur médiation utilisent désormais
des poids nommés dans `rw_external_war_ai_values.txt`. Chaque poids commence à
zéro et exige la garde réelle de son tour et de son action. Les gardes vérifient
déjà les identités personnelles, la guerre, les autorités, le parent, le numéro
du dossier et les fenêtres. Un contexte invalide conserve un poids nul.

Les tendances, compétences, ressources et opinions sont celles du personnage
qui décide. Le lige, le protecteur, le déclarant et le médiateur restent distincts.
Le profil ne consulte aucun trait privé d'un tiers. Il lit ses propres opinions
et liens familiaux ou alliances, les rôles publics du dossier et, pour le déclarant,
la position de sa guerre exacte. Les effets et conditions restent communs aux
joueurs et à l'IA.

## Tendances natives

Chaque facteur ci-dessous vaut `clamp(1 + axe/200, 0.5, 1.5)`. La prudence utilise
le signe inverse de l'audace. Les traits et modificateurs CK3/AGOT se combinent
d'abord dans les axes natifs. Plusieurs choix utilisent des divisions par ces
facteurs strictement positifs pour exprimer une préférence opposée.

| Axe | Utilisation directe |
| --- | --- |
| Audace | Fermeté, refus, prudence en sens inverse |
| Honneur | Recherche de résolution par le lige et accord de médiation |
| Compassion | Recherche d'une résolution et accord de médiation |
| Vengeance | Désapprobation, refus du déclarant et refus de médiation |
| Énergie | Initiative et préférence inverse pour laisser passer |
| Sociabilité | Médiation, accusé de réception et accord du médiateur |
| Rationalité | Sensibilité de la réponse du déclarant à sa position de guerre |
| Avidité | Aucun facteur direct dans cette tranche, les contreparties natives sont encore à négocier |
| Zèle | Aucun facteur direct dans ce profil de guerre de revendication politique |

Les deux dernières lignes conservent leurs effets indirects possibles sur les
opinions, moyens, autres tendances et comportements natifs. L'inventaire général
de AI_DECIDER_AUDIT.md reste distinct. Cette tranche n'achève pas le suivi de
chacun de ses traits dans tous les contextes. Un effet net dépend aussi des
autres choix disponibles et de leurs propres poids.

## Contexte pris en compte

- Une opinion personnelle d'au moins 25 multiplie l'affinité concernée par 1.25.
  Une opinion d'au plus -25 la multiplie par 0.75. Un proche parent ou allié la
  multiplie aussi par 1.25. L'affinité est bornée entre 0.5 et 2. Les liens publics et
  l'opinion ont ici des contributions intentionnellement distinctes.
- Le lige considère le défenseur principal. Le protecteur considère le détenteur
  réel du titre représentatif de son dossier. L'affinité pour l'attaquant favorise
  la retenue et réduit les réponses correctives. L'attachement au camp visé produit
  l'effet inverse. Le médiateur évalue sa propre relation au demandeur et au vassal.
- La capacité d'attention commence à 1. Une guerre en cours, un niveau de stress
  d'au moins 2, une santé inférieure à 3 ou un engagement personnel des familles
  de service/faveur reconnues la multiplient chacun par 0.75.
  Elle est bornée entre 0.25 et 1. Les réponses actives sont réduites, tandis
  que laisser passer ou exprimer une censure peu coûteuse devient plus probable.
- Des fonds inférieurs à 50 réduisent par 0.75 la préférence pour préparer une
  intervention native ou l'accepter comme médiateur. Les messages gratuits ne
  reçoivent aucun coût fictif et gardent leur préférence indépendante de l'or.
- La demande de médiation reçoit un facteur de diplomatie
  `clamp(0.9 + diplomacy/100, 0.75, 1.25)`.
- Le déclarant répond à la demande de son lige avec un facteur de 1.25 pour
  l'accusé de réception et 0.8 pour le refus. Le risque politique de refuser son
  lige reste distinct de celui de refuser une autre autorité protectrice.
- À partir d'un score attaquant de 25, le facteur de position du refus multiplie
  par le facteur de rationalité. À -25 ou moins, il divise par ce facteur.
  L'accusé de réception utilise l'inverse. Cette préférence concerne la teneur
  de la réponse publique. L'effet d'un accusé de réception garde sa portée initiale.

## Choix effectifs

| Choix | Base conservée | Motivations principales |
| --- | --- | --- |
| Laisser passer | 30 | Prudence, affinité attaquant, faible initiative, attention occupée |
| Désapprouver | 30 | Vengeance, fermeté, camp visé, signal politique peu coûteux |
| Demander la fin de guerre | 25 | Compassion, initiative, liens aux deux camps, honneur du lige |
| Intervention native | 20 | Même résolution, capacité d'attention, moyens propres |
| Solliciter le lige adverse | 25 | Résolution, sociabilité, diplomatie, capacité d'attention |
| Accuser réception | 30 | Sociabilité, prudence, relation à l'auteur, rôle, position de guerre |
| Refuser la demande | 20 | Fermeté, vengeance, relation à l'auteur, rôle, position de guerre |
| Accepter la médiation | 30 | Honneur, compassion, initiative, sociabilité, relations aux deux parties, moyens |
| Décliner la médiation | 25 | Vengeance, affinité pour son vassal, relation au protecteur, attention occupée |
| Signaler une tentative existante | 100 | Fait actuel de mise en file ou d'envoi du jour, avec la garde existante |

Les neuf premiers poids admissibles restent entre 1 et 300. Le dernier conserve
son poids de 100 seulement quand son fait et son tour sont valides. Ces bornes
portent sur les préférences. Les actions, prérequis et effets gardent leurs gardes
actuelles. Le nombre de dossiers ou de relations n'est pas plafonné par ce profil.

## Limites conservées

La déclaration de guerre IA et le parcours entre pairs conservent leurs politiques
précédentes. L'âge conserve ses gardes adultes et ses effets natifs indirects.
Martialité et prouesse n'ont aucun coefficient direct dans ces choix diplomatiques.
Foi et culture influencent notamment les opinions et les tendances natives.
Leur appréciation explicite, les intérêts de tous les titres visés, la puissance,
les soutiens attendus, la crainte, les enjeux dynastiques détaillés et les effets
propres de chaque trait restent à revoir. Le profil n'ajoute aucun recours à des
informations secrètes pour remplir ces dimensions.

## Vérifications et campagne groupée

Huit régressions de source couvrent les gardes, les axes du décideur, les rôles,
les contreparties publiques, les poids raccordés et la lecture seule. Les
empreintes de sept fichiers d'effets/gardes/cycle restent identiques. Les deux
graphes d'événements, après retrait des seuls `ai_chance`, restent identiques.
Le kit livré réutilise ces contrôles avec mutations négatives.

Les docs moteur générées confirment les entrées de santé, stress, alliances,
famille et score attaquant en scope de guerre. Les sources de valeurs AGOT
utilisent des divisions par des valeurs dynamiques. Cette inspection confirme
les formes sources utilisées et ne démontre pas leur évaluation dans ce profil.

La campagne finale doit comparer les poids et décisions en changeant un facteur
à la fois, avec personnages dans les rôles inversés, relations contradictoires,
titres représentatifs distincts, stress, santé, engagements, trésorerie et scores
de guerre opposés. Vérifier les profils hors contexte, les fenêtres périmées,
les rechargements, les choix natifs et la conservation des mêmes conséquences.
Observer plusieurs tirages et le coût de calcul. Aucun résultat comportemental
ou de performance nouveau n'est revendiqué.

## Extension du bénéficiaire de la revendication

AI_EXTERNAL_BENEFICIARY.md ajoute l'affinité propre du décideur avec le tiers
revendiquant capturé. Les tours du lige, du protecteur, du déclarant et du
médiateur restent distincts. Le socle et PRIVATE0.0.10 correspondants attestent
32 sources de runtime. Coefficients provisoires, delta0, non testé moteur.

## Extension des titres protégés

AI_PROTECTED_TITLE_STAKES.md ajoute au protecteur un lecteur des titres réellement
visés de ses vassaux directs. Rang maximal, titre principal du détenteur actuel
et pluralité de faits valides modulent sa préoccupation existante. Le socle et
PRIVATE0.0.10 attestent 33 sources de runtime. Coefficients provisoires, delta0,
non testé moteur. Les intérêts des autres décideurs restent à approfondir.

## Extension des autres décideurs et de la médiation

AI_EXTERNAL_TITLE_STAKES.md raccorde les enjeux exacts du conflit au lige du
déclarant, au médiateur et à l'attachement du déclarant à son objectif connu.
Les titres du défenseur principal et des détenteurs sous lui ont leurs gardes
propres. Le socle et PRIVATE0.0.10 attestent 35 sources de runtime. Coefficients
provisoires, delta0, non testé moteur. La revue suivante concerne puissance et
soutiens connus.
