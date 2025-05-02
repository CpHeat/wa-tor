from settings import simulation_parameters
from classes.fish import Fish
from classes.shark import Shark
import random


class Planet:
    def __init__(self, follow_entities):
        '''Initialize empty grid
        '''
        self.height = simulation_parameters.get('grid_height')
        self.width = simulation_parameters.get('grid_width')
        self.num_fish = self.count_fish = simulation_parameters.get('fish_starting_population')
        self.num_shark = self.count_shark = simulation_parameters.get('shark_starting_population')
        self.count_eaten_fish = self.count_shark_eats = 0

        self.count_reproduced_fish = self.count_reproduced_shark = 0
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.follow_fish = follow_entities
        self.follow_shark = follow_entities
        self.dead_fishes_age = 0
        self.dead_sharks_age = 0

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

    def get_grid(self):
        return self.grid

    def check_entities(self):
        print("self.entities", self.check_counter)
        self.next_entities = []
        self.check_counter += 1

        # Reset to zero on each call — statistics for each round
        self.count_eaten_fish = self.count_shark_eats = 0
        self.count_reproduced_fish = self.count_reproduced_shark = 0
        self.dead_fishes_age = 0
        self.dead_sharks_age = 0
        for entity in self.entities:
            possibilities_from_neighbors = self.get_neighbors(entity.x, entity.y)
            coordinates_possibilities_from_neighbors = self.get_neighbors_coordinates(entity.x, entity.y)

            ################# case move no rep
            # selected_x,selected_y = random.choice(coordinates_possibilities_from_neighbors)
            # choice = [{'x': selected_x, 'y': selected_y}]
            # selected_x,selected_y = random.choice(coordinates_possibilities_from_neighbors)
            # choice = [{'x': selected_x, 'y': selected_y}]
            ################# case move & rep
            # selected_x,selected_y = random.choice(coordinates_possibilities_from_neighbors)
            # choice = [{'x': selected_x, 'y': selected_y},{'x': entity.x, 'y': entity.y}]
            choice = entity.move(possibilities_from_neighbors)

            len_choice = len(choice)
            match len_choice:
                case 2 | 1:  # check if move and reproduce entity is possible

                    target_x = choice[0].get('x')
                    target_y = choice[0].get('y')

                    if (target_x, target_y) in coordinates_possibilities_from_neighbors:
                        if len_choice == 2:  # move and reproduce entity
                            self.move_and_reproduce_entity(choice[0], choice[1], entity)
                        elif len_choice == 1:  # move (only) entity, eat (for shark)
                            self.move_eat_entity(choice[0], entity)
                case _:  # nothing to do
                    self.grid[entity.y][entity.x] = None
                    if isinstance(entity, Fish):
                        self.dead_fishes_age += entity.age
                        if entity in self.entities:
                            self.entities.remove(entity)
                            if entity in self.next_entities:
                                self.next_entities.remove(entity)
                        else:
                            self.next_entities.remove(entity)
                    else:  # dead shark
                        self.dead_sharks_age += entity.age
                        if entity in self.entities:
                            self.entities.remove(entity)
                            if entity in self.next_entities:
                                self.next_entities.remove(entity)
                        else:
                            self.next_entities.remove(entity)
                        self.count_shark -= 1

        # self.validate_entities()
        self.entities = self.next_entities
        return {'grid': self.grid, 'entities': self.entities, 'fishes_eaten': self.count_eaten_fish,
                'nb_fish': self.count_fish, 'nb_shark': self.count_shark,
                'nb_reproduction_shark': self.count_reproduced_shark,
                'nb_reproduction_fish': self.count_reproduced_fish, 'dead_fishes_age': self.dead_fishes_age,
                'dead_sharks_age': self.dead_sharks_age}

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

    def get_neighbors_coordinates(self, x, y):
        neighbors_coordinates = []

        # North (y - 1, wrap using height because rows wrap vertically)
        new_y = y - 1 if y != 0 else self.height - 1
        neighbors_coordinates.append((x, new_y))  # N

        # South (y + 1, wrap using height)
        new_y = y + 1 if y != self.height - 1 else 0
        neighbors_coordinates.append((x, new_y))  # S

        # East (x + 1, wrap using width because columns wrap horizontally)
        new_x = x + 1 if x != self.width - 1 else 0
        neighbors_coordinates.append((new_x, y))  # E

        # West (x - 1, wrap using width)
        new_x = x - 1 if x != 0 else self.width - 1
        neighbors_coordinates.append((new_x, y))  # W

        return neighbors_coordinates

    def move_entity(self, target_pos_dict, entity):
        print("current position", entity.x, entity.y)
        print("target position", target_pos_dict)
        target_x = target_pos_dict.get('x')
        target_y = target_pos_dict.get('y')
        old_x = entity.x
        old_y = entity.y
        entity.x = target_x
        entity.y = target_y
        self.grid[target_y][target_x] = entity
        self.grid[old_y][old_x] = None
        self.next_entities.append(entity)

    # to test
    def move_eat_entity(self, target_pos_dict, entity):
        print("move eat")
        target_x = target_pos_dict.get('x')
        target_y = target_pos_dict.get('y')
        if isinstance(entity, Shark):
            # eat first
            if isinstance(self.grid[target_y][target_x], Fish):
                entity.eat()
                victim = self.grid[target_y][target_x]
                if victim in self.entities:
                    self.entities.remove(victim)
                    if victim in self.next_entities:
                        self.next_entities.remove(victim)
                else:
                    self.next_entities.remove(victim)
                self.grid[target_y][target_x] = None

                self.count_shark_eats += 1
                self.count_eaten_fish += 1
            # then move
            self.move_entity(target_pos_dict, entity)

        elif isinstance(entity, Fish):
            # to move fish
            self.move_entity(target_pos_dict, entity)

    def reproduce_fish(self, old_pos_dict):
        old_x = old_pos_dict.get('x')
        old_y = old_pos_dict.get('y')
        baby_fish = Fish(old_x, old_y)
        self.grid[old_y][old_x] = baby_fish
        self.next_entities.append(baby_fish)
        self.count_reproduced_fish += 1
        self.count_fish += 1

    def reproduce_shark(self, old_pos_dict):
        old_x = old_pos_dict.get('x')
        old_y = old_pos_dict.get('y')
        baby_shark = Shark(old_x, old_y)
        self.grid[old_y][old_x] = baby_shark
        self.next_entities.append(baby_shark)
        self.count_reproduced_shark += 1
        self.count_shark += 1

    def move_and_reproduce_entity(self, target_pos_dict, old_pos_dict, entity):
        target_x = target_pos_dict.get('x')
        target_y = target_pos_dict.get('y')

        print("reproduce")
        if isinstance(entity, Shark):  # case shark
            # to move shark
            # check target cell
            if isinstance(self.grid[target_y][target_x], Fish):
                # to move & eat
                self.move_eat_entity(target_pos_dict, entity)
            elif self.grid[target_y][target_x] is None:
                # move
                self.move_entity(target_pos_dict, entity)

            # to reproduce shark
            self.reproduce_shark(old_pos_dict)


        elif isinstance(entity, Fish):  # case fish

            # to move fish
            self.move_entity(target_pos_dict, entity)
            # to reproduce fish
            self.reproduce_fish(old_pos_dict)