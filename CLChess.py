import sys
from board import Board
from game import Game


def parse_args(argv):
    board = Board()
    starting_turn = 0
    white_player = 'human'
    black_player = 'human'

    if len(argv) > 1:
        arg = argv[1]
        if arg.endswith('.txt'):
            board.init_board()
            starting_turn = board.read_move_file(arg) % 2
        elif arg in ('-', 'startpos'):
            board.init_board()
        else:
            board, starting_turn = Board.from_fen(arg)
    else:
        board.init_board()

    if len(argv) > 3:
        mode = argv[2]   # 'rand' or 'simple'
        side = argv[3]   # 'White', 'Black', or same as mode for bot-vs-bot

        if side == 'White':
            white_player = 'human'
            black_player = mode
        elif side == 'Black':
            white_player = mode
            black_player = 'human'
        else:
            white_player = mode
            black_player = side

    return board, white_player, black_player, starting_turn


if __name__ == '__main__':
    board, white_player, black_player, starting_turn = parse_args(sys.argv)
    game = Game(board, white_player, black_player, starting_turn)
    game.play()
