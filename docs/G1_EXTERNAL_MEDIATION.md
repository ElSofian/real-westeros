# Médiation entre le protecteur et le lige du déclarant

Tranche du 8 novembre 2026. **Static-checked**, expérimentale et **non testée
dans CK3**. Baseline et résultat 80/80 source, 0/20 campagne, delta 0.

## Demande du protecteur

Le rôle protecteur d'un dossier extérieur peut désormais solliciter le suzerain
original du déclarant. Dans l'exemple Leyton/Dayne, Doran demande à Mace
d'intervenir auprès de Leyton. Le relevé de déclaration fournit le lige et son
titre d'autorité. Les rôles, titres et parent exact du dossier restent ceux de
G1_EXTERNAL_RESPONSES.md. Le déclarant doit toujours dépendre de ce même lige.

La demande consomme le choix initial du protecteur. Elle capture personnellement
le médiateur et son titre, conserve sa date et ouvre une fenêtre de sept jours.
Le médiateur peut accepter d'essayer, décliner ou signaler une tentative déjà
préparée ou envoyée aujourd'hui. L'acceptation exige les capacités techniques du
parcours natif, dont une seule guerre locale de l'attaquant et un médiateur qui
n'y participe pas. Les réponses revalident les identités et autorités actuelles.

Le refus et le silence ne produisent aucune pénalité automatique. Une demande
périmée ou dont le contexte a changé devient inerte immédiatement et est close
par le nettoyage mensuel. Aucun remplaçant ou héritier ne reçoit le choix.
La demande vise le lige enregistré du déclarant. Une éventuelle sollicitation
d'un supérieur commun conserve un développement séparé.

## Consentement et tentative native

L'accord ferme d'abord la demande, conserve sa date et consomme sa fenêtre.
Une préparation à usage unique crée alors un dossier technique séparé, personnel
et lié à cette demande par identité et numéro. La réaction initiale du médiateur
reste conservée dans son propre dossier. Il peut ainsi reconsidérer sa position
après la sollicitation du protecteur sans réécrire sa première décision.

Le dossier technique réutilise la représentation des réponses extérieures et le
worker natif de G1_EXTERNAL_NATIVE_PEACE.md. Il conserve le même relevé de loi,
numéro parent, guerre, parties et date historique de déclaration. Il enregistre
le médiateur comme lige intervenant, son titre d'autorité et l'origine du
consentement. Les références de demande et de dossier technique sont croisées.

La préparation est consommée avant allocation. Une allocation ou une mise en
file indisponible laisse l'accord enregistré avec un résultat de transmission
indisponible. Elle ne relance pas automatiquement la création. Une préparation
réussie utilise la tentative native différée au lendemain. Le protecteur reçoit
une notification qui distingue ces deux situations.

Le consentement est revalidé à la mise en file, à l'envoi et à la liaison du
callback natif. La demande doit toujours désigner ce dossier et son numéro,
le même médiateur, l'autorité originale, la guerre et les parties. Le contexte
protecteur du titre représentatif doit rester actuel. Les dossiers natifs
antérieurs sans origine de médiation conservent leurs propres gardes.

## Tentatives concurrentes et résultats

Un contrôle local des dossiers de l'attaquant détecte une autre tentative sur
cette guerre exacte. Il examine les mises en file encore vivantes et les envois
du jour, en excluant le dossier lui-même. Il s'applique aux interventions directes
et aux médiations. Plusieurs autorités peuvent solliciter le même lige, avec des
réponses personnelles indépendantes. Une tentative concurrente empêche de préparer
une nouvelle intervention simultanée. Le médiateur peut informer le demandeur
qu'une tentative existe déjà. Les délais et autres restrictions natifs sont
revérifiés par le worker avant chaque véritable envoi.

CK3/AGOT conserve ses conditions, contreparties, coûts, refus et résolution de
guerre. L'accord de médiation, la mise en file et la notification ne démontrent
pas une paix effective. Le nouveau code utilise le worker existant et ne lance
aucun effet natif de guerre ou de paiement lui-même.

## IA, livraison et campagne finale

Les mêmes gardes et effets servent aux joueurs et à l'IA. Les préférences initiales
du protecteur utilisent compassion et hostilité envers l'attaquant. Celles du
médiateur utilisent honneur, relations aux deux parties, vengeance, moyens et
guerres en cours. La revue plus complète des motivations reste ouverte.

Les trois nouveaux fichiers originaux rejoignent les sources de runtime du kit
PRIVATE0.0.10, désormais au nombre de vingt-cinq. Les sorties natives générées
restent identiques à la tranche précédente. Utiliser le socle et les adaptateurs
du même commit. Huit régressions de source et une vérification du kit livré avec
mutations couvrent les rôles, le consentement, le rejeu, la conservation de la
décision initiale, les tentatives concurrentes et l'expiration.

La campagne finale doit observer Doran/Mace/Leyton avec joueur et IA dans chaque
rôle, une réaction initiale de Mace déjà close, plusieurs protecteurs, une tentative
native déjà en cours, les changements d'autorité, de titre ou de chef de guerre,
le refus, le silence, les rechargements et les échecs de transmission. Elle doit
suivre la négociation native et ses coûts jusqu'à l'issue réelle de la guerre,
y compris avec Mega Wars. Aucune observation moteur nouvelle n'est revendiquée.
