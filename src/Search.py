from defs import * 
from MoveGeneration import *

def Evaluation():
    # Need to be added!!
    return 0

def alphaBeta(board, alpha, beta, depth, player):
        if depth <= 0:
            return Evaluation()

        move_list = generateMoves(board)  # Need to be updated in accordance to the actual move function!!
        for move in move_list:
            # doMove()
            current_eval = -alphaBeta(board,-beta, -alpha, depth - 1, -player)
            # UndoMove() ??

            if current_eval >= beta:
                return beta

            if current_eval > alpha:
                alpha = current_eval

        return alpha


def Search(board, depth, player):
    best_move = None
    max_eval = float('-infinity')

    move_list = generateMoves(board)  # Need to be updated in accordance to the actual move function!!
    alpha = float('infinity')
    for move in move_list:
        # doMove()
        alpha = -alphaBeta(board, float('-infinity'), alpha, depth - 1, -player)
        # UndoMove ??

        if alpha > max_eval:
            max_eval = alpha
            best_move = move

    return best_move
