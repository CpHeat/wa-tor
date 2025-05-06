from abc import ABC
from typing import List, Dict
from settings import simulation_parameters
import random


class Animal(ABC):
    """
    Abstract base class representing a generic animal in the simulation.

    All animals have a position on the grid, age, reproduction cycle, and
    the ability to choose directions for movement and to reproduce.

    Attributes:
        x (int): X-coordinate on the grid.
        y (int): Y-coordinate on the grid.
        reproduction_time (int): Number of turns required before reproduction.
        reproduction_left (int): Remaining turns before next reproduction.
        age (int): Current age (in turns) of the animal.
        followed (bool): Whether this animal is tracked/followed in the simulation.
        children_number (int): Total number of offspring produced.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize an animal at the given (x, y) position.

        Args:
            x (int): X-coordinate on the grid.
            y (int): Y-coordinate on the grid.
        """
        self.x: int = x
        self.y: int = y
        self.reproduction_time: int = 0
        self.reproduction_left: int = 0
        self.age: int = 0
        self.followed: bool = False
        self.children_number: int = 0

    def choice_direction(self, choice_list: List[str]) -> List[Dict[str, int]]:
        """
        Select a random direction from the available choices and compute
        the new grid position, considering wrap-around at edges.

        Args:
            choice_list (List[str]): List of possible directions ('N', 'S', 'E', 'W').

        Returns:
            List[Dict[str, int]]: A list containing one dictionary with the new (x, y) position.
        """
        x: int = self.x
        y: int = self.y

        match random.choice(choice_list):
            case "N":
                y = simulation_parameters["grid_height"] - 1 if self.y == 0 else self.y - 1
            case "S":
                y = 0 if self.y == simulation_parameters["grid_height"] - 1 else self.y + 1
            case "W":
                x = simulation_parameters["grid_width"] - 1 if self.x == 0 else self.x - 1
            case "E":
                x = 0 if self.x == simulation_parameters["grid_width"] - 1 else self.x + 1

        return [{"x": x, "y": y}]

    def reproduce(self, new_position: Dict[str, int], old_position: Dict[str, int]) -> bool:
        """
        Determine if the animal reproduces, based on movement and reproduction cycle.

        Args:
            new_position (Dict[str, int]): The intended new (x, y) position.
            old_position (Dict[str, int]): The previous (x, y) position.

        Returns:
            bool: True if reproduction occurs, False otherwise.
        """
        if self.reproduction_left > 0:
            self.reproduction_left -= 1

        if (new_position != old_position) and self.reproduction_left == 0:
            self.reproduction_left = self.reproduction_time
            return True
        else:
            return False
