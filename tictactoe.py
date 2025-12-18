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


def player(board):
    # Returns the player who's turn it is
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


def actions(board):
    # Returns all cells in which a move can be made on
    # Set to store valid positions
    valid_moves = set()

    # Loop through board to find all EMPTY cells
    for row in range(len(board)):
        for cell in range(len(board[row])):
            if (board[row][cell] == EMPTY):
                valid_moves.add((row, cell))        

    # Return valid positions
    if len(valid_moves) > 0:
        return valid_moves
    else:
        return None


def result(board, action):
    # Return a copy of the board with the action being taken (shouldn't affect the actual board)
    new_board = copy.deepcopy(board)

    # If the row is invalid, return an exception
    if (action[0] >= 0 and action[0] <= 2) is not True:
        raise Exception
    
    # If the column is invalid, return an exception
    if (action[1] >= 0 and action[1] <= 2) is not True:
        raise Exception

    # If the action can be taken return the board with the action taken
    if new_board[action[0]][action[1]] == EMPTY:
        new_board[action[0]][action[1]] = player(board)
        return new_board
    # Action is not valid, return an exception
    else:
        raise Exception 


def winner(board):
    winner = utility(board)

    if winner == 1:
        return X
    
    elif winner == -1:
        return O
    
    else:
        return None
# Returns the winner of the game, if there is one.

# Returns True if game is over, False otherwise.


def terminal(board):
    winner = check_for_winner(board)

    # If someone won the game, return true
    if winner is not None:
        return True

    # Get the possible moves from the board
    moves = actions(board)

    # If there are no more moves left then there is a tie, return true
    if moves is None:
        return True
    
    # If this line is reached then the game isn't over, return false
    return False


def utility(board):
    # Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    winner = check_for_winner(board)
    if winner == X:
        return 1
    
    elif winner == O:
        return -1
    
    else:
        return 0
    

def minimax(board):
    p = player(board)

    highest_score = 0
    best_move = ()
    if p == X:
        highest_score = -1
    else:
        highest_score = 1

    for action in actions(board):
        new_board = copy.deepcopy(board)
        new_board[action[0]][action[1]] = p
        score = get_optimal_action(new_board)
        if p == X:
            if score > highest_score:
                highest_score = score
                best_move = action  
        else:
            if score < highest_score:
                highest_score = score
                best_move = action

    if len(best_move) != 0:
        return best_move
    else:
        return None  


def get_optimal_action(board):
    if terminal(board):
        return utility(board)
    
    p = player(board)
    
    highest_score = 0
    if p == X:
        highest_score = -1
    else:
        highest_score = 1

    for action in actions(board):
        new_board = copy.deepcopy(board)
        new_board[action[0]][action[1]] = p

        if p == X:
            highest_score = max(highest_score, get_optimal_action(new_board))
        else:
            highest_score = min(highest_score, get_optimal_action(new_board))
    
    return highest_score


def check_for_winner(board):
    # Returns the winner, if there is one
    player_score = 0
    vertical_rows = [0, 0, 0]
    winner = ""

    # Checks for winner in rows and vertical rows
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                player_score += 1
                vertical_rows[j] += 1

            elif board[i][j] == O:
                player_score -= 1
                vertical_rows[j] -= 1

        # Check if there is a winner in the current row
        winner = check_score(player_score)
        if winner is not None:
            return winner
        # If there was no winner for that row reset the score
        player_score = 0

    # Check if anyone won through vertical rows
    for i in range(len(vertical_rows)):
        winner = check_score(vertical_rows[i])
        if winner is not None:
            return winner

    # Checks the left diagonal in the board
    winner = check_diagonals(board, 0, 0)
    if winner is not None:
        return winner

    # Checks the right diagonal in the board
    winner = check_diagonals(board, 0, 2)
    if winner is not None:
        return winner

    # If this line is reached then there are no winners
    return None


# Returns a number representing who has their symbol in a cell
def check_column(board, row, column):
    if board[row][column] == X:
        return 1

    elif board[row][column] == O:
        return -1

    else:
        return 0


# Checks to see if someone has won for a specific combination
def check_score(player_score):
    if player_score == 3:
        return X

    elif player_score == -3:
        return O

    else:
        return None


# Checks a diagonal on the board
def check_diagonals(board, row, column):
    player_score = 0
    row_change = 1
    column_change = 0

    # If they are the same then this is a left diagonal
    if row == column:
        column_change = 1

    # If they are not the same this is a right diagonal
    else:
        column_change = -1

    # Checks a diagonal on the board
    for i in range(3):
        player_score += check_column(board, row, column)
        row += row_change
        column += column_change

    # Check if someone won through left diagonal
    winner = check_score(player_score)
    if winner is not None:
        return winner
    else:
        return None