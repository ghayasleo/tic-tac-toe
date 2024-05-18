import pygame

from src.board import Board
from src.font import Font
from src.color import Color
from src.player import Player
from src.constants import *


class Frame:
    screen_width = 1280
    screen_height = 720

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.screen.fill(Color.bg)
        pygame.display.set_caption(TITLE)
        pygame_icon = pygame.image.load('src/assets/img/favicon.png')
        pygame.display.set_icon(pygame_icon)

    def draw_board(self, board: list[int], text: str, scores: list[int]):
        self.screen.fill(Color.bg)
        for y in range(3):
            for x in range(3):
                tile = Board.step(x, y)
                self.draw_tile(x, y, board[tile])
        self.write_text(text, self.screen_width / 2,
                        (self.screen_height / 2) + (Board.grid_size / 2) + 10)
        score = f"{scores[0]} - {scores[1]}"
        players = f"{Player.X.name}       {Player.O.name}"
        self.write_text(TITLE, self.screen_width / 2, (self.screen_height / 2) -
                        (Board.grid_size / 2) - 90, font=Font.large, color=Color.theme)
        self.write_text(score, self.screen_width / 2, (self.screen_height /
                        2) + (Board.grid_size / 2) + 65, font=Font.small)
        self.write_text(players, self.screen_width / 2, (self.screen_height /
                        2) + (Board.grid_size / 2) + 95, font=Font.xsmall)

    def draw_tile(self, x: int, y: int, symbol: int):
        tile_top, tile_left = self.get_top_left_of_tile(x, y)

        rect = pygame.Rect(tile_left, tile_top,
                           Board.tile_size, Board.tile_size)
        box = pygame.draw.rect(self.screen, Color.bg, rect)
        hover = box.collidepoint(pygame.mouse.get_pos())
        if hover:
            box = pygame.draw.rect(self.screen, Color.hover, rect)

        if y != 2:
            line_rect = pygame.Rect(
                tile_left + Board.tile_size - 4, tile_top, 4, Board.tile_size)
            line = pygame.draw.rect(
                self.screen, Color.white, line_rect, border_radius=10)
            box.clip(line)
        if x != 2:
            line_rect = pygame.Rect(
                tile_left, tile_top + Board.tile_size - 4, Board.tile_size, 4)
            line = pygame.draw.rect(
                self.screen, Color.white, line_rect, border_radius=10)
            box.clip(line)

        self.render_symbol(symbol, tile_left, tile_top)

    def get_top_left_of_tile(self, x: int, y: int):
        tile_x = y * Board.tile_size
        tile_y = x * Board.tile_size
        tile_left = (self.screen_width / 2 + tile_x - Board.grid_size / 2)
        tile_top = self.screen_height / 2 + tile_y - Board.grid_size / 2
        return (tile_top, tile_left)

    def render_symbol(self, symbol: int, tile_left: int, tile_top: int):
        sym: pygame.Surface
        if symbol == Player.O.value:
            sym = pygame.image.load('src/assets/svg/circle.svg')
        elif symbol == Player.X.value:
            sym = pygame.image.load('src/assets/svg/cross.svg')
        if symbol != Board.blank:
            rect = sym.get_rect()
            rect.center = tile_left + \
                int(Board.tile_size / 2), tile_top + int(Board.tile_size / 2)
            self.screen.blit(sym, rect)

    def write_text(self, text: str, left: int, top: int, font=None, color=Color.white):
        if not font:
            font = Font.base
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = left, top + text_rect.height / 2
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def get_clicked_spot(self, x_axis: int, y_axis: int):
        for y in range(3):
            for x in range(3):
                tile_top, tile_left = self.get_top_left_of_tile(x, y)
                rect = pygame.Rect(tile_left, tile_top,
                                   Board.tile_size, Board.tile_size)
                if rect.collidepoint(x_axis, y_axis):
                    return (x, y)
        return None

    def create_button(self, idx: int, url: str):
        size = 40
        left = size * idx + abs((idx - 1) * 20)
        top = self.screen_height - 40 - size
        rect = pygame.Rect(left, top, size, size)
        box = pygame.draw.rect(self.screen, Color.hover, rect, border_radius=5)
        pygame.draw.rect(self.screen, Color.btn_border,
                         rect, 1, border_radius=5)
        icon = pygame.image.load(url)
        icon_rect = icon.get_rect()
        icon_rect.center = left + size / 2, top + size / 2
        self.screen.blit(icon, icon_rect)
        return box

    def trigger_click(self, box: pygame.Rect, is_clicked: bool, two_players: bool):
        if is_clicked and box.collidepoint(pygame.mouse.get_pos()):
            return False if two_players == True else True
        return two_players
