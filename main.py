from customtkinter import *
from tkinter import Text
from functools import partial
import math
import webbrowser
import random

# =========================================
# FUNCTIONS
# =========================================
def get_current_record():
    try:
        with open("record.txt", "r") as file:
            record = int(file.read())
    except FileNotFoundError:
        record = 0
    return record

def show_video():
    webbrowser.open_new("https://www.youtube.com/watch?v=QAb3ATOpBpE")

def get_random_text():
    with open("texts.txt", encoding="utf-8") as file:
        texts = file.read().split("===")

    return random.choice(texts).strip()

def configure_text_box():
    global current_text

    current_text = get_random_text()

    text_box.configure(state="normal")
    text_box.delete("1.0", "end")
    text_box.insert("1.0", current_text)
    text_box.tag_add(
        "current",
        "1.0",
        "1.1"
    )
    text_box.configure(state="disabled")

def update_remaining_seconds(mins):
    global remaining_seconds
    remaining_seconds = mins * 60

def update_timer_text():
    global remaining_seconds

    count_min = math.floor(remaining_seconds / 60)
    timer_label.configure(text=f"0{count_min}:00")

def configure_typing_frame(mins):
    global remaining_seconds, selected_minutes

    selected_minutes = mins

    menu_frame.grid_remove()
    typing_frame.grid()

    update_remaining_seconds(mins)
    update_timer_text()
    configure_text_box()

def check_results():
    global correct_inputs, wrong_inputs, selected_minutes

    total_inputs = correct_inputs + wrong_inputs
    if total_inputs == 0:
        return 0, 0

    accuracy = round(correct_inputs/total_inputs * 100)
    wpm = int((correct_inputs / 5) / selected_minutes)

    return wpm, accuracy

def check_against_median(wpm):
    if wpm < 39:
        return "below average", "#F44336"
    elif wpm <= 47:
        return "average", "gray70"
    else:
        return "above average", "#4CAF50"

def write_new_record(new_record):
    with open("record.txt", "w") as file:
        file.write(str(new_record))
    menu_record_label.configure(text=f"🏆 PERSONAL BEST:  {new_record} WPM 🏆")

def configure_results_frame():
    global correct_inputs, wrong_inputs, current_record

    typing_frame.grid_remove()
    results_frame.grid()

    wpm, accuracy = check_results()
    median, median_color = check_against_median(wpm)

    wpm_label.configure(text=f"You managed to type {wpm} WPM")
    accuracy_label.configure(text=f"{accuracy}% ")
    correct_label.configure(text=correct_inputs)
    errors_label.configure(text=wrong_inputs)

    median_label.configure(text=f"You are {median} typer!", text_color=median_color)

    if wpm > current_record:
        current_record = wpm
        write_new_record(current_record)

        record_label.configure(text=f"🏆 NEW PERSONAL BEST! 🏆\n{current_record} WPM",text_color="#4CAF50")
    else:
        record_label.configure(text=f"Personal Best: {current_record} WPM",text_color="gray70")

def count_down():
    global timer_running, timer_id, remaining_seconds, current_index

    count_min = math.floor(remaining_seconds/60)
    count_sec = remaining_seconds % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    timer_label.configure(text=f"0{count_min}:{count_sec}")

    if remaining_seconds > 0:
        timer_running = True
        remaining_seconds -= 1
        timer_id = app.after(1000, count_down)

    else:
        timer_running = False
        current_index = 0
        check_results()
        configure_results_frame()

def return_to_menu():
    global timer_running, remaining_seconds, timer_id, current_index, correct_inputs, wrong_inputs

    if timer_id:
        app.after_cancel(timer_id)

    timer_id = None
    timer_running = False
    remaining_seconds = 0
    current_index = 0
    correct_inputs = 0
    wrong_inputs = 0

    typing_frame.grid_remove()
    results_frame.grid_remove()
    menu_frame.grid()

def handle_key_press(event):
    if not event.char:
        return

    if not timer_running and typing_frame.winfo_ismapped():
        count_down()

    if timer_running:
        check_input(event.char)

def check_input(char):
    global current_index, correct_inputs, wrong_inputs

    start = text_box.index(f"1.0 + {current_index} chars")
    end = text_box.index(f"1.0 + {current_index + 1} chars")

    next_start = text_box.index(f"1.0 + {current_index + 1} chars")
    next_end = text_box.index(f"1.0 + {current_index + 2} chars")

    text_box.tag_remove("current", start, end)
    text_box.tag_add("current",next_start,next_end)

    current_y = text_box.dlineinfo(start)[1]   #dlineinfo vraci info i vizua radku(x,y,sirka,vyska,baseline) v pixelech, [1] reprezentuje y
    next_y = text_box.dlineinfo(next_start)[1]

    if next_y > current_y:
        text_box.yview_scroll(1, "units")  #units zakladni jednotka posunu, 1 rika kolik radku dolu

    if char == current_text[current_index]:
        text_box.tag_add("correct",start,end)
        current_index += 1
        correct_inputs += 1
    else:
        text_box.tag_add("wrong",start,end)
        current_index += 1
        wrong_inputs += 1

# =========================================
# GLOBALS AND CONSTANTS
# =========================================
timer_running = False
timer_id = None
remaining_seconds = None
selected_minutes = 0

current_text = ""
current_index = 0

correct_inputs = 0
wrong_inputs = 0

current_record = get_current_record()

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

app.bind("<Key>", handle_key_press)

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

app_name_label = CTkLabel(menu_frame, text="Speed Typing Test", font=("Consolas", 46))
app_name_label.grid(row=0, column=0, pady=(50,60))

# BUTTONS FRAME
# =========================================
buttons_frame = CTkFrame(menu_frame, fg_color="transparent")
buttons_frame.grid(column=0, row=1)
buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

# TIME BUTTONS
for i, minutes in enumerate([1,3,5]):
    button = CTkButton(buttons_frame, text=f"{minutes} Minutes", font=("Consolas", 22), height=50, cursor="hand2", command=partial(configure_typing_frame, minutes))
    button.grid(column=i, row=0, padx=30)

# TUTORIAL BUTTON
tutorial_label = CTkLabel(menu_frame, text="How to type faster", font=("Consolas", 40))
tutorial_label.grid(column=0, row=2, pady=(120,50))
tutorial_button = CTkButton(menu_frame, text="Tutorial", font=("Consolas", 22), height=50, cursor="hand2", command=show_video)
tutorial_button.grid(column=0, row=3)

#PERSONAL BEST
menu_record_label = CTkLabel(menu_frame,text=f"🏆 PERSONAL BEST:  {current_record} WPM 🏆",font=("Consolas", 24, "bold"),text_color="#4CAF50")
menu_record_label.grid(column=0,row=4,pady=(120, 0))

# =========================================
# TYPING FRAME
# =========================================
typing_frame = CTkFrame(main_frame, fg_color="transparent")
typing_frame.grid(column=0, row=0, sticky="n")
typing_frame.grid_rowconfigure(1, weight=1)
typing_frame.grid_columnconfigure(0, weight=1)
typing_frame.grid_columnconfigure(1, weight=1)
typing_frame.grid_remove()

# TIMER
timer_label = CTkLabel(typing_frame, text="", font=("Consolas", 40))
timer_label.grid(column=0, row=0, pady=(20,0))

# TEXT BOX
text_box = Text(typing_frame, font=("Consolas", 28), bg="#2b2b2b", fg="white", wrap="word",  borderwidth=0, highlightthickness=0, padx=30, pady=30,
                    spacing2=50)
text_box.grid(column=0, row=1, sticky="nsew", padx=50, pady=(30,0))

text_box.tag_configure("correct",foreground="#4CAF50")
text_box.tag_configure("wrong", foreground="#F44336")
text_box.tag_configure("current", background="#3a3a3a")

# CANCEL BUTTON
cancel_button = CTkButton(typing_frame, text="Cancel", font=("Consolas", 30), height=46, cursor="hand2", command=return_to_menu)
cancel_button.grid(column=0, row=0, padx=(0,200), pady=(30,0), sticky="e")

# =========================================
# RESULTS FRAME
# =========================================
results_frame = CTkFrame(main_frame,fg_color="transparent")
results_frame.grid(column=0,row=0,sticky="nsew"
)
results_frame.grid_columnconfigure(0, weight=1)

# TITLE
results_label = CTkLabel(results_frame,text="TEST COMPLETE",font=("Consolas", 28),text_color="gray70")
results_label.grid(column=0,row=0,pady=(60, 25))

# WPM
wpm_label = CTkLabel(results_frame,text="",font=("Consolas", 72, "bold"),text_color="#4CAF50")
wpm_label.grid(column=0,row=1, pady=(25,75))

# STATS FRAME
# =========================================
stats_frame = CTkFrame(results_frame,fg_color="transparent")
stats_frame.grid(column=0,row=2)
stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

# CORRECT INPUTS
correct_label = CTkLabel(stats_frame, text="",font=("Consolas", 32, "bold"),text_color="#4CAF50")
correct_label.grid(column=0,row=0,padx=50)

correct_text_label = CTkLabel(stats_frame,text="CORRECT",font=("Consolas", 15),text_color="gray60")
correct_text_label.grid(column=0,row=1)

# ACCURACY
accuracy_label = CTkLabel(stats_frame,text="",font=("Consolas", 32, "bold"))
accuracy_label.grid(column=1,row=0,padx=50)

accuracy_text_label = CTkLabel(stats_frame,text="ACCURACY",font=("Consolas", 15),text_color="gray60")
accuracy_text_label.grid(column=1,row=1)

# ERRORS
errors_label = CTkLabel(stats_frame,text="",font=("Consolas", 32, "bold"),text_color="#F44336")
errors_label.grid(column=2,row=0,padx=50)

errors_text_label = CTkLabel(stats_frame,text="ERRORS",font=("Consolas", 15),text_color="gray60")
errors_text_label.grid(column=2,row=1)

# AVERAGE COMPARISON
median_label = CTkLabel(results_frame,text="",font=("Consolas", 26),text_color="gray70")
median_label.grid(column=0,row=4,pady=(60, 25))

#CURRENT RECORD
record_label = CTkLabel(results_frame,text="",font=("Consolas", 30),text_color="gray70")
record_label.grid(column=0,row=5,pady=(35, 40))

# MENU BUTTON
menu_button = CTkButton(results_frame,text="Back to Menu",font=("Consolas", 20),height=50,width=200,cursor="hand2",command=return_to_menu)
menu_button.grid(column=0,row=6,pady=(30, 50))


results_frame.grid_remove()

app.mainloop()