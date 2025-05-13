def generate_king_moves(state: tuple, pos_not_move: list) -> list:
    """Return list (action, state) or None"""
    x, y = state[0], state[1]
    directions = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0),           (1, 0),
        (-1, 1),  (0, 1),  (1, 1)
    ]
    moves = []
    for (dx, dy) in directions:
        new_x = x + dx
        new_y = y + dy
        if 0 <= new_x < 9 and 0 <= new_y < 18 and (new_x, new_y) not in pos_not_move:
            moves.append(((dx, dy),(new_x, new_y)))# (action, state)
    return moves

def enemy_capture_moves(enemy_pos: tuple):
    moves = []
    directions = [
        (-1, -1), (1, -1),
        (-1, 1),  (1, 1)
    ]
    for (dx, dy) in directions:
        new_x = enemy_pos[0] + dx
        new_y = enemy_pos[1] + dy
        if 0 <= new_x < 9 and 0 <= new_y < 18:
            moves.append((new_x, new_y))
    return moves