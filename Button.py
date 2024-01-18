import pygame
import Constants as c
import Images as i


class Button:
    def __init__(self, x: int, y: int, name: str):
        self.info = name
        self.clickable = True
        self.x = x
        self.y = y

    def display_button(self, screen: pygame.Surface, *args):
        pass

    def is_clicked(self, mouse_x: int, mouse_y: int):
        if not self.clickable:
            return False

        if self.is_point_inside(mouse_x, mouse_y):
            return True

        return False

    def is_point_inside(self, x: int, y: int):
        pass


class ImageButton(Button):
    def __init__(self, x: int, y: int, name: str, image: pygame.image):
        super().__init__(x, y, name)
        self.image = image
        self.info = name
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def display_button(self, screen: pygame.Surface, *args):
        screen.blit(self.image, self.rect.topleft)

    def is_point_inside(self, x: int, y: int):
        return self.rect.collidepoint(x, y)


class TextButton(Button):
    def __init__(self, x: int, y: int, name: str, width: int, height: int, text: str, text_size: int):
        super().__init__(x, y, name)
        self.rect = pygame.Rect(x, y, width, height)
        self.text_size = text_size
        self.text = text

    def display_button(self, screen: pygame.Surface, rect_color: tuple[int, int, int] = c.GRAY, text_color: tuple[int, int, int] = c.RED, transparency: int = 0):
        if transparency == 0:
            pygame.draw.rect(screen, rect_color, self.rect)

        font = pygame.font.Font(None, self.text_size)
        text = font.render(self.text, True, text_color)

        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_point_inside(self, x: int, y: int):
        return self.rect.collidepoint(x, y)


class ButtonFactory:

    @staticmethod
    def create_starting_screen_button() -> TextButton:
        play_button = TextButton(c.WIDTH / 2.4, c.HEIGHT / 2, "Play", 200, 100, text="PLAY", text_size=40)
        return play_button

    @staticmethod
    def create_main_menu_buttons():
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
    def create_roles_menu_buttons(role_dict: dict):
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
    def create_action_buttons():
        result_hand_button = [
            ImageButton(300, 550, "Hand", image=i.back_of_cities),
            ImageButton(495, 550, "Build", image=i.research_station_image)
        ]

        return result_hand_button

    @staticmethod
    def create_city_buttons(cities, player_cards) -> list[Button]:
        city_buttons = []

        x = 5
        for card in player_cards:
            card_button = ImageButton(x, 550, card, image=pygame.image.load(cities[card].image))
            city_buttons.append(card_button)
            x += 190

        return city_buttons
