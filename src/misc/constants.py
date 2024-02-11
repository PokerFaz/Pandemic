from typing import NewType

top_left = (0, 0)
WIDTH = 1500
HEIGHT = 800
GREEN = (0, 255, 0)
DARK_GREEN = (1, 50, 32)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_YELLOW = (246, 233, 48)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
HEIGHT_PLAYER = 40
LENGTH_PLAYER = 40
RADIUS_OF_CIRCLE = 10
MAX_NUMBER_OF_CARDS = 7
MAX_NUMBER_OF_MESSAGES = 19
NUMBER_OF_INFECTION_RATE_MARKERS = 7
STARTING_LOCATION = "Atlanta"
NUMBER_OF_PLAYERS = ("2", "3", "4")
DIFFICULTIES = ("EASY", "NORMAL", "COVID19")
color = NewType("color", tuple[int, int, int])

text_size = 40
text_y = 710
action_names = [("Hand", text_size, (315, text_y), BLACK), ("Build", text_size, (530, text_y), BLACK),
                ("Treat", text_size, (755, text_y), BLACK), ("Cure", text_size, (960, text_y), BLACK),
                ("Share", text_size, (1132, text_y), BLACK), ("Skip", text_size, (1300, text_y), BLACK)]

EVENT_CARDS_NAMES = ["One quiet night", "Resilient population", "Airlift", "Forecast", "Government grant"]
