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
from abc import ABC

class DataHandler(ABC):
    simulation_chrononwise_data = []

    @classmethod
    def chronon_data_handling(cls, simulation_data: dict):
        """
        calculer les enfant nés
        stocker les poissons morts
        stocker le nb d'individus
        stocker l'age des morts
        """
        chronon_data = {
            'fishes_born': simulation_data['nb_reproduction_fish'],
            'sharks_born': simulation_data['nb_reproduction_shark'],
            'total_born': simulation_data['nb_reproduction_fish'] + simulation_data['nb_reproduction_shark'],
            'fishes_eaten': simulation_data['fishes_eaten'],
            'sharks_starved': simulation_data['sharks_starved']
        }

        cls.simulation_chrononwise_data.append(chronon_data)


    def simulation_end_data_handling(self):
        pass