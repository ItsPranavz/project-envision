import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import pyautogui
import keyboard

class RedFocusFilter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.5)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.update_overlay()

        # Corrected key bindings for specific events
        self.root.bind("<Button-1>", self.click_through)  # Left mouse click
        self.root.bind("<Button-3>", self.click_through)  # Right mouse click

        # Hotkey to exit the program
        keyboard.add_hotkey('esc', self.exit_program)

    def update_overlay(self):
        screenshot = pyautogui.screenshot()

        # Split into channels
        r, g, b = screenshot.split()

        # Blur blue and green channels
        g = g.filter(ImageFilter.GaussianBlur(radius=5))
        b = b.filter(ImageFilter.GaussianBlur(radius=5))

        # Merge channels back
        filtered_image = Image.merge("RGB", (r, g, b))

        photo = ImageTk.PhotoImage(filtered_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

        # Update the overlay less frequently to prevent flickering
        self.root.after(10, self.update_overlay)  # 1-second interval

    def click_through(self, event):
        x, y = self.root.winfo_pointerxy()

        # Temporarily hide the overlay for a very short time
        self.root.withdraw()
        pyautogui.click(x, y)  # Perform the click at the current pointer position

        # Bring the overlay back immediately with minimal delay
        self.root.after(10, self.root.deiconify)  # Delay shortened to 50ms for smoother experience

    def exit_program(self):
        self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RedFocusFilter()
    app.run()