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

    def add_cards(self, cards: list[Card]):
        self.deck.extend(cards)

    def shuffle(self):
        random.shuffle(self.deck)

    def remove_top_cards(self, number_of_removed_cards: int):
        self.deck = self.deck[number_of_removed_cards:]

    def get_cards(self, number: int):
        return [city.name for city in self.deck[:number]]


class PlayerDeck(Deck):
    def __init__(self, cities: dict):
        super().__init__()
        for city_info in cities.values():
            city_card = CityCard(city_info.name, pygame.image.load(city_info.image))
            self.deck.append(city_card)

    # ADDS EPIDEMIC CARDS TO THE PLAYER DECK BASED ON THE DIFFICULTY
    def prepare_deck(self, difficulty: str):
        number_of_epidemic_cards = 4 if difficulty == "EASY" else (5 if difficulty == "NORMAL" else 6)
        cards_per_deck = int(len(self.deck) / number_of_epidemic_cards)
        epidemic_card = EpidemicCard()

        # SPLITS THE INTERVAL INTO SMALL INTERVALS BASED ON NUM OF EPIDEMIC CARDS AND RANDOMLY CHOOSES ONE NUMBER FROM EACH INTERVAL
        random_indices = [random.choice(range(start, end)) for start, end in
                          zip(range(0, len(self.deck), cards_per_deck),
                              range(cards_per_deck, len(self.deck) + 1, cards_per_deck))]

        result = []
        for i, card in enumerate(self.deck):
            if i in random_indices:
                result.append(epidemic_card)
            result.append(card)

        self.deck = result


class InfectionDeck(Deck):
    def __init__(self, cities):
        super().__init__()
        for city_info in cities.values():
            city_card = InfectionCard(city_info.name)
            self.deck.append(city_card)
