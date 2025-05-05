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
        self.num_fish = self.count_fish = simulation_parameters.get('fish_starting_population')
        self.num_shark = self.count_shark = simulation_parameters.get('shark_starting_population')
        self.count_eaten_fish = self.count_shark_eats = 0

        self.count_reproduced_fish = self.count_reproduced_shark = 0
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.follow_fish = simulation_parameters.get('follow_entities')
        self.follow_shark = simulation_parameters.get('follow_entities')
        self.shuffle = simulation_parameters.get('shuffle_entities')
        self.dead_fishes_age = 0
        self.dead_sharks_age = 0
        self.nb_shark_starved = 0

        self.entities = []
        self.next_entities = []
        self.populate()

        self.check_counter = 0

    def populate(self):
        '''Populate randomly the grid with fishes and sharks
        '''
        random_indices = random.sample(range(self.height * self.width), self.num_fish + self.num_shark)

        random_indices_shark = random.sample(random_indices, self.num_shark)

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
        print("self.entities", self.entities)
        print(f"start grid: {self.grid}")
        self.next_entities = []
        self.check_counter += 1

        # Reset to zero on each call — statistics for each round
        self.count_eaten_fish = self.count_shark_eats = 0
        self.count_reproduced_fish = self.count_reproduced_shark = 0
        self.dead_fishes_age = 0
        self.dead_sharks_age = 0

        for entity in self.entities:
            if not entity is None:
                possibilities_from_neighbors = self.get_neighbors(entity.x, entity.y)
                choice = entity.move(possibilities_from_neighbors)

                if len(choice) == 0:
                    print(f"dead {entity}")
                    self.dead_shark(entity)
                else:
                    print(f"init move {entity}")
                    self.move(entity, choice)
        
        self.entities = self.next_entities

        if self.shuffle:
            random.shuffle(self.entities)
        
        return {'grid': self.grid, 'entities': self.entities, 'fishes_eaten': self.count_eaten_fish,
                'nb_fish': self.count_fish, 'nb_shark': self.count_shark, 'nb_shark_starved' : self.nb_shark_starved,
                'nb_reproduction_shark': self.count_reproduced_shark,
                'nb_reproduction_fish': self.count_reproduced_fish, 'dead_fishes_age': self.dead_fishes_age,
                'dead_sharks_age': self.dead_sharks_age}

    def move(self, entity, choice):

        target_x = choice[0].get('x')
        target_y = choice[0].get('y')
        previous_x = entity.x
        previous_y = entity.y

        # check si on mange
        if isinstance(entity, Shark):
            # eat first
            if isinstance(self.grid[target_y][target_x], Fish):
                print(f"eat {entity}")
                self.shark_eats(entity, target_x, target_y)

        print(f"move {entity}")
        self.move_entity(entity, target_x, target_y)

        if len(choice) == 2:

            print(f"reproduce {entity}")
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
        self.destroy_entity(self.grid[y][x], x, y)
        self.count_shark_eats += 1
        self.count_eaten_fish += 1

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

    def dead_shark(self, entity):
        self.dead_sharks_age += entity.age
        self.nb_shark_starved += 1
        self.count_shark -= 1

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
    #
    # # to test
    # def move_eat_entity(self, target_pos_dict, entity):
    #
    #     target_x = target_pos_dict.get('x')
    #     target_y = target_pos_dict.get('y')
    #     if isinstance(entity, Shark):
    #         # eat first
    #         if isinstance(self.grid[target_y][target_x], Fish):
    #             entity.eat()
    #             victim = self.grid[target_y][target_x]
    #             if victim in self.entities:
    #                 self.entities.remove(victim)
    #                 if victim in self.next_entities:
    #                     self.next_entities.remove(victim)
    #             else:
    #                 self.next_entities.remove(victim)
    #             self.grid[target_y][target_x] = None
    #
    #             self.count_shark_eats += 1
    #             self.count_eaten_fish += 1
    #         # else:
    #             # entity.lost_life()
    #         # then move
    #         self.move_entity(target_pos_dict, entity)
    #
    #     elif isinstance(entity, Fish):
    #         # to move fish
    #         self.move_entity(target_pos_dict, entity)
    #
    # def reproduce_fish(self, old_pos_dict):
    #     old_x = old_pos_dict.get('x')
    #     old_y = old_pos_dict.get('y')
    #     baby_fish = Fish(old_x, old_y)
    #     self.grid[old_y][old_x] = baby_fish
    #     self.next_entities.append(baby_fish)
    #     self.count_reproduced_fish += 1
    #     self.count_fish += 1
    #
    # def reproduce_shark(self, old_pos_dict):
    #     old_x = old_pos_dict.get('x')
    #     old_y = old_pos_dict.get('y')
    #     baby_shark = Shark(old_x, old_y)
    #     self.grid[old_y][old_x] = baby_shark
    #     self.next_entities.append(baby_shark)
    #     self.count_reproduced_shark += 1
    #     self.count_shark += 1

    # def move_and_reproduce_entity(self, target_pos_dict, old_pos_dict, entity):
    #
    #     target_x = target_pos_dict.get('x')
    #     target_y = target_pos_dict.get('y')
    #
    #     if isinstance(entity, Shark):  # case shark
    #         # to move shark
    #         # check target cell
    #         if isinstance(self.grid[target_y][target_x], Fish):
    #             # to move & eat
    #             self.move_eat_entity(target_pos_dict, entity)
    #         elif self.grid[target_y][target_x] is None:
    #             # move
    #             self.move_entity(target_pos_dict, entity)
    #
    #         # to reproduce shark
    #         self.reproduce_shark(old_pos_dict)
    #
    #
    #     elif isinstance(entity, Fish):  # case fish
    #
    #         # to move fish
    #         self.move_entity(target_pos_dict, entity)
    #         # to reproduce fish
    #         self.reproduce_fish(old_pos_dict)
