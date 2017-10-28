"""
	board[]		  : unsigned int64 1D array of length 32 (1st 16 elements represent white and the other 16 elements represent the black),  
	                each element inside the array specify the location of the corresponding element 
			        array element number 1 specify rock of the White and so on.
	WhiteBitBoard : unsigned int64 variable Specify the white pieces exact locations  
	BlackBitBoard : unsigned int64 variables Specify the black pieces exact locations 
	move   		  : string is a src to dst string, in form of "FileRank"..(e.g. "A1 to B1"),
	piece  		  : is char indicating name of piece as "K"
	FEN    		  : string representing the chess board in Forsyth–Edwards Notation
	pastMoves 	  : list contains all past moves.

"""

"""
Integration Team Work / 
Implementation Team Work to test their code also [But read from console rather than GUI]

# will be called in main script at the initialization once only #
 get FEN at the program start from GUI and feed it to doFEN2Board(FEN);

 get Move from GUI and feed it to doMove();

"""

#_____________________________________________________________________________#
#This will convert the FEN file and covert it to a board 
#  return the array board[], BlackBitBoard , WhiteBitBoard
"""
Note in python you can return more than 1 variable ex : return board, BlackBitBoard, WhiteBitBoard will return all of those 
and in call you can simple use : Board,BlackBB,WhiteBB = readFEN2Board(FEN);
"""
def doFEN2Board(FEN) :  # (Safaa) and (Sara)
    return FEN



#_____________________________________________________________________________
#This will check if a move of a certain piece result in a check 
# return true : if move will cause Check
# return false otherwise.

def testCheck(BlackBitBoard,WhiteBitBoard, move, board =[], *args ): # (Gamal Mohammed)
    return BlackBitBoard

#_____________________________________________________________________________#
#This will return all possible moves for a certain piece
#return the list with updated board , BlackBitBoard , WhiteBitBoard after Move
def generateMoves(BlackBitBoard,WhiteBitBoard,piece, board =[], *args ): # (Hager) and (Abdelrhman)
    return BlackBitBoard
#_____________________________________________________________________________#
#This will do a sepcific move.[piece name and move included as generated from FEM file)
#return the updated board , BlackBitBoard , WhiteBitBoard
def doMove(BlackBitBoard,WhiteBitBoard, move, board =[], *args  ): #Hesham Magdy
     return BlackBitBoard

#_____________________________________________________________________________#
#Update the pastMoves list by adding the current move to be done [to account for Fifty-Move Rule]
#Update board , BlackBitBoard , WhiteBitBoard [to account for Threefold repetition draw rule]
def updatePastMoves(move): #(Sara) and (Safa)
    return move

