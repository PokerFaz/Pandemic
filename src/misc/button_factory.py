from src.misc.constants import WIDTH, HEIGHT, NUMBER_OF_PLAYERS, DIFFICULTIES
import src.misc.images as i
from pygame import Surface
from src.models.buttons.button import Button
from src.models.buttons.image_button import ImageButton
from src.models.buttons.text_button import TextButton
from src.models.card import CityCard, EventCard
from src.misc.utility import resize, my_enumerate


class ButtonFactory:

    @staticmethod
    def create_starting_screen_button() -> TextButton:
        play_button = TextButton(WIDTH / 2.4, HEIGHT / 2, "Play", 200, 100, text="PLAY", text_size=40)
        return play_button

    @staticmethod
    def create_main_menu_buttons() -> list[TextButton]:
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
        CREATES ROLE BUTTONS LIST THAT CONTAINS THE ROLE AND ON WHICH SCREEN THEY WILL APPEAR ON
        PLUS ADDITIONAL BUTTONS
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
    def create_city_buttons(player_cards: list[CityCard | EventCard], new_x: float = 180, new_y: float = 250,
                            per_row: int = -1) -> list[ImageButton]:
        x = 5
        city_buttons = [
            ImageButton(x + 190 * index, 550 - counter * (new_y + 40), card, image=resize(card.image, new_x, new_y))
            for counter, index, card in my_enumerate(player_cards, per_row)]

        return city_buttons

    @staticmethod
    def create_disease_removal_options_buttons(available_choices: list[tuple[str, int]]) -> list[TextButton]:
        x = 300
        # NO IDEA WHY INDEX IS TREATED AS STR
        result = [TextButton(x + 250 * int(index), 650, color, 80, 80, f'{str(number_of_diseases)}', 50) for
                  index, (color, number_of_diseases) in enumerate(available_choices)]

        return result

    @staticmethod
    def create_share_buttons(player_info: list[tuple[str, Surface]]) -> list[Button]:
        x = 5
        player_buttons: list[Button] = [ImageButton(x + 190 * int(index), 550, name, image=resize(image, 200, 200))
                                        for index, (name, image) in enumerate(player_info, start=0)]

        additional_buttons = [
            TextButton(700, 650, "Give", 100, 70, "Give", 50),
            TextButton(850, 650, "Take", 100, 70, "Take", 50)
        ]

        player_buttons.extend(additional_buttons)

        return player_buttons

    def create_cure_buttons(self, player_cards: list[CityCard | EventCard]) -> list[Button]:
        city_buttons: list[Button] = self.create_city_buttons(player_cards)
        cure_button = TextButton(1400, 650, "cure", 100, 55, "CURE", 40)
        city_buttons.append(cure_button)
        return city_buttons

    def create_remove_menu_buttons(self, player_cards: list[CityCard | EventCard], per_row: int) -> list[Button]:
        city_buttons: list[Button] = self.create_city_buttons(player_cards, per_row=per_row)
        print(player_cards)
        remove_button = TextButton(1350, 650, "remove", 120, 55, "REMOVE", 40)
        city_buttons.append(remove_button)
        return city_buttons
