import tkinter as tk
from pydub import AudioSegment
from pydub.generators import WhiteNoise
from pydub.playback import play
import threading
import pystray
from PIL import Image

# 创建噪音
def create_noise():
    noise = AudioSegment.silent(duration=50000, frame_rate=44100) #无声噪音
    #noise = WhiteNoise().to_audio_segment(duration=1000)    #有声噪音,调试用的
    return noise

# 播放噪音
def play_noise(noise):
    global is_playing
    while is_playing:
        play(noise)

# 创建GUI界面
def create_gui():
    global is_playing
    window = tk.Tk()
    window.title("Bluetooth Headset Keeper")
    window.geometry("200x100")

    def play():
        global is_playing
        is_playing = True
        threading.Thread(target=play_noise, args=(create_noise(),)).start()

    def stop():
        global is_playing
        is_playing = False

    tk.Button(window, text="Play", command=play).pack()
    tk.Button(window, text="Stop", command=stop).pack()
    tk.Button(window, text="Exit", command=exit_program).pack()

    window.mainloop()

# 退出程序
def exit_program(icon, item):
    icon.stop()

# 创建系统托盘图标
def create_tray_icon():
    global icon
    image = Image.open("icon.png")
    menu = (pystray.MenuItem("Open", create_gui), pystray.MenuItem("Exit", exit_program))
    icon = pystray.Icon("Bluetooth Headset Keeper", image, "Bluetooth Headset Keeper", menu)
    icon.run()

is_playing = False
create_tray_icon()