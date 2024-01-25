import networkx as nx
from src.misc import constants as c
from src.models.city import City
from src.misc.utility import load_json_from_file, find_file, join_path, distance_between_two_points


class Board:
    def __init__(self):
        self.cities: dict[str, City] = {}
        self.graph = nx.Graph()
        self.outbreaks_counter = 0
        self.infection_rate_counter = 0

    def add_cities(self):
        data = load_json_from_file(find_file("cities.json"))

        # INITIALIZING THE CITIES
        for city_data in data:
            image_path_parts = city_data["image"].split(",")
            image = join_path(*image_path_parts)

            city = City(city_data["name"], city_data["color"], image, city_data["x"], city_data["y"],
                        True if city_data["name"] == "Atlanta" else False)

            self.graph.add_node(city)
            self.cities[city.name] = city

    def add_connections(self):
        connections = load_json_from_file(find_file("connections.json"))

        # ADDING THE CONNECTIONS IN THE GRAPH
        for connection in connections:
            city1 = connection["city1"]
            city2 = connection["city2"]

            self.graph.add_edge(city1, city2)

    def has_edge(self, chosen_city: str, player_city: str) -> bool:
        return self.graph.has_edge(chosen_city, player_city)

    def is_shuttle_flight(self, player_city: str, destination: str) -> bool:
        return self.cities[player_city].has_research_station_ and self.cities[destination].has_research_station_

    def get_city_at_coordinates(self, mouse_x: float, mouse_y: float) -> City | None:
        for city in self.cities:
            if distance_between_two_points(mouse_x, mouse_y,
                                           self.cities[city].x, self.cities[city].y) < c.RADIUS_OF_CIRCLE:
                return self.cities[city]

        return None
