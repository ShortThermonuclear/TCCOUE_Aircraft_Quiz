from tkinter import *
from functools import partial


class DisplayHelp:
    def __init__(self, partner):
        background = "#FFE6CC"

        self.help_box = Toplevel()
        self.help_box.title("Help / Info")
        self.help_box.iconphoto(False, PhotoImage(file="D_02_Help Icon.png"))

        self.help_frame = Frame(self.help_box, width=400,
                                height=300, bg=background)
        self.help_frame.grid()

        # Strings for labels
        intro_text = ("To start the quiz, enter how many questions you want "
                      "to answer and choose a difficulty.")

        easy_text = "Identify whether the shown aircraft is civilian or military."
        medium_text = "Identify which country the shown aircraft was made in."
        hard_text = ("Choose the correct name from 4 options. "
                     "You only have 30 seconds per question!")
        hints_text = ("During the quiz, use Hints for tips, Stats to see your "
                      "current score, and End to quit early. Press Next to "
                      "move to the next question after answering")
        end_text = ("When the quiz is finished, you can choose to play "
                    "again or return to the start screen.")

        # List of labels to be made
        # (text | font | fg | justify | padx | pady | wraplength | sticky)
        help_labels_list = [
            [intro_text, ("Helvetica", 10), None, "left", 20, (15, 8), 340, "w"],
            ["————————  Easy  ————————", ("Helvetica", 11, "bold"), "#2a7a2a", "center", 15, (8, 0), 300, "ew"],
            [easy_text, ("Helvetica", 10), None, "left", 30, (0, 8), 330, "w"],
            ["———————  Medium  ———————", ("Helvetica", 11, "bold"), "#b07a00", "center", 15, (8, 0), 300, "ew"],
            [medium_text, ("Helvetica", 10), None, "left", 30, (0, 8), 330, "w"],
            ["————————  Hard  ————————", ("Helvetica", 11, "bold"), "#cc0000", "center", 15, (8, 0), 300, "ew"],
            [hard_text, ("Helvetica", 10), None, "left", 30, (0, 8), 330, "w"],
            [hints_text, ("Helvetica", 10), None, "left", 30, (8, 0), 330, "w"],
            [end_text, ("Helvetica", 10), None, "left", 30, (8, 8), 330, "w"],
        ]

        # Create help / info labels and add them to the reference list...
        help_label_ref = []
        for count, item in enumerate(help_labels_list):
            make_label = Label(self.help_frame, text=item[0], font=item[1],
                               fg=item[2], justify=item[3],
                               bg=background, wraplength=item[6])
            make_label.grid(row=count, padx=item[4], pady=item[5], sticky=item[7])
            help_label_ref.append(make_label)

        # Button that leads to close_help - destroying the window
        self.dismiss_button = Button(self.help_frame,
                                     text="Dismiss",
                                     font=("Arial", 11, "bold"), bg="#FFD897",
                                     fg="#333333",
                                     width=16, height=1,
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=9, pady=(5, 15))

    # Closes the help GUI
    def close_help(self, partner):
        self.help_box.destroy()

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    DisplayHelp(root)
    root.mainloop()