#agent 2 chế độ exploit (khai thác) và khám phá (explore)
import numpy as np
import random

BOARD_SIZE = 4
ACTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Trái, Phải, Lên, Xuống
ACTION_NAMES = ['L', 'R', 'U', 'D']

# Thêm chướng ngại vật
walls = [(1, 1), (2, 1)]  # Các ô bị cấm (tường)

# Khởi tạo bảng Q
Q_table = np.zeros((BOARD_SIZE, BOARD_SIZE, len(ACTIONS)))
print(Q_table)

# Các thông số Q-learning
alpha = 0.5      # learning rate
gamma = 0.9      # discount factor
epsilon = 0.2    # tỉ lệ random (explore)

goal = (3, 3)

def is_valid(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, len(ACTIONS)-1)  # explore
    else:
        x, y = state
        return np.argmax(Q_table[x][y])  # exploit

def step(state, action_index):
    dx, dy = ACTIONS[action_index]
    x, y = state
    new_x, new_y = x + dx, y + dy
    if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
        return state, -5  # Đi ra ngoài rìa -> phạt
    if (new_x, new_y) in walls:
        return state, -10  # Đụng vào tường -> phạt nặng
    if (new_x, new_y) == goal:
        return (new_x, new_y), 10  # phần thưởng khi tới đích
    return (new_x, new_y), -1  # mất 1 điểm cho mỗi bước (khuyến khích đi nhanh hơn)

# Quá trình học
for episode in range(500):
    state = (0, 0)
    while state != goal:
        action_index = choose_action(state)
        next_state, reward = step(state, action_index)

        x, y = state
        next_x, next_y = next_state

        # Cập nhật Q_table theo công thức Q-learning
        Q_table[x][y][action_index] = Q_table[x][y][action_index] + alpha * (
            reward + gamma * np.max(Q_table[next_x][next_y]) - Q_table[x][y][action_index]
        )

        state = next_state

# Hiển thị bảng Q đơn giản (chỉ in giá trị lớn nhất tại mỗi ô)
# print("Bảng Q đơn giản sau học:")
# for i in range(BOARD_SIZE):
#     for j in range(BOARD_SIZE):
#         best_action = np.argmax(Q_table[i][j])
#         print(f"{ACTION_NAMES[best_action]}", end=' ')
#     print()

# In toàn bộ Q_table chi tiết
print("\n=== Q-table sau học ===")
for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        print(f"Vị trí ({i},{j}):")
        for k, action in enumerate(ACTION_NAMES):
            print(f"  Hành động {action}: {Q_table[i][j][k]:.5f}")
        print()
print(Q_table)
