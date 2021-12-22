
import random

import move_chess as MC
import value_chess as VC
import init_chess as IC

from config import *
from open_book import opening_book


def random_AI_move(color):
	valid_moves = MC.get_valid_moves(color)
			
	#check if a checkmate has occured
	if king_in_check[color]:
		for m in valid_moves:
			#play the first move which gets rid of the check
			if not MC.still_in_check(color, m):
				MC.auto_move(color, m)
				return
		print("Checkmate!")
		exit()
		
	
	# keep choosing random moves until one gets played
	move = random.choice(valid_moves)
	while(1):
		if MC.auto_move(color, move) == False:
			valid_moves.remove(move)
		
			if valid_moves == []:
				print("Stalemate")
				exit()
			
			move = random.choice(valid_moves)
			continue
		else:
			break
	
	return





def simple_AI_move(color):
	valid_moves = MC.get_valid_moves(color)
	
	
	#check if the current board position is in the opening book
	curr_fen = IC.convert_to_FEN()
	
	if curr_fen in opening_book.keys():
		#play an opening book move
		book_moves = opening_book[curr_fen]['moves']
		book_probs = opening_book[curr_fen]['prob']
		move = random.choices(book_moves, book_probs)[0]
		MC.auto_move(color, move)
	
		return 
	
	
	
	#keep track of the best move(s)
	if color == 'White': top_score = -10000 
	else: top_score = 10000
	
	candidate_moves = []
	in_check_moves = []
	
	# keep a hard copy of the board state
	boardSave = board.copy()
	
	#check if a checkmate has occured
	if king_in_check[color]:
		for m in valid_moves:
			#play the first move which gets rid of the check
			if not MC.still_in_check(color, m):
				MC.auto_move(color, m)
				return
		print("Checkmate!")
		exit()
	
	
	# get the top possible move based on next board state
	for m in valid_moves:
		test_score = test_move(color, boardSave, m)
		
		if (color =='White' and test_score > top_score) or (color == 'Black' and test_score < top_score):
			top_score = test_score
			candidate_moves.insert(0, m)
		else:
			candidate_moves.append(m)
		#reset the temporary board
		boardSave = board.copy()



	while(1):
		#get the top candidate move
		move = candidate_moves.pop(0)
		
		if MC.auto_move(color, move) == False:
		
			if candidate_moves == []:
				print("Stalemate")
				exit()
			
			continue
		else:
			break
	
	return







def test_move(color, curr_board, move):

	#make the move
	if move not in ['O-O', 'O-O-O']:
		piece1 = curr_board[move[0:2]]
		curr_board[move[0:2]] = chess_pieces['blank']
		curr_board[move[2:4]] = piece1
		
		#check for if en passent has been performed
		try:
			if move[4] == 'P':
				if color == 'White':
					board[move[2]+'5'] = chess_pieces['blank']
			else:
				board[move[2]+'4'] = chess_pieces['blank']
		except:
			pass
		
	else:
		if move == 'O-O':
			if color == 'White':
				curr_board['E1'] = chess_pieces['blank']
				curr_board['F1'] = chess_pieces['w_rook']
				curr_board['G1'] = chess_pieces['w_king']
				curr_board['H1'] = chess_pieces['blank']
			else:
				curr_board['E8'] = chess_pieces['blank']
				curr_board['F8'] = chess_pieces['b_rook']
				curr_board['G8'] = chess_pieces['b_king']
				curr_board['H8'] = chess_pieces['blank']
		elif move == 'O-O-O':
			if color == 'White':
				curr_board['E1'] = chess_pieces['blank']
				curr_board['D1'] = chess_pieces['w_rook']
				curr_board['C1'] = chess_pieces['w_king']
				curr_board['B1'] = chess_pieces['blank']
				curr_board['A1'] = chess_pieces['blank']
			else:
				curr_board['E8'] = chess_pieces['blank']
				curr_board['D8'] = chess_pieces['b_rook']
				curr_board['C8'] = chess_pieces['b_king']
				curr_board['B8'] = chess_pieces['blank']
				curr_board['A8'] = chess_pieces['blank']
	
	
	
	return VC.calc_score(curr_board, 'advanced')




def minimax_AI_move(color, depth):
	pass







def minimax():
	pass











