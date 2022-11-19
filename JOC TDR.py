import arcade
import time
import pyglet


PLAYER_SCALING = 1
TILE_SCALING = 0.75
MOVEMENT_SPEED = 3.3
DRETA = 0
ESQUERRA = 1
ADALT = 2
ABAIX = 3
WIDTH, HEIGHT = (round(128 * 15 * TILE_SCALING), round(128 * 10 * TILE_SCALING))
CAMERA_SPEED = 0.2


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

    def close(self):
        self.texture = self.frames[0]
        self.imatge_index = 0
        self.open = False
        self.key_e = False
        self.start_time = 0
        self.stay = 0


'''
class Room:
    def __init__(self):
        self.map_name = None

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

        self.controls = False
        self.tecla_dreta = False
        self.tecla_esquerra = False
        self.tecla_abaix = False
        self.tecla_adalt = False

        self.camera_for_sprites = arcade.Camera(WIDTH, HEIGHT)
        self.camera_for_gui = arcade.Camera(WIDTH, HEIGHT)
        self.physics_engines = []

        self.tile_map = None
        self.scenes = []
        self.current_map = 0
        self.map_folder = 'Tiled_maps'
        self.grass_stone_map_name = "Mapa de prova"
        self.parquet_map_name = "Mapa parquet"
        self.map_path = None

        self.pantalla_negra = False
        self.transparency = 0
        self.opaquing = False

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

        layer_options = {
            "Obstacles": {
                "use_spatial_hash": False,},
        }

        self.map_path = f'{self.map_folder}/{self.parquet_map_name}.tmj'
        self.tile_map = arcade.load_tilemap(self.map_path, TILE_SCALING, layer_options)
        self.scene_1 = [arcade.Scene.from_tilemap(self.tile_map), 0]
        self.scenes.append(self.scene_1)

        self.map_path = f'{self.map_folder}/{self.grass_stone_map_name}.tmj'
        self.tile_map = arcade.load_tilemap(self.map_path, scaling=TILE_SCALING)
        self.scene_2 = [arcade.Scene.from_tilemap(self.tile_map), 1]
        self.scenes.append(self.scene_2)

        arcade.set_background_color(arcade.color.BLACK)

        for n in self.scenes:
            for x in n[0].name_mapping:
                if x == "Obstacles":
                    physics_engine = [arcade.PhysicsEngineSimple(self.player_sprite, n[0].name_mapping[x]), n[1]]
                    self.physics_engines.append(physics_engine)

        self.controls = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.player_sprite.change_y = 0
            if self.controls:
                self.player_sprite.change_x = MOVEMENT_SPEED
            self.tecla_dreta = True

        if key == arcade.key.LEFT:
            self.player_sprite.change_y = 0
            if self.controls:
                self.player_sprite.change_x = -MOVEMENT_SPEED
            self.tecla_esquerra = True

        if key == arcade.key.UP:
            self.player_sprite.change_x = 0
            if self.controls:
                self.player_sprite.change_y = MOVEMENT_SPEED
            self.tecla_adalt = True

        if key == arcade.key.DOWN:
            self.player_sprite.change_x = 0
            if self.controls:
                self.player_sprite.change_y = -MOVEMENT_SPEED
            self.tecla_abaix = True

        if key == arcade.key.E and not self.motxilla.open:
            if self.controls:
                self.motxilla.key_e = True

        if key == arcade.key.ESCAPE:
            arcade.exit()
        if key == arcade.key.M:
            self.minimize()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.tecla_dreta = False
            if self.controls:
                if self.tecla_adalt:
                    self.player_sprite.change_y = MOVEMENT_SPEED
                if self.tecla_abaix:
                    self.player_sprite.change_y = -MOVEMENT_SPEED
                if self.tecla_esquerra:
                    self.player_sprite.change_x = -MOVEMENT_SPEED

        if key == arcade.key.LEFT:
            self.tecla_esquerra = False
            if self.controls:
                if self.tecla_adalt:
                    self.player_sprite.change_y = MOVEMENT_SPEED
                if self.tecla_abaix:
                    self.player_sprite.change_y = -MOVEMENT_SPEED
                if self.tecla_dreta:
                    self.player_sprite.change_x = MOVEMENT_SPEED

        if key == arcade.key.UP:
            self.tecla_adalt = False
            if self.controls:
                if self.tecla_dreta:
                    self.player_sprite.change_x = MOVEMENT_SPEED
                if self.tecla_esquerra:
                    self.player_sprite.change_x = -MOVEMENT_SPEED
                if self.tecla_abaix:
                    self.player_sprite.change_y = -MOVEMENT_SPEED

        if key == arcade.key.DOWN:
            self.tecla_abaix = False
            if self.controls:
                if self.tecla_dreta:
                    self.player_sprite.change_x = MOVEMENT_SPEED
                if self.tecla_esquerra:
                    self.player_sprite.change_x = -MOVEMENT_SPEED
                if self.tecla_adalt:
                    self.player_sprite.change_y = MOVEMENT_SPEED

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

        for n in self.scenes:
            spritelist_dict = n[0].name_mapping
            if n[1] == self.current_map:
                for x in spritelist_dict:
                    if x != "Decoration":
                        spritelist_dict[x].draw()
                    if x == "Decoration":
                        for elem in range(len(spritelist_dict[x])):
                            if spritelist_dict[x][elem].center_y > self.player_sprite.center_y:
                                spritelist_dict[x][elem].draw()

        self.player_list.draw()

        for n in self.scenes:
            spritelist_dict = n[0].name_mapping
            if n[1] == self.current_map:
                for x in spritelist_dict:
                    if x == "Decoration":
                        for elem in range(len(spritelist_dict[x])):
                            if spritelist_dict[x][elem].center_y < self.player_sprite.center_y:
                                spritelist_dict[x][elem].draw()

        self.camera_for_gui.use()

        arcade.draw_rectangle_filled(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT,
                                     [0, 0, 0, self.transparency])
        self.motxilla_list.draw()

    def on_update(self, delta_time):

        lower_left_corner = pyglet.math.Vec2(self.player_sprite.center_x - self.width / 2,
                                             self.player_sprite.center_y - self.height / 2)

        if self.transparency == 255:
            self.camera_for_sprites.move_to(lower_left_corner, 1)
        else:
            self.camera_for_sprites.move_to(lower_left_corner, CAMERA_SPEED)

        if self.player_sprite.right + self.player_sprite.change_x > WIDTH:
            self.player_sprite.right = WIDTH
        elif self.player_sprite.left + self.player_sprite.change_x < 0:
            self.player_sprite.left = 2
        else:
            self.player_sprite.center_x += self.player_sprite.change_x

        if (self.player_sprite.bottom <= 0 and self.player_sprite.right < 128 * TILE_SCALING * 2 and
           self.player_sprite.change_y < 0 and self.current_map == 0)\
                or (self.pantalla_negra and self.player_sprite.direccio == ABAIX):
            self.controls = False
            if self.motxilla.open:
                self.motxilla.close()
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = 0
            self.player_sprite.direccio = ABAIX
            if not self.opaquing and self.transparency == 0:
                self.opaquing = True
            self.pantalla_negra = True
            if self.transparency < 255 and self.opaquing:
                self.transparency += 5
            elif self.transparency == 255 and self.opaquing:
                self.opaquing = False
                self.current_map = 1
                self.player_sprite.top = HEIGHT
            elif self.transparency > 0 and not self.opaquing:
                self.transparency -= 5
                if self.transparency == 0:
                    if self.tecla_abaix:
                        self.player_sprite.change_y = -MOVEMENT_SPEED
                    if self.tecla_adalt:
                        self.player_sprite.change_y = MOVEMENT_SPEED
                    if self.tecla_esquerra:
                        self.player_sprite.change_x = -MOVEMENT_SPEED
                    if self.tecla_dreta:
                        self.player_sprite.change_x = MOVEMENT_SPEED
                    self.controls = True
                    self.pantalla_negra = False
        elif (self.player_sprite.top >= HEIGHT and self.player_sprite.right < 128 * TILE_SCALING * 2 and
                self.player_sprite.change_y > 0 and self.current_map == 1)\
                or (self.pantalla_negra and self.player_sprite.direccio == ADALT):
            self.controls = False
            if self.motxilla.open:
                self.motxilla.close()
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = 0
            self.player_sprite.direccio = ADALT
            if not self.opaquing and self.transparency == 0:
                self.opaquing = True
            self.pantalla_negra = True
            if self.transparency < 255 and self.opaquing:
                self.transparency += 5
            elif self.transparency == 255 and self.opaquing:
                self.opaquing = False
                self.current_map = 0
                self.player_sprite.bottom = 0
            elif self.transparency > 0 and not self.opaquing:
                self.transparency -= 5
                if self.transparency == 0:
                    if self.tecla_abaix:
                        self.player_sprite.change_y = -MOVEMENT_SPEED
                    if self.tecla_adalt:
                        self.player_sprite.change_y = MOVEMENT_SPEED
                    if self.tecla_esquerra:
                        self.player_sprite.change_x = -MOVEMENT_SPEED
                    if self.tecla_dreta:
                        self.player_sprite.change_x = MOVEMENT_SPEED
                    self.controls = True
                    self.pantalla_negra = False

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

        for physics_engine in self.physics_engines:
            if physics_engine[1] == self.current_map:
                physics_engine[0].update()

        for x in self.scenes:
            if x[1] == self.current_map:
                x[0].update_animation(delta_time, ["Ground", "Obstacles", "Decoration"])


def main():
    my_game = Game()
    my_game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
