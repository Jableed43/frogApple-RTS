import pygame
from src.constants import WIDTH
from src.utils import load_sprite_sheets

class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        # How fast we move our player in every frame
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        # To track wich animation my player is facing
        self.direction = "left"
        # Animation is reseting every time we change direction
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.load_character_assets()
    
    def load_character_assets(self):
        self.sprites = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
        self.idle = self.sprites["idle_left"][0]
        self.image = self.idle # Establecer una imagen por defecto

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        # Limitar el movimiento horizontal
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def move_left(self, vel):
        # Move the player to the left, wich is a negative value in x axis
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        # Move the player to the right, wich is a positive value in x axis
        self.x_vel = vel 
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def loop(self, fps):
        # Every frame we are failling adds a little bit of vertical speed, never adds more than 1 per frame
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        # Count once every frame, move character in a correct direction, updating animation
        self.move(self.x_vel, self.y_vel)
        
        if self.hit:
            self.hit_count += 1
            if self.hit_count > fps * 2:
                self.hit = False
                self.hit_count = 0

        self.fall_count += 1 
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
    
    def hit_head(self):
        self.count = 0
        # bounce agains block and go downwards
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        # negative Y means player is jumping
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
            elif self.jump_count == 3:
                sprite_sheet = "double_jump"
        # it's double because it means it is falling from a high altitude
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall" 
        # player is moving horizontally (whether right or left)
        elif self.x_vel != 0:
            sprite_sheet = "run"
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.sprites[sprite_sheet_name]
        # sprite global counter // delays the frame change % -> when last frame is reached it goes back to 0
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        # determines what frame to show, it's very important
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        # Mask is a mapping of all of the pixel that exist in the sprite -> pixel perfect collision
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def draw(self, win):
        # The rect below let you test your code without using sprites
        # pygame.draw.rect(win, self.COLOR, self.rect)
        win.blit(self.sprite, (self.rect.x, self.rect.y))