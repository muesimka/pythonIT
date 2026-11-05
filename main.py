"""
Точка входа — Task Manager GUI
Версия 0.2.0
"""
import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src", "ui"))

from interface import Interface

if __name__ == "__main__":
    app = Interface(window_w=400, window_h=400)
    app.mainloop()
