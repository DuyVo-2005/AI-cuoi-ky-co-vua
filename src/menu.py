import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
from tkinter import scrolledtext
import subprocess
import pygame
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from translation import translate
from algorithm import *
from tam_hau.index import tam_hau
from ma_di_tuan import solve_knights_tour_backtracking, solve_knights_tour_a_star
from king_and_pawn_move import enemy_capture_moves
from search_with_no_observation_algoritm import search_with_no_observation_solve

knights_tour_imported = True
BUTTON_WIDTH = 20
language = "Vietnamese"
CURRENT_DIRECTORY_PATH = os.path.dirname(__file__)

pygame.init()
pygame.mixer.init()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        CHIEU_RONG_MAN_HINH = self.winfo_screenwidth()
        CHIEU_DAI_MAN_HINH = self.winfo_screenheight()
        CHIEU_RONG_CUA_SO = 600
        CHIEU_DAI_CUA_SO = 600
        toa_do_x_man_hinh = (CHIEU_RONG_MAN_HINH // 2) - (CHIEU_RONG_CUA_SO // 2)
        toa_do_y_man_hinh = (CHIEU_DAI_MAN_HINH // 2) - (CHIEU_DAI_CUA_SO // 2)
        self.title(translate(language, "Trò chơi cờ vua"))
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_DAI_CUA_SO}+{toa_do_x_man_hinh}+{toa_do_y_man_hinh}")
        self["bg"] = "#FFCC33"
        self.current_frame = None
        self.solving_in_progress = False 
        self.show_frame(StartFrame)
        
    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = frame_name(self)
        self.current_frame.pack(fill="both", expand=True)

def coords_to_algebraic(row, col, board_dim=8):
    if 0 <= row < board_dim and 0 <= col < board_dim:
        return chr(ord('a') + col) + str(board_dim - row)
    return "??"

class KnightsTourFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self["bg"] = "#FFCC33"
        self.pack(fill="both", expand=True)

        self.board_size_px = 480
        self.board_dim = 8
        self.cell_size = self.board_size_px // self.board_dim
        self.solution_path = None
        self.animation_id = None
        self.current_step = 0
        self.knight_item = None
        self.drawn_animation_elements = []
        self.delay_ms = 250

        main_paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg="#FFCC33")
        main_paned_window.pack(fill="both", expand=True, padx=5, pady=5)

        control_frame = tk.Frame(main_paned_window, bg="#FFCC33", padx=10, pady=10, width=250)
        control_frame.pack_propagate(False)
        main_paned_window.add(control_frame, stretch="never")
        tk.Label(control_frame, text=translate(language, "Mã Đi Tuần"), font=("Times New Roman", 16, "bold"), bg="#FFCC33", fg="#008080").pack(pady=(0, 10))
        tk.Label(control_frame, text=translate(language, "Chọn thuật toán:"), font=("Times New Roman", 11), bg="#FFCC33").pack(pady=(5, 0), anchor='w')
        algorithm_options = ["Backtracking", "A*"]
        self.algorithm_ccb = ttk.Combobox(control_frame, values=algorithm_options, width=BUTTON_WIDTH + 5, state="readonly")
        self.algorithm_ccb.pack(pady=5, anchor='w')
        self.algorithm_ccb.current(0)

        solve_button_state = tk.NORMAL if knights_tour_imported else tk.DISABLED
        self.solve_button = tk.Button(control_frame, text=translate(language, "Tìm đường đi"), font=("Times New Roman", 13), width=BUTTON_WIDTH, state=solve_button_state, command=self.run_solver)
        self.solve_button.pack(pady=10) 

        self.start_stop_button = tk.Button(control_frame, text=translate(language, "Bắt đầu Hoạt ảnh"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=self.start_stop_animation, state=tk.DISABLED)
        self.start_stop_button.pack(pady=5) 

        tk.Label(control_frame, text=translate(language, "Tốc độ (ms/bước):"), font=("Times New Roman", 11), bg="#FFCC33").pack(pady=(10, 0), anchor='w') 
        self.speed_scale = tk.Scale(control_frame, from_=50, to=1000, resolution=50, orient=tk.HORIZONTAL, bg="#FFCC33", highlightthickness=0, length=200, command=self.update_speed) 
        self.speed_scale.set(self.delay_ms)
        self.speed_scale.pack(pady=0, anchor='w') 

        self.status_label = tk.Label(control_frame, text="", font=("Times New Roman", 12), bg="#FFCC33", fg="blue", wraplength=230, justify=tk.LEFT) 
        self.status_label.pack(pady=10, fill=tk.X, anchor='nw')

        back_button = tk.Button(control_frame, text=translate(language, "Quay lại"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(BotVSBotModeFrame))
        back_button.pack(side=tk.BOTTOM, pady=20)

        right_frame = tk.Frame(main_paned_window, bg="#FFCC33")
        main_paned_window.add(right_frame, stretch="always")

        board_canvas_frame = tk.Frame(right_frame, bg="#AAAAAA", padx=5, pady=5)
        board_canvas_frame.pack(pady=(5,0), padx=5) 

        self.canvas = tk.Canvas(board_canvas_frame, width=self.board_size_px, height=self.board_size_px, bg="white", highlightthickness=0)
        self.canvas.pack()

        list_frame = tk.Frame(right_frame, bg="#FFCC33", padx=5, pady=5)
        list_frame.pack(pady=5, padx=5, fill="both", expand=True)

        tk.Label(list_frame, text=translate(language, "Các nước đã đi:"), font=("Times New Roman", 12, "bold"), bg="#FFCC33").pack(anchor="w")
        self.move_list_text = scrolledtext.ScrolledText(list_frame, height=8, width=50, state=tk.DISABLED, font=("Courier New", 10))
        self.move_list_text.pack(fill="both", expand=True)

        self.draw_board() 


    def draw_board(self):
        self.canvas.delete("board_elements") 
        for row in range(self.board_dim):
            for col in range(self.board_dim):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "#FFFFFF" if (row + col) % 2 == 0 else "#D3D3D3"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags="board_elements")
        self.clear_animation_elements()

    def clear_animation_elements(self):
        if self.knight_item:
            self.canvas.delete(self.knight_item)
            self.knight_item = None
        for item_id in self.drawn_animation_elements:
            self.canvas.delete(item_id)
        self.drawn_animation_elements = []
        self.move_list_text.config(state=tk.NORMAL)
        self.move_list_text.delete('1.0', tk.END)
        self.move_list_text.config(state=tk.DISABLED)

    def update_speed(self, value):
        self.delay_ms = int(value)

    def run_solver(self):
        if not knights_tour_imported:
             messagebox.showerror("Lỗi.")
             return

        if self.parent.solving_in_progress:
            messagebox.showwarning(translate(language,"Cảnh báo"), translate(language,"Một thuật toán khác đang chạy, vui lòng đợi."))
            return

        if self.animation_id:
            self.stop_animation_if_running()

        selected_algorithm = self.algorithm_ccb.get()
        print(f"DEBUG: Selected algorithm: {selected_algorithm}")
        self.parent.solving_in_progress = True
        self.solve_button.config(state=tk.DISABLED)
        self.start_stop_button.config(state=tk.DISABLED, text=translate(language, "Bắt đầu Hoạt ảnh"))
        self.status_label.config(text=translate(language, f"Đang tìm đường đi bằng {selected_algorithm}..."))
        self.draw_board()
        self.update_idletasks()

        solution = None
        solve_time = 0
        try:
            start_time = time.time()

            self.solution_path = solve_knights_tour_backtracking(self.board_dim)
            if selected_algorithm == "Backtracking":
                solution = solve_knights_tour_backtracking(self.board_dim)
            elif selected_algorithm == "A*":
                solution = solve_knights_tour_a_star(self.board_dim)
            else:
                 messagebox.showerror("Lỗi", f"Thuật toán không hợp lệ: {selected_algorithm}")
                 self.parent.solving_in_progress = False
                 self.solve_button.config(state=tk.NORMAL)
                 self.status_label.config(text=translate(language, "Chọn thuật toán và nhấn Tìm đường đi."))
                 return 


            end_time = time.time()
            solve_time = end_time - start_time

            if isinstance(solution, list) and len(solution) == self.board_dim * self.board_dim:
                self.solution_path = solution
                self.status_label.config(text=translate(language, "Đã tìm thấy lời giải!") + f" ({solve_time:.2f}s)\n" + translate(language,"Sẵn sàng hoạt ảnh."))
                self.start_stop_button.config(state=tk.NORMAL)
            else:
                self.solution_path = None
                self.status_label.config(text=translate(language, "Không tìm thấy lời giải.") + f" ({solve_time:.2f}s)")
                if solution is not None:
                     print(f"DEBUG: Solver trả về kết quả không hợp lệ: {solution}")
                     messagebox.showwarning(translate(language,"Thông báo"), translate(language,"Thuật toán trả về kết quả không hợp lệ."))
                else:
                     messagebox.showinfo(translate(language,"Thông báo"), translate(language,"Không tìm thấy lời giải cho Mã đi tuần."))

        except Exception as e:
            self.solution_path = None
            self.status_label.config(text=translate(language, "Lỗi khi giải!"))
            messagebox.showerror(translate(language, "Lỗi giải thuật"), f"{translate(language, 'Có lỗi xảy ra khi chạy thuật toán Mã đi tuần')}:\n{e}")
            print(f"Lỗi Exception khi giải Mã đi tuần: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.parent.solving_in_progress = False
            self.solve_button.config(state=tk.NORMAL)
            print(f"DEBUG: Kết thúc run_solver. self.solution_path is None: {self.solution_path is None}")

    def start_stop_animation(self):
        if self.animation_id:
            self.stop_animation_if_running()
            self.status_label.config(text=translate(language, "Đã tạm dừng hoạt ảnh."))
        elif self.solution_path:
            self.clear_animation_elements() 
            self.current_step = 0
            self.start_stop_button.config(text=translate(language, "Dừng Hoạt ảnh"))
            self.status_label.config(text=translate(language, "Đang chạy hoạt ảnh..."))
            self.solve_button.config(state=tk.DISABLED)

            start_row, start_col = self.solution_path[0]
            start_x = start_col * self.cell_size + self.cell_size / 2
            start_y = start_row * self.cell_size + self.cell_size / 2
            self.knight_item = self.canvas.create_text(start_x, start_y, text="♞", font=("Arial", int(self.cell_size * 0.6)), fill="black")

            self.update_move_list(0, start_row, start_col)

            self.animation_id = self.canvas.after(self.delay_ms, self.animate_step)

    def animate_step(self):
        self.animation_id = None 

        next_step = self.current_step + 1
        if next_step < len(self.solution_path):
            
            prev_row, prev_col = self.solution_path[self.current_step]
            curr_row, curr_col = self.solution_path[next_step]

            prev_x_center = prev_col * self.cell_size + self.cell_size / 2
            prev_y_center = prev_row * self.cell_size + self.cell_size / 2
            curr_x_center = curr_col * self.cell_size + self.cell_size / 2
            curr_y_center = curr_row * self.cell_size + self.cell_size / 2

            if self.knight_item:
                self.canvas.coords(self.knight_item, curr_x_center, curr_y_center)

            num_id = self.canvas.create_text(curr_x_center, curr_y_center - self.cell_size * 0.3, 
                                             text=str(next_step + 1),
                                             font=("Arial", int(self.cell_size * 0.25)), fill="blue")
            self.drawn_animation_elements.append(num_id)

            line_id = self.canvas.create_line(prev_x_center, prev_y_center, curr_x_center, curr_y_center,
                                              fill="red", width=2, arrow=tk.LAST) 
            self.drawn_animation_elements.append(line_id)
            self.canvas.lower(line_id, self.knight_item) 

            self.update_move_list(next_step, curr_row, curr_col)


            self.current_step = next_step
            self.animation_id = self.canvas.after(self.delay_ms, self.animate_step)

        else:
            self.status_label.config(text=translate(language, "Hoạt ảnh hoàn thành!"))
            self.start_stop_button.config(text=translate(language, "Chạy lại Hoạt ảnh")) 
            self.solve_button.config(state=tk.NORMAL) 

    def update_move_list(self, step_index, row, col):
        notation = coords_to_algebraic(row, col, self.board_dim)
        move_text = f"{step_index + 1:>3}. {notation}\n" 
        self.move_list_text.config(state=tk.NORMAL)
        self.move_list_text.insert(tk.END, move_text)
        self.move_list_text.see(tk.END) 
        self.move_list_text.config(state=tk.DISABLED)

    def stop_animation_if_running(self):
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
            self.start_stop_button.config(text=translate(language, "Tiếp tục Hoạt ảnh")) 
            self.solve_button.config(state=tk.NORMAL) 


    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self["bg"] = "#FFCC33"
        self.pack(fill="both", expand=True)
        self.board_size_px = 480
        self.board_dim = 8
        self.cell_size = self.board_size_px // self.board_dim
        self.solution_path = None
        self.animation_id = None
        self.current_step = 0
        self.knight_item = None
        self.drawn_animation_elements = []
        self.delay_ms = 250
        main_paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg="#FFCC33")
        main_paned_window.pack(fill="both", expand=True, padx=5, pady=5)
        control_frame = tk.Frame(main_paned_window, bg="#FFCC33", padx=10, pady=10, width=250) 
        control_frame.pack_propagate(False)
        main_paned_window.add(control_frame, stretch="never")
        tk.Label(control_frame, text=translate(language, "Mã Đi Tuần"), font=("Times New Roman", 16, "bold"), bg="#FFCC33", fg="#008080").pack(pady=(0, 10))
        tk.Label(control_frame, text=translate(language, "Chọn thuật toán:"), font=("Times New Roman", 11), bg="#FFCC33").pack(pady=(5, 0), anchor='w')
        algorithm_options = ["Backtracking", "A*"]
        self.algorithm_ccb = ttk.Combobox(control_frame, values=algorithm_options, width=BUTTON_WIDTH + 5, state="readonly")
        self.algorithm_ccb.pack(pady=5, anchor='w')
        self.algorithm_ccb.current(0)

        solve_button_state = tk.NORMAL if knights_tour_imported else tk.DISABLED
        self.solve_button = tk.Button(control_frame, text=translate(language, "Tìm đường đi"), font=("Times New Roman", 13), width=BUTTON_WIDTH, state=solve_button_state, command=self.run_solver)
        self.solve_button.pack(pady=10) 
        self.start_stop_button = tk.Button(control_frame, text=translate(language, "Bắt đầu Hoạt ảnh"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=self.start_stop_animation, state=tk.DISABLED)
        self.start_stop_button.pack(pady=5) 

        tk.Label(control_frame, text=translate(language, "Tốc độ (ms/bước):"), font=("Times New Roman", 11), bg="#FFCC33").pack(pady=(10, 0), anchor='w') # Điều chỉnh pady, anchor nếu muốn
        self.speed_scale = tk.Scale(control_frame, from_=50, to=1000, resolution=50, orient=tk.HORIZONTAL, bg="#FFCC33", highlightthickness=0, length=200, command=self.update_speed) # Điều chỉnh length nếu muốn
        self.speed_scale.set(self.delay_ms)
        self.speed_scale.pack(pady=0, anchor='w') 

        self.status_label = tk.Label(control_frame, text="", font=("Times New Roman", 12), bg="#FFCC33", fg="blue", wraplength=230, justify=tk.LEFT) # Điều chỉnh wraplength, justify nếu muốn
        self.status_label.pack(pady=10, fill=tk.X, anchor='nw') 

        back_button = tk.Button(control_frame, text=translate(language, "Quay lại"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(BotVSBotModeFrame))
        back_button.pack(side=tk.BOTTOM, pady=20)

        right_frame = tk.Frame(main_paned_window, bg="#FFCC33")
        main_paned_window.add(right_frame, stretch="always")
        board_canvas_frame = tk.Frame(right_frame, bg="#AAAAAA", padx=5, pady=5)
        board_canvas_frame.pack(pady=(5,0), padx=5)

        self.canvas = tk.Canvas(board_canvas_frame, width=self.board_size_px, height=self.board_size_px, bg="white", highlightthickness=0)
        self.canvas.pack()

        list_frame = tk.Frame(right_frame, bg="#FFCC33", padx=5, pady=5)
        list_frame.pack(pady=5, padx=5, fill="both", expand=True)

        tk.Label(list_frame, text=translate(language, "Các nước đã đi:"), font=("Times New Roman", 12, "bold"), bg="#FFCC33").pack(anchor="w")
        self.move_list_text = scrolledtext.ScrolledText(list_frame, height=8, width=50, state=tk.DISABLED, font=("Courier New", 10))
        self.move_list_text.pack(fill="both", expand=True)

        self.draw_board()


    def draw_board(self):
        self.canvas.delete("board_elements") 
        for row in range(self.board_dim):
            for col in range(self.board_dim):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "#FFFFFF" if (row + col) % 2 == 0 else "#D3D3D3"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags="board_elements")
        self.clear_animation_elements()

    def clear_animation_elements(self):
        if self.knight_item:
            self.canvas.delete(self.knight_item)
            self.knight_item = None
        for item_id in self.drawn_animation_elements:
            self.canvas.delete(item_id)
        self.drawn_animation_elements = []
        self.move_list_text.config(state=tk.NORMAL)
        self.move_list_text.delete('1.0', tk.END)
        self.move_list_text.config(state=tk.DISABLED)

    def update_speed(self, value):
        self.delay_ms = int(value)

    def run_solver(self):
        """Lấy thuật toán đã chọn, gọi hàm giải và chuẩn bị cho animation."""
        if not knights_tour_imported:
             messagebox.showerror("Lỗi", "Module 'ma_di_tuan.py' chưa được tải.")
             return
        if self.parent.solving_in_progress:
            messagebox.showwarning(translate(language,"Cảnh báo"), translate(language,"Một thuật toán khác đang chạy, vui lòng đợi."))
            return
        if self.animation_id:
            self.stop_animation_if_running()
        selected_algorithm = self.algorithm_ccb.get()
        print(f"DEBUG: Selected algorithm: {selected_algorithm}")
        self.parent.solving_in_progress = True
        self.solve_button.config(state=tk.DISABLED)
        self.start_stop_button.config(state=tk.DISABLED, text=translate(language, "Bắt đầu Hoạt ảnh"))
        self.status_label.config(text=translate(language, f"Đang tìm đường đi bằng {selected_algorithm}..."))
        self.draw_board()
        self.update_idletasks()

        solution = None
        solve_time = 0
        try:
            start_time = time.time()
            if selected_algorithm == "Backtracking":
                solution = solve_knights_tour_backtracking(self.board_dim)
            elif selected_algorithm == "A*":
                solution = solve_knights_tour_a_star(self.board_dim)
            else:
                 messagebox.showerror("Lỗi", f"Thuật toán không hợp lệ: {selected_algorithm}")
                 self.parent.solving_in_progress = False
                 self.solve_button.config(state=tk.NORMAL)
                 self.status_label.config(text=translate(language, "Chọn thuật toán và nhấn Tìm đường đi."))
                 return 
            end_time = time.time()
            solve_time = end_time - start_time
            if isinstance(solution, list) and len(solution) == self.board_dim * self.board_dim:
                self.solution_path = solution
                self.status_label.config(text=translate(language, "Đã tìm thấy lời giải!") + f" ({solve_time:.2f}s)\n" + translate(language,"Sẵn sàng hoạt ảnh."))
                self.start_stop_button.config(state=tk.NORMAL)
            else:
                self.solution_path = None
                self.status_label.config(text=translate(language, "Không tìm thấy lời giải.") + f" ({solve_time:.2f}s)")
                if solution is not None:
                     print(f"DEBUG: Solver trả về kết quả không hợp lệ: {solution}")
                     messagebox.showwarning(translate(language,"Thông báo"), translate(language,"Thuật toán trả về kết quả không hợp lệ."))
                else:
                     messagebox.showinfo(translate(language,"Thông báo"), translate(language,"Không tìm thấy lời giải cho Mã đi tuần."))

        except Exception as e:
            self.solution_path = None
            self.status_label.config(text=translate(language, "Lỗi khi giải!"))
            messagebox.showerror(translate(language, "Lỗi Solver"), f"{translate(language, 'Có lỗi xảy ra khi chạy thuật toán Mã đi tuần')}:\n{e}")
            print(f"Lỗi Exception khi giải Mã đi tuần: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.parent.solving_in_progress = False
            self.solve_button.config(state=tk.NORMAL)
            print(f"DEBUG: Kết thúc run_solver. self.solution_path is None: {self.solution_path is None}")



    def start_stop_animation(self):
        if self.animation_id:
            self.stop_animation_if_running()
            self.status_label.config(text=translate(language, "Đã tạm dừng hoạt ảnh."))
        elif self.solution_path:
            self.clear_animation_elements() 
            self.current_step = 0
            self.start_stop_button.config(text=translate(language, "Dừng Hoạt ảnh"))
            self.status_label.config(text=translate(language, "Đang chạy hoạt ảnh..."))
            self.solve_button.config(state=tk.DISABLED)

            start_row, start_col = self.solution_path[0]
            start_x = start_col * self.cell_size + self.cell_size / 2
            start_y = start_row * self.cell_size + self.cell_size / 2
            self.knight_item = self.canvas.create_text(start_x, start_y, text="♞", font=("Arial", int(self.cell_size * 0.6)), fill="black")

            self.update_move_list(0, start_row, start_col)

            self.animation_id = self.canvas.after(self.delay_ms, self.animate_step)

    def animate_step(self):
        self.animation_id = None 

        next_step = self.current_step + 1
        if next_step < len(self.solution_path):
            
            prev_row, prev_col = self.solution_path[self.current_step]
            curr_row, curr_col = self.solution_path[next_step]

            prev_x_center = prev_col * self.cell_size + self.cell_size / 2
            prev_y_center = prev_row * self.cell_size + self.cell_size / 2
            curr_x_center = curr_col * self.cell_size + self.cell_size / 2
            curr_y_center = curr_row * self.cell_size + self.cell_size / 2

            if self.knight_item:
                self.canvas.coords(self.knight_item, curr_x_center, curr_y_center)

            num_id = self.canvas.create_text(curr_x_center, curr_y_center - self.cell_size * 0.3, 
                                             text=str(next_step + 1),
                                             font=("Arial", int(self.cell_size * 0.25)), fill="blue")
            self.drawn_animation_elements.append(num_id)

            line_id = self.canvas.create_line(prev_x_center, prev_y_center, curr_x_center, curr_y_center,
                                              fill="red", width=2, arrow=tk.LAST) 
            self.drawn_animation_elements.append(line_id)
            self.canvas.lower(line_id, self.knight_item) 

            self.update_move_list(next_step, curr_row, curr_col)


            self.current_step = next_step
            self.animation_id = self.canvas.after(self.delay_ms, self.animate_step)

        else:
            self.status_label.config(text=translate(language, "Hoạt ảnh hoàn thành!"))
            self.start_stop_button.config(text=translate(language, "Chạy lại Hoạt ảnh")) 
            self.solve_button.config(state=tk.NORMAL) 

    def update_move_list(self, step_index, row, col):
        notation = coords_to_algebraic(row, col, self.board_dim)
        move_text = f"{step_index + 1:>3}. {notation}\n" 
        self.move_list_text.config(state=tk.NORMAL)
        self.move_list_text.insert(tk.END, move_text)
        self.move_list_text.see(tk.END) 
        self.move_list_text.config(state=tk.DISABLED)

    def stop_animation_if_running(self):
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
            self.start_stop_button.config(text=translate(language, "Tiếp tục Hoạt ảnh")) 
            self.solve_button.config(state=tk.NORMAL) 


def set_English_and_go_to_home_frame(parent):
    global language
    language = "English"
    parent.show_frame(HomeFrame)
    parent.title(translate(language, "Trò chơi cờ vua"))
    
def set_Vietnamese_and_go_to_home_frame(parent):
    global language
    language = "Vietnamese"
    parent.show_frame(HomeFrame)
    
class StartFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#FFCC33"
        tk.Label(self, text="Chọn ngôn ngữ (Select language): ", font=("Times New Roman", 15, "bold"), width=30, fg="#008080", bg="#FFCC33").pack(pady=10)
        tk.Button(self, text="Tiếng Việt", font=("Times New Roman", 13), command=lambda: set_Vietnamese_and_go_to_home_frame(parent), width= 20).pack(pady=5)
        tk.Button(self, text="English", font=("Times New Roman", 13), command=lambda: set_English_and_go_to_home_frame(parent), width= 20).pack(pady=5)
        
class HomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#FFCC33"
        tk.Label(self, text=translate(language, "Chào mừng đến với trò chơi cờ vua AI"), font=("Times New Roman", 15, "bold"), width=30, fg="#008080", bg="#FFCC33").pack(pady=10)
        tk.Button(self, text=translate(language, "Bắt đầu trò chơi"), font=("Times New Roman", 13), command=lambda: parent.show_frame(MenuFrame), width=BUTTON_WIDTH).pack(pady=5)       
        duong_dan_hinh_nen_menu = CURRENT_DIRECTORY_PATH + "/nen_menu.png"
        self.nen_menu = tk.PhotoImage(file=duong_dan_hinh_nen_menu) 
        label_nen_menu = tk.Label(self, image=self.nen_menu, bg="#FFCC33")
        label_nen_menu.pack(pady=5)

class ChartFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self["bg"] = "#FFCC33"
        self.pack(fill="both", expand=True)

        self.df = None 
        self.load_data() 

        control_panel = tk.Frame(self, bg="#FFCC33", padx=10, pady=10)
        control_panel.pack(side=tk.TOP, fill=tk.X)

        tk.Label(control_panel, text=translate(language, "Chọn tiêu chí:"), font=("Times New Roman", 12), bg="#FFCC33").pack(side=tk.LEFT, padx=(0, 5))
        self.criteria_ccb = ttk.Combobox(control_panel, values=[translate(language, "Thời gian thực thi"), translate(language, "Số bước di chuyển")], width=25, state="readonly")
        self.criteria_ccb.pack(side=tk.LEFT, padx=(0, 15))
        self.criteria_ccb.current(0) 

        tk.Label(control_panel, text=translate(language, "Chọn Level:"), font=("Times New Roman", 12), bg="#FFCC33").pack(side=tk.LEFT, padx=(0, 5))
        available_levels = self.df['Level'].unique().tolist() if self.df is not None and 'Level' in self.df.columns else ["LEVEL 1", "LEVEL 2", "LEVEL 3", "LEVEL 4"]
        self.level_ccb = ttk.Combobox(control_panel, values=available_levels, width=15, state="readonly")
        self.level_ccb.pack(side=tk.LEFT, padx=(0, 15))
        if available_levels: self.level_ccb.current(0) 

        draw_button_state = tk.NORMAL if self.df is not None else tk.DISABLED 
        self.draw_button = tk.Button(control_panel, text=translate(language, "Vẽ biểu đồ"), font=("Times New Roman", 11), command=self.draw_chart, state=draw_button_state)
        self.draw_button.pack(side=tk.LEFT, padx=(0, 15))
        back_button = tk.Button(control_panel, text=translate(language, "Quay lại Menu"), font=("Times New Roman", 11), command=lambda: parent.show_frame(MenuFrame))
        back_button.pack(side=tk.LEFT)

        self.chart_container_frame = tk.Frame(self, bg="white")
        self.chart_container_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = None 
        self.toolbar = None 

    def load_data(self):
        try:
            data_path = os.path.join(CURRENT_DIRECTORY_PATH, 'data.csv')
            self.df = pd.read_csv(data_path)
            print(f"DEBUG: Đã tải dữ liệu từ {data_path}. Số dòng: {len(self.df)}")
            if not all(col in self.df.columns for col in ['Level', 'Tên thuật toán', 'Thời gian thực thi', 'Số bước di chuyển']):
                 print("Cảnh báo: File data.csv thiếu các cột cần thiết ('Level', 'Tên thuật toán', 'Thời gian thực thi', 'Số bước di chuyển').")
                 self.df = None
        except FileNotFoundError:
            messagebox.showerror(translate(language, "Lỗi File"), translate(language, "Không tìm thấy file 'data.csv'. Hãy đảm bảo file này nằm cùng thư mục với menu.py"))
            print("ERROR: File data.csv not found.")
            self.df = None
        except Exception as e:
            messagebox.showerror(translate(language, "Lỗi Đọc File"), f"{translate(language, 'Lỗi khi đọc file data.csv')}: {e}")
            print(f"ERROR: Error reading data.csv: {e}")
            self.df = None

    def clear_chart(self):
        if self.toolbar:
            self.toolbar.destroy()
            self.toolbar = None
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
    def draw_chart(self):
        if self.df is None:
            messagebox.showwarning(translate(language, "Thiếu dữ liệu"), translate(language, "Không có dữ liệu để vẽ biểu đồ. Vui lòng kiểm tra file data.csv."))
            return
        selected_criteria_text = self.criteria_ccb.get()
        selected_level = self.level_ccb.get()
        criteria_map = {
            translate(language, "Thời gian thực thi"): 'Thời gian thực thi',
            translate(language, "Số bước di chuyển"): 'Số bước di chuyển'
        }
        selected_column = criteria_map.get(selected_criteria_text)

        if selected_column is None:
             messagebox.showerror(translate(language, "Lỗi Lựa chọn"), translate(language, "Tiêu chí lựa chọn không hợp lệ."))
             print(f"ERROR: Invalid criteria selected: {selected_criteria_text}")
             return 

        df_level = self.df[self.df['Level'] == selected_level].copy()

        if df_level.empty:
            messagebox.showinfo(translate(language, "Không có dữ liệu"), f"{translate(language, 'Không tìm thấy dữ liệu cho')}: {selected_level}")
            print(f"DEBUG: No data found for level: {selected_level}")
            self.clear_chart() 
            return

        algorithm_names = df_level['Tên thuật toán']
        metric_values = df_level[selected_column]

        self.clear_chart()
        self.fig = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        bars = self.ax.bar(algorithm_names, metric_values, color='skyblue') 
        for bar in bars:
            yval = bar.get_height()
            format_string = "%.4f" if selected_column == 'Thời gian thực thi' else "%d"
            self.ax.text(bar.get_x() + bar.get_width()/2.0, yval, format_string % yval, va='bottom', ha='center', fontsize=8) 

        self.ax.set_xlabel(translate(language, "Tên thuật toán"))
        self.ax.set_ylabel(selected_criteria_text) 
        self.ax.set_title(f"{translate(language, 'So sánh')} {selected_criteria_text} - {selected_level}")

        plt.setp(self.ax.get_xticklabels(), rotation=45, ha="right")

        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_container_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.chart_container_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()
     


class MusicFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#FFCC33"
        tk.Label(self, text=translate(language, "Bật nhạc nền?"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#008080").pack(pady=10)
        tk.Button(self, text=translate(language, "Bật"), font=("Times New Roman", 15), width=15, command=turn_on_music).pack(pady=5)
        tk.Button(self, text=translate(language, "Tắt"), font=("Times New Roman", 15), width=15, command=turn_off_music).pack(pady=5)
        tk.Button(self, text=translate(language, "Về menu"), font=("Times New Roman", 15), width=15, command = lambda: parent.show_frame(MenuFrame)).pack(pady=5)
        

class MenuFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#FFCC33"
        self.pack(pady=20)
        tk.Button(self, text=translate(language, "Chơi ngay"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(ModeFrame)).pack(pady=5)
        #tk.Button(self, text=translate(language, "Thành tích"), font=("Times New Roman", 13), width=BUTTON_WIDTH).pack(pady=5)
        tk.Button(self, text=translate(language, "Nhạc nền"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(MusicFrame)).pack(pady=5)
        tk.Button(self, text=translate(language, "Thông tin"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(InfoFrame)).pack(pady=5)
        tk.Button(self, text=translate(language, "Vẽ biểu đồ"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(ChartFrame)).pack(pady=5)
        tk.Button(self, text=translate(language, "Thoát"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=close_game).pack(pady=5)

class InfoFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#FFCC33"
        self.pack(pady=20)
        tk.Label(self, text=translate(language, "Thông tin chung"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#008080").pack(pady=10)
        tk.Label(self, text=translate(language, "GVHD: TS. Phan Thị Huyền Trang"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#FFFFFF").pack(pady=10)
        tk.Label(self, text=translate(language, "Thành viên nhóm"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#008080").pack(pady=10)
        tk.Label(self, text=translate(language, "Vũ Anh Quốc - Nhóm trưởng"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#FFFFFF").pack(pady=10)
        tk.Label(self, text=translate(language, "Võ Lê Khánh Duy"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#FFFFFF").pack(pady=10)
        tk.Label(self, text=translate(language, "Phan Đình Sáng"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#FFFFFF").pack(pady=10)
        tk.Button(self, text=translate(language, "Về menu"), font=("Times New Roman", 15), width=15, command = lambda: parent.show_frame(MenuFrame)).pack(pady=5)

class ModeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#FFCC33"
        self.pack(pady=20)
        tk.Label(self, text=translate(language, "Chọn chế độ chơi"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#008080").pack(pady=10)
        tk.Button(self, text=translate(language, "Người với người"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=show_player_vs_player_screen).pack(pady=5)
        tk.Button(self, text=translate(language, "Người với máy"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=show_player_vs_bot_screen).pack(pady=5)
        tk.Button(self, text=translate(language, "Máy với máy"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(BotVSBotModeFrame)).pack(pady=5)
        tk.Button(self, text=translate(language, "Về menu"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command = lambda: parent.show_frame(MenuFrame)).pack(pady=5)

start_state_tuple = (0,0)

def show_king_tour_screen(algorthm_name: str, level: int):
    def play_king_animation(path: list, enemies_positions: list, is_complex_environmnet: bool = False):
        SQSIZE = 75
        COLS = 18
        ROWS = 9
        WIDTH = SQSIZE * COLS
        HEIGHT = SQSIZE * ROWS

        king_img = pygame.image.load("assets/images/imgs-80px/white_king.png")
        enemies_img = pygame.image.load("assets/images/imgs-80px/black_pawn.png")
        attack_cell_img = pygame.image.load("assets/images/attack.png")

        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vua tẩu thoát")

        WHITE = (255, 255, 255)
        LIGHT_GREEN = (119, 154, 88)

        def draw_board():
            for row in range(ROWS):
                for col in range(COLS):
                    color = WHITE if (row + col) % 2 == 0 else LIGHT_GREEN
                    rect = pygame.Rect(col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                    pygame.draw.rect(screen, color, rect)
        
        def draw_image(pos, image):
            x = pos[1] * SQSIZE
            y = pos[0] * SQSIZE
            screen.blit(image, (x, y))

        if not is_complex_environmnet:
            for pos in path:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                screen.fill((0, 0, 0))
                draw_board()
                draw_image(pos, king_img)
                for enemy_pos in enemies_positions:
                    draw_image(enemy_pos, enemies_img)
                    for attack_pos in enemy_capture_moves(enemy_pos):
                        draw_image(attack_pos, attack_cell_img)
                pygame.display.flip()
                time.sleep(0.75)#Delay các bước 0.75 giây
        else:
            display_path= path[0] + path[1]
            for pos in range(len(path[0])):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                screen.fill((0, 0, 0))
                draw_board()
                draw_image(display_path[pos], king_img)
                draw_image(display_path[pos + len(path[0]) - 1], king_img)
                for enemy_pos in enemies_positions:
                    draw_image(enemy_pos, enemies_img)
                    for attack_pos in enemy_capture_moves(enemy_pos):
                        draw_image(attack_pos, attack_cell_img)
                pygame.display.flip()
                time.sleep(0.75)#Delay các bước 0.75 giây          

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
        pygame.quit()
    global start_state_tuple
    enimies_positions = []
    if level >= 1:
        enimies_positions.append((4,4)) #[(4,4),(3,3),(3,5),(5,3),(5,5)]
        enimies_positions.append((6,6))
    if level >= 2:
        enimies_positions.append((1,6))
        enimies_positions.append((3,8))
    if level >= 3:
        enimies_positions.append((6,1))
        enimies_positions.append((2,11))
    if level == 4:
        enimies_positions.append((5,12))
        enimies_positions.append((8,10))
    pos_not_move = []
    pos_not_move = enimies_positions.copy()
    for pos in enimies_positions:
        pos_not_move += enemy_capture_moves(pos)
    root = make_node(None, None, start_state_tuple)
    solution = None
    solution2 = None
    start_time = time.perf_counter()
    if algorthm_name == "Search with no observation":
        #Tập trạng thái khởi tạo
        initial_belief_set = [
            (0,0),
            (1,1)
        ]
        solution, solution2 = search_with_no_observation_solve(initial_belief_set, pos_not_move)
    elif algorthm_name == "BFS" or algorthm_name == "DFS":
        solution = uninformed_search(root, algorthm_name, pos_not_move)
    elif algorthm_name == "UCS":
        solution = UCS(root, pos_not_move)
    elif algorthm_name == "IDS":
        solution = IDS(root, pos_not_move)
    elif algorthm_name == "A*":
        solution = A_start(root, pos_not_move)
    elif algorthm_name == "IDA*":
        solution = IDA_star(root, pos_not_move)
    elif algorthm_name == "Greedy":
        solution = Greedy(root, pos_not_move)
    elif algorthm_name == "Simple hill climbing":
        solution = simple_hill_climbing(root, pos_not_move)
    elif algorthm_name == "Steepest ascent hill climbing":
        solution = steepest_ascent_hill_climbing(root, pos_not_move)
    elif algorthm_name == "Stochastic hill climbing":
        solution = stochastic_hill_climbing(root, pos_not_move)
    elif algorthm_name =="Stimulated annealing":
        solution = stimulated_annealing(root, pos_not_move)
    elif algorthm_name == "Beam search":
        solution = Beam_search(root, pos_not_move)
    elif algorthm_name == "Genetic algorithm":
        solution = genetic_algorithm(root, pos_not_move)
    end_time = time.perf_counter()
    
    if solution != None:
        print(f"Tên thuật toán: {algorthm_name}")
        print(f"Thời gian thực thi: {end_time - start_time:.9f} giây")
        print(f"Số bước di chuyển: {len(solution)}")
        if algorthm_name == "Search with no observation":
            print("Giải pháp:")
            print(solution)
            print(solution2)
            play_king_animation([solution, solution2], enimies_positions, is_complex_environmnet=True)
        else:
            if algorthm_name == "Genetic algorithm":
                messagebox.showinfo(translate(language, "Thông báo"), translate(language, "Tìm ra lời giải bằng Genetic algorithm"))
            else:                                     
                print(f"Giải pháp: {solution}")
                play_king_animation(solution, enimies_positions)
    else:
        messagebox.showinfo(translate(language, "Thông báo"), translate(language, "Không tìm ra lời giải"))
        
def show_player_vs_bot_screen():
    subprocess.run(["python", "src/main.py"])# hoặc "python3"
    
def show_player_vs_player_screen():
    subprocess.run(["python", "src/main_player_vs_player.py"])
   
class BotVSBotModeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#FFCC33"
        self.pack(pady=20)
        tk.Label(self, text=translate(language, "Chọn chế độ chơi"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#008080").pack(pady=10)
        tk.Button(self, text=translate(language, "Cuộc tẩu thoát của vua"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(KingBotSetupFrame)).pack(pady=5)
        tk.Button(self, text=translate(language, "Quân tám hậu"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: tam_hau()).pack(pady=5)
        tk.Button(self, text=translate(language, "Mã đi tuần"), font=("Times New Roman", 13), width=BUTTON_WIDTH, 
                  command=lambda: parent.show_frame(KnightsTourFrame)).pack(pady=5)

algorthm_name = None

class KingBotSetupFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#FFCC33"
        self.pack(pady=20)
        tk.Label(self, text=translate(language, "Chọn tên thuật toán"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#008080").pack(pady=10)
        self.algorithm_type_ccb = ttk.Combobox(self, values=["BFS", "DFS", "UCS", "IDS", "Greedy", "A*", "IDA*", "Simple hill climbing",
                                    "Steepest ascent hill climbing", "Stochastic hill climbing", "Stimulated annealing",
                                    "Beam search", "Genetic algorithm", "Search with no observation"], width=BUTTON_WIDTH + 10)
        self.algorithm_type_ccb.pack(pady=5)
        self.algorithm_type_ccb.current(0)
        tk.Label(self, text=translate(language, "Chọn cấp độ"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#008080").pack(pady=10)
        self.level_ccb = ttk.Combobox(self, values=["1", "2", "3", "4"], width=BUTTON_WIDTH + 10)
        self.level_ccb.pack(pady=5)
        self.level_ccb.current(0)
        tk.Button(self, text=translate(language, "Giải"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=self.load_algorithm).pack(pady=5)
    def load_algorithm(self):
        show_king_tour_screen(self.algorithm_type_ccb.get(), int(self.level_ccb.get()))
        
def turn_on_music():
    thu_muc_cha = CURRENT_DIRECTORY_PATH.replace("\\src", "")
    duong_dan_file_nhac = thu_muc_cha + "\\assets\\sounds\\background_music.mp3"
    pygame.mixer.music.load(duong_dan_file_nhac)
    pygame.mixer.music.play(-1)#-1: phát lặp lại vô hạn
    
def turn_off_music():  
    pygame.mixer.music.stop()
    
def close_game():
    global app
    if messagebox.askokcancel(translate(language, "Thoát"), translate(language, "Bạn có muốn thoát?")):
        app.destroy()
app = MainApp()
app.mainloop()