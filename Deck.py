import json
import random

import pygame.image


class Card:
    def __init__(self, card_type):
        self.card_type = card_type

    def __str__(self):
        return f"Type: {self.card_type}"


class CityCard(Card):
    def __init__(self, city_name, image, x, y):
        super().__init__("City Card")
        self.city_name = city_name
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()



class EpidemicCard(Card):
    def __init__(self):
        super().__init__("Epidemic Card")


class EventCard(Card):
    def __init__(self, name):
        super().__init__("Event Card")
        self.name = name


class InfectionCard(Card):
    def __init__(self, city):
        super().__init__("Infection Card")
        self.city = city


class PlayerDeck:
    def __init__(self):
        self.deck = []

    def __len__(self):
        return len(self.deck)

    def __str__(self):
        info = []
        for card in self.deck:
            info.append(card.city_name)

        return f"{info[0:]}"

    def make_starting_deck(self):
        with open("cities.json") as f:
            data = json.load(f)

        for city_info in data:
            city_card = CityCard(city_info["name"], pygame.image.load(city_info["image"]), city_info["x"], city_info["y"])
            self.deck.append(city_card)

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self, player, player_count):
        if int(player_count) == 2:
            number = 4
        elif int(player_count) == 3:
            number = 3
        else:
            number = 2

        player.cards.extend(self.deck[0:number])
        while number > 0:
            self.deck.pop(0)
            number -= 1


class InfectionDeck:
    pass
