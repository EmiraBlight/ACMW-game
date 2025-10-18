import pygame
from logic import unit_types
from math import sqrt
from queue import Queue
WIDTH, HEIGHT = 1560, 821
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
surface = pygame.Surface((WIDTH, HEIGHT),pygame.SRCALPHA)

def getClosest(position,lookup:dict[str,tuple[int,int]])->str|None:

    if not lookup:
        return None

    result = ""
    closest = (2**63)-2 #big enough

    for name,coord in lookup.items():
        distance =sqrt((position[0]-coord[0])**2+(position[1]-coord[1])**2)
        if distance< closest:
            closest = distance
            result = name
    return result



def timing_game(events:Queue) -> bool:
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)
    options_text = pygame.font.SysFont(None, 36)


    clock = pygame.time.Clock()

    score = 0
    clicks = 0
    running = True

    square_size = MARKERSIZE
    pos_x = bar_x
    direction = 1
    speed = 8

    while running:
        surface.fill((0, 0, 0, 0))
        while not events.empty():
            event = events.get()
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

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
                print(f"{score=}")

        pos_x += direction * speed
        if pos_x + square_size >= bar_x + bar_length or pos_x <= bar_x:
            direction *= -1
        pygame.draw.rect(surface, RED, (bar_x, bar_y - bar_height // 2, bar_length, bar_height))
        pygame.draw.line(surface, GREEN, (WIDTH // 2, bar_y - bar_height // 2),
                         (WIDTH // 2, bar_y + bar_height // 2 - 1), 20)
        pygame.draw.line(surface, LIME, (WIDTH // 2 + 40, bar_y - bar_height // 2),
                         (WIDTH // 2 + 40, bar_y + bar_height // 2 - 1), 60)
        pygame.draw.line(surface, LIME, (WIDTH // 2 - 40, bar_y - bar_height // 2),
                         (WIDTH // 2 - 40, bar_y + bar_height // 2 - 1), 60)
        pygame.draw.line(surface, YELLOW, (WIDTH // 2 - 120, bar_y - bar_height // 2),
                         (WIDTH // 2 - 120, bar_y + bar_height // 2 - 1), 100)
        pygame.draw.line(surface, YELLOW, (WIDTH // 2 + 120, bar_y - bar_height // 2),
                         (WIDTH // 2 + 120, bar_y + bar_height // 2 - 1), 100)
        pygame.draw.rect(surface, BLUE, (pos_x, bar_y - square_size // 2, square_size, square_size))

        text = font.render(f"Score: {score}/10", True, (255, 255, 255))
        surface.blit(text, (50, 50))
        clock.tick(60)
    surface.fill((0,0,0,0))
    return True
