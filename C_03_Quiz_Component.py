from tkinter import *
from functools import partial


class StartQuiz:
    """
    Initial Quiz interface -Asks the user for the amount of questions
    and the difficulty they want to choose
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
        Play(quiz_type)
        root.withdraw()


class Play:
    """
    Interface for playing the Quiz
    Adjusts layout based on quiz difficulty
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


if __name__ == "__main__":
    root = Tk()
    root.title("Aircraft Quiz")
    StartQuiz()
    root.mainloop()