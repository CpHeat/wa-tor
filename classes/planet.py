class Planet:
    '''
    A class representing a simulation of a planet grid populated with fish and sharks.
    
    The planet grid simulates a basic ecosystem where entities (fish and sharks) move, reproduce, and interact (such as sharks eating fish). The simulation is based on a set of parameters for grid size, initial populations, and other behaviors (such as entity following and shuffling of entities).

    Attributes:
        height (int): The number of rows in the grid.
        width (int): The number of columns in the grid.
        count_fish (int): The initial population of fish.
        count_shark (int): The initial population of sharks.
        count_reproduced_fish (int): The count of fish that have reproduced.
        count_reproduced_shark (int): The count of sharks that have reproduced.
        grid (list of lists): The grid where each cell holds an entity or None if empty.
        follow_fish (bool): Flag to indicate if the fish should be followed in the simulation.
        follow_shark (bool): Flag to indicate if the sharks should be followed in the simulation.
        shuffle (bool): Flag to determine if the entities should be shuffled randomly.
        dead_fishes (list): A list of dead fish entities.
        dead_sharks (list): A list of dead shark entities.
        entities (list): A list of all active entities (fish and sharks).
        next_entities (list): A list of entities after one simulation step.
    
    Methods:
        populate(): Populates the grid with randomly placed fish and sharks.
        get_grid(): Returns the current grid.
        check_entities(): Executes one step of the simulation, moving entities, handling reproduction, and managing deaths.
        move_prepare(entity, choice): Prepares the entity for movement, including eating (for sharks) and reproduction.
        reproduce_entity(entity, x, y): Reproduces an entity (either fish or shark) at the specified location.
        shark_eats(entity, x, y): Simulates a shark eating a fish.
        get_neighbors(x, y): Returns the neighboring entities around a given (x, y) position.
        move_entity(entity, x, y): Moves an entity to a new position on the grid.
        starved_shark(entity): Handles the event of a shark starving and being removed from the grid.
        destroy_entity(entity, x, y): Destroys an entity, removing it from both the grid and the entities list.
    '''
    
    def __init__(self):
        '''Initializes an empty grid for the simulation with a specified size and initial populations.'''
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
        '''Populates the grid with fish and sharks at random positions based on the starting populations.'''
        random_indices = random.sample(range(self.height * self.width), self.count_fish + self.count_shark))

        random_indices_shark = random.sample(random_indices, self.count_shark))

        for index, i in enumerate(random_indices_shark):
            y = i // self.width  # y-coordinate
            x = i % self.width  # x-coordinate
            new_shark = Shark(x, y)
            if self.follow_shark:
                new_shark.followed = True
                self.follow_shark = False
            self.grid[y][x] = new_shark
            self.entities.append(new_shark)

        random_indices_fish = list(set(random_indices) - set(random_indices_shark))

        for index, i in enumerate(random_indices_fish):
            y = i // self.width  # y-coordinate
            x = i % self.width  # x-coordinate
            new_fish = Fish(x, y)
            if self.follow_fish:
                new_fish.followed = True
                self.follow_fish = False
            self.grid[y][x] = new_fish
            self.entities.append(new_fish)

        if self.shuffle:
            random.shuffle(self.entities)

    def get_grid(self):
        '''Returns the current state of the grid.'''
        return self.grid

    def check_entities(self):
        '''Performs one simulation step, moving entities, checking reproduction, and managing deaths.'''
        self.next_entities = []
        self.count_reproduced_fish = self.count_reproduced_shark = 0
        self.dead_fishes = []
        self.dead_sharks = []

        for entity in self.entities:
            if entity is not None:
                possibilities_from_neighbors = self.get_neighbors(entity.x, entity.y)
                choice = entity.move(possibilities_from_neighbors)

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
        '''Prepares the entity for movement, handling eating (for sharks) and reproduction.'''
        target_x = choice[0].get('x')
        target_y = choice[0].get('y')
        previous_x = copy.deepcopy(entity.x)
        previous_y = copy.deepcopy(entity.y)

        if isinstance(entity, Shark):
            if isinstance(self.grid[target_y][target_x], Fish):
                self.shark_eats(entity, target_x, target_y)

        if target_x != previous_x or target_y != previous_y:
            self.move_entity(entity, target_x, target_y)

        if len(choice) == 2 and (target_x != previous_x or target_y != previous_y):
            self.reproduce_entity(entity, previous_x, previous_y)

    def reproduce_entity(self, entity, x, y):
        '''Reproduces an entity (either a fish or shark) at the specified position.'''
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
        '''Simulates a shark eating a fish, removing the fish from the grid and updating the count.'''
        entity.eat()
        self.count_fish -= 1
        self.dead_fishes.append(copy.deepcopy(self.grid[y][x]))
        self.destroy_entity(self.grid[y][x], x, y)

    def get_neighbors(self, x, y):
        '''Returns the neighboring entities around the given (x, y) position.'''
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
        '''Moves an entity to a new position on the grid.'''
        self.grid[y][x] = entity
        self.grid[entity.y][entity.x] = None
        entity.x = x
        entity.y = y
        self.next_entities.append(entity)

    def starved_shark(self, entity):
        '''Handles the event when a shark starves (due to no food), removing it from the grid.'''
        self.count_shark -= 1
        self.dead_sharks.append(copy.deepcopy(entity))
        self.destroy_entity(entity, entity.x, entity.y)

    def destroy_entity(self, entity, x, y):
        '''Removes an entity from the grid and the entities list.'''
        if entity in self.entities:
            index = self.entities.index(entity)
