
import random
from open_book import opening_book

# Position evaluation tables (piece-square tables)
# Positive = good for that piece type at that square, indexed rank 8→1, file A→H

_wp = [900, 900, 900, 900, 900, 900, 900, 900,
       50,  50,  50,  50,  50,  50,  50,  50,
       10,  10,  20,  30,  30,  20,  10,  10,
        5,   5,  10,  25,  25,  10,   5,   5,
        0,   0,   0,  20,  20,   0,   0,   0,
        5,  -5, -10,   0,   0, -10,  -5,   5,
        5,  10,  10, -20, -20,  10,  10,   5,
        0,   0,   0,   0,   0,   0,   0,   0]

_wk = [-50, -40, -30, -30, -30, -30, -40, -50,
       -40, -20,   0,   0,   0,   0, -20, -40,
       -30,   0,  10,  15,  15,  10,   0, -30,
       -30,   5,  15,  20,  20,  15,   5, -30,
       -30,   0,  15,  20,  20,  15,   0, -30,
       -30,   5,  10,  15,  15,  10,   5, -30,
       -40, -20,   0,   5,   5,   0, -20, -40,
       -50, -40, -30, -30, -30, -30, -40, -50]

_wb = [-20, -10, -10, -10, -10, -10, -10, -20,
       -10,   0,   0,   0,   0,   0,   0, -10,
       -10,   0,   5,  10,  10,   5,   0, -10,
       -10,   5,   5,  10,  10,   5,   5, -10,
       -10,   0,  10,  10,  10,  10,   0, -10,
       -10,  10,  10,  10,  10,  10,  10, -10,
       -10,   5,   0,   0,   0,   0,   5, -10,
       -20, -10, -10, -10, -10, -10, -10, -20]

_wr = [  0,   0,   0,   0,   0,   0,   0,   0,
          5,  10,  10,  10,  10,  10,  10,   5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
          0,   0,   0,   5,   5,   0,   0,   0]

_wq = [-20, -10, -10,  -5,  -5, -10, -10, -20,
       -10,   0,   0,   0,   0,   0,   0, -10,
       -10,   0,   5,   5,   5,   5,   0, -10,
        -5,   0,   5,   5,   5,   5,   0,  -5,
         0,   0,   5,   5,   5,   5,   0,  -5,
       -10,   5,   5,   5,   5,   5,   0, -10,
       -10,   0,   5,   0,   0,   0,   0, -10,
       -20, -10, -10,  -5,  -5, -10, -10, -20]

_bp = [  0,   0,   0,   0,   0,   0,   0,   0,
          5,  10,  10, -20, -20,  10,  10,   5,
          5,  -5, -10,   0,   0, -10,  -5,   5,
          0,   0,   0,  20,  20,   0,   0,   0,
          5,   5,  10,  25,  25,  10,   5,   5,
         10,  10,  20,  30,  30,  20,  10,  10,
         50,  50,  50,  50,  50,  50,  50,  50,
        900, 900, 900, 900, 900, 900, 900, 900]

_bk = [-50, -40, -30, -30, -30, -30, -40, -50,
       -40, -20,   0,   0,   0,   0, -20, -40,
       -30,   0,  10,  15,  15,  10,   0, -30,
       -30,   5,  15,  20,  20,  15,  -5, -30,
       -30,   0,  15,  20,  20,  15,   0, -30,
       -30,   5,  10,  15,  15,  10,  -5, -30,
       -40, -20,   0,   5,   5,   0, -20, -40,
       -50, -40, -30, -30, -30, -30, -40, -50]

_bb = [-20, -10, -10, -10, -10, -10, -10, -20,
       -10,   5,   0,   0,   0,   0,   5, -10,
       -10,  10,  10,  10,  10,  10,  10, -10,
       -10,   0,  10,  10,  10,  10,   0, -10,
       -10,   5,   5,  10,  10,   5,   5, -10,
       -10,   0,   5,  10,  10,   5,   0, -10,
       -10,   0,   0,   0,   0,   0,   0, -10,
       -20, -10, -10, -10, -10, -10, -10, -20]

_br = [  0,   0,   0,   5,   5,   0,   0,   0,
         -5,   0,   0,   0,   0,   0,   0,  -5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
         -5,   0,   0,   0,   0,   0,   0,  -5,
          5,   0,  10,  10,  10,  10,  10,   5,
          0,   0,   0,   0,   0,   0,   0,   0,
          0,   0,   0,   5,   5,   0,   0,   0]

_bq = [-20, -10, -10,  -5,  -5, -10, -10, -20,
       -10,   0,   0,   0,   0,   0,   0, -10,
       -10,   0,   5,   5,   5,   5,   0, -10,
        -5,   0,   5,   5,   5,   5,   0,  -5,
        -5,   0,   5,   5,   5,   5,   0,  -5,
       -10,   0,   5,   5,   5,   5,   0, -10,
       -10,   0,   0,   0,   0,   0,   0, -10,
       -20, -10, -10,  -5,  -5, -10, -10, -20]

_PST = {
    'w_pawn': _wp, 'w_knight': _wk, 'w_bishop': _wb,
    'w_rook': _wr, 'w_queen': _wq,
    'b_pawn': _bp, 'b_knight': _bk, 'b_bishop': _bb,
    'b_rook': _br, 'b_queen': _bq,
}

_BASE_VALUES = {
    'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 90
}


class Engine:

    @staticmethod
    def piece_value(piece, pos, style='traditional'):
        if piece == 'blank':
            return 0
        name = piece[2:]
        base = _BASE_VALUES.get(name, 0)

        if style == 'traditional' or name == 'king':
            return base

        file_num = ord(pos[0]) - 65
        rank = -(int(pos[1]) - 8)
        idx = rank * 8 + file_num

        try:
            return base + _PST[piece][idx] / 100.0
        except (KeyError, IndexError):
            return base - 1

    @staticmethod
    def calc_score(board, style='traditional'):
        score = 0
        for pos, piece in board.squares.items():
            if piece == 'blank':
                continue
            val = Engine.piece_value(piece, pos, style)
            if piece.startswith('w_'):
                score += val
            else:
                score -= val
        return score

    @staticmethod
    def random_move(color, board):
        valid_moves = board.get_valid_moves(color)
        if not valid_moves:
            print("Stalemate!")
            return None

        if board.king_in_check[color]:
            for m in valid_moves:
                if not board.still_in_check(color, m):
                    return board.auto_move(color, m)
            print("Checkmate!")
            return None

        random.shuffle(valid_moves)
        for m in valid_moves:
            result = board.auto_move(color, m)
            if result is not False:
                return result

        print("Stalemate!")
        return None

    @staticmethod
    def simple_move(color, board):
        # Opening book lookup
        curr_fen = board.to_fen()
        if curr_fen in opening_book:
            book = opening_book[curr_fen]
            move = random.choices(book['moves'], book['prob'])[0]
            return board.auto_move(color, move)

        valid_moves = board.get_valid_moves(color)
        if not valid_moves:
            print("Stalemate!")
            return None

        if board.king_in_check[color]:
            for m in valid_moves:
                if not board.still_in_check(color, m):
                    return board.auto_move(color, m)
            print("Checkmate!")
            return None

        # Score each move by simulating it on a board copy
        scored = []
        for m in valid_moves:
            sim = board.copy()
            sim.exec_move(color, m)
            scored.append((Engine.calc_score(sim, 'advanced'), m))

        scored.sort(key=lambda x: x[0], reverse=(color == 'White'))

        for _, m in scored:
            result = board.auto_move(color, m)
            if result is not False:
                return result

        print("Stalemate!")
        return None

    @staticmethod
    def minimax_move(color, board, depth):
        # TODO: implement alpha-beta minimax
        pass
