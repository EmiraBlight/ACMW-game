from queue  import Queue
import pygame
from enum import Enum
from logic import inventory,unit
from timingGame import timing_game
from horde import horde
import threading
from timingGame import surface
class loc(Enum):
    none=0
    anvil = 1
    table = 2
    enchant =3
    bow = 4

mini_game_running = False

event_queue = Queue()

def run_timing_game_thread():
    global mini_game_running, mini_game_result
    mini_game_result = timing_game(event_queue) #sp the game is being run in the background of the timing game
    mini_game_running = False #This little chunk of code is run in its own thread

progress :float = 0

units :list[unit] = []

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
progressBar =  pygame.Rect((1431,159),(1,73))
progressBar.topright = (1431,86)
res = None
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
        if mini_game_running:
            event_queue.put(event)
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:
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
                    if not itemHeld:
                        target_x, target_y = x, y
                        if not mini_game_running:
                            mini_game_running = True
                            threading.Thread(target=run_timing_game_thread, daemon=True).start()
                            itemHeld = "Sword"
                            mini_game_result = None
                        break
            elif item==enchant:
                if location!= loc.enchant:
                    location = loc.enchant
                    if not itemHeld:
                        target_x, target_y = x, y
                        if not mini_game_running:
                            mini_game_running = True
                            threading.Thread(target=run_timing_game_thread, daemon=True).start()
                            itemHeld = "Staff"
                            mini_game_result = None
                        break
            elif item==bowString:
                if location!=loc.bow:
                    location = loc.bow
                    if not itemHeld:
                        target_x, target_y = x, y
                        if not mini_game_running:
                            mini_game_running = True
                            threading.Thread(target=run_timing_game_thread, daemon=True).start()
                            itemHeld = "Bow"
                            mini_game_result = None
                        break


        if player.colliderect(item) and item==table:
            if location!= loc.table:
                location = loc.table
                if itemHeld:
                    units.append(unit(itemHeld,1000))
                    itemHeld= None
                break

        elif isNotColliding(player):
            if location!= loc.none:
                location = loc.none
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, GREEN, player)
    pygame.draw.rect(screen,RED,progressBar)
    screen.blit(surface, (0,0))
    pygame.display.update()
    second+=1
    if second == 60:
        second = 0
        if min%5==0:
            h.increaseDifficulty()
           # print("diff increased!")
        if not units:
            progress = h.progress()
            #print(f"progress: {progress*100}%")
            if progress>=1:
                print("GAME OVER")
                pygame.quit()
                exit()
        else:
            units = [i for i in units if i.damage(h.getDmg()/len(units))]
            print(units)

    progressBar =  pygame.Rect((1431,159),(progress*456,73))
    progressBar.topright = (1431,86)


    clock.tick(60)
