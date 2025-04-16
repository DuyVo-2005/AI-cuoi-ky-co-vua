from collections import deque
import os


N = 8  # Kích thước bàn cờ

# Hàm kiểm tra quân hậu có an toàn không
def is_safe(board, row, col):
    for r in range(row):
        c = board[r]
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

# Giải bài toán bằng BFS
def solve_n_queens_bfs(n):
    queue = deque([([], 0)])  # (board, row)
    node_count = 0  # Đếm số node đã duyệt

    while queue:
        board, row = queue.popleft()
        node_count += 1

        if row == n:
            return board, node_count  # Trả về nghiệm đầu tiên và số node đã duyệt

        for col in range(n):
            if is_safe(board, row, col):
                queue.append((board + [col], row + 1))

    return None, node_count  # Không tìm được nghiệm

# Lưu kết quả vào file
def save_solution_to_file(solution, node_count):
     # Lấy đường dẫn tuyệt đối đến thư mục chứa file bfs.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "solution.txt")

    with open(file_path, "w") as f:
        if solution:
            solution_str = ''.join(str(col + 1) for col in solution)  # Chuyển cột từ 0 -> 1
            f.write(f"{solution_str}\n")
        else:
            f.write("Khong tim thay nghiem.\n")
        f.write(f"{node_count}\n")

def solve_bfs():
  solution, node_count = solve_n_queens_bfs(N)
  save_solution_to_file(solution, node_count)

  print(f"Giải hoàn tất, đã ghi kết quả vào file 'solution.txt'")
