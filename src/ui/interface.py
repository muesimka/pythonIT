import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Frame import AppFrame
from Button import AppButton
from storage import load_tasks, save_tasks
from config import NAME_FILE_SAVES
from utils import insure_saves_file


class Interface(tk.Tk):
    def __init__(self, window_w=400, window_h=400):
        super().__init__()

        self.root_w = window_w
        self.root_h = window_h
        self.geometry(f"{self.root_w}x{self.root_h}")
        self.title("Task Manager")
        self.configure(bg="black")

        self.frames = {}
        self.buttons = {}
        self.tasks = []

        insure_saves_file(NAME_FILE_SAVES)
        self.tasks = load_tasks(NAME_FILE_SAVES)

        self.create_interface()

    def create_interface(self):
        self.create_frames(["menu", "tasks", "add"])
        self.create_menu()
        self.create_tasks_view()
        self.create_add_view()
        self.show_frame("menu")

    def create_frames(self, names):
        for name in names:
            frame = AppFrame(self, color="black", width=self.root_w, height=self.root_h)
            frame.place(x=0, y=0, relwidth=1, relheight=1)
            self.frames[name] = frame

    def create_menu(self):
        frame = self.frames["menu"]
        tk.Label(
            frame, text="Главное меню", bg="black", fg="white", font=("Arial", 22)
        ).pack(pady=30)

        self.buttons["show_tasks"] = AppButton(
            frame, text="Посмотреть все задачи", command=self.open_tasks
        )
        self.buttons["show_tasks"].pack(pady=10)

        self.buttons["add_task"] = AppButton(
            frame, text="Добавить задачу", command=lambda: self.show_frame("add")
        )
        self.buttons["add_task"].pack(pady=10)

        self.buttons["exit"] = AppButton(frame, text="Выход", command=self.on_exit)
        self.buttons["exit"].pack(pady=10)

    def create_tasks_view(self):
        frame = self.frames["tasks"]
        tk.Label(
            frame, text="Все задачи", bg="black", fg="white", font=("Arial", 20)
        ).pack(pady=20)

        list_frame = tk.Frame(frame, bg="black")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(
            list_frame,
            bg="#1a1a1a",
            fg="white",
            font=("Arial", 12),
            selectbackground="#444",
            yscrollcommand=scrollbar.set,
            height=12,
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)

        btn_frame = tk.Frame(frame, bg="black")
        btn_frame.pack(pady=15)

        AppButton(btn_frame, text="Удалить выбранную", command=self.delete_selected).pack(
            side=tk.LEFT, padx=5
        )
        AppButton(
            btn_frame, text="Вернуться в меню", command=lambda: self.show_frame("menu")
        ).pack(side=tk.LEFT, padx=5)

    def create_add_view(self):
        frame = self.frames["add"]
        tk.Label(
            frame, text="Добавить задачу", bg="black", fg="white", font=("Arial", 20)
        ).pack(pady=25)

        tk.Label(frame, text="Имя задачи:", bg="black", fg="white", font=("Arial", 12)).pack()
        self.entry_name = tk.Entry(frame, font=("Arial", 12), width=35)
        self.entry_name.pack(pady=5)

        tk.Label(frame, text="Содержимое:", bg="black", fg="white", font=("Arial", 12)).pack()
        self.entry_content = tk.Entry(frame, font=("Arial", 12), width=35)
        self.entry_content.pack(pady=5)

        btn_frame = tk.Frame(frame, bg="black")
        btn_frame.pack(pady=20)

        AppButton(btn_frame, text="Сохранить", command=self.save_new_task).pack(
            side=tk.LEFT, padx=5
        )
        AppButton(btn_frame, text="Назад", command=lambda: self.show_frame("menu")).pack(
            side=tk.LEFT, padx=5
        )

    def show_frame(self, name):
        self.frames[name].tkraise()

    def open_tasks(self):
        self.refresh_task_list()
        self.show_frame("tasks")

    def refresh_task_list(self):
        self.tasks = load_tasks(NAME_FILE_SAVES)
        self.task_listbox.delete(0, tk.END)
        if not self.tasks:
            self.task_listbox.insert(tk.END, "Список задач пуст")
            return
        for i, content in enumerate(self.tasks):
            parts = content.strip().split("|", 1)
            name = parts[0].strip()
            body = parts[1].strip() if len(parts) > 1 else ""
            self.task_listbox.insert(tk.END, f"{i + 1}. {name} — {body}")

    def save_new_task(self):
        name = self.entry_name.get().strip()
        content = self.entry_content.get().strip()
        if not name:
            messagebox.showwarning("Ошибка", "Имя задачи не может быть пустым!")
            return
        if not content:
            messagebox.showwarning("Ошибка", "Содержимое задачи не может быть пустым!")
            return
        self.tasks.append(f"{name} | {content}\n")
        save_tasks(self.tasks, NAME_FILE_SAVES)
        self.entry_name.delete(0, tk.END)
        self.entry_content.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача «{name}» добавлена!")
        self.show_frame("menu")

    def delete_selected(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите задачу для удаления")
            return
        idx = selection[0]
        if not self.tasks or idx >= len(self.tasks):
            return
        removed = self.tasks.pop(idx)
        save_tasks(self.tasks, NAME_FILE_SAVES)
        self.refresh_task_list()
        name = removed.split("|")[0].strip()
        messagebox.showinfo("Удалено", f"Задача «{name}» удалена")

    def on_exit(self):
        save_tasks(self.tasks, NAME_FILE_SAVES)
        self.destroy()


if __name__ == "__main__":
    app = Interface(window_w=400, window_h=400)
    app.mainloop()
