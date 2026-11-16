import tkinter as tk


class AppFrame(tk.Frame):
    def __init__(self, master, color, width, height):
        super().__init__(master, bg=color, width=width, height=height)
        self.master = master
        self.color = color
        self.width = width
        self.height = height
        self.pack_propagate(False)

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack()
