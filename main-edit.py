"""
Matilda Jansson
CMETE1
2021-04-12
"""

import time
import datetime
from datetime import date
from tkinter import *

animal_dict = {}
new_dict = {}
winter = ["11", "12", "01", "02", "03"]  # Months in the winter


class Visit:
    """
    Class for the visit
    """

    def __init__(self, date, time_arrival, time_departure):
        """
        creates new visit
        :param date: date for visit
        :param time_arrival: time for arrival
        :param time_departure: time for departure
        """

        self.date = date
        self.time_arrival = time_arrival
        self.time_departure = time_departure

    def __str__(self):
        """
        Visit information for printouts
        :return: A string including date and time for visit
        """

        print("\nYour visit: "
              "\nDate: " + self.date + "\nTime: " + str(self.time_arrival) + "-" + str(self.time_departure))
        return

    def opening_hours(self, user_input):
        """
        Compare month and date of visit with the opening hours for the zoo
        :param user_input: input from user on the format yy-mm-dd
        :return: user_input, day
        """
        global final_day, opening_time, closing_time

        user_input = list(map(int, user_input.split('-')))
        day = datetime.date(user_input[0], user_input[1], user_input[2])
        final_day = day.weekday()

        if final_day in [0, 1, 2, 3, 4]:
            opening_time = 14
            closing_time = 20
        else:
            opening_time = 10
            closing_time = 22

        return user_input, final_day, opening_time, closing_time

    def compare_time(self, an_dict):
        """
        Compare time of visit with the time the animals are awake.
        Uses input from user and a dictionary with the animals.
        :param an_dict: dictionary with animals and their attributes
        :return: attributes of animals in new dictionary
        """

        for key in an_dict:

            if (an_dict[key][1] > (int(self.time_arrival) and int(self.time_departure))) \
                    or (an_dict[key][2] < (int(self.time_arrival) or int(self.time_departure))):
                pass
            else:
                new_dict[key] = an_dict[key]

        return new_dict

    def compare_months(self, user_input2, an_dict):
        """
        Check if any animals hibernate.
        :param month: Month of visit
        :param winter_months: list with winter months
        :return: attributes of relevant animals
        """

        global final_dict
        user_input2 = list(map(str, user_input2.split('-')))

        if user_input2[1] in winter:
            final_dict = {}
            for key in an_dict:

                if an_dict[key][0] == " winter ":
                    pass
                else:
                    final_dict[key] = an_dict[key]
            return final_dict

        else:
            final_dict = an_dict
            return final_dict


def read_animals_from_file(file_name):
    """
    Makes a dictionary with the animals as keys and their attributes as values
    :param file_name: Name of the file with information
    :return: Dictionary with the animals and their attributes
    """

    fobj = open(file_name, "r")
    for line in fobj:
        key, value1, value2, value3, value4 = line.strip().split("/")

        animal_dict[key] = value1, int(value2), int(value3), value4
    fobj.close()

    return animal_dict


def print_relevant_animals(fin_dict):
    """
    Used to print the animals in a nice way
    :param: A dictionary with the final animals
    :return: string with information about the animals
    """

    for key in fin_dict:
        if fin_dict[key][3] == " -":
            print(key)
        else:
            print(key + "       *** feeding time at" + fin_dict[key][3] + " ***")

    return


def make_poster_file(name, fin_dict):
    """
    Creates a new file for the current date
    :param name: Name of the file
    :param fin_dict: A dictionary with the final animals
    :return:
    """
    fobj = open(name, "w")
    fobj.write(str(today) + "\n\n")
    fobj.write("Animals you can see today:\n\n")

    for key in fin_dict:
        if fin_dict[key][3] == " -":
            fobj.write(str(key) + "\n")
        else:
            fobj.write(str(key) + "       *** feeding time at" + str(fin_dict[key][3]) + " ***" + "\n")

    if today.weekday() in [2, 3, 4]:
        fobj.write("\n\nDon't miss the sea lion show at 15 today!")
    if today.weekday() in [0, 2, 4, 6]:
        fobj.write("\n\nCome watch our zookeepers talk about bumblebees as 16! ")
    else:
        pass

    fobj.close()
    return


def date_check(date):
    """
    Checks that the date is written on the right format and is after today
    :param date: input from user
    :return: the date (on the right format)
    """
    done = False
    while not done:
        try:
            input_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            if input_date < datetime.datetime.now().date():
                raise ValueError("The date you chose has passed")
        except ValueError as e:
            print(e)
            date = input("\nEnter the date on the format yyyy-mm-dd: ")
        else:
            done = True

    return date


def time_check_arrival(time_arrival, date):
    """
    Checks that the arrival time is valid
    :param time_arrival: input from user
    :param date: input from user
    :return: time_arrival that is valid
    """
    done = False
    while not done:

        if date in [0, 1, 2, 3, 4]:
            if int(time_arrival) < opening_time or int(time_arrival) > closing_time:
                time_arrival = check_valid_number(input("Type in your arrival within the opening hours: "))
            else:
                done = True
        else:
            if int(time_arrival) < opening_time or int(time_arrival) > closing_time:
                time_arrival = check_valid_number(input("Type in your arrival within the opening hours: "))
            else:
                done = True

    return time_arrival


def time_check_departure(time_departure, time_arrival, date):
    """
    Checks that the departure time is valid
    :param time_departure: input from user
    :param time_arrival: input from user (already checked)
    :param date: date (already checked)
    :return: time_departure that is valid
    """
    done = False
    while not done:

        if int(time_arrival) > int(time_departure):
            time_departure = check_valid_number(
                input("Your departure must be after your arrival, choose a new departure time: "))

        elif date in [0, 1, 2, 3, 4]:
            if int(time_departure) > closing_time:
                time_departure = check_valid_number(input("Type in your departure within the opening hours: "))
            else:
                done = True

        else:
            if int(time_departure) > closing_time:
                time_departure = check_valid_number(input("Type in your departure within the opening hours: "))
            else:
                done = True

    return time_departure


def check_valid_number(user_input):
    """
    Checks that the input is a number
    :param user_input:
    :return:
    """
    done = False
    while not done:
        try:
            int(user_input)
        except ValueError:
            user_input = input("Enter a valid time: ")
        else:
            done = True

    return user_input


def final_visit():
    """
    Asks for user inputs and prints what animals can be seen during the visit
    :return:
    """

    date = date_check(input("When do you want to visit Matilda's super cool zoo? (yyyy-mm-dd): "))

    your_visit = Visit(date, time_arrival=0, time_departure=0)
    your_visit.opening_hours(date)
    print("The zoo is open from " + str(opening_time) + "-" + str(closing_time) + "\n")

    time_arrival = time_check_arrival(check_valid_number(input("\nTime of arrival (whole hour): ")), final_day)
    time_departure = time_check_departure(check_valid_number(input("\nTime of departure (whole hour): ")), time_arrival,
                                          final_day)

    full_visit = Visit(date, time_arrival, time_departure)
    full_visit.__str__()

    read_animals_from_file("animals_on_zoo.txt")
    full_visit.compare_time(animal_dict)
    your_visit.compare_months(date, new_dict)
    print("\nYou can see the following animals during your visit: ")
    print_relevant_animals(final_dict)

    return


def schedule_for_today():
    """
    Creates a file for the current date with information about today's schedule
    :return:
    """
    global today
    today = date.today()

    your_visit = Visit(today, time_arrival=0, time_departure=0)
    your_visit.opening_hours(str(today))

    time_arrival = opening_time
    time_departure = closing_time

    read_animals_from_file("animals_on_zoo.txt")

    full_visit = Visit(today, time_arrival, time_departure)

    full_visit.compare_time(animal_dict)
    your_visit.compare_months(str(today), new_dict)
    make_poster_file(str(today) + ".txt", final_dict)


schedule_for_today()
final_visit()
