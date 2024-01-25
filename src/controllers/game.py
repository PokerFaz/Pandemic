from src.models.board import Board
from src.models.decks.infection_deck import InfectionDeck, Deck
from src.models.decks.player_deck import PlayerDeck
from src.models.player import Player
from pygame.sprite import Group
from src.misc.utility import from_color_to_str


class Game:
    def __init__(self):
        self.board = Board()
        self.player_count = 0
        self.difficulty = ""
        # NUMBER OF REMAINING CUBES AND WHETHER THE DISEASES ARE CURED / ERADICATED
        self.disease_info: dict[str, list[int | bool]] = {
            "Red": [24, False, False],
            "Blue": [24, False, False],
            "Yellow": [24, False, False],
            "Black": [24, False, False]
        }
        self.research_station_count = 5
        self.player_deck: PlayerDeck = PlayerDeck({})
        self.players_discard_pile: PlayerDeck = PlayerDeck({})
        self.infection_deck: InfectionDeck = InfectionDeck({})
        self.infection_discard_pile: InfectionDeck = InfectionDeck({})
        self.current_player: Player = Player()
        self.players = Group()

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
        self.infection_discard_pile.add_cards(target_cities)

        for i in range(9):
            city_color = from_color_to_str(self.board.cities[target_cities[i].name].color)
            diseases = 3 if i < 3 else (2 if i < 6 else 1)
            self.board.cities[target_cities[i].name].add_diseases(diseases, city_color)
            self.disease_info[city_color][0] -= diseases

    def initial_draw(self):

        n = 4 if int(self.player_count) == 2 else (3 if int(self.player_count) == 3 else 2)
        pp
        for player in self.players:
            drawn_cards = self.player_deck.get_cards(n)

            player.draw([city.name for city in drawn_cards])
            self.players_discard_pile.add_cards(drawn_cards)

            print(player)
            print(self.player_deck)

    def get_player(self, name: str) -> Player | None:
        for player in self.players:
            if player.name == name:
                return player
        return None

    def more_than_one_person_in_city(self, city_name: str) -> bool:
        return sum(1 for player in self.players if player.city == city_name) > 1

    def is_disease_cured(self, color: str) -> bool:
        return self.disease_info[color][1]

    def can_drive(self, player_city: str, target_city: str | None) -> bool:
        return (target_city is not None and
                self.board.graph.has_edge(player_city, target_city) and
                target_city != player_city)

    def can_shuttle(self, player_city: str, target_city: str | None) -> bool:
        return (target_city is not None and
                self.board.cities[target_city].has_research_station_ and
                player_city != target_city)

    def move(self, target_city_name: str, movement: str):
        target_city = self.board.cities.get(target_city_name, None)
        can_move = False

        match movement:
            case "basic":
                if self.can_drive(self.current_player.city, target_city_name) or self.can_shuttle(self.current_player.city, target_city_name):
                    can_move = True
            case "direct" | "charter":
                if self.current_player.city != target_city_name:
                    can_move = True

        if can_move:
            self.current_player.move(target_city.x, target_city.y, target_city_name)

    def add_research_station(self):
        self.research_station_count += 1

    def build_research_station(self, city_name: str):
        self.board.cities[city_name].has_research_station_ = True
        self.current_player.moves -= 1
        self.research_station_count -= 1

    def calculate_diseases_to_remove(self, color: str) -> int:
        is_disease_cured = self.disease_info[color][1]
        if is_disease_cured:
            return 3

        return 1

    def treat(self, color: str):
        to_remove = self.calculate_diseases_to_remove(color)
        self.board.cities[self.current_player.city].remove_diseases(to_remove, color)
        self.disease_info[color][0] += to_remove
        self.current_player.moves -= 1

        print(self.disease_info)

    def cure(self, color: str):
        self.disease_info[color][1] = True
        print(f"Cured {color}")
        self.current_player.moves -= 1

        print(self.disease_info)

    def share(self, other_player: Player, action: str):

        if action == "Give":
            self.current_player.cards.remove(self.current_player.city)
            other_player.cards.append(self.current_player.city)
        else:
            self.current_player.cards.append(self.current_player.city)
            other_player.cards.remove(self.current_player.city)

        self.current_player.moves -= 1

    def end_turn(self):
        self.current_player.replenish_moves()

        drawn_cards = self.player_deck.get_cards(2)
        self.current_player.draw([city.name for city in drawn_cards])



