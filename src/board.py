class Board:
    dimension = 3
    tile_size = 150
    grid_size = tile_size * dimension
    blank = 0

    def __init__(self):
        self.grid = [self.blank] * 9

    def step(x: int, y: int):
        return x * 3 + y

    def is_legal_move(self, coords: tuple[int, int], board: list[int]):
        tile = Board.step(*coords)
        if board[tile] != self.blank:
            return False
        return True

    def update_board(self, choice: int, player: int):
        self.grid[choice] = player
