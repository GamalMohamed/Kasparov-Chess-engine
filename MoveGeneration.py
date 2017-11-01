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
from collections import defaultdict
import re
def readFEN2Board(FEN) :
    ranks = FEN.split(" ")[0].split("/")
    Side_To_M = FEN.split(" ")[1]
    C_A = FEN.split(" ")[2]
    Left1=0
    Right1=0
    Left2=0
    Right2=0
    if (C_A[0]=="K"):
        Left1=1
    if(C_A[1]=="Q"):
        Right1=1
    if (C_A[2]=="k"):
        Left2=1
    if(C_A[3]=="q"):
        Right2=1
    C_A_L=[Left1,Right1,Left2,Right2]
    E_P_T_S=FEN.split(" ")[3]
    if(E_P_T_S=="-"):
        E_P_T_S=-1
    else:
        c=E_P_T_S[0]
        E_P_T_S=(8*(8-int(E_P_T_S[1])))+((ord(c)-96))
    H_M_Clk=FEN.split(" ")[4]
    F_M_Counter=FEN.split(" ")[5]
    ############ generate board  Array###############################################################
    board=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    mylist = ["P","P","P","P","P","P","P","P","R","N","B","Q","K","B","N","R","r","n","b","q","k","b","n","r","p","p","p","p","p","p","p","p"]
    D = defaultdict(list)
    for i,item in enumerate(mylist):D[item].append(i)   
    Arr = {k:v for k,v in D.items()}
    ranki=0
    index=0
    index2=0
    count1=0
    count2=0
    for rank in ranks:
        for r in rank:
            if (re.compile("([kqbnrpKQBNRP])").match(r)):
                index=index+1
                if(board[(Arr[r][0])]!=-1):
                    if(r=='p'): 
                        count1 += 1
                        index2=(Arr[r][count1])
                    elif (r=='P'):
                        count2 +=1
                        index2=(Arr[r][count2])
                    else: index2=(Arr[r][1])
                else:index2=(Arr[r][0])
                board[index2]=(ranki*8)+index
            else: index=index+int(r)
        ranki=ranki+1
        index=0
    ############ Whitebitboard & Blackbitboard    
    m=0
    n=0
    for x in range(15):
        if(board[x]!=-1 and m==0 ):
            m=1
            w = (1<<64-board[x])
        if(m==1 and board[x+1]!=-1 ): 
            w = w ^ (1<<64-board[x+1])
        if(board[x+16]!=-1 and n==0 ):
            n=1
            b = (1<<64-board[x+16])
        if(n==1 and board[x+17]!=-1 ):
            b = b ^ (1<<64-board[x+17])
    blackbitboard=('{0:064b}'.format(b))
    whitebitboard=('{0:064b}'.format(w))
    return(board,blackbitboard,whitebitboard,C_A_L,E_P_T_S,H_M_Clk,F_M_Counter) 



#_____________________________________________________________________________
#This will check if a move of a certain piece result in a check 
# return true : if move will cause Check
# return false otherwise.

def testCheck(BlackBitBoard,WhiteBitBoard, move,castling, board =[], *args ): # (Gamal Mohammed)
    return "true"


def generateMoves(BlackBitBoard,WhiteBitBoard,piece,left,right, board =[], *args ): # (Hager) and (Abdelrhman)
    possible=[]
    Chess_Chari={"K": [-1, -1, -1, 0,  0,  1, 1, 1, 3,12],"B": [-1,  0, -1, 0,  0,  1, 0, 1, 1,10,14],"R": [ 0, -1, 0,  0,  0, 0, 1, 0, 1,8,15]}
    Chess_Charj={"K": [-1,  0,  1, -1, 1, -1, 0, 1, 3,12],"B": [-1,  0,  1, 0,  0, -1, 0, 1, 1,10,14],"R": [ 0,  0, 0, -1,  1, 0, 0, 0, 1,8,15]}
    adi =Chess_Chari[piece]
    adj =Chess_Charj[piece]
    castling=[left,right]
    castlingx=[136,9]
    for j in range(2):
        print(board[adi[9+j]])
        if board[adi[9+j]]==-1:
            print(adi)
            continue;
        for i in range(8):
            x=board[adi[9+j]]
            idxi=int(x/8)+adi[i]
            idxj=x%8+adj[i]
            x=x+adi[i]*8+adj[i]
            check=1
            while 0 <= idxi <8 and 0 < idxj <=8 and check==1:
                if x<64:
                    l=1<<(64-x)
                if l&WhiteBitBoard>0:
                    break
                u=piece+str(j)+" "+str(board[adi[8+j]])+" "+ str(x)
                check=adi[8]
                if testCheck(BlackBitBoard,WhiteBitBoard,u,"false", board)=="true":
                    possible.append(x)
                if l&BlackBitBoard>0:
                    break
                idxi=idxi+adi[i]
                idxj=idxj+adj[i]
                #print(str(idxi) +"  "+ str(idxj))
                x=x+adi[i]*8+adj[i]
        if piece=="K":
            break
    for j in range(2):
        if adi[8]==3 and castling[j]==1:
            if WhiteBitBoard^castlingx[j]==0:
                if testCheck(BlackBitBoard,WhiteBitBoard,u,"true", board)=="true": #check 2 squares beside king and King
                    possible.append((j+1)*1000)
    return possible
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
#Bishop
board=[-1,-1,-1,-1,-1,-1,-1,-1 ,-1,-1,37,-1,-1,-1,-1,-1 ,-1,-1,-1,-1,-1,-1,-1,-1  ,-1,-1,-1,-1,-1,-1,-1,-1 ]
BlackBitBoard=1<<18
WhiteBitBoard=(1<<(64-37))
#King
#board=[-1,-1,-1,-1,-1,-1,-1,-1 ,-1,-1,-1,-1,61,-1,-1,-1 ,-1,-1,-1,-1,-1,-1,-1,-1  ,-1,-1,-1,-1,-1,-1,-1,-1 ]
#BlackBitBoard=0
#WhiteBitBoard=9
#Rook
#board=[-1,-1,-1,-1,-1,-1,-1,-1 ,37,-1,-1,-1,-1,-1,-1,-1 ,-1,-1,-1,-1,-1,-1,-1,-1  ,-1,-1,-1,-1,-1,-1,-1,-1]
#BlackBitBoard=1<<18
#WhiteBitBoard=(1<<(64-37))
x=generateMoves(BlackBitBoard,WhiteBitBoard,"B",0,1, board )
print (x)