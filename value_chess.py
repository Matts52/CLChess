

from config import *


# Position Evaluation Matrices

wp =  [900,  900,  900,  900,  900,  900,  900,  900,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
 5,  5, 10, 25, 25, 10,  5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5, -5,-10,  0,  0,-10, -5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

wk = [-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

wb = [-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

wr = [  0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0,  5,  5,  0,  0,  0]
  
wq = [-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]


bp = [0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
  0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
 50, 50, 50, 50, 50, 50, 50, 50,
 900,  900,  900,  900,  900,  900,  900,  900]

bk = [-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30, 5, 15,20, 20, 15,  -5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  -5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bb = [-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10,10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

br = [  0,  0,  0,  5, 5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, -0, 10, 10, 10, 10, 10,  5,
  0,  0,  0,  0,  0,  0,  0,  0]
  
bq = [-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]



def piece_values(piece, position, style='traditional'):


    if style == 'traditional':    
        if piece[2:] == 'pawn':
            return 1
        elif piece[2:] == 'knight':
            return 3
        elif piece[2:] == 'bishop':
            return 3
        elif piece[2:] == 'rook':
            return 5
        elif piece[2:] == 'queen':
            return 9
        elif piece[2:] == 'king':
            return 90

    file_num = ord(position[0]) - 65
    rank = -(int(position[1]) - 8)

    # bug occurs where list index is out of range sometimes, todo fix this
    try:
        if style == 'advanced':
        	#return a value which is the piece value plus any value it has for its current position
            if piece == 'w_pawn':
	            return 1 + wp[(rank*8)+file_num]/100.0
            elif piece == 'w_knight':
                return 3 + wk[(rank*8)+file_num]/100.0
            elif piece == 'w_bishop':
                return 3 + wb[(rank*8)+file_num]/100.0
            elif piece == 'w_rook':
                return 5 + wr[(rank*8)+file_num]/100.0
            elif piece == 'w_queen':
        	    return 9 + wq[(rank*8)+file_num]/100.0
            elif piece == 'w_king':
                return 90
            elif piece == 'b_pawn':
                return 1 + bp[(rank*8)+file_num]/100.0
            elif piece == 'b_knight':
                return 3 + bk[(rank*8)+file_num]/100.0
            elif piece == 'b_bishop':
                return 3 + bb[(rank*8)+file_num]/100.0
            elif piece == 'b_rook':
                return 5 + br[(rank*8)+file_num]/100.0
            elif piece == 'b_queen':
                return 9 + bq[(rank*8)+file_num]/100.0
            elif piece == 'b_king':
                return 90
    except:
        return piece_values(piece, position, 'traditional') - 1


    return 0



def calc_score(inBoard, style='traditional'):

    score = 0

    for key in board:
        if inBoard[key] == chess_pieces['w_pawn']: score += piece_values('w_pawn', key, style)
        elif inBoard[key] == chess_pieces['w_knight']: score += piece_values('w_knight', key, style)
        elif inBoard[key] == chess_pieces['w_bishop']: score += piece_values('w_bishop', key, style)
        elif inBoard[key] == chess_pieces['w_rook']: score += piece_values('w_rook', key, style)
        elif inBoard[key] == chess_pieces['w_queen']: score += piece_values('w_queen', key, style)
        elif inBoard[key] == chess_pieces['w_king']: score += piece_values('w_king', key, style)
        elif inBoard[key] == chess_pieces['b_pawn']: score -= piece_values('b_pawn', key, style)
        elif inBoard[key] == chess_pieces['b_knight']: score -= piece_values('b_knight', key, style)
        elif inBoard[key] == chess_pieces['b_bishop']: score -= piece_values('b_bishop', key, style)
        elif inBoard[key] == chess_pieces['b_rook']: score -= piece_values('b_rook', key, style)
        elif inBoard[key] == chess_pieces['b_queen']: score -= piece_values('b_queen', key, style)
        elif inBoard[key] == chess_pieces['b_king']: score -= piece_values('b_king', key, style)

    return score




def check_insuf_mat():

	Wpieces = [0,0,0,0,0]
	Bpieces = [0,0,0,0,0]

	for key in board:
		if board[key] == chess_pieces['w_pawn']: Wpieces[0] += 1
		elif board[key] == chess_pieces['w_knight']: Wpieces[1] += 1
		elif board[key] == chess_pieces['w_bishop']: Wpieces[2] += 1
		elif board[key] == chess_pieces['w_rook']: Wpieces[3] += 1
		elif board[key] == chess_pieces['w_queen']: Wpieces[4] += 1
		elif board[key] == chess_pieces['b_pawn']: Bpieces[0] += 1
		elif board[key] == chess_pieces['b_knight']: Bpieces[1] += 1
		elif board[key] == chess_pieces['b_bishop']: Bpieces[2] += 1
		elif board[key] == chess_pieces['b_rook']: Bpieces[3] += 1
		elif board[key] == chess_pieces['b_queen']: Bpieces[4] += 1

	
	print(Wpieces)
	
	if Wpieces[0] == 0 and Wpieces[3] == 0 and Wpieces[4] == 0 \
		and Bpieces[0] == 0 and Bpieces[3] == 0 and Bpieces[4] == 0 \
		and (Wpieces[1] + Wpieces[2] < 2) and (Bpieces[1] + Bpieces[2] < 2):
			return True
		
		
	return False






