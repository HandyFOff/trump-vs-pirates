import pygame
import random
pygame.init()

# Screen
FPS = pygame.time.Clock()
screen = pygame.display.set_mode((612, 228))
img_logo = pygame.image.load('assets/icon.png')
pygame.display.set_caption('HandyF Game')
pygame.display.set_icon(pygame.image.load('assets/icon.png'))

# BG MUSIC
bg_sound = pygame.mixer.Sound('assets/music/bg_music.mp3')
bg_sound.set_volume(0.1)

# BG
bg = pygame.image.load('assets/bg.jpg').convert_alpha()
bg_x = 0

# Player
player_anim_count = 0
player_speed = 10
player_x = 124
player_y = 150
jump_count = 8
is_jump = False

# Enemy
pirate_list_in_game = []
pirate = pygame.image.load('assets/enemy/pirate.png').convert_alpha()
pirate_time_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(pirate_time_spawn, 5000)

# Animations
walk_stand = pygame.image.load('assets/player/pygame_idle.png').convert_alpha()
walk_right = [
    pygame.image.load('assets/player/right/pygame_right_1.png').convert_alpha(),
    pygame.image.load('assets/player/right/pygame_right_2.png').convert_alpha(),
    pygame.image.load('assets/player/right/pygame_right_3.png').convert_alpha(),
    pygame.image.load('assets/player/right/pygame_right_4.png').convert_alpha(),
    pygame.image.load('assets/player/right/pygame_right_5.png').convert_alpha(),
    pygame.image.load('assets/player/right/pygame_right_6.png').convert_alpha(),
]
walk_left = [
    pygame.image.load('assets/player/left/pygame_left_1.png').convert_alpha(), 
    pygame.image.load('assets/player/left/pygame_left_2.png').convert_alpha(),
    pygame.image.load('assets/player/left/pygame_left_3.png').convert_alpha(),
    pygame.image.load('assets/player/left/pygame_left_4.png').convert_alpha(),
    pygame.image.load('assets/player/left/pygame_left_5.png').convert_alpha(),
    pygame.image.load('assets/player/left/pygame_left_6.png').convert_alpha(),
]

# Endless Screen
endless_label = pygame.font.Font('assets/fonts/BebasNeue-Regular.ttf', 40)
lose_label = endless_label.render('WASTED', False, (233, 0, 0))
restart = endless_label.render('Retry game', False, (255, 255, 255))
restart_hitbox = restart.get_rect(topleft=(232, 132))


# GamePlay
gameplay = True

# Game
running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 612, 0))

    if gameplay:
        # HITBOXES
        player_hitbox = walk_left[0].get_rect(topleft=(player_x, player_y))

        if pirate_list_in_game:
            for (i, mob) in enumerate(pirate_list_in_game):
                screen.blit(pirate, mob)
                mob.x -= 10

                if mob.x < -10:
                    pirate_list_in_game.pop(i)

                if player_hitbox.colliderect(mob):
                    gameplay = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 10:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 600:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 5:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 6
        if (bg_x == -618):
            bg_x = 0
    else:
        screen.fill((0, 0, 0))
        screen.blit(lose_label, (256, 62))
        screen.blit(restart, restart_hitbox)

        mouse = pygame.mouse.get_pos()
        if restart_hitbox.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 124
            pirate_list_in_game.clear()

    pygame.display.update()

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
            pygame.quit()
        if event.type == pirate_time_spawn:
            pirate_list_in_game.append(pirate.get_rect(topleft=(620, 155)))

    FPS.tick(18)
