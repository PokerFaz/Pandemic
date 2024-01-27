from src.models.board import Board
from src.models.card import EpidemicCard
from src.models.decks.infection_deck import InfectionDeck, Deck
from src.models.decks.player_deck import PlayerDeck
from src.models.player import Player
from pygame.sprite import Group
from src.misc.utility import from_color_to_str
from src.models.city import City
from collections import deque
from typing import Deque


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
        self.research_station_count = 2
        self.player_deck: PlayerDeck = PlayerDeck({})
        self.players_discard_pile: PlayerDeck = PlayerDeck({})
        self.infection_deck: InfectionDeck = InfectionDeck({})
        self.infection_discard_pile: InfectionDeck = InfectionDeck({})
        self.current_player: Player = Player()
        self.players = Group()

    def setup(self, log: Deque[str]):
        # CREATING THE CITY GRAPH IN THE BOARD
        self.setup_board()

        # CREATING THE DECKS
        self.setup_decks()

        # FIRST INFECTIONS OF 9 CITIES
        self.initial_infection(log)

        # DEALING CARDS TO ALL THE PLAYERS
        self.initial_draw(log)

        # ADD THE EPIDEMIC CARDS
        self.player_deck.prepare_deck(self.difficulty)

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

    def infect(self, target_city: City, color: str, number: int, log: Deque[str]):
        had_outbreak = target_city.add_diseases(number, color)
        if not had_outbreak:
            log.append(f"Added {number} {color} {'cube' if number == 1 else 'cubes'} in {target_city.name}")
            self.disease_info[color][0] -= number
        else:
            log.append(f"Outbreak happened in {target_city.name}")
            self.start_outbreak(target_city.name, color)

    def initial_infection(self, log: Deque[str]):
        target_cities = self.infection_deck.top_n_cards(9)
        self.infection_discard_pile.add_cards(target_cities)

        for i in range(9):
            city_color = from_color_to_str(self.board.cities[target_cities[i].name].color)
            diseases = 3 if i < 3 else (2 if i < 6 else 1)
            self.board.cities[target_cities[i].name].add_diseases(diseases, city_color)
            log.append(f"Added {diseases} {'cube' if diseases == 1 else 'cubes'} in {target_cities[i].name}")
            self.disease_info[city_color][0] -= diseases

    def initial_draw(self, log: Deque[str]):

        n = 4 if int(self.player_count) == 2 else (3 if int(self.player_count) == 3 else 2)

        for player in self.players:
            drawn_cards = self.player_deck.get_cards(n)
            log.append(f"{player.name} drew {[card.name for card in drawn_cards]}")

            player.draw([city for city in drawn_cards])
            self.players_discard_pile.add_cards(drawn_cards)

    def get_player(self, name: str) -> Player | None:
        for player in self.players:
            if player.name == name:
                return player
        return None

    def more_than_one_person_in_city(self, city_name: str) -> bool:
        return sum(1 for player in self.players if player.location == city_name) > 1

    def is_disease_cured(self, color: str) -> bool:
        return self.disease_info[color][1]

    def can_drive(self, player_city: str, target_city: str | None) -> bool:
        """
        Checks if the player can move to a city. Returns True if the cities are connected

        :param player_city: current position
        :param target_city: target position
        :return: bool: if it is possible or not
        """
        return (target_city is not None and
                self.board.graph.has_edge(player_city, target_city) and
                target_city != player_city)

    def can_shuttle(self, player_city: str, target_city: str | None) -> bool:
        """
        Checks if the player can move to a city.
        Only possible if both locations have a research station.

        :param player_city: current position
        :param target_city: target position
        :return: bool: if it possible or not
        """
        return (target_city is not None and
                self.board.cities[target_city].has_research_station_ and
                player_city != target_city)

    def move(self, target_city_name: str, movement: str, log: Deque[str]):
        """
        Moves the player to the target city, if possible. The different type of movements are:
        - basic: movement done without using any cards
        - direct: movement done by using a card.
            The player goes to the name of the card. If they are already there, nothing happens
        - charter: movement done by using a card.
            The player discards a card that has the same name as the position of their pawn.
            Moves to the city, chosen by the player

        :param target_city_name: the new position of the player
        :param movement: type of movement
        :param log: for documenting
        """
        target_city = self.board.cities.get(target_city_name, None)
        can_move = False

        match movement:
            case "basic":
                if self.can_drive(self.current_player.location, target_city_name) or self.can_shuttle(
                        self.current_player.location, target_city_name):
                    can_move = True
            case "direct" | "charter":
                if self.current_player.location != target_city_name:
                    can_move = True

        if can_move:
            self.current_player.move(target_city.x, target_city.y, target_city_name)
            log.append(f"{self.current_player.name} moved to {target_city_name}")

    def add_research_station(self):
        self.research_station_count += 1

    def build_research_station(self, city: City, log: Deque[str]):
        city.has_research_station_ = True
        log.append(f"{city.name} now has a research station")
        self.current_player.moves -= 1
        self.research_station_count -= 1

    def calculate_diseases_to_remove(self, color: str) -> int:
        is_disease_cured = self.disease_info[color][1]
        if is_disease_cured:
            return 3

        return 1

    def treat(self, color: str, log: Deque[str]):
        to_remove = self.calculate_diseases_to_remove(color)
        player_location = self.current_player.location

        self.board.cities[player_location].remove_diseases(to_remove, color)
        log.append(
            f"{self.current_player.name} treated {to_remove} {color.lower()} {'cube' if to_remove == 1 else 'cubes'} in {player_location}")
        self.disease_info[color][0] += to_remove
        self.current_player.moves -= 1

    def cure(self, color: str, log: Deque[str]):
        self.disease_info[color][1] = True
        log.append(f"{color} is cured")
        self.current_player.moves -= 1

    def share(self, other_player: Player, action: str, log: Deque[str]):

        if action == "Give":
            for card in self.current_player.cards:
                if card.name == self.current_player.location:
                    self.current_player.cards.remove(card)
                    other_player.cards.append(card)

            log.append(f"{self.current_player.name} gave {other_player.name} {self.current_player.location}")
        else:
            for card in other_player.cards:
                if card.name == self.current_player.location:
                    self.current_player.cards.append(card)
                    other_player.cards.remove(card)

            log.append(f"{self.current_player.name} took from {other_player.name} {self.current_player.location}")

        self.current_player.moves -= 1

    def increase_infection_marker(self):
        self.board.infection_rate_counter += 1

    def resolve_epidemic_card(self, log: Deque[str]):
        self.increase_infection_marker()
        log.append(f"Infection marker increased to: {self.board.infection_rate_counter}")

        card = self.infection_deck.get_bottom_card()
        to_be_infected_city = self.board.cities[card.name]
        color = from_color_to_str(to_be_infected_city.color)
        self.infect(to_be_infected_city, color, 3, log)

        self.infection_discard_pile.add_cards([card])

        print(f"DISCARD {self.infection_discard_pile}")

        self.infection_discard_pile.shuffle()
        self.infection_deck.add_to_front([card for card in self.infection_discard_pile])
        self.infection_discard_pile.deck.clear()

        print(f"DECK {self.infection_deck}")

    def skip(self):
        self.current_player.moves = 0

    def end_turn(self, log: Deque[str]):
        self.current_player.replenish_moves()

        drawn_cards = self.player_deck.get_cards(2)
        log.append(f"{self.current_player.name} drew {[card.name for card in drawn_cards]}")

        for card in drawn_cards:
            if isinstance(card, EpidemicCard):
                log.append(f"Resolving epidemic card:")
                self.resolve_epidemic_card(log)
                drawn_cards.remove(card)
            else:
                self.current_player.draw([card])

        counter = self.board.infection_rate_counter
        cards_to_take = 2 if counter < 3 else (3 if counter < 5 else 4)
        drawn_cards = self.infection_deck.top_n_cards(cards_to_take)

        for card in drawn_cards:
            target_city = self.board.cities[card.name]
            self.infect(target_city, from_color_to_str(target_city.color), 1, log)

    def start_outbreak(self, city_name: str, color: str):
        """
        Simulates the spread of outbreaks.

        How it works: it starts with the initial city and adds it to a deque. While this deque has an element
        we get the leftmost element and get its neighbours without repeating cities. If the neighbor starts
        an outbreak we add it to the deque. For each new outbreak we increase the outbreak counter

        :param city_name: starting outbreak city
        :param color: the color of the disease

        """
        to_outbreak: Deque[str] = deque([city_name])
        had_an_outbreak = [city_name]

        while to_outbreak:
            self.board.outbreaks_counter += 1
            current_city = to_outbreak.popleft()
            for neighbor in self.board.graph.neighbors(current_city):
                if neighbor not in had_an_outbreak:
                    had_outbreak = self.board.cities[neighbor].add_diseases(1, color)
                    if had_outbreak:
                        to_outbreak.append(neighbor)
                        had_an_outbreak.append(neighbor)

    def did_win(self) -> bool:
        return all(disease_state[1] for disease_state in self.disease_info.values())

    def did_lose(self) -> bool:
        did_lose = False
        if self.board.outbreaks_counter > 7 or any(True for disease_state in self.disease_info.values() if disease_state[0] <= 0) or len(self.player_deck) < 2:
            did_lose = True

        return did_lose

    def did_end(self) -> str:
        if self.did_win():
            return "Win"
        elif self.did_lose():
            return "Defeat"

        return "No"
