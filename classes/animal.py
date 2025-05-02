
from settings import simulation_parameters
import random

class Animal:
    def __init__(self, x :int, y:int):
        self.x = x
        self.y = y
        self.reproduction_time = 0
        self.reproduction_left =  0
        self.age = 0
        self.followed = False
        self.children_number = 0

    def choice_direction(self, list):
        x = self.x
        y = self.y
        match(random.choice(list)):
                case "N":
                    if(self.y == 0):
                        y = simulation_parameters["grid_height"] - 1
                    else:
                        y = self.y - 1
                case "S":
                    #verif en bas du tableau
                    if(simulation_parameters["grid_height"] - 1 == self.y):
                        y = 0
                    else:
                        y = self.y + 1
                case "W":
                    if(self.x == 0):
                        x = simulation_parameters["grid_width"] - 1
                    else:
                        x = self.x - 1
                case "E":
                    #verif à droite du tableau
                    if(simulation_parameters["grid_width"] - 1 == self.x):
                        x = 0
                    else :
                        x = self.x + 1
        
        return [{"x": x, "y": y}]
    
    def reproduce(self, new_position, old_position):
        if(self.reproduction_left > 0):
            self.reproduction_left -= 1

        if((new_position != old_position) and self.reproduction_left == 0):
            self.reproduction_left = self.reproduction_time
            return True
        else:
            return False

