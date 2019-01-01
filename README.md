# oxf5
Implémentation de l'algorithme CSA sur tout réseau de transport en commun publiant ses horaires au format GTFS.

## Installation d'un réseau
Les fichiers stop_times.txt, stops.txt, etc. correspondants doivent être mis dans ./data/nom_de_ces_horaires (nom_de_ces_horaires est un identifiant arbitraire comme "lyon", "confiture_de_fraises", ou "horaires_42"). Il faut ensuite appeler :


$ python3 src/make_connections.py nom_de_ces_horaires

(ce qui prend quelques minutes). Ensuite, on utilise le script principal, csa2.py, comme suit :

$ python3 src/csa2.py nom_de_ces_horaires id1 id2 heure

Où id1 et id2 sont respectivement les identifiant des arrêts de départ et d'arrivée, et heure, l'heure minimale de départ.

## Plus d'informations

Voir le wiki.
