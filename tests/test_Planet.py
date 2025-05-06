from classes.planet import Planet
from classes.fish import Fish
from classes.shark import Shark
import unittest


############ main
class TestPlanet(unittest.TestCase):

    def setUp(self):
        self.planet = Planet()
        
        

   
    def test_check_entities_runs(self):
        # Just check that it runs and returns a grid
        print("================call 1 ==================")
        print("grid before the check entities")
        grid_before = self.planet.grid
        print(grid_before)
        result = self.planet.check_entities()
        print("grid after the check entities")
        print(result['grid'])
        print("==================call 2================")
        print("grid before the check entities")
        grid_before = self.planet.grid
        print(grid_before)
        result = self.planet.check_entities()
        print("grid after the check entities")
        print(result['grid'])
        print('fishes_eaten', result['fishes_eaten'])
        
        self.assertEqual(len(result['grid']), self.planet.height)
        self.assertEqual(len(result['grid'][0]), self.planet.width) 
        
    '''  
    def test_move_eat_entity_shark_eats_fish(self):
        shark = Shark(0, 0)
        fish = Fish(1, 0)
        self.planet.grid[0][0] = shark
        self.planet.grid[0][1] = fish
        self.planet.move_eat_entity({'x': 1, 'y': 0}, shark)
        
        self.assertEqual(self.planet.count_shark_eats, 1)
        self.assertEqual(self.planet.count_eaten_fish, 1)
        self.assertEqual(self.planet.grid[0][1], shark)
        
        
    def test_initial_grid_size(self):
        self.assertEqual(len(self.planet.grid), 3)
        self.assertEqual(len(self.planet.grid[0]), 3)
        
    def test_population_counts(self):
        fish_count = []#sum(isinstance(e, Fish) for e in self.planet.entities)
        shark_count = [] # sum(isinstance(e, Shark) for e in self.planet.entities)
        
        for e in self.planet.entities:
            if (isinstance(e, Shark)):
                shark_count.append(e)
                
            elif (isinstance(e, Fish)) and (not(isinstance(e, Shark))):
                fish_count.append(e)
        self.assertEqual(len(fish_count), self.planet.num_fish)
        self.assertEqual(len(shark_count), self.planet.num_shark)
        #print("grid populated", self.planet.grid)
      
    def test_get_neighbors(self):
        neighbors = self.planet.get_neighbors(0, 0)
        #print(" neighbors of 0,0:", neighbors)
        self.assertEqual(neighbors, [self.planet.grid[2][0],self.planet.grid[1][0],self.planet.grid[0][1],self.planet.grid[0][2]])
        neighbors = self.planet.get_neighbors(1, 1)
        #print(" neighbors of 1,1:", neighbors)
        self.assertEqual(neighbors, [self.planet.grid[0][1],self.planet.grid[2][1],self.planet.grid[1][2],self.planet.grid[1][0]])
        self.assertEqual(len(neighbors), 4)
        
        
    def test_move_entity(self):
        shark = Shark(0, 0)
        
        self.planet.grid[0][0]=shark
        prev_len = len(self.planet.entities)
        self.planet.move_entity({'x': 1, 'y': 1},shark)
        self.assertEqual(shark.x, 1)
        self.assertEqual(shark.y, 1)
        self.assertIsInstance(self.planet.grid[1][1], Shark)
        self.assertIsNone(self.planet.grid[0][0])
        self.assertEqual(self.planet.grid[1][1], shark)
        self.assertEqual(len(self.planet.entities), prev_len + 1)
    
    def test_reproduce_fish(self):
        prev_count = self.planet.count_fish
        prev_count_rep = self.planet.count_reproduced_fish
        prev_len = len(self.planet.entities)
        #print("before grid to test rep fish ", self.planet.grid)
        self.planet.reproduce_fish({'x': 0, 'y': 0})
        #print("after grid to test rep fish ", self.planet.grid)
        self.assertEqual(self.planet.count_fish, prev_count + 1)
        self.assertEqual(self.planet.count_reproduced_fish, prev_count_rep + 1)
        self.assertEqual(len(self.planet.entities), prev_len + 1)
        self.assertIsInstance(self.planet.grid[0][0], Fish)
        self.assertNotIsInstance(self.planet.grid[0][0], Shark)
 
    def test_reproduce_shark(self):
        prev_count = self.planet.count_shark
        prev_count_rep = self.planet.count_reproduced_shark
        prev_len = len(self.planet.entities)
        #print("before grid to test rep shark ", self.planet.grid)
        self.planet.reproduce_shark({'x': 2, 'y': 2})
        #print("after grid to test rep shark ", self.planet.grid)
        self.assertEqual(self.planet.count_shark, prev_count + 1)
        self.assertEqual(self.planet.count_reproduced_shark, prev_count_rep + 1)
        self.assertEqual(len(self.planet.entities), prev_len + 1)
        self.assertIsInstance(self.planet.grid[2][2], Shark)
'''
   

if __name__ == '__main__':
    unittest.main()




