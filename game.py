import pygame
pygame.init()
from src.screens import show_start_screen, show_win_screen, draw
from src.mechanics import generate_random_fruit, handle_move
from src.utils import get_background
from src.constants import BLOCK_SIZE, HEIGHT, WIDTH, ADD_FRUIT_EVENT, FPS, GAME_STATE
from src.entities.player import Player
from src.entities.fire import Fire
from src.entities.block import Block

def main(window):
    global GAME_STATE

    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 74)
    font_rules = pygame.font.Font(None, 36)
    font_win = pygame.font.Font(None, 74)
    font_options = pygame.font.Font(None, 36)
    score_font = pygame.font.Font(None, 36)
    score = 0

    while True: # Bucle principal para permitir reiniciar el juego
        # Inicialización del juego
        background_tiles, background_image = get_background("Pink.png")
        block_size = BLOCK_SIZE
        player = Player(100, 100, 50, 50)
        fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
        fire.on()
        floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range((WIDTH // block_size) + 1)]
        objects = [*floor,
                   Block(0, HEIGHT - block_size * 2, block_size),
                   Block(block_size * 3, HEIGHT - block_size * 4, block_size),
                   Block(block_size * 6, HEIGHT - block_size * 3, block_size),
                   Block(block_size * 1, HEIGHT - block_size * 5, block_size),
                   Block(block_size * 8, HEIGHT - block_size * 3, block_size),
                   fire]
        fruits = pygame.sprite.Group()
        initial_fruit_count = 3
        max_fruits_on_screen = 3
        fruit_delay = 2500
        fruit_spawned_count = 0
        score = 0

        show_start_screen(window, font_title, font_rules)

        if len(fruits) < max_fruits_on_screen:
            fruits.add(generate_random_fruit(objects))
            fruit_spawned_count = 1

        pygame.time.set_timer(ADD_FRUIT_EVENT, fruit_delay)

        running = True
        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player.jump_count < 3:
                        player.jump()
                if event.type == ADD_FRUIT_EVENT and len(fruits) < max_fruits_on_screen and fruit_spawned_count < initial_fruit_count:
                    fruits.add(generate_random_fruit(objects))
                    fruit_spawned_count += 1
                    pygame.time.set_timer(ADD_FRUIT_EVENT, fruit_delay)

            player.loop(FPS)
            fire.loop()
            handle_move(player, objects)

            # Update frutas
            for fruit in fruits:
                if fruit.loop(FPS):
                    score -= 1
                    if score < 0:
                        score = 0
                    fruits.remove(fruit)
                    if len(fruits) < max_fruits_on_screen:
                        fruits.add(generate_random_fruit(objects))

            # Detección de colisión entre el jugador y las frutas
            fruits_collected = pygame.sprite.spritecollide(player, fruits, False, pygame.sprite.collide_mask)
            for fruit in fruits_collected:
                fruit.collect()
                score += 1
                fruits.remove(fruit)
                if len(fruits) < max_fruits_on_screen:
                    fruits.add(generate_random_fruit(objects))

            # Verificar condición de victoria
            if score >= 100:
                if show_win_screen(window, font_win, font_options):
                    running = False # Salir del bucle del juego para reiniciar
                else:
                    running = False # Salir del bucle del juego para terminar
                    pygame.quit()
                    quit()
            else:
                # Dibujar el juego normalmente si no se ha alcanzado el score
                draw(window, background_tiles, background_image, player, objects, fruits, score, score_font)


if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RocketTechSchool-Project")
    main(window)