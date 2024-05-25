import math
import pygame
from pygame.locals import *

from src.frame import Frame
from src.player import Player
from src.color import Color
from src.board import Board
from src.sound import Sound
from src.input import Input


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
        self.show_board = False
        txt = self.player.turns
        # self.frame.draw_board(self.board.grid, txt, self.scores)
        self.button_toggle = self.frame.create_button(idx=1, url="src/assets/svg/user.svg")

        self.input_rendered = False
        self.add_inputs()

        pygame.display.update()

    def start(self):
        self.flag = True
        while self.flag:
            self.events()
            if not self.show_board:
                self.name_screen()
            else:
                self.board_screen()
            self.bottom_menu()
            pygame.display.update()
            self.clock.tick(100)
        return

    def add_inputs(self):
        # if not self.input_rendered:
        input_width, input_height = 200, 50
        left = (self.frame.screen_width / 2) - (input_width / 2)
        left_one = (self.frame.screen_width / 2) - input_width - 10
        left_two = (self.frame.screen_width / 2) + 10
        top = (self.frame.screen_height / 2) - (input_height / 2)
        btn_left = (self.frame.screen_width / 2) - (40 / 2)
        self.login = self.frame.create_button(idx=2, url="src/assets/svg/login.svg",top=top + input_height + 10, left=btn_left)

        if self.two_players:
            self.input_one = Input(left_one, top, input_width, input_height, placeholder="Player one")
            self.input_two = Input(left_two, top, input_width, input_height, placeholder="Player two")
            self.input_boxes = [self.input_two, self.input_one]
        else:
            self.input_one = Input(left, top, input_width, input_height, placeholder="Your Name")
            self.input_boxes = [self.input_one]
        self.input_rendered = True

    def name_screen(self):
        for box in self.input_boxes:
            box.update()
        self.frame.screen.fill(Color.bg)
        for box in self.input_boxes:
            box.draw(self.frame.screen)

        btn_left = (self.frame.screen_width / 2) - (40 / 2)
        input_height = self.input_boxes[0].rect.height
        top = (self.frame.screen_height / 2) - (input_height / 2)
        self.login = self.frame.create_button(idx=2, url="src/assets/svg/login.svg",top=top + input_height + 20, left=btn_left)
        if self.is_btn_clicked and self.login.collidepoint(pygame.mouse.get_pos()):
            self.show_board = True

    def board_screen(self):
        if self.coords and self.board.is_legal_move(self.coords, self.board.grid) and not self.game_over:
            Sound.click_sound.play()
            choice = Board.step(*self.coords)
            if self.two_players:
                self.board.update_board(choice, self.player.value)
            else:
                self.board.update_board(choice, self.player.value)
            self.player = self.player.other

            if not self.two_players:
                self.frame.draw_board(
                    self.board.grid, self.player.turns, self.scores)
                pygame.display.update()
                best_score = -math.inf
                best_move = None
                for i in range(len(self.board.grid)):
                    if self.board.grid[i] == self.board.blank:
                        self.board.grid[i] = Player.O.value
                        score = self.minimax(self.board.grid, False, 0)
                        self.board.grid[i] = self.board.blank
                        if score > best_score:
                            best_score = score
                            best_move = i
                if not isinstance(best_move, type(None)):
                    self.board.grid[best_move] = Player.O.value
                self.player = self.player.other
                self.frame.draw_board(self.board.grid, self.player.turns, self.scores)
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
                self.delay = self.current_time + 1000
            elif result == self.draw:  # if the game is draw
                Sound.draw_sound.play()
                self.txt = "Game Draw"
                self.delay = self.current_time + 1000
        if self.delay and self.delay < self.current_time:  # Restart game after 1 second
            self.board.grid = [self.board.blank] * 9
            self.txt = self.player.turns
            self.game_over = False
            self.delay = None
        self.frame.draw_board(self.board.grid, self.player.turns, self.scores)

    def events(self):
        self.coords = None
        self.current_time = pygame.time.get_ticks()
        self.is_btn_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the program is quit
                self.flag = False
                return
            if event.type == MOUSEBUTTONUP:  # Checked if mouse button is clicked
                self.coords = self.frame.get_clicked_spot(event.pos[0], event.pos[1])
                self.is_btn_clicked = True
            for box in self.input_boxes:
                box.handle_event(event)

    def bottom_menu(self):
        old_two_player = self.two_players
        self.two_players = self.frame.trigger_click(self.button_toggle, self.is_btn_clicked, self.two_players)
        if self.two_players != old_two_player:
            self.board.grid = [self.board.blank] * 9
            self.scores = [0, 0]
            self.player = Player.X
            self.show_board = False
            self.add_inputs()

        if self.two_players:
            self.button_toggle = self.frame.create_button(1, "src/assets/svg/users.svg")
        else:
            self.button_toggle = self.frame.create_button(1, "src/assets/svg/user.svg")

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
