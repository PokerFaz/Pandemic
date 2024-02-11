from src.models.buttons.text_button import TextButton
from src.models.buttons.image_button import ImageButton
from src.models.player import Player
from src.controllers.game import Game
from src.misc.button_factory import ButtonFactory
from src.gui.gui import write, display_image
from src.misc import constants as c, images as i
import random
import pygame


class Menu:
    def __init__(self):
        """
        Initializes menu object

        Attributes:
        screen (pygame.Surface) - the main screen where objects will be displayed
        """
        self.screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

    def start(self, game: Game, button_factory: ButtonFactory):
        """
        Initializes the starting sequence of the game

        :param game: passing it to functions
        :param button_factory: passing it to functions
        :return: nothing
        """

        pygame.init()

        self.setup_starting_screen(button_factory)
        self.setup_main_menu(button_factory, game)
        self.setup_role_menu(game, button_factory)
        self.setup_final_screen(game.players, game)

    def setup_starting_screen(self, button_factory: ButtonFactory):
        """
        Sets up the starting screen of the game

        :param button_factory: for creating the start button
        :return: nothing
        """

        start_button = button_factory.create_starting_screen_buttons()
        self.display_starting_screen(start_button)
        self.loop_starting_screen(start_button)

    def display_starting_screen(self, button: TextButton):
        """
        Displays the starting menu screen

        :param button: the start button to be displayed
        :return: nothing
        """

        display_image(self.screen, i.earth, (0, 0))
        display_image(self.screen, i.logo, (450, 0))

        button.display_button(self.screen)

        pygame.display.flip()

    @staticmethod
    def loop_starting_screen(button: TextButton):
        """
        Handles the event loop for the starting screen

        :param button: the start button
        :return: nothing
        """

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button.is_clicked(mouse_x, mouse_y):
                        run = False
                        break

    def setup_main_menu(self, button_factory: ButtonFactory, game: Game):
        """
        Sets up the main menu

        :param button_factory: for creating the menu buttons
        :param game: for getting its attributes
        :return: nothing
        """

        wait = True
        main_menu_buttons = button_factory.create_main_menu_buttons()

        while wait:
            self.display_main_menu(main_menu_buttons, str(game.player_count), game.difficulty)
            wait = self.handle_main_menu_loop(main_menu_buttons, game)

    def display_main_menu(self, buttons: [TextButton], player_size: str, difficulty: str):
        """
        Display the main menu

        :param buttons: all main menu buttons
        :param player_size: the chosen current number of players
        :param difficulty: the chosen current difficulty
        :return: nothing
        """

        display_image(self.screen, i.earth, (0, 0))
        display_image(self.screen, i.logo, (450, 0))

        for button in buttons[:-1]:
            color = c.BLACK
            if button.info == player_size or button.info == difficulty:
                color = c.GREEN
            button.display_button(self.screen, text_color=color, transparency=255)

        buttons[-1].display_button(self.screen)

        write(self.screen, "Number of players:", 72, (c.WIDTH / 17, c.HEIGHT / 2.3))
        write(self.screen, "Difficulty:", 72, (c.WIDTH / 1.62, c.HEIGHT / 2.3))

        pygame.display.flip()

    @staticmethod
    def handle_main_menu_loop(buttons: [TextButton], game: Game) -> bool:
        """
        Handles the event loop of the main menu.

        :param buttons: all main menu buttons
        :param game: for getting its attributes
        :return: true if the player hasn't pressed the continue button else false
        """
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    for button in buttons:
                        if button.is_clicked(mouse_x, mouse_y) and button.info == "Continue":
                            if game.player_count == 0 or game.difficulty == "":
                                break
                            else:
                                return False
                        elif button.is_clicked(mouse_x, mouse_y) and button.info in ("2", "3", "4"):
                            game.player_count = int(button.info)
                            return True
                        elif button.is_clicked(mouse_x, mouse_y):
                            game.difficulty = button.info
                            return True

    def setup_role_menu(self, game: Game, button_factory: ButtonFactory):
        """
        Sets up the role menu

        :param game: for getting its attributes
        :param button_factory: for creating role menu buttons
        :return: nothing
        """
        role_dict = {
            "Scientist": (i.role_1, i.role_1_pin),
            "Researcher": (i.role_2, i.role_2_pin),
            "Operations Expert": (i.role_3, i.role_3_pin),
            "Contingency Planner": (i.role_4, i.role_4_pin),
            "Dispatcher": (i.role_5, i.role_5_pin),
            "Medic": (i.role_6, i.role_6_pin),
            "Quarantine Specialist": (i.role_7, i.role_7_pin)
        }

        offset_x = 0
        player_number = 1

        role_buttons = button_factory.create_roles_menu_buttons(role_dict)

        while player_number <= int(game.player_count):
            self.display_role_menu(player_number, role_buttons, 1)
            role = self.get_user_input_for_role_menu(role_buttons, 1)

            while type(role) is int:
                self.display_role_menu(player_number, role_buttons, role)
                role = self.get_user_input_for_role_menu(role_buttons, role)

            player_image = pygame.transform.scale(role_dict[role][1], (c.LENGTH_PLAYER, c.HEIGHT_PLAYER))
            player = Player(role, player_image, 285 + offset_x, 250, offset_x)
            game.players.add(player)

            player_number += 1
            offset_x -= 5

    def display_role_menu(self, player_number: int, buttons: list[tuple[ImageButton, int] | tuple[TextButton, int]], part):
        """
        Displays the role menu. It has two parts

        :param player_number: number of players in the game
        :param buttons: buttons to be displayed
        :param part: part of the display
        :return: nothing
        """
        display_image(self.screen, i.earth, (0, 0))
        write(self.screen, f"Choose Player {player_number} role:", 72, (50, 100))

        for (button, button_part) in buttons:
            if button_part == part:
                button.display_button(self.screen) if button.info != "Random" else button.display_button(self.screen,
                                                                                                         rect_color=c.BLACK,
                                                                                                         text_color=c.WHITE)

        if part == 2:
            write(self.screen, "Random", 60, (1263, 300), c.WHITE)

        pygame.display.flip()

    @staticmethod
    def get_user_input_for_role_menu(buttons: list[tuple[ImageButton, int] | tuple[TextButton, int]], part: int) -> int | str:
        """
        Gets the user input depending on the part. It can return:
         - number: if it switches to another part of the role menu
         - role name: the name of the role or random if the user wants a random character

        :param buttons: for checking if they are pressed
        :param part: what part of the role menu are we in
        :return: str or int for switching between parts of the role menu or the role's name
        """

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    for (button, button_part) in buttons:
                        if button_part == part:
                            if button.is_clicked(mouse_x, mouse_y) and button.info == "More roles":
                                return 2
                            elif button.is_clicked(mouse_x, mouse_y) and button.info == "Previous":
                                return 1
                            elif button.is_clicked(mouse_x, mouse_y) and button.info == "Random":
                                current_available_roles = [button for button, button_part in buttons if
                                                           button.info not in (
                                                               "More roles", "Previous", "Random", "taken")]

                                chosen_button = random.choice(current_available_roles)

                                result = chosen_button.info
                                chosen_button.info = "taken"
                                chosen_button.image = i.back_image
                                chosen_button.clickable = False
                                return result
                            elif button.is_clicked(mouse_x, mouse_y):
                                result = button.info
                                button.info = "taken"
                                button.image = i.back_image
                                button.clickable = False
                                return result

    def setup_final_screen(self, players: pygame.sprite.Group, game: Game):
        """
        Sets up the final screen that displays the game's difficulty and players

        :param players: players in the game
        :param game: for getting its attributes
        :return: nothing
        """

        start_button = TextButton(1200, 400, "start", 200, 100, text="Start?", text_size=40)
        self.display_chosen_game_options(players, game.difficulty, start_button)
        self.loop_final_screen(start_button)

    def display_chosen_game_options(self, players: pygame.sprite.Group, difficulty: str, start_button: TextButton):
        """
        Display final screen

        :param players: all the players in the game
        :param difficulty: difficulty of the game
        :param start_button: the start button to start the actual game
        :return: nothing
        """

        display_image(self.screen, i.earth, (0, 0))
        write(self.screen, f"Game's settings:", 60, (200, 100), c.RED)
        write(self.screen, f'Difficulty: {difficulty}', 60, (200, 200), c.GREEN)

        y = 300
        counter = 1
        for player in players:
            write(self.screen, f'Players {counter} role: {player.name}', 60, (200, y), c.WHITE)
            y += 100
            counter += 1

        start_button.display_button(self.screen, c.GRAY)

        pygame.display.flip()

    @staticmethod
    def loop_final_screen(start_button: TextButton):
        """
        Handles the final screen event loop

        :param start_button: the button for continuing the game
        :return: nothing
        """
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if start_button.is_clicked(mouse_x, mouse_y):
                        run = False
                        break
