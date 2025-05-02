import unittest
from classes.shark import Shark
from classes.fish import Fish

class test_shark(unittest.TestCase):

#
#   Commande de base 
# 

    #deplacer vers le nord
    def test_shark_deplacement_nord(self):
        instance = Shark(x=4, y=7)
        self.assertEqual(instance.move([None, 1, 1, 1]), [{"x":4, "y":6}])

    #deplacer vers le sud
    def test_shark_deplacement_sud(self):
        instance = Shark(x=4, y=7)
        self.assertEqual(instance.move([1, None, 1, 1]), [{"x":4, "y":8}])

    #deplacer vers l'ouest
    def test_shark_deplacement_west(self):
        instance = Shark(x=4, y=7)
        self.assertEqual(instance.move([1, 1, 1, None]), [{"x":3, "y":7}])
    
    #deplacer vers l'est
    def test_shark_deplacement_est(self):
        instance = Shark(x=4, y=7)
        self.assertEqual(instance.move([1, 1, None, 1]), [{"x":5, "y":7}])

    #conserver la même position car pas de place de mouvement
    def test_shark_deplacement_none(self):
        instance = Shark(x=4, y=7)
        self.assertEqual(instance.move([1, 1, 1, 1]), [{"x":4, "y":7}])

    #utiliser la méthode reproduce
    def test_shark_reproduce(self):
         list_result = ""
         test_reproduce = Shark(x=4, y=7)
         for _ in range(5):
             list_result = test_reproduce.move([1, None, 1, 1])
         self.assertEqual(list_result, [{"x":4, "y":8}, {"x":4, "y":7}])
    
    #ne pas utiliser la méthode reproduce (ne peux pas se déplacer)
    def test_shark_impossible_reproduce(self):
        list_result = ""
        test_reproduce = Shark(x=4, y=7)
        for _ in range(5):
            list_result = test_reproduce.move([1, 1, 1, 1])
        self.assertEqual(list_result, [{"x":4, "y":7}])
    
    #faire un reproduce quand il peut
    def test_shark_reproduce_after_move(self):
        list_result = ""
        test_reproduce = Shark(x=4, y=7)
        for _ in range(6):
            list_result = test_reproduce.move([1, 1, 1, 1])
        list_result = test_reproduce.move([None, 1, 1, 1])
        self.assertEqual(list_result, [{"x":4, "y":6}, {"x":4, "y":7}])

#
# mouvement pour le requin
# 
    #se déplacer sur les case poisson
    def test_shark_move_fish(self):
        list_result = ""
        test_reproduce = Shark(x=4, y=7)
        list_result = test_reproduce.move([None, 1, Fish(x=5,y=7), 1])
        print(list_result)
        self.assertEqual(list_result, [{"x":5, "y":7}])


#
# Commande spécial pour le requin
# 

    #tester la dépense d'energie s'il y a mouvement
    def test_shark_energie_consume(self):
        instance = Shark(x=4, y=7)
        instance.move([1,None,1,1])
        print(f"deplacement du requin restant: {instance.shark_starvation_left} ")
        self.assertEqual(instance.shark_starvation_left, instance.shark_starvation_time - 1)

    #tester la dépense de vie s'il n'y a plus de mouvement restant
    def test_shark_life_consume(self):
        instance = Shark(x=4, y=7)
        for _ in range(4):
            instance.move([1,None,1,1])
            print(f"deplacement du requin restant: {instance.shark_starvation_left}  vie restante: {instance.shark_starting_energy_left}")
        
        self.assertEqual(instance.shark_starvation_left, instance.shark_starting_energy_left - 1)

    #tester la dépense d'energie s'il n'y a pas de mouvement
    def test_shark_energie_not_consume(self):
        instance = Shark(x=4, y=7)
        for _ in range(4):
            instance.move([1,1,1,1])
            print(f"deplacement du requin restant: {instance.shark_starvation_left}  vie restante: {instance.shark_starting_energy_left}")
        self.assertEqual(instance.shark_starvation_left, instance.shark_starvation_time)

    #tester la mort du requin
    def test_shark_death(self):
        list_result = ""
        instance = Shark(x=4, y=7)
        instance.shark_starting_energy_left = 0
        list_result = instance.move([1,None,1,1])
        print(list_result)
        self.assertEqual(list_result, [])

    #remettre de l'energie quand on appelle la fonction eat
    def test_shark_add_energie(self):
        list_result = ""
        instance = Shark(x=4, y=7)
        for _ in range(3):
            instance.move([1,None,1,1])
            print(f"deplacement du requin restant: {instance.shark_starvation_left}  vie restante: {instance.shark_starting_energy_left}")
        instance.eat()
        print("mange")
        print(f"deplacement du requin restant: {instance.shark_starvation_left}  vie restante: {instance.shark_starting_energy_left}")
        self.assertEqual(instance.shark_starvation_left, instance.shark_starvation_time)

#
# test global
# 

    #test complet
    def test_shark_global(self):
            instance = Shark(x=4, y=7)
            for _ in range(20):
                result = instance.move([1,None,1,1])
                print(f"deplacement du requin restant: {instance.shark_starvation_left} | vie restante: {instance.shark_starting_energy_left} | renvoie: {result}")

if __name__ == '__main__':
    unittest.main()