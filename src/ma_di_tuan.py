import time 
BOARD_SIZE = 8

def is_safe(x, y, board):

    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == -1

def print_solution(board):

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            print(f"{board[i][j]:2d}", end=" ")
        print()

def solve_kt_util(x, y, move_i, board, x_move, y_move):
    """
    Hàm đệ quy quay lui để giải bài toán Mã đi tuần.
    Args:
        x (int): Tọa độ hàng hiện tại.
        y (int): Tọa độ cột hiện tại.
        move_i (int): Số thứ tự bước đi hiện tại (từ 1 đến BOARD_SIZE*BOARD_SIZE).
        board (list[list[int]]): Bàn cờ lưu trữ các bước đi.
        x_move (list[int]): Các thay đổi tọa độ x cho 8 nước đi của quân Mã.
        y_move (list[int]): Các thay đổi tọa độ y cho 8 nước đi của quân Mã.
    Returns:
        bool: True nếu tìm thấy lời giải từ vị trí này, False nếu không.
    """
    # Nếu đã đi hết tất cả các ô
    if move_i == BOARD_SIZE * BOARD_SIZE:
        return True

    # Thử tất cả các nước đi tiếp theo từ vị trí (x, y) hiện tại
    for k in range(8):
        next_x = x + x_move[k]
        next_y = y + y_move[k]
        if is_safe(next_x, next_y, board):
            board[next_x][next_y] = move_i # Đánh dấu bước đi
            # Gọi đệ quy cho nước đi tiếp theo
            if solve_kt_util(next_x, next_y, move_i + 1, board, x_move, y_move):
                return True
            else:
                # Nếu đi tiếp không thành công, quay lui (backtrack)
                board[next_x][next_y] = -1 # Bỏ đánh dấu
    return False

def solve_knights_tour(board_size=8):
   
    global BOARD_SIZE
    BOARD_SIZE = board_size 

    board = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    x_move = [2, 1, -1, -2, -2, -1, 1, 2]
    y_move = [1, 2, 2, 1, -1, -2, -2, -1]


    start_x, start_y = 0, 0
    board[start_x][start_y] = 0 

    if not solve_kt_util(start_x, start_y, 1, board, x_move, y_move):
        print("Không tìm thấy lời giải")
        return None
    else:
        print("Tìm thấy lời giải!")

        path = [None] * (BOARD_SIZE * BOARD_SIZE)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] != -1: 
                    path[board[r][c]] = (r, c) 

        if None in path:
             print("Lỗi: Đường đi trích xuất không đầy đủ.")
             return None 

        return path 

if __name__ == '__main__':
    print(f"Bắt đầu giải Mã đi tuần cho bàn cờ {BOARD_SIZE}x{BOARD_SIZE}...")
    start_time = time.time()
    solution_path = solve_knights_tour(BOARD_SIZE)
    end_time = time.time()

    if solution_path:
        print(f"\nĐường đi tìm được (danh sách tọa độ (hàng, cột)):")
        print(solution_path[:10], "...")
        print(f"\nTổng số bước: {len(solution_path)}")
    print(f"Thời gian giải: {end_time - start_time:.4f} giây")
