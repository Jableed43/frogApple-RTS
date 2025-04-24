import random
import pygame
from src.constants import HEIGHT, WIDTH, PLAYER_VEL
from src.entities.fruit import Fruit


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    # it stops the player from moving when change direction
    player.x_vel = 0
    collide_left = handle_horizontal_collision(player, objects, -PLAYER_VEL * 2)
    collide_right = handle_horizontal_collision(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
    
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        # this will tell if player collided to the object
        if pygame.sprite.collide_mask(player, obj):
            # place the player over the object
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            # player is underneath the object, hits its head
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
        
            # this way we can track which objects the player is colliding
            # we can cause an effect to the player due collision
            collided_objects.append(obj)

    return collided_objects

def handle_horizontal_collision(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    
    player.move(-dx, 0)
    player.update()
    return collided_object

def generate_random_fruit(blocks):
    fruit_size = 32 # Altura de la fruta
    min_y = int(HEIGHT * 0.25) # 1/4 de la altura desde la parte superior (para que no estén DEMASIADO abajo al principio)
    max_y = HEIGHT - fruit_size # Asegura que la fruta no se genere cortada en la parte inferior
    player_width = 64 # Ancho del jugador (ajusta si es diferente)
    margin_x = player_width

    while True:
        x = random.randrange(margin_x, WIDTH - fruit_size - margin_x)
        y = random.randrange(min_y, max_y + 1) # Rango de Y limitado al 3/4 inferior (aproximadamente)
        fruit = Fruit(x, y)
        if not any(fruit.rect.colliderect(block.rect) for block in blocks):
            return fruit