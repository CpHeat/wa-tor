import copy

from settings import simulation_parameters
from classes.fish import Fish
from classes.shark import Shark
import random


class Planet:
    def __init__(self):
        '''Initialize empty grid
        '''
        self.height = simulation_parameters.get('grid_height')
        self.width = simulation_parameters.get('grid_width')
        self.count_fish = simulation_parameters.get('fish_starting_population')
        self.count_shark = simulation_parameters.get('shark_starting_population')

        self.count_reproduced_fish = self.count_reproduced_shark = 0
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.follow_fish = simulation_parameters.get('follow_entities')
        self.follow_shark = simulation_parameters.get('follow_entities')
        self.shuffle = simulation_parameters.get('shuffle_entities')
        self.dead_fishes = []
        self.dead_sharks = []

        self.entities = []
        self.next_entities = []
        self.populate()

    def populate(self):
        '''Populate randomly the grid with fishes and sharks
        '''
        random_indices = random.sample(range(self.height * self.width), self.count_fish + self.count_shark)

        random_indices_shark = random.sample(random_indices, self.count_shark)

        for index, i in enumerate(random_indices_shark):
            y = i // self.width  # y
            x = i % self.width  # x
            new_shark = Shark(x, y)
            if self.follow_shark:
                new_shark.followed = True
                self.follow_shark = False
            self.grid[y][x] = new_shark
            self.entities.append(new_shark)

        random_indices_fish = list(set(random_indices) - set(random_indices_shark))

        for index, i in enumerate(random_indices_fish):
            y = i // self.width  # y
            x = i % self.width  # x
            new_fish = Fish(x, y)
            if self.follow_fish:
                new_fish.followed = True
                self.follow_fish = False
            self.grid[y][x] = new_fish
            self.entities.append(new_fish)
        if self.shuffle:
            random.shuffle(self.entities)

    def get_grid(self):
        return self.grid

    def check_entities(self):
        self.next_entities = []

        # Reset to zero on each call — statistics for each round
        self.count_reproduced_fish = self.count_reproduced_shark = 0
        self.dead_fishes = []
        self.dead_sharks = []

        for entity in self.entities:
            # If entity didn't die this turn
            if not entity is None:
                possibilities_from_neighbors = self.get_neighbors(entity.x, entity.y)
                choice = entity.move(possibilities_from_neighbors)

                # If list is empty it means it is a dead shark
                if len(choice) == 0:
                    self.starved_shark(entity)
                else:
                    self.move_prepare(entity, choice)

        self.entities = self.checked_entities

        if self.shuffle:
            random.shuffle(self.entities)

        return {'grid': self.grid, 'entities': self.entities, 'dead_fishes': self.dead_fishes, 'dead_sharks': self.dead_sharks,
                'nb_fish': self.count_fish, 'nb_shark': self.count_shark,
                'nb_reproduction_shark': self.count_reproduced_shark,
                'nb_reproduction_fish': self.count_reproduced_fish}

    def move_prepare(self, entity, choice):

        target_x = choice[0].get('x')
        target_y = choice[0].get('y')
        previous_x = copy.deepcopy(entity.x)
        previous_y = copy.deepcopy(entity.y)

        # check if eat
        if isinstance(entity, Shark):
            # eat first
            if isinstance(self.grid[target_y][target_x], Fish):
                self.shark_eats(entity, target_x, target_y)

        if int(target_x) != int(previous_x) or int(target_y) != int(previous_y):
            self.move_entity(entity, target_x, target_y)

        if len(choice) == 2 and (target_x != previous_x or target_y != previous_y):
            self.reproduce_entity(entity, previous_x, previous_y)

    def reproduce_entity(self, entity, x, y):
        if isinstance(entity, Fish):
            baby = Fish(x, y)
            self.count_reproduced_fish += 1
            self.count_fish += 1
        else:
            baby = Shark(x, y)
            self.count_reproduced_shark += 1
            self.count_shark += 1

        self.grid[y][x] = baby
        self.next_entities.append(baby)

    def shark_eats(self, entity, x, y):
        entity.eat()
        self.count_fish -= 1
        self.dead_fishes.append(copy.deepcopy(self.grid[y][x]))
        self.destroy_entity(self.grid[y][x], x, y)

    def get_neighbors(self, x, y):
        neighbors = []

        # North (up)
        new_y = y - 1 if y != 0 else self.height - 1
        neighbors.append(self.grid[new_y][x])

        # South (down)
        new_y = y + 1 if y != self.height - 1 else 0
        neighbors.append(self.grid[new_y][x])

        # East (right)
        new_x = x + 1 if x != self.width - 1 else 0
        neighbors.append(self.grid[y][new_x])

        # West (left)
        new_x = x - 1 if x != 0 else self.width - 1
        neighbors.append(self.grid[y][new_x])

        return neighbors

    def move_entity(self, entity, x, y):

        self.grid[y][x] = entity
        self.grid[entity.y][entity.x] = None
        entity.x = x
        entity.y = y
        self.next_entities.append(entity)

    def starved_shark(self, entity):
        self.count_shark -= 1
        self.dead_sharks.append(copy.deepcopy(entity))
        self.destroy_entity(entity, entity.x, entity.y)

    def destroy_entity(self, entity, x, y):
        if entity in self.entities:
            index = self.entities.index(entity)
            self.entities[index] = None
            if entity in self.next_entities:
                self.next_entities.remove(entity)
        else:
            self.next_entities.remove(entity)
        self.grid[y][x] = None