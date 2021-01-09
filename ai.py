import random
from copy import deepcopy
from operator import sub



opponent = {'w': 'b', 'b': 'w'}


# Get all checkers' position for one color
def get_checkers(board, color):
    result = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == color:
                result.append((i, j))
            if board[i][j] == color.isupper():
                result.append((i,j))
    return result

# If a piece is King
def is_king(piece):
    return piece.isupper()

def allowed_moves(board, color):
    result = []
    board = deepcopy(board)
    checkers = get_checkers(board, color)
    for checker in checkers:
        row = checker[0]
        col = checker[1]
        left = col-1
        right = col+1
        if color == 'w' or is_king(board[row][col]):
            left_result = _traverse_left(board, row - 1, max(row - 3, -1), -1, board[row][col], left)
            right_result = _traverse_right(board, row - 1, max(row - 3, -1), -1, board[row][col], right)
            left_result.insert(0, checker)
            result.append(left_result)
            right_result.insert(0, checker)
            result.append(right_result)
        if color == 'b' or is_king(board[row][col]):
            left_result = _traverse_left(board, row + 1, min(row + 3, 8), 1, board[row][col], left)
            right_result = _traverse_right(board, row + 1, min(row + 3, 8), 1, board[row][col], right)
            left_result.insert(0, checker)
            result.append(left_result)
            right_result.insert(0, checker)
            result.append(right_result)
    result = list(filter(lambda move: len(move) > 1, result))
    return result

def _traverse_left(board, start, stop, step, color, left, skipped =[]):
    moves = []
    last = []
    for r in range(start, stop, step):
        if left < 0:
            break
        current = board[r][left]
        if current == '_':
            if skipped:
                moves.append(skipped)
                moves.append((r, left))
            else:
                moves.append((r, left))
            if last:
                if step == -1:
                    row = max(r-3, 0)
                else:
                    row = min(r+3, 8)
                _traverse_left(board, r+step, row, step, color, left-1, skipped=last)
                _traverse_right(board, r+step, row, step, color, left+1, skipped=last)
            break
        elif current == color:
            break
        else:
            last = [current]
        left -= 1
    return moves

def _traverse_right(board, start, stop, step, color, right, skipped=[]):
    moves = []
    last = []
    for r in range(start, stop, step):
        if right >= 8:
            break
        current = board[r][right]
        if current == '_':
            if skipped:
                moves.append(skipped)
                moves.append((r, right))
            else:
                moves.append((r, right))
            if last:
                if step == -1:
                    row = max(r-3, 0)
                else:
                    row = min(r+3, 8)
                _traverse_left(board, r+step, row, step, color, right - 1, skipped=last)
                _traverse_right(board, r+step, row, step, color, right + 1, skipped=last)
            break
        elif current == color:
            break
        else:
            last = [current]
        right += 1
    return moves

def play(board, color):
    """
        Play must return the next move to play.
        You can define here any strategy you would find suitable.
    """

    # value, best_move = maxValue(board, 3, color)
    # return best_move
    return random_play(board, color)

# If there's capture move, return capture move
# Else return random allowed move
def random_play(board, color):
    """
        An example of play function based on allowed_moves.
    """
    moves = allowed_moves(board, color)
    capture_move = find_capture(moves)
    if capture_move:
        return capture_move
    # There will always be an allowed move
    # because otherwise the game is over and
    # 'play' would not be called by main.py
    else:
        return random.choice(moves)

def find_capture(moves):
    for move in moves:
        first_tuple_elements = [a_move[0] for a_move in move]
        difference = sub(first_tuple_elements[0], first_tuple_elements[1])
        if abs(difference) > 1:
            return move

def evaluate(board, maxplayer):
    return board.count(maxplayer) - board.count(opponent.get(maxplayer)) + (board.count(maxplayer.upper()) * 0.5 - board.count(opponent.get(maxplayer).upper()) * 0.5)

# Get boards by simulating all possible moves
def get_all_moves(board, color):
    moves = []
    boards = []
    valid_moves = allowed_moves(board, color)
    for move in valid_moves:
        piece = move[0]
        temp_board = deepcopy(board)
        temp_piece = (piece[0], piece[1])
        new_board = simulate_move(temp_piece, move, temp_board)
        boards.append(new_board)
        moves.append(move)
    return boards, moves

def maxValue(board, depth, maxplayer):
    if depth == 0:
        return evaluate(board, maxplayer), board

    maxEval = float('-inf')
    best_move = None
    states, moves = get_all_moves(board, maxplayer)
    captured = find_capture(moves)
    if captured:
        return maxEval, captured
    for state in states:
        for move in moves:
            evaluation = minValue(state, depth-1, opponent.get(maxplayer))[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
    return maxEval, best_move

def minValue(board, depth, minplayer):
    if depth == 0:
        return evaluate(board, minplayer), board

    minEval = float('inf')
    best_move = None
    states, moves = get_all_moves(board, minplayer)
    captured = find_capture(moves)
    if captured:
        return minEval, captured
    for state in states:
        for move in moves:
            evaluation = maxValue(state, depth-1, opponent.get(minplayer))[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
    return minEval, best_move

def simulate_move(piece, move, board):
    destination = move[-1]
    row = piece[0]
    col = piece[1]
    destination_row = destination[0]
    destination_col = destination[1]
    toMove = board[row][col]
    first_tuple_elements = [a_move[0] for a_move in move]
    difference = sub(first_tuple_elements[0], first_tuple_elements[1])
    if abs(difference) > 1:
        board = new_board(board, col, row, (col + destination_col)//2, (row + destination_row)// 2, '_' )
    board = new_board(board, col, row, destination_col, destination_row, toMove)
    return board

def new_board(board, old_col, old_row, new_col, new_row, toMove):
    str1 = board[new_row]
    str2 = board[old_row]
    list1 = list(str1)
    list2 = list(str2)
    list1[new_col] = toMove
    str1 = ''.join(list1)
    list2[old_col] = '_'
    str2 = ''.join(list2)
    board[new_row] = str1
    board[old_row] = str2
    return board