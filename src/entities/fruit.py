import pygame
from os.path import join, dirname, abspath
from src.utils import load_sprite_sheets

class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.SPRITES = self.load_fruit_sprites() # Cargar sprites durante la inicialización
        self.animation_count = 0
        self.image = self.SPRITES["Apple"][0] # Usa el primer sprite por defecto
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.collected = False

    def load_fruit_sprites(self):
        return load_sprite_sheets("Items", "Fruits", 32, 32, False)

    def loop(self, fps):
        if not self.collected:
            self.animation_count += 1
            # Animación básica (puedes expandir esto)
            animation_loop = 4
            current_sprite_index = self.animation_count // animation_loop % len(self.SPRITES["Apple"])
            self.image = self.SPRITES["Apple"][current_sprite_index]
            self.mask = pygame.mask.from_surface(self.image)
            return False # La fruta aún no ha desaparecido
        return False # Si ya fue colectada, no necesita "loop"

    def collect(self):
        self.collected = True

    def draw(self, win):
        if not self.collected:
            win.blit(self.image, self.rect)