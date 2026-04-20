
from engine import Engine


class Game:
    """Owns the game loop. white_player / black_player are 'human', 'rand', or 'simple'."""

    def __init__(self, board, white_player='human', black_player='human', starting_turn=0):
        self.board = board
        self.white_player = white_player
        self.black_player = black_player
        self.starting_turn = starting_turn

    def _take_turn(self, color):
        player = self.white_player if color == 'White' else self.black_player
        if player == 'human':
            return self.board.get_move(color)
        if player == 'rand':
            return Engine.random_move(color, self.board)
        if player == 'simple':
            return Engine.simple_move(color, self.board)
        raise ValueError(f"Unknown player type: {player}")

    def play(self):
        colors = ['White', 'Black']
        idx = self.starting_turn
        while True:
            color = colors[idx]
            self.board.print_board()
            result = self._take_turn(color)
            if result is None:
                return
            idx = 1 - idx
