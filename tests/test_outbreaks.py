import unittest
from src.controllers.game import Game
from collections import deque


class TestOutbreaks(unittest.TestCase):
    def test_outbreaks(self):
        game = Game()
        game.board.add_cities()
        game.board.add_connections()

        madrid = game.board.cities["Madrid"]
        london = game.board.cities["London"]
        sao_paulo = game.board.cities["Sao Paulo"]
        new_york = game.board.cities["New York"]
        paris = game.board.cities["Paris"]


        game.infect(madrid, "Blue", 3, deque())
        game.infect(london, "Blue", 3, deque())
        game.infect(sao_paulo, "Yellow", 3, deque())

        game.infect(madrid, "Blue", 1, deque())

        self.assertEqual(game.board.outbreaks_counter, 2)
        diseases_in_new_york = sum(number for number in new_york.diseases.values())
        diseases_in_paris = sum(number for number in paris.diseases.values())
        diseases_in_sao_paulo = sum(number for number in sao_paulo.diseases.values())
        self.assertEqual(diseases_in_new_york, 2)
        self.assertEqual(diseases_in_paris, 2)
        self.assertEqual(diseases_in_sao_paulo, 4)


if __name__ == '__main__':
    unittest.main()
