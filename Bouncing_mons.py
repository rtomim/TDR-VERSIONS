import arcade
import random
import sys
import time

'''
width=1280, height=720 (Fullscreen)
'''
WIDTH, HEIGHT = arcade.window_commands.get_display_size()
SPRITE_SCALING_PLAYER = 1
SPRITE_SCALING_POKEMON = 1
POKEMON_COUNT = 50
POKEMON_FILES = ["Corsola_RZ.png", "Eevee_RZ.png", "Snorlax_RZ.png", "Espeon_RZ.png", "Jumpluff_RZ.png",
                 "Mudkip_RZ.png", "Oddish_RZ.png", "Pikachu_RZ.png", "Pichu_RZ.png"]


class Pokemon(arcade.Sprite):

    def __init__(self, filename, scaling_factor):
        super().__init__(filename, scaling_factor)

        self.change_x = 0
        self.change_y = 0

    def update(self):

        if self.right + self.change_x > WIDTH:
            self.right = WIDTH
        elif self.left + self.change_x < 0:
            self.left = 0
        else:
            self.center_x += self.change_x

        if self.top + self.change_y > HEIGHT:
            self.top = HEIGHT
        elif self.bottom + self.change_y < 0:
            self.bottom = 0
        else:
            self.center_y += self.change_y

        if self.left == 0:
            self.change_x *= -1
        if self.right == WIDTH:
            self.change_x *= -1
        if self.top == HEIGHT:
            self.change_y *= -1
        if self.bottom == 0:
            self.change_y *= -1


class Game(arcade.Window):
    # class that represents the main window of the game

    def __init__(self):
        # initializer
        super().__init__(WIDTH, HEIGHT, 'Bouncing \'Mons', fullscreen=True)
        arcade.set_background_color(arcade.color.WISTERIA)
        self.yay_sound = arcade.load_sound("emerald_0214.wav")
        self.catch_sound = arcade.load_sound("emerald_000A.wav")

        self.player_sprite = None
        self.player_list = None
        self.pokemon_list = None
        self.set_mouse_visible(False)
        self.score = 0
        self.waiting = False
        self.start_time = 0

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.pokemon_list = arcade.SpriteList()

        self.score = 0
        self.waiting = False

        self.player_sprite = arcade.Sprite("Pinball_RS_Poké_Ball.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for pokemon in range(POKEMON_COUNT):

            pokemon = Pokemon(POKEMON_FILES[random.randrange(len(POKEMON_FILES))], SPRITE_SCALING_POKEMON)
            pokemon.center_x = random.randrange(WIDTH)
            pokemon.center_y = random.randrange(HEIGHT)
            while pokemon.change_x == 0 and pokemon.change_y == 0:
                pokemon.change_x = random.randrange(-4, 4)
                pokemon.change_y = random.randrange(-4, 4)

            self.pokemon_list.append(pokemon)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.pokemon_list.draw()

        output = "Score: " + str(self.score)
        arcade.draw_text(output, 10, HEIGHT-20, arcade.color.BLACK)
        
    def on_mouse_motion(self, x, y, dx, dy):

        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M:
            self.minimize()
        if key == arcade.key.ESCAPE:
            arcade.exit()

    def on_update(self, delta_time):

        self.pokemon_list.update()
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.pokemon_list)

        for pokemon in hit_list:
            pokemon.remove_from_sprite_lists()
            arcade.play_sound(self.catch_sound)
            self.score += 1

        if self.score == POKEMON_COUNT and not self.waiting:
            self.start_time = time.time()
            arcade.play_sound(self.yay_sound)
            self.waiting = True

        elif 2 <= time.time() - self.start_time:
            if self.start_time != 0:
                sys.exit()


def main():
    # main method

    window = Game()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
