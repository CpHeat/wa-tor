from typing import List, Dict, Any
from settings import simulation_parameters
from classes.animal import Animal
from classes.fish import Fish


class Shark(Animal):
    """
    Represents a shark entity in the simulation.

    Sharks can move, eat fish, reproduce, and starve if they don't feed
    within a certain number of turns. Each shark tracks its age, energy,
    and reproduction cycle.

    Attributes:
        shark_starvation_time (int): Number of turns a shark can survive without eating.
        shark_energy_gain (int): Energy regained when eating a fish.
        reproduction_time (int): Number of turns before the shark can reproduce.
        shark_starvation_left (int): Current remaining turns before starvation.
        reproduction_left (int): Remaining turns before next reproduction.
        fishes_eaten (int): Total number of fish eaten by this shark.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize a shark at the given (x, y) position.

        Args:
            x (int): X-coordinate on the grid.
            y (int): Y-coordinate on the grid.
        """
        super().__init__(x, y)
        self.shark_starvation_time: int = simulation_parameters['shark_starvation_time']
        self.shark_energy_gain: int = simulation_parameters['shark_energy_gain']
        self.reproduction_time: int = simulation_parameters["shark_reproduction_time"]

        self.shark_starvation_left: int = self.shark_starvation_time
        self.reproduction_left: int = self.reproduction_time

        self.fishes_eaten: int = 0

    def move(self, position_list: List[Any]) -> List[Dict[str, int]]:
        """
        Decide the shark's next movement based on neighboring positions.

        The shark prioritizes moving toward adjacent fish, otherwise moves
        to empty neighboring cells. If it reproduces, a baby shark is left
        at the old position.

        Args:
            position_list (List[Any]): List of neighboring grid cells (north, south, east, west).

        Returns:
            List[Dict[str, int]]: A list of dictionaries indicating the new position,
                                  and possibly the old position if reproduction occurs.
                                  Returns an empty list if the shark has starved.
        """
        self.age += 1
        self.shark_starvation_left -= 1

        old_position: Dict[str, int] = {"x": self.x, "y": self.y}
        verif: Dict[str, Any] = {
            "N": position_list[0],
            "S": position_list[1],
            "E": position_list[2],
            "W": position_list[3]
        }

        direction: List[str] = []
        direction_fish: List[str] = []
        list_result: List[Dict[str, int]] = []

        for key, value in verif.items():
            if isinstance(value, Fish):
                direction_fish.append(key)
            elif value is None:
                direction.append(key)

        if direction_fish:
            list_result = self.choice_direction(direction_fish)
        elif direction:
            list_result = self.choice_direction(direction)

        # Move or stay in place
        if len(list_result) == 1:
            new_position = list_result[0]
        else:
            new_position = old_position
            list_result.append(new_position)

        # Handle reproduction
        if self.reproduce(new_position, old_position):
            self.children_number += 1
            list_result.append(old_position)

        return list_result if self.shark_starvation_left > 0 else []

    def eat(self) -> None:
        """
        Handle the shark eating a fish, restoring its starvation counter
        by the defined energy gain, capped by its maximum starvation time.
        """
        self.shark_starvation_left += self.shark_energy_gain
        if self.shark_starvation_left > self.shark_starvation_time:
            self.shark_starvation_left = self.shark_starvation_time
        self.fishes_eaten += 1
