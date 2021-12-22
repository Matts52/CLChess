
from config import *

import move_chess as MC
import config as CF
import value_chess as VC

# -*- coding: utf-8 -*-



def init_chess_pieces():
    #init white piece characters
    chess_pieces['b_pawn'] = u"♙"
    chess_pieces['b_knight'] = u"♘"
    chess_pieces['b_rook'] = u"♖"
    chess_pieces['b_bishop'] = u"♗"
    chess_pieces['b_queen'] = u"♕"
    chess_pieces['b_king'] = u"♔"

    #init black piece characters
    chess_pieces['w_pawn'] = u"♟"
    chess_pieces['w_knight'] = u"♞"
    chess_pieces['w_rook'] = u"♜"
    chess_pieces['w_bishop'] = u"♝"
    chess_pieces['w_queen'] = u"♛"
    chess_pieces['w_king'] = u"♚"

    #init black square
    chess_pieces['blank'] = '·'

    return


def init_board():
    #init each square to a dot
    for i in numbers:
        for j in letters:
            board[j+i] = chess_pieces['blank']

    #init pawns to starting positions
    for j in ['A','B','C','D','E','F','G','H']:
        board[j+'2'] = chess_pieces['w_pawn']
        board[j+'7'] = chess_pieces['b_pawn']

    #init pieces to starting positions
    board['A1'] = chess_pieces['w_rook']
    board['H1'] = chess_pieces['w_rook']
    board['A8'] = chess_pieces['b_rook']
    board['H8'] = chess_pieces['b_rook']

    board['B1'] = chess_pieces['w_knight']
    board['G1'] = chess_pieces['w_knight']
    board['B8'] = chess_pieces['b_knight']
    board['G8'] = chess_pieces['b_knight']

    board['C1'] = chess_pieces['w_bishop']
    board['F1'] = chess_pieces['w_bishop']
    board['C8'] = chess_pieces['b_bishop']
    board['F8'] = chess_pieces['b_bishop']

    board['D1'] = chess_pieces['w_queen']
    board['E1'] = chess_pieces['w_king']
    board['D8'] = chess_pieces['b_queen']
    board['E8'] = chess_pieces['b_king']

    return



def print_board():
    counter = 0
    number_cnt = 1

    #print the eigth rank on the LHS
    print('\n'+numbers[0], end=' ')
    for key in board:
        print(board[key], end=' ')

        #check if we have reached edge of the board and still on a valid rank
        counter += 1
        if counter == 8 and number_cnt < 8:
            print('\n'+numbers[number_cnt], end=' ')
            number_cnt += 1
            counter = 0
        
    #print the files on the bottom
    print('\n',end='  ')
    for l in letters:
        print(l, end=' ')

    print('\n')
    print("Move: " + str(CF.total_moves))
    print("Score: " + str(VC.calc_score(board)))
    return



def read_move_file(moveFile):
    with open(moveFile, 'r') as f:
        lines = f.readlines()
        alt = 0
        for line in lines:
            parts = line.split()
            if alt == 0:
                if len(parts) == 1:
                    MC.auto_move("White", parts[0])
                else:
                    MC.auto_move("White", parts[0], parts[1])
                alt += 1
            else:
                if len(parts) == 1:
                    MC.auto_move("Black", parts[0])
                else:
                    MC.auto_move("Black", parts[0], parts[1])
                alt -= 1
            print_board()





def import_fen(fenStr):
    fenList = fenStr.split()
    fenP = fenList[0].split('/')

    pieces = []

    #build each rank out so its blanks are individually represented
    builder = ''
    for line in fenP:
        for item in line:
            if ord(item) < 57:
                for i in range(0, ord(item)-48):
                    builder = builder + 'z'
            else:
                builder = builder + item
        pieces.append(builder)
        builder = ''


    j = 0
    for i in range(0,8,1):
        while j < 8:
          
          #enter in pieces where they should go
          if pieces[i][j]=='p':board[letters[j]+numbers[i]]=chess_pieces['b_pawn']
          elif pieces[i][j]=='r':board[letters[j]+numbers[i]]=chess_pieces['b_rook']
          elif pieces[i][j]=='n':board[letters[j]+numbers[i]]=chess_pieces['b_knight']
          elif pieces[i][j]=='b':board[letters[j]+numbers[i]]=chess_pieces['b_bishop']
          elif pieces[i][j]=='q':board[letters[j]+numbers[i]]=chess_pieces['b_queen']
          elif pieces[i][j]=='k':board[letters[j]+numbers[i]]=chess_pieces['b_king']
          elif pieces[i][j]=='P':board[letters[j]+numbers[i]]=chess_pieces['w_pawn']
          elif pieces[i][j]=='R':board[letters[j]+numbers[i]]=chess_pieces['w_rook']
          elif pieces[i][j]=='N':board[letters[j]+numbers[i]]=chess_pieces['w_knight']
          elif pieces[i][j]=='B':board[letters[j]+numbers[i]]=chess_pieces['w_bishop']
          elif pieces[i][j]=='Q':board[letters[j]+numbers[i]]=chess_pieces['w_queen']
          elif pieces[i][j]=='K':board[letters[j]+numbers[i]]=chess_pieces['w_king']
          elif pieces[i][j]=='z':board[letters[j]+numbers[i]]=chess_pieces['blank'] 

          j += 1
        j = 0


    #add in en passent attack square tracker
    if fenList[3] != '-':
        if fenList[3][1] == '3':
            en_pass_tracker['White'] = fenList[3][0].upper()
        else:
            en_pass_tracker['Black'] = fenList[3][0].upper()



    #add in castling rights, assume movement unless denoted otherwise
    king_movement['White'] = True
    king_movement['Black'] = True
    rook_movement['White'] = [True,True]
    rook_movement['Black'] = [True,True]

    if fenList[2] != '-':
        for l in fenList[2]:
            if l == 'K':
                king_movement['White'] = False
                rook_movement['White'][1] = False
            elif l == 'Q':
                king_movement['White'] = False
                rook_movement['White'][0] = False
            elif l == 'k':
                king_movement['Black'] = False
                rook_movement['Black'][1] = False
            elif l == 'q':
                king_movement['Black'] = False
                rook_movement['Black'][0] = False
    


    #return whos move it is
    if fenList[1] == 'w': return 0
    else: return 1



def convert_to_FEN():
	
	fen_str = ''
	
	for key in board:
		#add symbols in for the positions of each piece
		if board[key] == chess_pieces['w_pawn']: fen_str = fen_str + 'P'
		elif board[key] == chess_pieces['w_knight']: fen_str = fen_str + 'N'
		elif board[key] == chess_pieces['w_bishop']: fen_str = fen_str + 'B'
		elif board[key] == chess_pieces['w_rook']: fen_str = fen_str + 'R'
		elif board[key] == chess_pieces['w_queen']: fen_str = fen_str + 'Q'
		elif board[key] == chess_pieces['w_king']: fen_str = fen_str + 'K'
		elif board[key] == chess_pieces['b_pawn']: fen_str = fen_str + 'p'
		elif board[key] == chess_pieces['b_knight']: fen_str = fen_str + 'n'
		elif board[key] == chess_pieces['b_bishop']: fen_str = fen_str + 'b'
		elif board[key] == chess_pieces['b_rook']: fen_str = fen_str + 'r'
		elif board[key] == chess_pieces['b_queen']: fen_str = fen_str + 'q'
		elif board[key] == chess_pieces['b_king']: fen_str = fen_str + 'k'
		elif board[key] == chess_pieces['blank']: fen_str = fen_str + 'z'
		
		if key[0] == 'H': fen_str = fen_str + '/'
	
	#replace blanks with number of blanks
	fen_str = fen_str.replace('zzzzzzzz', '8')
	fen_str = fen_str.replace('zzzzzzz', '7')
	fen_str = fen_str.replace('zzzzzz', '6')
	fen_str = fen_str.replace('zzzzz', '5')
	fen_str = fen_str.replace('zzzz', '4')
	fen_str = fen_str.replace('zzz', '3')
	fen_str = fen_str.replace('zz', '2')
	fen_str = fen_str.replace('z', '1')
	
	#cut off final slash
	return fen_str[0:-1]
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	



