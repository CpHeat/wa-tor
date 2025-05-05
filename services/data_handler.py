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



forme finale du data a enregistrer :

dict = {
    "simulation_id": 0
    "date": DATE,
   "duration":SMALLINT,
   "grid_height" SMALLINT,
   "grid_width" SMALLINT,
   "animal_count" SMALLINT,
   "fish_count" SMALLINT,
   "shark_count" SMALLINT,
   "life_expectancy" NUMERIC(8,2)  ,
   "fish_life_expectancy" NUMERIC(8,2)  ,
   "shark_life_expectancy" NUMERIC(8,2)  ,
   "reproduction" SMALLINT,
   "fish_reproduction" SMALLINT,
   "shark_reproduction" SMALLINT,
   "fish_eaten" SMALLINT,
   "shark_starved" SMALLINT,
   "detail": {
       "chronon":,
       animal_count SMALLINT,
       fish_count SMALLINT,
       shark_count SMALLINT,
       reproduction SMALLINT,
       fish_reproduction SMALLINT,
       shark_reproduction SMALLINT,
       fish_eaten SMALLINT,
       shark_starved SMALLINT,
   }
}



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