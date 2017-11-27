from MoveGeneration import * 

###  Main Script 
###  Test ReadFEN
FEN_Test2="rnbqkbnr/pppp1ppp/8/8/3pP3/2P5/PP3PPP/RNBQKBNR b KQkq - 1 3"
FEN_Test="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
board,blackbitboard,whitebitboard,C_A_L,E_P_T_S,H_M_Clk,F_M_Counter=readFEN2Board(FEN_Test)
print(board)
print(blackbitboard)
print(whitebitboard)
print(C_A_L)
print(E_P_T_S)
print(H_M_Clk)
print(F_M_Counter)


"""
#Testing Bishop Moves
#Bishop [of order 0]

board =[-1,-1,-1,-1,-1,-1,-1,-1 ,-1,-1,37,-1,-1,-1,-1,-1 ,-1,-1,-1,-1,-1,-1,-1,-1 ,-1,-1,-1,-1,-1,-1,-1,-1]
BlackBitBoard= 1<<18
WhiteBitBoard=(1<<(64-37))
print('Chess Board pieces positions:');displayPieces(board)
print('White Bit Board');displayBitBoard(WhiteBitBoard)
print('Black Bit Board');displayBitBoard(BlackBitBoard)

x=generateMoves(BlackBitBoard,WhiteBitBoard,"B",0,0,0, board )

"""

"""
#Testing King Moves
 
board=[-1,-1,-1,-1,-1,-1,-1,-1 ,-1,-1,-1,-1,61,-1,-1,-1 ,-1,-1,-1,-1,-1,-1,-1,-1  ,-1,-1,-1,-1,-1,-1,-1,-1 ]
BlackBitBoard=0
WhiteBitBoard=(1<<(64-61))
print('Chess Board pieces positions:');displayPieces(board)
print('White Bit Board');displayBitBoard(WhiteBitBoard)
print('Black Bit Board');displayBitBoard(BlackBitBoard)

x=generateMoves(BlackBitBoard,WhiteBitBoard,"K",0,0,0, board )

"""

"""
#Testing Rook Moves
#Rook [of order 0]

board=[-1,-1,-1,-1,-1,-1,-1,-1 ,37,-1,-1,-1,-1,-1,-1,-1 ,-1,-1,-1,-1,-1,-1,-1,-1  ,-1,-1,-1,-1,-1,-1,-1,-1]
BlackBitBoard=1<<18
WhiteBitBoard=(1<<(64-37))
print('Chess Board pieces positions:');displayPieces(board)
print('White Bit Board');displayBitBoard(WhiteBitBoard)
print('Black Bit Board');displayBitBoard(BlackBitBoard)

x=generateMoves(BlackBitBoard,WhiteBitBoard,"R",0,0,0, board )

"""




###################################################################
"""
#Testing Knight Moves 
Knight [of order 0]
board=[-1,-1,-1,-1,-1,-1,-1,-1 ,-1,37,-1,-1,-1,-1,-1,-1 ,-1,-1,-1,-1,-1,-1,-1,-1  ,-1,-1,-1,-1,-1,-1,-1,-1]
BlackBitBoard=1<<18
WhiteBitBoard=(1<<(64-37))

print('Chess Board pieces positions:');displayPieces(board)
print('White Bit Board');displayBitBoard(WhiteBitBoard)
print('Black Bit Board');displayBitBoard(BlackBitBoard)

x=generateMoves(BlackBitBoard,WhiteBitBoard,"N",0,0,0, board )

###################################################################
"""


#Testing Pawns Moves 

#Pawn [2 pawns at 9 and 18] 
board=[9,18,-1,-1,-1,-1,-1,-1 ,-1,-1,-1,-1,7,-1,-1,-1 ,-1,-1,-1,-1,-1,-1,-1,-1  ,-1,-1,-1,-1,-1,-1,-1,-1]
BlackBitBoard=1<<(64-25) #Piece can be captured 
BlackBitBoard=BlackBitBoard | 1<<(64-27) #Piece can be captured

WhiteBitBoard=(1<<(64-9))
WhiteBitBoard=WhiteBitBoard | (1<<(64-18))

print('Chess Board pieces positions:');displayPieces(board)
print('White Bit Board');displayBitBoard(WhiteBitBoard)
print('Black Bit Board');displayBitBoard(BlackBitBoard)

print('Moving the first pawn : ')
x=generateMoves(BlackBitBoard,WhiteBitBoard,"P",0,0,0, board )
print('Moving the second pawn : ')
x=generateMoves(BlackBitBoard,WhiteBitBoard,"P",0,0,1, board )
 
"""
#Testing Queen Moves :

board=[-1,-1,-1,-1,-1,-1,-1,-1 ,-1,-1,-1,11,-1,-1,-1,-1 ,-1,-1,-1,-1,-1,-1,-1,-1  ,-1,-1,-1,-1,-1,-1,-1,-1]
BlackBitBoard= (1<<(64-18))
WhiteBitBoard= (1<<(64-11))

print('Chess Board pieces positions:');displayPieces(board)
print('White Bit Board');displayBitBoard(WhiteBitBoard)
print('Black Bit Board');displayBitBoard(BlackBitBoard)

x=generateMoves(BlackBitBoard,WhiteBitBoard,"Q",0,0,0, board )

"""

print('Possible Moves : ')
print (x)
