from dataStructures import OpenList, CloseList, SearchNode, extract_path, make_node
from king_and_pawn_move import generate_king_moves

from collections import deque
import math
import random
import os
import numpy

end_state_tuple = (8,17)
visited_nodes = None

CURRENT_DIRECTORY_PATH = os.path.dirname(__file__)

def show_path_in_file(solution):
    print(f"Số không gian trạng thái mở rộng: {len(visited_nodes.set)}")
    with open(CURRENT_DIRECTORY_PATH + "/result.txt", "w", encoding="utf-8") as f:
        f.write("Solution: ")
        if solution == None:
            f.write("\nNo solution")
        else:
            for state in solution:               
                f.write(f"\n{state}")
        f.write("\nClose list: ")
        if visited_nodes == None:
            f.write("\nNone")
        else:
            for state in visited_nodes.set:
                f.write(f"\n{state}")


def is_goal(state:tuple) -> bool:
    return state == end_state_tuple
            
def uninformed_search(root: SearchNode, type: str, pos_not_move: list):
    global visited_nodes
    visited_nodes = None
    print(root.state)
    print(end_state_tuple)
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
            solution = extract_path(n)
            show_path_in_file(solution)
            return solution
        
        for action, new_state in generate_king_moves(n.state, pos_not_move):
            if not close_list.lookup(new_state):#
                new_node = make_node(n, action, new_state)
                open_list.insert(new_node)
    visited_nodes = close_list
    show_path_in_file(None)
    return None

def DeepLimitedSearch(node: SearchNode, depth_limit, pos_not_move: list):
    stack = [(node, [])]# Stack chứa (node, path)
    close_list = CloseList()
    global visited_nodes
    visited_nodes = None
    
    while stack:
        current_node, path = stack.pop()# Lấy phần tử cuối cùng (LIFO)        
        if is_goal(current_node.state):
            visited_nodes = close_list
            return path        
        if close_list.lookup(current_node.state):
            continue       
        close_list.insert(current_node.state)# Đánh dấu đã xét
        
        if len(path) < depth_limit:# mở rộng nếu chưa đạt depth_limit
            for action, new_state in generate_king_moves(current_node.state, pos_not_move):
                if not close_list.lookup(new_state):
                    new_node = make_node(current_node, action, new_state)
                    stack.append((new_node, path + [new_state]))
    visited_nodes = close_list
    return None
       
def IDS(root: SearchNode, pos_not_move: list):
    max_depth = 1000000000000
    for depth in range(max_depth + 1):
        solution = DeepLimitedSearch(root, depth, pos_not_move)
        if solution != None:
            show_path_in_file(solution)
            return solution
    show_path_in_file(None)
    return None
    

def UCS(root: SearchNode, pos_not_move: list):
    global visited_nodes
    visited_nodes = None
    open_list = OpenList("UCS")
    open_list.insert(root)
    close_list = CloseList()
    
    while not open_list.is_empty():
        current_node = open_list.pop()[1] # index 0 là cost
        if is_goal(current_node.state):
            visited_nodes = close_list
            solution = extract_path(current_node)
            show_path_in_file(solution)
            return solution
        
        if close_list.lookup(current_node.state):
            continue
        
        close_list.insert(current_node.state)
        
        for action, new_state in generate_king_moves(current_node.state, pos_not_move):
            if not close_list.lookup(new_state):
                new_node = make_node(current_node, action, new_state)
                open_list.insert(new_node) 
    visited_nodes = close_list
    show_path_in_file(None)
    return None

def heuristic(state: tuple) -> int:
    global end_state_tuple
    return abs(state[0] - end_state_tuple[0]) + abs(state[1] - end_state_tuple[1])

def Greedy(root: SearchNode, pos_not_move: list):
    global visited_nodes
    visited_nodes = None
    queue = deque()
    queue.append((root, heuristic(root.state)))
    close_list = CloseList()
    
    while queue:
        queue = deque(sorted(queue, key=lambda x: x[1])) 
        current_node, current_heuristic = queue.popleft()
        
        if is_goal(current_node.state):
            visited_nodes = close_list
            solution = extract_path(current_node)
            show_path_in_file(solution)
            return solution
        
        if close_list.lookup(current_node.state):
            continue
        
        close_list.insert(current_node.state)
        
        for action, new_state in generate_king_moves(current_node.state, pos_not_move):
            if not close_list.lookup(new_state):
                new_node = make_node(current_node, action, new_state)
                queue.append((new_node, heuristic(new_node.state)))
    visited_nodes = close_list
    show_path_in_file(None)
    return None

def A_start(root: SearchNode, pos_not_move: list):
    # f(n) = g(n) + h(n) = node_cost + heristic
    global visited_nodes
    visited_nodes = None
    queue = deque()
    queue.append((root, root.g_cost + heuristic(root.state)))
    close_list = CloseList()
    
    while queue:
        queue = deque(sorted(queue, key=lambda x: x[1]))  
        current_node, current_cost = queue.popleft()# Lấy phần tử có path_cost nhỏ nhất
        
        if is_goal(current_node.state):
            visited_nodes = close_list
            solution = extract_path(current_node)
            show_path_in_file(solution)
            return solution
        
        if close_list.lookup(current_node.state):
            continue
        
        close_list.insert(current_node.state)
        
        for action, new_state in generate_king_moves(current_node.state, pos_not_move):
            if not close_list.lookup(new_state):
                new_node = make_node(current_node, action, new_state)
                queue.append((new_node, new_node.g_cost + heuristic(new_node.state)))
    visited_nodes = close_list
    show_path_in_file(None)
    return None

# IDA* tăng ngưỡng xét từ vd 0, 2, 4, 6 (mỗi lần xét chỉ lấy giá trị bé hơn hoặc bằng ngưỡng)
def IDA_star(root: SearchNode, pos_not_move: list):
    def search(node: SearchNode, path: set, threshold, pos_not_move: list):# Tìm kiếm theo DFS với giới hạn threshold
        f_cost = node.g_cost + heuristic(node.state)
        if f_cost > threshold:
            return f_cost, None
        if is_goal(node.state):
            solution = extract_path(node)
            return None, solution
        min_threshold = float("inf")
        path.add(node.state)
        for action, new_state in generate_king_moves(node.state, pos_not_move):
            if new_state in path:
                continue  
            new_node = make_node(node, action, new_state)
            result, found_path = search(new_node, path.copy(), threshold, pos_not_move)# Truyền bản sao của path
            if found_path:
                return None, found_path

            min_threshold = min(min_threshold, result)

        path.remove(node.state)# Xóa khỏi tập hợp khi quay lui
        return min_threshold, None# Trả về threshold mới nếu không tìm thấy lời giải

    threshold = root.g_cost + heuristic(root.state)
    while True:
        close_list = CloseList()
        new_threshold, path = search(root, close_list.set, threshold, pos_not_move)
        if path:
            show_path_in_file(path)
            return path
        if new_threshold == float("inf"):# Không tìm thấy lời giải
            show_path_in_file(None)
            return None
        threshold = new_threshold
 
def simple_hill_climbing(root: SearchNode, pos_not_move: list):
    global visited_nodes
    visited_nodes = CloseList()
    current_node = root
    visited_nodes.insert(current_node.state)
    while True:
        if is_goal(current_node.state):
            solution = extract_path(current_node)
            show_path_in_file(solution)
            return solution
        neighbors = generate_king_moves(current_node.state, pos_not_move)
        if not neighbors:
            show_path_in_file(None)
            return None
        for action, state in neighbors:
            if heuristic(state) < heuristic(current_node.state):
                current_node = make_node(current_node, action, state)
                visited_nodes.insert(current_node.state)
                break
        else:
            show_path_in_file(None)
            return None

def steepest_ascent_hill_climbing(root: SearchNode, pos_not_move: list):
    global visited_nodes
    visited_nodes = CloseList()
    current_node = root
    while True:
        if is_goal(current_node.state):
            solution = extract_path(current_node)
            show_path_in_file(solution)
            return solution
        neighbors = generate_king_moves(current_node.state, pos_not_move)#Trả về (action, state)
        if not neighbors:
            show_path_in_file(None)
            return None
        best_neighbor = min(neighbors, key=lambda x: heuristic(x[1]))#Chọn hàng xóm tốt nhất theo heuristic nhỏ nhất
        if heuristic(best_neighbor[1]) >= heuristic(current_node.state):#Không tìm thấy trạng thái tốt hơn, dừng lại
            show_path_in_file(None)
            return None
        current_node = make_node(current_node, best_neighbor[0], best_neighbor[1])#Tạo node mới để lưu đường đi
        visited_nodes.insert(current_node.state)

# được quay lui nếu còn con của node hiện tại
def stochastic_hill_climbing(root: SearchNode, pos_not_move):#leo đồi ngẫu nhiên
    global visited_nodes
    visited_nodes = CloseList()
    current_node = root
    visited_nodes.insert(current_node.state)
    while True:
        if is_goal(current_node.state):
            solution = extract_path(current_node)
            show_path_in_file(solution)
            return solution
        neighbors = generate_king_moves(current_node.state, pos_not_move)#Trả về (action, state)
        if not neighbors:
            show_path_in_file(None)
            return None
        random.shuffle(neighbors)  # Trộn ngẫu nhiên danh sách hàng xóm
        for action, new_state in neighbors:
            if heuristic(new_state) < heuristic(current_node.state):
                current_node = make_node(current_node, action, new_state)#Tạo node mới để lưu đường đi
                visited_nodes.insert(current_node.state)
                break
        else:
            show_path_in_file(None)
            return None

def stimulated_annealing(root: SearchNode, pos_not_move):
    global visited_nodes
    max_iterations = 100000
    current_node = root
    visited_nodes.insert(current_node.state)
    iteration = 0
    visited_nodes = CloseList()
    T = random.uniform(pow(10, 4), pow(10, 6))
    while iteration < max_iterations and T > 1e-3:# T > 1e-3: T quá bé
        iteration += 1
        if is_goal(current_node.state):
            solution = extract_path(current_node)
            show_path_in_file(solution)
            return solution
        neighbors = generate_king_moves(current_node.state, pos_not_move)#Trả về (action, state)
        if not neighbors:
            return None
        random.shuffle(neighbors)#Trộn ngẫu nhiên danh sách hàng xóm
        for action, new_state in neighbors:
            if heuristic(new_state) < heuristic(current_node.state):
                current_node = make_node(current_node, action, new_state)#Tạo node mới để lưu đường đi
                visited_nodes.insert(current_node.state)
                break
        else:
            state_and_cost_list = []
            for action, new_state in neighbors:
                p = numpy.exp(-(heuristic(current_node.state) - heuristic(new_state)) / T)
                state_and_cost_list.append((action, new_state, p))           
            max_p_node = max(state_and_cost_list, key=lambda x: x[2])#biến xác suất cao chọn
            current_node = make_node(current_node, max_p_node[0], max_p_node[1])
            visited_nodes.insert(current_node.state)
            anpha = random.uniform(0, 1)
            T = anpha * T #Giảm nhiệt độ với anphal hệ số làm nguội
    show_path_in_file(None)
    return None
            
# Tìm k (vd 2 hoặc ít hơn) node tốt nhất xét tiếp
def Beam_search(root: SearchNode, pos_not_move):
    global end_state_tuple, visited_nodes
    visited_nodes = None
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
            solution = extract_path(current_node)
            show_path_in_file(solution)
            return solution
        neighbors, neighbors2 = generate_king_moves(current_node.state, pos_not_move), None
        
        if len(open_list.deque) >= 2:
            current_node2 = open_list.pop()[1]
            close_list.insert(current_node2.state)
            if is_goal(current_node2.state):
                visited_nodes = close_list
                solution = extract_path(current_node2)
                show_path_in_file(solution)
                return solution
            neighbors2 = generate_king_moves(current_node2.state, pos_not_move)
        
        if not neighbors and not neighbors2:
            show_path_in_file(None)
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
    show_path_in_file(None)
    return None