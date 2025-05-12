
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data", "solution.txt")

def solve_8_queens_nhin_thay_1_phan(filename=file_path):
    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == abs(i - row):
                return False
        return True

    def backtrack(row, board):
        if row == 8:
            return board.copy()
        for col in range(8):
            if is_safe(board, row, col):
                board[row] = col
                result = backtrack(row + 1, board)
                if result:
                    return result
                board[row] = -1
        return None

    board = [-1] * 8
    solution = backtrack(0, board)

    if solution:
        with open(filename, "w", encoding="utf-8") as f:
            result_string = ''.join(str(col + 1) for col in solution)
            f.write(result_string)
        print(f"Đã ghi lời giải vào file '{filename}': {result_string}")
    else:
        print("Không tìm thấy lời giải.")

# # Gọi hàm
# solve_8_queens_and_save()
