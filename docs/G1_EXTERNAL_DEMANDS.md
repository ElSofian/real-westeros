# Demandes politiques des autorités extérieures

Tranche du 8 novembre 2026. **Static-checked**, expérimentale et **non testée dans
CK3**. Baseline et résultat 80/80 source, 0/20 campagne, delta 0.

## Demande et réponse personnelles

Le dossier extérieur peut désormais porter une demande de mettre fin à la guerre.
Le suzerain du déclarant et chaque autorité protectrice conservent leur décision
indépendante. L'auteur doit encore détenir son autorité enregistrée et le dossier
doit conserver son contexte exact de guerre, de parties et de titre représentatif.
Les règles d'admission de G1_EXTERNAL_RESPONSES.md restent applicables.

La demande consomme le choix initial de sept jours avant l'envoi du message.
Elle conserve sa date et ouvre une fenêtre de réponse distincte de sept jours
pour le déclarant original. L'autorité ne peut alors revenir à la désapprobation
ou envoyer une seconde demande depuis ce dossier. Les choix d'une autre autorité
gardent leur propre état et leur propre fenêtre.

Le déclarant peut accuser réception ou refuser. L'accusé de réception clôt la
demande avec une date de réponse et informe son auteur. La négociation d'une paix
effective, son acceptation par les parties et les éventuels engagements restent
à développer. Le texte du choix précise explicitement cette portée.

Un refus clôt d'abord la demande et consomme sa fenêtre, puis applique la réaction
politique de son auteur. Refuser son suzerain direct entraîne -15 d'opinion pendant
deux ans, avec le modificateur existant de refus. Refuser le protecteur du camp
attaqué entraîne -10 pendant deux ans, avec le modificateur existant de censure.
Le protecteur exerce ici une pression politique distincte de l'autorité du lige.

## Identité et expiration

Un contrôle d'identité commun est utilisé par les deux tours. Le tour de
l'autorité exige le personnage enregistré, l'état initial et sa fenêtre. Le tour
du déclarant exige le déclarant enregistré, l'état de demande, sa date et la
fenêtre de réponse. Les contrôles revalident la guerre, les chefs principaux,
le parent et son numéro, le titre d'autorité et le contexte du rôle protecteur.
Une succession, un transfert ou un changement de chef ne transmet pas le choix.

Les effets consomment l'état avant opinion ou notification. Les événements tardifs,
rejoués ou présentés à un tiers ne peuvent exécuter la réponse. Les fenêtres
expirées refusent immédiatement les effets. Le nettoyage mensuel clôt les demandes
expirées avec un résultat neutre. Le silence ne produit aucune opinion de refus.
Les règles de conservation et de nettoyage des dossiers précédents subsistent.

Les dossiers initiaux créés avant cette extension restent utilisables s'ils
satisfont leurs gardes actuelles. Seul l'envoi explicite d'une demande crée sa
date et sa fenêtre de réponse. Les dossiers déjà clos restent clos.

## IA, livraison et suite

Les joueurs et l'IA exécutent les mêmes gardes et effets. Les préférences initiales
différencient l'honneur du lige et la compassion du protecteur, puis leurs moyens,
guerres et opinion du déclarant. La réponse utilise l'honneur, l'audace, la
vengeance et l'opinion de l'auteur. La revue exhaustive du contexte reste ouverte.

Les fichiers existants de PRIVATE0.0.9 portent cette extension. Aucun nouvel ajout
au code natif n'est nécessaire. Utiliser le socle et les adaptateurs du même
commit. Six régressions supplémentaires contrôlent les tours, les réponses, la
séparation des autorités, les fenêtres, l'absence de conséquence d'un accusé de
réception et les dossiers antérieurs. Le contrôle du kit livré réutilise ces
gardes avec des mutations négatives supplémentaires.

La campagne finale doit observer des demandes simultanées, les deux rôles,
les réponses joueur/IA, le rechargement, l'expiration silencieuse, les événements
rejoués, les changements de contexte et les conséquences d'opinion exactes.
Les conditions natives du CB, de la guerre et de sa résolution restent à vérifier
dans ce nouveau parcours. La suite porte sur une réponse négociée avec des termes
explicites, puis son lien à une paix native et à une éventuelle aide supérieure.
