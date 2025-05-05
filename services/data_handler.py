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
   fish_starting_population SMALLINT,
   shark_starting_population SMALLINT,
   fish_reproduction_time SMALLINT,
   shark_reproduction_time SMALLINT,
   shark_starvation_time SMALLINT,
   shark_energy_gain SMALLINT,
   shuffled_entities BOOLEAN,
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
from datetime import datetime

from services.persistence_handler import PersistenceHandler


class DataHandler(ABC):
    simulation_chronon_data = []
    simulation_data = None

    @classmethod
    def reset_data(cls):
        cls.simulation_chronon_data = []
        cls.simulation_data = None

    @classmethod
    def chronon_data_handling(cls, simulation_chronon, simulation_chronon_data: dict):
        """
        calculer les enfant nés
        stocker les poissons morts
        stocker le nb d'individus
        stocker l'age des morts
        """
        # chronon_data = {
        #     'chronon': simulation_chronon,
        #     'animal_count': ,
        #     'fish_count': ,
        #     'shark_count': ,
        #     'fish_reproduction': simulation_chronon_data['nb_reproduction_fish'],
        #     'shark_reproduction': simulation_chronon_data['nb_reproduction_shark'],
        #     'total_born': simulation_chronon_data['nb_reproduction_fish'] + simulation_chronon_data['nb_reproduction_shark'],
        #     'fishes_eaten': simulation_chronon_data['fishes_eaten'],
        #     'sharks_starved': simulation_chronon_data['sharks_starved']
        # }

        # cls.simulation_chrononwise_data.append(chronon_data)

    @classmethod
    def final_data_handling(cls, simulation_chronon_data):

        simulation_id = PersistenceHandler.get_next_simulation_id()

        data = {
            "simulation_id": simulation_id,
            "date": datetime.now(),
            "duration": 50,
            "grid_height": 10,
            "grid_width": 10,
            "fish_starting_population": 8,
            "shark_starting_population": 6,
            "fish_reproduction_time": 9,
            "shark_reproduction_time": 8,
            "shark_starvation_time": 4,
            "shark_energy_gain": 3,
            "shuffled_entities": True,
            "animal_count": 54,
            "fish_count": 12,
            "shark_count": 47,
            "life_expectancy": 2.87,
            "fish_life_expectancy": 5.87,
            "shark_life_expectancy": 6.51,
            "reproduction": 10,
            "fish_reproduction": 7,
            "shark_reproduction": 5,
            "fish_eaten": 45,
            "shark_starved": 23,
            "detail": [
                {
                    "chronon": 1,
                    "animal_count": 14,
                    "fish_count": 75,
                    "shark_count": 54,
                    "reproduction": 5,
                    "fish_reproduction": 4,
                    "shark_reproduction": 3,
                    "fish_eaten": 14,
                    "shark_starved": 57,
                },
                {
                    "chronon": 2,
                    "animal_count": 58,
                    "fish_count": 45,
                    "shark_count": 1,
                    "reproduction": 7,
                    "fish_reproduction": 3,
                    "shark_reproduction": 8,
                    "fish_eaten": 145,
                    "shark_starved": 87,
                }
            ]
        }

        pass

