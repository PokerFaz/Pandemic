from src.misc.constants import color
from src.misc.utility import from_str_to_color


class City:
    def __init__(self, name: str, colour: str, image: str, x: int, y: int, has_research_station_: bool):
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
        self.x = x
        self.y = y

    def __str__(self):
        return (f"{self.name} - Color: {self.color}, "
                f"Diseases: {self.diseases}")

    def has_research_station(self) -> bool:
        return self.has_research_station_

    def remove_research_station(self):
        self.has_research_station_ = False

    def has_diseases(self) -> bool:
        return sum(self.diseases.values()) > 0

    def add_diseases(self, number: int, colour: str):

        if self.diseases[colour] + number < 4:
            self.diseases[colour] = self.diseases[colour] + number
            print(f"Added to {self.name} {number} cubes")
        else:
            pass  # WRITE AN OUTBREAK!!!!!!!!!!!!!!

    def remove_diseases(self, number: int, colour: str):
        self.diseases[colour] = max(self.diseases[colour] - number, 0)
