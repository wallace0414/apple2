import pygame
import random

WIDTH = 1280
HEIGHT = 620
BALLOON_SPEED = 4
FONT_COLOR = (100, 131, 142)
GAME_TIME = 10000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Apple catch')
clock = pygame.time.Clock()

bg_surf = pygame.image.load('img/sky1.png').convert_alpha()
bg_surf = pygame.transform.rotozoom(bg_surf, 0, 0.7)
bg_rect = bg_surf.get_rect(bottomleft=(0, HEIGHT))

apple_surf = pygame.image.load('img/apple_1.png').convert_alpha()
apple_surf = pygame.transform.rotozoom(apple_surf, 0, 0.05)
apple_rect = []
apple_timer = pygame.USEREVENT + 1
pygame.time.set_timer(apple_timer, 1000)

penguin_surf = pygame.image.load('img/penguin.png').convert_alpha()
penguin_surf = pygame.transform.rotozoom(penguin_surf, 0, 0.7)
penguin_rect = penguin_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))

game_font = pygame.font.SysFont('arial', 30, bold=True)
title_surf = game_font.render('APPLE CATCH', True, FONT_COLOR)
title_rect = title_surf.get_rect(center=(WIDTH / 2, 200))
run_surf = game_font.render('Press space to run', True, FONT_COLOR)
run_rect = run_surf.get_rect(center=(WIDTH / 2, HEIGHT - 150))

start_time = pygame.time.get_ticks()
score = 0
running = True
active = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            penguin_rect = penguin_surf.get_rect(center=(mouse_x, HEIGHT - 50))
        if event.type == apple_timer:
            apple_rect.append(apple_surf.get_rect(
                center=(random.randint(50, WIDTH - 50), 30)))

    screen.blit(bg_surf, bg_rect)

    if active:
        for index, balloon_rect in enumerate(apple_rect):
            apple_rect[index].top += BALLOON_SPEED
            mov_y = random.randint(0, 2)
            if mov_y == 0:
                apple_rect[index].left -= 2
            else:
                apple_rect[index].left += 2
            if apple_rect[index].bottom <= -10:
                del apple_rect[index]
            if balloon_rect.colliderect(penguin_rect):
                del apple_rect[index]
                score += 1

            screen.blit(apple_surf, balloon_rect)
        screen.blit(penguin_surf, penguin_rect)

        score_surf = game_font.render('score: ' + str(score), True, FONT_COLOR)
        score_rect = score_surf.get_rect(topleft=(10, 10))
        screen.blit(score_surf, score_rect)

        time_left = int((start_time + GAME_TIME - pygame.time.get_ticks()) / 1000)
        if time_left <= 0:
            active = False
        time_left_surf = game_font.render('time left: ' + str(time_left), True, FONT_COLOR)
        time_left_rect = time_left_surf.get_rect(topleft=(10, 50))
        screen.blit(time_left_surf, time_left_rect)

    else:
        screen.blit(title_surf, title_rect)
        screen.blit(apple_surf, apple_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        screen.blit(penguin_surf, penguin_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        screen.blit(run_surf, run_rect)

        if score:
            final_score_surf = game_font.render('SCORE: ' + str(score), True, FONT_COLOR)
            final_score_rect = final_score_surf.get_rect(center=(WIDTH / 2, HEIGHT - 220))
            screen.blit(final_score_surf, final_score_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            score = 0
            apple_rect = []
            start_time = pygame.time.get_ticks()
            active = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
