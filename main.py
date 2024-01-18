import pygame
from Button import ButtonFactory
from Board import Board, GUI
from Player import Player
from Deck import Deck, PlayerDeck, InfectionDeck
import Constants as c
import Menu
import Images as i

pygame.init()

# MAKE THE WINDOW THE SIZE OF YOUR SCREEN
screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
# CREATE THE BOARD
board = Board()
button_factory = ButtonFactory()

# STARTING SCREEN WHERE THE USER HAS TO CLICK THE START BUTTON TO CONTINUE TO THE NEXT SCREEN
start_button = button_factory.create_starting_screen_button()
Menu.display_starting_screen(screen, start_button)
Menu.wait_to_continue_to_main_menu(start_button)

wait = True
main_menu_buttons = button_factory.create_main_menu_buttons()
while wait:
    Menu.display_main_menu(screen, main_menu_buttons, str(board.player_count), board.difficulty)
    wait = Menu.wait_to_continue_to_role_menu(main_menu_buttons, board)

number_of_players = board.player_count
player_number = 1
players = pygame.sprite.Group()
role_dict = {
    "Scientist": (i.role_1, i.role_1_pin),
    "Researcher": (i.role_2, i.role_2_pin),
    "Operations Expert": (i.role_3, i.role_3_pin),
    "Contingency Planner": (i.role_4, i.role_4_pin),
    "Dispatcher": (i.role_5, i.role_5_pin),
    "Medic": (i.role_6, i.role_6_pin),
    "Quarantine Specialist": (i.role_7, i.role_7_pin)
}

role_buttons = button_factory.create_roles_menu_buttons(role_dict)  # list of (Button, int) where int is the related to what part will be the button displayed
offset_x = 0
print(role_buttons)
# PICKING AND CREATING THE PLAYERS
while player_number <= int(board.player_count):
    Menu.display_role_menu(screen, player_number, role_buttons, 1)
    role = Menu.get_user_input(role_buttons, 1)
    while type(role) is int:
        Menu.display_role_menu(screen, player_number, role_buttons, role)
        role = Menu.get_user_input(role_buttons, role)

    print(role)
    player_image = pygame.transform.scale(role_dict[role][1], (c.LENGTH_PLAYER, c.HEIGHT_PLAYER))
    player = Player(role, player_image, 285 + offset_x, 250, offset_x)
    print(player)
    players.add(player)

    player_number += 1
    offset_x -= 5

# MAKING THE FINAL SCREEN BEFORE THE START OF THE GAME
Menu.display_chosen_game_options(screen, players, board)
# CREATING THE CITY GRAPH IN THE BOARD
board.add_cities()
board.add_connections()

# CREATES THE GUI
game = GUI(screen, board)
action_buttons = button_factory.create_action_buttons()
game.action_button_list.extend(action_buttons)

# CREATING THE DECKS
player_deck = PlayerDeck(board.cities)
players_discard_pile = Deck()
player_deck.shuffle()

infection_deck = InfectionDeck(board.cities)
infection_discard_pile = Deck()
infection_deck.shuffle()

# FIRST INFECTIONS OF 9 CITIES
target_cities = infection_deck.get_cards(9)
infection_deck.remove_top_cards(9)
infection_discard_pile.add_cards(target_cities)

for i in range(9):
    city_color = board.cities[target_cities[i].name].color
    diseases = 3 if i < 3 else (2 if i < 6 else 1)
    board.cities[target_cities[i].name].add_diseases(diseases, city_color)

# DEALING CARDS TO ALL THE PLAYERS
n = 4 if int(board.player_count) == 2 else (3 if int(board.player_count) == 3 else 2)

for player in players:
    drawn_cards = player_deck.get_cards(n)

    player.draw([city.name for city in drawn_cards])
    player_deck.remove_top_cards(n)
    players_discard_pile.add_cards(drawn_cards)

    print(player)
    print(player_deck)

run = True
# GAME LOOP
while run:
    # PLAYERS TURN
    for player in players:
        game.display_current_board_position(player, players)
        while player.moves > 0:
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                mouse_x, mouse_y = pygame.mouse.get_pos()
                # ACTIONS POSSIBLE WITH MENU OFF
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game.action_menu_open is False:

                    # CHECKING TO SEE IF THE PLAYER TRIES TO OPEN THE ACTION MENU
                    if mouse_y in range(780, 800):
                        game.display_action_menu()
                        game.display_action_icons()

                        pygame.display.flip()
                    else:
                        # CHECKING IF THE PLAYER TRIES TO MOVE TO ANOTHER CITY
                        chosen_city = board.get_city_at_coordinates(mouse_x, mouse_y)
                        print(chosen_city)
                        print(player.city)
                        if chosen_city is not None and (board.has_edge(chosen_city, player.city)
                                                        or (board.cities[chosen_city].has_research_station
                                                            and board.cities[player.city].has_research_station)):
                            player.move(board.cities[chosen_city].x, board.cities[chosen_city].y, chosen_city)
                            game.display_current_board_position(player, players)
                            break

                # ACTIONS POSSIBLE WITH MENU ON
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game.action_menu_open is True:

                    # CLOSING THE MENU
                    if mouse_y not in range(540, 800):
                        game.action_menu_open = False
                        game.display_current_board_position(player, players)
                        pygame.display.flip()
                    else:
                        # CHECKING IF THE PLAYER HAS PRESSED AN ACTION BUTTON
                        for button in game.action_button_list:
                            if button.is_clicked(mouse_x, mouse_y):
                                if button.info == "Hand" or button.info == "Build":
                                    card_buttons = button_factory.create_city_buttons(board.cities, player.cards)
                                    game.display_player_hand(card_buttons)
                                    game.handle_button_action(card_buttons, button.info, player, players)
                                    game.action_menu_open = False

        player.replenish_moves()

pygame.quit()
