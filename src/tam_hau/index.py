import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from .bfs import solve_bfs
from .dfs import solve_dfs
from .utils import *

def clear(text):
  text.delete("1.0", tk.END)
def insert(text, message):
  text.insert("end", message)

def tam_hau():
  # Tạo cửa sổ chính
  root = tk.Tk()
  root.title("Menu Bài Toán Tám Hậu")
  root.geometry("400x300")
  root.resizable(False, False)
  root.configure(bg="#000fff")

  # Thêm Combobox để chọn
  options = ["Giải với BFS", "Giải với DFS"]
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