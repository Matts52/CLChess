

from config import *

import config as CF
import value_chess as VC
import init_chess as IC


def auto_move(color, auto, autoProm=None):
	valid_moves = get_valid_moves(color)


	if valid_moves == []:
		print("Stalemate!")
		exit()

	print(en_pass_tracker)

	en_pass_tracker[color] = ''


    #check if auto move was valid

    #check if a check threat has been removed
	if king_in_check[color]:
		if still_in_check(color, auto):
			return False
		king_in_check[color] = False
                    

    #prevent a piece from performing a discovered check on its own king
	if auto not in ['O-O', 'O-O-O'] and disc_king_in_check(color, auto):
		return False 
		 	
 
 	# execute the move and scan for promotion, autopromote to queen
 	#for now for simplicity
	exec_move(color, auto)
	scan_promote(color, 'queen')

	CF.total_moves += 1

	report_king_in_check(color)

	if VC.check_insuf_mat():
		IC.print_board()
		print("Draw by insufficient material!")
		exit()

	return True



def get_move(color):

    valid_moves = get_valid_moves(color)


    if valid_moves == []:
        print("Stalemate!")
        exit()

    print(valid_moves)

    print(en_pass_tracker)

    en_pass_tracker[color] = ''

    #check if a checkmate has occured
    if king_in_check[color]:
        way_out = False
        for m in valid_moves:
            if not still_in_check(color, m):
                print(m)
                way_out = True
                break
        if way_out == False:
            print("Checkmate!")
            exit()


    while(1):
        entered = input("Enter "+color+" Move: ")
        if entered in valid_moves:

            #check if the check threat has been removed
            if king_in_check[color]:
                if still_in_check(color, entered):
                    print("You must remove the check on your king")
                    continue
                king_in_check[color] = False
                break

            #prevent a piece from performing a discovered check on its own king
            if entered not in ['O-O', 'O-O-O'] and \
                    disc_king_in_check(color, entered):
                print("This move puts the king in check")
                continue    

            break           

        elif entered == 'resign':
            print(color+" Resigns!")
            exit()
        else:
            print("Please enter a valid move")

    exec_move(color, entered)
    scan_promote(color)

    CF.total_moves += 1

    report_king_in_check(color)

    if VC.check_insuf_mat():
        IC.print_board()
        print("Draw by insufficient material!")
        exit()

    return



def report_king_in_check(color):
    
    if color=='Black': pref='w_'
    else: pref='b_'

    pos = ''

    #scan the board for the opposing king
    for key in board:
        if board[key] == chess_pieces[pref+'king']:
            pos = key

    if pos == '':
    	print("What the Heck!")

    #get the next possible moves for the same colors
    if color=='White': next_moves = get_valid_moves('White')
    else: next_moves = get_valid_moves('Black')


    #if a next move can attack the king, this is an illegal move
    for m in next_moves:
        if m[2:4] == pos:
            if color == 'White': king_in_check['Black'] = True
            else: king_in_check['White'] = True

    return




def still_in_check(color, move):

    if color=='White': pref='w_'
    else: pref='b_'

    #scan the board for the king
    for key in board:
        if board[key] == chess_pieces[pref+'king']:
            pos = key
            #if it was the king that moved, check its new location
            if pos == move[0:2]:
                pos = move[2:4]


    #remember where the pieces were
    piece1 = board[move[0:2]]
    piece2 = board[move[2:4]]

    board[move[0:2]] = chess_pieces['blank']
    board[move[2:4]] = piece1

    #get the next possible moves for the opposite colors
    if color=='White': next_moves = get_valid_moves('Black')
    else: next_moves = get_valid_moves('White')


    board[move[0:2]] = piece1
    board[move[2:4]] = piece2

    #if a next move can attack the king, the king is still in check
    for m in next_moves:
        if m[2:4] == pos:
            return True

    return False





def disc_king_in_check(color, move):

    if color=='White': pref='w_'
    else: pref='b_'

    #scan the board for the king
    for key in board:
        if board[key] == chess_pieces[pref+'king']:
            pos = key
            #if it was the king that moved, check its new location
            if pos == move[0:2]:
                pos = move[2:4]


    #get the piece that is moving
    piece = board[move[0:2]]    
    piece2 = board[move[2:4]]

    #temporarily see what would happen if the piece was not in that square
    board[move[0:2]] = chess_pieces['blank']
    board[move[2:4]] = piece

    #get the next possible moves for the opposite colors
    if color=='White': next_moves = get_valid_moves('Black')
    else: next_moves = get_valid_moves('White')

    #replace the pieces that were in the squares
    board[move[0:2]] = piece
    board[move[2:4]] = piece2

    #if a next move can lead to an attack on the king, this is an illegal move
    for m in next_moves :
        if m[2:4] == pos:
            return True

    return False



def scan_promote(color, piece=None):

    if color == 'White':
        prom = '8'
        promP = 'w_'
    else:
        prom = '1'
        promP = 'b_'


    # scan for pawn promotion
    for i in letters:
        if board[i+prom] == chess_pieces[promP+'pawn']:
            while(1):
                #if reading from an automated game, choose the automated choice
                if piece is not None:
                    board[i+prom] = chess_pieces[promP+piece]
                    break

                #prompt user for promotion piece
                promotePiece = input("Enter Promotion Piece: ")
                if promotePiece == "Queen":
                    board[i+prom] = chess_pieces[promP+'queen']
                    break
                elif promotePiece == "Knight":
                    board[i+prom] = chess_pieces[promP+'knight']
                    break
                elif promotePiece == "Bishop":
                    board[i+prom] = chess_pieces[promP+'bishop']
                    break
                elif promotePiece == "Rook":
                    board[i+prom] = chess_pieces[promP+'rook']
                    break
                print("Please enter a valid promotion piece")

    return





def get_valid_moves(color, castleCheck=False):
    rank = 0
    file_num = 0
    moveset = []

    if color == 'White':
        #pieces owned by white
        my_pieces = [chess_pieces['w_pawn'],chess_pieces['w_knight'],
            chess_pieces['w_bishop'],chess_pieces['w_queen'],chess_pieces['w_king'],
            chess_pieces['w_rook']]

        #takeable pieces
        oth_pieces = [chess_pieces['b_pawn'],chess_pieces['b_knight'],
            chess_pieces['b_bishop'],chess_pieces['b_queen'], chess_pieces['b_king'],
            chess_pieces['b_rook']]

        pref = 'w_'
    else:
        my_pieces = [chess_pieces['b_pawn'],chess_pieces['b_knight'],
            chess_pieces['b_bishop'],chess_pieces['b_queen'], chess_pieces['b_king'],
            chess_pieces['b_rook']]

        oth_pieces = [chess_pieces['w_pawn'],chess_pieces['w_knight'],
            chess_pieces['w_bishop'],chess_pieces['w_queen'], chess_pieces['w_king'],
            chess_pieces['w_rook']]

        pref = 'b_'



    for key in board:
        
        #get pawn moves
        if board[key] == chess_pieces[pref+'pawn']:
            rank = int(key[1])
            #first move pawn movement
            if (rank == 2 and color == 'White') or (rank==7 and color=='Black'):
                if color == 'White': rank+=2
                else: rank-=2

                if board[key[0]+str(rank)] not in my_pieces and \
                        board[key[0]+str(rank)] not in oth_pieces and \
                        board[key[0]+str(rank-1)] not in my_pieces:
                    moveset.append(key+key[0]+str(rank))
            

                rank = int(key[1])

            #typical pawn movement
            if color == 'White': rank += 1
            else: rank-=1

            if rank > 0 and rank < 9:
                if board[key[0]+str(rank)] not in my_pieces and \
                        board[key[0]+str(rank)] not in oth_pieces:
                    moveset.append(key+key[0]+str(rank))

            #pawn attack
            file_num = ord(key[0])
            if file_num - 1 > 64 and rank <9 and rank > 0:
                if board[chr(file_num-1)+str(rank)] in oth_pieces:
                    moveset.append(key+chr(file_num-1)+str(rank))
            if file_num + 1 < 73 and rank <9  and rank > 0:
                if board[chr(file_num+1)+str(rank)] in oth_pieces:
                    moveset.append(key+chr(file_num+1)+str(rank))

            #en passent movement
            if rank > 0  and rank < 9:
                if color == 'White':
                    if en_pass_tracker['Black'] != '':
                        en_num = ord(en_pass_tracker['Black'])
                        if (file_num - en_num == 1 or file_num - en_num == -1) and \
                            int(key[1]) == 5:
                                moveset.append(key+chr(en_num)+str(rank)+'P')
                else:
                    if en_pass_tracker['White'] != '':
                        en_num = ord(en_pass_tracker['White'])
                        if (file_num - en_num == 1 or file_num - en_num == -1) and \
                            int(key[1]) == 4:
                                moveset.append(key+chr(en_num)+str(rank)+'P')


        #get knight moves
        elif board[key] == chess_pieces[pref+'knight']:
            file_num = ord(key[0])
            rank = int(key[1])

            # go throu each combination of knight move
            if file_num + 1 < 73 and rank + 2 < 9:
                if board[chr(file_num+1)+str(rank+2)] not in my_pieces:    
                    moveset.append(key+chr(file_num+1)+str(rank+2))

            if file_num - 1 > 64 and rank + 2 < 9:
                if board[chr(file_num-1)+str(rank+2)] not in my_pieces:    
                    moveset.append(key+chr(file_num-1)+str(rank+2))

            if file_num + 2 < 73 and rank + 1 < 9:
                if board[chr(file_num+2)+str(rank+1)] not in my_pieces:    
                    moveset.append(key+chr(file_num+2)+str(rank+1))

            if file_num - 2 > 64 and rank + 1 < 9:
                if board[chr(file_num-2)+str(rank+1)] not in my_pieces:    
                    moveset.append(key+chr(file_num-2)+str(rank+1))

            if file_num + 2 < 73 and rank - 1 > 0:
                if board[chr(file_num+2)+str(rank-1)] not in my_pieces:    
                    moveset.append(key+chr(file_num+2)+str(rank-1))
            
            if file_num - 2 > 64 and rank - 1 > 0:
                if board[chr(file_num-2)+str(rank-1)] not in my_pieces:    
                    moveset.append(key+chr(file_num-2)+str(rank-1))
            
            if file_num + 1 < 73 and rank - 2  > 0:
                if board[chr(file_num+1)+str(rank-2)] not in my_pieces:    
                    moveset.append(key+chr(file_num+1)+str(rank-2))
            
            if file_num - 1 > 64 and rank - 2 > 0:
                if board[chr(file_num-1)+str(rank-2)] not in my_pieces:    
                    moveset.append(key+chr(file_num-1)+str(rank-2))


        # get bishop moves
        elif board[key] == chess_pieces[pref+'bishop']:

            #set up a blocking boolean for blocked diagonals, counterclockwise
            b_blocked = [False,False,False,False]

            file_num = ord(key[0])
            rank = int(key[1])


            #get bishop like moves
            # get leftward moves
            for i in range(1,8,1):
                if file_num + i > 64 and file_num + i < 73:
                    if rank + i > 0 and rank + i < 9:
                        if b_blocked[3]:
                            pass
                        elif board[chr(file_num+i)+str(rank+i)] not in my_pieces: 
                            moveset.append(key+chr(file_num+i)+str(rank+i))
                            if board[chr(file_num+i)+str(rank+i)] in oth_pieces:
                                b_blocked[3] = True
                        else:
                            b_blocked[3] = True

                    if rank - i > 0 and rank - i < 9:
                        if b_blocked[2]:
                            pass
                        elif board[chr(file_num+i)+str(rank-i)] not in my_pieces:
                            moveset.append(key+chr(file_num+i)+str(rank-i))
                            if board[chr(file_num+i)+str(rank-i)] in oth_pieces:
                                b_blocked[2] = True
                        else:
                            b_blocked[2] = True
    

            # get rightward moves
            for i in range(-1,-8,-1):
                if file_num + i > 64 and file_num + i < 73:
                    if rank + i > 0 and rank + i < 9:
                        if b_blocked[0]:
                            pass
                        elif board[chr(file_num+i)+str(rank+i)] not in my_pieces: 
                            moveset.append(key+chr(file_num+i)+str(rank+i))
                            if board[chr(file_num+i)+str(rank+i)] in oth_pieces:
                                b_blocked[0] = True
                        else:
                            b_blocked[0] = True

                    if rank - i > 0 and rank - i < 9:
                        if b_blocked[1]:
                            pass
                        elif board[chr(file_num+i)+str(rank-i)] not in my_pieces:
                            moveset.append(key+chr(file_num+i)+str(rank-i))
                            if board[chr(file_num+i)+str(rank-i)] in oth_pieces:
                                b_blocked[1] = True
                        else:
                            b_blocked[1] = True


        

        # get rook moves
        elif board[key] == chess_pieces[pref+'rook']:


            file_num = ord(key[0])
            rank = int(key[1])

            r_blocked = [False,False,False,False]

            #get rooklike moves
            for i in range(1,8,1):
                # get rightward moves
                if file_num + i < 73:
                    if r_blocked[0]: 
                        pass
                    elif board[chr(file_num+i)+str(rank)] not in my_pieces:
                        moveset.append(key+chr(file_num+i)+str(rank))
                        if board[chr(file_num+i)+str(rank)] in oth_pieces:
                            r_blocked[0] = True
                    else:
                        r_blocked[0] = True

                #get upward moves
                if rank + i < 9:
                    if r_blocked[1]:
                        pass
                    elif board[chr(file_num)+str(rank+i)] not in my_pieces:
                        moveset.append(key+chr(file_num)+str(rank+i))
                        if board[chr(file_num)+str(rank+i)] in oth_pieces:
                            r_blocked[1] = True
                    else:
                        r_blocked[1] = True
                
                #get leftward moves
                if file_num - i > 64:
                    if r_blocked[3]:
                        pass
                    elif board[chr(file_num-i)+str(rank)] not in my_pieces:
                        moveset.append(key+chr(file_num-i)+str(rank))
                        if board[chr(file_num-i)+str(rank)] in oth_pieces:
                            r_blocked[3] = True
                    else:
                        r_blocked[3] = True
                
                #get downward moves
                if rank - i > 0:
                    if r_blocked[2]: 
                        pass
                    elif board[chr(file_num)+str(rank-i)] not in my_pieces:
                        moveset.append(key+chr(file_num)+str(rank-i))
                        if board[chr(file_num)+str(rank-i)] in oth_pieces:
                            r_blocked[2] = True
                    else:
                        r_blocked[2] = True




        #get king moves
        elif board[key] == chess_pieces[pref+'king'] and castleCheck == False:
            file_num = ord(key[0])
            rank = int(key[1])

            #get standard one square moves
            if file_num + 1 < 73 and \
                    board[chr(file_num+1)+str(rank)] not in my_pieces:
                moveset.append(key+chr(file_num+1)+str(rank))
            
            if file_num+1 < 73 and rank+1 < 9 and \
                    board[chr(file_num+1)+str(rank+1)] not in my_pieces:
                moveset.append(key+chr(file_num+1)+str(rank+1))
            
            if file_num+1<73 and rank-1>0 and \
                    board[chr(file_num+1)+str(rank-1)] not in my_pieces:
                moveset.append(key+chr(file_num+1)+str(rank-1))
            
            if rank+1<9 and board[chr(file_num)+str(rank+1)] not in my_pieces:
                moveset.append(key+chr(file_num)+str(rank+1))
            
            if rank-1>0 and board[chr(file_num)+str(rank-1)] not in my_pieces:
                moveset.append(key+chr(file_num)+str(rank-1))
            
            if file_num-1>64 and board[chr(file_num-1)+str(rank)] not in my_pieces:
                moveset.append(key+chr(file_num-1)+str(rank))
            
            if file_num-1>64 and rank+1 < 9 and \
                    board[chr(file_num-1)+str(rank+1)] not in my_pieces:
                moveset.append(key+chr(file_num-1)+str(rank+1))
            
            if file_num-1>64 and rank-1>0 and \
                    board[chr(file_num-1)+str(rank-1)] not in my_pieces:
                moveset.append(key+chr(file_num-1)+str(rank-1))



            #get castling moves
            if not king_in_check[color]:
                if color == 'White' and king_movement['White'] == False and\
                        rook_movement['White'][1] == False and\
                        board['F1'] == chess_pieces['blank'] and \
                        board['G1'] == chess_pieces['blank'] and\
                        castle_cutoff_check('White','Short') == False and\
                        board['E1'] == chess_pieces['w_king']:
                            moveset.append('O-O')
                if color == 'White' and king_movement['White'] == False and\
                        rook_movement['White'][0] == False and\
                        board['D1'] == chess_pieces['blank'] and \
                        board['C1'] == chess_pieces['blank'] and \
                        board['B1'] == chess_pieces['blank'] and \
                        castle_cutoff_check('White','Long') == False and\
                        board['E1'] == chess_pieces['w_king']:
                            moveset.append('O-O-O')
                if color == 'Black' and king_movement['Black'] == False and\
                        rook_movement['Black'][1] == False and\
                        board['F8'] == chess_pieces['blank'] and \
                        board['G8'] == chess_pieces['blank'] and\
                        castle_cutoff_check('Black','Short') == False and\
                        board['E8'] == chess_pieces['b_king']:
                            moveset.append('O-O')
                if color == 'Black' and king_movement['Black'] == False and\
                        rook_movement['Black'][0] == False and\
                        board['D8'] == chess_pieces['blank'] and \
                        board['C8'] == chess_pieces['blank'] and \
                        board['B8'] == chess_pieces['blank'] and \
                        castle_cutoff_check('Black','Long') == False and\
                        board['E8'] == chess_pieces['b_king']:
                            moveset.append('O-O-O')
                

        # get queen moves
        elif board[key] == chess_pieces[pref+'queen']:

            file_num = ord(key[0])
            rank = int(key[1])

            q_blocked = [False,False,False,False,False,False,False,False]
           
            #get rooklike moves
            for i in range(1,8,1):
                # get rightward moves
                if file_num + i < 73:
                    if q_blocked[4]: 
                        pass
                    elif board[chr(file_num+i)+str(rank)] not in my_pieces:
                        moveset.append(key+chr(file_num+i)+str(rank))
                        if board[chr(file_num+i)+str(rank)] in oth_pieces:
                            q_blocked[4] = True
                    else:
                        q_blocked[4] = True

                #get upward moves
                if rank + i < 9:
                    if q_blocked[5]:
                        pass
                    elif board[chr(file_num)+str(rank+i)] not in my_pieces:
                        moveset.append(key+chr(file_num)+str(rank+i))
                        if board[chr(file_num)+str(rank+i)] in oth_pieces:
                            q_blocked[5] = True
                    else:
                        q_blocked[5] = True
                
                #get leftward moves
                if file_num - i > 64:
                    if q_blocked[7]:
                        pass
                    elif board[chr(file_num-i)+str(rank)] not in my_pieces:
                        moveset.append(key+chr(file_num-i)+str(rank))
                        if board[chr(file_num-i)+str(rank)] in oth_pieces:
                            q_blocked[7] = True
                    else:
                        q_blocked[7] = True
                
                #get downward moves
                if rank - i > 0:
                    if q_blocked[6]: 
                        pass
                    elif board[chr(file_num)+str(rank-i)] not in my_pieces:
                        moveset.append(key+chr(file_num)+str(rank-i))
                        if board[chr(file_num)+str(rank-i)] in oth_pieces:
                            q_blocked[6] = True
                    else:
                        q_blocked[6] = True

            
            #get bishop like moves
            # get leftward moves
            for i in range(1,8,1):
                if file_num + i > 64 and file_num + i < 73:
                    if rank + i > 0 and rank + i < 9:
                        if q_blocked[3]:
                            pass
                        elif board[chr(file_num+i)+str(rank+i)] not in my_pieces: 
                            moveset.append(key+chr(file_num+i)+str(rank+i))
                            if board[chr(file_num+i)+str(rank+i)] in oth_pieces:
                                q_blocked[3] = True
                        else:
                            q_blocked[3] = True

                    if rank - i > 0 and rank - i < 9:
                        if q_blocked[2]:
                            pass
                        elif board[chr(file_num+i)+str(rank-i)] not in my_pieces:
                            moveset.append(key+chr(file_num+i)+str(rank-i))
                            if board[chr(file_num+i)+str(rank-i)] in oth_pieces:
                                q_blocked[2] = True
                        else:
                            q_blocked[2] = True
    

            # get rightward moves
            for i in range(-1,-8,-1):
                if file_num + i > 64 and file_num + i < 73:
                    if rank + i > 0 and rank + i < 9:
                        if q_blocked[0]:
                            pass
                        elif board[chr(file_num+i)+str(rank+i)] not in my_pieces: 
                            moveset.append(key+chr(file_num+i)+str(rank+i))
                            if board[chr(file_num+i)+str(rank+i)] in oth_pieces:
                                q_blocked[0] = True
                        else:
                            q_blocked[0] = True

                    if rank - i > 0 and rank - i < 9:
                        if q_blocked[1]:
                            pass
                        elif board[chr(file_num+i)+str(rank-i)] not in my_pieces:
                            moveset.append(key+chr(file_num+i)+str(rank-i))
                            if board[chr(file_num+i)+str(rank-i)] in oth_pieces:
                                q_blocked[1] = True
                        else:
                            q_blocked[1] = True


    return moveset




def castle_cutoff_check(color, side):

    if color == 'White' and side == 'Short':
        squares = ['F1','G1']
    elif color == 'White' and side == 'Long':
        squares = ['C1','D1']
    elif color == 'Black' and side == 'Short':
        squares = ['F8','G8']
    else:
        squares = ['C8','D8']

    #get the next possible moves for the opposite colors
    if color=='White': next_moves = get_valid_moves('Black', True)
    else: next_moves = get_valid_moves('White', True)

    #if a next move can lead to cutting off king, this is an illegal move
    for m in next_moves:
        if m[2:4] in squares:
            return True

    return False





def exec_move(color, entered): 

    #check for a castling move first
    if entered == 'O-O':
        if color == 'White':
            king_movement['White'] = True
            board['E1'] = chess_pieces['blank']
            board['F1'] = chess_pieces['w_rook']
            board['G1'] = chess_pieces['w_king']
            board['H1'] = chess_pieces['blank']
        else:
            king_movement['Black'] = True
            board['E8'] = chess_pieces['blank']
            board['F8'] = chess_pieces['b_rook']
            board['G8'] = chess_pieces['b_king']
            board['H8'] = chess_pieces['blank']
        return
    elif entered == 'O-O-O':
        if color == 'White':
            king_movement['White'] = True
            board['E1'] = chess_pieces['blank']
            board['D1'] = chess_pieces['w_rook']
            board['C1'] = chess_pieces['w_king']
            board['B1'] = chess_pieces['blank']
            board['A1'] = chess_pieces['blank']
        else:
            king_movement['Black'] = True
            board['E8'] = chess_pieces['blank']
            board['D8'] = chess_pieces['b_rook']
            board['C8'] = chess_pieces['b_king']
            board['B8'] = chess_pieces['blank']
            board['A8'] = chess_pieces['blank']
        return


    # replace the current piece position with a blank and swap the desired position
    piece = board[entered[0:2]]
    board[entered[2:4]] = piece
    board[entered[0:2]] = chess_pieces['blank']

    # check for an track en passant opportunities
    if piece == chess_pieces['w_pawn'] or piece == chess_pieces['b_pawn']:
        if abs(int(entered[1]) - int(entered[3])) == 2:
            en_pass_tracker[color] = entered[0]


    #check for if en passent has been performed
    try:
        if entered[4] == 'P':
            if color == 'White':
                board[entered[2]+'5'] = chess_pieces['blank']
            else:
                board[entered[2]+'4'] = chess_pieces['blank']

    except:
        pass

    #check for rook and king movement
    if entered[0:2] == 'A1':
        rook_movement['White'][0] = True
    elif entered[0:2] == 'H1':
        rook_movement['White'][1] = True
    elif entered[0:2] == 'A8':
        rook_movement['Black'][0] = True
    elif entered[0:2] == 'H8':
        rook_movement['Black'][1] = True
    elif entered[0:2] == 'E1':
        king_movement['White'] = True
    elif entered[0:2] == 'E8':
        king_movement['Black'] = True

    return










