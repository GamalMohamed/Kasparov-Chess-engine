
# coding: utf-8

# In[6]:




# In[3]:

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
    mylist = ["P","P","P","P","P","P","P","P","R","N","B","Q","K","B","N","R","p","p","p","p","p","p","p","p","r","n","b","q","k","b","n","r"]
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


# In[ ]:





# In[ ]:




# In[ ]:



