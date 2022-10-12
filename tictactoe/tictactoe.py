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
    none_count = 0
    # Looping over the board
    for row in board:
        for col in row:
            if col == None:
                none_count += 1
    # A nice ternary to make things look cool
    return "X" if none_count == 9 else "O" if (none_count % 2) == 0 else "X"


def actions(board):
    actions = set()
    for i in range(len(board)):
        for x in range(len(board[0])):
            if board[i][x] == None:
                actions.add((i, x))
    return actions


def result(board, action):
    # This will create a deepcopy of the board
    # Therefore %ifying it wouldn't have any impact on the board
    board_copy = [row[:] for row in board]
    if board_copy[action[0]][action[1]]:
        raise RuntimeError('Invalid action !')
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checking horizontally
    for i in board:
        h_counter = 0
        prev_x = 0
        for x in i:
            if x == prev_x and x:
                h_counter += 1
            prev_x = x
        if h_counter == 2:
            return prev_x

    # Checking vertically
    for i in range(len(board)):
        v_counter = 0
        prev_x = 0
        for x in range(len(board)):
            if board[x][i] == prev_x and board[x][i]:
                v_counter += 1
            prev_x = board[x][i]
        if v_counter == 2:
            return prev_x

    # Checking Diagonally
    i_counter = 0
    i_prev = 0
    x = len(board) - 1 # Starting from the right corner
    x_counter = 0
    x_prev = 0
    for i in range(len(board)):
        if board[i][i] == i_prev:
            i_counter += 1
        if board[i][x] == x_prev:
            x_counter += 1
        i_prev = board[i][i]
        x_prev = board[i][x]
        x -= 1
    return i_prev if i_counter == 2 else x_prev if x_counter == 2 else None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not winner(board):
        for i in board:
            for x in i:
                if not x:
                    return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    return 1 if w == "X" else -1 if w == "O" else 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def max_value(board):
        if terminal(board):
            return utility(board)
        v = - 10
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = 10
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    if terminal(board):
        return None

    if player(board) == "X":
        if board == initial_state():
            return (0, 0)
        # In this case, the boundaries are -1 and 1
        # Having a -10 and a 10 and lowest and highest are enough
        v = -10
        next_action = None
        for action in actions(board):
            # comp the min_value
            min_v = min_value(result(board, action))
            if min_v > v:
                v = min_v
                next_action = action
        return next_action
    else:
        v = 10
        optimal_a = None
        for action in actions(board):
            max_v = max_value(result(board, action))
            if max_v < v:
                v = max_v
                optimal_a = action
        return optimal_a
