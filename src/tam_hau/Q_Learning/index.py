import random
import os
from collections import defaultdict
from .q_learning_model_generation import q_learning, load_q_model, default_q_values

BOARD_SIZE = 8
EPISODES = 5000
ALPHA = 0.1          # Learning rate
GAMMA = 0.9          # Discount factor
EPSILON = 0.1        # Exploration rate

# Hàm kiểm tra xem có xung đột khi đặt hậu ở cột col không
def is_safe(state, row, col):
    for r, c in enumerate(state):
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True


# 🧠 Sau huấn luyện: chơi thử
def solve_q_learning(insert, clear, text_1):
    Q = load_q_model()
    state = tuple()
    for row in range(BOARD_SIZE):
        action = Q[state].index(max(Q[state]))
        if not is_safe(state, row, action):
            print("Thất bại tại hàng", row)
            print("Trạng thái: ", state)
            print("Hàng động", action)
            clear(text_1)
            insert(text_1, "Thất bại tại hàng " + str(row) + "\n")
            insert(text_1, "Trạng thái: " + str(state) + "\n")
            insert(text_1, "Hàng động: " + str(action) + "\n")
            return False
        state = state + (action,)
    print("Thành công! Giải: ", state)
    clear(text_1)
    insert(text_1, "Thành công! Giải: " + str(state) + "\n")
    state = tuple(x + 1 for x in state)
    save_solution_to_file(state)
    insert(text_1, "Đã lưu giải pháp vào file solution.txt\n")
    return True

def save_solution_to_file(solution):
     # Lấy đường dẫn tuyệt đối đến thư mục chứa file bfs.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "../", "data", "solution.txt")

    with open(file_path, "w") as f:
        if solution:
            solution_str = ''.join(map(str, solution)) 
            f.write(f"{solution_str}\n")
        else:
            f.write("Khong tim thay nghiem.\n")

# solve_q_learning()
