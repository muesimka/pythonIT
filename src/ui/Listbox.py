import tkinter as tk


class AppListbox(tk.Listbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

    def clear(self):
        self.delete(0, tk.END)

    def add_item(self, text):
        self.insert(tk.END, text)
