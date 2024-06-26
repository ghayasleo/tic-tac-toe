import time
import math
import pygame
from pygame.locals import *

from src.frame import Frame
from src.player import Player
from src.board import Board
from src.sound import Sound
from src.input import Input
from src.color import Color
from src.button import Button
from src.visualize import Figure


class Game:
    draw = 20
    cont = 10

    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.frame = Frame()
        self.board = Board()
        self.player = Player.X
        self.two_players = False
        self.players = ["", "Bot - Normal"]
        self.outcome = 'draw'
        self.winner = ''
        self.game_over = False
        self.scores = [0, 0]
        self.dificulty_levels = {
            "Normal": 5,
            "Hard": 6,
            "Expert": 7,
        }
        self.bot_difficulty = self.dificulty_levels.get("Normal")
        self.delay = None
        self.delay_bot_move = None
        self.is_btn_clicked = False
        self.display = "name"
        self.show_stats = False
        txt = self.player.turns
        # self.frame.draw_board(self.board.grid, txt, self.scores, self.players)
        self.button_toggle = self.frame.create_icon_btn(idx=1, url="src/assets/svg/user.svg")
        self.chart_toggle = self.frame.create_icon_btn(idx=2, url="src/assets/svg/chart.svg")
        self.difficulty_toggle = self.frame.create_icon_btn(idx=3, url="src/assets/svg/Normal.svg")
        self.btn1 = self.frame.create_button("Head To Head", 1)
        self.btn2 = self.frame.create_button("First Moves", 2, left=self.btn1.left)
        self.btn3 = self.frame.create_button("Wins", 3, left=self.btn2.left)
        self.graph = "wins"
        self.dataset = "src/assets/dataset.csv"
        self.img_url = "./src/assets/img/plot.png"
        self.figure = Figure(self.dataset, self.img_url)
        self.input_rendered = False
        self.add_inputs()

        pygame.display.update()

    def start(self):
        self.flag = True
        while self.flag:
            self.events()
            if self.display == "name":
                self.name_screen()
            elif self.display == "board":
                self.board_screen()
            elif self.display == "graph":
                self.graph_screen()
            self.bottom_menu()
            pygame.display.update()
            self.clock.tick(100)
        return

    def graph_screen(self):
        self.frame.screen.fill(Color.bg)
        img = self.img_url.replace("plot", self.graph)
        image = pygame.image.load(img)
        left = self.frame.screen_width / 2 - image.get_width() / 2
        top = self.frame.screen_height / 2 - image.get_height() / 2
        self.frame.screen.blit(image, (left, top))

        if self.is_btn_clicked and self.btn1.collidepoint(pygame.mouse.get_pos()):
            self.graph = "head-to-head"
        if self.is_btn_clicked and self.btn2.collidepoint(pygame.mouse.get_pos()):
            self.graph = "first-move"
        if self.is_btn_clicked and self.btn3.collidepoint(pygame.mouse.get_pos()):
            self.graph = "wins"

    def add_inputs(self):
        # if not self.input_rendered:
        input_width, input_height = 200, 50
        left = (self.frame.screen_width / 2) - (input_width / 2)
        left_one = (self.frame.screen_width / 2) - input_width - 10
        left_two = (self.frame.screen_width / 2) + 10
        top = (self.frame.screen_height / 2) - (input_height / 2)
        btn_left = (self.frame.screen_width / 2) - (40 / 2)
        self.login = self.frame.create_icon_btn(idx=2, url="src/assets/svg/login.svg",top=top + input_height + 10, left=btn_left)

        if self.two_players:
            self.input_one = Input(left_one, top, input_width, input_height, placeholder="Player one")
            self.input_two = Input(left_two, top, input_width, input_height, placeholder="Player two")
            self.input_boxes = [self.input_one, self.input_two]
        else:
            self.input_one = Input(left, top, input_width, input_height, placeholder="Your Name")
            self.input_boxes = [self.input_one]
        self.input_rendered = True

    def name_screen(self):
        for box in self.input_boxes:
            box.update()
        self.frame.screen.fill(Color.bg)
        self.frame.write_title()
        for box in self.input_boxes:
            box.draw(self.frame.screen)

        btn_left = (self.frame.screen_width / 2) - (40 / 2)
        input_height = self.input_boxes[0].rect.height
        top = (self.frame.screen_height / 2) - (input_height / 2)
        self.login = self.frame.create_icon_btn(idx=2, url="src/assets/svg/login.svg",top=top + input_height + 20, left=btn_left)
        if self.is_btn_clicked and self.login.collidepoint(pygame.mouse.get_pos()):
            is_empty = False
            for idx, input in enumerate(self.input_boxes):
                if input.text == "":
                    is_empty = True
                else:
                    self.players[idx] = input.text
            if len(self.input_boxes) == 1:
                self.players[1] = "Bot - Normal"
            if not is_empty:
                self.display = "board"
                self.first_move = self.players[0]
                self.second_move = self.players[1]

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
                self.frame.draw_board(self.board.grid, self.player.turns, self.scores, self.players)
                pygame.display.update()
                best_score = -math.inf
                best_move = None
                for i in range(len(self.board.grid)):
                    if self.board.grid[i] == self.board.blank:
                        self.board.grid[i] = Player.O.value
                        score = self.minimax(self.board.grid, False, 0, self.bot_difficulty, -math.inf, math.inf)
                        self.board.grid[i] = self.board.blank
                        if score > best_score:
                            best_score = score
                            best_move = i
                if not isinstance(best_move, type(None)):
                    self.board.grid[best_move] = Player.O.value
                self.player = self.player.other
                self.frame.draw_board(self.board.grid, self.player.turns, self.scores, self.players)
                pygame.display.update()

            result = self.game_result(self.board.grid)
            self.game_over = result != self.cont
            if result == Player.X.value or result == Player.O.value:
                self.player = self.player.other
                Sound.win_sound.play()
                self.winner = self.players[result - 1]
                self.outcome = 'win'
                self.scores[self.player.value - 1] += 1
                self.txt = self.player.winning
                if not self.two_players:
                    self.player = self.player.X
                self.update_csv()
                if self.two_players:
                    self.second_move = self.players[self.player.value - 1]
                    self.player = self.player.other
                self.first_move = self.players[self.player.value - 1]
                self.delay = self.current_time + 1000
            elif result == self.draw:  # if the game is draw
                Sound.draw_sound.play()
                self.winner = ''
                self.outcome = 'draw'
                self.txt = "Game Draw"
                self.update_csv()
                self.delay = self.current_time + 1000
        if self.delay and self.delay < self.current_time:  # Restart game after 1 second
            self.board.grid = [self.board.blank] * 9
            self.txt = self.player.turns
            self.game_over = False
            self.delay = None
        self.frame.draw_board(self.board.grid, self.player.turns, self.scores, self.players)

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
        if self.display == "board" and not self.two_players:
            if self.is_btn_clicked and self.difficulty_toggle.collidepoint(pygame.mouse.get_pos()):
                if self.bot_difficulty == self.dificulty_levels.get("Normal"):
                    self.bot_difficulty = self.dificulty_levels.get("Hard")
                    self.players[1] = "Bot - Hard"
                elif self.bot_difficulty == self.dificulty_levels.get("Hard"):
                    self.bot_difficulty = self.dificulty_levels.get("Expert")
                    self.players[1] = "Bot - Expert"
                elif self.bot_difficulty == self.dificulty_levels.get("Expert"):
                    self.bot_difficulty = self.dificulty_levels.get("Normal")
                    self.players[1] = "Bot - Normal"
                self.board.grid = [self.board.blank] * 9
                self.scores = [0, 0]
                self.player = Player.X

    def bottom_menu(self):
        old_two_player = self.two_players
        self.two_players = self.frame.trigger_click(self.button_toggle, self.is_btn_clicked, self.two_players)
        if self.two_players != old_two_player:
            self.board.grid = [self.board.blank] * 9
            self.scores = [0, 0]
            self.player = Player.X
            self.display = "name"
            self.add_inputs()

        if self.two_players:
            self.button_toggle = self.frame.create_icon_btn(1, "src/assets/svg/users.svg")
        else:
            self.button_toggle = self.frame.create_icon_btn(1, "src/assets/svg/user.svg")
        if self.display == "board":
            if not self.two_players:
                key_list = list(self.dificulty_levels.keys())
                val_list = list(self.dificulty_levels.values())
                position = val_list.index(self.bot_difficulty)
                self.difficulty_toggle = self.frame.create_icon_btn(idx=3, url=f"src/assets/svg/{key_list[position]}.svg")
        self.chart_toggle = self.frame.create_icon_btn(idx=2, url="src/assets/svg/chart.svg")
        if self.is_btn_clicked and self.chart_toggle.collidepoint(pygame.mouse.get_pos()):
            if not self.display == "graph":
                self.display = "graph"
            else:
                if self.players[0] != "":
                    self.display = "board"
                else:
                    self.display = "name"
        if self.display == "graph":
            self.btn1 = self.frame.create_button("Head To Head", 1)
            self.btn2 = self.frame.create_button("First Moves", 2, left=self.btn1.left)
            self.btn3 = self.frame.create_button("Wins", 3, left=self.btn2.left)

    def update_csv(self):
        # print(self.first_move, self.second_move)
        player_two = self.players[1] if "-" not in self.players[1] else "Bot"
        winner = self.winner if "-" not in self.winner else "Bot"
        winner = winner if self.outcome == 'win' else ''
        row = f"{self.players[0]},{player_two},{winner},{self.outcome},{self.first_move}"
        key_list = list(self.dificulty_levels.keys())
        val_list = list(self.dificulty_levels.values())
        position = val_list.index(self.bot_difficulty)
        difficulty = key_list[position]
        if not self.two_players:
            row += f",{difficulty}\n"
        else:
            row += ",\n"
        with open('src/assets/dataset.csv','a') as fd:
            fd.write(row)
            fd.close()
            self.figure.create_figure()

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

    def minimax(self, board: list[int], is_maximizing: bool, depth: int, max_depth: int, alpha: float, beta: float):
        result = self.game_result(board)

        if result!= self.cont or depth == max_depth:
            if result == self.draw:
                return 0
            else:
                return 1 if result == self.player.O.value else -1
        if is_maximizing:
            best_score = -math.inf
            for i in range(len(board)):
                if board[i] == self.board.blank:
                    board[i] = self.player.O.value
                    score = self.minimax(board, False, depth + 1, max_depth, alpha, beta)
                    board[i] = self.board.blank
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha or depth == max_depth:
                        break
            return best_score
        else:
            best_score = math.inf
            for i in range(len(board)):
                if board[i] == self.board.blank:
                    board[i] = self.player.X.value
                    score = self.minimax(board, True, depth + 1, max_depth, alpha, beta)
                    board[i] = self.board.blank
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha or depth == max_depth:
                        break
            return best_score