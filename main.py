import pygame
import math
from Board import Board
from Player import Player
from Deck import PlayerDeck
import Constants as c
import Menu
import Images as I

pygame.init()

# MAKE THE WINDOW THE SIZE OF YOUR SCREEN
screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
# CREATING THE BOARD
board = Board()
Menu.draw_starting_screen(screen)
Menu.draw_main_menu(screen, board)

number_of_players = board.player_count
counter = 1
players = pygame.sprite.Group()
role_dict = {
    "Scientist": (I.role_1, 0, I.role_1_pin),
    "Researcher": (I.role_2, 0, I.role_2_pin),
    "Operations Expert": (I.role_3, 0, I.role_3_pin),
    "Contingency Planner": (I.role_4, 0, I.role_4_pin),
    "Dispatcher": (I.role_5, 0, I.role_5_pin),
    "Medic": (I.role_6, 0, I.role_6_pin),
    "Quarantine Specialist": (I.role_7, 0, I.role_7_pin)
}
offset_x = 0
# PICKING AND CREATING THE PLAYERS
while counter <= int(board.player_count):
    role = Menu.draw_role_menu_1(screen, counter, role_dict)
    player_image = pygame.transform.scale(role_dict[role][2], (c.LENGTH_PLAYER, c.HEIGHT_PLAYER))
    player = Player(role, player_image, 285 + offset_x, 250)
    print(player)
    role_dict[role] = (I.back_image, 1)
    players.add(player)
    counter += 1
    offset_x -= 10

# MAKING THE FINAL SCREEN BEFORE THE START OF THE GAME
Menu.draw_chosen_game_options(screen, players, board)

# CREATING THE CITY GRAPH IN THE BOARD
board.add_cities()
board.add_connections()

# CREATING THE DECK
player_deck = PlayerDeck()
player_deck.make_starting_deck()
player_deck.shuffle()
print(player_deck)

# DEALING CARDS TO ALL THE PLAYERS
for player in players:
    player_deck.draw(player, board.player_count)
    print(player)
    print(player_deck)

# DRAWING THE INITIAL POSITION OF THE BOARD AND THE PLAYER
board.draw(screen)
players.draw(screen)
pygame.display.flip()

run = True
# GAME LOOP
while run:
    for player in players:
        action_counter = 4
        screen.blit(player.image, (20, 20))
        pygame.display.flip()

        while action_counter > 0:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # ACTIONS POSSIBLE WITH MENU OFF
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and board.action_menu_open is False:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # CHECKING TO SEE IF THE PLAYER WANTS TO OPEN THE ACTION MENU
                    if mouse_x in range(0, 1500) and mouse_y in range(780, 800):
                        board.draw_action_menu(screen)
                        board.draw_actions(screen)
                        pygame.display.flip()

                    # CHECKING IF THE PLAYER WANTS TO MOVE TO ANOTHER CITY
                    for city in board.cities:
                        distance = math.sqrt(
                            (mouse_x - board.cities[city].x) ** 2 + (mouse_y - board.cities[city].y) ** 2)
                        if distance <= c.RADIUS_OF_CIRCLE and board.graph.has_edge(board.cities[city],
                                                                                   board.cities[player.city]):
                            player.move(board.cities[city].x, board.cities[city].y)
                            board.draw_current_board_position(screen, player, players)
                            player.city = city
                            pygame.display.flip()
                            action_counter -= 1

                # ACTIONS POSSIBLE WITH MENU ON
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and board.action_menu_open is True:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # CLOSING THE MENU
                    if mouse_y not in range(540, 800):
                        go = False
                        board.action_menu_open = False
                        board.draw_current_board_position(screen, player, players)
                        pygame.display.flip()

                    # CHECKING IF THE PLAYER HAS PRESSED A BUTTON
                    for button in board.button_list:
                        if button.is_clicked(mouse_x, mouse_y):
                            if button.name == "Hand":
                                board.draw_hand(screen, player, players)
                                break
pygame.quit()
