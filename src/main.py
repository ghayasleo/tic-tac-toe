import pygame
import math
import pickle
import os
from pygame.locals import *
from src.constants import *


# def addMatch(data):
#     with open(MATCH_FILE, 'wb') as file:
#         pickle.dump(data, file)


# def getMatches():
#     if os.path.exists(MATCH_FILE):
#         with open(MATCH_FILE, 'rb') as file:
#                 loaded_data = pickle.load(file)
#                 return loaded_data


# def saveMatch(data):
#     if os.path.exists(MATCH_FILE):
#         matches = getMatches()
#         matches.append(data)
#         addMatch(matches)


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


def step(x: int, y: int):
    return x * 3 + y


def create_text(text: str, left: int, top: int, font = None, color = CLR_WHITE):
    if not font:
        font = FONT_BASE
    textSurf = font.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.center = left, top + textRect.height / 2
    SCREEN.blit(textSurf, textRect)
    return textRect


def create_board(board: list[int], notify: str):
    SCREEN.fill(CLR_BG)

    for y in range(3):
        for x in range(3):
            tile = step(x, y)
            drawTile(x, y, board[tile])
    create_text(notify, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + (GRID_SIZE / 2) + 10)

    score = f"{SCORES[0]} - {SCORES[1]}"
    players = f"{symbol_to_text(PLAYER_X)}       {symbol_to_text(PLAYER_O)}"
    create_text(TITLE, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - (GRID_SIZE / 2) - 90, font=FONT_L, color=THEME_CLR)
    create_text(score, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + (GRID_SIZE / 2) + 65, font=FONT_SM)
    create_text(players, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + (GRID_SIZE / 2) + 95, font=FONT_XS)


def update_board(board: list[int], choice: int, player: int):
    board[choice] = player


def symbol_to_text(symbol: int):
    if symbol == PLAYER_O:
        return "O"
    elif symbol == PLAYER_X:
        return "X"
    return ""


def get_top_left_of_tile(x: int, y: int):
    tile_x = y * TILE_SIZE
    tile_y = x * TILE_SIZE
    tile_left = (SCREEN_WIDTH / 2 + tile_x - GRID_SIZE / 2)
    tile_top = SCREEN_HEIGHT / 2 + tile_y - GRID_SIZE / 2
    return (tile_top, tile_left)


def drawTile(x: int, y: int, symbol: int):
    tile_top, tile_left = get_top_left_of_tile(x, y)

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


def is_legal_move(coords: tuple[int, int], board: list[int]):
    tile = step(*coords)
    if board[tile] != BLANK:
        return False
    return True


def get_clicked_spot(x_axis: int, y_axis: int):
    for y in range(3):
        for x in range(3):
            tile_top, tile_left = get_top_left_of_tile(x, y)
            rect = pygame.Rect(tile_left, tile_top, TILE_SIZE, TILE_SIZE)
            if rect.collidepoint(x_axis, y_axis):
                return (x, y)
    return None


def game_result(board: list[int]):
    def check_horizontal(player: int):
        for i in [0, 3, 6]:
            row = board[i:i+3]
            if BLANK not in row and sum(row) == 3 * player:
                return player

    def check_vertical(player: int):
        for i in range(3):
            column = board[i::3]
            if BLANK not in column and sum(column) == 3 * player:
                return player

    def check_diagonals(player: int):
        diagonal1 = board[0::4]
        diagonal2 = board[2:7:2]
        if (BLANK not in diagonal1 and sum(diagonal1) == 3 * player) or (BLANK not in diagonal2 and sum(diagonal2) == 3 * player):
            return player

    for player in [PLAYER_X, PLAYER_O]:
        if any([check_horizontal(player), check_vertical(player), check_diagonals(player)]):
            return player

    is_draw = BLANK not in board
    return DRAW if is_draw else CONT


def check_result(board: list[int], player: int):
    result = game_result(board)

    if result == player:
        return f"{symbol_to_text(player)} wins!"
    elif result == DRAW:
        return "Game Draw"


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


obj = {
    PLAYER_X: "X",
    PLAYER_O: "O",
    CONT: "Continue",
    DRAW: "Draw"
}

def minimax(board: list[int], is_maximizing: bool, depth: int):
    result = game_result(board)

    if result != CONT:
        if result == DRAW:
            return 0
        else:
            return 1 if result == PLAYER_O else -1
    if is_maximizing:
        best_score = -math.inf
        for i in range(len(board)):
            if board[i] == BLANK:
                board[i] = PLAYER_O
                score = minimax(board, False, depth + 1)
                board[i] = BLANK
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(len(board)):
            if board[i] == BLANK:
                board[i] = PLAYER_X
                score = minimax(board, True, depth + 1)
                board[i] = BLANK
                best_score = min(score, best_score)
        return best_score


def turns(sym, two_players):
    if two_players:
        msg = f"{sym}'s Turn"
    else:
        msg = "Your Turn"
    return msg


def main():
    global SCREEN, SCORES, FONT_BASE, FONT_SM, FONT_XS, FONT_L

    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    SCREEN.fill(CLR_BG)
    clock = pygame.time.Clock()
    pygame.display.set_caption(TITLE)
    pygame_icon = pygame.image.load('src/assets/img/favicon.png')
    pygame.display.set_icon(pygame_icon)
    FONT_L = pygame.font.Font('src/assets/font/sora/Sora-Bold.ttf', L_FONT_SIZE)
    FONT_BASE = pygame.font.Font('src/assets/font/sora/Sora-Regular.ttf', BASE_FONT_SIZE)
    FONT_SM = pygame.font.Font('src/assets/font/sora/Sora-Regular.ttf', SM_FONT_SIZE)
    FONT_XS = pygame.font.Font('src/assets/font/sora/Sora-Regular.ttf', XS_FONT_SIZE)
    pygame.mixer.init()
    click_sound = pygame.mixer.Sound("src/assets/audio/click.mp3")
    win_sound = pygame.mixer.Sound("src/assets/audio/win.mp3")
    draw_sound = pygame.mixer.Sound("src/assets/audio/draw.mp3")
    board = [BLANK] * 9
    two_players = False
    game_over = False
    turn = PLAYER_X
    SCORES = [0, 0]
    sym = symbol_to_text(turn)
    msg = turns(sym, two_players)
    delay = None
    create_board(board, msg)
    pygame.display.update()

    while True:
        coords = None
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == MOUSEBUTTONUP:
                coords = get_clicked_spot(event.pos[0], event.pos[1])
        if coords and is_legal_move(coords, board) and not game_over:
            click_sound.play()
            choice = step(*coords)
            if two_players:
                update_board(board, choice, turn)
            else:
                update_board(board, choice, turn)
            turn = PLAYER_X if turn == PLAYER_O else PLAYER_O
            sym = symbol_to_text(turn)
            msg = turns(sym, two_players)

            if not two_players:
                create_board(board, msg)
                pygame.display.update()
                bestScore = -math.inf
                bestMove = None
                for i in range(len(board)):
                    if board[i] == BLANK:
                        board[i] = PLAYER_O
                        score = minimax(board, False, 0)
                        board[i] = BLANK
                        if score > bestScore:
                            bestScore = score
                            bestMove = i
                if not isinstance(bestMove, type(None)):
                    board[bestMove] = PLAYER_O
                turn = PLAYER_X if turn == PLAYER_O else PLAYER_O
                create_board(board, msg)
                pygame.display.update()

            result = game_result(board)
            game_over = result != CONT
            if result == PLAYER_X or result == PLAYER_O:
                win_sound.play()
                player = PLAYER_X if turn == PLAYER_O else PLAYER_O
                msg = f"{symbol_to_text(player)} wins!"
                SCORES[player - 1] += 1
                delay = current_time + 1000
            elif result == DRAW:
                draw_sound.play()
                msg = "Game Draw"
                delay = current_time + 1000
        if delay and delay < current_time:
            board = [BLANK] * 9
            msg = turns(sym, two_players)
            game_over = False
            delay = None

        create_board(board, msg)
        pygame.display.update()
        clock.tick(100)
