import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import subprocess

from translation import translate
from main_king import Main
from algorithm import *

BUTTON_WIDTH = 20
language = "Vietnamese"
play_music = False

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
        self.show_frame(StartFrame)
        
    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = frame_name(self)
        self.current_frame.pack(fill="both", expand=True)

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
        DUONG_DAN_THU_MUC_HIEN_HANH = os.path.dirname(__file__)
        duong_dan_hinh_nen_menu = DUONG_DAN_THU_MUC_HIEN_HANH + "/nen_menu.png"
        self.nen_menu = tk.PhotoImage(file=duong_dan_hinh_nen_menu) # Lưu tham chiếu nền menu của windows
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
        tk.Button(self, text=translate(language, "Thành tích"), font=("Times New Roman", 13), width=BUTTON_WIDTH).pack(pady=5)
        tk.Button(self, text=translate(language, "Nhạc nền"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(MusicFrame)).pack(pady=5)
        tk.Button(self, text=translate(language, "Thông tin"), font=("Times New Roman", 13), width=BUTTON_WIDTH).pack(pady=5)
        tk.Button(self, text=translate(language, "Thoát"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=close_game).pack(pady=5)

class ModeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#FFCC33"
        self.pack(pady=20)
        tk.Label(self, text=translate(language, "Chọn chế độ chơi"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#008080").pack(pady=10)
        tk.Button(self, text=translate(language, "Người với người"), font=("Times New Roman", 13), width=BUTTON_WIDTH).pack(pady=5)
        tk.Button(self, text=translate(language, "Người với máy"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=show_player_vs_bot_screen).pack(pady=5)
        tk.Button(self, text=translate(language, "Máy với máy"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(BotVSBotModeFrame)).pack(pady=5)

start_state_tuple = (0,0)

def show_king_tour_screen(algorthm_name: str, level: int):
    global start_state_tuple
    root = make_node(None, None, start_state_tuple)
    solution = None
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
    if solution != None:
        if algorthm_name == "Genetic algorithm":
            messagebox.showinfo(translate(language, "Thông báo"), translate(language, "Tìm ra lời giải bằng Genetic algorithm"))
        else:
            print(f"Số bước di chuyển: {len(solution)}")
            main = Main()
            main.path = solution
            main. number_of_enermies = level
            main.mainloop()
    else:
        messagebox.showinfo(translate(language, "Thông báo"), translate(language, "Không tìm ra lời giải"))
        
def show_player_vs_bot_screen():
    subprocess.run(["python", "src/main.py"])# hoặc "python3"
   
class BotVSBotModeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#FFCC33"
        self.pack(pady=20)
        tk.Label(self, text=translate(language, "Chọn chế độ chơi"), font=("Times New Roman", 15, "bold"), bg = "#FFCC33", fg="#008080").pack(pady=10)
        tk.Button(self, text=translate(language, "Cuộc tẩu thoát của vua"), font=("Times New Roman", 13), width=BUTTON_WIDTH, command=lambda: parent.show_frame(BotVSBotSetupFrame)).pack(pady=5)
        tk.Button(self, text=translate(language, "Quân tám hậu"), font=("Times New Roman", 13), width=BUTTON_WIDTH).pack(pady=5)
        tk.Button(self, text=translate(language, "Sáng"), font=("Times New Roman", 13), width=BUTTON_WIDTH).pack(pady=5)

algorthm_name = None

class BotVSBotSetupFrame(tk.Frame):
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
    global play_music
    play_music = True
    
def turn_off_music():
    global play_music
    play_music = False
def close_game():
    global app
    if messagebox.askokcancel(translate(language, "Thoát"), translate(language, "Bạn có muốn thoát?")):
        app.destroy()
app = MainApp()
app.mainloop()