import pygame

from src.frame import Frame


class Button:
    def __init__(self, idx: int, url: str) -> None:
        size = 40
        left = size * idx + abs((idx - 1) * 20)
        top = Frame.screen_height - 40 - size
        rect = pygame.Rect(left, top, size, size)
        box = pygame.draw.rect(SCREEN, CLR_HOVER, rect, border_radius=5)
        pygame.draw.rect(SCREEN, CLR_BTN_BORDER, rect, 1, border_radius=5)
        icon = pygame.image.load(url)
        icon_rect = icon.get_rect()
        icon_rect.center = left + size / 2, top + size / 2
        SCREEN.blit(icon, icon_rect)
