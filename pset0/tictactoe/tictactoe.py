"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    aantalX = 0
    aantalO = 0
    for rows in board:
        for item in rows:
            if item == X:
                aantalX += 1
            if item == O:
                aantalO += 1

    if aantalX == aantalO:
        return X
    if aantalX > aantalO:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    PossibleMoves=[]
    for i, rows in enumerate(board):
        for j,item in enumerate(rows):
            if item == None:
                PossibleMoves.append((i,j))
                
    return PossibleMoves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    P = player(board)
    newBoard = []
    newBoard = copy.deepcopy(board)

    if action in actions(board):
        i = action[0]
        j = action[1]
        newBoard[i][j] = P

        return newBoard
    else:
        raise Exception("This action is invalid")



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check horizontale wins
    for i, rows in enumerate(board):
        aantalX = 0
        aantalO = 0

        for j, items in enumerate(rows):
            if board[i][j] == X:
                aantalX += 1
            elif board[i][j] == O:
                aantalO += 1

        if aantalX == 3:
            return X
        if aantalO == 3:
            return O
    
    # Check verticale wins
    for i, rows in enumerate(board):
        aantalX = 0
        aantalO = 0

        for j, items in enumerate(rows):
            if board[j][i] == X:
                aantalX += 1
            elif board[j][i] == O:
                aantalO += 1

        if aantalX == 3:
            return X
        if aantalO == 3:
            return O

    # Check diagonale wins pt1
    aantalX = 0
    aantalO = 0
    for i, rows in enumerate(board):
        

        if board[i][i] == X:
                aantalX += 1
        elif board[i][i] == O:
                aantalO += 1

    if aantalX == 3:
            return X
    if aantalO == 3:
            return O

    # Check diagonale wins pt2
    aantalX = 0
    aantalO = 0

    for i, rows in enumerate(board):
        if board[3-i-1][i] == X:
                aantalX += 1
        elif board[3-i-1][i] == O:
                aantalO += 1

    if aantalX == 3:
            return X
    if aantalO == 3:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    filled = True
    if winner(board) is not None:
        return True
    else:
        for row in board:
            for item in row:
                if item is EMPTY:
                    filled = False
        return filled


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    WIN = winner(board)

    if WIN == X:
        return 1
    elif WIN == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
            return None

    currentPlayer = player(board)
    OptimalScore = -2
    MinimalScore = 2
    nextMove = None

    
    for moves in actions(board):
        newBoard = result(board, moves)
        if currentPlayer == X:
            NewScore = MinMove(newBoard)
            if NewScore > OptimalScore:
                OptimalScore = NewScore
                nextMove = moves
        else:
            NewScore = MaxMove(newBoard)
            if NewScore < MinimalScore:
                MinimalScore = NewScore                    
                nextMove = moves
        
    return nextMove

def MinMove(board):

    if terminal(board):
            return utility(board)

    MinimalScore = 2
    

    for moves in actions(board):
        newBoard = result(board, moves)
        NewScore = MaxMove(newBoard)    
        MinimalScore = min(NewScore, MinimalScore)

    
    return MinimalScore

def MaxMove(board):

    if terminal(board):
            return utility(board)

    OptimalScore = -2

    for moves in actions(board):
        newBoard = result(board, moves)
        NewScore = MinMove(newBoard)
        OptimalScore = max(NewScore, OptimalScore)

    return OptimalScore


