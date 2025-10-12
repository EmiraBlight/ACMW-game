import pygame
from enum import Enum
from timingGame import timing_game
class loc(Enum):
    none=0
    anvil = 1
    table = 2



pygame.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Some cool game probably")

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)

mini = False

square_size = 50
x, y = WIDTH // 2, HEIGHT // 2
target_x, target_y = x, y
speed = 7
player = pygame.Rect(x - square_size // 2, y - square_size // 2, square_size, square_size)
anvil = pygame.Rect(100, 100,75,75)
table = pygame.Rect(250,250, 75,225)
interactables = [anvil,table]  # list of things we can interact with
clock = pygame.time.Clock()


def isNotColliding(p)-> bool:

    for item in interactables:
        if p.colliderect(item):
            return False
    return True

location = loc.none
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                target_x, target_y = event.pos
    dx, dy = target_x - x, target_y - y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance > speed:
        x += speed * dx / distance
        y += speed * dy / distance
    else:
        x, y = target_x, target_y

    player = pygame.Rect(x - square_size // 2, y - square_size // 2, square_size, square_size)
    # Check for collisions with interactables
    for item in interactables:
        if player.colliderect(item) and item==anvil:
            if location != loc.anvil:
                location = loc.anvil
                print(f"Player is colliding with the anvil!")
                mini=True
                target_x, target_y = x, y# stops user from moving when game ends
                res= timing_game(screen)
                mini=False
                if res>0:
                    print(f"{res=}")
                    # Will add logic to give player item here
                break
        if player.colliderect(item) and item==table:
            if location!= loc.table:
                location = loc.table
                print(f"Player is colliding with the table!")
                break
        elif isNotColliding(player):
            if location!= loc.none:
                print("player not colliding with anything!")
                location = loc.none

    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, player)
    pygame.draw.rect(screen, BLUE, anvil)
    pygame.draw.rect(screen, RED, table)
    pygame.display.flip()

    clock.tick(60)
