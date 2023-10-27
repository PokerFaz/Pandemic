import math
import pygame
import networkx as nx
import json
import Constants as c
import Images as I


class Button:
    def __init__(self, x, y, name, width=0, height=0, image=None, text=None, text_size=0, color=c.RED):
        if image is not None:
            self.image = image
            self.info = name
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
        else:
            self.info = name
            self.rect = pygame.Rect(x, y, width, height)
            font = pygame.font.Font(None, text_size)
            self.text = font.render(text, True, color)

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
    def __init__(self, name, color, image, x, y, has_research_station, number_of_diseases=0):
        self.name = name
        self.color = color
        self.image = image
        self.number_of_diseases = number_of_diseases
        self.has_research_station = has_research_station
        self.x = x
        self.y = y

    def __str__(self):
        return (f"{self.name} - Color: {self.color}, "
                f"Diseases: {self.number_of_diseases}")

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


def write(screen, text, text_size, x, y, color=c.RED, has_background=False):
    font = pygame.font.Font(None, text_size)
    text = font.render(text, True, color, c.WHITE if has_background else None)
    screen.blit(text, (x, y))


def draw_image(screen, image, coordinates):
    screen.blit(image, coordinates)


class Board:
    def __init__(self):
        self.cities = {}
        self.graph = nx.Graph()
        self.player_count = 0
        self.difficulty = ""
        self.outbreaks_counter = 0
        self.infection_rate_counter = 0
        self.action_menu_open = False
        self.action_button_list = []

    def add_cities(self):
        with open("cities.json") as f:
            data = json.load(f)

        # INITIALIZING THE CITIES
        for city_info in data:
            city = City(city_info["name"], city_info["color"], city_info["image"], city_info["x"], city_info["y"], True if city_info["name"] == "Atlanta" else False)
            print(city)
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

    def draw_board(self, screen):
        draw_image(screen, I.background, (0, 0))

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
            write(screen, f"{city.name}", 25, city.x - 15 if city.name != "Ho Chi Minh City" else city.x - 60, city.y + 15, c.GRAY if not city.has_research_station else c.BLACK, True)

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
                write(screen, "2", 30, x - 5, y + 20, c.BLACK)
            elif counter in range(3, 5):
                write(screen, "3", 30, x - 5, y + 20, c.BLUE)
            else:
                write(screen, "4", 30, x - 5, y + 20, c.RED)

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

    def draw_action_icons(self, screen):
        hand_button = Button(300, 550, "Hand", image=I.back_of_cities)
        hand_button.draw_button_with_image(screen)
        write(screen, "Hand", 40, 320, 710, c.BLACK)
        self.action_button_list.append(hand_button)
        build_rs_button = Button(495, 550, "Build", image=I.research_station_image)
        build_rs_button.draw_button_with_image(screen)
        write(screen, "Build", 40, 530, 710, c.BLACK)
        self.action_button_list.append(build_rs_button)

    def draw_current_board_position(self, screen, current_player, players):
        self.draw_board(screen)
        screen.blit(current_player.image, (20, 20))
        write(screen, f"{current_player.moves}", 60, 70, 20)
        players.draw(screen)

    def draw_hand(self, screen, player, players, build=False):
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
        run = True
        while run:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_y not in range(540, 800):
                        self.action_menu_open = False
                        self.draw_current_board_position(screen, player, players)

                        run = False
                        break

                    for card_button in hand:
                        # MOVE THE PLAYER TO THE CLICKED CARD'S NAME
                        if card_button.is_clicked(mouse_x, mouse_y) and player.city != card_button.info.city_name and build is False:
                            player.move(card_button.info.x, card_button.info.y, card_button.info.city_name)
                            player.cards.remove(card_button.info)
                            self.draw_current_board_position(screen, player, players)

                            run = False
                            break
                        # BUILD A RESEARCH STATION
                        elif card_button.is_clicked(mouse_x, mouse_y) and player.city == card_button.info.city_name and build is True:
                            self.cities[card_button.info.city_name].has_research_station = True
                            player.cards.remove(card_button.info)
                            player.moves -= 1
                            self.draw_current_board_position(screen, player, players)
                            run = False
                            break
                        # MOVE THE PLAYER ANYWHERE ON THE GRAPH
                        elif card_button.is_clicked(mouse_x, mouse_y) and player.city == card_button.info.city_name:
                            player.cards.remove(card_button.info)
                            self.draw_current_board_position(screen, player, players)
                            pygame.display.flip()
                            while run:
                                for event_ in pygame.event.get():
                                    if event_.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                        mouse_x, mouse_y = pygame.mouse.get_pos()

                                        for city in self.cities:
                                            distance = math.sqrt((mouse_x - self.cities[city].x) ** 2 + (mouse_y - self.cities[city].y) ** 2)
                                            if distance <= c.RADIUS_OF_CIRCLE:
                                                player.move(self.cities[city].x, self.cities[city].y, city)

                                                self.draw_current_board_position(screen, player, players)

                                                run = False
                                                break

