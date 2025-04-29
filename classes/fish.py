from settings import fish_reproduction_time
import random

class Fish:
    def __init__(self, position :[]):
        self.position = position
        self.reproduction_time = fish_reproduction_time

    def move(self, list):
        verif = {"N": list[0] , "S": list[1], "E": list[2], "W": list[3]}
        direction = []
        for key, value in verif.items():
            if(value == None):
                direction.append(key)               
        

        match(random.choice(direction)):
            case "N":
                self.position = [self.position[0] + 1, self.position[1]]
            case "S":
                self.position = [self.position[0] - 1, self.position[1]]
            case "E":
                self.position = [self.position[0], self.position[1] + 1]
            case "W":
                self.position = [self.position[0], self.position[1] - 1]

        return print(self.position)
    

    def reproduce(self):
        return []
