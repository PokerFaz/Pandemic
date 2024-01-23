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

role_1 = pygame.image.load(os.path.join("assets", "Scientist.png"))
role_2 = pygame.image.load(os.path.join("assets", "Researcher.png"))
role_3 = pygame.image.load(os.path.join("assets", "OperationsExpert.png"))
role_4 = pygame.image.load(os.path.join("assets", "ContingencyPlanner.png"))
role_5 = pygame.image.load(os.path.join("assets", "Dispatcher.png"))
role_6 = pygame.image.load(os.path.join("assets", "Medic.png"))
role_7 = pygame.image.load(os.path.join("assets", "QuarantineSpecialist.png"))
role_1_pin = pygame.image.load(os.path.join("assets", "GrayPin.png"))
role_2_pin = pygame.image.load(os.path.join("assets", "BrownPin.png"))
role_3_pin = pygame.image.load(os.path.join("assets", "DarkGreenPin.png"))
role_4_pin = pygame.image.load(os.path.join("assets", "TealPin.png"))
role_5_pin = pygame.image.load(os.path.join("assets", "PinkPin.png"))
role_6_pin = pygame.image.load(os.path.join("assets", "OrangePin.png"))
role_7_pin = pygame.image.load(os.path.join("assets", "Pin.png"))

back_of_cities = pygame.image.load(os.path.join("assets", "Cities/BackOfCity.png"))
back_of_cities = pygame.transform.scale(back_of_cities, (100, 140))
research_station_image = pygame.image.load(os.path.join("assets", "ResearchStation.png"))
treat_image = pygame.image.load((os.path.join("assets", "treat.png")))
treat_image = pygame.transform.scale(treat_image, (140, 140))
