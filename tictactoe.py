"""
Tic Tac Toe Player
"""

import math

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

# Returns the player who's turn it is
def player(board):
    x_moves = 0
    o_moves = 0

    # Get the number of x and o moves on the board
    for row in board:
        for cell in range(len(row)):
            if row[cell] == X:
                x_moves += 1
            
    
            elif row[cell] == O:
                o_moves += 1

    # Compare the number of x moves and o moves
    # If equal amount of moves then it's x's turn
    if (x_moves == o_moves):
        return X
    
    # Else it's o's turn
    else:
        return O

# Returns all cells in which a move can be made on
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Set to store valid positions
    valid_moves = set()

    # Loop through board to find all EMPTY cells
    for row in board:
        for cell in range(board):
            if (row[cell] == EMPTY):
                valid_moves.add((row, cell))        

    # Return valid positions
    return valid_moves


def result(board, action):
    # Return a copy of the board with the action being taken (shouldn't affect the actual board)

    # If the action is not valid return an exception
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
