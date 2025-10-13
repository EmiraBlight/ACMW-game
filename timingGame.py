import pygame

def timing_game(screen)->int:
    MARKERSIZE = 40
    WIDTH, HEIGHT = 1920, 1080
    pygame.display.set_caption("Click the button as close to the middle as possible")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    bar_y = HEIGHT // 2
    bar_length = 600
    bar_height = MARKERSIZE
    bar_x = (WIDTH - bar_length) // 2

    square_size = MARKERSIZE
    pos_x = bar_x
    direction = 1
    speed = 10

    RED = (255, 0, 0)
    LIME = (100, 255, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 150, 255)
    GREEN = (0, 255, 0)
    score = 0
    clicks = 0
    running = True

    text = font.render(f"Score: {score}/10", True, (255, 255, 255))
    text_surface =  text.get_rect()
    has_run = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicks+=1
                center_x = WIDTH // 2
                distance = abs(pos_x + square_size/2 - center_x)

                if distance < 200:
                    points = max(1, int(6 - (distance / 20)))#Add points (max 5 if you hit dead center)
                    score += points
                else:
                    score = max(0, score - 1)  #u suck and lost points

                if score > 9:
                    running = False #done once you get a score greater than 9

        pos_x += direction * speed
        if pos_x + square_size >= bar_x + bar_length or pos_x <= bar_x:
            direction *= -1 #Turn arround if at end of block


        pygame.draw.rect(screen, RED,(bar_x, bar_y - bar_height//2, bar_length, bar_height))


        pygame.draw.line(screen, GREEN,(WIDTH//2, bar_y - (bar_height//2)), (WIDTH//2, bar_y+ bar_height//2-1), 20)#green center

        pygame.draw.line(screen, LIME,(WIDTH//2+40, bar_y - (bar_height//2)), (WIDTH//2+40, bar_y+ bar_height//2-1), 60)
        pygame.draw.line(screen, LIME,(WIDTH//2-40, bar_y - (bar_height//2)), (WIDTH//2-40, bar_y+ bar_height//2-1), 60)#greenish yellow markers

        pygame.draw.line(screen, YELLOW,(WIDTH//2-120, bar_y - bar_height//2), (WIDTH//2-120, bar_y+ bar_height//2-1), 100)#yellow
        pygame.draw.line(screen, YELLOW,(WIDTH//2+120, bar_y - bar_height//2), (WIDTH//2+120, bar_y+ bar_height//2-1), 100)
        pygame.draw.rect(screen, BLUE,(pos_x, bar_y - square_size//2, square_size, square_size))
        text = font.render(f"Score: {score}/10", True, (255, 255, 255))
        screen.fill((0, 0, 0), text_surface)
        screen.blit(text, screen.fill((0, 0, 0), text_surface))

        pygame.display.flip()
        clock.tick(60) #60 fps till I implement vsync
    return clicks
