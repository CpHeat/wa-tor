import copy
import random
from typing import List, Optional, Dict, Any

from settings import simulation_parameters
from classes.fish import Fish
from classes.shark import Shark


class Planet:
    """
    Represents a simulated ecosystem grid containing fish and sharks.

    This class manages a 2D grid where fish and shark entities interact,
    move, reproduce, and die over time. The simulation updates in discrete
    steps, where each entity decides on its movement or action based on 
    neighboring cells.

    Key responsibilities:
    - Initialize the grid with random placement of fish and sharks.
    - Keep track of living and dead entities (fish and sharks).
    - Update entity states each simulation turn (movement, eating, reproduction).
    - Provide statistics on the ecosystem, such as population counts and 
      reproduction events.
    - Handle wrapping around grid edges, meaning the grid behaves like a torus.

    Attributes:
        height (int): Grid height.
        width (int): Grid width.
        count_fish (int): Current number of fish.
        count_shark (int): Current number of sharks.
        count_reproduced_fish (int): Number of fish reproduced this turn.
        count_reproduced_shark (int): Number of sharks reproduced this turn.
        grid (List[List[Optional[Any]]]): 2D grid of entities.
        follow_fish (bool): Whether to track a specific fish.
        follow_shark (bool): Whether to track a specific shark.
        shuffle (bool): Whether to shuffle entity update order each turn.
        dead_fishes (List[Fish]): List of fish that died this turn.
        dead_sharks (List[Shark]): List of sharks that died this turn.
        entities (List[Any]): Current list of all active entities.
        next_entities (List[Any]): List to hold entities for the next turn.
    """
    def __init__(self) -> None:
        """
        Initialize the Planet grid with specified width and height,
        and populate it with initial fish and shark populations.
        """
        self.height: int = simulation_parameters.get('grid_height')
        self.width: int = simulation_parameters.get('grid_width')
        self.count_fish: int = simulation_parameters.get('fish_starting_population')
        self.count_shark: int = simulation_parameters.get('shark_starting_population')

        self.count_reproduced_fish: int = 0
        self.count_reproduced_shark: int = 0
        self.grid: List[List[Optional[Any]]] = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.follow_fish: bool = simulation_parameters.get('follow_entities')
        self.follow_shark: bool = simulation_parameters.get('follow_entities')
        self.shuffle: bool = simulation_parameters.get('shuffle_entities')
        self.dead_fishes: List[Fish] = []
        self.dead_sharks: List[Shark] = []

        self.entities: List[Any] = []
        self.next_entities: List[Any] = []
        self.populate()

    def populate(self) -> None:
        """
        Randomly populate the grid with initial fish and sharks,
        marking one fish and one shark as followed if enabled.
        """
        random_indices = random.sample(range(self.height * self.width), self.count_fish + self.count_shark)
        random_indices_shark = random.sample(random_indices, self.count_shark)

        for i in random_indices_shark:
            y, x = divmod(i, self.width)
            new_shark = Shark(x, y)
            if self.follow_shark:
                new_shark.followed = True
                self.follow_shark = False
            self.grid[y][x] = new_shark
            self.entities.append(new_shark)

        random_indices_fish = list(set(random_indices) - set(random_indices_shark))

        for i in random_indices_fish:
            y, x = divmod(i, self.width)
            new_fish = Fish(x, y)
            if self.follow_fish:
                new_fish.followed = True
                self.follow_fish = False
            self.grid[y][x] = new_fish
            self.entities.append(new_fish)

        if self.shuffle:
            random.shuffle(self.entities)

    def get_grid(self) -> List[List[Optional[Any]]]:
        """
        Return the current grid state.

        Returns:
            A 2D list representing the grid.
        """
        return self.grid

    def check_entities(self) -> Dict[str, Any]:
        """
        Update all entities (fish and sharks) for one simulation step.

        Returns:
            A dictionary containing updated grid, entities, dead fishes, dead sharks,
            and various statistics.
        """
        self.next_entities = []
        self.count_reproduced_fish = 0
        self.count_reproduced_shark = 0
        self.dead_fishes = []
        self.dead_sharks = []

        for entity in self.entities:
            if entity is not None:
                neighbors = self.get_neighbors(entity.x, entity.y)
                choice = entity.move(neighbors)

                if not choice:
                    self.starved_shark(entity)
                else:
                    self.move_prepare(entity, choice)

        self.entities = self.next_entities

        if self.shuffle:
            random.shuffle(self.entities)

        return {
            'grid': self.grid,
            'entities': self.entities,
            'dead_fishes': self.dead_fishes,
            'dead_sharks': self.dead_sharks,
            'nb_fish': self.count_fish,
            'nb_shark': self.count_shark,
            'nb_reproduction_shark': self.count_reproduced_shark,
            'nb_reproduction_fish': self.count_reproduced_fish
        }

    def move_prepare(self, entity: Any, choice: List[Dict[str, int]]) -> None:
        """
        Prepare an entity's movement and handle reproduction if applicable.

        Args:
            entity: The entity (Fish or Shark) to move.
            choice: A list of move choices containing target coordinates.
        """
        target_x = choice[0]['x']
        target_y = choice[0]['y']
        previous_x = copy.deepcopy(entity.x)
        previous_y = copy.deepcopy(entity.y)

        if isinstance(entity, Shark):
            if isinstance(self.grid[target_y][target_x], Fish):
                self.shark_eats(entity, target_x, target_y)

        self.move_entity(entity, target_x, target_y)

        if len(choice) == 2 and (target_x != previous_x or target_y != previous_y):
            self.reproduce_entity(entity, previous_x, previous_y)

    def reproduce_entity(self, entity: Any, x: int, y: int) -> None:
        """
        Reproduce an entity at the specified location.

        Args:
            entity: The parent entity (Fish or Shark).
            x: The x-coordinate for the new entity.
            y: The y-coordinate for the new entity.
        """
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

    def shark_eats(self, entity: Shark, x: int, y: int) -> None:
        """
        Handle shark eating a fish at the given coordinates.

        Args:
            entity: The shark entity.
            x: The x-coordinate of the fish.
            y: The y-coordinate of the fish.
        """
        entity.eat()
        self.count_fish -= 1
        self.dead_fishes.append(copy.deepcopy(self.grid[y][x]))
        self.destroy_entity(self.grid[y][x], x, y)

    def get_neighbors(self, x: int, y: int) -> List[Optional[Any]]:
        """
        Get the north, south, east, and west neighbors of a grid cell.

        Args:
            x: X-coordinate.
            y: Y-coordinate.

        Returns:
            A list of neighboring cells (entities or None).
        """
        neighbors = []

        # North
        neighbors.append(self.grid[(y - 1) % self.height][x])

        # South
        neighbors.append(self.grid[(y + 1) % self.height][x])

        # East
        neighbors.append(self.grid[y][(x + 1) % self.width])

        # West
        neighbors.append(self.grid[y][(x - 1) % self.width])

        return neighbors

    def move_entity(self, entity: Any, x: int, y: int) -> None:
        """
        Move an entity to a new position on the grid.

        Args:
            entity: The entity to move.
            x: The new x-coordinate.
            y: The new y-coordinate.
        """
        self.grid[y][x] = entity
        if entity.x != x or entity.y != y:
            self.grid[entity.y][entity.x] = None
            entity.x = x
            entity.y = y
        self.next_entities.append(entity)

    def starved_shark(self, entity: Shark) -> None:
        """
        Handle a shark that has starved to death.

        Args:
            entity: The starving shark.
        """
        self.count_shark -= 1
        self.dead_sharks.append(copy.deepcopy(entity))
        self.destroy_entity(entity, entity.x, entity.y)

    def destroy_entity(self, entity: Any, x: int, y: int) -> None:
        """
        Remove an entity from the grid and entity lists.

        Args:
            entity: The entity to remove.
            x: The x-coordinate.
            y: The y-coordinate.
        """
        if entity in self.entities:
            index = self.entities.index(entity)
            self.entities[index] = None
            if entity in self.next_entities:
                self.next_entities.remove(entity)
        else:
            self.next_entities.remove(entity)
        self.grid[y][x] = None
