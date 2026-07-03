from tkinter import *


class DisplayHints:
    """
    Hints component — shows general guidance first, then reveals
    extra aircraft information.
    """

    def __init__(self, aircraft, quiz_type):
        self.aircraft = aircraft
        self.quiz_type = quiz_type
        self.revealed = False

        background = "#FFF8E7"

        # Frame for hints component
        self.hint_frame = Frame(root, bg=background, padx=10, pady=10)
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
                                command=root.destroy)
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


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Hints Test")

    # Test aircraft data
    test_aircraft = ['Harrier Jump Jet (AV-8B)', 'UK / USA',
                     'Military', 'Harrier-Jump-Jet']

    # Opens hints component straight away
    DisplayHints(test_aircraft, "country")

    root.mainloop()