import csv
import random

def get_aircraft(quiz_type):
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


    # Prints statements for testing
    print("Correct aircraft:", correct_aircraft)
    print("Answer options:", answer_options)
    print("Correct answer:", correct_answer)


get_aircraft("purpose")