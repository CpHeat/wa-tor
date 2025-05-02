from settings import simulation_parameters
from classes.animal import Animal
from classes.fish import Fish

class Shark(Animal):

    def __init__(self,x:int, y:int):
        super().__init__(x, y)
        #nb deplacement avant retirer une vie
        self.shark_starvation_time = simulation_parameters['shark_starvation_time']
        #nb de vie du requin
        self.shark_starting_energy_time = simulation_parameters['shark_starting_energy']
        #temps avant reproduction
        self.reproduction_time = simulation_parameters["shark_reproduction_time"]
            
        self.shark_starvation_left = self.shark_starvation_time
        self.shark_starting_energy_left = self.shark_starting_energy_time
        self.reproduction_left =  self.reproduction_time

        self.fish_eaten = 0


    def move(self, list):
        old_position = {"x": self.x, "y": self.y}
        verif = {"N": list[0] , "S": list[1], "E": list[2], "W": list[3]}
        direction = []
        direction_fish = []
        list_result = []
        for key, value in verif.items():
            if((isinstance(value,Fish)) and (isinstance(value,Shark) == False)):
                direction_fish.append(key)
            elif(value == None):
                direction.append(key)          
        
        if( len(direction_fish) > 0):
            list_result = self.choice_direction(direction_fish)
        elif( len(direction) > 0):
            list_result = self.choice_direction(direction)

        #move
        if(len(list_result) == 1):
            new_position = list_result[0]
            self.lost_life()
        #not move
        else:
            new_position = old_position       
            list_result.append(new_position)

        if(self.reproduce(new_position , old_position) == True):
            list_result.append(old_position)

        return list_result if self.shark_starting_energy_left > 0 else []
    
    def eat(self):
        self.shark_starvation_left = self.shark_starvation_time

    def lost_life(self):
        if(self.shark_starvation_left > 0):
            self.shark_starvation_left -= 1
        elif(self.shark_starting_energy_left > 0):
            self.shark_starting_energy_left -= 1
            self.shark_starvation_left = self.shark_starvation_time
