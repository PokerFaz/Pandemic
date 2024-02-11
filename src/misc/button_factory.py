from src.misc.constants import WIDTH, HEIGHT, NUMBER_OF_PLAYERS, DIFFICULTIES
import src.misc.images as i
from pygame import Surface
from src.models.buttons.button import Button
from src.models.buttons.image_button import ImageButton
from src.models.buttons.text_button import TextButton
from src.models.city import City
from src.models.card import CityCard, EventCard
from src.misc.utility import load_image, resize, my_enumerate


class ButtonFactory:

    @staticmethod
    def create_yes_no_buttons() -> list[TextButton]:
        """
        Creates "Yes" and "No" buttons

        :return: the buttons
        """

        yes_button = TextButton(WIDTH / 1.8 - 70, HEIGHT / 2 + 20, "yes", 50, 30, "Yes", 40)
        no_button = TextButton(WIDTH - WIDTH / 1.8 - 70, HEIGHT / 2 + 20, "no", 50, 30, "No", 40)
        return [yes_button, no_button]

    @staticmethod
    def create_starting_screen_buttons() -> TextButton:
        """
        Creates the buttons for the starting screen

        :return: the buttons
        """

        play_button = TextButton(WIDTH / 2.4, HEIGHT / 2, "Play", 200, 100, text="PLAY", text_size=40)
        return play_button

    @staticmethod
    def create_main_menu_buttons() -> list[TextButton]:
        """
        Creates buttons for the main menu

        :return: the buttons
        """

        player_count_x = WIDTH / 7.5
        result = [
            TextButton(player_count_x + 100 * index, HEIGHT / 1.8, str(count), 22, 45, text=str(count), text_size=72)
            for index, count in enumerate(NUMBER_OF_PLAYERS)]

        # DIFFICULTY BUTTONS
        difficulty_x = WIDTH / 2 + 50
        counter = 0
        width_offset = 0

        for diff in DIFFICULTIES:
            difficulty_button = TextButton(difficulty_x, HEIGHT / 1.8, diff, 120 + width_offset, 45, text=diff,
                                           text_size=58)

            result.append(difficulty_button)

            difficulty_x += 140 if counter == 0 else 180
            width_offset += 45 if counter < 1 else 0

            counter += 1

        continue_button = TextButton(WIDTH / 2.4, HEIGHT / 1.3, "Continue", 200, 100, text="CONTINUE", text_size=40)
        result.append(continue_button)

        return result

    @staticmethod
    def create_roles_menu_buttons(role_dict: dict[str, (Surface, Surface)]) -> list[tuple[ImageButton, int] | tuple[TextButton, int]]:
        """
        Creates the buttons for the role menu. Depending on the part of the screen, it will return different buttons

        :param role_dict: the roles that will be made as buttons
        :return: the buttons
        """

        image_x = 25
        role_menu_part = 1
        buttons = []

        for counter, role in enumerate(role_dict.keys()):
            role_button = ImageButton(image_x, 250, role, image=role_dict[role][0])
            buttons.append((role_button, role_menu_part))

            # ROLES ARE SPLIT BECAUSE OF 2 SCREENS
            if counter == 3:
                image_x = 25
                role_menu_part += 1
            else:
                image_x += 400

        additional_buttons = [(TextButton(1225, 250, "Random", 242, 342, text="?", text_size=100), 2),
                              (TextButton(1200, 700, "More roles", 300, 100, text="More Roles", text_size=40), 1),
                              (TextButton(0, 700, "Previous", 300, 100, text="Previous Roles", text_size=40), 2)]

        buttons.extend(additional_buttons)
        return buttons

    @staticmethod
    def create_action_buttons() -> list[ImageButton]:
        """
        Creates the action buttons

        :return: the buttons
        """

        result_hand_button = [
            ImageButton(300, 550, "Hand", image=i.back_of_cities),
            ImageButton(495, 550, "Build", image=i.research_station_image),
            ImageButton(720, 555, "Treat", image=i.treat_image),
            ImageButton(920, 550, "Cure", image=i.flask_image),
            ImageButton(1080, 540, "Share", image=i.exchange_image),
            ImageButton(1250, 550, "Skip", image=i.treat_image)
        ]

        return result_hand_button

    @staticmethod
    def create_player_hand_buttons(player_cards: list[CityCard | EventCard], new_x: float = 180, new_y: float = 250,
                                   per_row: int = -1) -> list[ImageButton]:
        """
        Creates buttons from the player hand

        :param player_cards: player's cards
        :param new_x: the position by x
        :param new_y: the position by y
        :param per_row: the number of rows needed to display the buttons
        :return: the buttons
        """

        x = 5
        city_buttons = [
            ImageButton(x + 190 * index, 550 - counter * (new_y + 40), card, image=resize(card.image, (new_x, new_y)))
            for counter, index, card in my_enumerate(player_cards, per_row)]

        return city_buttons

    def create_hand_menu_buttons(self, player_cards: list[CityCard | EventCard]) -> list[Button]:
        """
        Creates the buttons for the hand action

        :param player_cards: player's cards
        :return: the buttons
        """

        buttons: list[Button] = self.create_player_hand_buttons(player_cards)
        buttons.append(TextButton(1320, 650, "event", 178, 50, "Show event cards", 30))

        return buttons

    @staticmethod
    def create_disease_removal_options_buttons(available_choices: list[tuple[str, int]]) -> list[TextButton]:
        """
        Creates buttons for the treat action

        :param available_choices: the disease that will be made as buttons
        :return: the buttons
        """

        x = 300

        result = [TextButton(x + 250 * int(index), 650, color, 80, 80, f'{str(number_of_diseases)}', 50) for
                  index, (color, number_of_diseases) in enumerate(available_choices)]

        return result

    @staticmethod
    def create_player_buttons(player_info: list[tuple[str, Surface]]) -> list[ImageButton]:
        """
        Creates players' icon buttons

        :param player_info: represent their name and their pin image
        :return: the buttons
        """

        x = 5
        player_buttons: list[ImageButton] = [ImageButton(x + 190 * int(index), 550, name, image=resize(image, (200, 200)))
                                             for index, (name, image) in enumerate(player_info, start=0)]

        return player_buttons

    def create_share_buttons(self, players_info: list[tuple[str, Surface]]) -> list[Button]:
        """
        Creates buttons for the share action

        :param players_info: players' name and pin image
        :return: the buttons
        """

        buttons: list[Button] = self.create_player_buttons(players_info)

        additional_buttons = [
            TextButton(700, 650, "Give", 100, 70, "Give", 50),
            TextButton(850, 650, "Take", 100, 70, "Take", 50)
        ]

        buttons.extend(additional_buttons)

        return buttons

    def create_cure_buttons(self, player_cards: list[CityCard | EventCard]) -> list[Button]:
        """
        Creates cure buttons

        :param player_cards: player's cards
        :return: the buttons
        """

        city_buttons: list[Button] = self.create_player_hand_buttons(player_cards)
        cure_button = TextButton(1400, 650, "cure", 100, 55, "CURE", 40)
        city_buttons.append(cure_button)
        return city_buttons

    def create_remove_menu_buttons(self, player_cards: list[CityCard | EventCard], per_row: int) -> list[Button]:
        """
        Creates buttons for the remove cards menu

        :param player_cards: player's cards
        :param per_row: rows needed to display the cards
        :return: the buttons
        """

        city_buttons: list[Button] = self.create_player_hand_buttons(player_cards, per_row=per_row)
        print(player_cards)
        remove_button = TextButton(1350, 650, "remove", 120, 55, "REMOVE", 40)
        city_buttons.append(remove_button)
        return city_buttons

    @staticmethod
    def create_forecast_buttons(infection_cards: list[City]) -> list[Button]:
        """
        Creates buttons for the forecast event card

        :param infection_cards: the cards that will be turned into buttons
        :return: the buttons
        """
        starting_x = 5
        forecast_buttons: list[Button] = [ImageButton(starting_x + index * 190, 500, card, load_image(card.image)) for index, card in enumerate(infection_cards)]
        forecast_buttons.append(TextButton(1300, 600, "ready", 100, 50, "Ready", 40))

        return forecast_buttons

    @staticmethod
    def create_rp_buttons(infection_card_names: list[str]) -> list[TextButton]:
        """
        Creates buttons for resilient population event card

        :param infection_card_names: information about all discarded infection cards
        :return: the buttons
        """

        starting_x = 5
        starting_y = 5
        result = [TextButton(starting_x + index * 210, starting_y + counter * 55, name, 190, 50, name, 30)
                  for counter, index, name in my_enumerate(infection_card_names, 7)]

        return result
