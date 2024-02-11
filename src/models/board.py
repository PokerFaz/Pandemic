import networkx as nx
from src.misc import constants as c
from src.models.city import City
from src.misc.utility import load_json_from_file, find_file, join_path, distance_between_two_points


class Board:
    def __init__(self):
        """
        Initializes the pandemic board

        Attributes:
        - cities (dict[str, City]): maps each city name to its City objects
        - graph (Graph): connected graph which represents the connection between the cities
        - outbreaks_counter (int): keeps track of the number of outbreaks
        - infection_rate_counter (int): keeps track of the current infection rate counter
        or how many cards have to be drawn in the infection phase
        """

        self.cities: dict[str, City] = {}
        self.graph = nx.Graph()
        self.outbreaks_counter = 0
        self.infection_rate_counter = 0

    def add_cities(self):
        """
        Sets up the cities dictionary attribute

        :return: nothing
        """
        data = load_json_from_file(find_file("cities.json"))

        # INITIALIZING THE CITIES
        for city_data in data:
            image_path_parts = city_data["image"].split(",")
            image = join_path(*image_path_parts)

            city = City(city_data["name"], city_data["color"], image, city_data["x"], city_data["y"],
                        True if city_data["name"] == "Atlanta" else False)

            self.cities[city.name] = city

    def add_connections(self):
        """
        Sets up the connection graph attribute

        :return: nothing
        """

        connections = load_json_from_file(find_file("connections.json"))

        # ADDING THE CONNECTIONS IN THE GRAPH
        for connection in connections:
            city1 = connection["city1"]
            city2 = connection["city2"]

            self.graph.add_edge(city1, city2)

    def has_edge(self, chosen_city: str, player_city: str) -> bool:
        """
        Checks if two cities are connected

        :param chosen_city: first city
        :param player_city: second city
        :return: true if connected else false
        """
        return self.graph.has_edge(chosen_city, player_city)

    def get_neighbors(self, city_name: str) -> list[City]:
        """
        Gets all neighbouring cities of a given city

        :param city_name: the name of the city for which we get its neighbors
        :return: list of all the city neighbors
        """

        return [self.cities[neighbor] for neighbor in self.graph.neighbors(city_name)]

    def get_city_at_coordinates(self, mouse_x: float, mouse_y: float) -> City | None:
        """
        Used for finding the city that the user tried to click.

        :param mouse_x: position of the input by x
        :param mouse_y: position of the input by y
        :return: City | None
        """
        for city in self.cities:
            if distance_between_two_points(mouse_x, mouse_y,
                                           self.cities[city].x, self.cities[city].y) < c.RADIUS_OF_CIRCLE:
                return self.cities[city]

        return None
