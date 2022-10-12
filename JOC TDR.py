import arcade
import time
import pyglet


PLAYER_SCALING = 1
TILE_SCALING = 0.75
MOVEMENT_SPEED = 6
DRETA = 0
ESQUERRA = 1
ADALT = 2
ABAIX = 3
WIDTH, HEIGHT = (round(128 * 15 * TILE_SCALING), round(128 * 10 * TILE_SCALING))
CAMERA_SPEED = 1


main_path = "Sprites_animacions/PELUSO_"
motxilla_path = "Sprites_animacions/MOTXILLA-"


def load_frame_pair(filename):
    return [arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True)]


class Protagonista(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.imatge_index = 0
        self.direccio = None
        self.has_moved = False
        self.standing_costat = load_frame_pair(f'{main_path}STANDING_COSTAT.png')

        self.walk_frames_x = []
        for x in range(8):
            frame = load_frame_pair(f'{main_path}COSTAT_{x}.png')
            self.walk_frames_x.append(frame)

        self.walk_frames_y = []
        for x in range(6):
            frame = arcade.load_texture(f'{main_path}ADALT_{x}.png')
            self.walk_frames_y.append(frame)
        for x in range(6):
            frame = arcade.load_texture(f'{main_path}ABAIX_{x}.png')
            self.walk_frames_y.append(frame)

        self.texture = self.walk_frames_y[6]

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x > 0 and self.direccio != DRETA:
            self.direccio = DRETA
        if self.change_x < 0 and self.direccio != ESQUERRA:
            self.direccio = ESQUERRA
        if self.change_y > 0 and self.direccio != ADALT:
            self.direccio = ADALT
        if self.change_y < 0 and self.direccio != ABAIX:
            self.direccio = ABAIX

        if self.change_x != 0:
            self.has_moved = True
            self.imatge_index += 1
            if self.imatge_index > 28:
                self.imatge_index = 0
            self.texture = self.walk_frames_x[self.imatge_index // 4][self.direccio]

        if self.change_y > 0:
            self.has_moved = True
            self.imatge_index += 1
            if self.imatge_index > 15:
                self.imatge_index = 0
            self.texture = self.walk_frames_y[self.imatge_index // 3]

        if self.change_y < 0:
            self.has_moved = True
            self.imatge_index += 1
            if self.imatge_index > 15:
                self.imatge_index = 0
            self.texture = self.walk_frames_y[self.imatge_index // 3 + 6]

        if self.change_x == 0 and self.change_y == 0 and self.has_moved:
            if self.direccio == DRETA:
                self.texture = self.standing_costat[DRETA]
            if self.direccio == ESQUERRA:
                self.texture = self.standing_costat[ESQUERRA]
            if self.direccio == ADALT:
                self.texture = self.walk_frames_y[0]
            if self.direccio == ABAIX:
                self.texture = self.walk_frames_y[6]


class Motxilla(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.imatge_index = 0
        self.open = False
        self.key_e = False
        self.start_time = 0
        self.stay = 0

        self.frames = []
        for x in range(6):
            frame = arcade.load_texture(f'{motxilla_path}{x+1}.png')
            self.frames.append(frame)

        self.texture = self.frames[0]

    def update_animation(self, delta_time: float = 1 / 60):
        if self.imatge_index > 4 and self.stay < 30:
            self.texture = self.frames[-1]
            self.stay += 1
        elif self.stay >= 30:
            self.start_time = 0
            self.imatge_index = 0
            self.texture = self.frames[0]
            self.stay = 0
            self.open = False
        elif self.imatge_index == 0:
            self.texture = self.frames[1]
            self.imatge_index += 1
            self.start_time = time.time()
        elif 0.066 <= time.time() - self.start_time:
            self.texture = self.frames[self.imatge_index + 1]
            self.imatge_index += 1
            self.start_time = time.time()


'''
class Room:
    def __init__(self):
        self.tiled_map = None

    def setup_room_1(self):

        room = Room()
        room.tiled_map = arcade.load_tilemap('Tiled_maps/Mapa de prova.tmj', TILE_SCALING)

        return room
    def setup_room_2(self):

        room = Room()
        room.tiled_map = arcade.load_tilemap('Tiled_maps/room_2.tmj', TILE_SCALING)

        return room
'''


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, 'Mr. Pelussy', fullscreen=True)
        self.player_name = ""
        self.player_sprite = None
        self.player_list = None
        self.motxilla = None
        self.motxilla_list = None

        self.set_mouse_visible(False)

        self.tecla_dreta = False
        self.tecla_esquerra = False
        self.tecla_abaix = False
        self.tecla_adalt = False

        self.camera_for_sprites = arcade.Camera(WIDTH, HEIGHT)
        self.camera_for_gui = arcade.Camera(WIDTH, HEIGHT)

        self.tile_map = None
        self.ground_list = None

    def setup(self):
        self.player_name = "Mr. Peluse"
        self.player_sprite = Protagonista()
        self.player_sprite.center_x = WIDTH/2
        self.player_sprite.center_y = HEIGHT/2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.motxilla = Motxilla()
        self.motxilla.center_x = 60
        self.motxilla.center_y = arcade.window_commands.get_display_size()[1] - 60
        self.motxilla_list = arcade.SpriteList()
        self.motxilla_list.append(self.motxilla)

        map_folder = 'Tiled_maps'
        map_name = 'Mapa de prova.tmj'
        map_path = f'{map_folder}/{map_name}'
        self.tile_map = arcade.load_tilemap(map_path, scaling=TILE_SCALING)

        self.ground_list = self.tile_map.sprite_lists["Ground"]

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = MOVEMENT_SPEED
            self.tecla_dreta = True

        if key == arcade.key.LEFT:
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = -MOVEMENT_SPEED
            self.tecla_esquerra = True

        if key == arcade.key.UP:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = MOVEMENT_SPEED
            self.tecla_adalt = True

        if key == arcade.key.DOWN:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = -MOVEMENT_SPEED
            self.tecla_abaix = True

        if key == arcade.key.E and not self.motxilla.open:
            self.motxilla.key_e = True

        if key == arcade.key.ESCAPE:
            arcade.exit()
        if key == arcade.key.M:
            self.minimize()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.tecla_dreta = False
            if self.tecla_adalt:
                self.player_sprite.change_y = MOVEMENT_SPEED
            if self.tecla_abaix:
                self.player_sprite.change_y = -MOVEMENT_SPEED

        if key == arcade.key.LEFT:
            self.tecla_esquerra = False
            if self.tecla_adalt:
                self.player_sprite.change_y = MOVEMENT_SPEED
            if self.tecla_abaix:
                self.player_sprite.change_y = -MOVEMENT_SPEED

        if key == arcade.key.UP:
            self.tecla_adalt = False
            if self.tecla_dreta:
                self.player_sprite.change_x = MOVEMENT_SPEED
            if self.tecla_esquerra:
                self.player_sprite.change_x = -MOVEMENT_SPEED

        if key == arcade.key.DOWN:
            self.tecla_abaix = False
            if self.tecla_dreta:
                self.player_sprite.change_x = MOVEMENT_SPEED
            if self.tecla_esquerra:
                self.player_sprite.change_x = -MOVEMENT_SPEED

        if not self.tecla_dreta and not self.tecla_esquerra:
            self.player_sprite.change_x = 0

        if not self.tecla_adalt and not self.tecla_abaix:
            self.player_sprite.change_y = 0

        if key == arcade.key.E:
            self.motxilla.key_e = False

    def on_draw(self):
        arcade.start_render()

#        arcade.set_background_color(arcade.color.WISTERIA)

        self.camera_for_sprites.use()

        self.ground_list.draw()
        self.player_list.draw()

        self.camera_for_gui.use()

        self.motxilla_list.draw()

    def on_update(self, delta_time):

        lower_left_corner = pyglet.math.Vec2(self.player_sprite.center_x - self.width / 2,
                                             self.player_sprite.center_y - self.height / 2)

        self.camera_for_sprites.move_to(lower_left_corner, CAMERA_SPEED)

        if self.player_sprite.right + self.player_sprite.change_x > WIDTH:
            self.player_sprite.right = WIDTH
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

        if self.player_sprite.change_x != 0:
            self.player_sprite.change_y = 0
        if self.player_sprite.change_y != 0:
            self.player_sprite.change_x = 0

        self.player_sprite.update_animation()

        if self.motxilla.key_e:
            if not self.motxilla.open:
                self.motxilla.key_e = False
                self.motxilla.open = True

        if self.motxilla.open:
            self.motxilla.update_animation()


def main():
    my_game = Game()
    my_game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
