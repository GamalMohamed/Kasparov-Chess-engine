
# coding: utf-8

# In[ ]:

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
from collections import namedtuple
import re
import re
import numpy as np
import os
import sys
import random
import time
import array
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

def readFEN2Board(FEN) :
    ranks = FEN.split(" ")[0].split("/")
    Side_To_M = FEN.split(" ")[1]
    C_A = FEN.split(" ")[2]    # Castling Ability
    Left1,Right1,Left2,Right2=0,0,0,0
    if (C_A[0]=="K"):
        Left1=1
    if(C_A[1]=="Q"):
        Right1=1
    if (C_A[2]=="k"):
        Left2=1
    if(C_A[3]=="q"):
        Right2=1
    C_A_L=[Left1,Right1,Left2,Right2]
    E_P_T_S=FEN.split(" ")[3]  # En Passant Target Square
    if(E_P_T_S=="-"):
        E_P_T_S=-1
    else:
        c=E_P_T_S[0]
        E_P_T_S=(8*(8-int(E_P_T_S[1])))+((ord(c)-96))
    H_M_Clk=FEN.split(" ")[4]    # Half-Move Clock
    F_M_Counter=FEN.split(" ")[5] #Full-Move Counter
    ############ generate board  Array###############################################################
    board=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]  # initial -1
    boardblack=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
	
	#8 P White  , R to R white,8P Black ,R to R Black
    mylist = ["P","P","P","P","P","P","P","P","R","N","B","Q","K","B","N","R","p","p","p","p","p","p","p","p","r","n","b","q","k","b","n","r"] 
    D = defaultdict(list)
    for i,item in enumerate(mylist):D[item].append(i)   
    Arr = {k:v for k,v in D.items()}
    ranki,index,index2,count1,count2=0,0,0,0,0
	# Array board 
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
    m,n,b,w=0,0,0,0
    for x in range(15):
        if(board[x]!=-1 and m==0 ):      #first 16 elements in board Array for White pieces
            m=1
            w = (1<<64-board[x])
        if(m==1 and board[x+1]!=-1 ): 
            w = w ^ (1<<64-board[x+1])
        if(board[x+16]!=-1 and n==0 ):   #last 16 elements in board Array for Black pieces
            n=1
            b = (1<<64-board[x+16])
        if(n==1 and board[x+17]!=-1 ):
            b = b ^ (1<<64-board[x+17])
#    white=0;
#    black=(1<<64-board[16]);
#    for a in range(16):
#        if(board[a]!=-1):
#            white=white | (1<<64-board[a])
#        if(board[a+16]!=-1):
#            black=black | (1<<64-board[a+16])
#    print("black=",black)
#    print(white)
    blackbitboard=b
    whitebitboard=w
    o=16
    for x in board:
        boardblack[o]=x
        o=o+1
        if o==32:
            o=0
    p=[]
    return(board,boardblack,blackbitboard,whitebitboard, Side_To_M,C_A_L,E_P_T_S,H_M_Clk,F_M_Counter,p)
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
def CheckMate(BlackBitBoard,WhiteBitBoard, move,castling, board,boardbl, *args):
    # Emulate move
    emulated_board = board[:]    
    emulated_boardbl = boardbl[:]
	#Debug [Abdelrhman : 11 August ] 
    #print(move);
    displayPieces(emulated_board);
    BlackBitBoard,WhiteBitBoard,emulated_board,x,l = doMove(BlackBitBoard,WhiteBitBoard,move,emulated_board,emulated_boardbl)
    #print (emulated_board)
    #print (BlackBitBoard)
    #print (WhiteBitBoard)
    return True;
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


def generateMoves(BlackBitBoard,WhiteBitBoard,piece,left,right,order, board,boardbl ): # (Hager) and (Abdelrhman)
    possible=[]
	#Chess_Chari is a dictionary (in form {'piece':adi} describes :
	#a-   the possible x coordinate move : [one of available -max- 8 options] from adi[i] where 0<=i<=7 
	#b-   the 'piece' corresponding index in board adi[9+j] where j corresponds to the jth replica of piece
	#c-   adi[8] (=1 when piece can make its move many times , =2 if move done only one time , =3 in case of king)
	
	#order specify the order of pawn [from 0 to 7] , Bishop,Rook and Knight [0 or 1] 
    
    Chess_Chari={"K": [-1, -1, -1, 0,  0,  1, 1, 1,  3,12], 	"Q": [-1,-1,-1,0 ,0, 1,1,1,1, 11] ,"N": [-1,-2,-1,-2,1,2,1 ,2 ,2, 9,14],"P":[-1,-1,-1,-2,0,0,0,0,2, 0,1,2,3,4,5,6,7],	"B": [-1,  0, -1, 0,  0,  1, 0, 1, 1, 10,13],"R": [ 0, -1, 0,  0,  0, 0, 1, 0, 1, 8,15]}
	
    Chess_Charj={"K": [-1,  0,  1, -1, 1, -1, 0, 1,  3,12], 	"Q": [-1, 0,1 ,-1,1,-1,0,1,1, 11] ,"N": [-2,-1,2 , 1,2,1,-2,-1,2, 9,14],"P":[-1,0,1,0,0,0,0,0,2, 0,1,2,3,4,5,6,7],	"B": [-1,  0,  1, 0,  0, -1, 0, 1, 1, 10,13],"R": [ 0,  0, 0, -1,  1, 0, 0, 0, 1, 8,15]}
    adi =Chess_Chari[piece]#get the vector adi corresponds to the piece 
    adj =Chess_Charj[piece]#get the vector adj corresponds to the piece 
    castling=[left,right]
    castlingx=[136,9]
    capture=[]
    t=0;
    pawn=0
    for j in range(order):
        if board[adi[9+j]]==-1:#If piece is dead then return None
            print(adi)
            continue;       
        print(board[adi[9+j]])
        for i in range(8):
            x=board[adi[9+j]]#Get old poistion of the piece
            xold=x
            idxi=int(x/8)+adi[i]#Make a proposed vertical move : starts from 0 to 7 
            idxj=x%8+adj[i]#Make a proposed horizontal move : starts from 0 to 7 
            if x%8==0:
                idxi=int(x/8)+adi[i]-1
                idxj=8+adj[i]
            x=idxi*8+idxj #new position 
            check=1
            while 0 <= idxi <8 and 0 < idxj <=8 and check==1:
                u=piece+str(j)+" "+str(xold)+" "
                v=u
                cast=0            
                pawn=0
                if x<=64:
                    l=1<<(64-x)
                if l&WhiteBitBoard>0:
                    break
                if(piece=="P" and (i==0 or i==2)): #Pawn is in capturing move
                    if l&BlackBitBoard==0:#If no capture then no capturing move can be done 
                        break
#                if(piece=="P" and (i==4 or i==5) ): #Pawn can capture pawnbeside hime
#                    if xold<33 or xold>40:                        
#                        break
#                    else:
#                        lbf=1<<(65-(x))                   
#                        laf=1<<(63-x)
#                        print("lbf = ",lbf," laf = ",laf,lbf&BlackBitBoard)
#                        if lbf&BlackBitBoard!=0 or laf&BlackBitBoard!=0:#If no capture then no capturing move can be done 
#                            break
                if(piece=="P" and i==3 ): #Pawn can make 2 move
                    if xold<49 or xold>56:
#                        lbf=1<<(65-x)                   
#                        laf=1<<(63-x)
#                        print("lbf = ",lbf," laf = ",laf,lbf&BlackBitBoard)
#                        if lbf&BlackBitBoard!=0 or laf&BlackBitBoard!=0:#If no capture then no capturing move can be done 
#                            break
#                    else:
                        break
                u=u + str(x)
                check=adi[8]
                #print (u)
                if CheckMate(BlackBitBoard,WhiteBitBoard,u,False, board,boardbl)==True:
                    t=t+1
                    possible.append(u)
                    if l&BlackBitBoard>0:
                        if board[24]==x or board[31]==x: #check if it capture rook
                            capture.append("R")
                        elif board[25]==x or board[30]==x: #check if it capture Knight
                            capture.append("N")
                        elif board[26]==x or board[29]==x: #check if it capture B
                            capture.append("B")
                        elif board[27]==x:					#check if it capture queen
                            capture.append("Q")
                        elif board[28]==x:					#check if it capture King
                            capture.append("K")
                        else:
                            pawn=1
                            capture.append("P")				#check if it capture pawn
                        break
                if l&BlackBitBoard>0:
                     break
                capture.append("-")
                idxi=idxi+adi[i]
                idxj=idxj+adj[i]
                #print(str(idxi) +"  "+ str(idxj))
                x=x+adi[i]*8+adj[i]
        if piece=="K":
            break
    j=0
    for j in range(2):
        if adi[8]==3 and castling[j]==1:
            if (WhiteBitBoard & castlingx[j])^castlingx[j]==0:
                if CheckMate(BlackBitBoard,WhiteBitBoard,v+str((j+1)*1000),True, board,boardbl)==True: #check 2 squares beside king and King
                    possible.append(v+str((j+1)*1000))
                    capture.append("-")
    cast=0
    if piece=='R' or piece=='K' :
         cast=xold
    return possible,capture,pawn,cast

# _____________________________________________________________________________#
# This will do a sepcific move.[piece name and move included as generated from
# FEM file)
# return the updated board , BlackBitBoard , WhiteBitBoard
def doMove(BlackBitBoard, WhiteBitBoard, move, Board, BoardBlack):  # Hesham Magdy
    srcPos = int(move.split(" ")[1])# Move p0 13 45   [32 
    dstPos = int(move.split(" ")[2])
    if int(dstPos) == 1000:        
        Board[12] = 59
        BoardBlack[28] = 59
        if Board[8] == 57:
            Board[8]=60
            BoardBlack[24] = 60
        else:
           Board[15]=60
           BoardBlack[31] = 60 
        WhiteBitBoard = WhiteBitBoard ^ 184;
        return BlackBitBoard, WhiteBitBoard, Board, BoardBlack, 1
    if int(dstPos) == 2000:
        Board[12] = 63
        BoardBlack[28] = 63
        if Board[8] == 64:
            Board[8]=62
            BoardBlack[24] = 62
        else:
           Board[15]=62
           BoardBlack[31] = 62 
        WhiteBitBoard = WhiteBitBoard ^ 15;
        return BlackBitBoard, WhiteBitBoard, Board, BoardBlack, 2
    if srcPos <65 and srcPos > 0 and dstPos < 65 and dstPos > 0:       
        index1 = Board.index(srcPos)  if srcPos in Board else -1   # My piece 
        index2 = Board.index(dstPos)  if dstPos in Board else -1  # My piece 
       # print(index2,move)
        if index2 != -1:          # If dstPos exists in the Board ; Then capture will be done
            index2 = Board.index(dstPos) # Get index (Piece) of the captured piece of opponent
            Board[index2] = -1           # opponent piece died
            if int(index2/16) >= 1:
                BoardBlack[index2 - 16]=-1
            else:
                BoardBlack[index2 + 16]=-1
            if int(index2/16) < 1 and int(index1/16) >= 1: # destination white - Source black 
			    # Put zero in BlackBitBoard srcPos and one in BlackBitBoard dstPos
				# Put zero in WhiteBitBoard dstPos
                WhiteBitBoard = WhiteBitBoard ^  (1<<(64-dstPos)) ;  # XOR with 1 will invert bit (originally we know it is 1) so it will be zero 
                BlackBitBoard = BlackBitBoard |  (1<<(64-dstPos)) ;  # OR With 1 will put 1 in dstPos and leave others the same 
                BlackBitBoard = BlackBitBoard ^  (1<<(64-srcPos)) ;
				
            elif int(index2/16) >= 1 and int(index1/16) < 1:# destination black - Source  white
                # Put zero in WhiteBitBoard srcPos and one in WhiteBitBoard dstPos
				# Put zero in BlackBitBoard dstPos
                WhiteBitBoard = WhiteBitBoard |  (1<<(64-dstPos)) ;  # XOR with 1 will invert bit (originally we know it is 1) so it will be zero 
                BlackBitBoard = BlackBitBoard ^  (1<<(64-dstPos)) ;  # OR With 1 will put 1 in dstPos and leave others the same 
                WhiteBitBoard = WhiteBitBoard ^  (1<<(64-srcPos)) ;
        else:				  # If dstPos doesn't exists in the board ; Then Move 
            if index1/16 < 1:
                WhiteBitBoard = WhiteBitBoard |  (1<<(64-dstPos)) ;
                WhiteBitBoard = WhiteBitBoard ^  (1<<(64-srcPos)) ;
            else:
                BlackBitBoard = BlackBitBoard |  (1<<(64-dstPos)) ; 
                BlackBitBoard = BlackBitBoard ^  (1<<(64-srcPos)) ;
				
        Board[index1] = dstPos
        if int(index1 / 16) >= 1:
            BoardBlack[index1 - 16]=dstPos
        else:
            BoardBlack[index1 + 16]=dstPos
    else:
        print('Invalid Coordinates for doMove')
        return BlackBitBoard, WhiteBitBoard, Board, BoardBlack, 0
    return BlackBitBoard, WhiteBitBoard, Board, BoardBlack, 0
def generateallmoves(move,depth): #Hager Samir
    node = namedtuple('node', ['mymove','board','boardblack','blackbitboard','whitebitboard','C_A_L','array','capture','pawn'])
    array=[]
    nodes=[]
    pieces=['R','N','B','Q','K','P']
    order=2			#number of piecies
    dicpos={'R':[],'N':[],'B':[],'Q':[],'K':[],'P':[]}#possibole moves for all pieces
    diccap={'R':[],'N':[],'B':[],'Q':[],'K':[],'P':[]}#for all possible move what it capture if not capture='-'
    if depth%2==0: #if I will play
        for piece in pieces:
            ca=move.C_A_L[:]
            boardo=move.board[:]
            boardbl=move.boardblack[:]
            if piece=='P':
                order=8
            elif piece=='Q':
                order=1
            possible,capture,pawn,cast=generateMoves(move.blackbitboard,move.whitebitboard,piece,move.C_A_L[0],move.C_A_L[1],order, boardo,boardbl)#generate move for piece
            dicpos[piece]=possible #i put possibole moves to this piece
            diccap[piece]=capture #i put if it capture any thing in this possibole move to this piece
            i=0
            if(cast==57):
                ca[1]=0
            elif cast==64:
                ca[0]=0
            elif cast==61:
                ca[1]=0
                ca[0]=0
            for move2 in possible:
                boardo=move.board[:]
                boardbl=move.boardblack[:]
                nboard=[]
                nblackbitboard,nwhitebitboard,nboard,nboardbl,cas=doMove(move.blackbitboard, move.whitebitboard, move2, boardo,boardbl)#get the new move
                print(move2)
                print(move.board)
                print(nboard)
                print(move.whitebitboard)                   
                print(nwhitebitboard)
                print(move.C_A_L)
                print(ca)
                newmove=node(move2,nboard,nboardbl,nblackbitboard,nwhitebitboard,move.C_A_L,array,capture[i],pawn)#create new node for anext move
                i=i+1
                nodes.append(newmove)
    else: #if other team play
        for piece in pieces:
            ca=move.C_A_L[:]
            boardo=move.board[:]
            boardbl=move.boardblack[:]
            if piece=='P':
                order=8
            elif piece=='Q':
                order=1
            possible,capture,pawn,cast=generateMoves(move.whitebitboard,move.blackbitboard,piece,move.C_A_L[2],move.C_A_L[3],order,boardbl, boardo)#generate move for piece
            dicpos[piece]=possible #i put possibole moves to this piece
            diccap[piece]=capture #i put if it capture any thing in this possibole move to this piece
            i=0
            if(cast==57):
                ca[1]=0
            elif cast==64:
                ca[0]=0
            elif cast==61:
                ca[1]=0
                ca[0]=0
            for move2 in possible:
                boardo=move.board[:]
                boardbl=move.boardblack[:]
                nboard=[]
                nwhitebitboard,nblackbitboard,nboardbl,nboard,cas=doMove( move.whitebitboard,move.blackbitboard, move2,boardbl, boardo)#get the new move                
                newmove=node(move2,nboard,nboardbl,nblackbitboard,nwhitebitboard,move.C_A_L,array,capture[i],pawn)#create new node for anext move
                i=i+1
                nodes.append(newmove)
    move=move._replace(array=nodes)#update father node to know its childreen

#    print (move.array)
#    print (move.boardblack)
#    print (move.blackbitboard)
#    print (move.whitebitboard)
#    print (nodes)    
    return move
def getcapture(allcap):
    capuredmove=[]
    for node in allcap:
        if node.capture!='-':
            capuredmove.append(node)
    return capuredmove
node = namedtuple('node', ['mymove','board','boardblack','blackbitboard','whitebitboard','C_A_L','array','capture','pawn'])
board,boardblack,blackbitboard,whitebitboard,Side_To_M,C_A_L,E_P_T_S,H_M_Clk,F_M_Counter,p=readFEN2Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/4K2R b KQkq e3 0 1")
#"k7/8/8/8/4Q3/8/8/4K3 w ---- - 0 1"
capture='-'
pawn=0
lastmove=node("",board,boardblack,blackbitboard,whitebitboard,C_A_L,p,capture,pawn)
#print(board)
#print(lastmove)
lastmove2=generateallmoves(lastmove,0)
#print(getcapture(lastmove2.array))
#print(E_P_T_S)
#print (board)
#print (lastmove.boardblack)
#print (lastmove.blackbitboard)
#print (lastmove.whitebitboard)
#print (lastmove2.board)
#print (lastmove2.boardblack)
#print (lastmove2.blackbitboard)
#print (lastmove2.whitebitboard)
#print (lastmove2.C_A_L)
#print (lastmove2.array)

############################# update_half move clock & full move counter
halfmove_clock=0
fullmove_counter=1
def update_half_full(piece_type,capture,Side_To_M):
    if piece_type == 1 or capture != "-":    
        halfmove_clock = 0         #  reset clock if piece is pawm or captured piece
    else:
        halfmove_clock += 1
    if Side_To_M=="b":
        fullmove_counter += 1        #  increment full move counter only after the black moves.
    return fullmove_counter,halfmove_clock 
##############################################################################################
zArray= np.zeros((2,6,64)) 
zCastle= np.zeros((4)) 
zEnPassant= np.zeros((8)) 
FileMasks8 =[]
FileMasks8.append(0x101010101010101)
FileMasks8.append(0x202020202020202)
FileMasks8.append(0x404040404040404)
FileMasks8.append(0x808080808080808)
FileMasks8.append(0x1010101010101010)
FileMasks8.append(0x2020202020202020)
FileMasks8.append(0x4040404040404040)
FileMasks8.append(0x8080808080808080)
def random64() :
    # Random bytes
    csprng = random.SystemRandom()
    # Random (probably large) integer
    random_int = csprng.getrandbits(64)
    return random_int
def getZobristHash( WP,WN, WB, WR, WQ, WK, BP,BN, BB, BR, BQ ,BK, EP, CWK, CWQ,CBK, CBQ, WhiteToMove):
        returnZKey = 0
        for square in range(64):
            if (((WP >> square) & 1) == 1):
                returnZKey |= int(zArray[0][0][square])
            elif (((BP >> square) & 1) == 1):
            
                returnZKey ^= int(zArray[1][0][square])
            
            elif (((WN >> square) & 1) == 1):
            
                returnZKey ^= int(zArray[0][1][square])
            
            elif (((BN >> square) & 1) == 1):
            
                returnZKey ^= int(zArray[1][1][square])
            
            elif  (((WB >> square) & 1) == 1):
            
                returnZKey ^= int(zArray[0][2][square])
            
            
            elif  (((BB >> square) & 1) == 1):
            
                returnZKey ^= int(zArray[1][2][square])
            
            elif  (((WR >> square) & 1) == 1):
            
                returnZKey ^= int(zArray[0][3][square])
            
            elif  (((BR >> square) & 1) == 1):
            
                returnZKey ^= int(zArray[1][3][square])
            
            elif  (((WQ >> square) & 1) == 1):
            
                returnZKey ^= int(zArray[0][4][square])
            
            elif  (((BQ >> square) & 1) == 1):
            
                returnZKey ^= int(zArray[1][4][square])
            
            elif  (((WK >> square) & 1) == 1):
            
                returnZKey ^= int(zArray[0][5][square])
            
            elif (((BK >> square) & 1) == 1):
            
                returnZKey ^= int(zArray[1][5][square])
            
        for column in range(8):
        
            if (EP ==FileMasks8[column]):
                
                returnZKey ^= int(zEnPassant[column])
            
        
        if (CWK):
            returnZKey ^= int(zCastle[0])
        if (CWQ):
            returnZKey ^= int(zCastle[1])
        if (CBK):
            returnZKey ^= int(zCastle[2])
        if (CBQ):
            returnZKey ^= int(zCastle[3])
        if (not WhiteToMove):
            returnZKey ^= zBlackMove
        return returnZKey
def zobristFillArray() :
    for colour in range(2):
        for pieceType in range(6):
                for square in range (64):
                    zArray[colour,pieceType,square] =random64()
    for column in range(8):
          zEnPassant[column]=random64()
    for index in range(4):
          zCastle[index]=random64()
    zBlackMove=random64() 

def testDistribution():   
    sampleSize = 2000;
    sampleSeconds = 10;
    startTime = int(round(time.time() * 1000))
    endTime = startTime + (sampleSeconds * 1000);
    distArray= np.zeros((sampleSize)) 
    while (int(round(time.time() * 1000))<endTime):
        for i in range(1000):
            ind=(int)((random64()% (sampleSize / 2)) + (sampleSize / 2))
            distArray[ind]=distArray[ind]+1;
            
        for k in range(sampleSize):
            print(distArray[k]) 
#zobristFillArray() 
#testDistribution()
#getZobristHash( 0,0, 0, 0, 0,0, 0,0,0, 0,0 ,0,0, 0,0,0,0, 1)


# In[ ]:



