import pygame
from src.constants import HEIGHT, WIDTH

def show_start_screen(window, font_title, font_rules):
    window.fill((0, 0, 0))
    title_text = font_title.render("Ninja Frog Apple Collector", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    window.blit(title_text, title_rect)
    rules_text = [
        "Welcome to the game!",
        "Use the left/right arrow keys to move.",
        "Press SPACE to jump.",
        "Collect the apples before they disappear.",
        "Each apple gives 1 point.",
        "If an apple disappears, you lose 1 point.",
        "Try to get 100 points!",
        "",
        "Press any key to start."
    ]
    y_offset = HEIGHT // 2
    for line in rules_text:
        rule = font_rules.render(line, True, (200, 200, 200))
        rule_rect = rule.get_rect(center=(WIDTH // 2, y_offset))
        window.blit(rule, rule_rect)
        y_offset += 30
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def show_win_screen(window, font_win, font_options):
    window.fill((0, 0, 0))
    win_text = font_win.render("Congratulations! You won!", True, (0, 255, 0))
    win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    window.blit(win_text, win_rect)

    play_again_text = font_options.render("Press 'R' to Replay", True, (255, 255, 255))
    play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(play_again_text, play_again_rect)

    quit_text = font_options.render("Press 'Q' to Exit the game", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    window.blit(quit_text, quit_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Indica que el jugador quiere rejugar
                if event.key == pygame.K_q:
                    return False # Indica que el jugador quiere salir
                
def draw(win, background_tiles, background_image, player, objects, fruits, score=None, font=None):
    for tile in background_tiles:
        win.blit(background_image, tile)
    for obj in objects:
        obj.draw(win)
    player.draw(win)
    fruits.draw(win)
    if score is not None and font is not None:
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        win.blit(score_text, (10, 10))
    pygame.display.update()