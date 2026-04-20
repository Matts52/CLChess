
from pieces import Pawn, Knight, Bishop, Rook, Queen, King

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
NUMBERS = ['8', '7', '6', '5', '4', '3', '2', '1']

PIECE_SYMBOLS = {
    'w_pawn': '♟', 'w_knight': '♞', 'w_rook': '♜',
    'w_bishop': '♝', 'w_queen': '♛', 'w_king': '♚',
    'b_pawn': '♙', 'b_knight': '♘', 'b_rook': '♖',
    'b_bishop': '♗', 'b_queen': '♕', 'b_king': '♔',
    'blank': '·'
}

_FEN_TO_PIECE = {
    'p': 'b_pawn', 'r': 'b_rook', 'n': 'b_knight', 'b': 'b_bishop',
    'q': 'b_queen', 'k': 'b_king',
    'P': 'w_pawn', 'R': 'w_rook', 'N': 'w_knight', 'B': 'w_bishop',
    'Q': 'w_queen', 'K': 'w_king',
}
_PIECE_TO_FEN = {v: k for k, v in _FEN_TO_PIECE.items()}
_PIECE_TO_FEN['blank'] = 'z'

_BACK_RANK = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']

_PIECE_CLASSES = {
    'pawn': Pawn, 'knight': Knight, 'bishop': Bishop,
    'rook': Rook, 'queen': Queen, 'king': King,
}


class Board:
    def __init__(self):
        self.squares = {l + n: 'blank' for n in NUMBERS for l in LETTERS}
        self.king_in_check = {'White': False, 'Black': False}
        self.en_pass_tracker = {'White': '', 'Black': ''}
        self.king_movement = {'White': False, 'Black': False}
        self.rook_movement = {'White': [False, False], 'Black': [False, False]}
        self.total_moves = 1

    def copy(self):
        b = Board()
        b.squares = self.squares.copy()
        b.king_in_check = self.king_in_check.copy()
        b.en_pass_tracker = self.en_pass_tracker.copy()
        b.king_movement = self.king_movement.copy()
        b.rook_movement = {
            'White': self.rook_movement['White'][:],
            'Black': self.rook_movement['Black'][:]
        }
        b.total_moves = self.total_moves
        return b

    def init_board(self):
        for sq in self.squares:
            self.squares[sq] = 'blank'
        for l in LETTERS:
            self.squares[l + '2'] = 'w_pawn'
            self.squares[l + '7'] = 'b_pawn'
        for i, l in enumerate(LETTERS):
            self.squares[l + '1'] = 'w_' + _BACK_RANK[i]
            self.squares[l + '8'] = 'b_' + _BACK_RANK[i]

    @classmethod
    def from_fen(cls, fen_str):
        board = cls()
        parts = fen_str.split()
        ranks = parts[0].split('/')

        for rank_idx, rank_str in enumerate(ranks):
            file_idx = 0
            for ch in rank_str:
                if ch.isdigit():
                    for _ in range(int(ch)):
                        board.squares[LETTERS[file_idx] + NUMBERS[rank_idx]] = 'blank'
                        file_idx += 1
                else:
                    board.squares[LETTERS[file_idx] + NUMBERS[rank_idx]] = _FEN_TO_PIECE[ch]
                    file_idx += 1

        if len(parts) > 3 and parts[3] != '-':
            key = 'White' if parts[3][1] == '3' else 'Black'
            board.en_pass_tracker[key] = parts[3][0].upper()

        board.king_movement = {'White': True, 'Black': True}
        board.rook_movement = {'White': [True, True], 'Black': [True, True]}
        if len(parts) > 2 and parts[2] != '-':
            for ch in parts[2]:
                if ch == 'K':
                    board.king_movement['White'] = False
                    board.rook_movement['White'][1] = False
                elif ch == 'Q':
                    board.king_movement['White'] = False
                    board.rook_movement['White'][0] = False
                elif ch == 'k':
                    board.king_movement['Black'] = False
                    board.rook_movement['Black'][1] = False
                elif ch == 'q':
                    board.king_movement['Black'] = False
                    board.rook_movement['Black'][0] = False

        turn = 0 if (len(parts) < 2 or parts[1] == 'w') else 1
        return board, turn

    def to_fen(self):
        fen = ''
        for n in NUMBERS:
            for l in LETTERS:
                fen += _PIECE_TO_FEN[self.squares[l + n]]
            if n != '1':
                fen += '/'
        for count in range(8, 0, -1):
            fen = fen.replace('z' * count, str(count))
        return fen

    def print_board(self):
        from engine import Engine
        print()
        for n in NUMBERS:
            print(n, end=' ')
            for l in LETTERS:
                print(PIECE_SYMBOLS[self.squares[l + n]], end=' ')
            print()
        print('\n  ', end='')
        for l in LETTERS:
            print(l, end=' ')
        print(f'\n\nMove: {self.total_moves}')
        print(f'Score: {Engine.calc_score(self)}')

    def read_move_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
        alt = 0
        for line in lines:
            parts = line.split()
            if not parts:
                continue
            color = 'White' if alt == 0 else 'Black'
            prom = parts[1] if len(parts) > 1 else None
            self.auto_move(color, parts[0], prom)
            self.print_board()
            alt = 1 - alt
        return alt

    # --- move generation ---

    def get_valid_moves(self, color, castle_check=False):
        pref = 'w_' if color == 'White' else 'b_'
        moveset = []
        for pos, piece in self.squares.items():
            if not piece.startswith(pref):
                continue
            piece_name = piece[2:]
            cls = _PIECE_CLASSES.get(piece_name)
            if cls:
                moveset.extend(cls(color).get_moves(pos, self, castle_check=castle_check))
        return moveset

    def still_in_check(self, color, move):
        pref = 'w_' if color == 'White' else 'b_'
        king_pos = next(pos for pos, p in self.squares.items() if p == pref + 'king')
        if king_pos == move[0:2]:
            king_pos = move[2:4]

        piece1, piece2 = self.squares[move[0:2]], self.squares[move[2:4]]
        self.squares[move[0:2]] = 'blank'
        self.squares[move[2:4]] = piece1

        opp = 'Black' if color == 'White' else 'White'
        in_check = any(m[2:4] == king_pos for m in self.get_valid_moves(opp))

        self.squares[move[0:2]] = piece1
        self.squares[move[2:4]] = piece2
        return in_check

    def disc_king_in_check(self, color, move):
        pref = 'w_' if color == 'White' else 'b_'
        king_pos = next(pos for pos, p in self.squares.items() if p == pref + 'king')
        if king_pos == move[0:2]:
            king_pos = move[2:4]

        piece, piece2 = self.squares[move[0:2]], self.squares[move[2:4]]
        self.squares[move[0:2]] = 'blank'
        self.squares[move[2:4]] = piece

        opp = 'Black' if color == 'White' else 'White'
        in_check = any(m[2:4] == king_pos for m in self.get_valid_moves(opp))

        self.squares[move[0:2]] = piece
        self.squares[move[2:4]] = piece2
        return in_check

    def castle_cutoff_check(self, color, side):
        target = {
            ('White', 'Short'): ['F1', 'G1'], ('White', 'Long'): ['C1', 'D1'],
            ('Black', 'Short'): ['F8', 'G8'], ('Black', 'Long'): ['C8', 'D8'],
        }[(color, side)]
        opp = 'Black' if color == 'White' else 'White'
        return any(m[2:4] in target for m in self.get_valid_moves(opp, castle_check=True))

    def report_king_in_check(self, color):
        opp = 'Black' if color == 'White' else 'White'
        opp_pref = 'b_' if color == 'White' else 'w_'
        king_pos = next((pos for pos, p in self.squares.items() if p == opp_pref + 'king'), None)
        if king_pos and any(m[2:4] == king_pos for m in self.get_valid_moves(color)):
            self.king_in_check[opp] = True

    # --- move execution ---

    def exec_move(self, color, move):
        rank = '1' if color == 'White' else '8'
        pref = 'w_' if color == 'White' else 'b_'

        if move == 'O-O':
            self.king_movement[color] = True
            self.squares['E' + rank] = 'blank'
            self.squares['F' + rank] = pref + 'rook'
            self.squares['G' + rank] = pref + 'king'
            self.squares['H' + rank] = 'blank'
            return

        if move == 'O-O-O':
            self.king_movement[color] = True
            self.squares['A' + rank] = 'blank'
            self.squares['B' + rank] = 'blank'
            self.squares['C' + rank] = pref + 'king'
            self.squares['D' + rank] = pref + 'rook'
            self.squares['E' + rank] = 'blank'
            return

        piece = self.squares[move[0:2]]
        self.squares[move[2:4]] = piece
        self.squares[move[0:2]] = 'blank'

        if piece in ('w_pawn', 'b_pawn') and abs(int(move[1]) - int(move[3])) == 2:
            self.en_pass_tracker[color] = move[0]

        try:
            if move[4] == 'P':
                ep_rank = '5' if color == 'White' else '4'
                self.squares[move[2] + ep_rank] = 'blank'
        except IndexError:
            pass

        _castling = {'A1': ('White', 0), 'H1': ('White', 1),
                     'A8': ('Black', 0), 'H8': ('Black', 1)}
        if move[0:2] in _castling:
            c, i = _castling[move[0:2]]
            self.rook_movement[c][i] = True
        elif move[0:2] == 'E1':
            self.king_movement['White'] = True
        elif move[0:2] == 'E8':
            self.king_movement['Black'] = True

    def scan_promote(self, color, piece=None):
        rank = '8' if color == 'White' else '1'
        pref = 'w_' if color == 'White' else 'b_'
        for l in LETTERS:
            sq = l + rank
            if self.squares[sq] == pref + 'pawn':
                if piece is not None:
                    self.squares[sq] = pref + piece
                    return
                while True:
                    choice = input("Enter Promotion Piece (Queen/Knight/Bishop/Rook): ")
                    if choice in ('Queen', 'Knight', 'Bishop', 'Rook'):
                        self.squares[sq] = pref + choice.lower()
                        return
                    print("Please enter a valid promotion piece")

    def check_insuf_mat(self):
        counts = {c: {'pawn': 0, 'knight': 0, 'bishop': 0, 'rook': 0, 'queen': 0}
                  for c in ('White', 'Black')}
        for piece in self.squares.values():
            if piece == 'blank':
                continue
            color = 'White' if piece.startswith('w_') else 'Black'
            name = piece[2:]
            if name in counts[color]:
                counts[color][name] += 1
        for c in ('White', 'Black'):
            if counts[c]['pawn'] or counts[c]['rook'] or counts[c]['queen']:
                return False
            if counts[c]['knight'] + counts[c]['bishop'] >= 2:
                return False
        return True

    # --- high-level move interface ---

    def auto_move(self, color, move, auto_prom=None):
        """Execute a move programmatically (used by AI). Returns True on success,
        False if the move leaves the king in check, None on game over."""
        valid_moves = self.get_valid_moves(color)
        if not valid_moves:
            print("Stalemate!")
            return None

        self.en_pass_tracker[color] = ''

        if self.king_in_check[color]:
            if self.still_in_check(color, move):
                return False
            self.king_in_check[color] = False

        if move not in ('O-O', 'O-O-O') and self.disc_king_in_check(color, move):
            return False

        self.exec_move(color, move)
        self.scan_promote(color, auto_prom or 'queen')
        self.total_moves += 1
        self.report_king_in_check(color)

        if self.check_insuf_mat():
            self.print_board()
            print("Draw by insufficient material!")
            return None

        return True

    def get_move(self, color):
        """Prompt the human player for a move. Returns True on success, None on game over."""
        valid_moves = self.get_valid_moves(color)
        if not valid_moves:
            print("Stalemate!")
            return None

        self.en_pass_tracker[color] = ''

        if self.king_in_check[color]:
            if not any(not self.still_in_check(color, m) for m in valid_moves):
                print("Checkmate!")
                return None

        while True:
            entered = input(f"Enter {color} Move: ").upper()
            if entered == 'resign':
                print(f"{color} Resigns!")
                return None
            if entered not in valid_moves:
                print("Please enter a valid move")
                continue
            if self.king_in_check[color] and self.still_in_check(color, entered):
                print("You must remove the check on your king")
                continue
            if entered not in ('O-O', 'O-O-O') and self.disc_king_in_check(color, entered):
                print("This move puts the king in check")
                continue
            break

        self.king_in_check[color] = False
        self.exec_move(color, entered)
        self.scan_promote(color)
        self.total_moves += 1
        self.report_king_in_check(color)

        if self.check_insuf_mat():
            self.print_board()
            print("Draw by insufficient material!")
            return None

        return True
