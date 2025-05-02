from settings import simulation_parameters
from classes.fish import Fish
from classes.shark import Shark
import random

'''
class Fish:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Shark:
    def __init__(self,x,y):
        self.x = x
        self.y = y
'''


class Planet:
    def __init__(self, follow_entities):
        '''Initialize empty grid
        '''
        self.height = simulation_parameters.get('grid_height')
        self.width = simulation_parameters.get('grid_width')
        self.num_fish = self.count_fish = simulation_parameters.get('fish_reproduction_time')
        self.num_shark = self.count_shark = simulation_parameters.get('shark_starting_population')
        self.count_eaten_fish = self.count_shark_eats = 0
        self.count_reproduced_fish = self.count_reproduced_shark = 0
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.follow_fish = follow_entities
        self.follow_shark = follow_entities
        self.dead_fishes_age = 0
        self.dead_sharks_age = 0

        self.entities = []
        self.populate()

    def populate(self):
        '''Populate randomly the grid with fishes and sharks
        '''
        random_indices = random.sample(range(self.height * self.width), self.num_fish + self.num_shark)

        random_indices_shark = random.sample(random_indices, self.num_shark)

        for i in random_indices_shark:
            y = i // self.width  # y
            x = i % self.width  # x
            new_shark = Shark(x, y)
            if self.follow_shark:
                new_shark.followed = True
                self.follow_shark = False
            self.grid[y][x] = new_shark
            self.entities.append(new_shark)

        random_indices_fish = list(set(random_indices) - set(random_indices_shark))

        for i in random_indices_fish:
            y = i // self.width  # y
            x = i % self.width  # x
            new_fish = Fish(x, y)
            if self.follow_shark:
                new_fish.followed = True
                self.follow_fish = False
            self.grid[y][x] = new_fish
            self.entities.append(new_fish)

    def get_grid(self):
        return self.grid

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
        target_x = target_pos_dict.get('x')
        target_y = target_pos_dict.get('y')
        print("entity to move", entity)
        print("entity x", entity.x, "entity y", entity.y)
        print("target_pos_dict:", target_pos_dict)
        old_x = entity.x
        old_y = entity.y
        entity.x = target_x
        entity.y = target_y
        print("old cell before", self.grid[old_y][old_x])
        print("moveeeeeeeeeeeee before")
        print(self.grid)
        self.grid[target_y][target_x] = entity
        self.grid[old_y][old_x] = None
        print("old cell after", self.grid[old_y][old_x])
        print("moveeeeeeeeeeeee after")
        print(self.grid)
        self.entities.append(entity)

    
    # to test    
    def move_eat_entity(self, target_pos_dict, entity):
        target_x = target_pos_dict.get('x')
        target_y = target_pos_dict.get('y')
        if isinstance(entity,Shark): # case shark
            # eat first
            if isinstance(self.grid[target_y][target_x],Fish):
                entity.eat()
                self.count_shark_eats +=1
                self.count_eaten_fish +=1
            # then move
            self.move_entity(target_pos_dict,entity)
            
        elif (isinstance(entity, Fish)): #case fish        
            # to move fish
            self.move_entity(target_pos_dict,entity)
        
        
        
    def reproduce_fish(self,old_pos_dict):
        old_x = old_pos_dict.get('x')
        old_y = old_pos_dict.get('y')
        print("grid for rep fish")
        baby_fish = Fish(old_x, old_y)
        self.grid[old_y][old_x] = baby_fish
        print("after grid for rep fish")
        self.entities.append(baby_fish)
        self.count_reproduced_fish += 1
        self.count_fish += 1

    def reproduce_shark(self, old_pos_dict):
        old_x = old_pos_dict.get('x')
        old_y = old_pos_dict.get('y')
        baby_shark = Shark(old_x, old_y)
        self.grid[old_y][old_x] = baby_shark
        self.entities.append(baby_shark)
        self.count_reproduced_shark += 1
        self.count_shark += 1

    def move_and_reproduce_entity(self, target_pos_dict, old_pos_dict, entity):
        target_x = target_pos_dict.get('x')
        target_y = target_pos_dict.get('y')

        if isinstance(entity, Shark):  # case shark
            # to move shark
            # check target cell
            if isinstance(self.grid[target_y][target_x], Fish) and (not (isinstance(entity, Shark))):
                # to move & eat
                print(f" move_eat_entity({target_pos_dict},{entity}) ")
                self.move_eat_entity(target_pos_dict, entity)

            elif self.grid[target_y][target_x] is None:
                # move
                self.move_entity(target_pos_dict, entity)
            else:
                pass

            # to reproduce shark
            self.reproduce_shark(old_pos_dict)


        elif (isinstance(entity, Fish)) and (not (isinstance(entity, Shark))):  # case fish

            # to move fish
            self.move_entity(target_pos_dict, entity)
            # to reproduce fish
            self.reproduce_fish(old_pos_dict)

    def check_entities(self):
        entity_copy = self.entities.copy()
        self.entities = []

        # Reset to zero on each call — statistics for each round
        self.count_eaten_fish = self.count_shark_eats = 0
        self.count_fish = self.count_shark = 0
        self.count_reproduced_fish = self.count_reproduced_shark = 0 
        self.dead_fishes_age = 0
        self.dead_sharks_age = 0
        for entity in entity_copy :
            print(f"check this entity.x: {entity.x}, entity.y: {entity.y}" )
            possibilities_from_neighbors = self.get_neighbors(entity.x,entity.y)
            coordinates_possibilities_from_neighbors = self.get_neighbors_coordinates(entity.x,entity.y)
            
                


            print("possibilities_from_neighbors:", possibilities_from_neighbors)
            print("coordinates_possibilities_from_neighbors:", coordinates_possibilities_from_neighbors)
            print("before calling move entity x", entity.x, "entity y", entity.y)
            ################# case move no rep
            # selected_x,selected_y = random.choice(coordinates_possibilities_from_neighbors)
            # choice = [{'x': selected_x, 'y': selected_y}]
            # selected_x,selected_y = random.choice(coordinates_possibilities_from_neighbors)
            # choice = [{'x': selected_x, 'y': selected_y}]
            ################# case move & rep
            # selected_x,selected_y = random.choice(coordinates_possibilities_from_neighbors)
            # choice = [{'x': selected_x, 'y': selected_y},{'x': entity.x, 'y': entity.y}]
            choice = entity.move(possibilities_from_neighbors)

            print("after calling move entity x", entity.x, "entity y", entity.y)
            print("choice:", choice)
            len_choice = len(choice)
            match len_choice:
                case 2 | 1:  # check if move and reproduce entity is possible

                    target_x = choice[0].get('x')
                    target_y = choice[0].get('y')

                    if (target_x,target_y) in coordinates_possibilities_from_neighbors:
                        print(f"ok to move & rep | to move no rep entity at row: {entity.y} col: {entity.x} to target row:{target_y} col:{target_x}")
                        if len_choice == 2: # move and reproduce entity
                            self.move_and_reproduce_entity(choice[0],choice[1],entity)
                        elif len_choice == 1: # move (only) entity, eat (for shark)
                            self.move_eat_entity(choice, entity)
                            
                            

                    else:
                        print("invalid choices")
                case _:  # nothing to do
                    print("no move")
                    if isinstance(entity, Fish):
                        self.dead_fishes_age += entity.age
                    elif isinstance(entity, Shark):
                        self.dead_sharks_age += entity.age

        return {'grid': self.grid, 'entities': self.entities, 'fishes_eaten': self.count_eaten_fish,
                'nb_fish': self.count_fish, 'nb_shark': self.count_shark,
                'nb_reproduction_shark': self.count_reproduced_shark,
                'nb_reproduction_fish': self.count_reproduced_fish, 'dead_fishes_age': self.dead_fishes_age,
                'dead_sharks_age': self.dead_sharks_age}