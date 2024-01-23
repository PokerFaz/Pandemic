from src.models.board import Board
from src.models.decks.infection_deck import InfectionDeck, Deck
from src.models.decks.player_deck import PlayerDeck
from src.models.player import Player
import pygame


class Game:
    def __init__(self):
        self.board = Board()
        self.player_count = 0
        self.difficulty = ""
        # NUMBER OF REMAINING CUBES AND WHETHER THE DISEASES ARE CURED
        self.disease_info: dict[str: (int, bool)] = {
            "Red": (24, False),
            "Blue": (24, False),
            "Yellow": (24, False),
            "Black": (24, False)
        }
        self.research_station_count = 7
        self.player_deck = None
        self.players_discard_pile = None
        self.infection_deck = None
        self.infection_discard_pile = None
        self.players = pygame.sprite.Group()

    def setup(self):
        # CREATING THE CITY GRAPH IN THE BOARD
        self.setup_board()

        # CREATING THE DECKS
        self.setup_decks()

        # FIRST INFECTIONS OF 9 CITIES
        self.initial_infection()

        # DEALING CARDS TO ALL THE PLAYERS
        self.initial_draw()

    def setup_board(self):
        self.board.add_cities()
        self.board.add_connections()

    def setup_decks(self):
        self.player_deck = PlayerDeck(self.board.cities)
        self.players_discard_pile = Deck()
        self.player_deck.shuffle()

        self.infection_deck = InfectionDeck(self.board.cities)
        self.infection_discard_pile = Deck()
        self.infection_deck.shuffle()

    def initial_infection(self):
        target_cities = self.infection_deck.get_cards(9)
        self.infection_deck.remove_top_cards(9)
        self.infection_discard_pile.add_cards(target_cities)

        for i in range(9):
            city_color = self.board.cities[target_cities[i]].color
            diseases = 3 if i < 3 else (2 if i < 6 else 1)
            self.board.cities[target_cities[i]].add_diseases(diseases, city_color)

    def initial_draw(self):

        n = 4 if int(self.player_count) == 2 else (3 if int(self.player_count) == 3 else 2)

        for player in self.players:
            drawn_cards = self.player_deck.get_cards(n)

            player.draw([city for city in drawn_cards])
            self.player_deck.remove_top_cards(n)
            self.players_discard_pile.add_cards(drawn_cards)

            print(player)
            print(self.player_deck)

    def move_player_to_destination(self, player: Player, city_name: str):
        target_city = self.board.cities[city_name]
        player.move(target_city.x, target_city.y, city_name)

    def build_research_station(self, player: Player, city_name: str):
        self.board.cities[city_name].has_research_station = True
        player.moves -= 1

    def treat(self, player: Player, number: int,  color: str):
        self.board.cities[player.city].remove_diseases(number, color)
        player.moves -= 1
