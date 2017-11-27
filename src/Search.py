from defs import * 
from MoveGeneration import *

visited_nodes = 0

def ProbePvTable():
    return 0

def StorePvMove(move):
    return 0


def Quiescence(alpha, beta):
    return 0

def AplhaBeta(alpha, beta, depth):
    if depth <= 0:
        return Quiescence(alpha,beta)
    
    visited_nodes+=1

    # Check for repitition & 50 move (need to add history table!)
    # Check if reached max depth
    # ?

    moveslist = generateMoves()
    bestMove = NOMOVE
    score = -INFINITE
    OldAlpha = alpha

    PvMove = ProbePvTable()
	#if PvMove != NOMOVE:
		# Check if move in PV table
	
    for move in moveslist:
        # PickNextMove()
        score = -AlphaBeta(-beta, -alpha, depth - 1) 
        if score > alpha:
            if score >= beta:
                return beta
            # fetch history table
            alpha = score
            bestMove = move 
       
        if alpha != OldAlpha:
            StorePvMove(BestMove)
    return alpha


def SearchPosition():
    bestMove = NOMOVE
    bestScore = -INFINITE
    score = -INFINITE

    # Clear_for_search()

    # Iterative Deepening
    for currentDepth in range(FIXEDDEPTH):
        score = AplhaBeta(-INFINITE, INFINITE, currentDepth)
        
        bestScore = score

        bestMove = ProbePvTable()

    return bestMove

