#Kết quả là 1 cây tìm kiếm (mỗi nhánh là áp 1 hành động lên một tập trạng thái)
#Trạng thái trùng trong tập thì lấy 1
#Search with no observation
from collections import deque

SQSIZE = 75
COLS = 18
ROWS = 9
WIDTH = SQSIZE * COLS
HEIGHT = SQSIZE * ROWS

MOVES = {
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),           (1, 0),
    (-1, 1),  (0, 1),  (1, 1)
}

#Tập trạng thái mục tiêu
goal_set = [
    (7,17),
    (8,17)    
]

max_depth = 10000
danger_zones = set()

def is_valid_move(x, y):
    """Hàm kiểm tra ô có hợp lệ"""
    return 0 <= x < ROWS and 0 <= y < COLS and (x, y) not in danger_zones

def move(state, direction):  
    state = list(state)
    state[0] += direction[0]
    state[1] += direction[1]
    if not is_valid_move(state[0], state[1]):
        return None
    return tuple(state)

def apply_action_to_belief(belief, action):
    result = []
    visited = set()
    for state in belief:
        new_state = move(state, action)
        if new_state is None:
            new_state = state#giữ nguyên trạng thái nếu không di chuyển được
        if new_state not in visited:
            visited.add(new_state)                    
            result.append(new_state)
    return result

def is_goal_belief_set(belief):
    return all(state in goal_set for state in belief)

# def is_near_goal(state: tuple)->bool:
#     """
#     Kiểm tra trạng thái có gần giống trạng thái đích.
#     Ví dụ trạng thái đích cho biết tọa độ y là 17
#     """
#     return state[1] == (17)
        
def search_with_no_observation(initial_belief_set: list):
    queue = deque()
    visited = set()
    queue.append((initial_belief_set, []))
    depth = 0
    while queue and depth < max_depth:
        belief_set, actions = queue.popleft()
        frozen_belief_set = frozenset(belief_set)# set add set lỗi unhashable (do set có thể thay đổi thứ tự)
        if frozen_belief_set in visited:
            continue
        visited.add(frozen_belief_set)
        print("=====================")
        print(f"Actions: {actions}\n")
        print(f"Belief set (size={len(belief_set)}):")
        for state in belief_set:
            print(state)
            print("----")
        if is_goal_belief_set(belief_set):
            print("Reached goal set!")
            return actions
        for action in MOVES:
            new_belief = apply_action_to_belief(belief_set, action)
            if new_belief:
                queue.append((new_belief, actions + [action]))
        depth += 1
    return None

def search_with_no_observation_solve(initial_belief_set: list, attack_zone: list):
    global danger_zones
    #pawns_pos = [(6, 6), (9, 9)]
    #danger_zones = get_danger_zones(pawns_pos)
    danger_zones = set(attack_zone)
    first_path = [initial_belief_set[0]]
    second_path = [initial_belief_set[1]]

    plan = search_with_no_observation(initial_belief_set)
    print("Plan to reach goal:", plan)
    if plan is not None:
        order_path = 1
        for state in initial_belief_set:
            for action in plan:
                state = list(state)
                state[0] += action[0]
                state[1] += action[1]
                if not is_valid_move(state[0], state[1]):
                    continue
                state = tuple(state)
                if order_path == 1:
                    first_path += [state]
                else:
                    second_path += [state]
            order_path = 2
        return first_path, second_path