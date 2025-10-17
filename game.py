import pygame
from enum import Enum
from logic import inventory,unit
from timingGame import timing_game
from horde import horde


class loc(Enum):
    none=0
    anvil = 1
    table = 2
    enchant =3
    bow = 4



units :list[unit] = [unit("sword",100),unit("Bow",100)]

second: int = 0
min: int = 0
pygame.init()
WIDTH, HEIGHT = 1560, 821
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_image = pygame.image.load('assets/background.png').convert()
pygame.display.set_caption("Some cool game probably")

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
YELLOW = (255,255,0)
square_size = 50
x, y = WIDTH // 2, HEIGHT // 2
target_x, target_y = x, y
speed = 7
player = pygame.Rect(x - square_size // 2, y - square_size // 2, square_size, square_size)
anvil = pygame.Rect(150, 250,75,75)
table = pygame.Rect(294,405, 225,75)
enchant = pygame.Rect(85,445,88,211)
bowString = pygame.Rect(506,618,35,77)
interactables = [anvil,table,enchant,bowString]  # list of things we can interact with
clock = pygame.time.Clock()


h = horde()

def isNotColliding(p)-> bool:

    for item in interactables:
        if p.colliderect(item):
            return False
    return True

location = loc.none
running = True
itemHeld = None
font = pygame.font.SysFont(None, 48)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            if event.button == 1:
                if event.pos[0]>108 and event.pos[0]<703 and event.pos[1]<703 and event.pos[1]>278:
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
        if player.colliderect(item):
            if item==anvil:
                if location != loc.anvil:
                    location = loc.anvil
                    print(f"Player is colliding with the anvil!")
                    if not itemHeld:
                        target_x, target_y = x, y
                        res= timing_game(screen)
                        if res:
                            print(f"{res=}")
                            itemHeld = "Sword"
                        break
            elif item==enchant:
                if location!= loc.enchant:
                    location = loc.enchant
                    print(f"Player is colliding with the enchant table!")
                    if not itemHeld:
                        target_x, target_y = x, y
                        res= timing_game(screen)
                        if res:
                            print(f"{res=}")
                            itemHeld = "Staff"
                        break
            elif item==bowString:
                if location!=loc.bow:
                    location = loc.bow
                    print(f"Player is colliding with the bow table!")
                    if not itemHeld:
                        target_x, target_y = x, y
                        res= timing_game(screen)
                        if res:
                            print(f"{res=}")
                            itemHeld = "Staff"
                        break


        if player.colliderect(item) and item==table:
            if location!= loc.table:
                location = loc.table
                print(f"Player is colliding with the table!")
                if itemHeld:
                    units.append(unit(itemHeld))
                    itemHeld= None
                    print(f"{inventory=}")
                break

        elif isNotColliding(player):
            if location!= loc.none:
                print("player not colliding with anything!")
                location = loc.none
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, GREEN, player)
    #pygame.draw.rect(screen, BLUE, anvil)
    #pygame.draw.rect(screen, RED, table) no longer render, just hitboxes now
    text = font.render(f"Inventory: {str(inventory)}, Item held: {itemHeld}", True, (255, 255, 255))
    screen.blit(text, (50, 50))
    pygame.display.update()
    second+=1
    if second == 60:
        second = 0
        min+=1
        if min%5==0:
            h.increaseDifficulty()
            print("diff increased!")
        if not units:
            print(f"Hordes progress: {h.progress()}")
        else:
            units = [i for i in units if i.damage(h.getDmg()/len(units))]
            print(units)



    clock.tick(60)
