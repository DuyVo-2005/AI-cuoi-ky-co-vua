import pickle
import os
import random
from collections import defaultdict


BOARD_SIZE = 8
EPISODES = 5000
ALPHA = 0.1          # Learning rate
GAMMA = 0.9          # Discount factor
EPSILON = 0.1        # Exploration rate

# Hàm kiểm tra xem có xung đột khi đặt hậu ở cột col không
def is_safe(state, row, col):
    for r, c in enumerate(state):
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

def default_q_values():
    return [0.0 for _ in range(BOARD_SIZE)]

# >> Hàm huấn luyện Q-learning, tạo ra model và lưu file <<
def q_learning(episodes=EPISODES, alpha=ALPHA, gamma=GAMMA, epsilon=EPSILON):
  # Khởi tạo bảng Q: {(state): [q0, q1, ..., q7]}
  Q = defaultdict(default_q_values)

  for episode in range(episodes):
      state = tuple()
      total_reward = 0
      for row in range(BOARD_SIZE):
          # Chọn hành động: cột để đặt hậu
          if random.random() < epsilon: # Với xác suất EPSILON, ...
              action = random.randint(0, BOARD_SIZE - 1) # ... hoặc là hành động ngẫu nhiên (action = 1 ... 7)
          else:
              q_values = Q[state] # ... hoặc là chọn hành động tốt nhất theo Q-value hiện tại
              action = q_values.index(max(q_values))

          # Kiểm tra hành động có hợp lệ không
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

          # Cập nhật Q-value
          old_q = Q[state][action]
          if not done:
              max_future_q = max(Q[next_state])
          else:
              max_future_q = 0
          Q[state][action] = old_q + alpha * (reward + gamma * max_future_q - old_q)

          state = next_state
          total_reward += reward

          if done:
              break

  # Lưu trữ bảng Q vào file pkl
  base_dir = os.path.dirname(os.path.abspath(__file__))
  model_path = os.path.join(base_dir, 'q_learn_model.pkl')
  with open(model_path, 'wb') as f:
    pickle.dump(dict(Q), f)

# >> Hàm load model <<
def load_q_model():
    model_path = os.path.join(os.path.dirname(__file__), 'q_learn_model.pkl')
    with open(model_path, 'rb') as f:
        raw_q = pickle.load(f)
        Q = defaultdict(lambda: [0.0 for _ in range(8)], raw_q)
    return Q

if __name__ == "__main__":
    q_learning()
    print("Q-learning model has been generated and saved to 'q_learn_model.pkl'")

