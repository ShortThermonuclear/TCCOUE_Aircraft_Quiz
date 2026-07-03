from tkinter import *


class TimerTest:
    """
    Test window for checking whether a timer can update an empty label.
    """

    def __init__(self):
        # Main frame
        self.test_frame = Frame(root, padx=20, pady=20)
        self.test_frame.pack()

        # Empty timer label
        self.timer_label = Label(self.test_frame,
                                 text="",
                                 font=["Helvetica", 16, "bold"])
        self.timer_label.pack(pady=(5,0))

        # Feedback label
        self.feedback_label=Label(self.test_frame,
                                  text="",
                                  font=["Helvetica", 16, "bold"])
        self.feedback_label.pack(pady=3)


        # Button to start timer
        self.start_button = Button(self.test_frame,
                                   text="Start Timer",
                                   font=["Helvetica", 12],
                                   command=self.start_timer)
        self.start_button.pack()

    def start_timer(self):
        """Starts the 10s timer."""
        self.time_left = 10
        self.countdown()

    def countdown(self):
        """Updates the label every second."""

        if self.time_left > 5:
            self.timer_label.config(text=f"⏱ Time left: {self.time_left}s", fg="#CC3333")
        else:
            self.timer_label.config(text=f"⏱ Time left: {self.time_left}s", fg="#FF0000")

        if self.time_left == 0:
            self.timer_label.config(text="⏱ Time's up!", fg="#FF0000")
            return

        self.time_left -= 1
        self.test_frame.after(1000, self.countdown)


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Timer Test")
    TimerTest()
    root.mainloop()