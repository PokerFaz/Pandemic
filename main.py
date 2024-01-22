from src.misc.button_factory import ButtonFactory
from src.gui.gui import GUI
from src.controllers.game import Game
from src.gui.menu import Menu

button_factory = ButtonFactory()
game = Game()

menu = Menu()
menu.start(game, button_factory)

game.setup()

game_gui = GUI(menu.screen, game.board)
action_buttons = button_factory.create_action_buttons()
game_gui.action_button_list.extend(action_buttons)

game.start_loop(game_gui, button_factory)
