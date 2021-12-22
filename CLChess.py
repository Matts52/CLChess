
import sys

from config import *
import init_chess as IC
import value_chess as VC
import move_chess as MC
import AI_chess as AI


# -*- coding: utf-8 -*-

'''
Todo:
    50 move rule
    3 repetition draw
    furthered piece value calculation
    move tracking
    Better code structure
    AI to play against
'''


#init pieces
IC.init_chess_pieces()



turn = 0
fenRead = False
autoMoves = False

# read move files
if len(sys.argv) > 1:
    if sys.argv[1][-4:] == '.txt':
    	IC.init_board()
    	turn = IC.read_move_file(sys.argv[1])
    	autoMoves = True
    elif sys.argv[1] == '-':
        IC.init_board()
        IC.print_board()
    else:
        turn = IC.import_fen(sys.argv[1])
        IC.print_board()
        fenRead = True



#if we have not read a fen and not read automoves, init the board
if not fenRead and not autoMoves:
    IC.init_board()
    IC.init_board()
    IC.print_board()



# if we are currently on blacks move, allow it to move before the loop
if turn == 1:
	#we are playing the random bot
	if len(sys.argv) > 3:
		if sys.argv[2] == "rand":
			if sys.argv[3] == 'White':
				AI.random_AI_Move('Black')
				IC.print_board()
			else:
				MC.get_move('Black')
				IC.print_board()
		elif sys.argv[2] == 'simple':
			if sys.argv[3] == 'White':
				AI.simple_AI_move('Black')
				IC.print_board()
			else:
				MC.get_move('Black')
				IC.print_board()
    #else we are playing human controlled game
	else:
		MC.get_move('Black')
		IC.print_board()




#play the game

#playing vs simple bot
if len(sys.argv) > 3 and sys.argv[2] == "simple":
	if sys.argv[3] == 'simple':
		for i in range(0,4):
			AI.simple_AI_move("White")
			IC.print_board()
			AI.simple_AI_move("Black")
			IC.print_board()
	
	elif sys.argv[3] == 'White':
		while(1):
			MC.get_move('White')
			IC.print_board()
			AI.simple_AI_move('Black')
			IC.print_board()
	else:
		while(1):
			AI.simple_AI_move('White')
			IC.print_board()
			MC.get_move('Black')
			IC.print_board()


#playing vs random bot
if len(sys.argv) > 3 and sys.argv[2] == "rand":
	if sys.argv[3] == 'rand':
		while(1):
			AI.random_AI_move("White")
			IC.print_board()
			AI.random_AI_move("Black")
			IC.print_board()
	
	elif sys.argv[3] == 'White':
		while(1):
			MC.get_move('White')
			IC.print_board()
			AI.random_AI_move('Black')
			IC.print_board()
	else:
		while(1):
			AI.random_AI_move('White')
			IC.print_board()
			MC.get_move('Black')
			IC.print_board()


#playing human vs human
while(1):
	MC.get_move('White')
	IC.print_board()
	MC.get_move('Black')
	IC.print_board()




