import tkinter as tk


class AppButton(tk.Button):

    def __init__(
        self,
        master,
        text,
        command=None,
        bg="#dc2626",
        fg="#ffffff",
        hover_bg="#b91c1c",
        width=24,
        **kwargs,
    ):
        super().__init__(
            master,
            text=text,
            command=command,
            font=("Segoe UI", 11),
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            relief="flat",
            bd=0,
            padx=18,
            pady=11,
            cursor="hand2",
            width=width,
            **kwargs,
        )
        self._bg = bg
        self._hover = hover_bg
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event=None):
        self.configure(bg=self._hover)

    def _on_leave(self, _event=None):
        self.configure(bg=self._bg)
