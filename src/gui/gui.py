import pygame
import networkx
from src.models.buttons.button import Button
from src.models.buttons.text_button import TextButton
from src.models.buttons.image_button import ImageButton
from src.models.city import City
from src.misc import constants as c
from src.models.player import Player
from src.misc.images import background
from src.controllers.game import Game
from src.misc.button_factory import ButtonFactory
from src.models.board import Board
from src.misc.utility import load_image, resize, from_str_to_color, from_color_to_str
from typing import Callable


def iterate_diseases(city_diseases: dict[str, int]):
    for color, number in city_diseases.items():
        if number > 0:
            yield number, color


def write(screen: pygame.Surface, text: str, text_size: int, x: float, y: float, color: c.color = c.RED,
          has_background: bool = False):
    font = pygame.font.Font(None, text_size)
    text = font.render(text, True, color, c.WHITE if has_background else None)
    screen.blit(text, (x, y))


def display_image(screen: pygame.Surface, image: pygame.Surface, coordinates: (int, int)):
    screen.blit(image, coordinates)


def have_the_same_color(cities: dict[str, City], buttons: list[ImageButton]) -> str | None:
    colors = [cities[button.info].color for button in buttons]
    if len(set(colors)) == 1:
        return from_color_to_str(colors[0])

    return None


class GUI:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.action_menu_open = False
        self.action_button_list = []

    @staticmethod
    def get_next_input() -> (float, float):
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

    def display_connecting_lines(self, edges: networkx.classes.reportviews.EdgeView, cities: dict[str, City]):
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

    def display_cities(self, cities: dict[str, City]):
        radius = c.RADIUS_OF_CIRCLE
        for key in cities:
            city = cities[key]
            center = (city.x, city.y)
            pygame.draw.circle(self.screen, city.color, center, radius)
            write(self.screen, f"{city.name}", 25,
                  city.x - 15 if city.name not in ("Ho Chi Minh City", "Istanbul") else city.x - 60,
                  city.y + 15, c.GRAY if not city.has_research_station_ else c.BLACK, True)
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

    def display_action_menu(self, height: float = 260):
        self.action_menu_open = True

        # STACKOVERFLOW CODE FOR TRANSPARENT RECT
        action_menu = pygame.Surface((c.WIDTH, height), pygame.SRCALPHA)
        action_menu.fill((128, 128, 128, 220))
        self.screen.blit(action_menu, (0, c.HEIGHT - height))

    def display_contents_on_menu_screen(self, buttons: list[Button],
                                        modifications: dict[str, tuple[c.color, c.color] | bool],
                                        texts: list[tuple[str, int, float, float, c.color]] = ()):
        for button in buttons:
            if isinstance(button, TextButton) and button.info in modifications.keys():
                button.display_button(self.screen, rect_color=modifications[button.info][0],
                                      text_color=modifications[button.info][1])
            elif button:
                button.display_button(self.screen)
                if isinstance(button, ImageButton) and modifications.get(button.info, False):
                    self.highlight_buttons(button)

        for text in texts:
            if text:
                write(self.screen, *text)

    def display_current_board_position(self, game: Game):
        self.display_board(game.board)
        self.screen.blit(game.current_player.image, (20, 20))
        write(self.screen, f"{game.current_player.moves}", 60, 70, 20)
        game.players.draw(self.screen)

    def display_buttons(self, card_buttons: [Button]):
        for button in card_buttons:
            button.display_button(self.screen)

    def display_cure_menu(self, buttons: list[Button],
                          modifications: dict[str, tuple[c.color, c.color] | bool]):
        self.display_action_menu()
        self.display_contents_on_menu_screen(buttons, modifications)

    @staticmethod
    def display_player_hand(screen: pygame.Surface, cards: list[pygame.Surface], starting_x: float, starting_y: float):
        for card in cards:
            display_image(screen, card, (starting_x, starting_y))
            starting_x += 200

    def display_players_cards(self, game: Game, screen: pygame.Surface):
        x = 10
        y = 50
        for player in game.players:
            display_image(screen, player.image, (x, y + 20))
            self.display_player_hand(screen,
                                     [resize(load_image(game.board.cities[city_name].image), 160, 222) for city_name in
                                      player.cards], x + 100, y)
            y += 150

    def picking_cards_for_remove_menu(self, buttons: [Button], difference: int,
                                      modifications: dict[str, tuple[c.color, c.color] | bool]):
        self.display_action_menu(600)
        picked_buttons: list[ImageButton] = []
        while True:
            self.display_contents_on_menu_screen(buttons, modifications)
            pygame.display.flip()

            mouse_x, mouse_y = self.get_next_input()

            pressed_button: Button | None = self.find_pressed_button(mouse_x, mouse_y, buttons, {"remove": len(picked_buttons) == difference})

            if pressed_button is not None:
                if pressed_button.info == "remove":
                    return picked_buttons
                if isinstance(pressed_button, ImageButton):
                    if pressed_button in picked_buttons:
                        picked_buttons.remove(pressed_button)
                        modifications[pressed_button.info] = False
                    else:
                        picked_buttons.append(pressed_button)
                        modifications[pressed_button.info] = True

    def remove_cards_from_player(self, player: Player, button_factory: ButtonFactory, game: Game, difference: int):
        city_buttons = button_factory.create_remove_menu_buttons(game.board.cities, player.cards, 5)
        modifications = {city.info: False for city in city_buttons[:-1]}
        modifications.update({"resume": (c.WHITE, c.RED)})
        print([button.info for button in city_buttons])
        cards = self.picking_cards_for_remove_menu(city_buttons, difference, modifications)
        player.remove_cards([card.info for card in cards])

    @staticmethod
    def find_pressed_button(mouse_x: float, mouse_y: float, buttons: [TextButton, ImageButton],
                            additional_requirements: dict[str, bool]) -> Button | None:
        for button in buttons:
            if button.is_clicked(mouse_x, mouse_y) and (
                    additional_requirements[button.info] if button.info in additional_requirements.keys() else True):
                return button

        return None

    def get_city(self, board: Board, additional_requirements: list[Callable[[City], bool]]) -> City:
        while True:
            mouse_x, mouse_y = self.get_next_input()
            destination = board.get_city_at_coordinates(mouse_x, mouse_y)

            if destination is not None and all(function(destination) for function in additional_requirements):
                break

        return destination

    def highlight_buttons(self, buttons: list[ImageButton] | ImageButton):
        if type(buttons) is ImageButton:
            pygame.draw.circle(self.screen, c.GREEN, (buttons.x + 90, buttons.y + 125), 10)
        else:
            for button in buttons:
                pygame.draw.circle(self.screen, c.GREEN, (button.x + 90, button.y + 125), 10)

    def picking_player_and_action_for_share(self, share_buttons: list[Button],
                                            modifications: dict[str, tuple[c.color, c.color] | bool],
                                            game: Game) -> tuple[Player, str] | tuple[None, None]:
        chosen_player = None
        while True:
            self.display_contents_on_menu_screen(share_buttons, modifications)
            pygame.display.flip()

            mouse_x, mouse_y = self.get_next_input()

            if mouse_y not in range(540, 800):
                return None, None

            pressed_button = self.find_pressed_button(mouse_x, mouse_y, share_buttons,
                                                      {"Give": chosen_player is not None,
                                                       "Take": chosen_player is not None})
            if pressed_button is None:
                pass
            elif pressed_button.info == "Give" and chosen_player is not None and game.current_player.has(
                    game.current_player.city):
                return chosen_player, "Give"
            elif pressed_button.info == "Take" and chosen_player is not None and chosen_player.has(
                    game.current_player.city):
                return chosen_player, "Take"
            elif type(pressed_button) is ImageButton:
                if chosen_player is not None:
                    modifications[chosen_player.name] = False
                print(chosen_player)
                chosen_player = game.get_player(pressed_button.info)
                print(chosen_player)
                modifications[chosen_player.name] = True

    def handle_share_action(self, game: Game, button_factory: ButtonFactory):
        players: list[tuple[str, pygame.Surface]] = [(pl.name, pl.image) for pl in game.players if
                                                     game.current_player.city == pl.city and game.current_player != pl]
        share_buttons = button_factory.create_share_buttons(players)

        self.display_current_board_position(game)
        self.display_action_menu()
        modifications = {button.info: False for button in share_buttons[:-2]}

        other_player, action = self.picking_player_and_action_for_share(share_buttons, modifications, game)

        if action is not None:
            game.share(other_player, action)
            if len(game.current_player.cards) > c.MAX_NUMBER_OF_CARDS:
                self.remove_cards_from_player(game.current_player, button_factory, game, 1)
            elif len(other_player.cards) > c.MAX_NUMBER_OF_CARDS:
                self.remove_cards_from_player(other_player, button_factory, game, 1)

    @staticmethod
    def are_cure_requirements_met(game: Game, picked_buttons: [ImageButton], color: str | None):
        return (
                game.board.cities[game.current_player.city].has_research_station and
                len(picked_buttons) == 3 and
                color is not None and
                game.is_disease_cured(color) is False
        )

    def picking_cards_for_cure(self, game: Game, buttons: list[Button],
                               modifications: dict[str, tuple[c.color, c.color] | bool]) -> list[ImageButton] | None:
        picked_buttons: list[ImageButton] = []
        while True:
            self.display_cure_menu(buttons, modifications)
            pygame.display.flip()

            mouse_x, mouse_y = self.get_next_input()

            if mouse_y not in range(540, 800):
                self.action_menu_open = False
                return None

            pressed_button: Button | None = self.find_pressed_button(mouse_x, mouse_y, buttons, {
                "cure": self.are_cure_requirements_met(game, picked_buttons,
                                                       have_the_same_color(game.board.cities, picked_buttons))})

            if pressed_button is not None:
                if pressed_button.info == "cure":
                    return picked_buttons
                if isinstance(pressed_button, ImageButton):
                    if pressed_button in picked_buttons:
                        picked_buttons.remove(pressed_button)
                        modifications[pressed_button.info] = False
                    else:
                        picked_buttons.append(pressed_button)
                        modifications[pressed_button.info] = True

    def handle_cure_action(self, game: Game, button_factory: ButtonFactory):
        buttons = button_factory.create_cure_buttons(game.board.cities, game.current_player.cards)
        modifications = {city.info: False for city in buttons[:-1]}
        modifications.update({buttons[-1].info: (c.WHITE, c.RED)})

        self.display_current_board_position(game)

        picked_cards_buttons = self.picking_cards_for_cure(game, buttons, modifications)
        if picked_cards_buttons is not None:
            color = have_the_same_color(game.board.cities, picked_cards_buttons)
            game.cure(color)
            game.current_player.remove_cards([card.info for card in picked_cards_buttons])

    def get_user_input_in_treat(self, choices: list[TextButton]) -> str | None:
        while True:
            mouse_x, mouse_y = self.get_next_input()
            if mouse_y not in range(540, 800):
                return None

            disease_button = self.find_pressed_button(mouse_x, mouse_y, choices, {})
            if disease_button is not None:
                return disease_button.info

    def handle_treat_action(self, game: Game, button_factory: ButtonFactory):
        """
        REMOVES DISEASES FROM A CITY
        IF A CITY HAS 1 TYPE OF DISEASE IT REMOVES N CUBES OF IT
        IF IT HAS MORE, THEN THE PLAYER CHOOSES WHICH DISEASE THEY WANT TO REMOVE
        """

        diseases = [(colour, value) for colour, value in
                    game.board.cities[game.current_player.city].diseases.items() if
                    value > 0]
        if len(diseases) == 1:
            game.treat(diseases[0][0])
        else:
            self.display_current_board_position(game)
            choices = button_factory.create_disease_removal_options_buttons(diseases)
            self.display_action_menu()
            self.display_contents_on_menu_screen(choices,
                                                 {choice.info: (from_str_to_color(choice.info), c.WHITE) for choice in
                                                  choices},
                                                 [("Pick what disease you want to treat", 50, c.WIDTH / 3.2, 580,
                                                   c.RED)])

            pygame.display.flip()

            result = self.get_user_input_in_treat(choices)

            if result:
                game.treat(result)

    def handle_hand_action(self, city_name: str, action: str, game: Game):
        if action == "Hand" and game.current_player.city != city_name:
            game.move(city_name, "direct")
        elif action == "Hand":
            self.display_current_board_position(game)
            pygame.display.flip()

            destination = self.get_city(game.board, [])
            game.move(destination.name, "charter")
        elif action == "Build":
            if game.research_station_count == 0:
                self.display_current_board_position(game)
                pygame.display.flip()

                city_to_remove_research_station = self.get_city(game.board, [City.has_research_station])
                game.add_research_station()
                city_to_remove_research_station.remove_research_station()

            game.build_research_station(city_name)

        game.current_player.remove_cards([city_name])

    def handle_hand_screen(self, card_buttons: list[Button], action: str, game: Game):
        self.display_current_board_position(game)
        self.display_action_menu()
        self.display_contents_on_menu_screen(card_buttons, {})
        pygame.display.flip()

        while True:
            mouse_x, mouse_y = self.get_next_input()

            if mouse_y not in range(540, 800):
                self.action_menu_open = False
                self.display_current_board_position(game)
                break

            pressed_card_button = self.find_pressed_button(mouse_x, mouse_y, card_buttons, {})
            if pressed_card_button is not None:
                city_name = pressed_card_button.info
                self.handle_hand_action(city_name, action, game)

                self.display_current_board_position(game)
                break

    def handle_actions_with_menu(self, button_factory: ButtonFactory, game: Game, mouse_x: float,
                                 mouse_y: float):
        while True:
            if mouse_y not in range(540, 800):
                self.action_menu_open = False
                break

            pressed_button = self.find_pressed_button(mouse_x, mouse_y, self.action_button_list, {
                "Treat": game.board.cities[game.current_player.city].has_diseases(),
                "Cure": game.board.cities[game.current_player.city].has_research_station,
                "Share": game.more_than_one_person_in_city(game.current_player.city)})
            if pressed_button is None:
                mouse_x, mouse_y = self.get_next_input()
            else:
                if pressed_button.info in ("Hand", "Build"):
                    card_buttons = button_factory.create_city_buttons(game.board.cities, game.current_player.cards)
                    self.handle_hand_screen(card_buttons, pressed_button.info, game)
                    self.action_menu_open = False
                elif pressed_button.info == "Treat":
                    self.handle_treat_action(game, button_factory)
                elif pressed_button.info == "Cure":
                    self.handle_cure_action(game, button_factory)
                elif pressed_button.info == "Share":
                    self.handle_share_action(game, button_factory)
                elif pressed_button.info == "Skip":
                    game.current_player.moves = 0

                break

    @staticmethod
    def handle_actions_without_menu(game: Game, mouse_x: float, mouse_y: float):
        # CHECKING IF THE PLAYER TRIES TO MOVE TO ANOTHER CITY
        chosen_city = game.board.get_city_at_coordinates(mouse_x, mouse_y)
        if chosen_city is not None:
            game.move(chosen_city.name, "basic")

    def start(self, game: Game, button_factory: ButtonFactory):
        cards_screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
        run = True
        while run:
            # PLAYERS TURN
            for player in game.players:
                game.current_player = player
                self.display_current_board_position(game)
                while player.moves > 0:
                    pygame.display.flip()

                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            # ACTIONS POSSIBLE WITH MENU OFF
                            if self.action_menu_open is False:
                                # OPENING MENU SCREEN
                                if mouse_y in range(780, 800):
                                    texts = [("Hand", 40, 315, 710, c.BLACK), ("Build", 40, 530, 710, c.BLACK),
                                             ("Treat", 40, 755, 710, c.BLACK), ("Cure", 40, 960, 710, c.BLACK),
                                             ("Share", 40, 1132, 710, c.BLACK), ("Skip", 40, 1300, 710, c.BLACK)]
                                    self.display_action_menu()
                                    self.display_contents_on_menu_screen(self.action_button_list, {},
                                                                         texts)
                                # ACTIONS POSSIBLE WITH MENU OFF
                                else:
                                    self.handle_actions_without_menu(game, mouse_x, mouse_y)
                                    self.display_current_board_position(game)
                            # ACTIONS POSSIBLE WITH MENU ON
                            else:
                                if mouse_y in range(540, 800):
                                    self.handle_actions_with_menu(button_factory, game, mouse_x, mouse_y)

                                self.display_current_board_position(game)
                                self.action_menu_open = False
                        # PLAYER WANTS TO CHECK ALL PLAYERS' HANDS. THIS SCREEN ONLY SHOWS WHEN THE PLAYER HOLDING THE "P" BUTTON
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                            cards_screen.fill(c.GRAY)
                            self.display_players_cards(game, cards_screen)
                        elif event.type == pygame.KEYUP and event.key == pygame.K_p:
                            self.display_current_board_position(game)
                game.end_turn()
                if len(game.current_player.cards) > c.MAX_NUMBER_OF_CARDS:
                    print("hi")
                    self.remove_cards_from_player(game.current_player, button_factory, game, len(game.current_player.cards) - c.MAX_NUMBER_OF_CARDS)
                    self.action_menu_open = False

        pygame.quit()
