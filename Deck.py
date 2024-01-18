import random
import pygame.image


class Card:
    def __init__(self, card_type, name):
        self.card_type = card_type
        self.name = name

    def __str__(self):
        return f"Type: {self.card_type}"


class CityCard(Card):
    def __init__(self, city, image):
        super().__init__("City Card", city)
        self.image = image
        self.rect = self.image.get_rect()


class EpidemicCard(Card):
    def __init__(self):
        super().__init__("Epidemic Card", "epidemic_card")


class EventCard(Card):
    def __init__(self, name):
        super().__init__("Event Card", name)


class InfectionCard(Card):
    def __init__(self, city):
        super().__init__("Infection Card", city)


class Deck:
    def __init__(self):
        self.deck = []

    def __len__(self):
        return len(self.deck)

    def __str__(self):
        info = [card.name for card in self.deck]
        return str(info)

    def add_cards(self, cards):
        self.deck.extend(cards)

    def shuffle(self):
        random.shuffle(self.deck)

    def remove_top_cards(self, number_of_removed_cards):
        self.deck = self.deck[number_of_removed_cards:]

    def get_cards(self, number):
        return self.deck[:number]


class PlayerDeck(Deck):
    def __init__(self, cities):
        super().__init__()
        for city_info in cities.values():
            city_card = CityCard(city_info.name, pygame.image.load(city_info.image))
            self.deck.append(city_card)


class InfectionDeck(Deck):
    def __init__(self, cities):
        super().__init__()
        for city_info in cities.values():
            city_card = InfectionCard(city_info.name)
            self.deck.append(city_card)
