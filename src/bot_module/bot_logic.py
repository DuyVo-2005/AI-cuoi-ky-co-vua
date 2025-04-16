import chess
import numpy as np
import random

# Pawn positional score
pawn_score = np.array([
    [90,  90,  90,  90,  90,  90,  90,  90],   
    [30,  30,  30,  40,  40,  30,  30,  30],   
    [20,  20,  20,  30,  30,  30,  20,  20],   
    [10,  10,  10,  20,  20,  10,  10,  10],   
    [5,   5,  10,  20,  20,   5,   5,   5],   
    [0,   0,   0,   5,   5,   0,   0,   0],   
    [0,   0,   0, -10, -10,   0,   0,   0],   
    [0,   0,   0,   0,   0,   0,   0,   0]    
])

# Knight positional score
knight_score = np.array([
    [-5,   0,   0,   0,   0,   0,   0,  -5],   
    [-5,   0,   0,  10,  10,   0,   0,  -5],   
    [-5,   5,  20,  20,  20,  20,   5,  -5],   
    [-5,  10,  20,  30,  30,  20,  10,  -5],   
    [-5,  10,  20,  30,  30,  20,  10,  -5],   
    [-5,   5,  20,  10,  10,  20,   5,  -5],   
    [-5,   0,   0,   0,   0,   0,   0,  -5],   
    [-5, -10,   0,   0,   0,   0, -10,  -5]    
])

# Bishop positional score
bishop_score = np.array([
    [ 0,   0,   0,   0,   0,   0,   0,   0],   
    [ 0,   0,   0,   0,   0,   0,   0,   0],   
    [ 0,   0,   0,  10,  10,   0,   0,   0],   
    [ 0,   0,  10,  20,  20,  10,   0,   0],   
    [ 0,   0,  10,  20,  20,  10,   0,   0],   
    [ 0,  10,   0,   0,   0,   0,  10,   0],   
    [ 0,  30,   0,   0,   0,   0,  30,   0],   
    [ 0,   0, -10,   0,   0, -10,   0,   0]    
])

# Rook positional score
rook_score = np.array([
    [50,  50,  50,  50,  50,  50,  50,  50],   
    [50,  50,  50,  50,  50,  50,  50,  50],   
    [ 0,   0,  10,  20,  20,  10,   0,   0],   
    [ 0,   0,  10,  20,  20,  10,   0,   0],   
    [ 0,   0,  10,  20,  20,  10,   0,   0],   
    [ 0,   0,  10,  20,  20,  10,   0,   0],
    [ 0,   0,  10,  20,  20,  10,   0,   0],   
    [ 0,   0,   0,  20,  20,   0,   0,   0]  
])

# King positional score
king_score = np.array([
    [0,   0,   0,   0,   0,   0,   0,   0],   
    [0,   0,   5,   5,   5,   5,   0,   0],   
    [0,   5,   5,  10,  10,   5,   5,   0],   
    [0,   5,  10,  20,  20,  10,   5,   0],   
    [0,   5,  10,  20,  20,  10,   5,   0],   
    [0,   0,   5,  10,  10,   5,   0,   0],   
    [0,   5,   5,  -5,  -5,   0,   5,   0],   
    [0,   0,   5,   0, -15,   0,  10,   0]    
])

piece_values = {
    chess.PAWN: 100.0,
    chess.KNIGHT: 300.0,
    chess.BISHOP: 350.0,
    chess.ROOK: 500.0,
    chess.QUEEN: 900.0,
    chess.KING: 10000.0  # Không dùng trong đánh giá vì vua không bị bắt
}

'''Hàm chuyển tọa độ uci của ô thành tọa độ index'''
def uci_square_to_index(uci_square):
    square = chess.parse_square(uci_square)
    row, col = divmod(square, 8)
    
    row = 7 - row
    return (row, col)
'''Hàm lấy giá trị của quân cờ dựa trên loại quân cờ và vị trí của nó'''
def value_of(piece:chess.Piece, _row, _col):
    sign = (1 if piece.color == chess.WHITE else -1)
    row = (_row if piece.color == chess.WHITE else 7 - _row)
    col = _col

    if piece.piece_type == 1:
        # Quân Pawn
        return (piece_values[chess.PAWN] + pawn_score[row][col]) * sign
    elif piece.piece_type == 2:
        # Quân Knight
        return (piece_values[chess.KNIGHT] + king_score[row][col]) * sign
    elif piece.piece_type == 3:
        # Quân Bishop
        return (piece_values[chess.BISHOP] + bishop_score[row][col]) * sign
    elif piece.piece_type == 4:
        # Quân Rook
        return (piece_values[chess.ROOK] + rook_score[row][col]) * sign
    elif piece.piece_type == 5:
        # Quân Queen
        return (piece_values[chess.QUEEN]) * sign
    elif piece.piece_type == 6:
        # Quân King
        return (piece_values[chess.KING]) * sign



# Hàm Evaluate
# Hàm đánh giá vị trí của bàn cờ
def evaluate_board(board:chess.Board):
    """
    Đánh giá bàn cờ dựa trên giá trị quân cờ.
    - Dương nếu lợi thế cho trắng, âm nếu lợi thế cho đen.
    """

    # 
    
    eval_score = 0.0
    
    for piece in piece_values:
        eval_score += len(board.pieces(piece, chess.WHITE)) * piece_values[piece]
        eval_score -= len(board.pieces(piece, chess.BLACK)) * piece_values[piece]

    # # Duyệt qua từng ô
    # for square in chess.SQUARES:
    #     piece = board.piece_at(square)
    #     if piece:  # Nếu ô đó có quân cờ
    #         uci_square = chess.square_name(square)
    #         index = uci_square_to_index(uci_square)
    #         eval_score += value_of(piece, index[0], index[1])
    
    return eval_score

# Hàm Search
# Thuật toán Minimax với cắt tỉa Alpha-Beta
def minimax(board:chess.Board, depth, alpha, beta, maximizing_player, count):
    """
    Triển khai thuật toán Minimax với cắt tỉa Alpha-Beta.
    - depth: Độ sâu tối đa của thuật toán.
    - alpha: Giá trị tốt nhất của người chơi tối ưu.
    - beta: Giá trị tốt nhất của đối thủ.
    - maximizing_player: True nếu là lượt của Trắng, False nếu là lượt của Đen.
    """
    count[0] += 1

    if depth == 0:
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False, count)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Cắt tỉa beta
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True, count)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Cắt tỉa alpha
        return min_eval



'''
    ===============================================================
    ===============================================================
    Hàm chính, nhận chess.Board, trả về 1 chess.Move
'''
# Chọn nước đi tốt nhất bằng Minimax
def find_best_move(board, depth=3):

    best_move = None
    best_value = float('-inf') if board.turn == chess.WHITE else float('inf')

    count = [0]

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth, float('-inf'), float('inf'), not board.turn, count)
        board.pop()

        if (board.turn == chess.WHITE and board_value > best_value) or (board.turn == chess.BLACK and board_value < best_value):
            best_value = board_value
            best_move = move

    print("count:", count[0])

    return best_move
