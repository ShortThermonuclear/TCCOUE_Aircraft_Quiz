from tkinter import *
from functools import partial


class StartQuiz:
    """
    Initial Quiz interface - Asks the user for the amount of questions
     and the difficulty they want to choose
    """

    def __init__(self):

        self.start_frame = Frame(padx=20, pady=20)
        self.start_frame.grid()

        # Strings for labels
        heading_string  = ("This is a quiz involving Aircraft of all kinds! \n"
                           "Airplanes, Helicopters, Military Aircraft and more.")
        question_string = "How many questions do you want to answer?"
        comment_string  = "Press <Enter> to confirm your choice."

        # List of labels to be made ( text | font | row )
        start_labels_list = [
            [heading_string, ("Helvetica", "16", "bold"), 1],
            [question_string, ("Helvetica", "14"), 2],
            [comment_string, ("Helvetica", "14"), 4]
        ]

        # Create labels and add them to the reference list...
        start_label_ref = []
        for item in start_labels_list:
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               justify="center", pady=10, padx=10)
            make_label.grid(row=item[2])
            start_label_ref.append(make_label)

        # Extract comment label so can be changed to an error message
        self.comment_label = start_label_ref[2]

        # create Entry Box...
        self.nums_questions_entry = Entry(self.start_frame, font=["Arial", "20", "bold"],
                                          width=10)
        self.nums_questions_entry.grid(row=3)
        # Binds Enter button to entry box.
        self.nums_questions_entry.bind("<Return>", self.check_questions)

        # Initializing the after_entry variable,
        # so that the timer does not keep running.
        self.after_entry = None

        # Difficulty label — Hidden until valid number entered
        self.difficulty_label = Label(self.start_frame,
                                      text="What difficulty would you like to choose?",
                                      font=["Helvetica", "14"], justify="center",
                                      padx=10, pady=10)


        # Difficulty Frame — Hidden until valid number entered
        self.difficulty_frame  = Frame(self.start_frame)


        # List of buttons to be made ( text | bg )
        diff_button_list = [
            ["Easy", "#D5E8D4"],
            ["Medium", "#FFE6CC"],
            ["Hard", "#F8CECC"]
        ]

        # Create buttons and add them to the reference list...
        diff_button_ref = []
        for count, item in enumerate(diff_button_list):
            make_button = Button(self.difficulty_frame, text=item[0],
                                 font=["Helvetica", "18", "bold"],
                                 fg="#330000", bg=item[1], width=9, height=2)
            make_button.grid(row = 0, column=count, padx=13, pady=10)
            diff_button_ref.append(make_button)

        # Extract difficulty buttons...
        self.easy_button = diff_button_ref[0]
        self.medium_button = diff_button_ref[1]
        self.hard_button = diff_button_ref[2]

        # Info Label — Hidden until valid number entered
        self.diff_info_label = Label(self.start_frame,
                                     text="Click [ Help / Info ] for information about the Difficulties!",
                                     font=["Helvetica", "13", "bold"], fg="#C41E3A",
                                     justify="center", pady=8)


        # Frame for bottom misc buttons
        self.bottom_btn_frame = Frame(self.start_frame)
        self.bottom_btn_frame.grid(row=8)

        # Stats button
        self.stats_button = Button(self.bottom_btn_frame, text="Statistics",
                                   font=["Helvetica", "16"],
                                   fg="#330000", bg="#D3D3D3", width=15, height=1, state="disabled")
        self.stats_button.grid(row=0, column=0, padx=25, pady=10)

        # Help Button
        self.help_button = Button(self.bottom_btn_frame, text="Help / Info",
                                  font=["Helvetica", "16"],
                                  fg="#330000", bg="#D3D3D3", width=15, height=1, state="disabled")
        self.help_button.grid(row=0, column=1, padx=25, pady=10)

    def set_diff_buttons(self, state):
        """Shows or hides difficulty section"""
        if state == NORMAL:
            # Show label and buttons.
            self.difficulty_label.grid(row=5)
            self.difficulty_frame.grid(row=6)
            self.diff_info_label.grid(row=7)

        else:
            # Hide label and buttons.
            self.difficulty_label.grid_remove()
            self.difficulty_frame.grid_remove()
            self.diff_info_label.grid_remove()

    def check_questions(self, *args):
        """
        Check users have entered have 1 or more rounds
        """
        # Retrieve questions wanted from entry box
        questions_wanted = self.nums_questions_entry.get()
        # Reset label and entry box ( for when users enter another value)
        self.comment_label.config(font=("Helvetica", "14"))
        self.nums_questions_entry.config(bg="#FFFFFF")

        error = "Please choose a whole number more than 0."
        has_errors = "no"

        # checks that the number is more than zero and is an integer
        try:
            questions_wanted = int(questions_wanted)
            # cancels any ongoing timers
            self.cancel_after()

            if questions_wanted > 0:
                # shows and confirms to the user the amount of questions that they entered.
                self.comment_label.config(text=f"You have chosen to answer {questions_wanted} questions!",
                                          font=["Helvetica", "14", "bold"],
                                          fg = "#006400")
                # enables the difficulty buttons
                self.set_diff_buttons(NORMAL)

            # If the number is not valid, or less than 0, an error will show up
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            # cancels any ongoing timers
            self.cancel_after()
            # Hides difficulty buttons If invalid input.
            self.set_diff_buttons(DISABLED)
            # function that edits the comment label after 2.2s
            self.after_entry = self.comment_label.after(2200, self.on_after)
            # configures comment label to show error and deletes the input
            self.comment_label.config(text = error, font=["Helvetica", "14", "bold"], fg="#C41E3A")
            self.nums_questions_entry.config(bg="#F4CCCC")
            self.nums_questions_entry.delete(0, END)

    # edits the comment label back to the original comment
    def on_after(self):
        """ Configures error comment back to original"""
        self.comment_label.configure(text="Press <Enter> to confirm your choice.",
                                     font=["Helvetica", "14"],
                                     fg = "#000000")
        self.nums_questions_entry.configure(bg="#ffffff")

    def cancel_after(self):
        """Cancels any pending timers / after() events."""
        if self.after_entry is not None:
            self.comment_label.after_cancel(self.after_entry)
            self.after_entry = None

    def to_help(self):
        """
        Displays information for playing the game
        Disables the button so more windows can not be opened.
        """
        DisplayHelp(self)
        self.help_button.config(state="disabled")

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
            [intro_text, ("Helvetica", 10), None, LEFT, 20, (15, 8), 340, "w"],
            ["————————  Easy  ————————", ("Helvetica", 11, "bold"), "#2a7a2a", CENTER, 15, (8, 0), 300, "ew"],
            [easy_text, ("Helvetica", 10), None, LEFT, 30, (0, 8), 330, "w"],
            ["———————  Medium  ———————", ("Helvetica", 11, "bold"), "#b07a00", CENTER, 15, (8, 0), 300, "ew"],
            [medium_text, ("Helvetica", 10), None, LEFT, 30, (0, 8), 330, "w"],
            ["————————  Hard  ————————", ("Helvetica", 11, "bold"), "#cc0000", CENTER, 15, (8, 0), 300, "ew"],
            [hard_text, ("Helvetica", 10), None, LEFT, 30, (0, 8), 330, "w"],
            [hints_text, ("Helvetica", 10), None, LEFT, 30, (8, 0), 330, "w"],
            [end_text, ("Helvetica", 10), None, LEFT, 30, (8, 8), 330, "w"],
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


# Main Routine
if __name__ ==  "__main__":
    root=Tk()
    root.title("Aircraft Quiz")
    icon = PhotoImage(file='D_01_Airplane Icon.png') # changes the Icon
    root.iconphoto(False, icon)
    StartQuiz()
    root.mainloop()