import unittest
from src.controllers.game import Game
from src.models.player import Player
from src.models.card import CityCard
from src.misc.images import role_1_pin
from src.misc.utility import from_color_to_str
from collections import deque


class TestActions(unittest.TestCase):
    def test_build(self):
        game = Game()
        game.setup(deque())

        madrid = game.board.cities["Madrid"]
        game.build_research_station(madrid, deque())

        self.assertTrue(madrid.has_research_station())
        self.assertEqual(game.research_station_count, 6)

    def test_cure(self):
        game = Game()
        game.setup(deque())

        game.cure("Red", deque())

        self.assertTrue(game.is_disease_cured("Red"))

    def test_treat(self):
        game = Game()
        game.setup(deque())

        city = next(city for city in game.board.cities.values() if city.has_diseases())
        # NECESSARY MOVEMENT BECAUSE TREATS ONLY WORKS IN THE CURRENT PLAYER LOCATION
        game.current_player.move(city.x, city.y, city.name)

        city_color = from_color_to_str(city.color)
        current_number_of_diseases = city.diseases[city_color]

        game.treat(city_color, deque())

        self.assertEqual(city.diseases[city_color], current_number_of_diseases - 1)

    def test_share_give(self):
        game = Game()
        game.player_count = 2
        game.difficulty = "EASY"

        game = Game()
        game.difficulty = "EASY"
        game.player_count = 2
        player1 = Player("first", role_1_pin)
        player2 = Player("second", role_1_pin)
        game.players.add(player1, player2)
        game.setup(deque())

        game.current_player = player1

        card = next(card for card in player1.cards if isinstance(card, CityCard))

        game.share(card, player2, "Give", deque())
        self.assertEqual(len(player1.cards), 3)
        self.assertEqual(len(player2.cards), 5)

    def test_share_take(self):
        game = Game()
        game.player_count = 2
        game.difficulty = "EASY"

        game = Game()
        game.difficulty = "EASY"
        game.player_count = 2
        player1 = Player("first", role_1_pin)
        player2 = Player("second", role_1_pin)
        game.players.add(player1, player2)
        game.setup(deque())

        game.current_player = player1

        card = next(card for card in player2.cards if isinstance(card, CityCard))

        game.share(card, player2, "Take", deque())
        self.assertEqual(len(player1.cards), 5)
        self.assertEqual(len(player2.cards), 3)


if __name__ == '__main__':
    unittest.main()
