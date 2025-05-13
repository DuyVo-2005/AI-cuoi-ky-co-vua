#agent 2 chế độ exploit (khai thác) và khám phá (explore)

import numpy as np
import random

BOARD_SIZE = 8

def convert_action_to_alpha(pos: tuple):
    if pos == (0, -1):
        return "U"
    if pos == (1, -1):
        return "UR"
    if pos == (1, 0):
        return "R"
    if pos == (1, 1):
        return "DR"
    if pos == (0, 1):
        return "D"
    if pos == (-1, 1):
        return "DL"
    if pos == (-1, 0):
        return "L"
    if pos == (-1, -1):
        return "UL"

ACTIONS = [(-1, -1), (0, -1), (1, -1),
            (-1, 0),           (1, 0),
            (-1, 1),  (0, 1),  (1, 1)]

ACTION_NAMES = []
for action in ACTIONS:
    action_name = convert_action_to_alpha(action)
    ACTION_NAMES.append(action_name)

#B1. Khởi tạo Q-table và điền giá trị ban đầu là 0 cho các vị trí (chưa biết gì cả)
Q_table = np.zeros((BOARD_SIZE, BOARD_SIZE, len(ACTIONS)))
# ĐỊNH NGHĨA CẤU TRÚC DỮ LIỆU
## Kích thước là (8, 8, 8):
## Trục 1 và 2 (8x8): đại diện cho tất cả các ô vị trí trên bàn cờ.
## Trục 3 (8): đại diện cho 8 hành động có thể thực hiện ở mỗi ô.
# Ý NGHĨA
## Q_table[x][y][a] lưu giá trị Q tại vị trí (x, y) khi thực hiện hành động thứ a
## Mỗi giá trị Q đại diện cho mức độ tốt (phần thưởng kỳ vọng) của việc thực hiện 1 hành động đó tại 1 vị trí

print("Q-table khởi tạo:")
for row in range(BOARD_SIZE):
    for col in range(BOARD_SIZE):
        print(Q_table[row][col])
    print()

enemy_pawns = [(3, 3), (3, 5)]# Ví dụ: Tốt địch ở d4 và f4
danger_zones = set()#Tập hợp các ô nguy hiểm

def is_valid(x, y):
    """Hàm kiểm tra ô có hợp lệ"""
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and (x, y) not in danger_zones

def get_danger_zones(pawns: list)->set:
    """
    Hàm xác định các ô nguy hiểm
    Input: list các tuple vị trị mà tốt đứng
    Output: set các vị trí mà tốt kiểm soát
    """
    danger_zones = set()
    for x, y in pawns:
        danger_zones.add((x, y))#Ô Tốt đứng
        #Các ô Tốt có thể tấn công(4 ô đường chéo xung quanh Tốt)
        if is_valid(x + 1, y + 1):
            danger_zones.add((x + 1, y + 1))
        if is_valid(x + 1, y - 1):
            danger_zones.add((x + 1, y - 1))
        if is_valid(x - 1, y - 1):
            danger_zones.add((x - 1, y - 1))
        if is_valid(x - 1, y + 1):
            danger_zones.add((x - 1, y + 1))
    return danger_zones

def heuristic(state: tuple) -> int:
    return abs(state[0] - goal_pos[0]) + abs(state[1] - goal_pos[1])

danger_zones = get_danger_zones(enemy_pawns)
alpha = 0.2#Tốc độ học
gamma = 0.8#Hệ số chiết khấu: agent đến phần thưởng là bao xa.
epsilon = 0.2#Xác suất chọn hành động ngẫu nhiên
start_pos = (7, 4)#e7
goal_pos = (3, 4)#e3
episodes = 1000#Số lượng tập huấn luyện

for episode in range(episodes):
    #B2. Bắt đầu 1 episode
    x, y = start_pos
    while (x, y) != goal_pos:
        #B3. Tác nhân thực hiện hành động 
        #Chọn hành động
        if random.uniform(0, 1) < epsilon:#Chọn ngẫu nhiên
            action_idx = random.randint(0, 7)
        else:
            action_idx = np.argmax(Q_table[x, y])#Chọn theo kinh nghiệm đã được học
        dx, dy = ACTIONS[action_idx]
        new_x, new_y = x + dx, y + dy
        if not is_valid(new_x, new_y):
            R = -100
            Q_table[x, y, action_idx] += alpha * (R - Q_table[x, y, action_idx])
            break#B7. Kết thúc huấn luyện nếu đi vào ô nguy hiểm hoặc không hợp lệ
        else:
            #B4. Xác định phần thường
            R = 100 if (new_x, new_y) == goal_pos else -1# R (reward)max -> phần thưởng càng lớn càng gần đích
            #B5. Tính lại Q-value cho trạng thái mới
            max_new_q = np.max(Q_table[new_x, new_y])
            current_q = Q_table[x, y, action_idx]
            p = 1 - heuristic((new_x, new_y))/14#P(s,a,s’)): xác suất đi từ trạng thái s đến s’ qua hành động a (0 -> 1 – dựa vào thực tế -> setup)
            Q_table[x, y, action_idx] += alpha * (R + gamma * p * max_new_q - current_q)
            #B6. Chuyển sang trạng thái mới
            x, y = new_x, new_y
    #B8. Lặp lại các bước 2 - 8 cho số episode mong muốn
            
#Kiểm tra đường đi từ vị trí bắt đầu đến đích
x, y = start_pos
path = [(x, y)]
while (x, y) != goal_pos:  
    action_idx = np.argmax(Q_table[x, y])
    dx, dy = ACTIONS[action_idx]
    
    x, y = x + dx, y + dy
    if not is_valid(x, y):
        print("Vua đang đi vào ô nguy hiểm có tọa độ là:", (x, y))
        break
    path.append((x, y))

# print("Đường đi đã học:", path)

# for row in range(BOARD_SIZE):
#     for col in range(BOARD_SIZE):
#         print(Q_table[row][col])
#     print()
 
print("\n=== Q-table sau học ===")
for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        print(f"Vị trí ({i},{j}):")
        for k, action in enumerate(ACTION_NAMES):
            print(f"  Hành động {action}: {Q_table[i][j][k]:.5f}")
        print()
print(Q_table)   