import pygame
import networkx
from src.models.buttons.text_button import TextButton
from src.models.buttons.image_button import ImageButton
from src.models.city import from_str_to_color
from src.models.board import Board
from src.models.city import City
from src.misc import constants as c
from src.models.buttons.button import Button
from src.models.player import Player
from src.misc.images import background
from src.misc.utility import distance_between_two_points


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
    def __init__(self, screen: pygame.Surface, board: Board):
        self.board = board
        self.screen = screen
        self.action_menu_open = False
        self.action_button_list = []

    @staticmethod
    def get_next_input() -> (int, int):
        while True:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

    def display_connecting_lines(self, edges: networkx.classes.reportviews.EdgeView):
        for city1, city2 in edges:
            if city1 == "San Francisco" and city2 == "Tokyo":
                pygame.draw.line(self.screen, c.BLACK, (self.board.cities[city1].x, self.board.cities[city1].y),
                                 (0, 200), 2)
                pygame.draw.line(self.screen, c.BLACK, (self.board.cities[city2].x, self.board.cities[city2].y),
                                 (1500, 251), 2)
            elif city1 == "San Francisco" and city2 == "Manila":
                pygame.draw.line(self.screen, c.BLACK, (self.board.cities[city1].x, self.board.cities[city1].y),
                                 (0, 300), 2)
                pygame.draw.line(self.screen, c.BLACK, (self.board.cities[city2].x, self.board.cities[city2].y),
                                 (1500, 420), 2)
            elif city1 == "Los Angeles" and city2 == "Sydney":
                pygame.draw.line(self.screen, c.BLACK, (self.board.cities[city1].x, self.board.cities[city1].y),
                                 (0, 362), 2)
                pygame.draw.line(self.screen, c.BLACK, (self.board.cities[city2].x, self.board.cities[city2].y),
                                 (1500, 630), 2)
            else:
                pygame.draw.line(self.screen, c.BLACK, (self.board.cities[city1].x, self.board.cities[city1].y),
                                 (self.board.cities[city2].x, self.board.cities[city2].y), 2)

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

    def display_outbreaks(self):
        write(self.screen, "Outbreaks:", 43, 20, 500, c.BLACK)

        write(self.screen, f"{self.board.outbreaks_counter}", 43, 187, 503, c.GREEN)

    def display_infection_rate(self):
        write(self.screen, "Infection rate", 50, 1170, 30, c.BLACK)

        counter = 0
        x = 1100
        y = 100

        while counter < 7:
            pygame.draw.circle(self.screen, c.DARK_GREEN if counter == self.board.outbreaks_counter else c.GREEN,
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

    def display_board(self):
        display_image(self.screen, background, (0, 0))

        self.display_connecting_lines(self.board.graph.edges)
        self.display_cities(self.board.cities)
        self.display_outbreaks()
        self.display_infection_rate()
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

    def display_current_board_position(self, current_player: Player, players: pygame.sprite.Group):
        self.display_board()
        self.screen.blit(current_player.image, (20, 20))
        write(self.screen, f"{current_player.moves}", 60, 70, 20)
        players.draw(self.screen)

    def display_player_hand(self, card_buttons: [Button]):
        self.display_action_menu()

        for button in card_buttons:
            button.display_button(self.screen)

        pygame.display.flip()

    def display_disease_choices(self, available_choices: list[TextButton]):
        self.display_action_menu()
        write(self.screen, "Pick what disease you want to treat", 50, c.WIDTH / 3.2, 580)

        for index in range(len(available_choices)):
            rectangle_color = from_str_to_color(available_choices[index].info)
            available_choices[index].display_button(self.screen, rect_color=rectangle_color, text_color=c.WHITE)

    def pick_a_card(self, card_buttons: list[TextButton | ImageButton]) -> str | None:
        run = True
        while run:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # PLAYER TRIES TO REMOVE THE ACTION MENU
                    if mouse_y not in range(540, 800):
                        self.action_menu_open = False
                        return None

                    for card_button in card_buttons:
                        if card_button.is_clicked(mouse_x, mouse_y):
                            return card_button.info

    def pick_a_city(self) -> str:
        while True:
            mouse_x, mouse_y = self.get_next_input()

            for city, city_data in self.board.cities.items():
                if distance_between_two_points(mouse_x, mouse_y, city_data.x, city_data.y) < c.RADIUS_OF_CIRCLE:
                    return city

    @staticmethod
    def find_pressed_button(mouse_x: int, mouse_y: int, buttons: list[TextButton | ImageButton]) -> TextButton | ImageButton | None:
        for button in buttons:
            if button.is_clicked(mouse_x, mouse_y):
                return button

        return None

    def handle_button_action(self, card_buttons: list[TextButton | Button], action: str, player: Player, players: pygame.sprite.Group):
        while True:
            mouse_x, mouse_y = self.get_next_input()

            if mouse_y not in range(540, 800):
                self.action_menu_open = False
                self.display_current_board_position(player, players)
                pygame.display.flip()
                break

            pressed_card_button = self.find_pressed_button(mouse_x, mouse_y, card_buttons)
            if pressed_card_button is not None:
                pressed_card_name = pressed_card_button.info

                if pressed_card_name == player.city and action == "Hand":
                    self.display_current_board_position(player, players)
                    pygame.display.flip()

                    mouse_x, mouse_y = self.get_next_input()

                    destination = self.board.get_city_at_coordinates(mouse_x, mouse_y)
                    target_city = self.board.cities[destination]
                    player.move(target_city.x, target_city.y, destination)

                elif pressed_card_name == player.city and action == "Build":
                    self.board.cities[pressed_card_name].has_research_station = True
                    player.moves -= 1

                elif pressed_card_name != player.city:
                    target_city = self.board.cities[pressed_card_name]
                    player.move(target_city.x, target_city.y, pressed_card_name)

                player.cards.remove(pressed_card_name)
                if player.moves != 0:
                    self.display_current_board_position(player, players)
                    pygame.display.flip()
                break
