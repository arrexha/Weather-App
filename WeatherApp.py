import os
import sys
import io
import random
import time
from datetime import datetime
from urllib.request import urlopen
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # The main working imports

import requests

from dotenv import load_dotenv

load_dotenv()  # This loads the .env file before we use os.getenv()


PRIMARY_TEXT = "#3b4252"    # Soft gray for primary text
BUTTON_COLOR = "#6272a4"    # Soft gray-blue for buttons
BTN_TEXT = "white"      # Button text color
BG_COLOR = "#bfdbf7"    # Light blue background for the main app
FORECAST_BG = "#bfdbf7"    # Lighter background for forecast cards
FORECAST_TEXT = "#43496a" # Darker text for better contrast
HIGHLIGHT_COLOR = "#6082B6" 
CLOCK_COLOR = "#bfdbf7"  # Added blue-gray color


FONT_NAME = "Verdana"

# Modern Transparent Widgets
transparent = "#bfdbf7"      # Slightly transparent blue shade

#API Key
API_KEY = os.getenv("c069869f5f39308fb279f710ecb33c96")  # Should be set in your .env file

# Weather Icons
ICON_URL = "https://openweathermap.org/img/wn/{icon_code}@2x.png"



def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except (AttributeError, OSError) as e:
        print(f"Warning: Falling back to default path ({str(e)})")
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_app_icon():
    """Super reliable icon loader with detailed debugging"""
    print("\n=== Trying to load app icon ===")

    attempts = [
        ("ICO", os.path.join("assets", "weather.ico")),
        ("ICO", os.path.join(os.path.dirname(__file__), "weather.ico")),
        ("PNG", os.path.join("assets", "weather.png")),
        ("PNG", os.path.join(os.path.dirname(__file__), "weather.png")),
    ]

    for file_type, path in attempts:
        full_path = resource_path(path) if "assets" in path else path
        try:
            if os.path.exists(full_path):
                print(f"Trying {file_type} at: {full_path}")
                if file_type == "ICO":
                    app.iconbitmap(full_path)
                    print("✓ Successfully loaded ICO icon!")
                    return True
                else:  # PNG
                    img = tk.PhotoImage(file=full_path)
                    app.iconphoto(True, img)
                    print("✓ Successfully loaded PNG icon!")
                    return True
            else:
                print(f"File not found: {full_path}")
        except Exception as e:
            print(f"Failed to load {file_type}: {str(e)}")

    print("⚠ Could not load any icon - app will run without one")
    return False

def update_clock() -> None:
    """Updates the clock label every second"""
    current_time = time.strftime("%I:%M:%S %p")
    clock_label.config(text=f"🕒 {current_time}")
    clock_label.after(1000, update_clock)

def fetch_weather():
    city = city_entry.get()

    try:
        # Use units=metric to get Celsius
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={"c069869f5f39308fb279f710ecb33c96"}&units=metric"
        response = requests.get(url)
        data = response.json()
        weather_main = data['weather'][0]['main'].lower()

        for anim in animations.values():
            anim.stop()
        canvas.delete("weather")

        if weather_main in animations:
            animations[weather_main].start()

        temp = data['main']['temp']
        weather_desc = data['weather'][0]['description'].title()
        last_updated = datetime.now().strftime("%b %d at %I:%M %p")

        result_label.config(
            text=f"{round(temp)}°C • {weather_desc}\n🕒 Updated: {last_updated}",
            font=(FONT_NAME, 14),
            foreground=PRIMARY_TEXT,
            background=CLOCK_COLOR,
            justify="center"
        )

        icon_code = data['weather'][0]['icon']
        icon_url = ICON_URL.format(icon_code=icon_code)

        with urlopen(icon_url) as response:
            pil_image = Image.open(io.BytesIO(response.read()))

        resized_image = pil_image.resize((100, 100), Image.Resampling.LANCZOS)
        weather_photo = ImageTk.PhotoImage(image=resized_image)
        icon_label.config(image=weather_photo)
        icon_label.__weather_photo = weather_photo # type: ignore

        show_forecast(city)

    except Exception as e:
        result_label.config(
            text=f"Error: {str(e)}",
            foreground="#FF0000"
        )

def show_forecast(city):
    try:
        # Use units=metric to get Celsius
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={"c069869f5f39308fb279f710ecb33c96"}&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json()

        for child_widget in forecast_frame.winfo_children():
            child_widget.destroy()

        forecast_dates = []
        for forecast in data['list']:
            date = forecast['dt_txt'].split()[0]
            if date not in forecast_dates:
                forecast_dates.append(date)
                if len(forecast_dates) == 5:
                    break

        for i, date in enumerate(forecast_dates):
            for forecast in data['list']:
                forecast_date, forecast_time = forecast['dt_txt'].split()
                if forecast_date == date:
                    if "12:00:00" in forecast_time or (i == 0 and forecast_time >= "06:00:00"):
                        temp = forecast['main']['temp']
                        desc = forecast['weather'][0]['description']
                        icon_code = forecast['weather'][0]['icon']

                        date_obj = datetime.strptime(date, "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%a %b %d")

                        card = tk.Frame(forecast_frame, bg=FORECAST_BG, padx=5, pady=5)
                        card.grid(row=0, column=i, padx=5)

                        tk.Label(card, text=formatted_date, bg=FORECAST_BG, fg=FORECAST_TEXT,
                                 font=(FONT_NAME, 10, "bold")).pack()

                        icon_url = ICON_URL.format(icon_code=icon_code)
                        with urlopen(icon_url) as response:
                            icon_data = response.read()
                        pil_img = Image.open(io.BytesIO(icon_data))
                        pil_img = pil_img.resize((50, 50), Image.Resampling.LANCZOS)
                        forecast_icon_img = ImageTk.PhotoImage(pil_img)

                        forecast_icon_label = tk.Label(card, bg=FORECAST_BG)
                        forecast_icon_label.config(image=forecast_icon_img)
                        forecast_icon_label.image = forecast_icon_img # type: ignore
                        forecast_icon_label.pack()

                        tk.Label(card, text=f"{round(temp)}°C", bg=FORECAST_BG, fg=FORECAST_TEXT,
                                 font=(FONT_NAME, 12, "bold")).pack()

                        tk.Label(card, text=desc.title(), bg=FORECAST_BG, fg=FORECAST_TEXT,
                                 font=(FONT_NAME, 9)).pack()
                        break

    except Exception as e:
        print(f"Forecast error: {e}")
        result_label.config(text=f"Forecast error: {str(e)}", foreground="#FF0000")


app = tk.Tk()
app.title("Weather App")
load_app_icon()
app.geometry("600x500")

def create_gradient(width: int,
                   height: int,
                   color1: str = "#6082B6",
                   color2: str = "#6272a4"):
    pil_img = Image.new("RGB", (width, height))
    for y in range(height):
        r = int(color1[1:3], 16) + (int(color2[1:3], 16) - int(color1[1:3], 16)) * y // height
        g = int(color1[3:5], 16) + (int(color2[3:5], 16) - int(color1[3:5], 16)) * y // height
        b = int(color1[5:7], 16) + (int(color2[5:7], 16) - int(color1[5:7], 16)) * y // height

        for x in range(width):
            pil_img.putpixel((x, y), (r, g, b))
    return ImageTk.PhotoImage(pil_img)

gradient = create_gradient(600, 500, "#d6d9f5", "#ADD8E6")

bg_label = tk.Label(app, image=gradient)
bg_label._gradient = gradient # type: ignore
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

canvas = tk.Canvas(app, bg='#ADD8E6', highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
canvas.lower("all")

class WeatherAnimation:
    def __init__(self, animation_canvas, effect_type):
        self.canvas = animation_canvas
        
        self.particles = []
        self.active = False

    def start(self):
        self.active = True
        self._animate()

    def stop(self):
        self.active = False

    def _animate(self):
        if not self.active:
            return

        if random.random() > 0.7:
            x = random.randint(0, self.canvas.winfo_width())
            self.particles.append({
                'id': self.canvas.create_text(
                    x, -10,
                    
                    font=("Arial", 16),
                    tags="weather"
                ),
                'x': x,
                'y': -10,
                
            })

        for p in self.particles[:]:
            self.canvas.move(p['id'], 0, p['speed'])
            p['y'] += p['speed']

            if p['y'] > self.canvas.winfo_height():
                self.canvas.delete(p['id'])
                self.particles.remove(p)

        self.canvas.after(30, self._animate)

main_frame = ttk.Frame(app, style="Card.TFrame")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

input_frame = ttk.Frame(main_frame)
input_frame.grid(row=0, column=0, columnspan=2, pady=10)

ttk.Label(input_frame, text="Enter City:").pack(side="left", padx=(0, 5))

city_entry = ttk.Entry(
    input_frame,
    font=(FONT_NAME, 12),
    width=20,
    style="TEntry"
)
city_entry.pack(side="left")

result_label = ttk.Label(main_frame, font=(FONT_NAME, 14, "bold"), justify="center")
result_label.grid(row=2, column=0, columnspan=2, pady=10)

icon_label = ttk.Label(main_frame)
icon_label.grid(row=1, column=0, columnspan=2, pady=10)

weather_btn = ttk.Button(
    main_frame,
    text="⛅ Get Weather",
    command=fetch_weather,
    style="Highlight.TButton"  # Use new style
)
weather_btn.grid(row=3, column=0, columnspan=2, pady=15, padx=15)

def on_enter(_event):
    weather_btn.config(style="Hover.TButton", font=(FONT_NAME, 12, "bold")) # type: ignore

def on_leave(_event):
    weather_btn.config(style="TButton", font=(FONT_NAME, 12, "normal")) # type: ignore

weather_btn.bind("<Enter>", on_enter)
weather_btn.bind("<Leave>", on_leave)

tk.Label(
    main_frame,
    text="5-Day Forecast",
    bg=BG_COLOR,
    fg=PRIMARY_TEXT,
    font=(FONT_NAME, 14, "bold")
).grid(row=4, column=0, columnspan=2, pady=(20, 5))

forecast_frame = tk.Frame(
    main_frame,
    bg=BG_COLOR,
    padx=5,
    pady=5
)
forecast_frame.grid(row=5, column=0, columnspan=2)

style = ttk.Style()
style.configure("TFrame", background=transparent)
style.configure("TLabel", background=transparent, foreground=PRIMARY_TEXT, font=(FONT_NAME, 12))
style.configure("TButton", background=BUTTON_COLOR, foreground="white", font=(FONT_NAME, 12, "bold"), borderwidth=3, relief="raised", padding=10)
style.configure("Card.TFrame", background=transparent, borderwidth=2, relief="groove", padding=10)
style.configure(
    "Highlight.TButton",
    background=HIGHLIGHT_COLOR,  
    foreground="white",
    font=(FONT_NAME, 14, "bold"),
    borderwidth=4,
    relief="raised",
    padding=12
)
style.map(
    "Highlight.TButton",
    background=[("active", "#42569c"), ("!active", HIGHLIGHT_COLOR)],
    foreground=[("active", "white")],
    relief=[("active", "sunken")]
)
style.configure(
    "TEntry",
    foreground="#333333",
    fieldbackground="white",
    bordercolor=HIGHLIGHT_COLOR,  
    padding=5,
    relief="solid",
    borderwidth=2
)

style.map("Hover.TButton", background=[("active", "#7a88c3")],  foreground=[("active", "white")],  relief=[("active", "sunken")])
style.map("Hover.TButton", background=[("active", "#7a88c3")], foreground=[("active", "white")], relief=[("active", "sunken")])

for widget in main_frame.winfo_children():
    if isinstance(widget, ttk.Widget):
        widget.configure(style='TLabel') # type: ignore
    else:
        widget.configure(relief='flat', borderwidth=0) # type: ignore
    widget.grid_configure(padx=10, pady=5)

clock_label = tk.Label(
    app,
    font=(FONT_NAME, 12),
    bg=CLOCK_COLOR,
    fg=PRIMARY_TEXT,
    bd=0
)
clock_label.pack(side="bottom", pady=10)

animations = {
    "snow": WeatherAnimation(canvas, "snow"),
    "rain": WeatherAnimation(canvas, "rain"),
    "clouds": WeatherAnimation(canvas, "clouds")
}

update_clock()
app.mainloop()