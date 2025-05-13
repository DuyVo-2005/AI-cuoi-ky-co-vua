import time
import heapq 

BOARD_SIZE = 8

x_move = [2, 1, -1, -2, -2, -1, 1, 2]
y_move = [1, 2, 2, 1, -1, -2, -2, -1]

def is_safe(x, y, board_size):
    return 0 <= x < board_size and 0 <= y < board_size

def solve_kt_util(x, y, move_i, board, x_move, y_move, board_size):
    if move_i == board_size * board_size:
        return True

    for k in range(8):
        next_x = x + x_move[k]
        next_y = y + y_move[k]
        if 0 <= next_x < board_size and 0 <= next_y < board_size and board[next_x][next_y] == -1:
            board[next_x][next_y] = move_i
            if solve_kt_util(next_x, next_y, move_i + 1, board, x_move, y_move, board_size):
                return True
            board[next_x][next_y] = -1
    return False


def solve_knights_tour_backtracking(board_size=8):
    board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
    start_x, start_y = 0, 0
    board[start_x][start_y] = 0

    if not solve_kt_util(start_x, start_y, 1, board, x_move, y_move, board_size):
        return None
    else:
        path = [None] * (board_size * board_size)
        for r in range(board_size):
            for c in range(board_size):
                if board[r][c] != -1:
                    path[board[r][c]] = (r, c)
        return path
def heuristic(visited_count, board_size):
    return (board_size * board_size) - visited_count
def coords_to_index(r, c, board_size):
    return r * board_size + c

def index_to_coords(index, board_size):
    return (index // board_size, index % board_size)

def count_set_bits(mask):
    count = 0
    while mask > 0:
        mask &= (mask - 1)
        count += 1
    return count

def solve_knights_tour_a_star(board_size=8):
    total_cells = board_size * board_size
    open_set = []
    g_score = {}
    came_from = {}
    start_row, start_col = 0, 0
    start_mask = 1 << coords_to_index(start_row, start_col, board_size)
    start_g = 0
    start_h = heuristic(1, board_size)
    start_f = start_g + start_h

    start_state = (start_row, start_col, start_mask)

    heapq.heappush(open_set, (start_f, start_g, start_row, start_col, start_mask))
    g_score[start_state] = start_g

    print(f"DEBUG (A*): Bắt đầu giải cho bàn cờ {board_size}x{board_size}...")

    while open_set:
        current_f, current_g, current_row, current_col, current_mask = heapq.heappop(open_set)
        current_state = (current_row, current_col, current_mask)
        if count_set_bits(current_mask) == total_cells:
            print("DEBUG (A*): Tìm thấy lời giải!")
            path = []
            u = current_state
            while u in came_from:
                parent_state = came_from[u]
                path.append((u[0], u[1]))
                u = parent_state 

            path.append((start_row, start_col))
            path.reverse() 
            if len(path) == total_cells:
                 return path
            else:
                 print(f"WARN (A*): Đường đi tái tạo có độ dài không khớp: {len(path)} vs {total_cells}")
                 return None
        for k in range(8):
            neighbor_row = current_row + x_move[k]
            neighbor_col = current_col + y_move[k]

            if is_safe(neighbor_row, neighbor_col, board_size):
                neighbor_index = coords_to_index(neighbor_row, neighbor_col, board_size)
                if (current_mask >> neighbor_index) & 1 == 0:
                    new_mask = current_mask | (1 << neighbor_index) 
                    new_g = current_g + 1

                    neighbor_state = (neighbor_row, neighbor_col, new_mask)
                    if neighbor_state not in g_score or new_g < g_score[neighbor_state]:
                        g_score[neighbor_state] = new_g
                        new_h = heuristic(count_set_bits(new_mask), board_size)
                        new_f = new_g + new_h
                        heapq.heappush(open_set, (new_f, new_g, neighbor_row, neighbor_col, new_mask))
                        came_from[neighbor_state] = current_state 
    print("DEBUG (A*): Open set rỗng, không tìm thấy lời giải.")
    return None

if __name__ == '__main__':
    print(f"Bắt đầu giải Mã đi tuần cho bàn cờ {BOARD_SIZE}x{BOARD_SIZE} bằng Backtracking...")
    start_time = time.time()
    solution_path_bt = solve_knights_tour_backtracking(BOARD_SIZE)
    end_time = time.time()
    if solution_path_bt:
        print(f"Backtracking tìm thấy lời giải trong {end_time - start_time:.4f} giây. Số bước: {len(solution_path_bt)}")
    else:
         print(f"Backtracking không tìm thấy lời giải trong {end_time - start_time:.4f} giây.")

    print(f"\nBắt đầu giải Mã đi tuần cho bàn cờ {BOARD_SIZE}x{BOARD_SIZE} bằng A*...")
    start_time = time.time()
    solution_path_a_star = solve_knights_tour_a_star(BOARD_SIZE)
    end_time = time.time()
    if solution_path_a_star:
        print(f"A* tìm thấy lời giải trong {end_time - start_time:.4f} giây. Số bước: {len(solution_path_a_star)}")
    else:
         print(f"A* không tìm thấy lời giải trong {end_time - start_time:.4f} giây.")