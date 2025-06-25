import tkinter as tk
import math
import time
import random

def spiral_window():
    root = tk.Tk()
    root.title("Don't Panic!")
    root.overrideredirect(True) # No title bar
    root.attributes('-topmost', True) # Stay on top
    label = tk.Label(root, text="🐍 Learn Python!", font=("Arial", 16), bg="black", fg="lime")
    label.pack()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    r = 100
    theta = 0
    center_x, center_y = screen_width // 2, screen_height // 2

    try:
        while True:
            x = int(center_x + r * math.cos(theta))
            y = int(center_y + r * math.sin(theta))
            root.geometry(f"+{x}+{y}")
            root.update()
            theta += 0.1
            r += 0.5
            time.sleep(0.01)
    except tk.TclError:
        pass # Window closed

if __name__ == "__main__":
    spiral_window()
	
