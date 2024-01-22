import math
import os
import networkx as nx
from src.misc import constants as c
from src.models.city import City
from src.misc.utility import load_json_from_file


def distance_between_click_and_city(mouse_x: int, mouse_y: int, city_x: int, city_y: int):
    return math.sqrt((mouse_x - city_x) ** 2 + (mouse_y - city_y) ** 2)


class Board:
    def __init__(self):
        self.cities: dict = {}
        self.graph = nx.Graph()
        self.outbreaks_counter = 0
        self.infection_rate_counter = 0

    def add_cities(self):
        data = load_json_from_file("cities.json")

        # INITIALIZING THE CITIES
        for city_data in data:
            image = os.path.join(*city_data["image"].split(","))

            city = City(city_data["name"], city_data["color"], image, city_data["x"], city_data["y"],
                        True if city_data["name"] == "Atlanta" else False)

            self.graph.add_node(city)
            self.cities[city.name] = city

    def add_connections(self):
        connections = load_json_from_file("connections.json")

        # ADDING THE CONNECTIONS IN THE GRAPH
        for connection in connections:
            city1 = connection["city1"]
            city2 = connection["city2"]

            self.graph.add_edge(city1, city2)

    def has_edge(self, chosen_city: str, player_city: str) -> bool:
        return self.graph.has_edge(chosen_city, player_city)

    def get_city_at_coordinates(self, mouse_x: int, mouse_y: int) -> str | None:
        for city in self.cities:
            if distance_between_click_and_city(mouse_x, mouse_y, self.cities[city].x,
                                               self.cities[city].y) < c.RADIUS_OF_CIRCLE:
                return city
