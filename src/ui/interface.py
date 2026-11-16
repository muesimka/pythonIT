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

# --- чёрно-красная палитра ---
BG = "#0a0a0a"
CARD = "#141414"
CARD_BORDER = "#2a2a2a"
RED = "#dc2626"
RED_HOVER = "#b91c1c"
RED_SOFT = "#7f1d1d"
RED_GLOW = "#ef4444"
MUTED = "#a3a3a3"
TEXT = "#fafafa"
INPUT_BG = "#1a1a1a"
SECONDARY = "#262626"
SECONDARY_HOVER = "#404040"


class Interface(tk.Tk):
    def __init__(self, window_w=440, window_h=600):
        super().__init__()

        self.root_w = window_w
        self.root_h = window_h
        self.geometry(f"{self.root_w}x{self.root_h}")
        self.minsize(400, 520)
        self.title("Task Manager")
        self.configure(bg=BG)
        self.resizable(True, True)

        self.frames = {}
        self.tasks = []

        insure_saves_file(NAME_FILE_SAVES)
        self.tasks = load_tasks(NAME_FILE_SAVES)

        self.create_interface()
        self._center_window()
        self.bind_shortcuts()

    def _center_window(self):
        self.update_idletasks()
        w, h = self.root_w, self.root_h
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def bind_shortcuts(self):
        self.bind("<Escape>", lambda e: self.show_frame("menu"))
        self.bind("<Control-n>", lambda e: self.show_frame("add"))
        self.bind("<Control-l>", lambda e: self.open_tasks())

    def create_interface(self):
        self.create_frames(["menu", "tasks", "add"])
        self.create_menu()
        self.create_tasks_view()
        self.create_add_view()
        self.show_frame("menu")

    def create_frames(self, names):
        for name in names:
            frame = AppFrame(self, color=BG, width=self.root_w, height=self.root_h)
            frame.place(x=0, y=0, relwidth=1, relheight=1)
            self.frames[name] = frame

    def _make_card(self, parent, padx=24, pady=24):
        outer = tk.Frame(parent, bg=CARD_BORDER, padx=1, pady=1)
        inner = tk.Frame(outer, bg=CARD, padx=padx, pady=pady)
        inner.pack(fill=tk.BOTH, expand=True)
        return outer, inner

    # ---------- MENU ----------
    def create_menu(self):
        frame = self.frames["menu"]

        # красная полоска сверху
        tk.Frame(frame, bg=RED, height=4).pack(fill=tk.X)

        top = tk.Frame(frame, bg=BG)
        top.pack(pady=(36, 8))

        tk.Label(top, text="●", bg=BG, fg=RED, font=("Segoe UI", 22)).pack()
        tk.Label(
            top, text="Task Manager", bg=BG, fg=TEXT, font=("Segoe UI", 26, "bold")
        ).pack(pady=(2, 0))


        # счётчик задач на главном экране
        self.menu_count = tk.Label(
            frame, text="", bg=BG, fg=RED_GLOW, font=("Segoe UI", 10)
        )
        self.menu_count.pack(pady=(12, 4))
        self._update_menu_count()

        card_outer, card = self._make_card(frame, padx=28, pady=26)
        card_outer.pack(pady=16, padx=40, fill=tk.X)

        AppButton(
            card,
            text="Посмотреть все задачи",
            command=self.open_tasks,
            bg=RED,
            hover_bg=RED_HOVER,
        ).pack(pady=7)

        AppButton(
            card,
            text="Добавить задачу",
            command=lambda: self.show_frame("add"),
            bg=RED_SOFT,
            hover_bg=RED,
        ).pack(pady=7)

        AppButton(
            card,
            text="Выход",
            command=self.on_exit,
            bg=SECONDARY,
            hover_bg=SECONDARY_HOVER,
        ).pack(pady=7)

        # подсказки
        hints = tk.Frame(frame, bg=BG)
        hints.pack(side=tk.BOTTOM, pady=14)
        tk.Label(
            hints,
            text="Ctrl+L — список   ·   Ctrl+N — новая   ·   Esc — меню",
            bg=BG,
            fg="#525252",
            font=("Segoe UI", 8),
        ).pack()

    def _update_menu_count(self):
        n = len(self.tasks)
        if n == 0:
            self.menu_count.config(text="Нет задач")
        elif n == 1:
            self.menu_count.config(text="1 задача")
        elif 2 <= n <= 4:
            self.menu_count.config(text=f"{n} задачи")
        else:
            self.menu_count.config(text=f"{n} задач")

    # ---------- TASKS ----------
    def create_tasks_view(self):
        frame = self.frames["tasks"]
        tk.Frame(frame, bg=RED, height=4).pack(fill=tk.X)

        head = tk.Frame(frame, bg=BG)
        head.pack(fill=tk.X, pady=(20, 8), padx=28)

        tk.Label(
            head, text="Все задачи", bg=BG, fg=TEXT, font=("Segoe UI", 20, "bold")
        ).pack(side=tk.LEFT)

        self.tasks_count_label = tk.Label(
            head, text="", bg=BG, fg=MUTED, font=("Segoe UI", 10)
        )
        self.tasks_count_label.pack(side=tk.RIGHT, pady=6)

        card_outer, card = self._make_card(frame, padx=10, pady=10)
        card_outer.pack(fill=tk.BOTH, expand=True, padx=28, pady=(4, 10))

        scroll = tk.Scrollbar(card)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(
            card,
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 11),
            selectbackground=RED,
            selectforeground=TEXT,
            activestyle="none",
            relief="flat",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scroll.set,
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.task_listbox.yview)

        # двойной клик — подсказка / фокус
        self.task_listbox.bind("<Double-Button-1>", lambda e: self.delete_selected())

        btn_row = tk.Frame(frame, bg=BG)
        btn_row.pack(pady=(2, 18))

        AppButton(
            btn_row,
            text="Удалить",
            command=self.delete_selected,
            bg=RED,
            hover_bg=RED_HOVER,
            width=12,
        ).pack(side=tk.LEFT, padx=6)

        AppButton(
            btn_row,
            text="Обновить",
            command=self.refresh_task_list,
            bg=SECONDARY,
            hover_bg=SECONDARY_HOVER,
            width=12,
        ).pack(side=tk.LEFT, padx=6)

        AppButton(
            btn_row,
            text="← Меню",
            command=lambda: self.show_frame("menu"),
            bg=SECONDARY,
            hover_bg=SECONDARY_HOVER,
            width=12,
        ).pack(side=tk.LEFT, padx=6)

        tk.Label(
            frame,
            text="Выделите задачу и нажмите «Удалить»  ·  двойной клик тоже удаляет",
            bg=BG,
            fg="#525252",
            font=("Segoe UI", 8),
        ).pack(pady=(0, 10))

    # ---------- ADD ----------
    def create_add_view(self):
        frame = self.frames["add"]
        tk.Frame(frame, bg=RED, height=4).pack(fill=tk.X)

        tk.Label(
            frame, text="Новая задача", bg=BG, fg=TEXT, font=("Segoe UI", 20, "bold")
        ).pack(pady=(28, 4))
        tk.Label(
            frame,
            text="Заполните оба поля и нажмите Сохранить",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(pady=(0, 16))

        card_outer, card = self._make_card(frame, padx=26, pady=22)
        card_outer.pack(padx=36, fill=tk.X)

        tk.Label(
            card, text="Название", bg=CARD, fg=MUTED, font=("Segoe UI", 9), anchor="w"
        ).pack(fill=tk.X)
        self.entry_name = tk.Entry(
            card,
            font=("Segoe UI", 12),
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=RED,
            relief="flat",
            bd=10,
            highlightthickness=1,
            highlightbackground=CARD_BORDER,
            highlightcolor=RED,
        )
        self.entry_name.pack(fill=tk.X, pady=(4, 16))

        tk.Label(
            card, text="Описание", bg=CARD, fg=MUTED, font=("Segoe UI", 9), anchor="w"
        ).pack(fill=tk.X)
        self.entry_content = tk.Entry(
            card,
            font=("Segoe UI", 12),
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=RED,
            relief="flat",
            bd=10,
            highlightthickness=1,
            highlightbackground=CARD_BORDER,
            highlightcolor=RED,
        )
        self.entry_content.pack(fill=tk.X, pady=(4, 6))

        # Enter = сохранить
        self.entry_name.bind("<Return>", lambda e: self.entry_content.focus())
        self.entry_content.bind("<Return>", lambda e: self.save_new_task())

        btn_row = tk.Frame(frame, bg=BG)
        btn_row.pack(pady=28)

        AppButton(
            btn_row,
            text="Сохранить",
            command=self.save_new_task,
            bg=RED,
            hover_bg=RED_HOVER,
            width=12,
        ).pack(side=tk.LEFT, padx=6)

        AppButton(
            btn_row,
            text="Очистить",
            command=self._clear_form,
            bg=SECONDARY,
            hover_bg=SECONDARY_HOVER,
            width=12,
        ).pack(side=tk.LEFT, padx=6)

        AppButton(
            btn_row,
            text="← Назад",
            command=lambda: self.show_frame("menu"),
            bg=SECONDARY,
            hover_bg=SECONDARY_HOVER,
            width=12,
        ).pack(side=tk.LEFT, padx=6)

    def _clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_content.delete(0, tk.END)
        self.entry_name.focus()

    # ---------- LOGIC ----------
    def show_frame(self, name):
        if name == "menu":
            self.tasks = load_tasks(NAME_FILE_SAVES)
            self._update_menu_count()
        if name == "add":
            self.after(100, lambda: self.entry_name.focus())
        self.frames[name].tkraise()

    def open_tasks(self):
        self.refresh_task_list()
        self.show_frame("tasks")

    def refresh_task_list(self):
        self.tasks = load_tasks(NAME_FILE_SAVES)
        self.task_listbox.delete(0, tk.END)

        n = len(self.tasks)
        self.tasks_count_label.config(
            text=f"{n}" if n else "0"
        )
        self._update_menu_count()

        if not self.tasks:
            self.task_listbox.insert(tk.END, "")
            self.task_listbox.insert(tk.END, "  Пока нет задач")
            self.task_listbox.insert(tk.END, "  Добавьте первую через меню")
            return

        for i, content in enumerate(self.tasks):
            parts = content.strip().split("|", 1)
            name = parts[0].strip()
            body = parts[1].strip() if len(parts) > 1 else ""
            self.task_listbox.insert(tk.END, f"  {i + 1}.  {name}")
            if body:
                self.task_listbox.insert(tk.END, f"      {body}")
            self.task_listbox.insert(tk.END, "")

    def save_new_task(self):
        name = self.entry_name.get().strip()
        content = self.entry_content.get().strip()
        if not name:
            messagebox.showwarning("Ошибка", "Введите название задачи")
            self.entry_name.focus()
            return
        if not content:
            messagebox.showwarning("Ошибка", "Введите описание задачи")
            self.entry_content.focus()
            return

        self.tasks.append(f"{name} | {content}\n")
        save_tasks(self.tasks, NAME_FILE_SAVES)
        self._clear_form()
        messagebox.showinfo("Готово", f"«{name}» добавлена")
        self.show_frame("menu")

    def delete_selected(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Сначала выберите задачу в списке")
            return

        line = self.task_listbox.get(selection[0]).strip()
        if not line or "Пока нет" in line or "Добавьте" in line:
            return

        idx = None
        try:
            if line[0].isdigit():
                idx = int(line.split(".")[0].strip()) - 1
        except (ValueError, IndexError):
            pass

        if idx is None:
            pos = selection[0]
            while pos >= 0:
                prev = self.task_listbox.get(pos).strip()
                if prev and prev[0].isdigit():
                    try:
                        idx = int(prev.split(".")[0].strip()) - 1
                        break
                    except ValueError:
                        pass
                pos -= 1

        if idx is None or idx < 0 or idx >= len(self.tasks):
            messagebox.showwarning("Ошибка", "Выберите строку с названием задачи")
            return

        name = self.tasks[idx].split("|")[0].strip()
        if not messagebox.askyesno("Удаление", f"Удалить «{name}»?"):
            return

        self.tasks.pop(idx)
        save_tasks(self.tasks, NAME_FILE_SAVES)
        self.refresh_task_list()
        messagebox.showinfo("Удалено", f"«{name}» удалена")

    def on_exit(self):
        save_tasks(self.tasks, NAME_FILE_SAVES)
        self.destroy()


if __name__ == "__main__":
    app = Interface()
    app.mainloop()
