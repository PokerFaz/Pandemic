from Button import TextButton
from Board import Board, write, display_image
import pygame
import Constants as c
import random
import Images as i


def display_starting_screen(screen: pygame.Surface, button):
    display_image(screen, i.earth, (0, 0))
    display_image(screen, i.logo, (450, 0))

    button.display_button(screen)

    pygame.display.flip()


def wait_to_continue_to_main_menu(button: TextButton):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button.is_clicked(mouse_x, mouse_y):
                    run = False
                    break


def display_main_menu(screen: pygame.Surface, buttons: [TextButton], player_size: str, difficulty: str):
    display_image(screen, i.earth, (0, 0))
    display_image(screen, i.logo, (450, 0))

    for button in buttons[:-1]:
        color = c.BLACK
        if button.info == player_size or button.info == difficulty:
            color = c.GREEN
        button.display_button(screen, text_color=color, transparency=255)
    buttons[-1].display_button(screen)

    write(screen, "Number of players:", 72, c.WIDTH / 17, c.HEIGHT / 2.3)
    write(screen, "Difficulty:", 72, c.WIDTH / 1.62, c.HEIGHT / 2.3)

    pygame.display.flip()


def wait_to_continue_to_role_menu(buttons: [TextButton], board: Board) -> bool:
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for button in buttons:
                    if button.is_clicked(mouse_x, mouse_y) and button.info == "Continue":
                        if board.player_count == 0 or board.difficulty == "":
                            break
                        else:
                            return False
                    elif button.is_clicked(mouse_x, mouse_y) and button.info in ("2", "3", "4"):
                        board.player_count = int(button.info)
                        return True
                    elif button.is_clicked(mouse_x, mouse_y):
                        board.difficulty = button.info
                        return True


def get_user_input(buttons, part):

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for (button, button_part) in buttons:
                    if button_part == part:
                        if button.is_clicked(mouse_x, mouse_y) and button.info == "More roles":
                            return 2
                        elif button.is_clicked(mouse_x, mouse_y) and button.info == "Previous":
                            return 1
                        elif button.is_clicked(mouse_x, mouse_y) and button.info == "Random":
                            current_available_roles = [button for button, button_part in buttons if
                                                       button.info not in ("More roles", "Previous", "Random", "taken")]
                            print([role.info for role in current_available_roles])
                            chosen_button = random.choice(current_available_roles)
                            print(chosen_button.info)
                            result = chosen_button.info
                            chosen_button.info = "taken"
                            chosen_button.image = i.back_image
                            chosen_button.clickable = False
                            return result
                        elif button.is_clicked(mouse_x, mouse_y):
                            result = button.info
                            button.info = "taken"
                            button.image = i.back_image
                            button.clickable = False
                            return result


def display_role_menu(screen, player_number, buttons, part):
    display_image(screen, i.earth, (0, 0))
    write(screen, f"Choose Player {player_number} role:", 72, 50, 100)

    for (button, button_part) in buttons:
        if button_part == part:
            button.display_button(screen) if button.info != "Random" else button.display_button(screen, rect_color=c.BLACK, text_color=c.WHITE)

    if part == 2:
        write(screen, "Random", 60, 1263, 300, c.WHITE)

    pygame.display.flip()


def display_chosen_game_options(screen, players, board):
    display_image(screen, i.earth, (0, 0))
    write(screen, f"Game's settings:", 60, 200, 100, c.RED)
    write(screen, f'Difficulty: {board.difficulty}', 60, 200, 200, c.GREEN)
    y = 300
    counter = 1
    for player in players:
        write(screen, f'Players {counter} role: {player.name}', 60, 200, y, c.WHITE)
        y += 100
        counter += 1

    start_button = TextButton(1200, 400, "start", 200, 100, text="Start?", text_size=40)
    start_button.display_button(screen, c.GRAY)

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
