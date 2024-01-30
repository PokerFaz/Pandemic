import pygame
import networkx

from src.models.buttons.button import Button
from src.models.buttons.text_button import TextButton
from src.models.buttons.image_button import ImageButton
from src.models.card import EventCard, CityCard, EpidemicCard, InfectionCard
from src.models.city import City
from src.models.player import Player
from src.models.board import Board
from src.misc.utility import resize, from_str_to_color, from_color_to_str
from src.misc import constants as c
from src.misc.images import background, red_disease, blue_disease, black_disease, yellow_disease
from src.misc.button_factory import ButtonFactory
from src.controllers.game import Game
from typing import Callable, Any, Deque
from collections import deque


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


def have_the_same_color(cities: list[City]) -> str | None:
    colors = [city.color for city in cities]
    if len(set(colors)) == 1:
        return from_color_to_str(colors[0])

    return None


class GUI:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.action_menu_open = False
        self.action_button_list: list[ImageButton] = []
        self.log_history: Deque[str] = deque()

    def get_next_input(self, main_screen: pygame.Surface, game: Game) -> (float, float):
        while True:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return mouse_x, mouse_y
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    self.display_messages()
                    pygame.display.flip()
                elif event.type == pygame.KEYUP and event.key == pygame.K_l:
                    self.screen.blit(main_screen, (0, 0))
                    pygame.display.flip()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.screen.fill(c.GRAY)
                    self.display_players_cards(game, self.screen)
                    pygame.display.flip()
                elif event.type == pygame.KEYUP and event.key == pygame.K_p:
                    self.screen.blit(main_screen, (0, 0))
                    pygame.display.flip()

    def display_messages(self):
        log_menu = pygame.Surface((c.WIDTH, c.HEIGHT), pygame.SRCALPHA)
        log_menu.fill((128, 128, 128, 220))

        while len(self.log_history) > 19:
            self.log_history.popleft()

        x = 10
        y = 10
        for message in self.log_history:
            write(log_menu, message, 30, x, y, c.BLACK)
            y += 40

        self.screen.blit(log_menu, (0, 0))

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

    def display_disease_info(self, disease_info: dict[str, list[int, bool, bool]]):
        starting_x = 1050
        pygame.draw.circle(self.screen, c.RED, (starting_x, 600), 20)
        pygame.draw.circle(self.screen, c.BLUE, (starting_x + 50, 600), 20)
        pygame.draw.circle(self.screen, c.YELLOW, (starting_x + 100, 600), 20)
        pygame.draw.circle(self.screen, c.BLACK, (starting_x + 150, 600), 20)

        display_image(self.screen, red_disease, (starting_x - 15, 585))
        display_image(self.screen, blue_disease, (starting_x + 35, 585))
        display_image(self.screen, yellow_disease, (starting_x + 85, 585))
        display_image(self.screen, black_disease, (starting_x + 135, 585))

        write(self.screen, "Cubes left", 20, starting_x - 100, 650, c.BLACK)
        write(self.screen, "Cured", 20, starting_x - 100, 700, c.BLACK)
        write(self.screen, "Eradicated", 20, starting_x - 100, 750, c.BLACK)

        starting_x = 1035
        for disease, info in disease_info.items():
            starting_y = 650
            write(self.screen, str(info[0]), 40, starting_x, starting_y, from_str_to_color(disease))
            starting_y += 50
            write(self.screen, str(info[1]), 25, starting_x, starting_y, c.GREEN if info[1] else c.BLACK)
            starting_y += 50
            write(self.screen, str(info[2]), 25, starting_x, starting_y, c.GREEN if info[2] else c.BLACK)
            starting_x += 50

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
        """
        Displays the action menu on the main screen

        :param height: how long is the action menu
        """
        self.action_menu_open = True

        # STACKOVERFLOW CODE FOR TRANSPARENT RECT
        action_menu = pygame.Surface((c.WIDTH, height), pygame.SRCALPHA)
        action_menu.fill((128, 128, 128, 220))
        self.screen.blit(action_menu, (0, c.HEIGHT - height))

    def display_contents_on_menu_screen(self, buttons: list[Button],
                                        modifications: dict[str, tuple[c.color, c.color] | Callable[..., None]],
                                        texts: list[tuple[str, int, float, float, c.color]] = ()):
        """
        Template for displaying objects on the menu screen

        :param buttons: buttons that will be displayed on the main screen
        :param modifications: changes made to the appearance of the buttons on the screen
        :param texts: texts that will be displayed on the main screen
        """
        for button in buttons:
            if isinstance(button, TextButton) and button.info in modifications.keys():
                button.display_button(self.screen, rect_color=modifications[button.info][0],
                                      text_color=modifications[button.info][1])
            elif button:
                button.display_button(self.screen)
                if isinstance(button, ImageButton) and button.info in modifications:
                    modifications[button.info](button)

        for text in texts:
            if text:
                write(self.screen, *text)

    def display_current_state(self, game: Game):
        """
        Displays the current state of the game

        :param game: used for getting the objects
        """

        self.display_board(game.board)
        display_image(self.screen, game.current_player.image, (20, 20))
        write(self.screen, f"{game.current_player.moves}", 60, 70, 20)
        self.display_disease_info(game.disease_info)
        game.players.draw(self.screen)

    def display_buttons(self, card_buttons: [Button]):
        for button in card_buttons:
            button.display_button(self.screen)

    def display_cure_menu(self, buttons: list[Button],
                          modifications: dict[str, tuple[c.color, c.color] | Callable[[ImageButton], None]]):
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
                                     [resize(card.image, 160, 222) for card in
                                      player.cards], x + 100, y)
            y += 150

    def ask_player_to_use_event_card(self, button_factory: ButtonFactory, game: Game):
        self.display_action_menu(800)
        yes_no_buttons = button_factory.create_yes_no_buttons()
        self.display_contents_on_menu_screen(yes_no_buttons, {}, [
            ("Do you want to use an event card?", 50, c.WIDTH / 3 - 70, c.HEIGHT / 2 - 30, c.RED)])
        pygame.display.flip()

        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, game)
            pressed_button = self.find_pressed_button(mouse_x, mouse_y, yes_no_buttons, {})
            if pressed_button is not None:
                if pressed_button.info == "yes":
                    self.handle_event_menu(button_factory, game)
                else:
                    break

    def display_end_screen(self, end_result: str):
        if end_result == "Defeat":
            write(self.screen, "DEFEAT", 100, 600, 350, c.RED)
        else:
            write(self.screen, "VICTORY", 100, 600, 350, c.GREEN)

    def picking_cards_for_remove_menu(self, buttons: [Button], difference: int, game: Game,
                                      modifications: dict[
                                          str, tuple[c.color, c.color] | Callable[[ImageButton], None]]) -> list[ImageButton]:
        self.display_action_menu(600)
        picked_buttons: list[ImageButton] = []
        while True:
            self.display_contents_on_menu_screen(buttons, modifications)
            pygame.display.flip()
            screen_copy = self.screen.copy()

            mouse_x, mouse_y = self.get_next_input(screen_copy, game)

            pressed_button: Button | None = self.find_pressed_button(mouse_x, mouse_y, buttons,
                                                                     {"remove": len(picked_buttons) == difference})

            if pressed_button is not None:
                if pressed_button.info == "remove":
                    return picked_buttons
                if isinstance(pressed_button, ImageButton):
                    if pressed_button in picked_buttons:
                        picked_buttons.remove(pressed_button)
                        modifications.pop(pressed_button.info)
                    else:
                        picked_buttons.append(pressed_button)
                        modifications[pressed_button.info] = self.highlight_buttons

    def remove_cards_from_player(self, game: Game, player: Player, button_factory: ButtonFactory, difference: int):
        city_buttons = button_factory.create_remove_menu_buttons(player.cards, 5)
        modifications = {"resume": (c.WHITE, c.RED)}
        cards = self.picking_cards_for_remove_menu(city_buttons, difference, game, modifications)
        self.log_history.append(f"{player.name} removed {[card.info.name for card in cards]}")
        player.remove_cards([card.info for card in cards])

    @staticmethod
    def find_pressed_button(mouse_x: float, mouse_y: float, buttons: [TextButton, ImageButton],
                            additional_requirements: dict[Any, bool]) -> Button | None:
        for button in buttons:
            if button.is_clicked(mouse_x, mouse_y) and (
                    additional_requirements[button.info] if button.info in additional_requirements.keys() else True):
                return button

        return None

    def get_city(self, game: Game, additional_requirements: list[Callable[[City], bool]]) -> City:
        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, game)
            destination = game.board.get_city_at_coordinates(mouse_x, mouse_y)

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
                                            modifications: dict[
                                                str, tuple[c.color, c.color] | Callable[[ImageButton], None]],
                                            game: Game) -> tuple[Player, str] | tuple[None, None]:
        chosen_player = None
        while True:
            self.display_contents_on_menu_screen(share_buttons, modifications)
            pygame.display.flip()
            screen_copy = self.screen.copy()

            mouse_x, mouse_y = self.get_next_input(screen_copy, game)

            if mouse_y not in range(540, 800):
                return None, None

            pressed_button = self.find_pressed_button(mouse_x, mouse_y, share_buttons,
                                                      {"Give": chosen_player is not None,
                                                       "Take": chosen_player is not None})
            if pressed_button is None:
                pass
            elif pressed_button.info == "Give" and chosen_player is not None and game.current_player.has(
                    game.current_player.location):
                return chosen_player, "Give"
            elif pressed_button.info == "Take" and chosen_player is not None and chosen_player.has(
                    game.current_player.location):
                return chosen_player, "Take"
            elif type(pressed_button) is ImageButton:
                if chosen_player is not None:
                    modifications.pop(chosen_player.name)
                chosen_player = game.get_player(pressed_button.info)
                modifications[chosen_player.name] = self.highlight_buttons

    def picking_cards_for_cure(self, game: Game, buttons: list[Button],
                               modifications: dict[str, tuple[c.color, c.color] | Callable[[ImageButton], None]]) -> \
            list[ImageButton] | None:
        picked_buttons: list[ImageButton] = []
        self.display_action_menu()
        while True:
            self.display_cure_menu(buttons, modifications)
            pygame.display.flip()
            screen_copy = self.screen.copy()

            mouse_x, mouse_y = self.get_next_input(screen_copy, game)

            if mouse_y not in range(540, 800):
                self.action_menu_open = False
                return None

            pressed_button: Button | None = self.find_pressed_button(mouse_x, mouse_y, buttons, {
                "cure": self.are_cure_requirements_met(game, picked_buttons,
                                                       have_the_same_color(
                                                           [game.board.cities[button.info.name] for button in
                                                            picked_buttons]))})

            if pressed_button is not None:
                if pressed_button.info == "cure":
                    return picked_buttons
                if isinstance(pressed_button, ImageButton):
                    if pressed_button in picked_buttons:
                        picked_buttons.remove(pressed_button)
                        modifications.pop(pressed_button.info)
                    else:
                        picked_buttons.append(pressed_button)
                        modifications[pressed_button.info] = self.highlight_buttons

    def handle_share_action(self, game: Game, button_factory: ButtonFactory):
        players: list[tuple[str, pygame.Surface]] = [(pl.name, pl.image) for pl in game.players if
                                                     game.current_player.location == pl.location and game.current_player != pl]
        share_buttons = button_factory.create_share_buttons(players)

        self.display_current_state(game)
        self.display_action_menu()

        other_player, action = self.picking_player_and_action_for_share(share_buttons, {}, game)

        if action is not None:
            game.share(other_player, action, self.log_history)
            if len(game.current_player.cards) > c.MAX_NUMBER_OF_CARDS:
                self.remove_cards_from_player(game, game.current_player, button_factory, 1)
            elif len(other_player.cards) > c.MAX_NUMBER_OF_CARDS:
                self.remove_cards_from_player(game, other_player, button_factory, 1)

    @staticmethod
    def are_cure_requirements_met(game: Game, picked_buttons: [ImageButton], color: str | None):
        return (
                game.board.cities[game.current_player.location].has_research_station and
                len(picked_buttons) == 3 and
                color is not None and
                game.is_disease_cured(color) is False
        )

    def handle_cure_action(self, game: Game, button_factory: ButtonFactory):
        buttons = button_factory.create_cure_buttons(
            [card for card in game.current_player.cards if not isinstance(card, EventCard)])
        for button in buttons:
            print(button.info)
        modifications = {buttons[-1].info: (c.WHITE, c.RED)}

        self.display_current_state(game)

        picked_cards_buttons = self.picking_cards_for_cure(game, buttons, modifications)
        if picked_cards_buttons is not None:
            color = have_the_same_color([game.board.cities[button.info.name] for button in picked_cards_buttons])
            game.cure(color, self.log_history)
            game.current_player.remove_cards([card.info for card in picked_cards_buttons])

    def get_user_input_in_treat(self, choices: list[TextButton], game: Game) -> str | None:
        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, game)
            if mouse_y not in range(540, 800):
                return None

            disease_button = self.find_pressed_button(mouse_x, mouse_y, choices, {})
            if disease_button is not None:
                return disease_button.info

    def handle_treat_action(self, game: Game, button_factory: ButtonFactory):
        """
        REMOVES DISEASES FROM A CITY
        IF A CITY HAS 1 TYPE OF DISEASE IT REMOVES N CUBES FROM IT
        IF IT HAS MORE, THEN THE PLAYER CHOOSES WHICH DISEASE THEY WANT TO REMOVE
        """

        diseases = [(colour, value) for colour, value in
                    game.board.cities[game.current_player.location].diseases.items() if
                    value > 0]
        if len(diseases) == 1:
            game.treat(diseases[0][0], self.log_history)
        else:
            self.display_current_state(game)
            choices = button_factory.create_disease_removal_options_buttons(diseases)
            self.display_action_menu()
            self.display_contents_on_menu_screen(choices,
                                                 {choice.info: (from_str_to_color(choice.info), c.WHITE) for choice in
                                                  choices},
                                                 [("Pick what disease you want to treat", 50, c.WIDTH / 3.2, 580,
                                                   c.RED)])

            pygame.display.flip()

            result = self.get_user_input_in_treat(choices, game)

            if result:
                game.treat(result, self.log_history)

    def write_number(self, number: str, button: Button):
        print("hey I work")
        write(self.screen, number, 70, button.x + 85, button.y + 110, c.GREEN)

    def handle_forecast(self, button_factory: ButtonFactory, game: Game) -> list[City]:
        infection_cards = game.infection_deck.top_n_cards(6)
        infection_cities = [game.board.cities[card.name] for card in infection_cards]
        forecast_buttons = button_factory.create_forecast_buttons(infection_cities)
        modifications: dict = {}

        self.display_current_state(game)
        self.display_action_menu(350)
        texts = [
            ("top", 30, 5, 750, c.BLACK),
            ("bottom", 30, 1000, 750, c.BLACK)
        ]
        self.display_contents_on_menu_screen(forecast_buttons, modifications, texts)
        pygame.display.flip()

        ordered_cards: list[City] = []
        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, game)
            pressed_button = self.find_pressed_button(mouse_x, mouse_y, forecast_buttons, {"ready": len(ordered_cards) == 6})

            if pressed_button is None:
                pass
            elif pressed_button.info == "ready":
                return ordered_cards
            elif pressed_button.info not in ordered_cards:
                ordered_cards.append(pressed_button.info)
                to_write = str(len(ordered_cards))
                modifications[pressed_button.info] = lambda button, number=to_write: self.write_number(number, button)
            elif pressed_button.info in ordered_cards:
                ordered_cards.remove(pressed_button.info)
                modifications = {button_info: lambda button, n=str(number): self.write_number(n, button) for
                                 number, button_info
                                 in enumerate(ordered_cards, start=1)}

            self.display_contents_on_menu_screen(forecast_buttons, modifications)
            pygame.display.flip()

    def handle_airlift(self, button_factory: ButtonFactory, game: Game):
        # CHANGE THE BUTTON FACTORY FUNCTION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        player_buttons = button_factory.create_share_buttons([(player.name, player.image) for player in game.players])[:-2]
        self.display_current_state(game)
        self.display_action_menu()
        self.display_contents_on_menu_screen(player_buttons, {})
        pygame.display.flip()
        chosen_player = None

        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, game)
            pressed_button = self.find_pressed_button(mouse_x, mouse_y, player_buttons, {})
            if pressed_button is None:
                pass
            else:
                chosen_player = game.get_player(pressed_button.info)
                break

        self.display_current_state(game)
        pygame.display.flip()

        player_new_location = self.get_city(game, [lambda city: city != game.board.cities[chosen_player.location]])
        chosen_player.move(player_new_location.x, player_new_location.y, player_new_location.name)

    def handle_resilient_population(self, button_factory: ButtonFactory, game: Game):
        infection_card_buttons = button_factory.create_rp_buttons([card.name for card in game.infection_discard_pile])

        self.display_action_menu(800)
        self.display_contents_on_menu_screen(infection_card_buttons, {})
        pygame.display.flip()

        screen_copy = self.screen.copy()
        while True:

            mouse_x, mouse_y = self.get_next_input(screen_copy, game)
            pressed_button = self.find_pressed_button(mouse_x, mouse_y, infection_card_buttons, {})
            if pressed_button is None:
                pass
            else:
                to_be_removed = pressed_button.info
                break

        for card in game.infection_discard_pile:
            if card.name == to_be_removed:
                game.infection_discard_pile.deck.remove(card)
                self.log_history.append(f"{to_be_removed} was removed from the game")

    def handle_event_menu(self, button_factory: ButtonFactory, game: Game):
        event_cards: list[EventCard] = [event_card for player in game.players for event_card in player.cards if
                                        isinstance(event_card, EventCard)]

        event_cards_buttons = button_factory.create_player_hand_buttons(event_cards)
        self.display_current_state(game)
        self.display_action_menu()
        self.display_contents_on_menu_screen(event_cards_buttons, {})
        pygame.display.flip()

        screen_copy = self.screen.copy()
        mouse_x, mouse_y = self.get_next_input(screen_copy, game)
        pressed_button = self.find_pressed_button(mouse_x, mouse_y, event_cards_buttons, {})

        if pressed_button is not None:
            match pressed_button.info.name:
                case "One quiet night":
                    game.skip_next_infection_step = True
                case "Resilient population":
                    self.handle_resilient_population(button_factory, game)
                    print(game.infection_discard_pile)

                case "Airlift":
                    self.handle_airlift(button_factory, game)
                case "Forecast":
                    ordered_cards = self.handle_forecast(button_factory, game)
                    ordered_infection_cards = [InfectionCard(elem) for elem in ordered_cards]
                    game.infection_deck.add_to_front(ordered_infection_cards)

                    for player in game.players:
                        if player.has("Forecast"):
                            player.cards.remove(pressed_button.info)
                            self.log_history.append(f"{player.name} used Forecast")

                case "Government grant":
                    self.display_current_state(game)
                    pygame.display.flip()

                    city = self.get_city(game, [])
                    self.handle_build(game, city)
                    for player in game.players:
                        if player.has("Government grant"):
                            player.cards.remove(pressed_button.info)
                            self.log_history.append(f"{player.name} used Government grant")

    def handle_build(self, game: Game, city: City):
        if game.research_station_count == 0:
            self.display_current_state(game)
            pygame.display.flip()

            city_to_remove_research_station = self.get_city(game, [City.has_research_station])
            self.log_history.append(
                f"{city_to_remove_research_station.name} now doesn't have a research station")
            game.add_research_station()
            city_to_remove_research_station.remove_research_station()

        game.build_research_station(city, self.log_history)

    def handle_hand_action(self, info: CityCard | str, button_factory: ButtonFactory, action: str, game: Game):
        if info == "event":
            self.handle_event_menu(button_factory, game)
        else:
            if action == "Hand" and game.current_player.location != info.name:
                game.move(info.name, "direct", self.log_history)
            elif action == "Hand":
                self.display_current_state(game)
                pygame.display.flip()

                destination = self.get_city(game, [])
                game.move(destination.name, "charter", self.log_history)
            elif action == "Build" and game.current_player.location == info.name:
                self.handle_build(game, game.board.cities[info.name])
                game.current_player.moves -= 1

            game.current_player.remove_cards([info])

    def handle_hand_screen(self, card_buttons: list[Button], button_factory: ButtonFactory, action: str, game: Game):
        self.display_current_state(game)
        self.display_action_menu()
        self.display_contents_on_menu_screen(card_buttons, {})
        pygame.display.flip()

        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, game)

            if mouse_y not in range(540, 800):
                self.action_menu_open = False
                self.display_current_state(game)
                break

            pressed_button = self.find_pressed_button(mouse_x, mouse_y, card_buttons,
                                                      {
                                                          button.info: isinstance(button.info,
                                                                                  CityCard) and game.current_player.location == button.info.name
                                                          for button in card_buttons} if action == "Build" else {
                                                          button.info: isinstance(button.info, CityCard) or isinstance(
                                                              button, TextButton)
                                                          for button in card_buttons})
            if pressed_button is not None:
                info = pressed_button.info
                self.handle_hand_action(info, button_factory, action, game)

                self.display_current_state(game)
                break

    def handle_actions_with_menu(self, button_factory: ButtonFactory, game: Game, mouse_x: float, mouse_y: float):
        while True:
            if mouse_y not in range(540, 800):
                self.action_menu_open = False
                break

            pressed_button = self.find_pressed_button(mouse_x, mouse_y, self.action_button_list, {
                "Treat": game.board.cities[game.current_player.location].has_diseases(),
                "Cure": game.board.cities[game.current_player.location].has_research_station,
                "Share": game.more_than_one_person_in_city(game.current_player.location)})

            if pressed_button is None:
                screen_copy = self.screen.copy()
                mouse_x, mouse_y = self.get_next_input(screen_copy, game)
            else:
                if pressed_button.info in ("Hand", "Build"):
                    buttons = button_factory.create_hand_menu_buttons(game.current_player.cards, pressed_button.info)

                    self.handle_hand_screen(buttons, button_factory, pressed_button.info, game)
                    self.action_menu_open = False
                elif pressed_button.info == "Treat":
                    self.handle_treat_action(game, button_factory)
                elif pressed_button.info == "Cure":
                    self.handle_cure_action(game, button_factory)
                elif pressed_button.info == "Share":
                    self.handle_share_action(game, button_factory)
                elif pressed_button.info == "Skip":
                    game.skip()
                    self.log_history.append(f"{game.current_player.name} skipped")

                break

    def handle_actions_without_menu(self, game: Game, mouse_x: float, mouse_y: float):
        """
        Handles actions without the menu being open. The only possible actions are moving the player currently

        :param game: used for game logic
        :param mouse_x: position of the input by x
        :param mouse_y: position of the input by y
        """

        # CHECKING IF THE PLAYER TRIES TO MOVE TO ANOTHER CITY
        chosen_city = game.board.get_city_at_coordinates(mouse_x, mouse_y)
        if chosen_city is not None:
            game.move(chosen_city.name, "basic", self.log_history)

    def end_turn(self, button_factory: ButtonFactory, game: Game):

        drawn_cards = game.player_deck.get_cards(2)
        self.log_history.append(f"{game.current_player.name} drew {[card.name for card in drawn_cards]}")

        self.ask_player_to_use_event_card(button_factory, game)

        self.display_current_state(game)
        pygame.display.flip()
        pygame.time.wait(100)

        for card in drawn_cards:
            if isinstance(card, EpidemicCard):
                self.ask_player_to_use_event_card(button_factory, game)

                self.log_history.append(f"Resolving epidemic card:")
                game.resolve_epidemic_card(self.log_history)
                drawn_cards.remove(card)
            else:
                game.current_player.draw([card])

        self.display_current_state(game)
        pygame.display.flip()
        pygame.time.wait(100)

        counter = game.board.infection_rate_counter
        cards_to_take = 2 if counter < 3 else (3 if counter < 5 else 4)
        drawn_cards = game.infection_deck.top_n_cards(cards_to_take)

        if not game.skip_next_infection_step:
            for card in drawn_cards:
                self.ask_player_to_use_event_card(button_factory, game)

                self.display_current_state(game)
                pygame.display.flip()
                pygame.time.wait(1000)

                target_city = game.board.cities[card.name]
                game.infect(target_city, from_color_to_str(target_city.color), 1, self.log_history)

                game.infection_discard_pile.add_cards([card])

            game.current_player.replenish_moves()
        game.skip_next_infection_step = False

    def start(self, game: Game, button_factory: ButtonFactory):
        """
        Starts the game. Each player's turn consists of 3 parts:
        - Do 4 actions(they may skip as well)
        - Draw 2 cards
        - Infect cities
        The last two are realized in the game.end_turn() function

        :param game: used for doing the game logic
        :param button_factory: for creating buttons
        """

        run = True
        while run:
            for player in game.players:
                game.current_player = player
                self.display_current_state(game)
                while player.moves > 0:
                    pygame.display.flip()

                    screen_copy = self.screen.copy()
                    mouse_x, mouse_y = self.get_next_input(screen_copy, game)

                    # ACTIONS POSSIBLE WITH MENU OFF
                    if self.action_menu_open is False:
                        # OPENING MENU SCREEN
                        if mouse_y in range(780, 800):
                            self.display_action_menu()
                            self.display_contents_on_menu_screen(self.action_button_list, {}, c.action_names)
                        # MOVING THE CHARACTER
                        else:
                            self.handle_actions_without_menu(game, mouse_x, mouse_y)
                            self.display_current_state(game)
                    # ACTIONS POSSIBLE WITH MENU ON
                    else:
                        if mouse_y in range(540, 800):
                            self.handle_actions_with_menu(button_factory, game, mouse_x, mouse_y)

                        self.display_current_state(game)
                        self.action_menu_open = False

                end_state = game.did_end()
                if end_state != "No":
                    self.display_end_screen(end_state)
                    pygame.display.flip()
                    while True:
                        d = self.get_next_input(self.screen, game)

                self.end_turn(button_factory, game)

                end_state = game.did_end()
                if end_state != "No":
                    self.display_end_screen(end_state)
                    pygame.display.flip()
                    while True:
                        d = self.get_next_input(self.screen, game)
                    
                if len(game.current_player.cards) > c.MAX_NUMBER_OF_CARDS:
                    self.remove_cards_from_player(game, game.current_player, button_factory,
                                                  len(game.current_player.cards) - c.MAX_NUMBER_OF_CARDS)

                self.action_menu_open = False

        pygame.quit()
