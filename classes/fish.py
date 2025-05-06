from typing import List, Dict, Any
from settings import simulation_parameters
from classes.animal import Animal
import random


class Fish(Animal):
    """
    Represents a fish entity in the simulation.

    Fish can move, reproduce, and age over time. They prefer moving into 
    empty neighboring cells and leave offspring at their previous location 
    when reproduction occurs.

    Attributes:
        reproduction_time (int): Number of turns required before reproduction.
        reproduction_left (int): Remaining turns before next reproduction.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize a fish at the given (x, y) position.

        Args:
            x (int): X-coordinate on the grid.
            y (int): Y-coordinate on the grid.
        """
        super().__init__(x, y)
        self.reproduction_time: int = simulation_parameters["fish_reproduction_time"]
        self.reproduction_left: int = self.reproduction_time

    def move(self, position_list: List[Any]) -> List[Dict[str, int]]:
        """
        Decide the fish's next movement based on neighboring positions.

        Fish only move into empty neighboring cells. If no move is possible, 
        they stay in place. If they reproduce, a baby fish is left at the 
        original location.

        Args:
            position_list (List[Any]): List of neighboring grid cells 
                                       (north, south, east, west).

        Returns:
            List[Dict[str, int]]: A list containing the new position, and 
                                  possibly the old position if reproduction occurs.
        """
        self.age += 1
        old_position: Dict[str, int] = {"x": self.x, "y": self.y}
        verif: Dict[str, Any] = {
            "N": position_list[0],
            "S": position_list[1],
            "E": position_list[2],
            "W": position_list[3]
        }

        direction: List[str] = []
        list_result: List[Dict[str, int]] = []

        for key, value in verif.items():
            if value is None:
                direction.append(key)

        if direction:
            list_result = self.choice_direction(direction)

        if len(list_result) == 1:
            new_position = list_result[0]
        else:
            new_position = old_position

        new_positions: List[Dict[str, int]] = [new_position]

        if self.reproduce(new_position, old_position):
            self.children_number += 1
            new_positions.append(old_position)

        return new_positions
