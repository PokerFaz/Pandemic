from src.misc.constants import color
from src.misc.utility import from_str_to_color


class City:
    def __init__(self, name: str, colour: str, image: str, x: int, y: int, has_research_station_: bool):
        """
        Initializes the city

        :param name: name of the city
        :param colour: color associated with the city
        :param image: image for the city
        :param x: positional argument by x
        :param y: positional argument by y
        :param has_research_station_: flag for whether the city has a research station

        Attributes:
        - diseases (dict[str, int]): mapping diseases in the city to their presence in it
        - is_protected (bool): flag for whether the city is protected from infection
        """
        self.name = name
        self.color: color = from_str_to_color(colour)
        self.image = image
        self.diseases: dict[str, int] = {
            "Red": 0,
            "Blue": 0,
            "Yellow": 0,
            "Black": 0
        }
        self.has_research_station_ = has_research_station_
        self.is_protected = False
        self.x = x
        self.y = y

    def __str__(self):
        return (f"{self.name} - Color: {self.color}, "
                f"Diseases: {self.diseases}"
                f"{self.has_research_station_}")

    def has_research_station(self) -> bool:
        """
        Checks if the city has a research station

        :return: true if it has else false
        """

        return self.has_research_station_

    def remove_research_station(self):
        """
        Removes from the city the research station

        :return: nothing
        """

        self.has_research_station_ = False

    def has_diseases(self) -> bool:
        """
        Checks if there are any disease cubes on the city

        :return: true if there are else false
        """

        return sum(self.diseases.values()) > 0

    def add_diseases(self, number: int, colour: str) -> bool:
        """
        Adds disease cubes to the city

        :param number: the number of added cubes
        :param colour: the color of the added cubes
        :return: true if there was an outbreak else false
        """

        if self.diseases[colour] + number < 4:
            self.diseases[colour] = self.diseases[colour] + number
            return False
        else:
            return True

    def remove_diseases(self, number: int, colour: str):
        """
        Removes disease cubes from the city

        :param number: the number of added cubes
        :param colour: the color of the added cubes
        :return: nothing
        """
        
        self.diseases[colour] = max(self.diseases[colour] - number, 0)
