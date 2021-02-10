'''
    Program: MicroMouse
    Author : akr
    
'''


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


        #Grid frame
        self.main_frame = Frame(self, bg='black', padx=5, pady=5)
        self.main_frame.grid(row=0)
        for i in range(self.dimension):
            for j in range(self.dimension):
                button = Button(self.main_frame, width=2, bd=0, bg=button_color)
                button.config(command=partial(self.button_click, button, i, j))
                button.grid(row=i, column=j, padx=1, pady=1, ipady=2, ipadx=4)
                self.cells.append(Cell(button, i, j))

        #Guide frame
        self.guide_frame = Frame(self, bg=button_frame_bg)
        self.guide_frame.grid(row=1)
        self.guide_label = Label(self.guide_frame, text="Place the Starting Point", width=80, bg=button_frame_bg, fg="white")
        self.guide_label.grid(sticky="we", ipadx=20, ipady=20)
        self.config(bg=button_frame_bg)
        

        #solve and reset button
        self.bottom_frame = Frame(self, borderwidth=10, bg=button_frame_bg)
        self.bottom_frame.grid(row=2, sticky="we")
        time_slider = Scale(self.bottom_frame, from_=0, to=10, tickinterval=1, resolution=.001, orient=HORIZONTAL, background=button_frame_bg, highlightbackground=button_frame_bg, fg="white")
        time_slider.grid(row=1, column=1, padx=(10,0), ipadx=150, ipady=1, sticky='WE')
        time_slider.set(9.960)
        solve = Button(self.bottom_frame, text="Solve", bd=2, bg=start_button_color)
        solve.config(command=self.solve)
        solve.grid(row=1, column=2, ipady=5, ipadx=10, padx=20)
        reset = Button(self.bottom_frame, text="Reset", bd=2, bg=start_button_color)
        reset.config(command=self.reset)
        reset.grid(row=1, column=3, ipady=5, ipadx=10)
        speed_title = Label(self.bottom_frame, text="Alter Speed", bg=button_frame_bg, fg="white")
        speed_title.grid(row=2, column=1)
        my_title = Label(self.bottom_frame, text="-akr", bg=button_frame_bg, fg="#151515")
        my_title.grid(row=2, column=3, padx=0, pady=0, sticky="e")
        messagebox.showinfo("Info","My application will be considering the diagonal boxes also as possible path")

        

    def get_about(self):
        about_details = tkinter.Toplevel()
        about_details.title("About")
        about_details.geometry('260x100+'+ str(root.winfo_x()+2)+ "+" + str(root.winfo_y()+32))
        about_label = tkinter.Label(about_details, text="Program: MicroMouse\nVersion: 1.0\nAuthor: Abhiraj K R")
        about_label.pack(fill="y", expand=True)
        ok_button = Button(about_details, bg=start_button_color, text="OK", command=about_details.destroy)
        ok_button.pack(padx=10, ipadx=20, pady=10)


    def make_grid(self):
        text_file = open("resources/file.txt","w")
        data=get_row.get()
        text_file.write(data)
        text_file.close()
        user_grid.destroy()
        messagebox.showinfo("Configuration Guide","Inorder to see your changes, you will have to close the application and open again")


    def change_color(self):
        color_file = open("resources/button_color.txt","w")
        color=get_color.get()
        color_file.write(color)
        color_file.close()
        color_grid.destroy()
        messagebox.showinfo("Configuration Guide","Inorder to see your changes, you will have to close the application and open again")


    def get_color(self):
        global color_grid
        global get_color
        global start_button_color
        color_grid = tkinter.Toplevel()
        color_grid.title("Configure Maze Color")
        color_grid.geometry('300x120+'+ str(root.winfo_x()+2)+ "+" + str(root.winfo_y()+32))
        conf_guide = tkinter.Label(color_grid, text="You can change the color of the main Maze ONLY\nEnter HEX code(eg: #ff0000) or text(eg: red)")
        conf_guide.grid(row=0, column=0, columnspan=2, padx=10)
        row_label = tkinter.Label(color_grid, text="Color: ")
        default_text = tkinter.StringVar()
        get_color = tkinter.Entry(color_grid, textvariable=default_text)
        default_text.set("blue")
        row_label.grid(row=1, column=0)
        get_color.grid(row=1, column=1)
        get_button = tkinter.Button(color_grid, text="Set", bg=start_button_color, command=self.change_color)
        get_button.grid(row=3, column=1, columnspan=2, ipadx=30, ipady=10, pady=10)


    def get_grid(self):
        global user_grid
        global get_row
        global start_button_color
        user_grid = tkinter.Toplevel()
        user_grid.title("Configure Maze")
        user_grid.geometry('260x120+'+ str(root.winfo_x()+2)+ "+" + str(root.winfo_y()+32))
        conf_guide = tkinter.Label(user_grid, text="This application supports only n x n grids\nEnter the number of rows below")
        conf_guide.grid(row=0, column=0, columnspan=2, padx=10)
        row_label = tkinter.Label(user_grid, text="Row: ")
        default_text = tkinter.StringVar()
        get_row = tkinter.Entry(user_grid, textvariable=default_text)
        default_text.set("20")
        row_label.grid(row=1, column=0)
        get_row.grid(row=1, column=1)
        get_button = tkinter.Button(user_grid, text="Set", bg=start_button_color, command=self.make_grid)
        get_button.grid(row=3, column=1, columnspan=2, ipadx=30, ipady=10, pady=10)


    def open_guide(self):
        global user_guide
        user_guide = tkinter.Toplevel()
        user_guide.title("Guide")
        user_guide.geometry('500x250+'+ str(root.winfo_x()+2)+ "+" + str(root.winfo_y()+32))
        step1_label=Label(user_guide,text="step1")
        step1_label.grid(row=0,column=0,padx=(20,0),pady=(50,0))
        step1_des=Label(user_guide,text="Select the Origin/Starting cell by simply clicking on any of the grid cell",bg="grey")
        step1_des.grid(row=0,column=1,padx=10,ipadx=10,pady=(50,0))
        step2_label=Label(user_guide,text="step2")
        step2_label.grid(row=1,column=0,padx=(20,0))
        step2_des=Label(user_guide,text="Select the Destination/Ending cell",bg="grey")
        step2_des.grid(row=1,column=1,padx=10,ipadx=10,pady=(10,0),sticky="we")
        step3_label=Label(user_guide,text="step3")
        step3_label.grid(row=2,column=0,padx=(20,0))
        step3_des=Label(user_guide,text="Select as many obstacles as you need",bg="grey")
        step3_des.grid(row=2,column=1,padx=10,ipadx=10,pady=(10,0),sticky="we")
        step4_label=Label(user_guide,text="step4")
        step4_label.grid(row=3,column=0,padx=(20,0))
        step4_des=Label(user_guide,text="Click on the 'Solve' button",bg="grey")
        step4_des.grid(row=3,column=1,padx=10,ipadx=10,pady=(10,0),sticky="we")
        ok_button=Button(user_guide,bg=start_button_color,text="OK",command=user_guide.destroy)
        ok_button.grid(row=4,column=0,columnspan=2,padx=10,ipadx=20,pady=10)


    def button_click(self, button, i, j):
        global origin_color
        global destination_color
        if self.origin is None:
            button.config(bg=origin_color,text="O",state=DISABLED)
            self.guide_label.config(text='Choose the destination')
            self.origin = Cell(button, i, j)
        elif self.destination is None:
            button.config(bg=destination_color, text='D',state=DISABLED)
            self.guide_label.config(text='Mark obstacles')
            self.destination = Cell(button, i, j)
        else:
            self.guide_label.config(text='Mark obstacles')
            if (i, j) in self.obstacles:
                button.config(bg=button_color)
                self.obstacles.remove((i, j))
            else:
                button.config(bg=obstacle_color)
                self.obstacles.append((i, j))


    def reset(self):
        global button_color
        self.origin = None
        self.destination = None
        self.open = []
        self.closed = []
        self.obstacles = []

        for cell in self.cells:
            cell.name.config(bg=button_color, text='')
            cell.reset_cell()

        self.guide_label.config(text="Place the origin")


    def solve(self):
        if self.origin is None or self.destination is None:
            self.guide_label.config(text='Check whether the "Origin" and "Destination" is selected')
            messagebox.showerror("Not Defined","Destination or Orgin is not defined")
        else:
            self.guide_label.config(text='Mouse is lookin for the path!!!!')

            current = self.origin
            self.open.append(current)

            #loop through the non obstacle cells
            while len(self.open) > 0:
                if current.pos == self.destination.pos:
                    self.retrace_path(current)
                    break

                self.open = sorted(self.open, key=operator.attrgetter('f'))
                current = self.open[0]

                if current.name != self.origin.name and current.name != self.destination.name:
                    current.name.config(bg='#ec73f4')
                    self.update()

                self.closed.append(current)
                self.open.remove(current)

                children = self.check_neighbours(current)

                for child in children:
                    if child not in self.open:
                        child.parent = current
                        child.g = current.g + distance(child.pos, current.pos)
                        child.h = distance(child.pos, self.destination.pos) * self.parameters
                        child.f = child.g + child.h
                        self.open.append(child)

                        if child.name != self.origin.name and child.name != self.destination.name:
                            child.name.config(bg='#f204d2')
                            self.update()
                        continue
                    elif child in self.open:
                        new_g = current.g + distance(child.pos, current.pos)
                        if new_g < child.g:
                            child.g = new_g
                            child.f = child.g + child.h
                            child.parent = current
                    else:
                        continue

            if len(self.open) == 0:
                self.guide_label.config(text='No Path found!!!')


    def check_neighbours(self, current):
        children = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                pos = (current.pos[0] + i, current.pos[1] + j)
                for cell in self.cells:
                    if pos == cell.pos:
                        child = cell
                if pos == current.pos:
                    continue
                else:
                    if 0 <= pos[0] < self.dimension and 0 <= pos[1] < self.dimension:
                        if pos in self.obstacles or child in self.closed:
                            continue
                        children.append(child)
        return children


    def retrace_path(self, current):
        global time_slider
        parent = current.parent
        while parent is not None:
            if parent.name != self.origin.name:
                user_time=time_slider.get()
                parent.name.config(bg='green')
                time.sleep(10-user_time)
                self.update()
            parent = parent.parent
        self.guide_label.config(text="Path Found!!!")


class Cell:
    def __init__(self, name, row, col):
        self.name = name
        self.pos = (row, col)
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def reset_cell(self):
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = ()


def distance(a, b):
    dist = int(math.sqrt(abs(a[0]-b[0])**2+abs(a[1]-b[1])**2)*10)
    return dist


if __name__ == '__main__':
    root = Tk()
    root.title("MicroMouse")
    root.iconbitmap("resources/icons/mouse.ico")
    app = MicroMouse(master=root)
    app.mainloop()
    root.quit()
