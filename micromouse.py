#import requirements
import time
import math
import tkinter
import operator
from PIL import Image,ImageTk
from functools import partial
from tkinter import Frame,Button,Tk,Label,Scale,HORIZONTAL,messagebox,PhotoImage,DISABLED,Menu


class MicroMouse(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        

        #fonts and colors
        global origin_color
        global destination_color
        global start_button_color
        global button_color
        global time_slider
        global obstacle_color
        button_color_file = open("resources/button_color.txt","r")
        button_color_data = str(button_color_file.read())
        button_color_file.close()
        button_color=button_color_data
        button_frame_bg = "black"
        start_button_color = "green"
        origin_color = '#b6efb8'
        destination_color = 'yellow'
        obstacle_color = "grey"
        

        #initializing variables
        text_file=open("resources/file.txt","r")
        data=int(text_file.read())
        text_file.close()
        self.dimension = data
        self.pack()
        self.origin = None
        self.destination = None
        self.cells = []
        self.open = []
        self.closed = []
        self.obstacles = []
        self.parameters = 1


        #Menu Region
        self.my_menu = Menu(self)
        self.master.config(menu=self.my_menu)

        self.config_window = Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label='Configure', menu=self.config_window)
        self.config_window.add_command(label='Grid Layout', command=self.get_grid)
        self.config_window.add_command(label='Cell color', command=self.get_color)
        self.config_window.add_separator()
        self.config_window.add_command(label="Exit", command=root.quit)

        self.guide_window = Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label='Guide', menu=self.guide_window)
        self.guide_window.add_command(label='Guide', command=self.open_guide)

        self.about_window = Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label='About', menu=self.about_window)
        self.about_window.add_command(label='About', command=self.get_about)

