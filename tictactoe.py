"""
Tic Tac Toe Player
"""

import copy
import math
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board: list[list]):
    """
    Returns player who has the next turn on a board.
    """

    # In the initial game state, X gets the first move.
    if board == initial_state():
        return X

    if terminal(board):
        return None

    count_of_x = sum(row.count(X) for row in board)
    count_of_o = sum(row.count(O) for row in board)
    if count_of_x <= count_of_o:
        return X
    else:
        return O


def actions(board: list[list]):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    default: set[tuple[int, int]] = set()
    if terminal(board):
        return default

    possible_actions = {
        (row_idx, col_idx)
        for row_idx, row in enumerate(board)
        for col_idx, value in enumerate(row)
        if value is EMPTY
    }
    return possible_actions


def result(board: list[list], action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise ValueError("Impossible move detected")

    player_piece = player(board)
    if player_piece is None:
        raise ValueError("Impossible move detected")

    new_board = copy.deepcopy(board)

    new_board[action[0]][action[1]] = player_piece

    return new_board


def winner(board: list[list]):
    """
    Returns the winner of the game, if there is one.
    """
    n = len(board)

    # Check rows for all 'X' or all 'O'
    for row in board:
        if all(cell == X for cell in row):
            return X
        if all(cell == O for cell in row):
            return O

    # Check columns for all 'X' or all 'O'
    for col in range(n):
        column = [board[row][col] for row in range(n)]
        if all(cell == X for cell in column):
            return X
        if all(cell == O for cell in column):
            return O

    # Check left diagonal (top-left to bottom-right) for all 'X' or all 'O'
    left_diag = [board[i][i] for i in range(n)]
    if all(cell == X for cell in left_diag):
        return X
    if all(cell == O for cell in left_diag):
        return O

    # Check right diagonal (top-right to bottom-left) for all 'X' or all 'O'
    right_diag = [board[i][n - i - 1] for i in range(n)]
    if all(cell == X for cell in right_diag):
        return X
    if all(cell == O for cell in right_diag):
        return O

    # If no winning line is found
    return None


def terminal(board: list[list]):
    """
    Returns True if game is over, False otherwise.
    """

    if board == initial_state():
        return False

    game_ended = False

    # check if there is a winner via any row
    for row in board:
        if not game_ended:
            game_ended = None not in row and all(x == row[0] for x in row)

    # check  if there is a winner via any column
    for col in range(len(board[0])):
        if not game_ended:
            column = [row[col] for row in board]
            game_ended = None not in column and all(x == column[0] for x in column)

    # check if there is a winner via any diagonal
    if not game_ended:
        n = len(board)
        left_diag = [board[i][i] for i in range(n)]
        right_diag = [board[i][n - i - 1] for i in range(n)]
        game_ended = None not in left_diag and all(x == left_diag[0] for x in left_diag)
        if not game_ended:
            game_ended = None not in right_diag and all(
                x == right_diag[0] for x in right_diag
            )

    # check if there a stalmate. (when there are no moves on the board again)
    if not game_ended:
        game_ended = all(value in (X, O) for row in board for value in row)

    return game_ended


def utility(board: list[list]):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    n = len(board)

    # Check rows for all 'X' or all 'O'
    for row in board:
        if all(cell == X for cell in row):
            return 1
        if all(cell == O for cell in row):
            return int(-1)

    # Check columns for all 'X' or all 'O'
    for col in range(n):
        column = [board[row][col] for row in range(n)]
        if all(cell == X for cell in column):
            return 1
        if all(cell == O for cell in column):
            return -1

    # Check left diagonal (top-left to bottom-right) for all 'X' or all 'O'
    left_diag = [board[i][i] for i in range(n)]
    if all(cell == X for cell in left_diag):
        return 1
    if all(cell == O for cell in left_diag):
        return -1

    # Check right diagonal (top-right to bottom-left) for all 'X' or all 'O'
    right_diag = [board[i][n - i - 1] for i in range(n)]
    if all(cell == X for cell in right_diag):
        return 1
    if all(cell == O for cell in right_diag):
        return -1

    # If no winning line is found
    return 0


def minimax(board: list[list]):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # return a random action for initial state
    if board == initial_state():
        return random.choice(list(actions(board)))

    current_player = player(board)
    if current_player is X:
        _, action = maximizing_action(board, alpha=float("-inf"), beta=float("inf"))
        return action
    elif current_player is O:
        _, action = minimizing_action(board, alpha=float("-inf"), beta=float("inf"))
        return action


def maximizing_action(board: list[list], alpha: float, beta: float):
    """
    Returns the maximum utility value and the best action for the maximizing player.
    """
    if terminal(board):
        return utility(board), None  # Base case: return the utility and no action

    v = float("-inf")
    best_action = None
    for action in actions(board):
        max_result, _ = minimizing_action(result(board, action), alpha, beta)
        v, best_action = (max_result, action) if max_result > v else (v, best_action)
        alpha = max(alpha, v)
        if beta <= alpha:  # Prune the branch
            break
    return v, best_action


def minimizing_action(board: list[list], alpha: float, beta: float):
    """
    Returns the minimum utility value and the best action for the minimizing player.
    """
    if terminal(board):
        return utility(board), None  # Base case: return the utility and no action

    v = float("inf")
    best_action = None
    for action in actions(board):
        max_result, _ = maximizing_action(result(board, action), alpha, beta)
        v, best_action = (max_result, action) if max_result < v else (v, best_action)
        beta = min(beta, v)
        if beta <= alpha:  # Prune the branch
            break
    return v, best_action
