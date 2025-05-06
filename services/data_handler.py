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

savoir combien de poissons a mangé un requin en moyenne, au min, au max




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
   "fishes_eaten" SMALLINT,
   "shark_starved" SMALLINT,
   "detail": {
       "chronon":,
       animal_count SMALLINT,
       fish_count SMALLINT,
       shark_count SMALLINT,
       reproduction SMALLINT,
       fish_reproduction SMALLINT,
       shark_reproduction SMALLINT,
       fishes_eaten SMALLINT,
       shark_starved SMALLINT,
   }
}



"""
from abc import ABC
from datetime import datetime

from classes.fish import Fish
from classes.shark import Shark
from services.persistence_handler import PersistenceHandler
from settings import simulation_parameters


class DataHandler(ABC):
    simulation_chronon_data = []
    simulation_data = None
    temporary_data = {
        'total_reproduction': 0,
        'fish_reproduction': 0,
        'shark_reproduction': 0,
        'fishes_eaten': [],
        'dead_fishes_age': 0,
        'sharks_starved': [],
        'dead_sharks_age': 0
    }

    @classmethod
    def reset_data(cls):
        cls.simulation_chronon_data = []
        cls.simulation_data = None
        cls.temporary_data = {
            'total_reproduction': 0,
            'fish_reproduction': 0,
            'shark_reproduction': 0,
            'fishes_eaten': [],
            'dead_fishes_age': 0,
            'sharks_starved': [],
            'dead_sharks_age': 0
        }

    @classmethod
    def chronon_data_handling(cls, simulation_chronon: int, simulation_chronon_data: dict):
        """
        calculer les enfant nés
        stocker les poissons morts
        stocker le nb d'individus
        stocker l'age des morts


        initial_data = {
            'entities': cls.planet.entities,
            'fishes_eaten': cls.planet.count_eaten_fish,
            'nb_shark_starved': cls.planet.nb_shark_starved,
            'nb_fish': cls.planet.count_fish, 'nb_shark': cls.planet.count_shark,
            'nb_reproduction_shark': cls.planet.count_reproduced_shark,
            'nb_reproduction_fish': cls.planet.count_reproduced_fish,
            'dead_fishes_age': cls.planet.dead_fishes_age,
            'dead_sharks_age': cls.planet.dead_sharks_age
        }
        """

        dead_fishes = len(simulation_chronon_data['dead_fishes'])
        dead_sharks = len(simulation_chronon_data['dead_sharks'])
        dead_animals = dead_fishes + dead_sharks

        chronon_data = {
            'chronon': simulation_chronon,
            'animal_count': simulation_chronon_data['nb_fish'] + simulation_chronon_data['nb_shark'],
            'fish_count': simulation_chronon_data['nb_fish'],
            'shark_count': simulation_chronon_data['nb_shark'],
            'fish_reproduction': simulation_chronon_data['nb_reproduction_fish'],
            'shark_reproduction': simulation_chronon_data['nb_reproduction_shark'],
            'total_reproduction': simulation_chronon_data['nb_reproduction_fish'] + simulation_chronon_data['nb_reproduction_shark'],
            'fishes_eaten': dead_fishes,
            'sharks_starved':  dead_sharks,
            'total_deaths': dead_animals
        }

        cls.temporary_data['total_reproduction'] += simulation_chronon_data['nb_reproduction_fish'] + simulation_chronon_data['nb_reproduction_shark']
        cls.temporary_data['fish_reproduction'] += simulation_chronon_data['nb_reproduction_fish']
        cls.temporary_data['shark_reproduction'] += simulation_chronon_data['nb_reproduction_shark']
        for dead_fish in simulation_chronon_data['dead_fishes']:
            cls.temporary_data['fishes_eaten'].append(dead_fish)
        for dead_shark in simulation_chronon_data['dead_sharks']:
            cls.temporary_data['sharks_starved'].append(dead_shark)

        # for entity in simulation_chronon_data['entities']:
        #     if isinstance(entity, Shark):
        #         if entity.fishes_eaten > cls.temporary_data['top_eater']:
        #             cls.temporary_data['top_eater'] = entity.fishes_eaten

        cls.simulation_chronon_data.append(chronon_data)

    @classmethod
    def final_data_handling(cls, simulation_chronon_data):
        """
        initial_data = {
            'entities': cls.planet.entities,
            'fishes_eaten': cls.planet.count_eaten_fish,
            'nb_shark_starved': cls.planet.nb_shark_starved,
            'nb_fish': cls.planet.count_fish, 'nb_shark': cls.planet.count_shark,
            'nb_reproduction_shark': cls.planet.count_reproduced_shark,
            'nb_reproduction_fish': cls.planet.count_reproduced_fish,
            'dead_fishes_age': cls.planet.dead_fishes_age,
            'dead_sharks_age': cls.planet.dead_sharks_age
        }
        """
        simulation_id = PersistenceHandler.get_next_simulation_id()
        life_expectancies = cls.calculate_life_expectancy()

        data = {
            "simulation_id": simulation_id,
            "date": datetime.now(),
            "duration": simulation_parameters['simulation_duration'],
            "grid_height": simulation_parameters['grid_height'],
            "grid_width": simulation_parameters['grid_width'],
            "fish_starting_population": simulation_parameters['fish_starting_population'],
            "shark_starting_population": simulation_parameters['shark_starting_population'],
            "fish_reproduction_time": simulation_parameters['fish_reproduction_time'],
            "shark_reproduction_time": simulation_parameters['shark_reproduction_time'],
            "shark_starvation_time": simulation_parameters['shark_starvation_time'],
            "shark_energy_gain": simulation_parameters['shark_energy_gain'],
            "shuffle_entities": simulation_parameters['shuffle_entities'],
            'animal_count': simulation_chronon_data['nb_fish'] + simulation_chronon_data['nb_shark'],
            'fish_count': simulation_chronon_data['nb_fish'],
            'shark_count': simulation_chronon_data['nb_shark'],
            "life_expectancy": life_expectancies['global_life_expectancy'],
            "fish_life_expectancy": life_expectancies['fish_life_expectancy'],
            "shark_life_expectancy": life_expectancies['shark_life_expectancy'],
            "total_reproduction": cls.temporary_data['total_reproduction'],
            "fish_reproduction": cls.temporary_data['fish_reproduction'],
            "shark_reproduction": cls.temporary_data['shark_reproduction'],
            "dead_animals": cls.temporary_data['fishes_eaten'] + cls.temporary_data['sharks_starved'],
            "fishes_eaten": len(cls.temporary_data['fishes_eaten']),
            "sharks_starved": len(cls.temporary_data['sharks_starved']),
            "total_deaths": len(cls.temporary_data['fishes_eaten']) + len(cls.temporary_data['sharks_starved']),
            "detail": [],
            "entities": []
        }

        for chronon_data in cls.simulation_chronon_data:
            data['detail'].append(chronon_data)

        data['entities'] = cls.handle_entities(simulation_chronon_data['entities'])

        PersistenceHandler.save_data(data)

    @classmethod
    def calculate_life_expectancy(cls):

        fishes_age = 0
        fishes_divider = 0
        sharks_age = 0
        sharks_divider = 0

        if cls.temporary_data['fishes_eaten']:
            for fish in cls.temporary_data['fishes_eaten']:
                fishes_age += fish.age
                fishes_divider += 1
            fishes_life_expectancy = fishes_age / fishes_divider
        else:
            fishes_life_expectancy = 0

        if cls.temporary_data['sharks_starved']:
            for shark in cls.temporary_data['sharks_starved']:
                sharks_age += shark.age
                sharks_divider += 1
            sharks_life_expectancy = sharks_age / sharks_divider
        else:
            sharks_life_expectancy = 0

        if cls.temporary_data['fishes_eaten'] or cls.temporary_data['sharks_starved']:
            global_life_expectancy = (fishes_age + sharks_age) / (fishes_divider + sharks_divider)
        else:
            global_life_expectancy = 0

        print("sharks_age",sharks_age)
        print("fishes_age",fishes_age)

        return {
            'fish_life_expectancy': round(fishes_life_expectancy, 2),
            'shark_life_expectancy': round(sharks_life_expectancy, 2),
            'global_life_expectancy': round(global_life_expectancy, 2)
        }

    @classmethod
    def handle_entities(cls, living_entities):

        entities_data = []
        i = 0
        for entity in living_entities:
            entities_data.append(cls.handle_entity(entity, True, i))
            i += 1
        for entity in cls.temporary_data['fishes_eaten']:
            entities_data.append(cls.handle_entity(entity, False, i))
            i += 1
        for entity in cls.temporary_data['sharks_starved']:
            entities_data.append(cls.handle_entity(entity, False, i))
            i += 1

        return entities_data

    @classmethod
    def handle_entity(cls, entity, is_alive, id):
        if isinstance(entity, Fish):
            species = "Fish"
            fishes_eaten = 0
        else:
            species = "Shark"
            fishes_eaten = entity.fishes_eaten

        return{
            'entity_id': id,
            'is_alive': is_alive,
            'age': entity.age,
            'species': species,
            'children': entity.children_number,
            'fishes_eaten': fishes_eaten
        }