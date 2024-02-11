import unittest
from src.models.player import Player
from src.controllers.game import Game
from src.misc.images import role_1_pin
from collections import deque

EXPECTED_INFECTION_DECK_CARDS = 39
EXPECTED_INFECTION_DISCARD_DECK = 9
EXPECTED_PLAYER_DECK_CARDS = 49
EXPECTED_NUMBER_OF_CITIES = 48
EXPECTED_LEFTOVER_DISEASE_CUBES = 4 * 24 - (3 * 1 + 3 * 2 + 3 * 3)


class TestBoard(unittest.TestCase):
    def test_cards(self):
        game = Game()
        game.difficulty = "EASY"
        game.player_count = 2
        player1 = Player("first", role_1_pin)
        player2 = Player("second", role_1_pin)
        game.players.add(player1, player2)

        game.setup(deque())

        self.assertEqual(len(game.decks.players_discard_pile), 0)
        self.assertEqual(len(game.decks.infection_discard_pile), EXPECTED_INFECTION_DISCARD_DECK)
        self.assertEqual(len(game.decks.infection_deck), EXPECTED_INFECTION_DECK_CARDS)
        self.assertEqual(len(game.decks.player_deck), EXPECTED_PLAYER_DECK_CARDS)
        for player in game.players:
            self.assertEqual(len(player.cards), 4)

    def test_general_stuff(self):
        game = Game()
        game.difficulty = "EASY"
        game.player_count = 2
        player1 = Player("first", role_1_pin)
        player2 = Player("second", role_1_pin)
        game.players.add(player1, player2)

        game.setup(deque())

        self.assertEqual(len(game.board.cities), EXPECTED_NUMBER_OF_CITIES)
        disease_number = sum(disease[0] for disease in game.disease_info.values())
        self.assertEqual(disease_number, EXPECTED_LEFTOVER_DISEASE_CUBES)
        self.assertEqual(game.current_player.location, "Atlanta")


if __name__ == '__main__':
    unittest.main()
