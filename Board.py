import pygame
import networkx as nx
import json
import Constants as c
import Images as I


class Button:
    def __init__(self, x, y, name, width=0, height=0, image=None, text=None, text_size=0, color=c.RED):
        if image is not None:
            self.image = image
            self.name = name
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
        else:
            self.name = name
            self.rect = pygame.Rect(x, y, width, height)
            font = pygame.font.Font(None, text_size)
            self.text = font.render(text, True, color)

    def __str__(self):
        print(f"{self.name}, {self.rect}, {self.rect.topleft}")

    def draw_button(self, screen, color=c.GRAY):
        pygame.draw.rect(screen, color, self.rect)
        text_rect = self.text.get_rect(center=self.rect.center)
        screen.blit(self.text, text_rect)

    def draw_button_with_image(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            return True
        return False


class City:
    def __init__(self, name, color, x, y, is_player_here=False, number_of_diseases=0):
        self.name = name
        self.color = color
        self.is_player_here = is_player_here
        self.number_of_diseases = number_of_diseases
        self.x = x
        self.y = y

    def __str__(self):
        return (f"{self.name} - Color: {self.color}, "
                f"Player Location: {self.is_player_here}, "
                f"Diseases: {self.number_of_diseases}")

    def add_player(self):
        self.is_player_here = True

    def remove_player(self):
        self.is_player_here = False

    def add_diseases(self, number):
        if self.number_of_diseases + number < 3:
            self.number_of_diseases = self.number_of_diseases + number
        else:
            pass  # WRITE AN OUTBREAK!!!!!!!!!!!!!!

    def remove_diseases(self, number):
        if self.number_of_diseases - number > 0:
            self.number_of_diseases = self.number_of_diseases - number
        else:
            self.number_of_diseases = 0


def write(screen, text, text_size, x, y, color=c.RED):
    font = pygame.font.Font(None, text_size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


class Board:
    def __init__(self):
        self.cities = {}
        self.graph = nx.Graph()
        self.player_count = 0
        self.difficulty = ""
        self.outbreaks_counter = 0
        self.infection_rate_counter = 0
        self.action_menu_open = False
        self.button_list = []

    def add_cities(self):
        with open("cities.json") as f:
            data = json.load(f)

        # INITIALIZING THE CITIES
        for city_info in data:
            city = City(city_info["name"], city_info["color"], city_info["x"], city_info["y"])

            self.graph.add_node(city)
            self.cities[city.name] = city

    def add_connections(self):
        # READING THE CONNECTIONS
        with open("connections.json") as f:
            connections = json.load(f)

        # ADDING AND DRAWING THE CONNECTIONS IN THE GRAPH
        for connection in connections:
            city1 = self.cities.get(connection["city1"])
            city2 = self.cities.get(connection["city2"])

            self.graph.add_edge(city1, city2)

    @staticmethod
    def draw_image(screen, image, coordinates):
        screen.blit(image, coordinates)

    def draw(self, screen):
        self.draw_image(screen, I.background, (0, 0))

        # DRAWING THE EDGES OF THE GRAPH
        for city1, city2 in self.graph.edges:
            if city1.name == "San Francisco" and city2.name == "Tokyo":
                pygame.draw.line(screen, c.BLACK, (city1.x, city1.y), (0, 200), 2)
                pygame.draw.line(screen, c.BLACK, (city2.x, city2.y), (1500, 251), 2)
            elif city1.name == "San Francisco" and city2.name == "Manila":
                pygame.draw.line(screen, c.BLACK, (city1.x, city1.y), (0, 300), 2)
                pygame.draw.line(screen, c.BLACK, (city2.x, city2.y), (1500, 420), 2)
            elif city1.name == "Los Angeles" and city2.name == "Sydney":
                pygame.draw.line(screen, c.BLACK, (city1.x, city1.y), (0, 362), 2)
                pygame.draw.line(screen, c.BLACK, (city2.x, city2.y), (1500, 630), 2)
            else:
                pygame.draw.line(screen, c.BLACK, (city1.x, city1.y), (city2.x, city2.y), 2)

        # DRAWING THE CITIES
        radius = c.RADIUS_OF_CIRCLE
        for key in self.cities:
            city = self.cities[key]
            center = (city.x, city.y)
            pygame.draw.circle(screen, city.color, center, radius)

        # DRAWING THE OUTBREAKS COUNTER
        write(screen, "Outbreaks:", 43, 20, 500, c.BLACK)
        write(screen, f"{self.outbreaks_counter}", 43, 187, 503, c.GREEN)

        # DRAWING THE INFECTION RATE MARKER
        write(screen, "Infection rate", 50, 1170, 30, c.BLACK)

        counter = 0
        x = 1100
        y = 100
        while counter < 7:
            pygame.draw.circle(screen, c.DARK_GREEN if counter == self.outbreaks_counter else c.GREEN, (x, y), radius)

            if counter in range(0, 3):
                write(screen, "2", 30, x-5, y+20, c.BLACK)
            elif counter in range(3, 5):
                write(screen, "3", 30, x-5, y+20, c.BLUE)
            else:
                write(screen, "4", 30, x-5, y+20, c.RED)

            counter += 1
            x += 60

        # DRAWING THE TAB WHERE YOUR CARDS/ACTIONS ARE GOING TO BE
        pygame.draw.rect(screen, c.GRAY, (0, 780, 1500, 20), border_top_left_radius=5, border_top_right_radius=5)

    def draw_action_menu(self, screen):
        self.action_menu_open = True
        # STACKOVERFLOW CODE FOR TRANSPARENT RECT
        action_menu = pygame.Surface((1500, 260), pygame.SRCALPHA)
        action_menu.fill((128, 128, 128, 220))
        screen.blit(action_menu, (0, 540))

    def draw_actions(self, screen):
        hand_button = Button(485, 550, "Hand", image=I.back_of_cities)
        hand_button.draw_button_with_image(screen)
        self.button_list.append(hand_button)

        write(screen, "Hand", 40, 500, 710, c.BLACK)

    def draw_current_board_position(self, screen, current_player,  players):
        self.draw(screen)
        players.draw(screen)
        screen.blit(current_player.image, (20, 20))

    def draw_hand(self, screen, player, players):
        self.draw_current_board_position(screen, player, players)
        self.draw_action_menu(screen)
        hand = []
        x = 5
        for card in player.cards:
            card_button = Button(x, 550, card, image=card.image)
            card_button.draw_button_with_image(screen)
            hand.append(card_button)
            x += 190

        pygame.display.flip()
