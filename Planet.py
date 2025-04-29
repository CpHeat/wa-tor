import random
import Fish
class Planet:
    def __init__(self, height:int, width:int, num_fish:int, num_shark:int):
        self.height = height
        self.width = width
        self.num_fish = num_fish
        self.num_shark = num_shark
        self.grid = [[]]
        self.entities_fish = []
        self.entities_shark = []
    
    def populate(self):
        
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        random_indices = random.sample(range(self.height * self.width), self.num_fish+self.num_shark)
        for i in random_indices:
            row = i // self.width 
            col = i % self.width 
            self.grid[row][col] = Fish.Fish(row, col)
        


       
        
    
    def get_grid(self):
        return self.grid
    
    def get_neighbors(self, x,y): 
        # from the position
        neighbors = [None]
        new_y = y-1 if y != 0 else self.height-1
        neighbors.append(self.grid[x][new_y]) # N
        new_y = y+1 if y != self.height-1 else 0
        neighbors.append(self.grid[x][new_y])  # S
        
        new_x = x+1 if x != self.width-1 else 0
        neighbors.append(self.grid[new_x][y])  # E
        
        new_x = x-1 if x != 0 else self.width -1
        neighbors.append(self.grid[new_x][y])  # W
        
        return neighbors
        
        
        
    

 
 
############ main
P = Planet(5,5,2,2)
P.populate()
print(P.get_grid())
print("voisins:", P.get_neighbors(0,0))
print("voisins:", P.get_neighbors(4,4))
print("voisins:", P.get_neighbors(0,4))
print("voisins:", P.get_neighbors(4,0))

  