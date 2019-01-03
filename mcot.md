# MCOT
## Titre

Planification de trajet dans un réseau de transports en commun.

## Bibliographie commentée (commune, moins de 500 mots)

L’augmentation de l’importance des transports en commun nécessite la réali-
sation d’algorithmes effiaces de planification de trajets les utilisant. De plus, les
initatives d’ouvertures des données (notamment cartographiques) ont permis
à des équipes de recherche de tester facilement les algorithmes qu’elles déve-
loppent.

L’ordre de grandeur des problèmes que doivent pouvoir résoudre les algo-
rithmes de planification de trajet modernes sont des réseaux de quelques millions
de connexions quotidiennes et de plusieurs milliers d’arrêts. De plus, le besoin
de proposer aux utilisateur des services en ligne qui calculent les itinéraires rend
nécessaire l’optimisation des algorithmes utilisés, pour qu’ils puissent être uti-
lisés dans ces services : le site de la Deutsche Bahn (la compagnie du réseau
ferroviaire allemand) répond à une centaine de requêtes par seconde, chacune
s’étendant potentiellement sur toute l’Allemagne.

En 2009, l’article 1 lance les recherches centrées sur la planification de trajets
en transport en commun, en soulignant que les algorithmes développés pour les
trajets en voitures (descendants de l’algorithme de Dijkstra pour la plupart) ne
sont pas adaptés à ce problème. En effet, les trajets possibles ne peuvent se faire
qu’à des heures données, et de plus, en fonction des conditions de circulation,
le même trajet peut prendre plus ou moins de temps.

En 2010, Hannah Bast publie un algorithme nommé Transfer Patterns 3, qui
parvient quand même à utiliser des graphes pour résoudre le problème. Cepen-
dant, sa technique nécessite un précalcul conséquent, estimé dans 4 équivalent
à 4 mois de calcul pour un ordinateur seul, ce qui est de toute façon hors de
notre portée matériellement.

L’algorithme que nous avons étudié a été publié en 2013 dans l’article 2
sous le nom de Connection Scan Algorithm (CSA). Ce dernier se distingue des
algorithmes précédents, en ceci qu’il n’utilise pas de graphes, mais des techniques
de programmation dynamique utilisant des tableaux. Un article 4 publié par
certains des auteurs de l’article original revient sur CSA en proposant des idées
d’optimisation de l’algorithme, qui en font sans conteste l’algorithme le plus
rapide dans le domaine étudié.

Il est évident que, sans précalcul, il faut au minimum, à chaque requête,
analyser toutes les connexions existantes, ce qui prend nécessairement un temps
conséquent. Cependant, avec précalcul, toute modification des horaires (à cause
d’accidents, de travaux...) nécessite de recommencer le précalcul, ce qui peut
prendre un temps considérable. Trouver une façon d’accorder la rapidité de
réponse à une requête et la capacité à d’adapter à une modification des horaires
est un problème conséquent.

De plus, dans chaque trajet fait en transports en commun, il y a de la marche.
Il faut donc à la fois prendre en compte des moyens de transport régis par des
horaires et des moyens de transport libres (ici, la marche). Parvenir à coupler
ces deux façons différentes de se déplacer est aussi un enjeu complexe puisqu’il
faut à la fois garantir l’optimalité du résultat et donner le résultat rapidement.

## Bibliographie

1. Hannah Bast, Car Or Public Transport – Two Worlds, https://www.researchgate.net/profile/Hannah_Bast/publication/262319862_Car_or_Public_Transport--Two_Worlds/links/0046353c641380991a000000/Car-or-Public-Transport--Two-Worlds.pdf
2. Julian Dibbelt, Thomas Pajor, Ben Strasser, Dorothea Wagner, Intri-guingly Simple and Fast Transit Routing, https://i11www.iti.kit.edu/extra/publications/dpsw-isftr-13.pdf
3. Hannah Bast, Erik Carlsson, Arno Eigenwillig, Robert Geisberger, Chris
Harrelson, Veselin Raychev, Fabien Viger, Fast Routing in Very Large
Public Transportation Networks using Transfer Patterns, http://ad.informatik.uni-freiburg.de/files/transferpatterns.pdf
4. Ben Strasser, Dorothea Wagner, Connection Scan Accelerated, https://epubs.siam.org/doi/pdf/10.1137/1.9781611973198.12
