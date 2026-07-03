from tkinter import *

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

        # Difficulty label — Hidden until valid number entered
        self.difficulty_label = Label(self.start_frame,
                                      text="What difficulty would you like to choose?",
                                      font=["Helvetica", "14"], justify="center",
                                      padx=10, pady=10)


        # Difficulty Frame — Hidden until valid number entered
        self.difficulty_frame  = Frame(self.start_frame)


        # List of difficulties ( text | font | fg | bg | column )
        diff_button_list = [
            ["Easy", ("Helvetica", "18", "bold"), "#330000","#D5E8D4", 0],
            ["Medium", ("Helvetica", "18", "bold"), "#330000","#FFE6CC", 1],
            ["Hard", ("Helvetica", "18", "bold"), "#330000", "#F8CECC", 2]
        ]

        # Create buttons and add them to the reference list...
        diff_button_ref = []
        for item in diff_button_list:
            make_button = Button(self.difficulty_frame, text=item[0], font=item[1],
                                 fg=item[2], bg=item[3], width=9, height=2)
            make_button.grid(row = 0, column=item[4], padx=13, pady=10)
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
            # Hides buttons in invalid input
            self.set_diff_buttons(DISABLED)
            # configures comment label to show error and deletes the input
            self.comment_label.config(text = error, font=["Helvetica", "14", "bold"], fg="#C41E3A")
            self.nums_questions_entry.config(bg="#F4CCCC")
            self.nums_questions_entry.delete(0, END)

# Main Routine
if __name__ ==  "__main__":
    root=Tk()
    root.title("Aircraft Quiz")
    icon = PhotoImage(file='D_01_Airplane Icon.png') # changes the Icon
    root.iconphoto(False, icon)
    StartQuiz()
    root.mainloop()