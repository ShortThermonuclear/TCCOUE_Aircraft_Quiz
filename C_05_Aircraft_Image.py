import csv
import random
from tkinter import *
from PIL import Image, ImageTk


def get_aircraft():
    """
    Retrieves aircraft data from csv file.
    Each row: name, country, purpose, image_filename
    :return: list of aircraft where each item is
             [name, country, purpose, image_filename]
    """

    file = open("00_aircraft.csv", "r")
    all_aircraft = list(csv.reader(file, delimiter=","))
    file.close()

    # Remove the first row
    all_aircraft.pop(0)

    return all_aircraft


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Aircraft image loading test")

    # Get aircraft data
    all_aircraft = get_aircraft()
    current_aircraft = random.choice(all_aircraft)

    # Get image filename from aircraft list
    image_filename = "aircraft_images/" + current_aircraft[3] + ".jpg"

    print("Testing image:", image_filename)

    # Open image with Pillow
    pil_image = Image.open(image_filename)

    # Resize image with Pillow
    pil_image = pil_image.resize((320, 200), Image.Resampling.LANCZOS)

    # Convert Pillow image into a Tkinter-compatible image
    photo = ImageTk.PhotoImage(pil_image)

    # Display image in a label
    image_label = Label(root, image=photo)
    image_label.pack(padx=20, pady=20)

    # Keep a reference to the image
    image_label.image = photo

    root.mainloop()