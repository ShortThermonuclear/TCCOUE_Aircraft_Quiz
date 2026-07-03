from tkinter import *

class StartQuiz:
    """
    Initial Quiz Interface - Asks the user for the amount of questions
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
        self.nums_questions_entry = Entry(self.start_frame,
                                          font=["Arial", "20", "bold"], width=10)
        self.nums_questions_entry.grid(row=3)

        # Binds enter button to entry box.
        self.nums_questions_entry.bind("<Return>", self.check_questions)

        # Frame for bottom misc buttons
        self.bottom_btn_frame = Frame(self.start_frame)
        self.bottom_btn_frame.grid(row=8)

        # Stats button
        self.stats_button = Button(self.bottom_btn_frame, text="Statistics",
                                   font=["Helvetica", "16"],
                                   fg="#330000", bg="#D3D3D3",
                                   width=15, height=1)
        self.stats_button.grid(row=0, column=0, padx=25, pady=10)
        self.stats_button.config(state="disabled") # disabled for now

        # Help Button
        self.help_button = Button(self.bottom_btn_frame, text="Help / Info",
                                  font=["Helvetica", "16"],
                                  fg="#330000", bg="#D3D3D3",
                                  width=15, height=1)
        self.help_button.grid(row=0, column=1, padx=25, pady=10)
        self.help_button.config(state="disabled")

    def check_questions(self, event):
        """
        Check users have entered have 1 or more questions
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

            # If the number is not valid, or less than 0, an error will show up
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            # configures comment label to show error and deletes the input
            self.comment_label.config(text = error, font=["Helvetica", "14"],
                                      fg="#C41E3A")
            self.nums_questions_entry.config(bg="#F4CCCC")
            self.nums_questions_entry.delete(0, END)

# Main Routine
if __name__ ==  "__main__":
    root=Tk()
    root.title("Aircraft Quiz")
    icon = PhotoImage(file='D_01_Airplane Icon.png') # changes the Icon.
    root.iconphoto(False, icon)
    StartQuiz()
    root.mainloop()