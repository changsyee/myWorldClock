###############################################################################
##  Analog + Digital Seoul & Sydney World Clock
##  Author: Chang S Yee (이창석)
##  Created: 2026-0205
##  Updated: 2026-0218 - Optimized by pre-creating hands and text objects, and
##  using itemconfig to update text instead of deleting/recreating.
###############################################################################
import tkinter as tk                     # Python GUI Library
import math; import time; import pytz    # utilities like timezone
from datetime import datetime

WIDTH = 700; HEIGHT = 610; RADIUS = 300  # Clock Window was 400x400, r 150
CNTR_X = WIDTH // 2; CNTR_Y = HEIGHT // 2

class AnalogClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seoul & Sydney World Clock")
        self.root.geometry("900x920")    # App Window size. was 1368x912
        self.root.configure(bg="black")
        
        # Optimization: Define Timezones once to save CPU cycles
        self.tz_seoul = pytz.timezone('Asia/Seoul')
        self.tz_sydney = pytz.timezone('Australia/Sydney')
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack(pady=(50, 0))         # was 20
        
        self.draw_clock_face()

        # define a Text widget for Day of the Week with styled text
        self.txtWdgDoW = tk.Text(root, height=3, borderwidth=0, highlightthickness=0, bg="black")
        self.txtWdgDoW.pack(pady=(0, 0), padx=10)
        self.txtWdgDoW.tag_configure("Hangul", justify="center", font=("Gungsuh", 28, "bold"))
        self.txtWdgDoW.tag_configure("EngHlv", justify="center", font=("Helvetica", 28, "bold"))

        # define Text & Label widget for Seoul & Sydney w styled text. #76D4EB/#58CD3E, CornflowerBlue/LimeGreen
        self.txtWdgSeoul = tk.Text(root, height=3, borderwidth=0, highlightthickness=0, bg="black", fg="#76D4EB")
        self.txtWdgSeoul.pack(pady=(20, 0), padx=10)
        self.txtWdgSeoul.tag_configure("Hangul", justify="center", font=("Gungsuh", 32, "bold"))
        self.txtWdgSeoul.tag_configure("EngHlv", justify="center", font=("Helvetica", 32, "bold"))
        
        self.LabelSydney = tk.Label(root, text="", font=("Helvetica", 30, "bold"), bg="black", fg="#58CD3E")
        self.LabelSydney.pack(pady=0)

        # Optimization: Pre-create the hands and text objects once
        # We store their IDs so we can move them later without deleting/recreating
        self.hour_hand = self.canvas.create_line(0, 0, 0, 0, width=7, fill="white", capstyle=tk.ROUND)
        self.min_hand = self.canvas.create_line(0, 0, 0, 0, width=4, fill="white", capstyle=tk.ROUND)
        self.sec_hand = self.canvas.create_line(0, 0, 0, 0, width=2, fill="yellow", capstyle=tk.ROUND)
        self.center_pin = self.canvas.create_oval(0, 0, 0, 0, fill="Magenta") # was Tan
        
        # Pre-create Year and Month-Day text objects
        self.year_text_id = self.canvas.create_text(100, 590, text="", font=("Helvetica", 32, "bold"), fill="wheat")
        self.date_text_id = self.canvas.create_text(600, 590, text="", font=("Helvetica", 32, "bold"), fill="wheat")
        #self.txtWdgSeoul.config(state=tk.DISABLED) # Make it read-only
        
        self.update_clock()

    def draw_clock_face(self):
        self.canvas.create_oval(CNTR_X - RADIUS, CNTR_Y - RADIUS, CNTR_X + RADIUS, CNTR_Y + RADIUS, width=4, outline="coral")
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x = CNTR_X + (RADIUS - 20) * math.cos(angle)
            y = CNTR_Y + (RADIUS - 20) * math.sin(angle)
            self.canvas.create_text(x, y, text=str(i), font=("Helvetica", 32, "bold"), fill="white")

    def update_hand(self, obj_id, angle, length):
        """Calculates new coordinates and moves an existing object."""
        angle_rad = math.radians(angle - 90)
        x = CNTR_X + length * math.cos(angle_rad)
        y = CNTR_Y + length * math.sin(angle_rad)
        self.canvas.coords(obj_id, CNTR_X, CNTR_Y, x, y)
    
    def update_clock(self):
        DicKorDoW = {1:"(월)", 2:"(화)", 3:"(수)", 4:"(목)", 5:"(금)", 6:"(토)", 7:"(일)"}
        DicColDoW = {1:"LightGreen", 2:"Orange", 3:"Blue", 4:"LightBlue", 5:"SlateBlue", 6:"Tomato", 7:"Tomato"}
        # LightGreen, Orange, Blue, NavyBlue, SlateBlue, Tomato, Tomato
        now = datetime.now()
        
        # 1. Update Hands (No deletion, just moving coordinates)
        sec_angle = now.second * 6
        min_angle = now.minute * 6 + now.second * 0.1
        hour_angle = (now.hour % 12) * 30 + now.minute * 0.5
        
        self.update_hand(self.hour_hand, hour_angle, RADIUS * 0.5)
        self.update_hand(self.min_hand, min_angle, RADIUS * 0.75)
        self.update_hand(self.sec_hand, sec_angle, RADIUS * 0.85)
        self.canvas.coords(self.center_pin, CNTR_X-5, CNTR_Y-5, CNTR_X+5, CNTR_Y+5)
        
        # 2. Update Canvas Text (itemconfig is much faster than create_text)
        self.canvas.itemconfig(self.year_text_id, text=f"{now.year:04d}")
        self.canvas.itemconfig(self.date_text_id, text=f"{now.month:02d}-{now.day:02d}")
        
        # 3. Update UI Text Widgets
        DoWnum = now.isoweekday()
        self.txtWdgDoW.delete("1.0", tk.END)
        self.txtWdgDoW.insert(tk.END, now.strftime('%a '), "EngHlv")
        self.txtWdgDoW.insert(tk.END, DicKorDoW.get(DoWnum), "Hangul")
        self.txtWdgDoW.config(fg=DicColDoW.get(DoWnum))

        # 4. World Clock Logic
        time_seoul = datetime.now(self.tz_seoul)
        time_sydney = datetime.now(self.tz_sydney)
        fmt = "%m-%d %H:%M"
        
        self.txtWdgSeoul.delete("1.0", tk.END)
        self.txtWdgSeoul.insert(tk.END, "🇰🇷 서울", "Hangul")
        self.txtWdgSeoul.insert(tk.END, f": {time_seoul.strftime(fmt)}", "EngHlv")
        
        self.LabelSydney.config(text=f"🇦🇺 Sydney: {time_sydney.strftime(fmt)}")
        
        # Loop again in 1 second
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalogClockApp(root)
    root.mainloop()