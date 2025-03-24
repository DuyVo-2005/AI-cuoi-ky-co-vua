import tkinter as tk
from PIL import Image, ImageTk
import os
from translation import translate
from tkinter import messagebox

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
        tk.Button(self, text=translate(language, "Người với máy"), font=("Times New Roman", 13), width=BUTTON_WIDTH).pack(pady=5)
        tk.Button(self, text=translate(language, "Máy với máy"), font=("Times New Roman", 13), width=BUTTON_WIDTH).pack(pady=5)
        
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