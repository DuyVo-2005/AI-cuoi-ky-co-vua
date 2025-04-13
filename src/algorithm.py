from dataStructures import OpenList, CloseList, SearchNode, extract_path, make_node
from knight import generate_knight_moves

def is_goal(state:tuple) -> bool:
    global end_state_tuple
    return state == end_state_tuple
            
def uninformed_search(root: SearchNode, type: str):
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
        
        for action, new_state in generate_knight_moves(n.state):
            if not close_list.lookup(new_state):#
                new_node = make_node(n, action, new_state)
                open_list.insert(new_node)
    visited_nodes = close_list
    return None

start_state_tuple = (0,0)
end_state_tuple = (7,1)
 
root = make_node(None, None, start_state_tuple)                       
solution = uninformed_search(root, "BFS")
print(f"Số bước di chuyển: {len(solution)}")
print(solution)
