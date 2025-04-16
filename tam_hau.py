N = 8  # Kích thước bàn cờ và số quân hậu

def is_safe(board, row, col):
    # Kiểm tra cột
    for i in range(row):
        if board[i] == col:
            return False

    # Kiểm tra đường chéo
    for i in range(row):
        if abs(board[i] - col) == abs(i - row):
            return False

    return True

def solve(board, row, solutions):
    if row == N:
        solutions.append(board[:])  # Lưu lại kết quả
        return

    for col in range(N):
        if is_safe(board, row, col):
            board[row] = col
            solve(board, row + 1, solutions)
            # Backtrack: không cần reset board[row] vì sẽ ghi đè lần sau

def print_solution(solution):
    for row in solution:
        line = ["."] * N
        line[row] = "Q"
        print(" ".join(line))
    print("\n")

# Khởi chạy
solutions = []
solve([0]*N, 0, solutions)

for i, sol in enumerate(solutions[:3]):  # In thử 3 cách đầu
    print(f"> Cách {i+1}:")
    print_solution(sol)
