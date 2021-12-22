

letters = ['A','B','C','D','E','F','G','H']
numbers = ['8','7','6','5','4','3','2','1']

board = {}
chess_pieces = {}

#track if a pawn has opened itself to en passent
en_pass_tracker = {'White':'','Black':''}

#track king castling rights
king_movement = {'White':False, 'Black':False}
rook_movement = {'White':[False,False],'Black':[False,False]}


#track whether king is in check
king_in_check = {'White':False, 'Black':False}

fifty_move_cnt = 0

total_moves = 1

