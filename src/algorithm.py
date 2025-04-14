from dataStructures import OpenList, CloseList, SearchNode, extract_path, make_node
from king_move import generate_king_moves

from collections import deque
import math
import random

end_state_tuple = (7,7)

def is_goal(state:tuple) -> bool:
    global end_state_tuple
    return state == end_state_tuple
            
def uninformed_search(root: SearchNode, type: str, level:int):
    global visited_nodes
    open_list = OpenList(type)
    open_list.insert(root)
    close_list = CloseList()
    
    while not open_list.is_empty():
        n = open_list.pop()
        if close_list.lookup(n.state):
            continue
            
        close_list.insert(n.state)
        
        if is_goal(n.state):
            visited_nodes = close_list
            return extract_path(n)
        
        for action, new_state in generate_king_moves(n.state, level):
            if not close_list.lookup(new_state):#
                new_node = make_node(n, action, new_state)
                open_list.insert(new_node)
    visited_nodes = close_list
    return None

def DeepLimitedSearch(node: SearchNode, depth_limit, level:int):
    stack = [(node, [])]# Stack chứa (node, path)
    close_list = CloseList()
    global visited_nodes
    
    while stack:
        current_node, path = stack.pop()# Lấy phần tử cuối cùng (LIFO)        
        if is_goal(current_node.state):
            visited_nodes = close_list
            return path        
        if close_list.lookup(current_node.state):
            continue       
        close_list.insert(current_node.state) # Đánh dấu đã xét
        
        if len(path) < depth_limit:  #mở rộng nếu chưa đạt depth_limit
            for action, new_state in generate_king_moves(current_node.state, level):
                if not close_list.lookup(new_state):
                    new_node = make_node(current_node, action, new_state)
                    stack.append((new_node, path + [new_state]))
    visited_nodes = close_list
    return None
       
def IDS(root: SearchNode, level:int):
    max_depth = 1000000000000
    for depth in range(max_depth + 1):
        solution = DeepLimitedSearch(root, depth, level)
        if solution != None:
            return solution
    return None
    

def UCS(root: SearchNode, level:int):
    global visited_nodes
    open_list = OpenList("UCS")
    open_list.insert(root)
    close_list = CloseList()
    
    while not open_list.is_empty():
        current_node = open_list.pop()[1] # index 0 là cost
        if is_goal(current_node.state):
            visited_nodes = close_list
            return extract_path(current_node)
        
        if close_list.lookup(current_node.state):
            continue
        
        close_list.insert(current_node.state)
        
        for action, new_state in generate_king_moves(current_node.state, level):
            if not close_list.lookup(new_state):
                new_node = make_node(current_node, action, new_state)
                open_list.insert(new_node) 
    visited_nodes = close_list
    return None

def heuristic(state: tuple) -> int:
    global end_state_tuple
    return abs(state[0] - end_state_tuple[0]) + abs(state[1] - end_state_tuple[1])

def Greedy(root: SearchNode, level:int):
    global visited_nodes
    queue = deque()
    queue.append((root, heuristic(root.state)))
    close_list = CloseList()
    
    while queue:
        queue = deque(sorted(queue, key=lambda x: x[1])) 
        current_node, current_heuristic = queue.popleft()
        
        if is_goal(current_node.state):
            visited_nodes = close_list
            return extract_path(current_node)
        
        if close_list.lookup(current_node.state):
            continue
        
        close_list.insert(current_node.state)
        
        for action, new_state in generate_king_moves(current_node.state, level):
            if not close_list.lookup(new_state):
                new_node = make_node(current_node, action, new_state)
                queue.append((new_node, heuristic(new_node.state)))
    visited_nodes = close_list
    return None

def A_start(root: SearchNode, level:int):
    # f(n) = g(n) + h(n) = node_cost + heristic
    global visited_nodes
    queue = deque()
    queue.append((root, root.g_cost + heuristic(root.state)))
    close_list = CloseList()
    
    while queue:
        queue = deque(sorted(queue, key=lambda x: x[1]))  
        current_node, current_cost = queue.popleft()# Lấy phần tử có path_cost nhỏ nhất
        
        if is_goal(current_node.state):
            visited_nodes = close_list
            return extract_path(current_node)
        
        if close_list.lookup(current_node.state):
            continue
        
        close_list.insert(current_node.state)
        
        for action, new_state in generate_king_moves(current_node.state, level):
            if not close_list.lookup(new_state):
                new_node = make_node(current_node, action, new_state)
                queue.append((new_node, new_node.g_cost + heuristic(new_node.state)))
    visited_nodes = close_list
    return None

# IDA* tăng ngưỡng xét từ vd 0, 2, 4, 6 (mỗi lần xét chỉ lấy giá trị bé hơn hoặc bằng ngưỡng)
def IDA_star(root: SearchNode, level: int):
    def search(node: SearchNode, path: set, threshold, level: int):# Tìm kiếm theo DFS với giới hạn threshold
        f_cost = node.g_cost + heuristic(node.state)
        if f_cost > threshold:
            return f_cost, None
        if is_goal(node.state):
            return None, extract_path(node)
        min_threshold = float("inf")
        path.add(node.state)
        for action, new_state in generate_king_moves(node.state, level):
            if new_state in path:
                continue  
            new_node = make_node(node, action, new_state)
            result, found_path = search(new_node, path.copy(), threshold, level)# Truyền bản sao của path
            if found_path:
                return None, found_path

            min_threshold = min(min_threshold, result)

        path.remove(node.state)# Xóa khỏi tập hợp khi quay lui
        return min_threshold, None# Trả về threshold mới nếu không tìm thấy lời giải

    threshold = root.g_cost + heuristic(root.state)
    while True:
        close_list = CloseList()
        new_threshold, path = search(root, close_list.set, threshold, level)
        if path:
            return path
        if new_threshold == float("inf"):# Không tìm thấy lời giải
            return None
        threshold = new_threshold
 
def simple_hill_climbing(root: SearchNode, level: int):
    current_node = root
    while True:
        if is_goal(current_node.state):
            return extract_path(current_node)
        neighbors = generate_king_moves(current_node.state, level)
        if not neighbors:
            return None
        for action, state in neighbors:
            if heuristic(state) < heuristic(current_node.state):
                current_node = make_node(current_node, action, state)
                break
        else:
            return None

def steepest_ascent_hill_climbing(root: SearchNode, level: int):
    current_node = root
    while True:
        if is_goal(current_node.state):
            return extract_path(current_node)
        neighbors = generate_king_moves(current_node.state, level)#Trả về (action, state)
        if not neighbors:
            return None
        best_neighbor = min(neighbors, key=lambda x: heuristic(x[1]))#Chọn hàng xóm tốt nhất theo heuristic nhỏ nhất
        if heuristic(best_neighbor[1]) >= heuristic(current_node.state):#Không tìm thấy trạng thái tốt hơn, dừng lại
            return None
        current_node = make_node(current_node, best_neighbor[0], best_neighbor[1])#Tạo node mới để lưu đường đi

# được quay lui nếu còn con của node hiện tại
def stochastic_hill_climbing(root: SearchNode, level):#leo đồi ngẫu nhiên
    current_node = root
    while True:
        if is_goal(current_node.state):
            return extract_path(current_node)
        neighbors = generate_king_moves(current_node.state, level)#Trả về (action, state)
        if not neighbors:
            return None
        random.shuffle(neighbors)  # Trộn ngẫu nhiên danh sách hàng xóm
        for action, new_state in neighbors:
            if heuristic(new_state) < heuristic(current_node.state):
                current_node = make_node(current_node, action, new_state)#Tạo node mới để lưu đường đi
                break
        else:
            return None


def stimulated_annealing(root: SearchNode, level):
    max_iterations = 100000
    current_node = root
    iteration = 0
    T = random.uniform(pow(10, 4), pow(10, 6))
    while iteration < max_iterations and T > 1e-3:# T > 1e-3: T quá bé
        iteration += 1
        if is_goal(current_node.state):
            return extract_path(current_node)
        neighbors = generate_king_moves(current_node.state, level)#Trả về (action, state)
        if not neighbors:
            return None
        random.shuffle(neighbors)#Trộn ngẫu nhiên danh sách hàng xóm
        for action, new_state in neighbors:
            if heuristic(new_state) < heuristic(current_node.state):
                current_node = make_node(current_node, action, new_state)#Tạo node mới để lưu đường đi
                break
        else:
            state_and_cost_list = []
            for action, new_state in neighbors:
                if T < 1e-3:
                    p = 1e-10
                else:
                    #p = pow(math.e, -(heuristic(current_node.state) - heuristic(new_state))/T)#Xác suất
                    
                    delta_E = heuristic(new_state) - heuristic(current_node.state)
                    #math.exp(709) số lớn nhất Python có thể xử lý
                    #math.exp(-709) là số rất nhỏ gần 0, không gây lỗi.
                    # p = math.exp(min(709, max(-709, delta_E / T)))
                    p = math.exp(max(-709, -delta_E / T))
                    
                state_and_cost_list.append((action, new_state, p))
            min_p_node = min(state_and_cost_list, key=lambda x: x[1])
            current_node = make_node(current_node, min_p_node[0], min_p_node[1])
            anpha = random.uniform(0, 1)
            T = anpha * T #Giảm nhiệt độ
            
# Tìm k (vd 2 hoặc ít hơn) node tốt nhất xét tiếp
def Beam_search(root: SearchNode, level):
    global end_state_tuple, visited_nodes
    #beam_width = 2
    open_list = OpenList("Beam search")# priority queue of ucs
    root.h_cost = heuristic(root.state)
    open_list.insert(root)
    close_list = CloseList()
    
    while not open_list.is_empty():
        current_node, current_node2 = open_list.pop()[1], None
        close_list.insert(current_node.state)
        if is_goal(current_node.state):
            visited_nodes = close_list
            return extract_path(current_node)
        neighbors, neighbors2 = generate_king_moves(current_node.state, level), None
        
        if len(open_list.deque) >= 2:
            current_node2 = open_list.pop()[1]
            close_list.insert(current_node2.state)
            if is_goal(current_node2.state):
                visited_nodes = close_list
                return extract_path(current_node2)
            neighbors2 = generate_king_moves(current_node2.state, level)
        
        if not neighbors and not neighbors2:
            return None
        
        open_list.deque.clear()#làm rỗng priority queue của open list
        
        for action, state in neighbors:
            if not close_list.lookup(state):
                close_list.insert(state)
                new_node = make_node(current_node, action, state)
                new_node.h_cost = heuristic(new_node.state)
                open_list.insert(new_node)
        if neighbors2 is not None:
            for action, state in neighbors2:
                if not close_list.lookup(state):
                    close_list.insert(state)
                    new_node = make_node(current_node, action, state)
                    new_node.h_cost = heuristic(new_node.state)
                    open_list.insert(new_node)

import random

def order_crossover(parent1: tuple, parent2: tuple):
    """Hàm lai ghép không trùng lặp giá trị"""
    size = len(parent1)
    parent1 = list(parent1)
    parent2 = list(parent2)
    start, end = sorted(random.sample(range(size), 2))
    
    child = [None] * size
    child2 = [None] * size
    
    child[start:end + 1] = parent1[start:end + 1]
    child2[start:end + 1] = parent2[start:end + 1]
    
    p2_index = 0
    for i in range(size):
        if child[i] is None:
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]
    
    p1_index = 0
    for i in range(size):
        if child2[i] is None:
            while parent1[p1_index] in child2:
                p1_index += 1
            child2[i] = parent1[p1_index]
    
    return tuple(child), tuple(child2)

def mutate(individual:tuple)->tuple:
    individual = list(individual)
    i, j = random.sample(range(len(individual)), 2)
    individual[i], individual[j] = individual[j], individual[i]
    return tuple(individual)

def genetic_algorithm(root: SearchNode, level: int):
    """không cần truy xuất đường đi"""
    if is_goal(root.state):
        return "Found goal state"
    
    open_list = OpenList("Genetic algorithm")
    close_list = CloseList()
    close_list.insert(root.state)
    populations_state = generate_king_moves(root.state, level)
    for action, state in populations_state:
        if not close_list.lookup(state):
            new_node = make_node(root, action, state)
            new_node.h_cost = heuristic(new_node.state)
            if is_goal(new_node.state):
                return "Found goal state"
            open_list.insert(new_node)
        
    while len(open_list.deque) >= 2:#phải có ít nhất 2 node lai ghép
        father_node, mother_node = open_list.pop()[1], open_list.pop()[1]
        child_state_1, child_state_2 = mutate(order_crossover(father_node.state, mother_node.state))
        close_list.insert(child_state_1)
        child_node1 = make_node(father_node, None, child_state_1)
        if is_goal(child_node1.state):
            return "Found goal state"
        
        close_list.insert(child_state_2)
        child_node2 = make_node(mother_node, None, child_state_2)
        if is_goal(child_node2.state):
            return "Found goal state"
        
        child_node1.h_cost = heuristic(child_node1.state)
        child_node2.h_cost = heuristic(child_node2.state)
        if not close_list.lookup(child_node1.state):
            open_list.insert(child_node1)
        if not close_list.lookup(child_node2.state):
            open_list.insert(child_node2)
    return None  