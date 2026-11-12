# Revue des valeurs et conséquences

## Contributions institutionnelles, 12 novembre 2026

B4 reçoit un [barème de contribution](INSTITUTIONAL_CONTRIBUTIONS.md) fixé selon
le payeur initial. Les nouveaux montants institutionnels sont50/100/200/400or et
les contrats déjà proposés gardent leur somme. Leurs transferts utilisent le
montant validé et consenti. Validation en jeu dans la campagne groupée.80/80+0/20,
delta réel+0.

## Correction du soutien et des promesses, 12 novembre 2026

B2/B3 reçoivent le [barème partagé](SUPPORT_REWARD_BALANCE.md). Le prestige dépend
du rang interne du prestataire et le bonus de la paire se renouvelle après un an.
La rupture du soutien contre or rejoint les engagements comparables à−15 pendant
deux ans. Les anciennes valeurs ci-dessous conservent leur rôle de relevé initial.
Validation en jeu dans la campagne groupée.80/80+0/20, delta réel+0.

## Suivi du 12 novembre 2026

B1 reçoit un correctif source avec une dernière décision discrétionnaire de
l'autorité après réponse ou silence. Les gardes et scénarios sont décrits dans
[PEACE_DEMAND_REVIEW.md](PEACE_DEMAND_REVIEW.md). Validation moteur à effectuer
pendant la session groupée du plan de cinq jours accepté par le propriétaire.
Les constats chiffrés ci-dessous décrivent la base auditée.80/80+0/20, delta réel +0.

## Conclusion du 9 novembre 2026

**Revue statique des scripts livrés. Équilibrage à corriger sur plusieurs points.**
Base examinée `77c7c72ee9d33527223f4b907369b3bd5bd9ab07`, dont les deux derniers
commits réservent les tâches. Les chiffres ci-dessous sont ceux du code. Aucun
montant de gameplay modifié dans cette revue. Baseline et résultat 80/80 source,
0/20 campagne, delta réel +0.

L'inventaire couvre les effets directs propres au mod dans les huit systèmes,
leurs appelants, leurs gardes de paiement/résolution, les opinions et les textes
FR/EN concernés. Il comporte 15 définitions d'opinion, 20 applications d'opinion,
8 applications de prestige et 11 couples débit/crédit d'or. Les conséquences
natives des guerres, révocations, arrestations et exécutions restent déléguées à
CK3/AGOT. Leur montant final et les interactions entre couches restent à observer.

## Points prioritaires

### B1 — La demande de paix possède une réponse mécaniquement avantageuse

L'accusé de réception ferme le dossier, laisse la guerre active et n'impose ni
engagement ni malus propre. Le refus explicite ferme aussi le dossier, mais coûte
15 d'opinion auprès du suzerain direct ou 10 auprès du protecteur extérieur.
Pour les effets propres à ces deux réponses, le premier choix est avantageux.
Le silence reste également neutre. La sélection IA peut préférer le refus pour
ses motivations, mais cette préférence ne crée aucune conséquence supplémentaire.

Le code et les textes concordent. Il s'agit d'une faiblesse de la décision de jeu.
La demande politique actuelle ne fournit aucun suivi propre après cet accusé.
L'intervention native demeure une autre décision du suzerain, soumise à ses gardes.
Un refus ne doit jamais devenir un crime automatiquement.

**Correction prioritaire à concevoir** — distinguer clairement une simple
notification d'une demande suivie d'une décision discrétionnaire de l'autorité.
Conserver le vrai CB et les conséquences natives. Éviter de faire de l'accusé une
fausse acceptation de paix ou une promesse implicite.
[Pairs](../mod/real_westeros/common/scripted_effects/rw_unlawful_war_response_effects.txt),
[extérieur](../mod/real_westeros/common/scripted_effects/rw_external_war_response_effects.txt).

### B2 — Tous les soutiens délivrent exactement 50 de prestige

Les cinq versements sont identiques, en service immédiat/différé contre or,
service immédiat/différé contre faveur, et clause de soutien d'un accord multiple.
Le rang, l'importance publique et le poids du prestataire ne modifient pas cette
récompense. Le service est payé 25 ou 50 or après négociation, ou par un hameçon de
faveur dans l'autre parcours. Une réduction négociée du prix conserve logiquement
le même service, mais la valeur de ce service reste uniforme pour tous les acteurs.

Le délai commun de 365 jours borne les nouvelles offres d'un même prestataire
pour les services or/faveur. Il ne borne pas les gains du bénéficiaire venant de
plusieurs prestataires. La famille des accords multiples a son propre délai de
90 jours et ses conditions institutionnelles. Le drapeau de mémoire publique
réduit les souvenirs créés, sans réduire les gains de prestige. Les contrats sont
protégés contre le rejeu individuel. Cela ne fournit pas un équilibrage global des
soutiens distincts.

**Correction prioritaire à préparer** — une valeur partagée du soutien, avec une
différence simple selon son importance et une règle explicite de répétition du
même soutien. Préserver les interactions utiles et les contrats distincts. Aucun
nouveau coefficient n'est validé par cette revue. Les IA initient actuellement ces
services vers leur suzerain, ce qui rend le cumul par plusieurs vassaux pertinent.
[Service](../mod/real_westeros/common/scripted_effects/rw_service_effects.txt),
[faveur](../mod/real_westeros/common/scripted_effects/rw_favor_service_effects.txt),
[accord multiple](../mod/real_westeros/common/scripted_effects/rw_multi_action_effects.txt),
[mémoire](../mod/real_westeros/common/scripted_effects/rw_political_memory_effects.txt).

### B3 — La durée du ressentiment dépend trop du parcours technique

Un soutien promis contre or puis rompu peut donner −15 pendant cinq ans.
La renonciation au soutien promis contre faveur, à une restitution promise ou à
une retenue militaire donne −15 pendant deux ans. Le soutien contre faveur
comprend aussi une variante négociée contre 25 or. Le seul mode de paiement ne
justifie donc pas les trois années supplémentaires de ressentiment.

**Correction prioritaire à préparer** — harmoniser les ruptures comparables ou
justifier une durée différente par la gravité et l'enjeu de l'engagement. Le
premier correctif peut rester limité à ces durées. Les réponses demeurent au choix
du bénéficiaire.
[Service](../mod/real_westeros/common/opinion_modifiers/rw_obligation_opinions.txt),
[faveur](../mod/real_westeros/common/opinion_modifiers/rw_favor_renunciation_opinions.txt),
[restitution](../mod/real_westeros/common/opinion_modifiers/rw_restitution_pledge_opinions.txt).

### B4 — Les paiements institutionnels et personnels ont la même petite échelle

25/50 or couvrent les services et compensations, 50 or la réhabilitation négociée
d'une maison et une promesse patrimoniale/dynastique. Les montants ne varient pas
avec les revenus, le rang, les biens disputés ou l'ampleur du préjudice. Les moyens
financiers influencent certaines préférences IA et la capacité de payer, sans
modifier le prix contractuel.

**Calibration ouverte** — ces montants sont encore des bases provisoires. Séparer
l'équilibrage des petits services personnels de celui des décisions
institutionnelles. Conserver les montants acceptés d'un contrat existant lors
d'une future évolution. La campagne doit inclure un petit seigneur et un grand
souverain avant de retenir une nouvelle échelle.

### B5 — Légitimité et stress des choix propres ne disposent pas de politique complète

Aucun effet direct propre au mod n'ajoute ou retire de légitimité, stress, piété,
effroi ou renommée dynastique. Les axes de personnalité, le stress et l'effroi
peuvent contribuer à une préférence IA. Ils ne produisent pas par eux-mêmes une
conséquence de l'action choisie. Les actes natifs peuvent conserver leurs propres
effets, notamment stress, tyrannie et opinion.

Cette absence de code ne démontre pas qu'un zéro a été étudié pour chaque acte.
Les décisions publiques de reconnaissance, disgrâce ou défi méritent une politique
explicite de légitimité. Les échanges privés peuvent garder un zéro justifié.
De même, les choix propres de mensonge, rupture ou sanction doivent être confrontés
aux traits concernés pour le stress, en évitant le double effet d'un acte natif.
Ces lacunes restent ouvertes. La revue ne leur attribue aucun point de livraison.

## Valeurs d'opinion actuelles

Les flèches indiquent qui éprouve l'opinion et envers qui. Les durées sont celles
des définitions. Aucun des 15 modificateurs ne précise `decaying` ou `stacking`.
La documentation de format installée présente leurs défauts à `no` et décrit la
réapplication simple comme un renouvellement de durée. Ils sont donc écrits comme
des valeurs fixes jusqu'à échéance. Vérifier l'affichage et le renouvellement dans
la version moteur installée reste un scénario de campagne.

| Action et opinion | Sens | Valeur | Durée | Revue |
|---|---|---:|---:|---|
| Réconciliation acceptée | Chaque partie → l'autre | +10 | 2 ans | Amélioration bilatérale modérée, cohérente |
| Réconciliation refusée | Pétitionnaire → destinataire | −5 | 1 an | Déception légère, cohérente |
| Soutien contre or promis puis rompu | Client → prestataire, si ressentiment choisi | −15 | 5 ans | Durée à harmoniser, B3 |
| Renonciation au soutien contre faveur/or | Client → prestataire, si ressentiment choisi | −15 | 2 ans | Référence comparable pour B3 |
| Réprimande après dossier | Médiateur → prestataire | −10 | 2 ans | Désapprobation personnelle cohérente |
| Excuses après dossier | Médiateur → prestataire, puis client → prestataire si réception acceptée | +5 chacun | 2 ans | Deux relations distinctes, geste modeste |
| Compensation appréciée | Client → prestataire payeur | +5 | 2 ans | Réponse volontaire, cohérente |
| Réparation après observation de complot | Observateur → participant payeur | +5 | 2 ans | N'efface pas les conséquences natives |
| Disgrâce de maison | Chef actuel → autorité émettrice | −20 | 5 ans | Ressentiment personnel distinct du décret institutionnel de 50 ans |
| Réhabilitation gratuite de maison | Souverain → pétitionnaire | +10 | 2 ans | Sens conforme au texte, représente la faveur du souverain |
| Restitution refusée | Demandeur → détenteur, si ressentiment choisi | −10 | 2 ans | Refus moins grave qu'une promesse rompue |
| Restitution promise puis renoncée | Demandeur → détenteur, si ressentiment choisi | −15 | 2 ans | Gradation −10/−15 cohérente |
| Retenue militaire promise puis violée | Bénéficiaire → prestataire, si ressentiment choisi | −15 | 2 ans | Base comparable pour B3 |
| Censure de guerre / désapprobation extérieure | Autorité → attaquant | −10 | 2 ans | Désapprobation modérée |
| Refus d'arrêter la guerre | Suzerain direct → attaquant | −15 | 2 ans | Plus sévère que la censure, faiblesse de choix B1 |

Le protecteur extérieur utilise −10 lors du refus, avec le modificateur de censure.
Il exprime un intérêt distinct de l'autorité du suzerain direct. Les autorités
éprouvent leurs opinions séparément. Les choix censure/demande/intervention sont
des branches alternatives du premier tour. Ne pas additionner automatiquement
−10 et −15 pour une seule réponse de la même autorité.

La réhabilitation gratuite améliore actuellement l'opinion du souverain envers
le pétitionnaire. Elle n'ajoute pas de gratitude dans l'autre sens. La
réhabilitation contre 50 or clôt le décret sans ajouter ce +10. Les deux textes
sont cohérents avec leur code. Ce sont deux variantes de faveur à présenter
explicitement lors de la revue de justice.
[Définitions](../mod/real_westeros/common/opinion_modifiers/),
[réhabilitation](../mod/real_westeros/common/scripted_effects/rw_house_affair_effects.txt),
[conditions payantes](../mod/real_westeros/common/scripted_effects/rw_house_terms_effects.txt).

### Cumul et renouvellement

Chaque résolution possède des gardes de dossier/version/tour avant ses effets.
La non-réapplication explicite du même modificateur existe pour compensation,
réparation de complot, disgrâce/réhabilitation et plusieurs réponses aux
renonciations. Elle manque sur réconciliation, ressentiment du service contre or,
réprimande/excuses et réponses de guerre. Une nouvelle affaire peut donc renouveler
un modificateur existant dans ces derniers parcours. Des identifiants d'opinion
différents peuvent coexister sur la même relation.

Cette différence de renouvellement doit être choisie et testée explicitement.
Elle ne permet pas de conclure que tous les malus s'additionnent à chaque clic.
Un cas ancien et une affaire nouvelle doivent conserver leurs identités distinctes.

## Prestige et or actuels

| Effet | Qui paie / reçoit | Montant direct |
|---|---|---:|
| Soutien immédiat ou différé contre or | Client paie prestataire, client reçoit prestige | 25/50 or et +50 prestige |
| Soutien immédiat ou différé contre faveur | Prestataire obtient hameçon sur client, client reçoit prestige | Hameçon natif ou variante 25 or, +50 prestige |
| Soutien d'accord multiple | Bénéficiaire de la clause | +50 prestige, indépendamment des autres clauses |
| Excuses après dossier | Prestataire présentant les excuses | −25 prestige |
| Regrets publics après ultimatum | Destinataire choisissant les regrets | −25 prestige |
| Décret de disgrâce | Souverain émetteur | −50 prestige |
| Compensation privée d'un service | Prestataire → client | 25/50 or |
| Retrait négocié d'allégation | Répondant → accusateur | 25/50 or |
| Compensation de charte | Souverain original → chef original | 25/50 or |
| Clause monétaire d'accord multiple | Payeur de clause → bénéficiaire de clause | 25/50 or |
| Réhabilitation négociée | Pétitionnaire → souverain accepté | 50 or |
| Promesse patrimoniale/dynastique | Payeur validé → bénéficiaire validé | 50 or |
| Réparation après complot observé | Participant → observateur consentant | 25 or |

Les cinq soutiens et les trois pertes de prestige totalisent les huit sites
identifiés. Les deux variantes de paiement des soutiens or/faveur, leurs chemins
différés et les sept autres transferts totalisent les onze couples débit/crédit.
Les paiements de compensation ne récompensent pas automatiquement le payeur en
prestige. Les propositions, contre-offres et simples relectures ne transfèrent
rien. Les prix 25/50 sont contrôlés par leurs gardes, directement ou par le protocole
contractuel commun. Le payeur est revalidé avant débit et le même montant est
crédité au bénéficiaire. La résolution est consommée avant les effets natifs.

Le coût de guerre, la paix blanche, les demandes natives d'arrêt de guerre,
les révocations, arrestations et exécutions conservent les coûts/récompenses du
moteur et d'AGOT. Ils ne sont pas inclus dans les huit effets de prestige propres.
L'affichage antérieur de 65 ou 150 prestige et de 790 or ne définit pas un barème
fixe Real Westeros. Mesurer les effets finaux et les éventuels doublons fait partie
de V1/V3/V5.

## Couverture des huit systèmes

| Système | Conclusion de cette revue |
|---|---|
| Liberté et légalité | Branches territoriales distinguées, gradation −10/−15, réponse avantageuse B1 et légitimité ouverte B5 |
| Affaires politiques | Réconciliation +10/−5 et réactions facultatives cohérentes, renouvellement à observer |
| Négociation | Prix/version/consentement cohérents en source, échelle des montants ouverte B4 |
| Promesses | Paiement à prestation et absence de récompense à signature cohérents, durée de rupture B3 |
| Justice | Coûts −25/−50 explicites, effets natifs séparés, faveur et gratitude distinguées, échelle institutionnelle B4 |
| Information | Allégation, paiement et regrets ne créent pas seuls un crime ni un pardon natif |
| Mémoire | Souvenirs publics bornés séparément, sans contrôle partagé des récompenses B2 |
| IA politique | Exécution partagée, préférences ne suffisent pas à contextualiser les montants ou ajouter du stress B2/B4/B5 |

## Vérification et suite bornée

300 tests existants de 18 modules ciblés passent, y compris les chemins négatifs
sur identité, coût, fonds insuffisants et rejeu. Première exécution interrompue
par l'accès Windows à une fixture temporaire. Relance avec un répertoire de tests
accessible réussie. Les contrôles structurels, télémétrie, score et diff sont
à enregistrer avec la PR. Ces tests ne mesurent pas l'équilibrage du jeu.

Prochaine correction à borner avant assemblage, B1 sur la demande politique.
B2/B3 constituent les deux autres corrections de cohérence prioritaires.
B4/B5 restent des calibrations et lacunes explicites à rapprocher des observations
de campagne. Ne pas lancer une simulation militaire supplémentaire pour les résoudre.
La campagne groupée conserve l'ensemble de ses scénarios et critères gelés.
