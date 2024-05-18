import pygame


class Sound:
    pygame.mixer.init()
    click_sound = pygame.mixer.Sound("src/assets/audio/click.mp3")
    win_sound = pygame.mixer.Sound("src/assets/audio/win.mp3")
    draw_sound = pygame.mixer.Sound("src/assets/audio/draw.mp3")
