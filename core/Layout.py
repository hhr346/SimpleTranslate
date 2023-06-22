from logging import root
import subprocess
import time
import tkinter as tk
import keyboard
from tkinter import Tk, Label, Button, Entry, END, Toplevel, Menu
from PIL import Image, ImageTk
from core import fanyi

a = fanyi.Translation()
class Layout():

    def __init__(self, root):

        # Set the entries
        Label(root, text="Input:").grid(row=0)
        Label(root, text="Output:").grid(row=1)
        self.e1 = Entry(root)
        self.e2 = Entry(root)
        self.e1.grid(row=0, column=1, padx=10, pady=5)
        self.e2.grid(row=1, column=1, padx=10, pady=5)
        self.e1.focus_set() # Set the focus on the input

        # Set the buttons in the bottom 
        self.bt1 = Button(root, text="Go", width=6, command=self.tran)
        self.bt2 = Button(root, text="Clear", width=6, command=self.clear)
        self.bt3 = Button(root, text="Listen", width=6, command=self.sound)

        '''
        img = Image.open("sound.png")
        width = img.size[0]   # 获取宽度
        height = img.size[1]
        img = img.resize((int(width*0.25), int(height*0.25)), Image.ANTIALIAS)
        photo_sound = ImageTk.PhotoImage(img)
        self.bt3 = Button(root, image=photo_sound, width=10, command=self.clear)
        '''

        # Set the bottons' locations 
        self.bt1.place(x=50, y=70)
        self.bt2.place(x=120, y=70)
        self.bt3.place(x=190, y=70)

        # Set the shortcut
        # root.bind('<Control-Return>', lambda event: self.tran())
        # root.bind('<Control-BackSpace>', lambda event: self.clear())
        root.bind('<Return>', lambda event: self.bt1.invoke())
        root.bind('<Control-BackSpace>', lambda event: self.bt2.invoke())
        root.bind('<Escape>', lambda event: self.bt3.invoke())
        root.bind('<Caps_Lock>', lambda event: self.bt3.invoke())
        # root.bind('<Control-space>', lambda event: self.toggle_visibility(root))
        keyboard.add_hotkey('Control+space', lambda: self.toggle_visibility(root=root))

    # 清理信息框
    def clear(self):
        self.e1.delete(0, END)
        self.e2.delete(0, END)

    # 展示翻译结果
    def tran(self):
        self.e2.delete(0, END)
        word = self.e1.get()
        try:
            val = a.tran(word)
        except KeyError:
            val = "Error!"
        self.e2.insert(0, val)
        self.sound()

    def toggle_visibility(self, root, event=None):
        if root.winfo_viewable():
            root.focus_force() # if the focus is not on it before withdrawing, it won't get focus
            self.e1.focus_set()
            root.withdraw()
        else:
            root.deiconify()
            root.focus_force()
            self.e1.focus_set()

    # Play the sound using FFmpeg command
    def sound(self):
        try:
            # Use the FFPLAY command to play the sound.mp3, you can also use the os command
            # NODISP can do it background, AUTOEXIT reassure that it will exit
            # SS T to handle the head loss problem
            # play_cmd = ['ffplay', '-ss', '0', '-t', '10', '-nodisp', '-autoexit', './sound_uk.mp3']
            play_cmd = ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', './sound_uk.mp3']
            # play_cmd = ['ffplay', '-nodisp', '-autoexit', '-nostdin', './sound_uk.mp3']
            play = subprocess.Popen(play_cmd)
            play.wait()
            time.sleep(0.1)
            play_cmd = ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', './sound_us.mp3']
            # play_cmd = ['ffplay', '-nodisp', '-autoexit', '-nostdin', './sound_us.mp3']
            subprocess.Popen(play_cmd)
            # os.system('.\\sound.mp3')
        except NameError:
            print('Sound Play Error!')
