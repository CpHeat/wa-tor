"""
dict{'grid', 'entities', 'fishes_eaten', 'nb_fish', 'nb_shark', 'nb_reproduction_shark', 'nb_reproduction_fish', 'dead_fishes_age', 'dead_sharks_age'}

esperance de vie des poissons:
a chaque tour calculer la moyene du tour, + le nombre de poissons concernés, ajouter a la moyene précédente * nb de poissons morts totaux, diviser par poissons totaux + novueaux poissons, stocker moyene + poissons totaux actualisés

nb reproduction moyenne
previous * nb de tour + nouvelle / nb de tour +1

en fin de simulation
generer une esperance de vie generale
generer un taux de reproduction general
recup nb de poissons
recup nb de requins
"""