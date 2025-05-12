import random
from collections import defaultdict
import os

BOARD_SIZE = 8
ALPHA = 0.1
GAMMA = 0.9

def is_safe(state, row, col):
    for r, c in enumerate(state):
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

def train_q_learning(episodes, epsilon):
    Q = defaultdict(lambda: [0.0 for _ in range(BOARD_SIZE)])
    for _ in range(episodes):
        state = tuple()
        for row in range(BOARD_SIZE):
            if random.random() < epsilon:
                action = random.randint(0, BOARD_SIZE - 1)
            else:
                action = Q[state].index(max(Q[state]))
            if is_safe(state, row, action):
                reward = 1
                next_state = state + (action,)
                done = (row == BOARD_SIZE - 1)
                if done:
                    reward = 100
            else:
                reward = -100
                next_state = None
                done = True
            old_q = Q[state][action]
            max_future_q = max(Q[next_state]) if not done else 0
            Q[state][action] = old_q + ALPHA * (reward + GAMMA * max_future_q - old_q)
            state = next_state
            if done:
                break
    return Q

def test_q_model(Q, test_games=100):
    success = 0
    for _ in range(test_games):
        state = tuple()
        valid = True
        for row in range(BOARD_SIZE):
            action = Q[state].index(max(Q[state]))
            if not is_safe(state, row, action):
                valid = False
                break
            state = state + (action,)
        if valid:
            success += 1
    return success / test_games

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "../", "data", "q_learning_results.txt")

def run_experiments():
    with open(file_path, "w") as f:
        f.write("EPISODES EPSILON SUCCESS_RATE\n")
        for episodes in [10, 100, 200, 500, 1000, 2000, 5000]:
            for epsilon in [0.01, 0.05, 0.1, 0.5]:
                total_success = 0
                runs = 30
                for _ in range(runs):
                    Q = train_q_learning(episodes, epsilon)
                    success_rate = test_q_model(Q)
                    total_success += success_rate
                avg_success = total_success / runs
                f.write(f"{episodes} {epsilon} {avg_success:.2f}\n")
                print(f"EPISODES={episodes}, EPSILON={epsilon}, AVG_SUCCESS={avg_success:.2f}")


import pandas as pd
import matplotlib.pyplot as plt
def draw_graph():
  # Đọc dữ liệu từ file
  df = pd.read_csv(file_path, sep=" ")

  # Tạo biểu đồ đường cho từng epsilon
  plt.figure(figsize=(10, 6))
  for eps in df['EPSILON'].unique():
      subset = df[df['EPSILON'] == eps]
      plt.plot(subset['EPISODES'], subset['SUCCESS_RATE'], marker='o', label=f'EPSILON = {eps}')

  # Tuỳ chỉnh hiển thị
  plt.title("Q-learning Success Rate vs EPISODES")
  plt.xlabel("EPISODES")
  plt.ylabel("SUCCESS RATE")
  plt.xticks(df['EPISODES'].unique())  # Hiển thị rõ các mốc EPISODES
  plt.grid(True)
  plt.legend()
  plt.tight_layout()
  plt.show()
