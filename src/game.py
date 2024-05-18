import math
import pygame
from pygame.locals import *

from src.frame import Frame
from src.player import Player
from src.board import Board
from src.sound import Sound


class Game:
    draw = 20
    cont = 10

    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.frame = Frame()
        self.board = Board()
        self.player = Player.X
        self.two_players = True
        self.game_over = False
        self.scores = [0, 0]
        self.delay = None
        self.is_btn_clicked = False
        txt = self.player.turns
        self.frame.draw_board(self.board.grid, txt, self.scores)
        self.button_toggle = self.frame.create_button(1, "src/assets/svg/user.svg")
        pygame.display.update()

    def start(self):
        while True:
            coords = None
            current_time = pygame.time.get_ticks()
            self.is_btn_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Check if the program is quit
                    return
                if event.type == MOUSEBUTTONUP:  # Checked if mouse button is clicked
                    coords = self.frame.get_clicked_spot(event.pos[0], event.pos[1])
                    self.is_btn_clicked = True
            if coords and self.board.is_legal_move(coords, self.board.grid) and not self.game_over:
                Sound.click_sound.play()
                choice = Board.step(*coords)
                if self.two_players:
                    self.board.update_board(choice, self.player.value)
                else:
                    self.board.update_board(choice, self.player.value)
                self.player = self.player.other

                if not self.two_players:
                    self.frame.draw_board(
                        self.board.grid, self.player.turns, self.scores)
                    pygame.display.update()
                    bestScore = -math.inf
                    bestMove = None
                    for i in range(len(self.board.grid)):
                        if self.board.grid[i] == self.board.blank:
                            self.board.grid[i] = Player.O.value
                            score = self.minimax(self.board.grid, False, 0)
                            self.board.grid[i] = self.board.blank
                            if score > bestScore:
                                bestScore = score
                                bestMove = i
                    if not isinstance(bestMove, type(None)):
                        self.board.grid[bestMove] = Player.O.value
                    self.player = self.player.other
                    self.frame.draw_board(
                        self.board.grid, self.player.turns, self.scores)
                    pygame.display.update()

                result = self.game_result(self.board.grid)
                self.game_over = result != self.cont
                if result == Player.X.value or result == Player.O.value:
                    Sound.win_sound.play()
                    self.player = self.player.other
                    self.scores[self.player.value - 1] += 1
                    self.txt = self.player.winning
                    if not self.two_players:
                        self.player = self.player.X
                    self.delay = current_time + 1000
                elif result == self.draw:  # if the game is draw
                    Sound.draw_sound.play()
                    self.txt = "Game Draw"
                    self.delay = current_time + 1000
            if self.delay and self.delay < current_time:  # Restart game after 1 second
                self.board.grid = [self.board.blank] * 9
                self.txt = self.player.turns
                self.game_over = False
                self.delay = None
            self.frame.draw_board(self.board.grid, self.player.turns, self.scores)
            old_two_player = self.two_players
            self.two_players = self.frame.trigger_click(self.button_toggle, self.is_btn_clicked, self.two_players)
            if self.two_players != old_two_player:
                self.board.grid = [self.board.blank] * 9
                self.scores = [0, 0]
                self.player = Player.X

            if self.two_players:
                self.button_toggle = self.frame.create_button(1, "src/assets/svg/users.svg")
            else:
                self.button_toggle = self.frame.create_button(1, "src/assets/svg/user.svg")
            pygame.display.update()
            self.clock.tick(100)

    def game_result(self, board: list[int]):
        def check_horizontal(player: int):
            for i in [0, 3, 6]:
                row = board[i:i+3]
                if self.board.blank not in row and sum(row) == 3 * player:
                    return player

        def check_vertical(player: int):
            for i in range(3):
                column = board[i::3]
                if self.board.blank not in column and sum(column) == 3 * player:
                    return player

        def check_diagonals(player: int):
            diagonal1 = board[0::4]
            diagonal2 = board[2:7:2]
            if (self.board.blank not in diagonal1 and sum(diagonal1) == 3 * player) or (self.board.blank not in diagonal2 and sum(diagonal2) == 3 * player):
                return player

        for player in [Player.X.value, Player.O.value]:
            if any([check_horizontal(player), check_vertical(player), check_diagonals(player)]):
                return player

        is_draw = self.board.blank not in board
        return self.draw if is_draw else self.cont

    def minimax(self, board: list[int], is_maximizing: bool, depth: int):
        result = self.game_result(board)

        if result != self.cont:
            if result == self.draw:
                return 0
            else:
                return 1 if result == self.player.O.value else -1
        if is_maximizing:
            best_score = -math.inf
            for i in range(len(board)):
                if board[i] == self.board.blank:
                    board[i] = self.player.O.value
                    score = self.minimax(board, False, depth + 1)
                    board[i] = self.board.blank
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(len(board)):
                if board[i] == self.board.blank:
                    board[i] = self.player.X.value
                    score = self.minimax(board, True, depth + 1)
                    board[i] = self.board.blank
                    best_score = min(score, best_score)
            return best_score
