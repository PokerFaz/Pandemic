from src.misc.constants import color
from src.misc.utility import from_str_to_color, from_color_to_str


class City:
    def __init__(self, name: str, colour: str, image: str, x: int, y: int, has_research_station: bool):
        self.name = name
        self.color: color = from_str_to_color(colour)
        self.image = image
        self.diseases: dict = {
            "Red": 0,
            "Blue": 1,
            "Yellow": 0,
            "Black": 0
        }
        self.has_research_station = has_research_station
        self.x = x
        self.y = y

    def __str__(self):
        return (f"{self.name} - Color: {self.color}, "
                f"Diseases: {self.diseases}")

    def add_diseases(self, number: int, colour: color):
        colour = from_color_to_str(colour)

        if self.diseases[colour] + number < 4:
            self.diseases[colour] = self.diseases[colour] + number
            print(f"Added to {self.name} {number} cubes")
        else:
            pass  # WRITE AN OUTBREAK!!!!!!!!!!!!!!

    def remove_diseases(self, number: int, colour: str):
        self.diseases[colour] = max(self.diseases[colour] - number, 0)
