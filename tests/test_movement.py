import unittest
from src.controllers.game import Game
from collections import deque


class TestMovement(unittest.TestCase):
    def test_drive(self):
        game = Game()
        game.setup(deque())

        # WHEN THE CITIES ARE CONNECTED
        game.move("Washington", "basic", deque())
        self.assertEqual(game.current_player.location, "Washington")
        self.assertEqual(game.current_player.moves, 3)

        # WHEN THE CITIES ARE NOT CONNECTED
        game.move("Bogota", "basic", deque())
        self.assertNotEqual(game.current_player.location, "Bogota")
        self.assertEqual(game.current_player.moves, 3)

        # WHEN THE MOVEMENT IS IN THE SAME PLACE
        game.move("Washington", "basic", deque())
        self.assertEqual(game.current_player.location, "Washington")
        self.assertEqual(game.current_player.moves, 3)

    def test_direct(self):
        game = Game()
        game.setup(deque())

        # MOVES DIRECTLY TO BOGOTA
        game.move("Bogota", "direct", deque())
        self.assertEqual(game.current_player.location, "Bogota")
        self.assertEqual(game.current_player.moves, 3)

        # TRIES TO MOVE TO THE SAME CITY
        game.move("Bogota", "direct", deque())
        self.assertEqual(game.current_player.location, "Bogota")
        self.assertNotEqual(game.current_player.moves, 2)


if __name__ == '__main__':
    unittest.main()
