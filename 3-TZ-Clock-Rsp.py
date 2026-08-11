###############################################################################
##  Analog + Digital Seoul & Sydney World Clock
##  2026-0205 Created with help of Gemini
##  2025-0728 Dynamic Image Repositioning to avoid clock hand overlap
###############################################################################
import tkinter as tk                     # Python GUI Library
import math; import time; import pytz    # utilities like timezone
from datetime import datetime

WIDTH = 700; HEIGHT = 610; RADIUS = 300
CNTR_X = WIDTH // 2; CNTR_Y = HEIGHT // 2

class AnalogClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seoul & Sydney World Clock")
        self.root.geometry("900x920")
        self.root.configure(bg="black")
        
        # Optimization: Define Timezones once to save CPU cycles
        self.tz_seoul = pytz.timezone('Asia/Seoul')
        self.tz_sydney = pytz.timezone('Australia/Sydney')
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack(pady=(50, 0))
        
        self.draw_clock_face()

        # Day of the Week Widget
        self.txtWdgDoW = tk.Text(root, height=3, borderwidth=0, highlightthickness=0, bg="black")
        self.txtWdgDoW.pack(pady=(0, 0), padx=10)
        self.txtWdgDoW.tag_configure("Hangul", justify="center", font=("Gungsuh", 28))
        self.txtWdgDoW.tag_configure("EngHlv", justify="center", font=("Helvetica", 28, "bold"))

        # Seoul & Sydney Widgets
        self.txtWdgSeoul = tk.Text(root, height=3, borderwidth=0, highlightthickness=0, bg="black", fg="#76D4EB")
        self.txtWdgSeoul.pack(pady=(20, 0), padx=10)
        self.txtWdgSeoul.tag_configure("Hangul", justify="center", font=("Gungsuh", 32))
        self.txtWdgSeoul.tag_configure("EngHlv", justify="center", font=("Helvetica", 32, "bold"))
        
        self.LabelSydney = tk.Label(root, text="", font=("Helvetica", 30, "bold"), bg="black", fg="#58CD3E")
        self.LabelSydney.pack(pady=0)
        
        # --- PRE-LOAD IMAGES ---
        # Subsample(6, 6) scales 512x512 down to roughly 85x85 pixels for the clock face.
        self.dow_images = {}
        try:
            self.dow_images[1] = tk.PhotoImage(file="512x512-Mon.png").subsample(6, 6)
            self.dow_images[2] = tk.PhotoImage(file="512x512-Tue.png").subsample(6, 6)
            self.dow_images[3] = tk.PhotoImage(file="512x512-Wed.png").subsample(6, 6)
            self.dow_images[4] = tk.PhotoImage(file="512x512-Thu.png").subsample(6, 6)
            self.dow_images[5] = tk.PhotoImage(file="512x512-Fri.png").subsample(6, 6)
            self.dow_images[6] = tk.PhotoImage(file="512x512-Sat.png").subsample(6, 6)
            self.dow_images[7] = tk.PhotoImage(file="512x512-Sun.png").subsample(6, 6)
        except tk.TclError:
            print("Warning: Emoticon PNG files not found. Ensure they are in the same directory.")

        # Create an image placeholder on the canvas. Initialized at the top (CNTR_Y - 140)
        self.canvas_img_id = self.canvas.create_image(CNTR_X, CNTR_Y - 140, anchor=tk.CENTER)

        # Optimization: Pre-create the hands and text objects once
        self.hour_hand = self.canvas.create_line(0, 0, 0, 0, width=7, fill="white", capstyle=tk.ROUND)
        self.min_hand = self.canvas.create_line(0, 0, 0, 0, width=4, fill="white", capstyle=tk.ROUND)
        self.sec_hand = self.canvas.create_line(0, 0, 0, 0, width=2, fill="yellow", capstyle=tk.ROUND)
        self.center_pin = self.canvas.create_oval(0, 0, 0, 0, fill="tan")
        
        # Pre-create Year and Month-Day text objects
        self.year_text_id = self.canvas.create_text(100, 590, text="", font=("Helvetica", 32, "bold"), fill="wheat")
        self.date_text_id = self.canvas.create_text(600, 590, text="", font=("Helvetica", 32, "bold"), fill="wheat")

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
        DicColDoW = {1:"SlateBlue", 2:"SlateBlue", 3:"SlateBlue", 4:"SlateBlue", 5:"SlateBlue", 6:"Tomato", 7:"Tomato"}
        
        now = datetime.now()
        
        # 1. Update Hands (No deletion, just moving coordinates)
        sec_angle = now.second * 6
        min_angle = now.minute * 6 + now.second * 0.1
        hour_angle = (now.hour % 12) * 30 + now.minute * 0.5
        
        self.update_hand(self.hour_hand, hour_angle, RADIUS * 0.5)
        self.update_hand(self.min_hand, min_angle, RADIUS * 0.75)
        self.update_hand(self.sec_hand, sec_angle, RADIUS * 0.85)
        self.canvas.coords(self.center_pin, CNTR_X-5, CNTR_Y-5, CNTR_X+5, CNTR_Y+5)
        
        # 2. Dynamic Image Positioning
        # 10 o'clock is 300 degrees, 2 o'clock is 60 degrees.
        hour_in_upper = (hour_angle >= 300 or hour_angle <= 60)
        # min_in_upper = (min_angle... # not used. only during 10 to 2 o'clock hr hand
        
        # If HOUR hands is in the upper region, shift the image down to 6 o'clock position
        if hour_in_upper: self.canvas.coords(self.canvas_img_id, CNTR_X, CNTR_Y + 140)
        else:             self.canvas.coords(self.canvas_img_id, CNTR_X, CNTR_Y - 140)

        # 3. Update Canvas Text & Image
        self.canvas.itemconfig(self.year_text_id, text=f"{now.year:04d}")
        self.canvas.itemconfig(self.date_text_id, text=f"{now.month:02d}-{now.day:02d}")
        
        DoWnum = now.isoweekday()

        if DoWnum in self.dow_images:
            self.canvas.itemconfig(self.canvas_img_id, image=self.dow_images[DoWnum])

        # 4. Update UI Text Widgets
        self.txtWdgDoW.delete("1.0", tk.END)
        self.txtWdgDoW.insert(tk.END, now.strftime('%a '), "EngHlv")
        self.txtWdgDoW.insert(tk.END, DicKorDoW.get(DoWnum), "Hangul")
        self.txtWdgDoW.config(fg=DicColDoW.get(DoWnum))

        # 5. World Clock Logic
        time_seoul = datetime.now(self.tz_seoul)
        time_sydney = datetime.now(self.tz_sydney)
        fmt = "%m-%d %H:%M"
        
        self.txtWdgSeoul.delete("1.0", tk.END)
        self.txtWdgSeoul.insert(tk.END, "서울", "Hangul")
        self.txtWdgSeoul.insert(tk.END, f": {time_seoul.strftime(fmt)}", "EngHlv")
        self.LabelSydney.config(text=f"Sydney: {time_sydney.strftime(fmt)}")

        if now.second == 0:
            self.root.geometry(f"+{now.minute*18}+28")    # move Window every minute

        # Loop again in 1 second
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalogClockApp(root)
    root.mainloop()
