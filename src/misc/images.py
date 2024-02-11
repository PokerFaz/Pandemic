import os
import pygame
from src.misc.constants import WIDTH, HEIGHT


background = pygame.image.load(os.path.join("assets", "PandemicMapV2.png"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
logo = pygame.image.load(os.path.join("assets", "PandemicLogo.png"))
logo = pygame.transform.scale(logo, (600, 300))
earth = pygame.image.load(os.path.join("assets", "Starting.png"))
earth = pygame.transform.scale(earth, (WIDTH, HEIGHT))
back_image = pygame.image.load(os.path.join("assets", "BackOfRole.png"))
infection_card_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Infection_card_back.png")), (120, 164))
disease_size = (30, 30)
blue_disease = pygame.transform.scale(pygame.image.load(os.path.join("assets", "blue_disease.png")), disease_size)
red_disease = pygame.transform.scale(pygame.image.load(os.path.join("assets", "red_disease.png")), disease_size)
black_disease = pygame.transform.scale(pygame.image.load(os.path.join("assets", "black_disease.png")), disease_size)
yellow_disease = pygame.transform.scale(pygame.image.load(os.path.join("assets", "yellow_disease.png")), disease_size)

role_1 = pygame.image.load(os.path.join("assets", "Scientist.png"))
role_2 = pygame.image.load(os.path.join("assets", "Researcher.png"))
role_3 = pygame.image.load(os.path.join("assets", "OperationsExpert.png"))
role_4 = pygame.image.load(os.path.join("assets", "ContingencyPlanner.png"))
role_5 = pygame.image.load(os.path.join("assets", "Dispatcher.png"))
role_6 = pygame.image.load(os.path.join("assets", "Medic.png"))
role_7 = pygame.image.load(os.path.join("assets", "QuarantineSpecialist.png"))
role_1_pin = pygame.image.load(os.path.join("assets", "GrayPin.png"))
role_2_pin = pygame.image.load(os.path.join("assets", "BrownPin.png"))
role_3_pin = pygame.image.load(os.path.join("assets", "Pin.png"))
role_4_pin = pygame.image.load(os.path.join("assets", "TealPin.png"))
role_5_pin = pygame.image.load(os.path.join("assets", "PinkPin.png"))
role_6_pin = pygame.image.load(os.path.join("assets", "OrangePin.png"))
role_7_pin = pygame.image.load(os.path.join("assets", "DarkGreenPin.png"))

epidemic_image = pygame.image.load(os.path.join("assets", "Epidemic_P.png"))
back_of_cities = pygame.image.load(os.path.join("assets", "Cities/BackOfCity.png"))
back_of_cities = pygame.transform.scale(back_of_cities, (100, 140))
research_station_image = pygame.image.load(os.path.join("assets", "ResearchStation.png"))
treat_image = pygame.image.load((os.path.join("assets", "treat.png")))
treat_image = pygame.transform.scale(treat_image, (140, 140))
flask = pygame.image.load(os.path.join("assets", "flask.png"))
flask_image = pygame.transform.scale(flask, (140, 140))
exchange = pygame.image.load(os.path.join("assets", "exchange.png"))
exchange_image = pygame.transform.scale(exchange, (180, 180))
event_pngs = ["OneQuietNight_E.png", "ResilientPopulation_E.png", "Airlift_E.png", "Forecast_E.png", "GovernmentGrant_E.png"]
event_card_images = [pygame.image.load(os.path.join("assets", event_png)) for event_png in event_pngs]
