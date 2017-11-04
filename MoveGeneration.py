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
from collections import defaultdict
import re

### Debug Functions :
#Display the bit board. [indicating the presence of a piece
#into the console window for debug purposes
# will be called one time for the white team and other time for the black team 
# ( Abdelrhman )
def displayBitBoard(BitBoard):
  BitBoardTemp=BitBoard;
  maskMax          =0xFFFFFFFFFFFFFF      #Mask which initilally will mask most 8th byte after show it   
  for rowNum in range(7,-1,-1):           #Display Eight rows
    BitBoardTemp= BitBoardTemp>>(8*rowNum)#Shift left the least bytes to display only one byte 
    print(format(BitBoardTemp,'#010b'))   #Display the concerned byte in binary 
    BitBoardTemp             = BitBoard & (maskMax)#Mask the most (rowNum+1)th Byte 
    maskMax = maskMax >> 8                #Shift left the mask 1 byte 

### Debug Functions :
#Display the 32 array of integers showing the pieces positions
#into the console window as (x,y) positions for debug purposes
# ( Abdelrhman )
def displayPieces(boardTemp):
 print('White side:')                      #Print the white side positions  
 for numLine in range(2):                  #Iterate for 2 rows 
  for numElem in range(8):                 #Each row contains 8 elements 
   piecePos=boardTemp[(8*numLine)+numElem];#get the corresponding decimal position from board  
   if(piecePos!=-1): 					   #If piece not dead display its position 
     print('('+str(int(piecePos/8))+' , '+str(piecePos%8)+')',end=" ")
										   #X position from 0 to 7 and y position from 1 to 8 
   else:
     print('Dead   ',end=" ")              #Otherwise display dead 
  print('');				
 print('Black side:') 					   #Do the same for the black team [the remaining 16 elements] 
 for numLine in range(2):
  for numElem in range(8):
   piecePos=boardTemp[16+(8*numLine)+numElem];
   if(piecePos!=-1): 
     print('('+str(int(piecePos/8))+' , '+str(piecePos%8)+')',end=" ")
   else:
     print('Dead   ',end=" ")  
  print('')

  
#_____________________________________________________________________________#
#This will convert the FEN file and covert it to a board
#  return the array board[], BlackBitBoard , WhiteBitBoard
# ( Safa Tharwat and Saraa Ahmed )
def readFEN2Board(FEN) :
    ranks = FEN.split(" ")[0].split("/")
    Side_To_M = FEN.split(" ")[1]
    C_A = FEN.split(" ")[2]
    Left1 = 0
    Right1 = 0
    Left2 = 0
    Right2 = 0
    if (C_A[0] == "K"):
        Left1 = 1
    if(C_A[1] == "Q"):
        Right1 = 1
    if (C_A[2] == "k"):
        Left2 = 1
    if(C_A[3] == "q"):
        Right2 = 1
    C_A_L = [Left1,Right1,Left2,Right2]
    E_P_T_S = FEN.split(" ")[3]
    if(E_P_T_S == "-"):
        E_P_T_S = -1
    else:
        c = E_P_T_S[0]
        E_P_T_S = (8 * (8 - int(E_P_T_S[1]))) + ((ord(c) - 96))
    H_M_Clk = FEN.split(" ")[4]
    F_M_Counter = FEN.split(" ")[5]
    ############ generate board
    ############ Array###############################################################
    board = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    mylist = ["P","P","P","P","P","P","P","P","R","N","B","Q","K","B","N","R","r","n","b","q","k","b","n","r","p","p","p","p","p","p","p","p"]
    D = defaultdict(list)
    for i,item in enumerate(mylist):D[item].append(i)   
    Arr = {k:v for k,v in D.items()}
    ranki = 0
    index = 0
    index2 = 0
    count1 = 0
    count2 = 0
    for rank in ranks:
        for r in rank:
            if (re.compile("([kqbnrpKQBNRP])").match(r)):
                index = index + 1
                if(board[(Arr[r][0])] != -1):
                    if(r == 'p'): 
                        count1 += 1
                        index2 = (Arr[r][count1])
                    elif (r == 'P'):
                        count2 +=1
                        index2 = (Arr[r][count2])
                    else: index2 = (Arr[r][1])
                else:index2 = (Arr[r][0])
                board[index2] = (ranki * 8) + index
            else: index = index + int(r)
        ranki = ranki + 1
        index = 0
    ############ Whitebitboard & Blackbitboard
    m = 0
    n = 0
    for x in range(15):
        if(board[x] != -1 and m == 0):
            m = 1
            w = (1 << 64 - board[x])
        if(m == 1 and board[x + 1] != -1): 
            w = w ^ (1 << 64 - board[x + 1])
        if(board[x + 16] != -1 and n == 0):
            n = 1
            b = (1 << 64 - board[x + 16])
        if(n == 1 and board[x + 17] != -1):
            b = b ^ (1 << 64 - board[x + 17])
    blackbitboard = ('{0:064b}'.format(b))
    whitebitboard = ('{0:064b}'.format(w))
    return(board,blackbitboard,whitebitboard,C_A_L,E_P_T_S,H_M_Clk,F_M_Counter) 

#Utility Function Used in CheckMate
#Gamal Mohammed 
def CheckAttackLine(BlackBitBoard,WhiteBitBoard,king_loc,step,board=[],potentialAttackers=[],board_limits=[]):
    i = king_loc + step
    esc = False
    while not esc:
        if i in board_limits:
            esc = True

        if WhiteBitBoard & (1 << i): # Hit white piece, I'm safe!
            break
        if BlackBitBoard & (1 << i): # Hit black piece, DANGER!!
            for p in range(16,len(board)):
                if board[p] == i:
                    if p in potentialAttackers: 
                        return False
        i+=step
    return True


#_____________________________________________________________________________
#This will check if a move of a certain piece result in a check
#   return true : if move will cause Check
#   return false otherwise.
# ( Gamal Mohammed )
def CheckMate(BlackBitBoard,WhiteBitBoard, move,castling, board=[], *args):
    # Emulate move
    emulated_board = board[:]
    BlackBitBoard,WhiteBitBoard,emulated_board = doMove(BlackBitBoard,WhiteBitBoard,move,emulated_board)

    if not castling:
        king_loc = emulated_board[12]
        count = 1
    else:
        side_squares = [3,2]
        king_loc = side_squares[0]
        count = 2

    for i in range(count):
        # 1.  Check Left diagonal attack line, if exists
        potentialAttackers = [16,17,18,19,20,21,22,23,26,29,27]         # Black Queen or Bishops or Pawns
        if king_loc != 7:
            board_limits = [7,15,23,31,39,47,55,56,63,57,58,59,60,61,62]
            if not CheckAttackLine(BlackBitBoard,WhiteBitBoard,king_loc,9,board,potentialAttackers,board_limits):
                return False

        # 2.  Check Right diagonal attack line, if exists
        if king_loc != 0:
            board_limits = [0,8,16,24,32,40,48,56,57,58,59,60,61,62,63]
            if not CheckAttackLine(BlackBitBoard,WhiteBitBoard,king_loc,7,board,potentialAttackers,board_limits):
                return False

        # 3.  Check Forward Vertical attack line, if exists
        potentialAttackers = [27,24,31]            # Black Queen or Rooks
        board_limits = range(0,64)
        if not CheckAttackLine(BlackBitBoard,WhiteBitBoard,king_loc,8,board,potentialAttackers,board_limits):
            return False

        # 4.  Check Right Horizontal attack line, if exists
        if king_loc != 0:
            board_limits = [0,8,16,24,32,40,48,56]
            if not CheckAttackLine(BlackBitBoard,WhiteBitBoard,king_loc,-1,board,potentialAttackers,board_limits):
                return False

        # 5.  Check Left Horizontal attack line, if exists
        if king_loc != 7:
            board_limits = [7,15,23,31,39,47,55,56,63]
            if not CheckAttackLine(BlackBitBoard,WhiteBitBoard,king_loc,1,board,potentialAttackers,board_limits):
                return False

        if count == 2:
            king_loc = side_squares[1]

    return True


def generateMoves(BlackBitBoard,WhiteBitBoard,piece,left,right,order, board =[], *args ): # (Hager) and (Abdelrhman)
    possible=[]
	#Chess_Chari is a dictionary (in form {'piece':adi} describes :
	#a-   the possible x coordinate move : [one of available -max- 8 options] from adi[i] where 0<=i<=7 
	#b-   the 'piece' corresponding index in board adi[9+j] where j corresponds to the jth replica of piece
	#c-   adi[8] (=1 when piece can make its move many times , =2 if move done only one time , =3 in case of king)
	
	#order specify the order of pawn [from 0 to 7] , Bishop,Rook and Knight [0 or 1] 
    
    Chess_Chari={"K": [-1, -1, -1, 0,  0,  1, 1, 1,  3,12], \
	"Q": [-1,-1,-1,0 ,0, 1,1,1,1, 11] ,"N": [-1,-2,-1,-2,1,2,1 ,2 ,2, 9,14],"P":[0,1,1,1,0,0,0,0,2, 0,1,2,3,4,5,6,7],\
	"B": [-1,  0, -1, 0,  0,  1, 0, 1, 1, 10,13],"R": [ 0, -1, 0,  0,  0, 0, 1, 0, 1, 8,15]}
	
    Chess_Charj={"K": [-1,  0,  1, -1, 1, -1, 0, 1,  3,12], \
	"Q": [-1, 0,1 ,-1,1,-1,0,1,1, 11] ,"N": [-2,-1,2 , 1,2,1,-2,-1,2, 9,14],"P":[0,0,1,-1,0,0,0,0,2, 0,1,2,3,4,5,6,7],\
	"B": [-1,  0,  1, 0,  0, -1, 0, 1, 1, 10,13],"R": [ 0,  0, 0, -1,  1, 0, 0, 0, 1, 8,15]}

    adi =Chess_Chari[piece]#get the vector adi corresponds to the piece 
    adj =Chess_Charj[piece]#get the vector adj corresponds to the piece
    
    castling =[left,right]
    castlingx=[136,9]

    #Iterate over the 2 	
	#Bishop ,knight and Rook has 2 positions in board [two types of bishops , knights and rooks]        
    j=order;
    if board[adi[9+j]]==-1:#If piece is dead then return None
          return ;
    x=board[adi[9+j]]      #Get old poistion of the piece  
    print('Old position : '+str(int(x/8))+' , '+str(x%8))
    if (piece == "P" and 8<x<=16): #If piece is pawn and this is the first move 
      adi[0]=2;	                  #Then pawn can move 2 squares forward 
    for i in range(8) :   
	
            x=board[adi[9+j]]    #Get old poistion of the piece  
            idxi=int(x/8)+adi[i] #Make a proposed horizontal move : starts from 0 to 7 
            idxj=x%8     +adj[i] #Make a proposed vertical   move : starts from 1 to 8 
            x= x + adi[i]*8 + adj[i]
            print('Proposed New position : ('+str(idxi)+' , '+str(idxj)+ ") = "+str(x))
            check=1
			
            while 0 <= idxi <8 and 0 < idxj <=8 and check==1:
                if x<64: #If x is valid then put proper value in l to check that no piece in proposed location
                    l=1<<(64-x)
                if l&WhiteBitBoard>0:#If piece exist then can't move forward 
                    break
                if(piece=="P" and (i==2 or i==3)): #Pawn is in capturing move	
                    if l&BlackBitBoard==0:#If no capture then no capturing move can be done 
                        break
                if(piece=="P" and (i==0 or i==1)): #Pawn is in not in capturing move	
                    if l&BlackBitBoard>0:#If it try to capture prevent as Pawn can't capture in this way  
                        break
						
                u=piece+str(j)+" "+str(board[adi[8+j]])+" "+ str(x)
				
                check=adi[8] #repeat the move if adi[8]==1 (Queen , Bishop and Rook only) 
                if CheckMate(BlackBitBoard,WhiteBitBoard,u,False, board)==True: 
                    print('New position : ('+str(idxi)+' , '+str(idxj)+ ") = "+str(x),end=" ")
                    possible.append(x)
                if l&BlackBitBoard>0:#If piece exist then capture and make move [Need to be completed ] 
                    print(' Capture Happens Here');
                    break
                print(" ")
                idxi=idxi+adi[i]
                idxj=idxj+adj[i]
                #print(str(idxi) +"  "+ str(idxj))
                x=x+adi[i]*8+adj[i]
    
			
    for j in range(2):
        if adi[8]==3 and castling[j]==1: #Happens with the King Only and if castling
            if WhiteBitBoard^castlingx[j]==0:
                if testCheck(BlackBitBoard,WhiteBitBoard,u,"true", board)=="true": #check 2 squares beside king and King
                    possible.append((j+1)*1000)
    
    return possible

#_____________________________________________________________________________#
#This will do a sepcific move.[piece name and move included as generated from
#FEM file)
#return the updated board , BlackBitBoard , WhiteBitBoard
def doMove(BlackBitBoard,WhiteBitBoard, move, board=[], *args): #Hesham Magdy
     return BlackBitBoard,WhiteBitBoard,board

#_____________________________________________________________________________#
#Update the pastMoves list by adding the current move to be done [to account
#for Fifty-Move Rule]
#Update board , BlackBitBoard , WhiteBitBoard [to account for Threefold
#repetition draw rule]
def updatePastMoves(move): #(Sara) and (Safa)
    return move

