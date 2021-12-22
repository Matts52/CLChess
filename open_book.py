

from config import *


# create an opening book for the AI to follow

# format of book -> opening_book = {"FEN": { Common Moves, probability of each move },...}

opening_book = {

#------- AS BLACK ----------#

#1. e4 
"rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR": { 'moves' : ["E7E5","C7C5","C7C6","D7D5"], 'prob' : [0.5,0.3,0.1,0.1] },

### E5 ###
#1. e4e5 2. Nf3
"rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R": { 'moves' : ["B8C6","G8F6","D7D5"], 'prob' : [0.75,0.2,0.05] },

# (Italian Game)
#1. e4e5 2. Nf3Nc6 3. BC4
"r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R": { 'moves' : ["F8C5","G8F6","F8E7"], 'prob' : [0.55,0.35,0.1] },


# (Ruy Lopez)
#1. e4e5 2. Nf3Nc6 3. Bb5
"r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R": { 'moves' : ["A7A6","G8F6","F7F5"], 'prob' : [0.9,0.07,0.03] },

#1. e4e5 2. Nf3Nc6 3. Bb5a6 Ba4 (Morphy's Defense, Columbus Variation)
"r1bqkbnr/1ppp1ppp/p1n5/4p3/B3P3/5N2/PPPP1PPP/RNBQK2R": { 'moves' : ["G8F6","D4D6"], 'prob' : [0.85,0.15] },

#1. e4e5 2. Nf3Nc6 3. Bb5a6 Ba4Kf3 4. O-O (Morphy's Defense, Columbus Variation)
"r1bqkb1r/1ppp1ppp/p1n2n2/4p3/B3P3/5N2/PPPP1PPP/RNBQ1RK1": { 'moves' : ["F8E7","B7B5", "F6E4"], 'prob' : [0.74,0.15,0.11] },

#1. e4e5 2. Nf3Nc6 3. Bb5a6 Ba4Kf3 4. O-OBe7 5. Re1 (Morphy's Defense, Columbus Variation, Closed)
"r1bqk2r/1pppbppp/p1n2n2/4p3/B3P3/5N2/PPPP1PPP/RNBQR1K1": { 'moves' : ["B7B5"], 'prob' : [1.0] },

#1. e4e5 2. Nf3Nc6 3. Bb5a6 Ba4Kf3 4. O-OBe7 5. Re1b5 (Morphy's Defense, Columbus Variation, Closed)
"r1bqk2r/2ppbppp/p1n2n2/1p2p3/4P3/1B3N2/PPPP1PPP/RNBQR1K1": { 'moves' : ["D7D6","O-O"], 'prob' : [0.66,0.34] },




### SICILIAN ###
#1. e4c6 2. Nf3 (Sicilian Beginning)
"rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R": { 'moves' : ["D4D6","B8C6","E4E6"], 'prob' : [0.4,0.3,0.3] },

#1. e4c6 2. Nd3Nc6 3. d4 (Open Sicilian) 
"r1bqkbnr/pp1ppppp/2n5/2p5/3PP3/5N2/PPP2PPP/RNBQKB1R": { 'moves' : ["C5D4"], 'prob' : [1.0] },

#1. e4c6 2. Nd3Nc6 3. d4cxd4 4. Nc3Nxd4 (Open Sicilian) 
"r1bqkbnr/pp1ppppp/2n5/8/3NP3/8/PPP2PPP/RNBQKB1R": { 'moves' : ["G8F6","E7E6","G7G6","E7E5"], 'prob' : [0.35,0.3,0.25,0.1] },


### CARO-KANN ###



### SCANDINAVIAN ###




#-------- AS WHITE ----------#

#first move
"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR": { 'moves' : ["E2E4","D2D4","G1F3","C2C4"], 'prob' : [0.55,0.3,0.10,0.05] },

### E5 ###
#1. e4e5
"rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR": { 'moves' : ["G1F3","B1C3","F2F4"], 'prob' : [0.9,0.05,0.05] },

#1. e4e5 2. Nf3Nc6
"r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R": { 'moves' : ["F1B5","F1C4","D2D4"], 'prob' : [0.6,0.2,0.2] },

# (Italian Game)
#1. e4e5 2. Nf3Nc6 3. Bc4Bc5 (Guicco Piano)
"r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R": { 'moves' : ["C2C3","O-O","D2D3","B2B4"], 'prob' : [0.6,0.2,0.1,0.1] },


# (Ruy Lopez)
#1. e4e5 2. Nf3Nc6 3. Bb5a6 (Morphy's Defense)
"r1bqkbnr/1ppp1ppp/p1n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R": { 'moves' : ["B5A4","B5C6"], 'prob' : [0.86,0.14] },

#1. e4e5 2. Nf3Nc6 3. Bb5a6 Ba4Kf3 (Morphy's Defense, Columbus Variation)
"r1bqkb1r/1ppp1ppp/p1n2n2/4p3/B3P3/5N2/PPPP1PPP/RNBQK2R": { 'moves' : ["O-O","D2D3", "D1E2"], 'prob' : [0.87,0.08,0.04] },

#1. e4e5 2. Nf3Nc6 3. Bb5a6 Ba4Kf3 4. O-OBe7 (Morphy's Defense, Columbus Variation, Closed)
"r1bqk2r/1pppbppp/p1n2n2/4p3/B3P3/5N2/PPPP1PPP/RNBQ1RK1": { 'moves' : ["F1E1","D2D3", "A4C6"], 'prob' : [0.9,0.07,0.03] },

#1. e4e5 2. Nf3Nc6 3. Bb5a6 Ba4Kf3 4. O-OBe7 5. Re1b5 (Morphy's Defense, Columbus Variation, Closed)
"r1bqk2r/2ppbppp/p1n2n2/1p2p3/B3P3/5N2/PPPP1PPP/RNBQR1K1": { 'moves' : ["A4B3"], 'prob' : [1.0] },




### SICILIAN ###
#1. e4c5
"rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR": { 'moves' : ["G1F3","B1C3","C2C3"], 'prob' : [0.8,0.1,0.1] },

#1. e4c5 2. Nf3Nc6 (Old Sicilian)
"r1bqkbnr/pp1ppppp/2n5/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R": { 'moves' : ["D2D4","F1B5","B1C3"], 'prob' : [0.8,0.15,0.05] },

#1. e4c6 2. Nd3Nc6 3. d4cxd4 (Open Sicilian) 
"r1bqkbnr/pp1ppppp/2n5/8/3pP3/5N2/PPP2PPP/RNBQKB1R": { 'moves' : ["F3D4"], 'prob' : [1.0] },

}





