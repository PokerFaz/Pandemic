from src.models.board import Board
from src.models.decks.infection_deck import InfectionDeck, Deck
from src.models.decks.player_deck import PlayerDeck
from src.gui.gui import GUI
from src.misc.button_factory import ButtonFactory
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

    def start_loop(self, game_gui: GUI, button_factory: ButtonFactory):
        run = True
        while run:
            # PLAYERS TURN
            for player in self.players:
                game_gui.display_current_board_position(player, self.players)
                while player.moves > 0:
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False

                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # ACTIONS POSSIBLE WITH MENU OFF
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_gui.action_menu_open is False:

                            # CHECKING TO SEE IF THE PLAYER TRIES TO OPEN THE ACTION MENU
                            if mouse_y in range(780, 800):
                                game_gui.display_action_menu()
                                game_gui.display_action_icons()

                                pygame.display.flip()
                            else:
                                # CHECKING IF THE PLAYER TRIES TO MOVE TO ANOTHER CITY
                                chosen_city = self.board.get_city_at_coordinates(mouse_x, mouse_y)
                                print(chosen_city)
                                if chosen_city is not None and (self.board.has_edge(chosen_city, player.city)
                                                                or (self.board.cities[chosen_city].has_research_station
                                                                    and self.board.cities[player.city].has_research_station)):
                                    player.move(self.board.cities[chosen_city].x, self.board.cities[chosen_city].y, chosen_city)
                                    game_gui.display_current_board_position(player, self.players)
                                    break

                        # ACTIONS POSSIBLE WITH MENU ON
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_gui.action_menu_open is True:

                            # CLOSING THE MENU
                            if mouse_y not in range(540, 800):
                                game_gui.action_menu_open = False
                                game_gui.display_current_board_position(player, self.players)
                                pygame.display.flip()
                            else:
                                # CHECKING IF THE PLAYER HAS PRESSED AN ACTION BUTTON
                                for button in game_gui.action_button_list:
                                    if button.is_clicked(mouse_x, mouse_y):
                                        if button.info == "Hand" or button.info == "Build":
                                            card_buttons = button_factory.create_city_buttons(self.board.cities,
                                                                                              player.cards)
                                            game_gui.display_player_hand(card_buttons)
                                            game_gui.handle_button_action(card_buttons, button.info, player, self.players)
                                            game_gui.action_menu_open = False
                                        elif button.info == "Treat":
                                            diseases = [(colour, value) for colour, value in
                                                        self.board.cities[player.city].diseases.items() if value > 0]
                                            if len(diseases) == 1:
                                                self.board.cities[player.city].remove_diseases(1, diseases[0][0])
                                                player.moves -= 1
                                                game_gui.display_current_board_position(player, self.players)

                                                game_gui.action_menu_open = False

                                            else:
                                                game_gui.display_current_board_position(player, self.players)
                                                choices = button_factory.create_disease_removal_options_buttons(
                                                    diseases)
                                                game_gui.display_disease_choices(choices)

                                                pygame.display.flip()
                                                mouse_x, mouse_y = game_gui.get_next_input()

                                                pressed_button = game_gui.find_pressed_button(mouse_x, mouse_y, choices)

                                                if mouse_y not in range(540, 800):
                                                    game_gui.action_menu_open = False
                                                    game_gui.display_current_board_position(player, self.players)
                                                    pygame.display.flip()
                                                    break

                                                while pressed_button is None:
                                                    mouse_x, mouse_y = game_gui.get_next_input()

                                                    if mouse_y not in range(540, 800):
                                                        game_gui.action_menu_open = False
                                                        game_gui.display_current_board_position(player, self.players)
                                                        pygame.display.flip()
                                                        break

                                                    pressed_button = game_gui.find_pressed_button(mouse_x, mouse_y,
                                                                                                  choices)
                                                if pressed_button is not None:
                                                    player.moves -= 1
                                                    self.board.cities[player.city].remove_diseases(1, pressed_button.info)

                                                    game_gui.display_current_board_position(player, self.players)

                                                    game_gui.action_menu_open = False

                player.replenish_moves()

        pygame.quit()
