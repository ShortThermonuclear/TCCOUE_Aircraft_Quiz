from tkinter import *


class DisplayStats:
    """
    Stats component — shows score for the current game.
    """

    def __init__(self, stats_bundle):
        background = "#E8DDED"
        box_bg = "#F7F7F7"
        comment_bg = "#FFF2CC"

        # Frame for stats component
        self.stats_frame = Frame(root, bg=background, padx=20, pady=18)
        self.stats_frame.grid()

        # Get values from stats bundle
        correct = stats_bundle[0]
        results_list = stats_bundle[1]

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
                                   text="This Quiz", bg=background,
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

        # Score label
        self.score_label = Label(self.numbers_frame,
                                 text=f"Score: {percent:.0f}%",
                                 font=["Helvetica", "14"],
                                 bg=box_bg)
        self.score_label.grid(row=3, sticky="w")

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
                                     command=root.destroy)
        self.dismiss_button.grid(row=3)


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Stats")
    root.configure(bg="#E8DDED")

    # Stats component test data

    # Perfect Score Test Data...
    # correct = 5
    # all_results_list = [True, True, True, True, True]

    # Lowest Score Test Data...
    # correct = 0
    # all_results_list = [False, False, False, False, False]

    # Random Score Test Data...
    correct = 3
    all_results_list = [True, False, True, True, False]

    # Bundle used to test stats component
    stats_bundle = [correct, all_results_list]

    # Opens stats component straight away
    DisplayStats(stats_bundle)

    root.mainloop()