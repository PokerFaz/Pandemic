from Board import Board, Button
import pygame
import Constants as c
import random
import Images as I


def write(screen, text, text_size, x, y, color=c.RED):
    font = pygame.font.Font(None, text_size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

def draw_image(screen, image, coordinates):
            screen.blit(image, coordinates)

def draw_starting_screen(screen):
            draw_image(screen, I.earth, (0, 0))
            draw_image(screen, I.logo, (450, 0))

            play_button = Button(c.WIDTH / 2.4, c.HEIGHT / 2, "Play", 200, 100, text="PLAY", text_size=40)
            play_button.draw_button(screen)

            pygame.display.flip()
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if play_button.is_clicked(mouse_x, mouse_y):
                            run = False
                            break

def draw_main_menu(screen, board):
            draw_image(screen, I.earth, (0, 0))
            draw_image(screen, I.logo, (450, 0))

            write(screen, "Number of players:", 72, c.WIDTH / 17, c.HEIGHT / 2.3)

            # PLAYER COUNT OPTIONS
            player_counts = ("2", "3", "4")
            player_count_x = c.WIDTH / 7.5
            for count in player_counts:
                color = c.GREEN if board.player_count == count else c.BLACK
                write(screen, count, 72, player_count_x, c.HEIGHT / 1.8, color)
                player_count_x += 100

            write(screen, "Difficulty:", 72, c.WIDTH / 1.62, c.HEIGHT / 2.3)

            # DRAW DIFFICULTY OPTIONS
            difficulties = ["EASY", "NORMAL", "COVID19"]
            difficulty_x = c.WIDTH / 2
            counter = 0
            for diff in difficulties:
                color = c.GREEN if board.difficulty == diff else c.BLACK
                write(screen, diff, 58, difficulty_x, c.HEIGHT / 1.8, color)

                if counter == 0:
                    difficulty_x += 200
                else:
                    difficulty_x += 260
                counter += 1

            continue_button = Button(c.WIDTH / 2.4, c.HEIGHT / 1.3, "Continue", 200, 100, text="CONTINUE", text_size=40)
            continue_button.draw_button(screen)

            pygame.display.flip()

            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        if continue_button.is_clicked(mouse_x,mouse_y) and board.player_count != 0 and board.difficulty != "":
                            run = False
                            break

                        player_count_x = c.WIDTH / 7.5
                        for count in player_counts:
                            if mouse_x in range(int(player_count_x), int(player_count_x + 25)) and mouse_y in range(
                                    int(c.HEIGHT / 1.8), int(c.HEIGHT / 1.8 + 40)):
                                run = False
                                board.player_count = count
                                draw_main_menu(screen, board)
                            player_count_x += 100

                        if mouse_y in range(442, 472):
                            if mouse_x in range(754, 847):
                                run = False
                                board.difficulty = "EASY"
                                draw_main_menu(screen, board)
                            elif mouse_x in range(952, 1117):
                                run = False
                                board.difficulty = "NORMAL"
                                draw_main_menu(screen, board)
                            elif mouse_x in range(1212, 1373):
                                run = False
                                board.difficulty = "COVID19"
                                draw_main_menu(screen, board)

def draw_role_menu_1(screen, number, role_dict):
            draw_image(screen, I.earth, (0, 0))
            write(screen, f"Choose Player {number} role:", 72, 50, 100)

            image_x = 25
            counter = 0
            role_names = ("Scientist", "Researcher", "Operations Expert", "Contingency Planner")
            role_button_list = []
            while counter < 4:
                role_button = Button(image_x, 250, role_names[counter], image=tuple(role_dict.values())[counter][0])
                role_button.draw_button_with_image(screen)
                if tuple(role_dict.values())[counter][1] != 1:
                    role_button_list.append(role_button)
                else:
                    print(f"{role_names[counter - 4]} is used")
                image_x += 400
                counter += 1

            print(role_dict)

            more_roles_button = Button(1200, 700, "More roles", 300, 100, text="More Roles", text_size=40)
            more_roles_button.draw_button(screen)

            pygame.display.flip()

            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for role in role_button_list:
                            if role.is_clicked(mouse_x, mouse_y):
                                run = False
                                return role.info

                        if more_roles_button.is_clicked(mouse_x, mouse_y):
                            run = False
                            name = draw_role_menu_2(screen, number, role_dict)
                            return name

def draw_role_menu_2(screen, number, role_dict):
            draw_image(screen, I.earth, (0, 0))
            write(screen, f"Choose Player {number} role:", 72, 50, 100)

            image_x = 25
            counter = 4
            role_names = ("Dispatcher", "Medic", "Quarantine Specialist")
            role_button_list = []
            while counter < 7:
                role_button = Button(image_x, 250, role_names[counter - 4], image=tuple(role_dict.values())[counter][0])
                role_button.draw_button_with_image(screen)
                if tuple(role_dict.values())[counter][1] != 1:
                    role_button_list.append(role_button)
                else:
                    print(f"{role_names[counter - 4]} is used")

                image_x += 400
                counter += 1

            random_card_button = Button(1225, 250, "Random", 242, 342, text="?", text_size=100, color=c.WHITE)
            random_card_button.draw_button(screen, c.BLACK)

            role_button_list.append(random_card_button)

            write(screen, "Random", 60, 1263, 300, c.WHITE)

            previous_button = Button(0, 700, "Previous", 300, 100, text="Previous Roles", text_size=40)
            previous_button.draw_button(screen)

            pygame.display.flip()

            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        if previous_button.is_clicked(mouse_x, mouse_y):
                            run = False
                            name = draw_role_menu_1(screen, number, role_dict)
                            return name

                        for role in role_button_list:
                            if role.info != "Random":
                                 if role.is_clicked(mouse_x, mouse_y):
                                    run = False
                                    return role.name
                            elif role.is_clicked(mouse_x, mouse_y):
                                run = False
                                current_available_roles = []

                                for key in role_dict:
                                    image = pygame.image.load("assets/BackOfRole.png")
                                    print(image)
                                    if role_dict[key][1] != 1:
                                        current_available_roles.append(key)

                                number = random.randint(0, len(current_available_roles) - 1)
                                return current_available_roles[number]

def draw_chosen_game_options(screen, players, board):
            draw_image(screen, I.earth, (0, 0))
            write(screen, f"Game's settings:", 60, 200, 100, c.RED)
            write(screen, f'Difficulty: {board.difficulty}', 60, 200, 200, c.GREEN)
            y = 300
            counter = 1
            for player in players:
                write(screen, f'Players {counter} role: {player.name}', 60, 200, y, c.WHITE)
                y += 100
                counter += 1

            start_button = Button(1200, 400, "start", 200, 100, text="Start?", text_size=40)
            start_button.draw_button(screen, c.GRAY)
            pygame.display.flip()

            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if start_button.is_clicked(mouse_x, mouse_y):
                            run = False
                            break