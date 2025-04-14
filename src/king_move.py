
def generate_king_moves(state: tuple, level: int):
    """Return list (action, state) or None"""
    enimies_positions = []
    pos_not_move = []
    
    if level >= 1:
        enimies_positions.append((4,4)) #[(4,4),(3,3),(3,5),(5,3),(5,5)]
    if level >= 2:
        enimies_positions.append((1,6))
    if level >= 3:
        enimies_positions.append((6,1))
    if level == 4:
        enimies_positions.append((1,1))
    
    pos_not_move = enimies_positions.copy()
    for pos in enimies_positions:
        pos_not_move += enemy_capture_moves(pos)

    x, y = state[0], state[1]
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    moves = []
    for (dx, dy) in directions:
        new_x = x + dx
        new_y = y + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8 and (new_x, new_y) not in pos_not_move:
            moves.append(((dx, dy),(new_x, new_y)))# (action, state)
    return moves

def enemy_capture_moves(enemy_pos: tuple):
    moves = []
    directions = [
        (-1, -1), (-1, 1),
        (1, -1),  (1, 1)
    ]
    for (dx, dy) in directions:
        new_x = enemy_pos[0] + dx
        new_y = enemy_pos[1] + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            moves.append((new_x, new_y))
    return moves