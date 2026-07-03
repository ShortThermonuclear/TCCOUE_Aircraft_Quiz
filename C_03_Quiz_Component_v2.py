from tkinter import *
from functools import partial


class StartQuiz:
    """
    Initial Quiz interface
    Asks the user for the amount of questions and the difficulty they want to choose
    """

    def __init__(self):
        
        self.start_frame = Frame(padx=20, pady=20)
        self.start_frame.grid()

        # List of buttons to be made ( text | bg | quiz type )
        diff_button_list = [
            ["Easy", "#D5E8D4", "purpose"],
            ["Medium", "#FFE6CC", "country"],
            ["Hard", "#F8CECC", "name"],
        ]

        # Create buttons and add them to the reference list...
        diff_button_ref = []
        for count, item in enumerate(diff_button_list):
            make_button = Button(self.start_frame, text=item[0],
                                 font=["Helvetica", "16", "bold"],
                                 fg="#330000", bg=item[1],
                                 width=9, height=2,
                                 command=partial(self.to_quiz, item[2]))
            make_button.grid(row = 0, column=count, padx=13, pady=10)
            diff_button_ref.append(make_button)


    def to_quiz(self, quiz_type):
        PlayQuiz(quiz_type)
        root.withdraw()


class PlayQuiz:
    """
    Main quiz window
    Adjusts layout based on quiz_type:
      "purpose" → Easy
      "country" → Medium
      "name" → Hard
    """

    def __init__(self, quiz_type):
        # Get which difficulty was chosen
        self.quiz_type = quiz_type

        # Maps each quiz type to the window titles using dictionary
        title_map = {
            "purpose": "Easy Mode",
            "country": "Medium Mode",
            "name": "Hard Mode",
        }
        self.play_box = Toplevel()
        self.play_box.title(title_map.get(quiz_type))
        self.play_box.configure(bg="white")
        self.play_box.protocol("WM_DELETE_WINDOW", root.destroy) # pressing [x] directly closes the program.

        # Quiz Frame
        self.quiz_frame = Frame(self.play_box, bg="white",
                                padx=20, pady=14)
        self.quiz_frame.pack(padx=10, pady=(10, 0))

        # No. of questions label
        self.question_label = Label(self.quiz_frame, text="Question 1 of N",
                                    font=["Helvetica", 13, "bold"], bg="white")
        self.question_label.pack(pady=(0, 4))

        # Frame for aircraft image
        img_frame = Frame(self.quiz_frame, bg="black")
        img_frame.pack()

        # placeholder label for aircraft image.
        self.image_label = Label(img_frame, bg="#D0D0D0",
                                    width=35, height=12,
                                    text="[ Aircraft Image ]",
                                    font=["Helvetica", 10], fg="#888888")
        self.image_label.pack()

        # Maps each of the quiz type to each of the questions
        question_map = {
            "country": "Which country made this aircraft?",
            "purpose": "What is the purpose of this aircraft?",
            "name": "What is the name of this aircraft?",
        }
        # label for question.
        self.question_label = Label(self.quiz_frame,
                                    text=question_map.get(quiz_type, "Identify this aircraft:"),
                                    font=["Helvetica", 11], bg="white")
        self.question_label.pack(pady=(12, 8))

        # Frame for the answer buttons
        self.answer_frame = Frame(self.quiz_frame, bg="white")
        self.answer_frame.pack()

        # Create answer buttons and add them to reference list...
        self.answer_button_ref = []
        # Checks if the quiz type is "purpose" Easy mode and changes buttons count to 2.
        btn_count = 2 if quiz_type == "purpose" else 4

        for item in range(btn_count):
            btn = Button(self.answer_frame, text="Option",
                            font=["Helvetica", 11], bg="#F0F0F0",
                            width=18, padx=8, pady=4)
            btn.grid(row=item // 2, column=item % 2, padx=12, pady=4)
            self.answer_button_ref.append(btn)

        # Feedback label - This is where the user gets the answer feedback; right or wrong.
        # Right now, it's empty.
        self.feedback_label = Label(self.quiz_frame, text="", height=1,
                                    font=["Helvetica", 10, "italic"], bg="white")
        self.feedback_label.pack(pady=(6, 4))

        # Frame of navigation bar
        self.nav_bar = Frame(self.play_box, bg="white", pady=8)
        self.nav_bar.pack(fill="x", padx=10, pady=(0, 8))

        # Give column 1 "centre_frame" all the extra space so it acts as the centre
        self.nav_bar.columnconfigure(0, weight=0)
        self.nav_bar.columnconfigure(1, weight=1)
        self.nav_bar.columnconfigure(2, weight=0)

        # End quiz button - closes the quiz.
        self.btn_end = Button(self.nav_bar,
                              text="End", font=["Helvetica", 10],
                              bg="#F4ACAC",
                              width=7, padx=6, pady=5,
                              command=self.close_play)
        self.btn_end.grid(row=0, column=0, sticky="w")

        # Centre frame - holding hints and stats button
        centre_frame = Frame(self.nav_bar, bg="white")
        centre_frame.grid(row=0, column=1)

        # Hints button
        self.btn_hints = Button(centre_frame,
                                text="Hints", font=["Helvetica", 10],
                                bg="#F5E6A3", width=7,
                                padx=6, pady=5, state="disabled")
        self.btn_hints.pack(side="left", padx=(0, 6))

        # Stats button
        self.btn_stats = Button(centre_frame,
                                text="Stats", font=["Helvetica", 10],
                                bg="#C9B8E8", width=7,
                                padx=6, pady=5, state="disabled")
        self.btn_stats.pack(side="left")

        # Next button
        self.btn_next = Button(self.nav_bar,
                               text="Next", font=["Helvetica", 10],
                               bg="#A8D5A2", width=7,
                               padx=6, pady=5, state="disabled")
        self.btn_next.grid(row=0, column=2, sticky="e")

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # quiz - allows new quiz to start. Good for testing aswell.
        root.deiconify()
        self.play_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Aircraft Quiz")
    StartQuiz()
    root.mainloop()