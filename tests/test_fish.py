import unittest
from classes.fish import Fish

class test_fish(unittest.TestCase):
    
    #deplacer vers le nord
    def test_fish_deplacement_nord(self):
        instance = Fish(x=4, y=7)
       # self.assertEqual(instance.move([None, 1, 1, 1]), [{"x":4, "y":6}])

    #deplacer vers le sud
    def test_fish_deplacement_sud(self):
        instance = Fish(x=4, y=7)
       # self.assertEqual(instance.move([None, 1, 1, 1]), [{"x":4, "y":6}])

    #deplacer vers l'ouest
    def test_fish_deplacement_west(self):
        instance = Fish(x=4, y=7)
       # self.assertEqual(instance.move([None, 1, 1, 1]), [{"x":4, "y":6}])
    
    #deplacer vers l'est
    def test_fish_deplacement_est(self):
        instance = Fish(x=4, y=7)
       # self.assertEqual(instance.move([None, 1, 1, 1]), [{"x":4, "y":6}])

    #conserver la même position car pas de place de mouvement
    def test_fish_deplacement_none(self):
        instance = Fish(x=4, y=7)
        self.assertEqual(instance.move([1, 1, 1, 1]), [{"x":4, "y":6}])

    #utiliser la méthode reproduce
    def test_fish_reproduce(self):
        list_result = ""
        test_reproduce = Fish(x=4, y=7)
        for _ in range(5):
            list_result = test_reproduce.move([1, None, 1, 1])
        self.assertEqual(list_result, [{"x":4, "y":2}, {"x":4, "y":1}])
    

if __name__ == '__main__':
    unittest.main()