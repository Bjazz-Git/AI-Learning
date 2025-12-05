import copy

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
    new_board = copy.deepcopy(board)

    # If the action can be taken return the board with the action taken
    if new_board[action[0]][action[1]] == EMPTY:
        new_board[action[0]][action[1]] = player(board)
        return new_board
    # Action is not valid, return an exception
    else:
        raise Exception 


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
    # Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    winner = checkWinningCombinations(board, X, O)
    if winner == X:
        return 1
    
    elif winner == O:
        return -1
    
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError

def checkWinningCombinations(board, player, opponent):
    vertical_rows = [0, 0, 0]
    player_score = 0
    winner = ""

    # Left Diagonal
    for i in range(len(board)):
        player_score += checkColumn(board, player, i, i)

    # Check if someone won through a diagonal
    winner = checkScore(player, opponent, player_score)
    if (winner is not None):
        return winner
        
    else:
        player_score = 0
    
    # Right Diagonal
    for i in range(len(board)):
        player_score += checkColumn(board, player, i, (len(board) - 1) - i)

    # Check if someone won through a diagonal
    winner = checkScore(player, opponent, player_score)
    if (winner is not None):
        return winner
        
    else:
        player_score = 0
    
    # Check Rows and Columns
    for i in range(len(board)):
        for j in range(len(board[i])):
            # If Player's symbol is in cell increase the score
            if board[i][j] == player:
                player_score += 1
                vertical_rows[j] += 1

            # If Opponent's symbol is in cell decrease the score
            elif board[i][j] == opponent:
                player_score -= 1
                vertical_rows[j] -= 1

        # Check if someone won through rows
        winner = checkScore(player, opponent, player_score)
        if (winner is not None):
            return winner
        else:
            player_score = 0

    # Check if someone won through vertical rows
    for row in vertical_rows:
        winner = checkScore(player, opponent, row)
        if (winner is not None):
            return winner
    
    # If this line was reached then no one has won yet
    return None
        

# Returns a number representing who has their symbol in a cell
def checkColumn(board, player, row, column):
    if (board[row][column] == player):
        return 1

    elif(board[row][column] != EMPTY):
        return -1
    
    else:
        return 0

# Checks to see if someone has one for a specific combination    
def checkScore(player, opponent, player_score):
    if (player_score == 3):
        return player
    
    elif (player_score == -3):
        return opponent
    
    else:
        return None




        
        



            


