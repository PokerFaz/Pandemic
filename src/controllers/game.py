from pygame.sprite import Group
from collections import deque
from typing import Deque
from src.models.board import Board
from src.models.decks.game_decks import GameDecks
from src.models.player import Player
from src.models.card import EventCard, CityCard
from src.models.city import City
from src.misc.utility import from_color_to_str
from src.misc.constants import NUMBER_OF_INFECTION_RATE_MARKERS


class Game:
    def __init__(self):
        """
        Initializes the game

        Attributes:
         - board (Board): The game board
        - player_count (int): The number of players in the game
        - difficulty (str): The difficulty of the game
        - disease_info (dict[str, list[int | bool]]): A dictionary containing information about diseases in the game
        It maps disease colors to lists containing:
            - The number of remaining disease cubes
            - Whether the disease is cured
            - Whether the disease is eradicated
        - research_station_count (int): The current number of research stations available in the game
        - decks (GameDecks): Decks used in the game:
                - player deck
                - infection deck
                - their respective discard piles
        - current_player (Player): The player whose turn it currently is
        - players (Group[Player]): All players in the game
        - skip_next_infection_step (bool): Indicates whether the next infection step should be skipped
        """

        self.board = Board()
        self.player_count = 0
        self.difficulty = ""
        self.disease_info: dict[str, list[int | bool]] = {
            "Red": [24, False, False],
            "Blue": [24, False, False],
            "Yellow": [24, False, False],
            "Black": [24, False, False]
        }
        self.research_station_count = 7
        self.decks = GameDecks()
        self.current_player: Player = Player()
        self.players: Group[Player] = Group()
        self.skip_next_infection_step = False

    def setup(self, log: Deque[str]):
        """
        Prepares the game

        :param log: logging the actions
        :return: nothing
        """

        # CREATING THE CITY GRAPH IN THE BOARD
        self.setup_board()

        # CREATING THE DECKS
        self.setup_decks()

        # FIRST INFECTIONS OF 9 CITIES
        self.initial_infection(log)

        # DEALING CARDS TO ALL THE PLAYERS
        self.initial_draw(log)

        # ADD THE EPIDEMIC CARDS
        self.decks.prepare_player_deck(self.difficulty)
        print(self.decks.infection_deck)

    def setup_board(self):
        """
        Prepares the board

        :return: nothing
        """

        self.board.add_cities()
        self.board.add_connections()

    def setup_decks(self):
        """
        Prepares the decks

        :return: nothing
        """

        self.decks.setup(self.board.cities)

    def infect(self, target_city: City, color: str, number: int, log: Deque[str]):
        """
        Infects a city with a specified number of disease cubes of a given color if not protected

        :param target_city: target city
        :param color: color of the infection
        :param number: number of added cubes
        :param log: logging the information
        :return: nothing
        """

        if target_city.is_protected or self.is_protected_by_medic(target_city, color):
            log.append(f"{target_city.name} was protected")
        elif self.is_disease_eradicated(color):
            log.append(f"{color} disease is eradicated, cant place diseases")
        else:
            had_outbreak = target_city.add_diseases(number, color)
            if not had_outbreak:
                log.append(f"Added {number} {color} {'cube' if number == 1 else 'cubes'} in {target_city.name}")
                self.disease_info[color][0] -= number
            else:
                log.append(f"Outbreak happened in {target_city.name}")
                self.start_outbreak(target_city.name, color)

    def initial_infection(self, log: Deque[str]):
        """
        The starting infection of 9 cities

        :param log: logging the information
        :return: nothing
        """

        target_cities = self.decks.infection_deck.top_n_cards(9)
        reversed_cards = target_cities
        reversed_cards.reverse()
        self.decks.infection_discard_pile.add_cards(reversed_cards)

        for i in range(9):
            city_color = from_color_to_str(self.board.cities[target_cities[i].name].color)
            diseases = 3 if i < 3 else (2 if i < 6 else 1)
            self.board.cities[target_cities[i].name].add_diseases(diseases, city_color)
            log.append(f"Added {diseases} {'cube' if diseases == 1 else 'cubes'} in {target_cities[i].name}")
            self.disease_info[city_color][0] -= diseases

    def initial_draw(self, log: Deque[str]):
        """
        Initial draw of all players. The number of cards depends on the number of players

        :param log: logging the information
        :return: nothing
        """

        n = 4 if int(self.player_count) == 2 else (3 if int(self.player_count) == 3 else 2)
        n=7
        for player in self.players:
            drawn_cards = self.decks.player_deck.top_n_cards(n)
            log.append(f"{player.name} drew {[card.name for card in drawn_cards]}")

            player.draw([city for city in drawn_cards])

    def get_player(self, name: str) -> Player | None:
        """
        Gets the player object from the name

        :param name: player's name
        :return: the player as an object or nothing if they don't exist
        """

        for player in self.players:
            if player.name == name:
                return player
        return None

    def more_than_one_person_in_city(self, city_name: str) -> bool:
        """
        Checks if there is more than one person in a given city

        :param city_name: the name of the city
        :return: true if there is more else false
        """

        return sum(1 for player in self.players if player.location == city_name) > 1

    def is_disease_cured(self, color: str) -> bool:
        """
        Gets the cure status of a disease

        :param color: the disease to be checked
        :return: true if it is cured else false
        """

        return self.disease_info[color][1]

    def is_disease_eradicated(self, color: str) -> bool:
        """
        Gets the eradicated status of a disease

        :param color: the disease to be checked
        :return: true if it is eradicated else false
        """

        return self.disease_info[color][2]

    def is_protected_by_medic(self, city: City, color: str) -> bool:
        """
        Checks for protection by medic. The city is protected if the medic is on the city
        and the city is cured

        :param city: city object to be checked
        :param color: disease to be checked
        :return: true if it is protected else false
        """

        medic = self.get_player("Medic")
        if medic is None:
            return False
        else:
            if medic.location == city.name and self.disease_info[color][1] is True:
                return True

        return False

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
        Only possible if both locations have a research station

        :param player_city: current position
        :param target_city: target position
        :return: bool: if it possible or not
        """

        return (target_city is not None and
                self.board.cities[target_city].has_research_station_ and
                player_city != target_city)

    def city_has_player(self, city_name: str) -> bool:
        """
        Checks if a player is on a given city

        :param city_name: the name of the city
        :return: true if there is a player else false
        """

        for player in self.players:
            if player.location == city_name:
                return True

        return False

    def check_for_automatic_treat(self, log: Deque):
        """
        Checks for the medic special ability -> automatic treat.
        If a disease is cured, the medic removes all cubes from the city

        :return: nothing
        """

        for color, (number, is_cured, is_eradicated) in self.disease_info.items():
            if is_cured:
                self.treat(color, log)

    @staticmethod
    def played_action(player: Player):
        """
        Decreases the number of moves for the player by 1

        :param player: The player whose moves are to be decreased
        """

        player.moves -= 1

    def use_card(self, card: EventCard | CityCard):
        """
        Removes the card from the player's hand and adds it to the discard pile

        :param card: the played card
        :return: nothing
        """

        self.current_player.remove_cards(card)
        self.decks.players_discard_pile.add_cards(card)

    def move(self, target_city_name: str, movement: str, log: Deque[str]):
        """
        Moves the current player to the target city, if possible. The different type of movements are:
         - basic: movement done without using any cards
         - direct: movement done by using a card
        The player goes to the name of the card. If they are already there, nothing happens
         - charter: movement done by using a card.
        The player discards a card that has the same name as the position of their pawn
        Moves to the city, chosen by the player

        :param target_city_name: the new position of the player
        :param movement: type of movement
        :param log: for documenting
        """
        save_player = self.current_player

        if hasattr(self.current_player, "link"):
            self.current_player: Player = self.current_player.link

        target_city = self.board.cities.get(target_city_name, None)
        can_move = False

        match movement:
            case "basic":
                if self.can_drive(self.current_player.location, target_city_name) or self.can_shuttle(
                        self.current_player.location, target_city_name) or (
                        save_player.name == "Dispatcher" and self.city_has_player(target_city_name)):
                    can_move = True
            case "direct" | "charter":
                if self.current_player.location != target_city_name:
                    can_move = True

        if can_move:
            if self.current_player.name == "Quarantine Specialist":
                for neighbor in self.board.get_neighbors(self.current_player.location):
                    neighbor.is_protected = False

            self.current_player.move(target_city.x, target_city.y, target_city_name)

            if self.current_player.name == "Medic":
                self.check_for_automatic_treat(log)
            elif self.current_player.name == "Quarantine Specialist":
                for neighbor in self.board.get_neighbors(self.current_player.location):

                    neighbor.is_protected = True

            self.played_action(save_player)
            log.append(f"{self.current_player.name} moved to {target_city_name}")

        self.current_player = save_player

    def add_research_station(self):
        """
        Adds 1 research station

        :return: nothing
        """
        self.research_station_count += 1

    def build_research_station(self, city: City, log: Deque[str]):
        """
        Builds a research station in the given city

        :param city: the city where the research station will be built
        :param log: logging the information
        :return: nothing
        """

        city.has_research_station_ = True
        log.append(f"{city.name} now has a research station")
        self.research_station_count -= 1

    def calculate_diseases_to_remove(self, color: str) -> int:
        """
        Returns how much disease cubes should be removed

        :param color: the disease that will be treated
        :return:
        """
        is_disease_cured = self.disease_info[color][1]
        if is_disease_cured:
            return 3
        elif self.current_player.name == "Medic":
            return 3
        return 1

    def treat(self, color: str, log: Deque[str]):
        """
        Treats diseases in the current player's location

        :param color: the disease which will be treated
        :param log: logging the information
        :return: nothing
        """

        to_remove = self.calculate_diseases_to_remove(color)
        player_location = self.current_player.location

        self.board.cities[player_location].remove_diseases(to_remove, color)
        log.append(
            f"{self.current_player.name} treated {to_remove} {color.lower()} {'cube' if to_remove == 1 else 'cubes'} in {player_location}")
        self.disease_info[color][0] += to_remove

        if self.disease_info[color][0] == 24 and self.is_disease_cured(color):
            self.disease_info[color][2] = True

        self.played_action(self.current_player)

    def cure(self, color: str, log: Deque[str]):
        """
        Cures a disease

        :param color: the disease to be cured
        :param log: logging the information
        :return: nothing
        """

        self.disease_info[color][1] = True
        log.append(f"{color} is cured")
        self.played_action(self.current_player)

    def share(self, card: CityCard | None, other_player: Player, action: str, log: Deque[str]):
        """
        Performs the share action which is where two players share a card

        :param card: the card that will be shared
        :param other_player: the other participant in the share
        :param action: Give or Take
        if it is Give -> current player gives to the other one
        if it is Take -> the other player gives to the current one
        :param log: logging the information
        :return: nothing
        """

        if card is None:
            card = next((player_card for player_card in self.current_player.cards if
                         player_card.name == self.current_player.location), None)

        if card is not None:
            if action == "Give":
                self.current_player.cards.remove(card)
                other_player.cards.append(card)

                log.append(f"{self.current_player.name} gave {other_player.name} {self.current_player.location}")
            else:
                self.current_player.cards.append(card)
                other_player.cards.remove(card)

                log.append(f"{self.current_player.name} took from {other_player.name} {self.current_player.location}")

            self.played_action(self.current_player)

    def increase_infection_marker(self):
        """
        Increases the marker by 1

        :return: nothing
        """

        self.board.infection_rate_counter += 1

    def resolve_epidemic_card(self, log: Deque[str]):
        """
        Resolves the epidemic card. There are 3 stages:
        1) Increases infection marker
        2) Puts 3 disease cubes in the city that is at the bottom of the infection deck
        3) Shuffles the infection discard deck and places it on top of the infection deck

        :param log: logging the information
        :return: nothing
        """

        self.increase_infection_marker()
        log.append(f"Infection marker increased to: {self.board.infection_rate_counter}")

        card = self.decks.infection_deck.get_bottom_card()
        to_be_infected_city = self.board.cities[card.name]
        color = from_color_to_str(to_be_infected_city.color)
        self.infect(to_be_infected_city, color, 3, log)

        self.decks.infection_discard_pile.add_cards([card])

        self.decks.infection_discard_pile.shuffle()
        self.decks.infection_deck.add_to_front([card for card in self.decks.infection_discard_pile])
        self.decks.infection_discard_pile.deck.clear()

    def skip(self):
        """
        Player skips his turn

        :return: nothing
        """

        self.current_player.moves = 0

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
        cities_that_had_outbreak = [city_name]

        while to_outbreak:
            self.board.outbreaks_counter += 1
            current_city = to_outbreak.popleft()

            for neighbor in self.board.get_neighbors(current_city):
                if not (neighbor.name in cities_that_had_outbreak or
                        neighbor.is_protected or
                        self.is_disease_eradicated(from_color_to_str(neighbor.color))):
                    had_outbreak = neighbor.add_diseases(1, color)
                    self.disease_info[color][0] -= 1
                    if had_outbreak:
                        to_outbreak.append(neighbor.name)
                        cities_that_had_outbreak.append(neighbor)

    def did_win(self) -> bool:
        """
        Checks if the players won. Players win if all diseases are cured

        :return: returns true if all are cured else false
        """

        return all(disease_state[1] for disease_state in self.disease_info.values())

    def did_lose(self) -> bool:
        """
        Checks if one of these conditions is met:
        1) the infection marker is above 7
        2) the cubes of a disease ran out
        3) the player cant draw 2 cards after ending his turn

        :return: true if one of the aforementioned conditions is met else false
        """

        did_lose = False
        if (self.board.outbreaks_counter > NUMBER_OF_INFECTION_RATE_MARKERS or
                any(True for disease_state in self.disease_info.values() if disease_state[0] <= 0) or
                len(self.decks.player_deck) < 2):
            did_lose = True

        return did_lose
