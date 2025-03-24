translations = {
    "Trò chơi cờ vua": "Chess game",
    "Chào mừng đến với trò chơi cờ vua AI": "Welcome to AI chess game",
    "Bắt đầu trò chơi": "Start game",
    "Chơi ngay": "Play now",
    "Thành tích": "Archiment",
    "Nhạc nền": "Music",
    "Bật nhạc nền?": "Turn on music?",
    "Bật": "On",
    "Tắt": "Off",
    "Thông tin": "About",
    "Thoát": "Exit",
    "Về menu": "Go to menu",
    "Bạn có muốn thoát?": "Do you want to exit?",
    "Chọn chế độ chơi": "Chose your play mode",
    "Người với người": "Player vs player",
    "Người với máy": "Player vs bot",
    "Máy với máy": "Bot vs bot"
}
    
def translate(language:str, text:str)->str:
    if language == "English":
        return translations.get(text, text)
    return text