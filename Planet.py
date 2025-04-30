import random
from Fish import Fish
from Shark import Shark
class Planet:
    def __init__(self, height:int, width:int, num_fish:int, num_shark:int):
        '''Initialize empty grid
        '''
        self.height = height
        self.width = width
        self.num_fish = num_fish
        self.num_shark = num_shark
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.entities = []
    
    def populate(self):
        '''Populate randomly the grid with fishes and sharks
        '''
        random_indices = random.sample(range(self.height * self.width), self.num_fish+self.num_shark)
        print("random_indices",random_indices)
        random_indices_sharq = random.sample(random_indices, self.num_shark)
        print("random_indices_sharq",random_indices_sharq)
        for i in random_indices_sharq:
            row = i // self.width 
            col = i % self.width 
            S = Shark(row,col)
            self.grid[row][col] = S 
            self.entities.append(S)
        
        random_indices_fish = list(set(random_indices)- set(random_indices_sharq))
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
        
        
    def check_entities(self):
        entity_copy = self.entities.copy()
        for entity in entity_copy :
            choice = entity.move(self.get_neighbors(entity.x,entity.y))
            if choice:
                target_x = choice.x
                target_y = choice.x
                old_x = entity.x
                old_y = entity.y
                if isinstance(entity,Shark):
                    entity.age +=1
                    # to move
                    if isinstance(self.grid[target_x][target_y],Fish):
                        entity.x = target_x
                        entity.y = target_y
                        self.grid[target_x][target_y] = entity
                        self.entities.append(entity)
                        self.num_fish -=1
                        entity.energy += energy
                    elif self.grid[target_x][target_y] is None:
                        entity.x = target_x
                        entity.y = target_y
                        self.grid[target_x][target_y] = entity
                    else: 
                        pass
                        
                    # to reproduce
                    if entity.age >= reprod_time:
                        baby_shark = Shark(old_x,old_y)
                        self.grid[old_x][old_y] = baby_shark 
                        self.entities.append(baby_shark)
                        self.num_shark +=1
                elif isinstance(entity,Fish):
                    if self.grid[target_x][target_y] is None:
                        # to move
                        entity.x = target_x
                        entity.y = target_y
                        self.grid[target_x][target_y] = entity
                        if entity.age >= reprod_time:
                            baby_fish = Fish(old_x,old_y)
                            self.grid[old_x][old_y] = baby_fish
                            self.entities.append(baby_fish)
                            self.num_fish +=1
                        
                    
                          
         


 
 
############ main
P = Planet(5,5,2,2)
P.populate()
print(P.get_grid())
print(P.entities)
print("voisins:", P.get_neighbors(0,0))
print("voisins:", P.get_neighbors(4,4))
print("voisins:", P.get_neighbors(0,4))
print("voisins:", P.get_neighbors(4,0))

  