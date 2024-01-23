import pygame
import networkx
from src.models.buttons.text_button import TextButton
from src.models.buttons.image_button import ImageButton
from src.models.city import from_str_to_color
from src.models.city import City
from src.misc import constants as c
from src.models.buttons.button import Button
from src.models.player import Player
from src.misc.images import background
from src.controllers.game import Game
from src.misc.button_factory import ButtonFactory
from src.models.board import Board


def iterate_diseases(city_diseases):
    for color, number in city_diseases.items():
        if number > 0:
            yield number, color


def write(screen, text, text_size, x, y, color=c.RED, has_background=False):
    font = pygame.font.Font(None, text_size)
    text = font.render(text, True, color, c.WHITE if has_background else None)
    screen.blit(text, (x, y))


def display_image(screen, image, coordinates):
    screen.blit(image, coordinates)


class GUI:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.action_menu_open = False
        self.action_button_list = []

    @staticmethod
    def get_next_input() -> (int, int):
        while True:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return mouse_x, mouse_y

    def display_diseases(self, city: City):
        try:
            iterator = iterate_diseases(city.diseases)

            number, color = next(iterator)
            write(self.screen, str(number), 40, city.x - 30, city.y - 15,
                  from_str_to_color(color) if color != "Yellow" else c.DARK_YELLOW)

            number, color = next(iterator)
            write(self.screen, str(number), 40, city.x + 10, city.y - 15,
                  from_str_to_color(color) if color != "Yellow" else c.DARK_YELLOW)

            number, color = next(iterator)
            write(self.screen, str(number), 40, city.x - 50, city.y - 15,
                  from_str_to_color(color) if color != "Yellow" else c.DARK_YELLOW)

        except StopIteration:
            pass

    def display_connecting_lines(self, edges: networkx.classes.reportviews.EdgeView, cities: dict[str: City]):
        for city1, city2 in edges:
            if city1 == "San Francisco" and city2 == "Tokyo":
                pygame.draw.line(self.screen, c.BLACK, (cities[city1].x, cities[city1].y),
                                 (0, 200), 2)
                pygame.draw.line(self.screen, c.BLACK, (cities[city2].x, cities[city2].y),
                                 (1500, 251), 2)
            elif city1 == "San Francisco" and city2 == "Manila":
                pygame.draw.line(self.screen, c.BLACK, (cities[city1].x, cities[city1].y),
                                 (0, 300), 2)
                pygame.draw.line(self.screen, c.BLACK, (cities[city2].x, cities[city2].y),
                                 (1500, 420), 2)
            elif city1 == "Los Angeles" and city2 == "Sydney":
                pygame.draw.line(self.screen, c.BLACK, (cities[city1].x, cities[city1].y),
                                 (0, 362), 2)
                pygame.draw.line(self.screen, c.BLACK, (cities[city2].x, cities[city2].y),
                                 (1500, 630), 2)
            else:
                pygame.draw.line(self.screen, c.BLACK, (cities[city1].x, cities[city1].y),
                                 (cities[city2].x, cities[city2].y), 2)

    def display_cities(self, cities: dict):
        radius = c.RADIUS_OF_CIRCLE
        for key in cities:
            city = cities[key]
            center = (city.x, city.y)
            pygame.draw.circle(self.screen, city.color, center, radius)
            write(self.screen, f"{city.name}", 25,
                  city.x - 15 if city.name not in ("Ho Chi Minh City", "Istanbul") else city.x - 60,
                  city.y + 15, c.GRAY if not city.has_research_station else c.BLACK, True)
            self.display_diseases(city)

    def display_outbreaks(self, outbreaks_counter: int):
        write(self.screen, "Outbreaks:", 43, 20, 500, c.BLACK)

        write(self.screen, f"{outbreaks_counter}", 43, 187, 503, c.GREEN)

    def display_infection_rate(self, outbreaks_counter: int):
        write(self.screen, "Infection rate", 50, 1170, 30, c.BLACK)

        counter = 0
        x = 1100
        y = 100

        while counter < 7:
            pygame.draw.circle(self.screen, c.DARK_GREEN if counter == outbreaks_counter else c.GREEN,
                               (x, y), c.RADIUS_OF_CIRCLE)

            if counter in range(0, 3):
                write(self.screen, "2", 30, x - 5, y + 20, c.BLACK)
            elif counter in range(3, 5):
                write(self.screen, "3", 30, x - 5, y + 20, c.BLUE)
            else:
                write(self.screen, "4", 30, x - 5, y + 20, c.RED)

            counter += 1
            x += 60

    def display_action_tab_opener(self):
        pygame.draw.rect(self.screen, c.GRAY, (0, 780, 1500, 20), border_top_left_radius=5, border_top_right_radius=5)

    def display_board(self, board: Board):
        display_image(self.screen, background, (0, 0))

        self.display_connecting_lines(board.graph.edges, board.cities)
        self.display_cities(board.cities)
        self.display_outbreaks(board.outbreaks_counter)
        self.display_infection_rate(board.infection_rate_counter)
        self.display_action_tab_opener()

    def display_action_menu(self):
        self.action_menu_open = True

        # STACKOVERFLOW CODE FOR TRANSPARENT RECT
        action_menu = pygame.Surface((1500, 260), pygame.SRCALPHA)
        action_menu.fill((128, 128, 128, 220))
        self.screen.blit(action_menu, (0, 540))

    def display_action_icons(self):
        for button in self.action_button_list:
            button.display_button(self.screen)

        write(self.screen, "Hand", 40, 320, 710, c.BLACK)
        write(self.screen, "Build", 40, 530, 710, c.BLACK)
        write(self.screen, "Treat", 40, 755, 710, c.BLACK)

    def display_current_board_position(self, current_player: Player, players: pygame.sprite.Group, board: Board):
        self.display_board(board)
        self.screen.blit(current_player.image, (20, 20))
        write(self.screen, f"{current_player.moves}", 60, 70, 20)
        players.draw(self.screen)

    def display_player_hand(self, card_buttons: [Button]):
        self.display_action_menu()

        for button in card_buttons:
            button.display_button(self.screen)

    def display_disease_choices(self, available_choices: list[TextButton]):
        self.display_action_menu()
        write(self.screen, "Pick what disease you want to treat", 50, c.WIDTH / 3.2, 580)

        for index in range(len(available_choices)):
            rectangle_color = from_str_to_color(available_choices[index].info)
            available_choices[index].display_button(self.screen, rect_color=rectangle_color, text_color=c.WHITE)

    @staticmethod
    def find_pressed_button(mouse_x: int, mouse_y: int,
                            buttons: list[TextButton | ImageButton]) -> TextButton | ImageButton | None:
        for button in buttons:
            if button.is_clicked(mouse_x, mouse_y):
                return button

        return None

    def handle_hand_screen(self, card_buttons: list[TextButton | Button], action: str,
                           player: Player, game: Game):
        while True:
            mouse_x, mouse_y = self.get_next_input()

            if mouse_y not in range(540, 800):
                self.action_menu_open = False
                self.display_current_board_position(player, game.players, game.board)
                break

            pressed_card_button = self.find_pressed_button(mouse_x, mouse_y, card_buttons)
            if pressed_card_button is not None:
                city_name = pressed_card_button.info
                self.handle_hand_action(city_name, action, player, game)

                self.display_current_board_position(player, game.players, game.board)
                break

    def handle_hand_action(self, city_name: str, action: str, player: Player, game: Game):
        if city_name == player.city and action == "Hand":
            self.display_current_board_position(player, game.players, game.board)
            pygame.display.flip()

            destination = self.get_destination(game.board)
            game.move_player_to_destination(player, destination)
        elif city_name != player.city and action == "Hand":
            game.move_player_to_destination(player, city_name)
        elif city_name == player.city and action == "Build":
            game.build_research_station(player, city_name)

        player.cards.remove(city_name)

    def get_destination(self, board: Board) -> str:
        while True:
            mouse_x, mouse_y = self.get_next_input()
            destination = board.get_city_at_coordinates(mouse_x, mouse_y)

            if destination is not None:
                break

        return destination

    @staticmethod
    def handle_actions_without_menu(board: Board, player: Player, mouse_x: int, mouse_y: int):
        # CHECKING IF THE PLAYER TRIES TO MOVE TO ANOTHER CITY
        chosen_city = board.get_city_at_coordinates(mouse_x, mouse_y)
        if chosen_city is not None and (board.has_edge(chosen_city, player.city)
                                        or board.is_shuttle_flight(player.city, chosen_city)):
            player.move(board.cities[chosen_city].x, board.cities[chosen_city].y, chosen_city)

    def get_chosen_disease(self, buttons: list[TextButton]) -> str | None:
        while True:
            mouse_x, mouse_y = self.get_next_input()

            if mouse_y not in range(540, 800):
                return None

            pressed_button = self.find_pressed_button(mouse_x, mouse_y, buttons)

            if pressed_button is not None:
                return pressed_button.info

    def handle_treat_action(self, game: Game, player: Player, button_factory: ButtonFactory):
        diseases = [(colour, value) for colour, value in
                    game.board.cities[player.city].diseases.items() if
                    value > 0]
        if len(diseases) == 1:
            game.treat(player, 1, diseases[0][0])
            self.display_current_board_position(player, game.players, game.board)

            self.action_menu_open = False
        else:
            self.display_current_board_position(player, game.players, game.board)
            choices = button_factory.create_disease_removal_options_buttons(diseases)
            self.display_disease_choices(choices)

            pygame.display.flip()
            chosen_disease_color = self.get_chosen_disease(choices)

            if chosen_disease_color is not None:
                game.treat(player, 1, chosen_disease_color)

            self.display_current_board_position(player, game.players, game.board)
            self.action_menu_open = False

    def handle_actions_with_menu(self, button_factory: ButtonFactory, game: Game, player: Player, mouse_x: int, mouse_y: int):
        # CHECKING IF THE PLAYER HAS PRESSED AN ACTION BUTTON
        for button in self.action_button_list:
            if button.is_clicked(mouse_x, mouse_y):
                if button.info in ("Hand", "Build"):
                    card_buttons = button_factory.create_city_buttons(game.board.cities,
                                                                      player.cards)
                    self.display_player_hand(card_buttons)
                    pygame.display.flip()

                    self.handle_hand_screen(card_buttons, button.info,
                                            player, game)
                    self.action_menu_open = False
                elif button.info == "Treat":
                    self.handle_treat_action(game, player, button_factory)

    def start(self, game: Game, button_factory: ButtonFactory):
        run = True
        while run:
            # PLAYERS TURN
            for player in game.players:
                self.display_current_board_position(player, game.players, game.board)

                while player.moves > 0:
                    pygame.display.flip()

                    mouse_x, mouse_y = self.get_next_input()

                    # ACTIONS POSSIBLE WITH MENU OFF
                    if self.action_menu_open is False:
                        if mouse_y in range(780, 800):
                            self.display_action_menu()
                            self.display_action_icons()
                        else:
                            self.handle_actions_without_menu(game.board, player, mouse_x, mouse_y)
                            self.display_current_board_position(player, game.players, game.board)
                    # ACTIONS POSSIBLE WITH MENU ON
                    else:
                        # CLOSING THE MENU
                        if mouse_y not in range(540, 800):
                            self.action_menu_open = False
                            self.display_current_board_position(player, game.players, game.board)
                        else:
                            self.handle_actions_with_menu(button_factory, game, player, mouse_x, mouse_y)

                player.replenish_moves()

        pygame.quit()
