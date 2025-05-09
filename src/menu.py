import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
from tkinter import scrolledtext
import subprocess
import pygame
import time

from translation import translate
from main_king import Main
from algorithm import *
from tam_hau.index import tam_hau
from ma_di_tuan import solve_knights_tour

BUTTON_WIDTH = 20
language = "Vietnamese"
DUONG_DAN_THU_MUC_HIEN_HANH = os.path.dirname(__file__)

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

        control_frame = tk.Frame(main_paned_window, bg="#FFCC33", padx=10, pady=10, width=200)
        control_frame.pack_propagate(False) 
        main_paned_window.add(control_frame, stretch="never") 

        tk.Label(control_frame, text=translate(language, "Mã Đi Tuần"), font=("Times New Roman", 16, "bold"), bg="#FFCC33", fg="#008080").pack(pady=(0, 10))

        self.solve_button = tk.Button(control_frame, text=translate(language, "Tìm đường đi"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=self.run_solver)
        self.solve_button.pack(pady=5)

        self.start_stop_button = tk.Button(control_frame, text=translate(language, "Bắt đầu Hoạt ảnh"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=self.start_stop_animation, state=tk.DISABLED)
        self.start_stop_button.pack(pady=5)

        tk.Label(control_frame, text=translate(language, "Tốc độ (ms/bước):"), font=("Times New Roman", 11), bg="#FFCC33").pack(pady=(10, 0))
        self.speed_scale = tk.Scale(control_frame, from_=50, to=1000, resolution=50, orient=tk.HORIZONTAL, bg="#FFCC33", highlightthickness=0, length=180, command=self.update_speed)
        self.speed_scale.set(self.delay_ms)
        self.speed_scale.pack(pady=0)

        self.status_label = tk.Label(control_frame, text="", font=("Times New Roman", 12), bg="#FFCC33", fg="blue", wraplength=180)
        self.status_label.pack(pady=10, fill=tk.X)

        back_button = tk.Button(control_frame, text=translate(language, "Quay lại"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(BotVSBotModeFrame))
        back_button.pack(side=tk.BOTTOM, pady=20)

        right_frame = tk.Frame(main_paned_window, bg="#FFCC33")
        main_paned_window.add(right_frame, stretch="always")

        board_canvas_frame = tk.Frame(right_frame, bg="#AAAAAA", padx=5, pady=5)
        board_canvas_frame.pack(pady=(5,0), fill=tk.X)

        self.canvas = tk.Canvas(board_canvas_frame, width=self.board_size_px, height=self.board_size_px, bg="white", highlightthickness=0)
        self.canvas.pack()

        list_frame = tk.Frame(right_frame, bg="#FFCC33", padx=5, pady=5)
        list_frame.pack(pady=5, fill="both", expand=True)

        tk.Label(list_frame, text=translate(language, "Các nước đã đi:"), font=("Times New Roman", 12, "bold"), bg="#FFCC33").pack(anchor="w")
        self.move_list_text = scrolledtext.ScrolledText(list_frame, height=6, width=50, state=tk.DISABLED, font=("Courier New", 10))
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
        if self.parent.solving_in_progress:
            return
        if self.animation_id:
            self.stop_animation_if_running()

        self.parent.solving_in_progress = True
        self.solve_button.config(state=tk.DISABLED)
        self.start_stop_button.config(state=tk.DISABLED, text=translate(language, "Bắt đầu Hoạt ảnh"))
        self.status_label.config(text=translate(language, "Đang tìm đường đi..."))
        self.draw_board() 
        self.update_idletasks()

        try:
            print("Bắt đầu giải Mã đi tuần...")
            start_time = time.time()
            self.solution_path = solve_knights_tour(self.board_dim)
            end_time = time.time()
            solve_time = end_time - start_time
            print(f"Giải xong trong {solve_time:.4f} giây.")

            if self.solution_path and len(self.solution_path) == self.board_dim * self.board_dim:
                self.status_label.config(text=translate(language, "Đã tìm thấy lời giải!") + f" ({solve_time:.2f}s)\n" + translate(language,"Sẵn sàng hoạt ảnh."))
                self.start_stop_button.config(state=tk.NORMAL) 
            else:
                self.status_label.config(text=translate(language, "Không tìm thấy lời giải.") + f" ({solve_time:.2f}s)")
                messagebox.showinfo(translate(language,"Thông báo"), translate(language,"Không tìm thấy lời giải cho Mã đi tuần."))
                self.solution_path = None 

        except Exception as e:
            self.status_label.config(text=translate(language, "Lỗi khi giải!"))
            messagebox.showerror(translate(language, "Lỗi Solver"), f"{translate(language, 'Có lỗi xảy ra khi chạy thuật toán Mã đi tuần')}:\n{e}")
            print(f"Lỗi khi giải Mã đi tuần: {e}")
            self.solution_path = None
        finally:
            self.parent.solving_in_progress = False
            self.solve_button.config(state=tk.NORMAL)

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
        duong_dan_hinh_nen_menu = DUONG_DAN_THU_MUC_HIEN_HANH + "/nen_menu.png"
        self.nen_menu = tk.PhotoImage(file=duong_dan_hinh_nen_menu) 
        label_nen_menu = tk.Label(self, image=self.nen_menu, bg="#FFCC33")
        label_nen_menu.pack(pady=5)

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
class ModeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#FFCC33"
        self.pack(pady=20)
        tk.Label(self, text=translate(language, "Chọn chế độ chơi"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#008080").pack(pady=10)
        tk.Button(self, text=translate(language, "Người với người"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=show_player_vs_player_screen).pack(pady=5)
        tk.Button(self, text=translate(language, "Người với máy"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=show_player_vs_bot_screen).pack(pady=5)
        tk.Button(self, text=translate(language, "Máy với máy"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(BotVSBotModeFrame)).pack(pady=5)



start_state_tuple = (0,0)

def show_king_tour_screen(algorthm_name: str, level: int):
    global start_state_tuple
    root = make_node(None, None, start_state_tuple)
    solution = None
    start_time = time.time()
    if algorthm_name == "BFS" or algorthm_name == "DFS":
        solution = uninformed_search(root, algorthm_name, level)
    elif algorthm_name == "UCS":
        solution = UCS(root, level)
    elif algorthm_name == "IDS":
        solution = IDS(root, level)
    elif algorthm_name == "A*":
        solution = A_start(root, level)
    elif algorthm_name == "IDA*":
        solution = IDA_star(root, level)
    elif algorthm_name == "Greedy":
        solution = Greedy(root, level)
    elif algorthm_name == "Simple hill climbing":
        solution = simple_hill_climbing(root, level)
    elif algorthm_name == "Steepest ascent hill climbing":
        solution = steepest_ascent_hill_climbing(root, level)
    elif algorthm_name == "Stochastic hill climbing":
        solution = stochastic_hill_climbing(root, level)
    elif algorthm_name =="Stimulated annealing":
        solution = stimulated_annealing(root, level)
    elif algorthm_name == "Beam search":
        solution = Beam_search(root, level)
    elif algorthm_name == "Genetic algorithm":
        solution = genetic_algorithm(root, level)
    end_time = time.time()
    if solution != None:
        if algorthm_name == "Genetic algorithm":
            messagebox.showinfo(translate(language, "Thông báo"), translate(language, "Tìm ra lời giải bằng Genetic algorithm"))
        else:
            print(f"Tên thuật toán: {algorthm_name}")
            print(f"Số bước di chuyển: {len(solution)}")
            print(f"Thời gian thực thi: {end_time - start_time:.9f} giây")
            print(f"Giải pháp: {solution}")
            main = Main()
            main.path = solution
            main.number_of_enermies = level
            main.mainloop()
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
                                    "Beam search", "Genetic algorithm"], width=BUTTON_WIDTH + 10)
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
    thu_muc_cha = DUONG_DAN_THU_MUC_HIEN_HANH.replace("\\src", "")
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