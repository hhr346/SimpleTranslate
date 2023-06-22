import gc
import time
from tkinter import Tk, Menu
from turtle import window_height
from keyboard import add_hotkey, wait
from core import Layout
from threading import Thread


# 翻译主窗口
def startTran():

    root = Tk()
    root.title("SimpleTranslate")
    root.attributes('-topmost', True)

    # Set the window size and the location
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 120
    root.geometry(f"{window_width}x{window_height}+{screen_width-window_width-10}+{screen_height-window_height-80}")

    Layout.Layout(root)
    root.mainloop()


if __name__ == '__main__':
    try:
        start_thread = Thread(target=startTran)
        start_thread.start()
    except:
        del start_thread
        gc.collect()
