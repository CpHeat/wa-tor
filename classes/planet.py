from settings import simulation_parameters
import random

class Fish:
    def __init__(self,x,y):
        self.x = x
        self.y = y
 
class Shark:
    def __init__(self,x,y):
        self.x = x
        self.y = y



class Planet:
    def __init__(self):
        '''Initialize empty grid
        '''
        self.height = simulation_parameters.get('grid_height')
        self.width = simulation_parameters.get('grid_width')
        self.num_fish = simulation_parameters.get('shark_nb')
        self.num_shark = simulation_parameters.get('fish_nb')
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.entities = []
        self.populate()
        
    
    def populate(self):
        '''Populate randomly the grid with fishes and sharks
        '''
        random_indices = random.sample(range(self.height * self.width), self.num_fish+self.num_shark)
        print("random_indices",random_indices)
        random_indices_shark = random.sample(random_indices, self.num_shark)
        print("random_indices_shark",random_indices_shark)
        for i in random_indices_shark:
            row = i // self.width 
            col = i % self.width 
            S = Shark(row,col)
            self.grid[row][col] = S 
            self.entities.append(S)
        
        random_indices_fish = list(set(random_indices)- set(random_indices_shark))
        print("random_indices_fish",random_indices_fish)
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
        
        
    def reproduce_entity(self):
        pass

        
    def check_entities(self):
        entity_copy = self.entities.copy()
        self.entities = []
        for entity in entity_copy :
            choice =   [{'x':0, 'y':1},{'x':0, 'y':2}]      #entity.move(self.get_neighbors(entity.x,entity.y))
            print("check_entities: choice", choice)
            print(f"check_entities: grid", self.grid)
            
            if len(choice) == 2: # move and reproduce
                target_x = choice[0].get('x')
                target_y = choice[0].get('y')
                old_x = entity.x
                old_y = entity.y
                if isinstance(entity,Shark):
                    
                    # to move & eat
                    if isinstance(self.grid[target_x][target_y],Fish):
                        # move
                        entity.x = target_x
                        entity.y = target_y
                        self.grid[target_x][target_y] = entity
                        self.entities.append(entity)
                        #entity.eat()
                        self.num_fish -=1
                        
                    elif self.grid[target_x][target_y] is None:
                        # move
                        entity.x = target_x
                        entity.y = target_y
                        self.grid[target_x][target_y] = entity
                        self.entities.append(entity)
                    else: 
                        pass
                        
                    # to reproduce
                    
                    baby_shark = Shark(old_x,old_y)
                    self.grid[old_x][old_y] = baby_shark 
                    self.entities.append(baby_shark)
                    self.num_shark +=1
                    
                elif isinstance(entity,Fish):
                    
                    # to move
                    entity.x = target_x
                    entity.y = target_y
                    self.grid[target_x][target_y] = entity
                    # to reproduce
                    baby_fish = Fish(old_x,old_y)
                    self.grid[old_x][old_y] = baby_fish
                    self.entities.append(baby_fish)
                    self.num_fish +=1
                    
            elif len(choice) == 1: # move 
                entity.x = target_x
                entity.y = target_y
                self.grid[target_x][target_y] = entity
                self.entities.append(entity)
            else: # nothing to do
                self.entities.append(entity)          
        return self.get_grid()
                        
                    


  