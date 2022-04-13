import json
import tkinter as tk


def openJsonFile():
    global data
    global names_list
    global position_list

    names_list = []
    position_list = []

    position_list_lastRecordsDel = 2
    names_list_lastRecordsDel = 4
    p = 0
    n = 0

    # open JSON file interchanges.json
    with open('interchanges.json') as i:
        # load JSON file into data list
        data = json.load(i)

    # find all locations in data list
    for item in data['locations']:
        # add location number to names_list
        names_list.append(item)
        # add location name to names_list
        names_list.append(data['locations'][item]['name'])
        # add location name to position_list
        position_list.append(data['locations'][item]['name'])

    # clean data by removing last two locations that dont exist
    while p < position_list_lastRecordsDel:
        del position_list[-1]
        p = p + 1

    while n < names_list_lastRecordsDel:
        del names_list[-1]
        n = n + 1


def findDistanceAndCost():

    global distance
    global false_exit
    false_exit = True
    false_entry = True
    distance = 0
    cost = 0.25

    # find the entry location number of input name from names_list
    entry_index = names_list.index(entry_position)
    entry_index -= 1
    entry = int(names_list[entry_index])

    # find the exit location number of input name from names_list
    exit_index = names_list.index(exit_position)
    exit_index -= 1
    exit = int(names_list[exit_index])

    # check to see if there is a gantry for this route if exit location is greater than entry location
    if exit > entry:
        try:
            # convert str into int
            exit = str(exit)
            false_exit = data['locations'][exit]['routes'][1]['exit']

            exit = int(exit)
            distance_output.config(text='0')
            cost_output.config(text='0')
            notes_output.insert(
                tk.END, 'Gantry does not exsit' + '\n' + 'for this route')

        except KeyError:
            pass

    exit = int(exit)

    # if exit location number is greater than entry location number print results
    if exit > entry and false_exit != False:

        while exit > entry:
            try:
                exit = str(exit)
                # find distance value of each exit location from the previous location and add it to distance variable
                distance += data['locations'][exit]['routes'][1]['distance']
                # subtract one from exit position for next exit position
                exit = int(exit) - 1
            # KeyError except for skipped location numbers
            except KeyError:
                exit = int(exit) - 1
                continue
        else:
            # convert distance to two decimal places
            distance_finalTwoDeciaml = "{:.2f}".format(distance)
            # output distance to GUI
            distance_output.config(text=distance_finalTwoDeciaml + 'km')
            # calculate cost
            final_cost = cost * distance
            # convert cost to two decimal places
            final_costTwoDecimal = "{:.2f}".format(final_cost)
            # output cost to GUI
            cost_output.config(text='$' + final_costTwoDecimal)

    # check to see if there is a gantry for this route if entry is greater than exit location
    if entry > exit:
        try:
            # convert str into int
            entry = str(entry)
            false_entry = data['locations'][entry]['routes'][1]['enter']
            entry = int(entry)
            distance_output.config(text='0')
            cost_output.config(text='0')
            notes_output.insert(
                tk.END, 'Gantry does not exsit' + '\n' + 'for this route')

        except KeyError:
            pass

    entry = int(entry)

    # if entry location number is greater than exit location number print results
    if entry > exit:
        while entry > exit and false_entry != False:
            try:
                entry = str(entry)
                # find distance value of each entry location from the previous location and add it to distance variable
                distance += data['locations'][entry]['routes'][1]['distance']
                entry = int(entry) - 1
            except KeyError:
                entry = int(entry) - 1
                continue
        else:
            distance_finalTwoDeciaml = "{:.2f}".format(distance)
            distance_output.config(text=distance_finalTwoDeciaml + 'km')
            final_cost = cost * distance
            final_costTwoDecimal = "{:.2f}".format(final_cost)
            cost_output.config(text='$' + final_costTwoDecimal)


def button_command():

    # clear previously saved data
    notes_output.delete('1.0', tk.END)

    global entry_position
    global exit_position

    # save input entry and exit position
    entry_position = entry1.get()
    exit_position = entry2.get()

    # call function to find distance and cost
    findDistanceAndCost()


def button_command_clear():

    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    distance_output.config(text="0")
    cost_output.config(text="0")
    notes_output.delete('1.0', tk.END)


if __name__ == "__main__":

    # create GUI
    window = tk.Tk()
    window.geometry('340x500')
    window.title("Trip Calculator")

    # create GUI
    entry_label = tk.Label(
        window, text="Enter Starting Position:")
    exit_label = tk.Label(window, text="Enter Exit Position:")
    entry1 = tk.Entry(window, width=20)
    entry2 = tk.Entry(window, width=20)
    distance_label = tk.Label(window, text="Distance")
    distance_output = tk.Label(window, text="0")
    cost_label = tk.Label(window, text="Cost")
    cost_output = tk.Label(window, text="0")
    availablePositions_label = tk.Label(
        window, text="Available Positions (Scroll):")
    availablePositions_output = tk.Text(window, width=20)
    notes_label = tk.Label(window, text="Notes:")
    notes_output = tk.Text(window, width=21)

    # open JSON file function
    openJsonFile()

    # print out available positions list
    for x in position_list:
        availablePositions_output.insert(tk.END, x + '\n')
    availablePositions_output.config(state=tk.DISABLED)

    # create Search button and call button_command
    tk.Button(window, text="Search", command=button_command).grid(
        row=2, column=0)
    # create Clear button and call button_command_clear
    tk.Button(window, text="Clear", command=button_command_clear).grid(
        row=2, column=1)

    # grid GUI components
    entry_label.grid(row=0, column=0)
    exit_label.grid(row=1, column=0)
    entry1.grid(row=0, column=1)
    entry2.grid(row=1, column=1)

    distance_label.grid(row=3, column=0)
    distance_output.grid(row=4, column=0)
    cost_label.grid(row=3, column=1)
    cost_output.grid(row=4, column=1)

    availablePositions_label.grid(row=5, column=0)
    availablePositions_output.grid(row=6, column=0)

    notes_label.grid(row=5, column=1)
    notes_output.grid(row=6, column=1)

    window.mainloop()
