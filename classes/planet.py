from settings import simulation_parameters
from classes.fish import Fish
from classes.shark import Shark
import random


'''
class Fish:
    def __init__(self,x,y):
        self.x = x
        self.y = y
 
class Shark:
    def __init__(self,x,y):
        self.x = x
        self.y = y
'''



class Planet:
    def __init__(self):
        '''Initialize empty grid
        '''
        self.height = 3#simulation_parameters.get('grid_height')
        self.width =  3 #simulation_parameters.get('grid_width')
        self.num_fish = 1#simulation_parameters.get('fish_reproduction_time')
        self.num_shark = 1# simulation_parameters.get('shark_starting_population')
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.entities = []
        self.populate()
        
    
    def populate(self):
        '''Populate randomly the grid with fishes and sharks
        '''
        random_indices = random.sample(range(self.height * self.width), self.num_fish+self.num_shark)
        
        random_indices_shark = random.sample(random_indices, self.num_shark)
        
        for i in random_indices_shark:
            row = i // self.width 
            col = i % self.width 
            S = Shark(row,col)
            self.grid[row][col] = S 
            self.entities.append(S)
        
        random_indices_fish = list(set(random_indices)- set(random_indices_shark))
        
        for i in random_indices_fish:
            row = i // self.width 
            col = i % self.width 
            F = Fish(row,col)
            self.grid[row][col] = F
            self.entities.append(F)
       
            
          
                    
                
                
            
        


       
        
    
    def get_grid(self):
        return self.grid
    
    def get_neighbors(self, x,y): 
        # from the position
        neighbors = []
        new_y = y-1 if y != 0 else self.height-1
        neighbors.append(self.grid[x][new_y]) # N
        new_y = y+1 if y != self.height-1 else 0
        neighbors.append(self.grid[x][new_y])  # S
        
        new_x = x+1 if x != self.width-1 else 0
        neighbors.append(self.grid[new_x][y])  # E
        
        new_x = x-1 if x != 0 else self.width -1
        neighbors.append(self.grid[new_x][y])  # W
        
        return neighbors
    
    def move_entity(self, target_pos_dict,entity):
        target_x = target_pos_dict.get('x')
        target_y = target_pos_dict.get('y')
        entity.x = target_x
        entity.y = target_y
        self.grid[target_x][target_y] = entity
        self.entities.append(entity)
        
    def move_eat_entity(self, choice, entity):
        self.move_entity(choice[0])
        #entity.eat()
        self.num_fish -=1
        
        
        
    def reproduce_fish(self,old_pos_dict):
        old_x = old_pos_dict.get('x')
        old_y = old_pos_dict.get('y')
        
        baby_fish = Fish(old_x,old_y)
        self.grid[old_x][old_y] = baby_fish
        self.entities.append(baby_fish)
        self.num_fish +=1
        
    def reproduce_shark(self,old_pos_dict):
        old_x = old_pos_dict.get('x')
        old_y = old_pos_dict.get('y')
        baby_shark = Shark(old_x,old_y)
        self.grid[old_x][old_y] = baby_shark 
        self.entities.append(baby_shark)
        self.num_shark +=1
        
        

        
    def check_entities(self):
        entity_copy = self.entities.copy()
        self.entities = []
        for entity in entity_copy :
            choice =   [{'x':0, 'y':1},{'x':0, 'y':2}]      #entity.move(self.get_neighbors(entity.x,entity.y))
            print("check_entities: choice", choice)
            print(f"check_entities: grid", self.grid)
            
            if len(choice) == 2: # move and reproduce entity
                target_x = choice[0].get('x')
                target_y = choice[0].get('y')
                
                if isinstance(entity,Shark): # case shark
                    # check target cell
                    if isinstance(self.grid[target_x][target_y],Fish):
                        # to move & eat
                        self.move_eat_entity(choice[0],entity)
                            
                    elif self.grid[target_x][target_y] is None:
                        # move
                        self.move_entity(choice[0],entity)
                    else: 
                        pass
                        
                    # to reproduce shark
                    
                    self.reproduce_shark(choice[1])
                    
                    
                elif isinstance(entity,Fish): #case fish
                    
                    # to move
                    self.move_entity(choice[0],entity)
                    # to reproduce fish
                    self.reproduce_fish(choice[1])
                    
                    
            elif len(choice) == 1: # move entity
                self.move_entity(choice[0],entity)
               
            else: # nothing to do
                self.entities.append(entity)          
        return self.get_grid()
                        
                    


  