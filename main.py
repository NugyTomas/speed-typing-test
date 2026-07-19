from customtkinter import (CTk,CTkFrame,CTkLabel,CTkButton,set_appearance_mode,set_default_color_theme)
from tkinter import Text
from functools import partial
import webbrowser
import random

class TypingTestApp:
    def __init__(self):
        # STATE
        self.timer_running = False
        self.timer_id = None
        self.remaining_seconds = 0
        self.selected_minutes = 0

        self.current_text = ""
        self.current_index = 0

        self.correct_inputs = 0
        self.wrong_inputs = 0

        self.current_record = self.get_current_record()

        # GUI
        self.setup_window()
        self.create_main_frame()
        self.create_menu_frame()
        self.create_typing_frame()
        self.create_results_frame()

    # SETUP / GUI
    def setup_window(self):
        self.app = CTk()
        self.app.title("Speed Typing Test")

        set_appearance_mode("dark")
        set_default_color_theme("green")

        self.app.minsize(1100, 700)

        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.75)

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.app.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

    def create_main_frame(self):
        self.main_frame = CTkFrame(self.app)
        self.main_frame.grid(column=0, row=0, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def create_menu_frame(self):
        self.menu_frame = CTkFrame(self.main_frame, fg_color="transparent")
        self.menu_frame.grid(column=0, row=0, sticky="n")
        self.menu_frame.grid_rowconfigure(index=0, weight=1)
        self.menu_frame.grid_columnconfigure(index=0, weight=1)

        app_name_label = CTkLabel(self.menu_frame, text="Speed Typing Test", font=("Consolas", 46))
        app_name_label.grid(row=0, column=0, pady=(50, 60))

        # BUTTONS FRAME
        # =========================================
        buttons_frame = CTkFrame(self.menu_frame, fg_color="transparent")
        buttons_frame.grid(column=0, row=1)
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # TIME BUTTONS
        for i, minutes in enumerate([1, 3, 5]):
            button = CTkButton(buttons_frame, text=f"{minutes} Minutes", font=("Consolas", 22), height=50,
                               cursor="hand2", command=partial(self.configure_typing_frame, minutes))
            button.grid(column=i, row=0, padx=30)

        # TUTORIAL BUTTON
        tutorial_label = CTkLabel(self.menu_frame, text="How to type faster", font=("Consolas", 40))
        tutorial_label.grid(column=0, row=2, pady=(120, 50))
        tutorial_button = CTkButton(self.menu_frame, text="Tutorial", font=("Consolas", 22), height=50, cursor="hand2",
                                    command=self.show_video)
        tutorial_button.grid(column=0, row=3)

        # PERSONAL BEST
        self.menu_record_label = CTkLabel(self.menu_frame, text=f"🏆 PERSONAL BEST:  {self.current_record} WPM 🏆",
                                     font=("Consolas", 24, "bold"), text_color="#4CAF50")
        self.menu_record_label.grid(column=0, row=4, pady=(120, 0))

    def create_typing_frame(self):
        self.typing_frame = CTkFrame(self.main_frame, fg_color="transparent")
        self.typing_frame.grid(column=0, row=0, sticky="n")
        self.typing_frame.grid_rowconfigure(1, weight=1)
        self.typing_frame.grid_columnconfigure(0, weight=1)
        self.typing_frame.grid_columnconfigure(1, weight=1)
        self.typing_frame.grid_remove()

        # TIMER LABEL
        self.timer_label = CTkLabel(self.typing_frame, text="", font=("Consolas", 40))
        self.timer_label.grid(column=0, row=0, pady=(20, 0))

        # TEXT BOX
        self.text_box = Text(self.typing_frame, font=("Consolas", 28), bg="#2b2b2b", fg="white", wrap="word", borderwidth=0,
                        highlightthickness=0, padx=30, pady=30,
                        spacing2=50)
        self.text_box.grid(column=0, row=1, sticky="nsew", padx=50, pady=(30, 0))

        self.text_box.tag_configure("correct", foreground="#4CAF50")
        self.text_box.tag_configure("wrong", foreground="#F44336")
        self.text_box.tag_configure("current", background="#3a3a3a")

        # CANCEL BUTTON
        cancel_button = CTkButton(self.typing_frame, text="Cancel", font=("Consolas", 30), height=46, cursor="hand2",
                                  command=self.return_to_menu)
        cancel_button.grid(column=0, row=0, padx=(0, 200), pady=(30, 0), sticky="e")

    def create_results_frame(self):
        self.results_frame = CTkFrame(self.main_frame, fg_color="transparent")
        self.results_frame.grid(column=0, row=0, sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=1)

        # TITLE
        results_label = CTkLabel(self.results_frame, text="TEST COMPLETE", font=("Consolas", 28), text_color="gray70")
        results_label.grid(column=0, row=0, pady=(60, 25))

        # WPM
        self.wpm_label = CTkLabel(self.results_frame, text="", font=("Consolas", 72, "bold"), text_color="#4CAF50")
        self.wpm_label.grid(column=0, row=1, pady=(25, 75))

        # STATS FRAME
        # =========================================
        stats_frame = CTkFrame(self.results_frame, fg_color="transparent")
        stats_frame.grid(column=0, row=2)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # CORRECT INPUTS
        self.correct_label = CTkLabel(stats_frame, text="", font=("Consolas", 32, "bold"), text_color="#4CAF50")
        self.correct_label.grid(column=0, row=0, padx=50)

        correct_text_label = CTkLabel(stats_frame, text="CORRECT", font=("Consolas", 15), text_color="gray60")
        correct_text_label.grid(column=0, row=1)

        # ACCURACY
        self.accuracy_label = CTkLabel(stats_frame, text="", font=("Consolas", 32, "bold"))
        self.accuracy_label.grid(column=1, row=0, padx=50)

        accuracy_text_label = CTkLabel(stats_frame, text="ACCURACY", font=("Consolas", 15), text_color="gray60")
        accuracy_text_label.grid(column=1, row=1)

        # ERRORS
        self.errors_label = CTkLabel(stats_frame, text="", font=("Consolas", 32, "bold"), text_color="#F44336")
        self.errors_label.grid(column=2, row=0, padx=50)

        errors_text_label = CTkLabel(stats_frame, text="ERRORS", font=("Consolas", 15), text_color="gray60")
        errors_text_label.grid(column=2, row=1)

        # AVERAGE COMPARISON
        self.median_label = CTkLabel(self.results_frame, text="", font=("Consolas", 26), text_color="gray70")
        self.median_label.grid(column=0, row=4, pady=(60, 25))

        # CURRENT RECORD
        self.record_label = CTkLabel(self.results_frame, text="", font=("Consolas", 30), text_color="gray70")
        self.record_label.grid(column=0, row=5, pady=(35, 40))

        # MENU BUTTON
        menu_button = CTkButton(self.results_frame, text="Back to Menu", font=("Consolas", 20), height=50, width=200,
                                cursor="hand2", command=self.return_to_menu)
        menu_button.grid(column=0, row=6, pady=(30, 50))

        self.results_frame.grid_remove()

    def show_video(self):
        webbrowser.open_new("https://www.youtube.com/watch?v=QAb3ATOpBpE")

    # APP LOGIC
    # =========================================

    # TYPING FRAME
    def configure_typing_frame(self, mins):
        self.selected_minutes = mins
        self.remaining_seconds = mins * 60

        self.menu_frame.grid_remove()
        self.typing_frame.grid()
        self.update_timer_text()
        self.configure_text_box()

    def get_random_text(self):
        with open("texts.txt", encoding="utf-8") as file:
            texts = file.read().split("===")

        return random.choice(texts).strip()

    def configure_text_box(self):
        self.current_text = self.get_random_text()

        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", self.current_text)
        self.text_box.tag_add(
            "current",
            "1.0",
            "1.1"
        )
        self.text_box.configure(state="disabled")

    def return_to_menu(self):
        if self.timer_id:
            self.app.after_cancel(self.timer_id)

        self.timer_id = None
        self.timer_running = False
        self.remaining_seconds = 0
        self.current_index = 0
        self.correct_inputs = 0
        self.wrong_inputs = 0

        self.typing_frame.grid_remove()
        self.results_frame.grid_remove()
        self.menu_frame.grid()

    # TIMER / INPUT
    def update_timer_text(self):
        count_min = self.remaining_seconds // 60
        self.timer_label.configure(text=f"{count_min:02}:00")

    def count_down(self):
        count_min = self.remaining_seconds // 60
        count_sec = self.remaining_seconds % 60

        self.timer_label.configure(text=f"{count_min:02}:{count_sec:02}")

        if self.remaining_seconds > 0:
            self.timer_running = True
            self.remaining_seconds -= 1
            self.timer_id = self.app.after(1000, self.count_down)

        else:
            self.timer_running = False
            self.current_index = 0
            self.configure_results_frame()

    def handle_key_press(self, event):
        if not event.char:
            return

        if not self.timer_running and self.typing_frame.winfo_ismapped():
            self.count_down()

        if self.timer_running:
            self.check_input(event.char)

    def check_input(self, char):
        start = self.text_box.index(f"1.0 + {self.current_index} chars")
        end = self.text_box.index(f"1.0 + {self.current_index + 1} chars")

        next_start = self.text_box.index(f"1.0 + {self.current_index + 1} chars")
        next_end = self.text_box.index(f"1.0 + {self.current_index + 2} chars")

        self.text_box.tag_remove("current", start, end)
        self.text_box.tag_add("current", next_start, next_end)

        current_y = self.text_box.dlineinfo(start)[1]
        next_y = self.text_box.dlineinfo(next_start)[1]

        if next_y > current_y:
            self.text_box.yview_scroll(1, "units")

        if char == self.current_text[self.current_index]:
            self.text_box.tag_add("correct", start, end)
            self.correct_inputs += 1
        else:
            self.text_box.tag_add("wrong", start, end)
            self.wrong_inputs += 1

        self.current_index += 1

    # RESULTS / RECORD
    def check_results(self):
        total_inputs = self.correct_inputs + self.wrong_inputs
        if total_inputs == 0:
            return 0, 0

        accuracy = round(self.correct_inputs / total_inputs * 100)
        wpm = int((self.correct_inputs / 5) / self.selected_minutes)

        return wpm, accuracy

    def check_against_median(self, wpm):
        if wpm < 39:
            return "below average", "#F44336"
        elif wpm <= 47:
            return "average", "gray70"
        else:
            return "above average", "#4CAF50"

    def get_current_record(self):
        try:
            with open("record.txt", "r") as file:
                record = int(file.read())
        except FileNotFoundError:
            record = 0
        return record

    def write_new_record(self):
        with open("record.txt", "w") as file:
            file.write(str(self.current_record))
        self.menu_record_label.configure(text=f"🏆 PERSONAL BEST:  {self.current_record} WPM 🏆")

    def configure_results_frame(self):
        self.typing_frame.grid_remove()
        self.results_frame.grid()

        wpm, accuracy = self.check_results()
        median, median_color = self.check_against_median(wpm)

        self.wpm_label.configure(text=f"You managed to type {wpm} WPM")
        self.accuracy_label.configure(text=f"{accuracy}% ")
        self.correct_label.configure(text=self.correct_inputs)
        self.errors_label.configure(text=self.wrong_inputs)

        self.median_label.configure(text=f"You are {median} typer!", text_color=median_color)

        if wpm > self.current_record:
            self.current_record = wpm
            self.write_new_record()
            self.record_label.configure(text=f"🏆 NEW PERSONAL BEST! 🏆\n{self.current_record} WPM", text_color="#4CAF50")

        else:
            self.record_label.configure(text=f"Personal Best: {self.current_record} WPM", text_color="gray70")

    # RUN
    def run(self):
        self.app.bind("<Key>", self.handle_key_press)
        self.app.mainloop()


typing_test = TypingTestApp()
typing_test.run()
