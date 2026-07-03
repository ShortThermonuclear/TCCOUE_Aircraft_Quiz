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

        # List of buttons to be made ( text | bg | quiz type )
        diff_button_list = [
            ["Easy", "#D5E8D4", "purpose"],
            ["Medium", "#FFE6CC", "country"],
            ["Hard", "#F8CECC", "name"],
        ]

        # Create buttons and add them to the reference list...
        diff_button_ref = []
        for count, item in enumerate(diff_button_list):
            make_button = Button(self.difficulty_frame, text=item[0],
                                 font=["Helvetica", "18", "bold"],
                                 fg="#330000", bg=item[1], width=9, height=2,
                                 command=partial(self.to_quiz, item[2]))
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
                                  fg="#330000", bg="#D3D3D3", width=15, height=1,
                                  command=self.to_help)
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
                self.questions_wanted = questions_wanted
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


    def to_quiz(self, quiz_type):
        """Launches Play with the chosen difficulty / quiz_type."""
        PlayQuiz(self.questions_wanted, quiz_type)
        root.withdraw()


class DisplayHelp:
    def __init__(self, partner):
        background = "#FFE6CC"

        self.help_box = Toplevel()
        self.help_box.title("Help / Info")
        self.help_box.iconphoto(False, PhotoImage(file="D_02_Help Icon.png"))

        # If users press cross at top, closes help and enables the help button
        self.help_box.protocol("WM_DELETE_WINDOW",
                               partial(self.close_help, partner))


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
        partner.help_button.config(state="normal")
        self.help_box.destroy()


class PlayQuiz:
    """
    Main quiz window
    Adjusts layout based on quiz_type:
      "purpose" → Easy
      "country" → Medium
      "name" → Hard
    """

    def __init__(self, how_many, quiz_type):
        # Get which difficulty was chosen
        self.quiz_type = quiz_type

        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)

        self.questions_played = IntVar()
        self.questions_played.set(0)

        self.questions_correct = IntVar()
        self.questions_correct.set(0)

        self.all_results_list = []

        # Initialize timer variables (Hard mode only)
        self.timer_id = None
        self.time_left = 20

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

        # Timer label (Hard mode only — hidden otherwise)
        self.timer_label = Label(self.quiz_frame, text="", font=["Helvetica", 11, "bold"],
                                    bg="white", fg="#CC3333")

        if quiz_type == "name":
            self.timer_label.pack(pady=(0, 6))

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
                                    text=question_map.get(quiz_type),
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
            answer_button = Button(self.answer_frame, text=self.answer_options[item],
                         font=["Helvetica", 11], bg="#F0F0F0",
                         bd=1, relief="solid", activebackground="#D3D3D3",
                         width=18, padx=8, pady=4,
                         command=partial(self.check_answer, item))
            answer_button.grid(row=item // 2, column=item % 2, padx=12, pady=4)
            self.answer_button_ref.append(answer_button)

        # Feedback label - This is where the user gets the answer feedback; right or wrong.
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
                                command=self.to_hints)
        self.btn_hints.pack(side="left", padx=(0, 6))

        # Stats button
        self.btn_stats = Button(centre_frame,
                                text="Stats", font=["Helvetica", 10],
                                bg="#C9B8E8", activebackground="#B0A0D8",
                                width=7, padx=6, pady=5, relief="solid", bd=1,
                                command=self.to_stats,
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

    # Timer logic - Hard mode

    def start_timer(self):
        """Starts the 20-second countdown for Hard mode."""
        self.cancel_timer()
        self.time_left = 20
        self.tick()

    def cancel_timer(self):
        """Cancels any running timer."""
        if self.timer_id is not None:
            self.play_box.after_cancel(self.timer_id)
            self.timer_id = None

    def tick(self, event=None):
        """Counts down one second at a time."""

        # Show timer and change colour when time is nearly finished.
        if self.time_left > 5:
            self.timer_label.config(text=f"Time left: {self.time_left}s",
                                    fg="#CC3333")
        else:
            self.timer_label.config(text=f"Time left: {self.time_left}s",
                                    fg="#FF0000")

        # If timer reaches zero, count the question as wrong.
        if self.time_left == 0:
            self.timer_label.config(text="Time's up!", fg="#FF0000")

            self.feedback_label.config(
                text=f"Time's up! The answer was {self.correct_answer}.",
                fg="red"
            )

            # Add wrong result to stats list.
            self.all_results_list.append(False)

            # Enable stats button after one question has been answered.
            self.btn_stats.config(state="normal")

            # Add one to the number of questions played.
            self.questions_played.set(self.questions_played.get() + 1)

            # Disable all answer buttons after time runs out.
            for button in self.answer_button_ref:
                button.config(state="disabled")

            # Check if quiz is finished.
            if self.questions_played.get() == self.questions_wanted.get():
                self.num_question_label.config(text="Quiz Complete!")
                self.btn_next.config(text="Done", state="disabled")
            else:
                self.btn_next.config(state="normal")

            self.timer_id = None
            return

        self.time_left -= 1

        # Run tick again after 1 second.
        self.timer_id = self.play_box.after(1000, self.tick, None)


    def new_question(self):
        """Gets a new question and resets the answer buttons."""
        # Cancels any timer from the previous question.
        self.cancel_timer()

        # Get new question information
        self.current_aircraft, self.answer_options, self.correct_answer = get_quiz_question(self.quiz_type)

        # Update question counter
        question_number = self.questions_played.get() + 1
        total_questions = self.questions_wanted.get()

        # Update number of questions done.
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

        # If Hard mode chosen, starts timer
        if self.quiz_type == "name":
            self.start_timer()

    def check_answer(self, answer_index):
        """Checks whether the selected answer is correct."""
        # Stops timer once user answers.
        self.cancel_timer()

        # Get chosen answer
        chosen_answer = self.answer_options[answer_index]

        # Add one to the number of questions played
        self.questions_played.set(self.questions_played.get() + 1)

        # Check if answer is correct and edits the feedback label
        if chosen_answer == self.correct_answer:
            self.feedback_label.config(text="Correct!", fg="green")
            self.questions_correct.set(self.questions_correct.get() + 1)
            self.all_results_list.append(True) # stores this as correct

        else:
            self.feedback_label.config(
                text=f"Incorrect. The answer was {self.correct_answer}.",
                fg="red"
            )
            self.all_results_list.append(False) # stores this as incorrect

        # Disable all answer buttons after one answer is chosen
        for button in self.answer_button_ref:
            button.config(state="disabled")

        # Enables stats button after one question has been answered.
        self.btn_stats.config(state="normal")

        # Check if quiz is finished
        if self.questions_played.get() == self.questions_wanted.get():
            self.question_label.config(text="Quiz Complete!")
            self.btn_next.config(text="Done", state="disabled")
        else:
            self.btn_next.config(state="normal")


    def to_hints(self):
        """Opens hints window."""
        DisplayHints(self, self.current_aircraft, self.quiz_type)

    def to_stats(self):
        """Opens stats window."""
        DisplayStats(self)

    def close_play(self):
        # Stops timer if closed
        self.cancel_timer()

        # reshow root (ie: choose rounds) and end current
        # quiz - allows new quiz to start. Good for testing aswell.
        root.deiconify()
        self.play_box.destroy()


class DisplayHints:
    """
    Hints component — shows general guidance first, then reveals
    extra aircraft information.
    """

    def __init__(self, partner, aircraft, quiz_type):
        self.partner = partner
        self.aircraft = aircraft
        self.quiz_type = quiz_type
        self.revealed = False

        background = "#FFF8E7"

        self.hint_box = Toplevel()
        self.hint_box.title("Hints")

        # If users press cross at top, closes hints and enables hints button.
        self.hint_box.protocol("WM_DELETE_WINDOW",
                               partial(self.close_hints, partner))

        # Disables hints button so more windows can not be opened.
        partner.btn_hints.config(state="disabled")

        # Frame for hints component
        self.hint_frame = Frame(self.hint_box, bg=background, padx=10, pady=10)
        self.hint_frame.grid()

        # Hints heading
        self.hint_heading_label = Label(self.hint_frame,
                                        bg=background,
                                        text="Hints",
                                        font=["Helvetica", "15", "bold"])
        self.hint_heading_label.grid(row=0, pady=(0, 8))

        # String for note that explains how hints work
        note_text = (
            "Look closely at the aircraft's shape, window layout, markings, "
            "and overall purpose.\n\n"
            "Click Reveal to show extra information that may help you answer."
        )

        self.note_label = Label(self.hint_frame,
                                bg=background, text=note_text,
                                wraplength=360, justify="left",
                                font=["Helvetica", "13"])
        self.note_label.grid(row=1, padx=10)

        # Label that will show the revealed hint
        self.reveal_label = Label(self.hint_frame,
                                  bg=background, text="",
                                  wraplength=360, justify="left",
                                  font=["Helvetica", "11", "bold"])

        # Button that reveals the hint
        self.reveal_button = Button(self.hint_frame,
                                    text="Reveal?",
                                    font=["Helvetica", "11", "bold"],
                                    bg="#F5E6A3", relief="ridge", bd=3,
                                    activebackground="#E8D870",
                                    width=14, command=self.reveal_info)
        self.reveal_button.grid(row=2, pady=20)

        # Button that closes hints component
        self.dismiss_button = Button(self.hint_frame,
                                     font=["Helvetica", "11", "bold"],
                                     text="Dismiss", bg="#D9D9D9",
                                     activebackground="#D3D3D3",
                                     width=16, relief="solid", bd=1,
                                     command=partial(self.close_hints, partner))
        self.dismiss_button.grid(row=3, pady=(0, 5))

    def reveal_info(self):
        """Reveals extra information for purpose quiz type."""

        self.reveal_button.grid_remove()
        self.reveal_label.grid(row=2, pady=10)

        # Stops user from revealing the hint more than once.
        if self.revealed:
            return

        # Easy mode hint
        if self.quiz_type == "purpose":
            text = (
                f"Country: {self.aircraft[1]}\n"
                f"Name: {self.aircraft[0]}"
            )

        # Medium mode hint
        elif self.quiz_type == "country":
            text = (
                f"Purpose: {self.aircraft[2]}\n"
                f"Name: {self.aircraft[0]}"
            )

        # Hard mode hint
        else:
            text = (
                f"Purpose: {self.aircraft[2]}\n"
                f"Country: {self.aircraft[1]}"
            )

        # Shows hint text depending on quiz type
        self.reveal_label.config(text=text)
        self.revealed = True

    def close_hints(self, partner):
        """Closes hints window and enables hints button again."""

        partner.btn_hints.config(state="normal")
        self.hint_box.destroy()


class DisplayStats:
    """
    Stats component — shows score for the current game.
    """

    def __init__(self, partner):
        background = "#E8DDED"
        box_bg = "#F7F7F7"
        comment_bg = "#FFF2CC"

        self.stats_box = Toplevel()
        self.stats_box.title("Stats")
        self.stats_box.configure(bg=background)

        # If users press cross at top, closes stats and enables stats button.
        self.stats_box.protocol("WM_DELETE_WINDOW",
                                partial(self.close_stats, partner))

        # Disables stats button so more windows can not be opened.
        partner.btn_stats.config(state="disabled")

        # Frame for stats component
        self.stats_frame = Frame(self.stats_box, bg=background, padx=20, pady=18)
        self.stats_frame.grid()

        # Get values from quiz
        correct = partner.questions_correct.get()
        results_list = partner.all_results_list

        # Work out total, incorrect and percentage
        total = len(results_list)
        incorrect = total - correct
        percent = correct / total * 100 if total > 0 else 0

        # Chooses comment based on score
        if percent == 100:
            comment = "Perfect score — outstanding quiz result!"
            comment_bg = "#D5E8D4"

        elif percent >= 70:
            comment = "Great score — you did really well!"
            comment_bg = "#D5E8D4"

        elif percent >= 40:
            comment = "Decent score — keep practising!"
            comment_bg = "#FFF2CC"

        else:
            comment = "Low score — try using the hints next time!"
            comment_bg = "#F8CECC"

        # Heading label
        self.heading_label = Label(self.stats_frame,
                                   text="Quiz Results", bg=background,
                                   font=["Helvetica", "18", "bold"])
        self.heading_label.grid(row=0, pady=(0, 18))

        # Frame that holds all the number stats
        self.numbers_frame = Frame(self.stats_frame, bg=box_bg,
                                   bd=2, relief="groove",
                                   padx=40, pady=20)
        self.numbers_frame.grid(row=1, padx=20, pady=(0, 18))

        # List of number labels to be made
        stats_numbers_list = [
            f"Questions answered: {total}",
            f"Correct: {correct}",
            f"Incorrect: {incorrect}",
            f"Score: {percent:.0f}%"
        ]

        # Create number labels and add them to reference list...
        self.stats_number_label_ref = []
        for count, item in enumerate(stats_numbers_list):
            self.stats_number_label = Label(self.numbers_frame,
                                            text=item,
                                            font=["Helvetica", "14"],
                                            bg=box_bg)
            self.stats_number_label.grid(row=count, sticky="w")

            self.stats_number_label_ref.append(self.stats_number_label)

        # Comment label
        self.comment_label = Label(self.stats_frame,
                                   text=comment, bg=comment_bg,
                                   font=["Helvetica", "14"],
                                   padx=8, pady=4)
        self.comment_label.grid(row=2, pady=(0, 22))

        # Button that closes stats component
        self.dismiss_button = Button(self.stats_frame,
                                     text="Dismiss",
                                     font=["Helvetica", "12"],
                                     bg="#F7F7F7", relief="solid",
                                     bd=1, width=24,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=3)

    def close_stats(self, partner):
        """Closes stats window and enables stats button again."""

        partner.btn_stats.config(state="normal")
        self.stats_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Aircraft Quiz")
    StartQuiz()
    root.mainloop()