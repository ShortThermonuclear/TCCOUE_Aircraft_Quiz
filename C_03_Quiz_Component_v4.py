import csv
import random
from tkinter import *
from tkinter import ttk
from functools import partial
from PIL import Image, ImageTk


def get_aircraft():
    """
    Retrieves aircraft data from csv file.
    Each row: name, country, type, purpose, image_filename
    :return: list of aircraft where each item is
             [name, country, type, purpose, image_filename]
    """

    file = open("00_aircraft.csv", "r")
    all_aircraft = list(csv.reader(file, delimiter=","))
    file.close()
    # remove the first row
    all_aircraft.pop(0)

    return all_aircraft


def get_quiz_question(quiz_type):
    """
    Chooses one correct aircraft and three wrong answer options
    for the current question, based on the quiz type.

    :param quiz_type: string - "purpose", "country", or "name"
    :return: correct_aircraft, answer_options (list of shuffled strings),
             correct_answer (string)
    """

    all_aircraft = get_aircraft()

    # choose random aircraft from list to be the correct answer
    correct_aircraft = random.choice(all_aircraft)

    # maps quiz type to the column index it relates to in each aircraft row
    column_index_map = {
        "name": 0,
        "country": 1,
        "purpose": 2,
    }
    column_index = column_index_map.get(quiz_type)
    correct_answer = correct_aircraft[column_index]

    # purpose (Easy mode) only has 2 buttons, so needs 1 wrong answer.
    # country/name (Medium/Hard) have 4 buttons, so need 3 wrong answers.
    wrong_answer_count = 1 if quiz_type == "purpose" else 3

    # loop until we have enough wrong answers that are different from
    # the correct answer and from each other
    wrong_answers = []
    while len(wrong_answers) < wrong_answer_count:
        candidate_aircraft = random.choice(all_aircraft)
        candidate_value = candidate_aircraft[column_index]
        if candidate_value != correct_answer and candidate_value not in wrong_answers:
            wrong_answers.append(candidate_value)

    # combine wrong answers and correct answer, then shuffle so the
    # correct answer isn't always in the same position
    answer_options = wrong_answers + [correct_answer]
    random.shuffle(answer_options)

    return correct_aircraft, answer_options, correct_answer


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
            make_button.grid(row=0, column=count, padx=13, pady=10)
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

        self.questions_wanted = IntVar()
        self.questions_wanted.set(5)

        self.questions_played = IntVar()
        self.questions_played.set(0)

        # Maps each quiz type to the window titles using dictionary
        title_map = {
            "purpose": "Easy Mode",
            "country": "Medium Mode",
            "name": "Hard Mode",
        }
        self.play_box = Toplevel()
        self.play_box.title(title_map.get(quiz_type))
        self.play_box.configure(bg="white")
        self.play_box.protocol("WM_DELETE_WINDOW", root.destroy)  # pressing [x] directly closes the program.

        # Quiz Frame
        self.quiz_frame = Frame(self.play_box, bg="white",
                                padx=20, pady=14,
                                bd=2, relief="groove")
        self.quiz_frame.pack(padx=10, pady=(10, 0))

        # No. of questions label
        self.num_question_label = Label(self.quiz_frame, text="Question 1 of N",
                                    font=["Helvetica", 13, "bold"], bg="white")
        self.num_question_label.pack(pady=(0, 4))

        # Frame for aircraft image
        img_frame = Frame(self.quiz_frame, bg="black", bd=1, relief="solid")
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

        # get the correct aircraft and shuffled answer options for this question
        self.correct_aircraft, self.answer_options, self.correct_answer = get_quiz_question(quiz_type)

        # Create answer buttons and add them to reference list...
        self.answer_button_ref = []
        # Checks if the quiz type is "purpose" Easy mode and changes buttons count to 2.
        btn_count = 2 if quiz_type == "purpose" else 4

        for item in range(btn_count):
            btn = Button(self.answer_frame, text=self.answer_options[item],
                         font=["Helvetica", 11], bg="#F0F0F0",
                         bd=1, relief="solid", activebackground="#D3D3D3",
                         width=18, padx=8, pady=4, command=partial(self.check_answer, item))
            btn.grid(row=item // 2, column=item % 2, padx=12, pady=4)
            self.answer_button_ref.append(btn)

        # Feedback label - This is where the user gets the answer feedback; right or wrong.
        # Right now, it's empty.
        self.feedback_label = Label(self.quiz_frame, text="", height=1,
                                    font=["Helvetica", 10, "italic"], bg="white")
        self.feedback_label.pack(pady=(6, 4))

        # Separator to divide navigator bar and quiz frame
        ttk.Separator(self.play_box, orient="horizontal").pack(
            fill="x", padx=0, pady=(6, 0))

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
                              bg="#F4ACAC", activebackground="#E88888",
                              width=7, padx=6, pady=5, relief="solid", bd=1,
                              command=self.close_play)
        self.btn_end.grid(row=0, column=0, sticky="w")

        # Centre frame - holding hints and stats button
        centre_frame = Frame(self.nav_bar, bg="white")
        centre_frame.grid(row=0, column=1)

        # Hints button
        self.btn_hints = Button(centre_frame,
                                text="Hints", font=["Helvetica", 10],
                                bg="#F5E6A3", activebackground="#E8D870",
                                width=7, padx=6, pady=5, relief="solid", bd=1,
                                state="disabled")
        self.btn_hints.pack(side="left", padx=(0, 6))

        # Stats button
        self.btn_stats = Button(centre_frame,
                                text="Stats", font=["Helvetica", 10],
                                bg="#C9B8E8", activebackground="#B0A0D8",
                                width=7, padx=6, pady=5, relief="solid", bd=1,
                                state="disabled")
        self.btn_stats.pack(side="left")

        # Next button
        self.btn_next = Button(self.nav_bar,
                               text="Next", font=["Helvetica", 10],
                               bg="#A8D5A2", activebackground="#80C07A",
                               width=7, padx=6, pady=5, relief="solid", bd=1,
                               command=self.new_question)
        self.btn_next.grid(row=0, column=2, sticky="e")

        # Starts off the quiz with a question.
        self.new_question()

    def new_question(self):
        """Gets a new question and resets the answer buttons."""

        # Get new question information
        self.current_aircraft, self.answer_options, self.correct_answer = get_quiz_question(self.quiz_type)

        # Update question counter
        question_number = self.questions_played.get() + 1
        total_questions = self.questions_wanted.get()

        self.num_question_label.config(
            text=f"Question {question_number} of {total_questions}"
        )

        # Get image file name through list
        image_filename = "aircraft_images/" + self.current_aircraft[3] + ".jpg"
        pil_image = Image.open(image_filename) # open image with pillow
        # Resize and sharpen with pillow
        pil_image = pil_image.resize((320, 200), Image.Resampling.LANCZOS)
        # Convert Pillow image into a Tkinter-compatible image
        self.photo = ImageTk.PhotoImage(pil_image)
        # Display image in a label
        self.image_label.config(image=str(self.photo), text="", width=320, height=200)

        # Put the new answers onto the buttons
        for count, button in enumerate(self.answer_button_ref):
            button.config(text=self.answer_options[count],
                          state="normal",
                          bg="#F0F0F0")

        # Reset feedback and next button
        self.feedback_label.config(text="")
        self.btn_next.config(state="disabled")

    def check_answer(self, answer_index):
        """Checks whether the selected answer is correct."""

        # Get chosen answer
        chosen_answer = self.answer_options[answer_index]

        # Add one to the number of questions played
        self.questions_played.set(self.questions_played.get() + 1)

        # Check if answer is correct
        if chosen_answer == self.correct_answer:
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.feedback_label.config(
                text=f"Incorrect. The answer was {self.correct_answer}.",
                fg="red"
            )

        # Disable all answer buttons after one answer is chosen
        for button in self.answer_button_ref:
            button.config(state="disabled")

        # Check if quiz is finished
        if self.questions_played.get() == self.questions_wanted.get():
            self.question_label.config(text="Quiz Complete!")
            self.btn_next.config(text="Done", state="disabled")
        else:
            self.btn_next.config(state="normal")

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # quiz - allows new quiz to start. Good for testing aswell.
        root.deiconify()
        self.play_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Aircraft Quiz")
    StartQuiz()
    root.mainloop()