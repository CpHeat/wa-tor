from settings import simulation_parameters
import random

class Fish:
    def __init__(self, x :int, y:int):
        self.x = x
        self.y = y
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
    

    def choice_direction(self, list):
        match(random.choice(list)):
                case "N":
                    if(self.y == 0):
                        self.y = simulation_parameters["grid_height"] - 1
                    else:
                        self.y = self.y - 1
                case "S":
                    #verif en bas du tableau
                    if(simulation_parameters["grid_height"] - 1 == self.y):
                        self.y = 0
                    else:
                        self.y = self.y + 1
                case "W":
                    if(self.x == 0):
                        self.x = simulation_parameters["grid_width"] - 1
                    else:
                        self.x = self.x - 1
                case "E":
                    #verif à droite du tableau
                    if(simulation_parameters["grid_width"] - 1 == self.x):
                        self.x = 0
                    else :
                        self.x = self.x + 1
        
        return [{"x": self.x, "y": self.y}]



    def reproduce(self, new_position, old_position):
        if(self.reproduction_left > 0):
            self.reproduction_left -= 1

        if((new_position != old_position) and self.reproduction_left == 0):
            self.reproduction_left = self.reproduction_time
            return True
        else:
            return False
