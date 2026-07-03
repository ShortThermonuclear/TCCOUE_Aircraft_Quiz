import csv

def get_aircraft():
    """
    Retrieves aircraft data from csv file.
    Each row: name, country, purpose, image_filename
    :return: list of aircraft where each item is
             [name, country purpose, image_filename]
    """
    file = open("00_aircraft.csv", "r")
    all_aircraft = list(csv.reader(file, delimiter=","))
    file.close()
    # Remove the first row
    all_aircraft.pop(0)

    # loop so that each item in list is named one
    # after another instead of one big line
    for aircraft in all_aircraft:
        print(aircraft)

# Main Routine
get_aircraft()