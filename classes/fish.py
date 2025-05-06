from settings import simulation_parameters
from classes.animal import Animal
import random

class Fish(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.reproduction_time = simulation_parameters["fish_reproduction_time"]
        self.reproduction_left =  self.reproduction_time

    def move(self, position_list):
        self.age += 1
        old_position = {"x": self.x, "y": self.y}
        print("old_position", old_position)
        verif = {"N": position_list[0] , "S": position_list[1], "E": position_list[2], "W": position_list[3]}

        print("position_list", position_list)

        direction = []
        list_result = []
        for key, value in verif.items():
            print(f"key {key}, value {value}")
            if value is None:
                direction.append(key)   
        
        if len(direction) > 0:
            list_result = self.choice_direction(direction)

        if len(list_result) == 1:
            new_position = list_result[0]
        else:
            new_position = old_position
        new_positions = [new_position]


        if self.reproduce(new_position, old_position):
            self.children_number += 1
            new_positions.append(old_position)

        print("list new_positions", new_positions)
        return new_positions