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
from src.misc.images import background, red_disease, blue_disease, black_disease, yellow_disease, infection_card_image, \
    back_of_cities
from src.misc.button_factory import ButtonFactory
from src.controllers.game import Game
from typing import Callable, Any, Deque, Generator
from collections import deque


def iterate_diseases(city_diseases: dict[str, int]) -> Generator[tuple[str, int], None, None]:
    """
    Yields disease information(number, color name) of a city if the disease is present in the city

    :param city_diseases:
    :return: tuple containing the disease number of cubes and color.
    """

    no_diseases = 0
    for color, number in city_diseases.items():
        if number > no_diseases:
            yield number, color


def write(screen: pygame.Surface, text: str, text_size: int, coordinates: tuple[int, int], color: c.color = c.RED,
          has_background: bool = False):
    """
    Displays text on a given screen

    :param screen: the screen where the text will be displayed
    :param text: the text to be displayed
    :param text_size: the font size of text
    :param coordinates: positional argument
    :param color: the color of the text
    :param has_background: used for displaying a rect behind the text if needed
    :return: nothing
    """

    font = pygame.font.Font(None, text_size)
    text = font.render(text, True, color, c.WHITE if has_background else None)
    screen.blit(text, coordinates)


def display_image(screen: pygame.Surface, image: pygame.Surface, coordinates: (int, int)):
    """
    Displays image on a given screen

    :param screen: the screen where the image will be displayed
    :param image: image to be displayed
    :param coordinates: positional argument
    :return: nothing
    """
    screen.blit(image, coordinates)


def have_the_same_color(cities: list[City]) -> str | None:
    """
    If the cards have the same color, it returns its name, otherwise it returns None

    :param cities: cities to be checked if they have the same color.
    :return: color name or None
    """
    colors = [city.color for city in cities]
    if len(set(colors)) == 1:
        return from_color_to_str(colors[0])

    return None


class GUI:
    """
    Represents a graphical user interface

    """

    def __init__(self, screen: pygame.Surface):
        """
            Initializes the GUI object.

            :param screen: the main screen for the game

            Attributes:
                action_menu_open: flag indicating whether the action menu is open or closed
                action_button_list: buttons for navigating the start of the action menu
                log_history: deque for keeping the log messages
            """
        self.screen = screen
        self.action_menu_open = False
        self.action_button_list: list[Button] = []
        self.log_history: Deque[str] = deque()

    @staticmethod
    def find_pressed_button(mouse_x: float, mouse_y: float, buttons: [TextButton, ImageButton],
                            additional_requirements: dict[Any, bool]) -> Button | None:
        """
        Used for finding a pressed button

        :param mouse_x: mouse location by x
        :param mouse_y: mouse location by y
        :param buttons: list of buttons to check for press
        :param additional_requirements: requirements that have to be met for a button, so it can be pressed
        :return: the pressed button or None
        """

        for button in buttons:
            if button.is_clicked(mouse_x, mouse_y) and (
                    additional_requirements[button.info] if button.info in additional_requirements.keys() else True):
                return button

        return None

    @staticmethod
    def is_outside_of_menu(mouse_y: int, menu_height: int = 240) -> bool:
        """
        Checks if the press was outside the menu

        :param mouse_y: mouse location by y
        :param menu_height: the height of the action menu
        :return: true if it is outside else false
        """

        return mouse_y not in range(c.HEIGHT - menu_height, c.HEIGHT)

    @staticmethod
    def are_cure_requirements_met(game: Game, number_of_picked_cards: int, color: str | None) -> bool:
        """
        Requirements that have to be met, so that the cure action ca be done

        :param game: used for its attributes and functions
        :param number_of_picked_cards: the number of cards that the player has chosen
        :param color: the color of the picked cards.
        If the cards had different color then it is None
        :return: bool
        """

        def required_number_of_cards() -> int:
            expected_number_of_cards = 3
            if game.current_player.name == "Scientist":
                expected_number_of_cards = 2

            return expected_number_of_cards

        return (
                game.board.cities[game.current_player.location].has_research_station() and
                number_of_picked_cards == required_number_of_cards() and
                color is not None and
                not game.is_disease_cured(color)
        )

    def get_next_input(self, main_screen: pygame.Surface, players: pygame.sprite.Group) -> (int, int):
        """
        Handles user input

        :param main_screen: copy of the previous screen. Used after user has stopped checking log messages
        and cards in all players
        :param players: used for displaying the screen with their cards
        :return: coordinates of the click
        """

        while True:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return mouse_x, mouse_y
                # PLAYER WANTS TO ACCESS THE LOG SCREEN
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    self.display_messages()
                    pygame.display.flip()
                # PLAYER WANTS TO ACCESS THE SCREEN WITH ALL PLAYERS' CARDS
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.screen.fill(c.GRAY)
                    self.display_players_cards(players)
                    pygame.display.flip()
                elif event.type == pygame.KEYUP and (event.key in (pygame.K_p, pygame.K_l)):
                    self.screen.blit(main_screen, c.top_left)
                    pygame.display.flip()

    def display_messages(self):
        """
        Displays the most recent log messages

        :return: nothing
        """
        opacity_level = 220

        log_menu = pygame.Surface((c.WIDTH, c.HEIGHT), pygame.SRCALPHA)
        log_menu.fill((*c.GRAY, opacity_level))

        while len(self.log_history) > c.MAX_NUMBER_OF_MESSAGES:
            self.log_history.popleft()

        x = 10
        y = 10
        text_size = 30

        for message in self.log_history:
            write(log_menu, message, text_size, (x, y), c.BLACK)
            y += 40

        self.screen.blit(log_menu, c.top_left)

    def display_diseases(self, city: City):
        """
        Displays on the main screen the diseases in a given city

        :param city: the city from where we get the disease information
        :return: nothing
        """
        text_size = 40
        y_offset = -15
        x_offsets = [-30, 10, -50]

        for (number, color), x_position in zip(iterate_diseases(city.diseases), x_offsets):
            write(self.screen, str(number), text_size, (city.x + x_position, city.y + y_offset),
                  from_str_to_color(color) if color != "Yellow" else c.DARK_YELLOW)

    def display_disease_info(self, disease_info: dict[str, list[int, bool, bool]]):
        """
        Displays the general information about all diseases in the game, including leftover cubes,
        is it cured and is it eradicated

        :param disease_info: information about the diseases
        :return: nothing
        """

        starting_x = 1050
        disease_colors = [c.RED, c.BLUE, c.YELLOW, c.BLACK]
        disease_images = [red_disease, blue_disease, yellow_disease, black_disease]

        circle_y = 600
        offset = -15
        for color, image in zip(disease_colors, disease_images):
            pygame.draw.circle(self.screen, color, (starting_x, circle_y), 2 * c.RADIUS_OF_CIRCLE)
            display_image(self.screen, image, (starting_x + offset, circle_y + offset))
            starting_x += 50

        starting_x = 1050 - 100
        text_y = 650
        write(self.screen, "Cubes left", 20, (starting_x, text_y), c.BLACK)
        write(self.screen, "Cured", 20, (starting_x, text_y + 50), c.BLACK)
        write(self.screen, "Eradicated", 20, (starting_x, text_y + 100), c.BLACK)

        starting_x = 1035
        starting_y = 650

        numbers_text_size = 40
        bool_text_size = 25

        for disease, info in disease_info.items():
            write(self.screen, str(info[0]), numbers_text_size, (starting_x, starting_y), from_str_to_color(disease))
            write(self.screen, str(info[1]), bool_text_size, (starting_x, starting_y + 50),
                  c.GREEN if info[1] else c.BLACK)
            write(self.screen, str(info[2]), bool_text_size, (starting_x, starting_y + 100),
                  c.GREEN if info[2] else c.BLACK)
            starting_x += 50

    def display_connecting_lines(self, edges: networkx.classes.reportviews.EdgeView, cities: dict[str, City]):
        """
        Displays the lines connecting the cities on the board

        :param edges: edges of the graph
        :param cities: city information
        :return: nothing
        """

        line_width = 2

        sf_tokyo_split_points = (0, 200), (1550, 251)
        sf_manila_split_points = (0, 300), (1500, 420)
        la_sydney_split_points = (0, 362), (1500, 630)

        for city1, city2 in edges:
            if city1 == "San Francisco" and city2 == "Tokyo":
                pygame.draw.line(self.screen, c.BLACK, (cities[city1].x, cities[city1].y),
                                 sf_tokyo_split_points[0], line_width)
                pygame.draw.line(self.screen, c.BLACK, (cities[city2].x, cities[city2].y),
                                 sf_tokyo_split_points[1], line_width)
            elif city1 == "San Francisco" and city2 == "Manila":
                pygame.draw.line(self.screen, c.BLACK, (cities[city1].x, cities[city1].y),
                                 sf_manila_split_points[0], line_width)
                pygame.draw.line(self.screen, c.BLACK, (cities[city2].x, cities[city2].y),
                                 sf_manila_split_points[1], line_width)
            elif city1 == "Los Angeles" and city2 == "Sydney":
                pygame.draw.line(self.screen, c.BLACK, (cities[city1].x, cities[city1].y),
                                 la_sydney_split_points[0], line_width)
                pygame.draw.line(self.screen, c.BLACK, (cities[city2].x, cities[city2].y),
                                 la_sydney_split_points[1], line_width)
            else:
                pygame.draw.line(self.screen, c.BLACK, (cities[city1].x, cities[city1].y),
                                 (cities[city2].x, cities[city2].y), line_width)

    def display_cities(self, cities: dict[str, City]):
        """
        Displays the cities on the board

        :param cities: for getting the city information
        :return: nothing
        """
        offset_y = 15
        city_name_size = 25

        for city in cities.values():
            center = (city.x, city.y)
            pygame.draw.circle(self.screen, city.color, center, c.RADIUS_OF_CIRCLE)

            if city.name not in ("Ho Chi Minh City", "Istanbul"):
                offset_x = -15
            else:
                offset_x = -60

            if city.has_research_station():
                color = c.BLACK
            else:
                color = c.GRAY

            write(self.screen, f"{city.name}", city_name_size, (city.x + offset_x, city.y + offset_y), color, True)

            self.display_diseases(city)

    def display_outbreaks(self, outbreaks_counter: int):
        """
        Displays the outbreaks counter on the board

        :param outbreaks_counter: number of current outbreaks that have happened
        :return: nothing
        """

        text_size = 43
        outbreaks_coordinates = (20, 500)
        counter_coordinates = (187, 503)

        write(self.screen, "Outbreaks:", text_size, outbreaks_coordinates, c.BLACK)
        write(self.screen, f"{outbreaks_counter}", text_size, counter_coordinates, c.GREEN)

    def display_infection_rate(self, rate_counter: int):
        """
        Displays the infection rate

        :param rate_counter: current rate counter
        :return: nothing
        """

        infection_text_size = 50
        infection_text_position = (1170, 30)

        write(self.screen, "Infection rate", infection_text_size, infection_text_position, c.BLACK)

        x = 1100
        y = 100
        number_size = 30
        number_offset_x = -5
        number_offset_y = 20

        for counter in range(c.NUMBER_OF_INFECTION_RATE_MARKERS):
            circle_color = c.DARK_GREEN if counter == rate_counter else c.GREEN

            pygame.draw.circle(self.screen, circle_color, (x, y), c.RADIUS_OF_CIRCLE)

            if counter < 3:
                number_color = c.BLACK
                number = "2"
            elif counter < 5:
                number_color = c.BLUE
                number = "3"
            else:
                number_color = c.RED
                number = "4"

            write(self.screen, number, number_size, (x + number_offset_x, y + number_offset_y), number_color)

            x += 60

    def display_action_tab_opener(self):
        rect_dimension = (0, 780, 1500, 20)
        pygame.draw.rect(self.screen, c.GRAY, rect_dimension, border_top_left_radius=5, border_top_right_radius=5)

    def display_board(self, board: Board):
        """
        Displays the board

        :param board: a board
        :return: nothing
        """

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

        opacity_level = 220
        start_x = 0

        # STACKOVERFLOW CODE FOR TRANSPARENT RECT
        action_menu = pygame.Surface((c.WIDTH, height), pygame.SRCALPHA)
        action_menu.fill((*c.GRAY, opacity_level))
        self.screen.blit(action_menu, (start_x, c.HEIGHT - height))

    def display_contents_on_menu_screen(self, buttons: list[Button],
                                        modifications: dict[str, tuple[c.color, c.color] | Callable[..., None]],
                                        texts: list[tuple[str, int, tuple[float, float], c.color]] = ()):
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

    def display_decks(self, game: Game):
        """
        Displays the  infection and player deck images. Top numbers are the cards left on the drawing piles the bottom are
        the cards on the discard piles

        :param game: used for getting the decks
        :return: nothing
        """

        back_of_cities_resize = (120, 164)
        infection_card_position = (20, 600)
        back_of_cities_position = (140, 600)

        infection_deck_position = (60, 650)
        infection_discard_pile_position = (60, 690)
        player_deck_position = (180, 650)
        players_discard_pile_position = (180, 690)

        text_size = 40

        display_image(self.screen, infection_card_image, infection_card_position)
        display_image(self.screen, resize(back_of_cities, back_of_cities_resize), back_of_cities_position)

        write(self.screen, str(len(game.decks.infection_deck)), text_size, infection_deck_position, c.WHITE)
        write(self.screen, str(len(game.decks.infection_discard_pile)), text_size, infection_discard_pile_position, c.WHITE)

        write(self.screen, str(len(game.decks.player_deck)), text_size, player_deck_position, c.WHITE)
        write(self.screen, str(len(game.decks.players_discard_pile)), text_size, players_discard_pile_position, c.WHITE)

    def display_current_state(self, game: Game):
        """
        Displays the current state of the game

        :param game: used for getting the objects
        """
        # THE BACKGROUND IMAGE
        display_image(self.screen, background, c.top_left)

        # CURRENT PLAYER INFORMATION
        display_image(self.screen, game.current_player.image, (20, 20))
        write(self.screen, f"{game.current_player.moves}", 60, (70, 20))

        # WHEN THE PLAYER IS THE DISPATCHER
        if hasattr(game.current_player, "link"):
            control_size = 20
            control_position = (15, 80)
            link_player_image_resize = (20, 20)
            link_player_image_position = (78, 75)

            write(self.screen, "Controls:", control_size, control_position, c.BLACK)
            display_image(self.screen, resize(game.current_player.link.image, link_player_image_resize),
                          link_player_image_position)

        self.display_board(game.board)
        self.display_decks(game)
        self.display_disease_info(game.disease_info)
        game.players.draw(self.screen)

    def display_players_cards(self, players: pygame.sprite.Group):
        """
        Displays every player's hand and their respective image

        :param players: players in the game
        :return: nothing
        """

        def display_player_hand(cards: list[pygame.Surface], starting_x: float, starting_y: float):
            """
            Displays the hand of a player at specific coordinates.

            :param cards: player's cards
            :param starting_x: positional argument by x
            :param starting_y: positional argument by y
            :return:
            """

            for card in cards:
                display_image(self.screen, card, (starting_x, starting_y))
                starting_x += 170

        image_x = 10
        image_y = 50
        card_resize = (160, 222)

        for player in players:
            # DISPLAYS PLAYER IMAGE
            display_image(self.screen, player.image, (image_x, image_y + 20))

            # DISPLAYS PLAYER'S HAND
            display_player_hand([resize(card.image, card_resize) for card in player.cards], image_x + 100, image_y)
            image_y += 150

    def display_end_screen(self, end_result: str):
        """
        Displays the ending screen

        :param end_result: outcome of the game
        :return: nothing
        """

        outcome = "DEFEAT" if end_result == "Defeat" else "VICTORY"
        outcome_size = 100
        outcome_position = (600, 350)

        write(self.screen, outcome, outcome_size, outcome_position, c.GREEN)

    def display_event_cards(self, cards: list[Button], game: Game):
        """
        Displays all acquired event cards

        :param cards: the event cards as buttons
        :param game: for getting the attributes
        :return: nothing
        """

        self.display_current_state(game)
        self.display_action_menu()
        self.display_contents_on_menu_screen(cards, {})
        pygame.display.flip()

    def ask_player_to_use_event_card(self, button_factory: ButtonFactory, game: Game):
        """
        Asks the player whether they want to use an event card

        :param button_factory: for creating the yes/no buttons
        :param game: getting the game's attributes
        :return: nothing
        """

        menu_height = 800
        text_size = 50
        text_x = c.WIDTH / 3 - 70
        text_y = c.HEIGHT / 2 - 30
        yes_no_buttons = button_factory.create_yes_no_buttons()

        self.display_action_menu(menu_height)
        self.display_contents_on_menu_screen(yes_no_buttons, {}, [
            ("Do you want to use an event card?", text_size, (text_x, text_y), c.RED)])
        pygame.display.flip()

        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, game.players)
            pressed_button = self.find_pressed_button(mouse_x, mouse_y, yes_no_buttons, {})

            if pressed_button is not None:
                if pressed_button.info == "yes":
                    self.handle_event_menu(button_factory, game)

                    self.display_action_menu(menu_height)
                    self.display_contents_on_menu_screen(yes_no_buttons, {}, [
                        ("Do you want to use an event card?", text_size, (text_x, text_y), c.RED)])
                    pygame.display.flip()
                else:
                    break

    def pick_cards_for_removal(self, buttons: [Button], difference: int, players: pygame.sprite.Group,
                               modifications: dict[str, tuple[c.color, c.color] | Callable[[ImageButton], None]]) \
            -> list[CityCard | EventCard]:
        """
        Allows users to remove cards from hand. Used after the user exceeded hand limit

        :param buttons: player cards as buttons
        :param difference: the number of cards needed to be removed to get to hand limit
        :param players: all players
        :param modifications: additional display features for the buttons
        :return: list of the chosen cards
        """
        menu_height = 600

        self.display_action_menu(menu_height)
        picked_buttons: list[ImageButton] = []

        while True:
            self.display_contents_on_menu_screen(buttons, modifications)
            pygame.display.flip()
            screen_copy = self.screen.copy()

            mouse_x, mouse_y = self.get_next_input(screen_copy, players)

            pressed_button = self.find_pressed_button(mouse_x, mouse_y, buttons,
                                                      {"remove": len(picked_buttons) == difference})

            if pressed_button is not None:
                if pressed_button.info == "remove":
                    return [button.info for button in picked_buttons]
                elif isinstance(pressed_button, ImageButton):
                    if pressed_button in picked_buttons:
                        picked_buttons.remove(pressed_button)
                        modifications.pop(pressed_button.info)
                    else:
                        picked_buttons.append(pressed_button)
                        modifications[pressed_button.info] = self.highlight_buttons

    def remove_cards_from_player(self, player: Player, game: Game, button_factory: ButtonFactory, difference: int):
        """
        Forces player to choose cards to remove after exceeding hand limit

        :param player: player that needs to remove cards
        :param game: getting attributes and its functions
        :param button_factory: creating card buttons
        :param difference: cards needed to be removed
        :return: nothing
        """

        cards_per_row = 5

        card_buttons = button_factory.create_remove_menu_buttons(player.cards, cards_per_row)
        modifications = {"resume": (c.WHITE, c.RED)}

        cards = self.pick_cards_for_removal(card_buttons, difference, game.players, modifications)

        self.log_history.append(f"{player.name} removed {[card.name for card in cards]}")

        player.remove_cards(cards)
        game.decks.players_discard_pile.add_cards(cards)

    def get_city(self, game: Game, additional_requirements: list[Callable[[City], bool]]) -> City:
        """
        Returns the chosen city by the user

        :param game: get its attributes
        :param additional_requirements: additional requirements for a city if needed
        :return: the chosen city
        """

        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, game.players)
            destination = game.board.get_city_at_coordinates(mouse_x, mouse_y)

            if destination is not None and all(function(destination) for function in additional_requirements):
                break

        return destination

    def highlight_buttons(self, buttons: list[ImageButton] | ImageButton):
        """
        Displays green circle over the chosen image buttons

        :param buttons: buttons that will be highlighted
        :return: nothing
        """

        x_offset = 90
        y_offset = 125

        if type(buttons) is ImageButton:
            pygame.draw.circle(self.screen, c.GREEN,
                               (buttons.x + x_offset, buttons.y + y_offset), c.RADIUS_OF_CIRCLE)
        else:
            for button in buttons:
                pygame.draw.circle(self.screen, c.GREEN,
                                   (button.x + x_offset, button.y + y_offset), c.RADIUS_OF_CIRCLE)

    def pick_player_and_action_for_share(self, share_buttons: list[Button], game: Game) -> tuple[Player, str] | tuple[None, None]:
        """
        Player chooses another player and an action for share

        :param share_buttons: buttons to be displayed
        :param game: get its attributes and functions
        :return: returns the chosen player and the action that will be taking or Nones
        """

        chosen_player = None
        modifications = {}

        while True:
            self.display_contents_on_menu_screen(share_buttons, modifications)
            pygame.display.flip()
            screen_copy = self.screen.copy()

            mouse_x, mouse_y = self.get_next_input(screen_copy, game.players)

            if self.is_outside_of_menu(mouse_y):
                return None, None

            pressed_button = self.find_pressed_button(mouse_x, mouse_y, share_buttons,
                                                      {"Give": chosen_player is not None,
                                                       "Take": chosen_player is not None})

            if pressed_button is None:
                pass
            elif pressed_button.info == "Give" and chosen_player is not None:
                return chosen_player, "Give"
            elif pressed_button.info == "Take" and chosen_player is not None:
                return chosen_player, "Take"
            elif type(pressed_button) is ImageButton:
                if chosen_player is not None:
                    modifications.pop(chosen_player.name)
                chosen_player = game.get_player(pressed_button.info)
                modifications[chosen_player.name] = self.highlight_buttons

    def pick_cards_for_cure(self, game: Game, buttons: list[Button],
                            modifications: dict[str, tuple[c.color, c.color] | Callable[[ImageButton], None]]) -> \
            list[ImageButton] | None:
        """
        User picks cards for the cure action. They have to be the same color

        :param game: get its attributes
        :param buttons: cards as buttons to be displayed
        :param modifications: additional appearance adjustments of buttons
        :return: list of the chosen buttons or None
        """

        picked_buttons: list[ImageButton] = []
        self.display_action_menu()
        while True:
            self.display_contents_on_menu_screen(buttons, modifications)
            pygame.display.flip()
            screen_copy = self.screen.copy()

            mouse_x, mouse_y = self.get_next_input(screen_copy, game.players)

            if self.is_outside_of_menu(mouse_y):
                break

            pressed_button: Button | None = self.find_pressed_button(mouse_x, mouse_y, buttons, {
                "cure": self.are_cure_requirements_met(game, len(picked_buttons),
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
        """
         Handles the gui of sharing cards between players.

        :param game: get its attributes
        :param button_factory: used for creating buttons
        :return: nothing
        """

        players: list[tuple[str, pygame.Surface]] = [(pl.name, pl.image) for pl in game.players if
                                                     game.current_player.location == pl.location and game.current_player != pl]
        share_buttons = button_factory.create_share_buttons(players)

        self.display_current_state(game)
        self.display_action_menu()

        other_player, action = self.pick_player_and_action_for_share(share_buttons, game)

        if action is not None:
            if (game.current_player.name == "Researcher" and action == "Give") or \
                    (other_player.name == "Researcher" and action == "Take"):

                player_cards = [card for card in game.get_player("Researcher").cards if isinstance(card, CityCard)]
                buttons = button_factory.create_player_hand_buttons(player_cards)
                self.display_current_state(game)
                self.display_action_menu()
                self.display_contents_on_menu_screen(buttons, {})
                pygame.display.flip()

                screen_copy = self.screen.copy()
                while True:
                    mouse_x, mouse_y = self.get_next_input(screen_copy, game.players)

                    pressed_button = self.find_pressed_button(mouse_x, mouse_y, buttons, {})
                    if pressed_button is None:
                        continue
                    else:
                        game.share(pressed_button.info, other_player, action, self.log_history)
                        break
            else:
                game.share(None, other_player, action, self.log_history)

            if len(game.current_player.cards) > c.MAX_NUMBER_OF_CARDS:
                self.remove_cards_from_player(game.current_player, game, button_factory, 1)
            elif len(other_player.cards) > c.MAX_NUMBER_OF_CARDS:
                self.remove_cards_from_player(other_player, game, button_factory, 1)

    def handle_cure_action(self, game: Game, button_factory: ButtonFactory):
        """
        Handles the gui for the cure action

        :param game: get its attributes
        :param button_factory: used for creating buttons
        :return: nothing
        """

        buttons = button_factory.create_cure_buttons(
            [card for card in game.current_player.cards if not isinstance(card, EventCard)])

        modifications = {buttons[-1].info: (c.WHITE, c.RED)}

        self.display_current_state(game)

        picked_cards_buttons = self.pick_cards_for_cure(game, buttons, modifications)
        if picked_cards_buttons is not None:
            color = have_the_same_color([game.board.cities[button.info.name] for button in picked_cards_buttons])
            game.cure(color, self.log_history)

            used_cards = [button.info for button in picked_cards_buttons]
            game.current_player.remove_cards(used_cards)
            game.decks.players_discard_pile.add_cards(used_cards)

    def get_user_input_in_treat(self, choices: list[TextButton], players: pygame.sprite.Group) -> str | None:
        """
        Chosen color to be treated by the user

        :param choices: all possible color buttons
        :param players: players in the game
        :return: color or None
        """

        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, players)
            if self.is_outside_of_menu(mouse_y):
                return None

            disease_button = self.find_pressed_button(mouse_x, mouse_y, choices, {})
            if disease_button is not None:
                return disease_button.info

    def handle_treat_action(self, game: Game, button_factory: ButtonFactory):
        """
        Handles gui for the treat action

        :param game: used for itrs attributes and functions
        :param button_factory: for creating the treat buttons
        :return: nothing
        """

        diseases = [(colour, value) for colour, value in
                    game.board.cities[game.current_player.location].diseases.items() if
                    value > 0]
        # IF THERE IS ONLY 1 DISEASE IN A CITY
        if len(diseases) == 1:
            game.treat(diseases[0][0], self.log_history)
        # IF THERE ARE MORE, THE USER CHOOSES ONE
        else:

            text_size = 50
            text_position = c.WIDTH / 3.2, 580
            text = ("Pick what disease you want to treat", text_size, text_position, c.RED)
            choices = button_factory.create_disease_removal_options_buttons(diseases)

            self.display_current_state(game)
            self.display_action_menu()
            self.display_contents_on_menu_screen(choices,
                                                 {choice.info: (from_str_to_color(choice.info), c.WHITE) for choice in
                                                  choices}, [text])
            pygame.display.flip()

            result = self.get_user_input_in_treat(choices, game.players)

            if result:
                game.treat(result, self.log_history)

    def write_number(self, number: str, button: Button, size: int = 70):
        offset_x = 85
        offset_y = 110

        write(self.screen, number, size, (button.x + offset_x, button.y + offset_y), c.GREEN)

    def handle_forecast(self, button_factory: ButtonFactory, game: Game) -> list[City]:
        """
        Handles the gui where the player reorders the first 6 infection cards

        :param button_factory: for creating the infection cards
        :param game: get its attributes
        :return: the newly ordered cards
        """

        menu_height = 350
        text_size = 30
        texts = ["top", "bottom"]
        text_positions = [(5, 750), (1000, 750)]
        texts = [(text, text_size, text_position, c.BLACK) for text, text_position in zip(texts, text_positions)]

        infection_cards = game.decks.infection_deck.top_n_cards(6)
        infection_cities = [game.board.cities[card.name] for card in infection_cards]
        forecast_buttons = button_factory.create_forecast_buttons(infection_cities)
        modifications = {}

        self.display_current_state(game)
        self.display_action_menu(menu_height)

        self.display_contents_on_menu_screen(forecast_buttons, modifications, texts)
        pygame.display.flip()

        ordered_cards: list[City] = []
        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, game.players)
            pressed_button = self.find_pressed_button(mouse_x, mouse_y, forecast_buttons,
                                                      {"ready": len(ordered_cards) == 6})

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
        """
        Handles the gui where the user chooses the player that will be moved and to what destination

        :param button_factory: for creating the player buttons
        :param game: getting its attributes
        :return: nothing
        """

        # CHANGE THE BUTTON FACTORY FUNCTION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        player_buttons = button_factory.create_player_buttons([(player.name, player.image) for player in game.players])
        self.display_current_state(game)
        self.display_action_menu()
        self.display_contents_on_menu_screen(player_buttons, {})
        pygame.display.flip()
        chosen_player = None

        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, game.players)
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
        """
        Handles the gui for resilient population. The player will choose what card of the discard
        infection pile will be removed from the game

        :param button_factory: used for creating
        :param game:
        :return:
        """

        menu_height = 800
        infection_card_buttons = button_factory.create_rp_buttons([card.name for card in game.decks.infection_discard_pile])

        self.display_action_menu(menu_height)
        self.display_contents_on_menu_screen(infection_card_buttons, {})
        pygame.display.flip()

        screen_copy = self.screen.copy()
        while True:

            mouse_x, mouse_y = self.get_next_input(screen_copy, game.players)
            pressed_button = self.find_pressed_button(mouse_x, mouse_y, infection_card_buttons, {})
            if pressed_button is None:
                pass
            else:
                to_be_removed = pressed_button.info
                break

        for card in game.decks.infection_discard_pile:
            if card.name == to_be_removed:
                game.decks.infection_discard_pile.deck.remove(card)
                self.log_history.append(f"{to_be_removed} was removed from the game")

    def play_event_card(self, card_name: str, game: Game, button_factory: ButtonFactory):
        """
        Plays an event card based on its name

        :param card_name: name of the played card
        :param game: used to get its attributes
        :param button_factory: for creating buttons
        :return: nothing
        """

        match card_name:
            case "One quiet night":
                game.skip_next_infection_step = True
            case "Resilient population":
                self.handle_resilient_population(button_factory, game)
            case "Airlift":
                self.handle_airlift(button_factory, game)
            case "Forecast":
                ordered_cards = self.handle_forecast(button_factory, game)
                ordered_infection_cards = [InfectionCard(elem) for elem in ordered_cards]
                game.decks.infection_deck.add_to_front(ordered_infection_cards)
            case "Government grant":
                self.display_current_state(game)
                pygame.display.flip()

                city = self.get_city(game, [lambda town: not town.has_research_station()])
                game.build_research_station(city, self.log_history)

    def handle_event_menu(self, button_factory: ButtonFactory, game: Game):
        """
        Handles the gui where the player can choose to play an event card

        :param button_factory: used for creating the card buttons
        :param game: for getting its attributes
        :return: nothing
        """

        event_cards: list[EventCard] = [event_card for player in game.players for event_card in player.cards if
                                        isinstance(event_card, EventCard)]
        event_cards_buttons = button_factory.create_player_hand_buttons(event_cards)

        self.display_event_cards(event_cards_buttons, game)

        while True:
            screen_copy = self.screen.copy()
            mouse_x, mouse_y = self.get_next_input(screen_copy, game.players)
            pressed_button = self.find_pressed_button(mouse_x, mouse_y, event_cards_buttons, {})

            self.is_outside_of_menu(mouse_y)
            if pressed_button is not None:
                self.play_event_card(pressed_button.info.name, game, button_factory)

                for player in game.players:
                    if player.has(pressed_button.info.name):
                        player.cards.remove(pressed_button.info)
                        self.log_history.append(f"{player.name} used {pressed_button.info.name}")

                game.decks.players_discard_pile.add_cards([pressed_button.info])

    def pick_event_card(self, game: Game, button_factory: ButtonFactory):
        """
        Player chooses what event card to pick from the discarded piles

        :param game: for getting its attributes
        :param button_factory: for creating the event buttons
        :return: nothing
        """

        event_cards_in_discard_pile = [card for card in game.decks.players_discard_pile if isinstance(card, EventCard)]
        event_card_buttons = button_factory.create_player_hand_buttons(event_cards_in_discard_pile)

        self.display_current_state(game)
        self.display_action_menu()
        self.display_contents_on_menu_screen(event_card_buttons, {})
        pygame.display.flip()

        while True:
            mouse_x, mouse_y = self.get_next_input(self.screen, game.players)
            pressed_button = self.find_pressed_button(mouse_x, mouse_y, event_card_buttons, {})

            if pressed_button is None:
                break
            else:
                game.decks.players_discard_pile.deck.remove(pressed_button.info)
                game.current_player.additional_card = pressed_button.info
                game.current_player.moves -= 1
                break

    def handle_special_planner(self, button_factory: ButtonFactory, game: Game):
        """
        Handles the special planner action, allowing the player to either choose an event card from the player
        discard pile to keep as an additional card or play the card

        :param button_factory: for passing it to functions
        :param game: getting its attributes
        :return: nothing
        """

        if game.current_player.additional_card is None:
            self.pick_event_card(game, button_factory)
        else:
            self.play_event_card(game.current_player.additional_card.name, game, button_factory)

            del game.current_player.additional_card
            game.current_player.additional_card = None

    def handle_special_dispatcher(self, button_factory: ButtonFactory, game: Game):
        """
        Handles special dispatcher action. Player can choose what player to control

        :param button_factory: for creating the player buttons
        :param game: for getting its attributes
        :return: nothing
        """

        player_buttons = button_factory.create_player_buttons([(player.name, player.image) for player in game.players])

        self.display_current_state(game)
        self.display_action_menu()
        self.display_contents_on_menu_screen(player_buttons, {})
        pygame.display.flip()

        while True:
            mouse_x, mouse_y = self.get_next_input(self.screen, game.players)
            pressed_button = self.find_pressed_button(mouse_x, mouse_y, player_buttons, {})

            if pressed_button is None:
                break
            else:
                game.current_player.link = game.get_player(pressed_button.info)
                break

    def handle_special_op_expert(self, button_factory: ButtonFactory, game: Game):
        """
        Handles operations expert action. Player chooses a card to discard and moves to whatever city they want

        :param button_factory: for creating the player card buttons
        :param game: for getting its attributes
        :return: nothing
        """

        player_cards_buttons = button_factory.create_player_hand_buttons(
            [card for card in game.current_player.cards if isinstance(card, CityCard)])

        self.display_current_state(game)
        self.display_action_menu()
        self.display_contents_on_menu_screen(player_cards_buttons, {})
        pygame.display.flip()

        while True:
            mouse_x, mouse_y = self.get_next_input(self.screen, game.players)
            pressed_button = self.find_pressed_button(mouse_x, mouse_y, player_cards_buttons, {})

            if self.is_outside_of_menu(mouse_y):
                break

            if pressed_button is None:
                continue
            else:
                menu_height = 80
                text_size = 40
                text_coordinates = (620, 750)

                chosen_card = pressed_button.info

                self.display_current_state(game)
                self.display_action_menu(menu_height)
                write(self.screen, "Choose a city to go to", text_size, text_coordinates, c.BLACK)
                pygame.display.flip()

                while True:
                    city = self.get_city(game, [lambda elem: elem.name != game.current_player.location])

                    if city is None:
                        continue
                    else:
                        destination = city
                        game.current_player.remove_cards([chosen_card])
                        game.current_player.move(destination.x, destination.y, destination.name)
                        break

                break

    def handle_hand_action(self, button_factory: ButtonFactory, game: Game):
        """
        Handles actions in the hand menu. Currently, they are related to movement only

        :param button_factory: for creating player hand cards
        :param game: for getting its attributes
        :return: nothing
        """

        buttons = button_factory.create_hand_menu_buttons(
            [card for card in game.current_player.cards if isinstance(card, CityCard)])

        self.display_current_state(game)
        self.display_action_menu()
        self.display_contents_on_menu_screen(buttons, {})
        pygame.display.flip()

        copy_screen = self.screen.copy()
        while True:
            mouse_x, mouse_y = self.get_next_input(copy_screen, game.players)

            if self.is_outside_of_menu(mouse_y):
                break

            pressed_button = self.find_pressed_button(mouse_x, mouse_y, buttons, {})

            if pressed_button is None:
                continue
            elif pressed_button.info == "event":
                self.handle_event_menu(button_factory, game)
                break
            else:
                chosen_city = pressed_button.info
                if game.current_player.location != chosen_city.name:
                    game.move(chosen_city.name, "direct", self.log_history)

                else:
                    self.display_current_state(game)
                    pygame.display.flip()

                    destination = self.get_city(game, [])
                    game.move(destination.name, "charter", self.log_history)

                game.use_card(chosen_city)

                break

    def remove_research_station(self, game: Game):
        """
        Player chooses from which city to remove a research station

        :param game: for getting its attributes and functions
        :return: nothing
        """

        menu_height = 70
        text_size = 30
        text_position = (500, 750)

        self.display_current_state(game)
        self.display_action_menu(menu_height)
        write(self.screen, "Choose a city to remove research station", text_size, text_position, c.BLACK)
        pygame.display.flip()

        city_to_remove_research_station = self.get_city(game, [lambda town: town.has_research_station()])
        self.log_history.append(f"{city_to_remove_research_station.name} now doesn't have a research station")
        game.add_research_station()
        city_to_remove_research_station.remove_research_station()

    def handle_build_action(self, button_factory: ButtonFactory, game: Game):
        """
        Player builds a research station on their location if they have the card. If the player
        is Operations Expert they can use whatever card

        :param button_factory: for creating the op expert hand
        :param game: for getting its attributes
        :return: nothing
        """

        if game.current_player.name != "Operations Expert":
            city = next((game.board.cities[card.name] for card in game.current_player.cards if
                         card.name == game.current_player.location), None)

            if city is not None:
                game.build_research_station(city, self.log_history)
                game.played_action(game.current_player)
        else:
            buttons = button_factory.create_player_hand_buttons(
                [card for card in game.current_player.cards if isinstance(card, CityCard)])

            self.display_current_state(game)
            self.display_action_menu()
            self.display_contents_on_menu_screen(buttons, {})
            pygame.display.flip()

            copy_screen = self.screen.copy()
            while True:
                mouse_x, mouse_y = self.get_next_input(copy_screen, game.players)

                if self.is_outside_of_menu(mouse_y):
                    break

                pressed_button = self.find_pressed_button(mouse_x, mouse_y, buttons, {})

                if pressed_button is None:
                    continue
                else:
                    chosen_card: CityCard = pressed_button.info
                    game.build_research_station(game.board.cities[game.current_player.location], self.log_history)
                    game.use_card(chosen_card)

                    game.current_player.moves -= 1
                    break

        # IF RESEARCH STATIONS HAVE RUN OUT
        if game.research_station_count == 0:
            self.remove_research_station(game)

    def handle_actions_with_menu(self, button_factory: ButtonFactory, game: Game, mouse_x: float, mouse_y: float):
        """
        Used for navigation to other menus

        :param button_factory: for creating the actions
        :param game: for getting its attributes
        :param mouse_x: initial button press coordinates by x
        :param mouse_y: initial button press coordinates by y
        :return: nothing
        """

        while True:
            if self.is_outside_of_menu(mouse_y):
                break

            pressed_button = self.find_pressed_button(mouse_x, mouse_y, self.action_button_list, {
                "Treat": game.board.cities[game.current_player.location].has_diseases(),
                "Cure": game.board.cities[game.current_player.location].has_research_station(),
                "Share": game.more_than_one_person_in_city(game.current_player.location),
                "Special": game.current_player.name != "Operations Expert" or game.board.cities[
                    game.current_player.location].has_research_station()})

            if pressed_button is None:
                screen_copy = self.screen.copy()
                mouse_x, mouse_y = self.get_next_input(screen_copy, game.players)
            else:
                match pressed_button.info:
                    case "Hand":
                        print(1)
                        self.handle_hand_action(button_factory, game)
                    case "Build":
                        self.handle_build_action(button_factory, game)
                    case "Treat":
                        self.handle_treat_action(game, button_factory)
                    case "Cure":
                        self.handle_cure_action(game, button_factory)
                    case "Share":
                        self.handle_share_action(game, button_factory)
                    case "Skip":
                        game.skip()
                        self.log_history.append(f"{game.current_player.name} skipped")
                    case "Special":
                        match game.current_player.name:
                            case "Contingency Planner":
                                self.handle_special_planner(button_factory, game)
                            case "Dispatcher":
                                self.handle_special_dispatcher(button_factory, game)
                            case "Operations Expert":
                                self.handle_special_op_expert(button_factory, game)

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

    def end_turn_infect(self, game: Game, button_factory: ButtonFactory):
        """
        Deals with infection at the end of player turn

        :param game: for getting its attributes
        :param button_factory: for passing it to functions
        :return: nothing
        """

        counter = game.board.infection_rate_counter
        cards_to_take = 2 if counter < 3 else (3 if counter < 5 else 4)
        drawn_cards = game.decks.infection_deck.top_n_cards(cards_to_take)

        if not game.skip_next_infection_step:
            for card in drawn_cards:
                self.ask_player_to_use_event_card(button_factory, game)

                self.display_current_state(game)
                pygame.display.flip()
                pygame.time.wait(1000)

                target_city = game.board.cities[card.name]
                if not target_city.is_protected:
                    game.infect(target_city, from_color_to_str(target_city.color), 1, self.log_history)

                game.decks.infection_discard_pile.add_cards([card])

            game.current_player.replenish_moves()
        game.skip_next_infection_step = False

    def end_turn(self, button_factory: ButtonFactory, game: Game):
        """
        Ends player turns. The player takes 2 cards and then, depending on the number in infection rate, the game
        takes this many cards and infect these cities

        :param button_factory: for passing it to functions
        :param game: for getting its attributes and functions
        :return: nothing
        """

        drawn_cards = game.decks.player_deck.top_n_cards(2)
        self.log_history.append(f"{game.current_player.name} drew {[card.name for card in drawn_cards]}")

        self.ask_player_to_use_event_card(button_factory, game)

        self.display_current_state(game)
        pygame.display.flip()
        pygame.time.wait(100)

        for card in drawn_cards:
            if isinstance(card, EpidemicCard):
                self.ask_player_to_use_event_card(button_factory, game)

                self.log_history.append("Resolving epidemic card:")
                game.resolve_epidemic_card(self.log_history)
                drawn_cards.remove(card)
            else:
                game.current_player.draw([card])

        self.display_current_state(game)
        pygame.display.flip()
        pygame.time.wait(100)

    def initial_protection(self, game: Game):
        """
        If there is a quarantine specialist, this protects the initial cities

        :param game:
        :return:
        """
        for player in game.players:
            if player.name == "Quarantine Specialist":
                for neighbor in game.board.get_neighbors("Atlanta"):
                    neighbor.is_protected = True
                    self.log_history.append(f"{neighbor.name} is protected")
                break

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

        self.initial_protection(game)

        run = True
        while run:
            for player in game.players:
                if player.name in ("Contingency Planner", "Dispatcher", "Operations Expert"):
                    if player.name == "Contingency Planner":
                        player.additional_card = None
                    elif player.name == "Dispatcher":
                        player.link = player

                    self.action_button_list.append(TextButton(100, 600, "Special", 150, 50, "Special action", 30))

                game.current_player = player
                self.display_current_state(game)
                while player.moves > 0:
                    pygame.display.flip()

                    screen_copy = self.screen.copy()
                    mouse_x, mouse_y = self.get_next_input(screen_copy, game.players)

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
                        d = self.get_next_input(self.screen, game.players)

                self.end_turn(button_factory, game)

                end_state = game.did_end()
                if end_state != "No":
                    self.display_end_screen(end_state)
                    pygame.display.flip()
                    while True:
                        d = self.get_next_input(self.screen, game.players)

                if len(game.current_player.cards) > c.MAX_NUMBER_OF_CARDS:
                    self.remove_cards_from_player(game.current_player, game, button_factory,
                                                  len(game.current_player.cards) - c.MAX_NUMBER_OF_CARDS)

                self.action_menu_open = False

                if self.action_button_list[-1].info == "Special":
                    self.action_button_list.pop()

        pygame.quit()
