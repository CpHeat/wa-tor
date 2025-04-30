from settings import simulation_parameters
from fish import Fish
import random


class Fhark(Fish):

    def __init__(self,x:int, y:int, ):
        super.__init__(x, y)
        self.shark_starvation_time = simulation_parameters['shark_starvation_time']

        def move(self, list):
            list_fish = []
            list_none = []
            old_position = {"x": self.x, "y": self.y}
            verif = {"N": list[0] , "S": list[1], "E": list[2], "W": list[3]}

            #vérif si il y a des poissons en voisin ou non
            for key, value in verif.items():
                if(isinstance(value, Fish)):
                    list_fish.append(key)
                elif(value == None):
                    list_none.append(key)
            
            if( len(list_fish) > 0):
                match(random.choice(list_fish)):
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
            elif(len(list_none) > 0):
                match(random.choice(list_none)):
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

