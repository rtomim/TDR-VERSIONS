import arcade
import sys
import random
import time

WIDTH, HEIGHT = arcade.window_commands.get_display_size()


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, 'Mr. Pelussy',)
        self.name = ""
        self.player_sprite = None
        self.player_list = None

print("SPREDIN DE CUCU")