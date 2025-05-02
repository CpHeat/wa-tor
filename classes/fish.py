from settings import simulation_parameters
from classes.animal import Animal
import random

class Fish(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.reproduction_time = simulation_parameters["fish_reproduction_time"]
        self.reproduction_left =  self.reproduction_time

    def move(self, list):
        old_position = {"x": self.x, "y": self.y}
        verif = {"N": list[0] , "S": list[1], "E": list[2], "W": list[3]}
        direction = []
        list_result = []
        for key, value in verif.items():
            if(value == None):
                direction.append(key)               
        
        if( len(direction) > 0):
            list_result = self.choice_direction(direction)

        if(len(list_result) == 1):
            new_position = list_result[0]
        else:
            new_position = old_position       
            list_result.append(new_position)

        if(self.reproduce(new_position , old_position) == True):
            list_result.append(old_position)

        return list_result