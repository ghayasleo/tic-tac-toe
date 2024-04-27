import pygame
from pygame.locals import *
from src.constants import *


def render_symbol(symbol: int, tile_left: int, tile_top: int):
    sym: pygame.Surface
    if symbol == PLAYER_O:
        sym = pygame.image.load('src/assets/svg/circle.svg')
    elif symbol == PLAYER_X:
        sym = pygame.image.load('src/assets/svg/cross.svg')
    if symbol != BLANK:
        rect = sym.get_rect()
        rect.center = tile_left + int(TILE_SIZE / 2), tile_top + int(TILE_SIZE / 2)
        SCREEN.blit(sym, rect)


def create_board(board: list[int]):
    for y in range(3):
        for x in range(3):
            tile = x*3+y
            is_empty = board[tile] == BLANK
            drawTile(x, y, board[tile], is_empty)


def drawTile(x: int, y: int, symbol: int, is_empty: bool):
    tile_x = y * TILE_SIZE
    tile_y = x * TILE_SIZE
    tile_left = (SCREEN_WIDTH / 2 + tile_x - GRID_SIZE / 2)
    tile_top = SCREEN_HEIGHT / 2 + tile_y - GRID_SIZE / 2

    rect = pygame.Rect(tile_left, tile_top, TILE_SIZE, TILE_SIZE)
    box = pygame.draw.rect(SCREEN, CLR_BG, rect)
    hover = box.collidepoint(pygame.mouse.get_pos())
    if hover:
        box = pygame.draw.rect(SCREEN, CLR_HOVER, rect)

    if y != 2:
        line_rect = pygame.Rect(tile_left + TILE_SIZE - 4, tile_top, 4, TILE_SIZE)
        line = pygame.draw.rect(SCREEN, CLR_WHITE, line_rect, border_radius=10)
        box.clip(line)
    if x != 2:
        line_rect = pygame.Rect(tile_left, tile_top + TILE_SIZE - 4, TILE_SIZE, 4)
        line = pygame.draw.rect(SCREEN, CLR_WHITE, line_rect, border_radius=10)
        box.clip(line)

    render_symbol(symbol, tile_left, tile_top)
    # textSurf = BASICFONT.render(f"×-○", True, CLR_WHITE)
    # textRect = textSurf.get_rect()
    # textRect.center = tile_left + int(TILE_SIZE / 2), tile_top + int(TILE_SIZE / 2)
    # SCREEN.blit(textSurf, textRect)


def main():
    global SCREEN, BASICFONT

    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    SCREEN.fill(CLR_BG)
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption(TITLE)
    BASICFONT = pygame.font.Font('src/assets/font/google-sans.ttf', SYM_SIZE)
    board = [BLANK] * 9
    create_board(board)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        board_surfacae = pygame.Surface((GRID_SIZE, GRID_SIZE))
        board_surfacae.blit(SCREEN, (0, 0))
        board_surfacae.fill("#00ff00")
        create_board(board)
        pygame.display.update()
        CLOCK.tick(60)
