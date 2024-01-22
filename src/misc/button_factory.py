import src.misc.constants as c
import src.misc.images as i
import pygame.image
from src.models.city import City
from src.models.buttons.image_button import ImageButton
from src.models.buttons.text_button import TextButton


class ButtonFactory:

    @staticmethod
    def create_starting_screen_button() -> TextButton:
        play_button = TextButton(c.WIDTH / 2.4, c.HEIGHT / 2, "Play", 200, 100, text="PLAY", text_size=40)
        return play_button

    @staticmethod
    def create_main_menu_buttons() -> list[TextButton]:
        player_count_x = c.WIDTH / 7.5
        result = []

        # NUMBER OF PLAYERS BUTTONS
        for count in c.NUMBER_OF_PLAYERS:
            number_button = TextButton(player_count_x, c.HEIGHT / 1.8, str(count), 22, 45, text=str(count),
                                       text_size=72)
            result.append(number_button)

            player_count_x += 100

        # DIFFICULTY BUTTONS
        difficulty_x = c.WIDTH / 2 + 50
        counter = 0
        width_offset = 0

        for diff in c.DIFFICULTIES:
            difficulty_button = TextButton(difficulty_x, c.HEIGHT / 1.8, diff, 120 + width_offset, 45, text=diff,
                                           text_size=58)

            result.append(difficulty_button)

            difficulty_x += 140 if counter == 0 else 180
            width_offset += 45 if counter < 1 else 0

            counter += 1

        continue_button = TextButton(c.WIDTH / 2.4, c.HEIGHT / 1.3, "Continue", 200, 100, text="CONTINUE", text_size=40)
        result.append(continue_button)

        return result

    @staticmethod
    def create_roles_menu_buttons(role_dict: dict[str: (pygame.image, pygame.image)]) -> list[tuple[ImageButton, int] | tuple[TextButton, int]]:
        image_x = 25
        counter = 0
        role_menu_part = 1
        buttons = []

        for role in role_dict.keys():
            role_button = ImageButton(image_x, 250, role, image=role_dict[role][0])
            buttons.append((role_button, role_menu_part))

            if counter == 3:
                image_x = 25
                role_menu_part = 2
            else:
                image_x += 400
            counter += 1

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
            ImageButton(720, 555, "Treat", image=i.treat_image)
        ]

        return result_hand_button

    @staticmethod
    def create_city_buttons(cities: dict[str: City], player_cards: list[str]) -> list[ImageButton]:
        x = 5
        city_buttons = [ImageButton(x + 190 * index, 550, card, image=pygame.image.load(cities[card].image)) for index, card in enumerate(player_cards, start=0)]

        return city_buttons

    @staticmethod
    def create_disease_removal_options_buttons(available_choices: list[tuple[str, int]]) -> list[TextButton]:
        x = 300
        result = [TextButton(x + 250 * index, 650, color, 80, 80, f'{str(number_of_diseases)}', 50) for index, (color, number_of_diseases) in enumerate(available_choices)]

        return result
