from collections import deque
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data", "solution.txt")

def solve_8_queens_with_ac3(filename=file_path):
    variables = [f"X{i}" for i in range(8)]
    # variables: ['X0', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7']
    domains = {var: list(range(8)) for var in variables}
    # domains: {
    # 'X0': [0, 1, 2, 3, 4, 5, 6, 7], 
    # 'X1': [0, 1, 2, 3, 4, 5, 6, 7], 
    # 'X2': [0, 1, 2, 3, 4, 5, 6, 7], 
    # 'X3': [0, 1, 2, 3, 4, 5, 6, 7], 
    # 'X4': [0, 1, 2, 3, 4, 5, 6, 7], 
    # 'X5': [0, 1, 2, 3, 4, 5, 6, 7], 
    # 'X6': [0, 1, 2, 3, 4, 5, 6, 7], 
    # 'X7': [0, 1, 2, 3, 4, 5, 6, 7]
    # }

    # Ràng buộc giữa mọi cặp biến khác nhau
    # Check quân hậu không tấn công nhau
    def constraints(xi, yi, xj, yj):
        i = int(xi[1])
        j = int(xj[1])
        return yi != yj and abs(yi - yj) != abs(i - j)

    # Hàm revise trong AC-3
    def revise(xi, xj):
        revised = False
        to_remove = []
        for yi in domains[xi]:
            if not any(constraints(xi, yi, xj, yj) for yj in domains[xj]):
                print("Không có xung đột")
                to_remove.append(yi)
                revised = True
        for yi in to_remove:
            domains[xi].remove(yi)
        return revised

    # Thuật toán AC-3
    def ac3():
        queue = deque((xi, xj) for xi in variables for xj in variables if xi != xj)
        print("Queue ban đầu:", queue)
        while queue:
            xi, xj = queue.popleft()
            if revise(xi, xj):
                if not domains[xi]:
                    return False
                for xk in variables:
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        print("Queue sau khi AC-3:", queue)
        return True

    # Backtracking sau khi AC-3 lọc miền
    def backtrack(assignment={}):
        if len(assignment) == 8:
            return assignment
        unassigned = [v for v in variables if v not in assignment]
        var = unassigned[0]
        for value in domains[var]:
            if all(constraints(var, value, other, assignment[other]) for other in assignment):
                assignment[var] = value
                result = backtrack(assignment)
                if result:
                    return result
                del assignment[var]
        return None

    # Bắt đầu giải
    if not ac3():
        print("Không có lời giải sau khi lọc AC-3.")
        return

    solution = backtrack()
    if solution:
        # Chuyển sang chuỗi 1-based index
        result = ''.join(str(solution[f"X{i}"] + 1) for i in range(8))
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Đã ghi lời giải vào file '{filename}': {result}")
    else:
        print("Không tìm thấy lời giải.")

# # Gọi hàm
# solve_8_queens_with_ac3()
