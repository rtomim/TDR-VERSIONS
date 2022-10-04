import arcade

WIDTH, HEIGHT = arcade.window_commands.get_display_size()
PLAYER_SCALING = 0.75
MOVEMENT_SPEED = 6



class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, 'Mr. Pelussy', fullscreen=True)
        self.player_name = ""
        self.player_sprite = None
        self.player_list = None
        self.set_mouse_visible(False)

    def setup(self):
        self.player_name = "Mr. Peluse"
        self.player_sprite = arcade.Sprite('Sprites_animacions/PELUSO_ABAIX_0.png', PLAYER_SCALING)
        self.player_sprite.center_x = WIDTH/2
        self.player_sprite.center_y = HEIGHT/2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        if key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if key == arcade.key.ESCAPE:
            arcade.exit()
        if key == arcade.key.M:
            self.minimize()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
        if key == arcade.key.DOWN:
            self.player_sprite.change_y = 0

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color((165, 140, 39))
        self.player_list.draw()

    def on_update(self, delta_time):

        if self.player_sprite.right + self.player_sprite.change_x > WIDTH:
            self.player_sprite.right = WIDTH - 2
        elif self.player_sprite.left + self.player_sprite.change_x < 0:
            self.player_sprite.left = 2
        else:
            self.player_sprite.center_x += self.player_sprite.change_x

        if self.player_sprite.top + self.player_sprite.change_y > HEIGHT:
            self.player_sprite.top = HEIGHT
        elif self.player_sprite.bottom + self.player_sprite.change_y < 0:
            self.player_sprite.bottom = 0
        else:
            self.player_sprite.center_y += self.player_sprite.change_y

        #self.player_sprite.update_animation()


def main():
    my_game = Game()
    my_game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
