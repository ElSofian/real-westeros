# Effectifs militaires et prudence à la déclaration

Tranche RW-004 du 8 novembre 2026. **Static-checked**, expérimentale,
**non testée dans CK3**. Départ et résultat 80/80 source et 0/20 campagne finale.
Delta réel 0.

## Périmètre et connaissances

La présélection initiale du défi prend désormais en compte trois déficits
numériques. Les identités sont celles déjà disponibles dans la fenêtre native,
avec déclarant, destinataire et lige actuel du déclarant. Le contexte complet
est vérifié avant de lire les métriques dépendantes de ces identités.

`current_military_strength` donne l'effectif courant natif du personnage.
`max_military_strength` donne son maximum natif. La métrique courante est distincte
de `current_raised_military_strength`. Le profil utilise les quantités courantes
et le maximum propre. Il ne convertit pas ce maximum en renforts promis.

Le destinataire est celui de l'interaction. Le défenseur final du CB, les titres
sélectionnés et les coalitions restent des contextes à vérifier séparément.
Les valeurs natives d'un lige peuvent inclure leurs agrégations natives. Les
deux comparaisons sont des signaux de risque distincts et ne somment pas les
soldats du déclarant et du lige en une armée commune.

Cette première étape traite les effectifs natifs et leur état. Les renforts
alliés attendus, leur disponibilité, leur consentement et les soutiens déjà
engagés gardent la revue suivante. Les relations d'alliance déjà pondérées dans
le profil conservent leur portée relationnelle. Qualité des troupes, commandement,
terrain, ravitaillement, distance et dragons restent à approfondir.

## Formules et coefficients provisoires

Soient A l'effectif courant du déclarant, D celui du destinataire, L celui de
son lige, M son propre maximum natif et R son facteur de rationalité.

| Composante | Condition numérique | Ajout de prudence avant rationalité |
|---|---|---|
| Infériorité face au destinataire | A >= 0, D > 0 et A < D | 20 × (1 − A/D) |
| Infériorité face au lige | A >= 0, L > 0 et A < L | 15 × (1 − A/L) |
| Écart au maximum propre | A >= 0, M > 0 et A < M | 10 × (1 − A/M) |

Chaque composante commence à 0. À effectifs égaux ou supérieurs à la référence,
elle vaut 0. Un dénominateur nul et une quantité courante négative la laissent
également à 0. Chaque division est protégée par un dénominateur strictement
positif dans sa propre condition numérique. Une quantité négative fournie par
le moteur est traitée comme inutilisable pour cette composante.

Les trois composantes sont bornées respectivement à 0..20, 0..15 et 0..10. Leur
somme est multipliée par le facteur de rationalité propre R, déjà borné à
0.5..1.5. Le risque militaire final reste entre 0 et 67.5. Ce risque s'ajoute à
la prudence existante, qui garde ses bornes de 0 à 250 et son seuil hors contexte
de 1000. La motivation conserve son calcul antérieur. Les coefficients sont
provisoires.

Par exemple, A=1000, D=2000, L=4000 et M=2000 donnent 10 + 11.25 + 5, soit
26.25 avant rationalité. Avec R=1, la prudence reçoit 26.25. Ce calcul illustre
la formule source. Son évaluation effective dans CK3 reste à observer.

## Vérifications et livraison

Les docs moteur générées décrivent ces métriques en scope de personnage. Les
sources AGOT inspectées utilisent déjà `current_military_strength` et sa division
par une référence. L'interface native expose des indicateurs d'effectif dans
les listes de personnages et dans la fenêtre de déclaration. Cette inspection
établit les formes utilisées, sans démontrer l'évaluation de ce profil ni une
équivalence entre effectif et probabilité de victoire.

Huit tests de source et un contrôle du kit livré vérifient le contexte avant les
lectures, dénominateurs positifs, quantités négatives, égalité, références distinctes,
sens de la formule, bornes, rationalité propre et raccordement à la prudence.
Les mutations négatives retirent les gardes ou inversent les références. Une
inversion enlève les quatre nouvelles valeurs et l'ajout à la prudence pour
comparer l'intégralité du profil précédent. Le contrôle de déclaration existant
conserve ses gardes de loi, hameçon et identités, ainsi que son interdiction des
écritures, tirages et recherches globales.

Les valeurs résident dans le fichier déjà livré et attesté. Le socle et
PRIVATE0.0.10 correspondants conservent 35 sources de runtime. Les quatre sorties
natives restent identiques. Les autres profils, effets et cycles conservent leur
contenu. Aucune permission ou conséquence supplémentaire n'est créée.

La campagne finale doit comparer infériorité, égalité, supériorité, deux effectifs
nuls, référence nulle, maximum nul, forces entamées et rationalités opposées.
Observer la case initiale, son choix final, découverte native et envoi, avec joueur
et IA, hameçon sélectionné, exceptions de loi et de contrat, changements de cible
ou de lige, rechargements, CB et coûts réels, Mega Wars et coût de calcul. Les
coalitions et soutiens restent explicitement à qualifier. Aucun lancement manuel
intermédiaire requis.
