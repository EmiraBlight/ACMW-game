import pygame
from logic import unit_types

WIDTH, HEIGHT = 1920, 1080
MARKERSIZE = 40
bar_y = HEIGHT // 2
bar_length = 600 #define resolution and game size specs
bar_height = MARKERSIZE
bar_x = (WIDTH - bar_length) // 2

RED = (255, 0, 0)
LIME = (100, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)


def timing_game(screen) -> str|None:
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)
    options_text = pygame.font.SysFont(None, 36)
    selected_option = None


    def draw_menu(selected_idx=None):
        title = font.render("Select Weapon to forge", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        for i, option in enumerate(unit_types):
            color = (255, 255, 0) if selected_idx == i else (200, 200, 200)
            text = options_text.render(f"{i + 1}. {option}", True, color) #print out the options
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + i * 60))
        pygame.display.update()

    running_menu = True
    draw_menu()

    while running_menu:
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1]:
                    selected_option = unit_types[0]
                    running_menu = False
                elif event.key in [pygame.K_2]:
                    selected_option = unit_types[1] #grab input and return result
                    running_menu = False
                elif event.key in [pygame.K_3]:
                    selected_option = unit_types[2]
                    running_menu = False

        draw_menu()# render the option menu till a choice is made

    clock = pygame.time.Clock()

    score = 0
    clicks = 0
    running = True

    square_size = MARKERSIZE
    pos_x = bar_x
    direction = 1
    speed = 8

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "Quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicks += 1
                center_x = WIDTH // 2
                distance = abs(pos_x + square_size / 2 - center_x)

                if distance < 200:
                    points = max(1, int(6 - (distance / 20)))
                    score += points
                else:
                    score = max(0, score - 1)

                if score > 9:
                    running = False

        pos_x += direction * speed
        if pos_x + square_size >= bar_x + bar_length or pos_x <= bar_x:
            direction *= -1

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, RED, (bar_x, bar_y - bar_height // 2, bar_length, bar_height))
        pygame.draw.line(screen, GREEN, (WIDTH // 2, bar_y - bar_height // 2),
                         (WIDTH // 2, bar_y + bar_height // 2 - 1), 20)
        pygame.draw.line(screen, LIME, (WIDTH // 2 + 40, bar_y - bar_height // 2),
                         (WIDTH // 2 + 40, bar_y + bar_height // 2 - 1), 60)
        pygame.draw.line(screen, LIME, (WIDTH // 2 - 40, bar_y - bar_height // 2),
                         (WIDTH // 2 - 40, bar_y + bar_height // 2 - 1), 60)
        pygame.draw.line(screen, YELLOW, (WIDTH // 2 - 120, bar_y - bar_height // 2),
                         (WIDTH // 2 - 120, bar_y + bar_height // 2 - 1), 100)
        pygame.draw.line(screen, YELLOW, (WIDTH // 2 + 120, bar_y - bar_height // 2),
                         (WIDTH // 2 + 120, bar_y + bar_height // 2 - 1), 100)
        pygame.draw.rect(screen, BLUE, (pos_x, bar_y - square_size // 2, square_size, square_size))

        text = font.render(f"Score: {score}/10", True, (255, 255, 255))
        screen.blit(text, (50, 50))
        pygame.display.update()
        clock.tick(60)

    return selected_option
