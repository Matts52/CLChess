
class Piece:
    def __init__(self, color):
        self.color = color
        self.pref = 'w_' if color == 'White' else 'b_'
        self.opp_pref = 'b_' if color == 'White' else 'w_'

    def _can_go(self, sq, board):
        return not board.squares[sq].startswith(self.pref)

    def _is_opp(self, sq, board):
        return board.squares[sq].startswith(self.opp_pref)

    def get_moves(self, pos, board, castle_check=False):
        raise NotImplementedError


class Pawn(Piece):
    def get_moves(self, pos, board, castle_check=False):
        moves = []
        file_num = ord(pos[0])
        rank = int(pos[1])
        d = 1 if self.color == 'White' else -1
        start_rank = 2 if self.color == 'White' else 7
        ep_rank = 5 if self.color == 'White' else 4

        # two-square advance from starting rank
        if rank == start_rank:
            mid = pos[0] + str(rank + d)
            dest = pos[0] + str(rank + 2 * d)
            if board.squares[mid] == 'blank' and board.squares[dest] == 'blank':
                moves.append(pos + dest)

        # one-square advance
        new_rank = rank + d
        if 1 <= new_rank <= 8:
            dest = pos[0] + str(new_rank)
            if board.squares[dest] == 'blank':
                moves.append(pos + dest)

            # diagonal captures
            for df in (-1, 1):
                nf = file_num + df
                if 65 <= nf <= 72:
                    dest = chr(nf) + str(new_rank)
                    if self._is_opp(dest, board):
                        moves.append(pos + dest)

        # en passant
        opp = 'Black' if self.color == 'White' else 'White'
        ep = board.en_pass_tracker[opp]
        if rank == ep_rank and ep:
            en_num = ord(ep)
            if abs(file_num - en_num) == 1:
                moves.append(pos + ep + str(rank + d) + 'P')

        return moves


class Knight(Piece):
    OFFSETS = [(1, 2), (1, -2), (-1, 2), (-1, -2),
               (2, 1), (2, -1), (-2, 1), (-2, -1)]

    def get_moves(self, pos, board, castle_check=False):
        moves = []
        file_num = ord(pos[0])
        rank = int(pos[1])
        for df, dr in self.OFFSETS:
            nf, nr = file_num + df, rank + dr
            if 65 <= nf <= 72 and 1 <= nr <= 8:
                dest = chr(nf) + str(nr)
                if self._can_go(dest, board):
                    moves.append(pos + dest)
        return moves


class _SlidingPiece(Piece):
    DIRECTIONS = ()

    def get_moves(self, pos, board, castle_check=False):
        moves = []
        file_num = ord(pos[0])
        rank = int(pos[1])
        for df, dr in self.DIRECTIONS:
            for i in range(1, 8):
                nf, nr = file_num + df * i, rank + dr * i
                if not (65 <= nf <= 72 and 1 <= nr <= 8):
                    break
                dest = chr(nf) + str(nr)
                if not self._can_go(dest, board):
                    break
                moves.append(pos + dest)
                if self._is_opp(dest, board):
                    break
        return moves


class Bishop(_SlidingPiece):
    DIRECTIONS = ((1, 1), (1, -1), (-1, 1), (-1, -1))


class Rook(_SlidingPiece):
    DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Queen(_SlidingPiece):
    DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1))


class King(Piece):
    def get_moves(self, pos, board, castle_check=False):
        moves = []
        file_num = ord(pos[0])
        rank = int(pos[1])

        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                nf, nr = file_num + df, rank + dr
                if 65 <= nf <= 72 and 1 <= nr <= 8:
                    dest = chr(nf) + str(nr)
                    if self._can_go(dest, board):
                        moves.append(pos + dest)

        if castle_check or board.king_in_check[self.color]:
            return moves

        color = self.color
        rank_ch = '1' if color == 'White' else '8'
        pref = self.pref
        king_sq = 'E' + rank_ch

        if board.king_movement[color] or board.squares[king_sq] != pref + 'king':
            return moves

        f_sq, g_sq = 'F' + rank_ch, 'G' + rank_ch
        if (not board.rook_movement[color][1] and
                board.squares[f_sq] == 'blank' and
                board.squares[g_sq] == 'blank' and
                not board.castle_cutoff_check(color, 'Short')):
            moves.append('O-O')

        b_sq, c_sq, d_sq = 'B' + rank_ch, 'C' + rank_ch, 'D' + rank_ch
        if (not board.rook_movement[color][0] and
                board.squares[b_sq] == 'blank' and
                board.squares[c_sq] == 'blank' and
                board.squares[d_sq] == 'blank' and
                not board.castle_cutoff_check(color, 'Long')):
            moves.append('O-O-O')

        return moves
