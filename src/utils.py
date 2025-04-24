import pygame
from os import listdir
from os.path import isfile, join, dirname, abspath
from src.constants import HEIGHT, WIDTH

# X rotation for facing direction
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    # points toward a folder and it's child folder
    path = join(dirname(dirname(abspath(__file__))), "assets", dir1, dir2) # Sube dos niveles para llegar a .python-platformer

    # get a list of every image-file path of the folder
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        #load the sprites and applies transparency
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        # Sprites are assumed to be horizontally aligned
        #if every sprite is X pixels wide, you can calculate how many sprites you have
        for i in range(sprite_sheet.get_width() // width):
            # Creates an empty surface the exact size of a sprite, allowing transparency
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            # Defines the area to cut from the sprite sheet
            rect = pygame.Rect(i * width, 0, width, height)
            #Copy that part of the sprite to the new surface
            surface.blit(sprite_sheet, (0, 0), rect)
            # Scale to double of it's size and save it to a list
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            # Sprites facing to the right
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            # Sprites facing to the left
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    # size is the dimension of the block
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    # 96 is X, 0 is Y
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_background(name):
    # Obtiene el directorio del script actual (utils.py)
    current_dir = dirname(abspath(__file__))
    # Sube un nivel (a la carpeta 'src') y luego entra a 'assets' y 'Background'
    image_path = join(dirname(current_dir), "assets", "Background", name)
    image = pygame.image.load(image_path)
    _, _, width, height = image.get_rect()
    tiles = []

    # X axis - horizontal tiles to fill the spaces, + 1 fill the gaps
    for i in range(WIDTH // width + 1):
        # Y axis
        for j in range(HEIGHT // height + 1):
            # current position of the tiles adding to list
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image