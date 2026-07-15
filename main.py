from customtkinter import *
from tkinter import Text
from functools import partial
import math
import webbrowser
import random
# =========================================
# FUNCTIONS
# =========================================
def show_video():
    webbrowser.open_new("https://www.youtube.com/watch?v=QAb3ATOpBpE")

def get_random_text():
    with open("texts.txt", encoding="utf-8") as file:
        texts = file.read().split("===")
        return random.choice(texts).strip()

def show_typing_frame(mins):
    menu_frame.grid_remove()
    typing_frame.grid()

    seconds = mins * 60
    count_down(seconds)

    current_text = get_random_text()

    text_box = Text(typing_frame, font=("Consolas", 28), bg="#2b2b2b", fg="white", wrap="word",  borderwidth=0, highlightthickness=0, padx=30, pady=30,
                    spacing2=50)
    text_box.grid(column=0, row=1, sticky="nsew", padx=50, pady=(30,0))

    text_box.configure(state="normal")
    text_box.delete("1.0", "end")
    text_box.insert("1.0", current_text)
    text_box.configure(state="disabled")

    print(current_text)

def count_down(seconds):
    count_min = math.floor(seconds/60)
    count_sec = seconds % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    timer_label.configure(text=f"0{count_min}:{count_sec}")

    if seconds > 0:
        app.after(1000, count_down, seconds-1)
    else:
        typing_frame.grid_remove()
        menu_frame.grid()

def handle_key(event):
    print(event.char)

# GLOBALS AND CONSTANTS
# =========================================

# =========================================
# WINDOW INITIALIZATION
# =========================================
app = CTk()
app.title("Speed Typing Test")

set_appearance_mode("dark")
set_default_color_theme("green")

app.minsize(1100, 700)

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

window_width = int(screen_width * 0.75)
window_height = int(screen_height * 0.75)

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x}+{y}")

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

app.bind("<Key>", handle_key)
# =========================================
# MAIN FRAME
# =========================================
main_frame = CTkFrame(app)
main_frame.grid(column=0, row=0, sticky="nsew")
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# =========================================
# MENU FRAME
# =========================================
menu_frame = CTkFrame(main_frame, fg_color="transparent")
menu_frame.grid(column=0, row=0, sticky="n")
menu_frame.grid_rowconfigure(index=0, weight=1)
menu_frame.grid_columnconfigure(index=0, weight=1)

app_name_label = CTkLabel(menu_frame, text="Speed Typing Test", font=("Consolas", 40))
app_name_label.grid(row=0, column=0, pady=(50,60))

# BUTTONS FRAME
# =========================================
buttons_frame = CTkFrame(menu_frame, fg_color="transparent")
buttons_frame.grid(column=0, row=1)
buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

for i, minutes in enumerate([1,3,5]):
    button = CTkButton(buttons_frame, text=f"{minutes} Minutes", font=("Consolas", 22), height=50, cursor="hand2", command=partial(show_typing_frame, minutes))
    button.grid(column=i, row=0, padx=30)

tutorial_label = CTkLabel(menu_frame, text="How to type faster", font=("Consolas", 32))
tutorial_label.grid(column=0, row=2, pady=(100,50))
tutorial_button = CTkButton(menu_frame, text="Tutorial", font=("Consolas", 22), height=50, cursor="hand2", command=show_video)
tutorial_button.grid(column=0, row=3)

# TYPING FRAME
# =========================================
typing_frame = CTkFrame(main_frame, fg_color="transparent")
typing_frame.grid(column=0, row=0, sticky="n")
typing_frame.grid_rowconfigure(1, weight=1)
typing_frame.grid_columnconfigure(0, weight=1)
typing_frame.grid_remove()

timer_label = CTkLabel(typing_frame, text="", font=("Consolas", 40))
timer_label.grid(column=0, row=0, pady=(20,0))
app.mainloop()