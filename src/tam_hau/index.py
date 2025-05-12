import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from .bfs import solve_bfs
from .dfs import solve_dfs
from .utils import *
from .Q_Learning.index import solve_q_learning, q_learning
from .Q_Learning.thong_ke import run_experiments, draw_graph
from .nhin_thay_mot_phan import solve_8_queens_nhin_thay_1_phan
from .ac3 import solve_8_queens_with_ac3

def clear(text):
  text.delete("1.0", tk.END)
def insert(text, message):
  text.insert("end", message)

def q_learning_model_window(text_1=None):
    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Q-Learning Model Generation")
    root.geometry("300x200")
    root.resizable(False, False)
    root.configure(bg="#f000ff")

    # Hàm thêm placeholder
    def add_placeholder(entry, placeholder_text):
        entry.insert(0, placeholder_text)
        entry.config(fg="grey")

        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, "end")
                entry.config(fg="black")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.config(fg="grey")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # Tạo các Entry với placeholder
    episodes = tk.Entry(root, width=35)
    add_placeholder(episodes, "Giá trị Episode (số lần luyện). vd: 5000")
    episodes.pack(pady=5)

    alpha = tk.Entry(root, width=35)
    add_placeholder(alpha, "Giá trị Alpha (tốc độ học). vd: 0.1")
    alpha.pack(pady=5)

    gamma = tk.Entry(root, width=35)
    add_placeholder(gamma, "Giá trị Gamma (hệ số giảm dần). vd: 0.9")
    gamma.pack(pady=5)

    epsilon = tk.Entry(root, width=35)
    add_placeholder(epsilon, "Giá trị Epsilon (tỷ lệ khám phá). vd: 0.1")
    epsilon.pack(pady=5)

    def gen_new_model_click():
        # Lấy giá trị từ các Entry
        episodes_value = int(episodes.get())
        alpha_value = float(alpha.get())
        gamma_value = float(gamma.get())
        epsilon_value = float(epsilon.get())

        # Gọi hàm q_learning với các tham số đã nhập
        q_learning(episodes=episodes_value, alpha=alpha_value, gamma=gamma_value, epsilon=epsilon_value)

        if text_1:
          # Hiển thị thông báo thành công
          insert(text_1, "Đã tạo Q-Learning Model mới thành công!\n")
    # Thêm nút xác nhận
    confirm_button = tk.Button(root, text="Tạo Q-Learning Model", command=gen_new_model_click)
    confirm_button.pack(pady=5)

    # Chạy vòng lặp chính của Tkinter
    root.mainloop()

def tam_hau():
  # Tạo cửa sổ chính
  root = tk.Tk()
  root.title("Menu Bài Toán Tám Hậu")
  root.geometry("400x300")
  root.resizable(False, False)
  root.configure(bg="#000fff")

  # Thêm Combobox để chọn
  options = ["Giải với BFS", "Giải với DFS", "Tạo Q-Learning Model mới", "Giải với Q-Learning"
             , "Thống kê Q-Learning với EPISODES và EPSILON", "Partial Observable Search",
             "Giải với AC-3 Backtracking"]
  combobox = ttk.Combobox(root, values=options, state="readonly")
  combobox.set("Chọn một tùy chọn")  # Thiết lập giá trị mặc định
  combobox.pack(pady=5)

  # Hàm xử lý khi nhấn nút xác nhận
  def confirm_selection():
    selected_option = combobox.get()
    # BFS
    if selected_option == "Giải với BFS":
      clear(text_1)
      insert(text_1, "Đang giải với BFS...\n")
      solve_bfs()
      data = read_lines_to_list()
      board = queen_board(data[0])
      insert(text_1, "Kết quả giải với BFS:\n")
      insert(text_1, "\n")
      insert(text_1, board)
      insert(text_1, "\n\n")
      insert(text_1, ">> Tổng số Node đã duyệt: " + data[1] + "\n")
      show_pygame_board(data[0])
    # DFS
    elif selected_option == "Giải với DFS":
      clear(text_1)
      insert(text_1, "Đang giải với DFS...\n")
      solve_dfs()
      data = read_lines_to_list()
      board = queen_board(data[0])
      insert(text_1, "Kết quả giải với DFS:\n")
      insert(text_1, "\n")
      insert(text_1, board)
      insert(text_1, "\n\n")
      insert(text_1, ">> Tổng số Node đã duyệt: " + data[1] + "\n")
      show_pygame_board(data[0])
    # Q-Learning Model mới
    elif selected_option == "Tạo Q-Learning Model mới":
      clear(text_1)
      insert(text_1, "Đang tạo Q-Learning Model mới...\n")
      q_learning_model_window(text_1)
    # Giải với Model hiện tại
    elif selected_option == "Giải với Q-Learning":
      clear(text_1)
      insert(text_1, "Đang giải với Q-Learning...\n")
      t = solve_q_learning(insert, clear, text_1)
      if t:
        data = read_lines_to_list()
        board = queen_board(data[0])
        insert(text_1, "Kết quả giải với Q-Learning model hiện tại:\n")
        insert(text_1, "\n")
        insert(text_1, board)
        insert(text_1, "\n\n")
        show_pygame_board(data[0])
    # Thống kê Q-Learning
    elif selected_option == "Thống kê Q-Learning với EPISODES và EPSILON":
      clear(text_1)
      insert(text_1, "Đang thống kê Q-Learning...\n")
      run_experiments()
      insert(text_1, "Đã thống kê Q-Learning thành công!\n")
      insert(text_1, "Đang vẽ biểu đồ...\n")
      draw_graph()
    # Partial Observable Search
    elif selected_option == "Partial Observable Search":
      clear(text_1)
      insert(text_1, "Đang giải với Partial Observable Search...\n")
      solve_8_queens_nhin_thay_1_phan()
      data = read_lines_to_list()
      board = queen_board(data[0])
      insert(text_1, "Kết quả giải với Nhìn thấy 1 phần:\n")
      insert(text_1, "\n")
      insert(text_1, board)
      insert(text_1, "\n\n")
      show_pygame_board(data[0])
    # Giải với AC-3 Backtracking
    elif selected_option == "Giải với AC-3 Backtracking":
      clear(text_1)
      insert(text_1, "Đang giải với AC-3 Backtracking...\n")
      solve_8_queens_with_ac3()
      data = read_lines_to_list()
      board = queen_board(data[0])
      insert(text_1, "Kết quả giải với AC-3 Backtracking:\n")
      insert(text_1, "\n")
      insert(text_1, board)
      insert(text_1, "\n\n")
      show_pygame_board(data[0])


      
    print(f"Giải Tám Hậu với: {selected_option}")

  # Thêm nút xác nhận
  confirm_button = tk.Button(root, text="Xác nhận", command=confirm_selection)
  confirm_button.pack(pady=5)

  # Scroll Text
  text_1 = ScrolledText(
      root,
      bd=0,
      bg="#000000",
      fg="#00FF00",
      highlightthickness=0
  )

  text_1.pack(pady=5, padx=10)

  # Chạy vòng lặp chính của Tkinter
  root.mainloop()