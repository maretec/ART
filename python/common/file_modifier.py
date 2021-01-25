import fileinput
import sys
import re

'''
Given a file pointer, it will write a new parameter and value in the following format:
Parameter : value
If you want a different value of empty spaces between parameter and value simply change {0:30} 
'''
def line_creator(file, parameter, value):
    file.write('{0:30}{1}'.format(parameter, ": " + value + "\n"))
    file.flush()


# Converts a datetime object to the MOHID date format.
def date_to_mohid_date(date):
    mohid_date = date.strftime("%Y %m %d") 
    mohid_date = mohid_date + " " + str(0) + " " + str(0) + " " + str(0)
    return mohid_date


'''
Given a file pointer, it will search in the file for parameter given and update its value on the line.
If not found it will create a new line using line_creator function.
'''


def modify_line(file, parameter, new_value):
    changed = False
    for line in fileinput.FileInput(file, inplace=True):
        if re.search(parameter, line):
            changed = True
            line = '{0:30}{1}'.format(parameter, ": " + new_value + "\n")
        sys.stdout.write(line)
    if not changed:
        line_creator(file, parameter, new_value)


def modify_end_dat_date(file, new_value):
    changed = False
    for line in fileinput.FileInput(file, inplace=True):
        if re.search("^END", line):
            changed = True
            line = '{0:30}{1}'.format("END", ": " + new_value + "\n")
        sys.stdout.write(line)
    if not changed:
        line_creator(file, "END", new_value)


def modify_start_dat_date(file, new_value):
    changed = False
    for line in fileinput.FileInput(file, inplace=True):
        if re.search("^START", line):
            changed = True
            line = '{0:30}{1}'.format("END", ": " + new_value + "\n")
        sys.stdout.write(line)
    if not changed:
        line_creator(file, "END", new_value)


def nomfinch_creator(work_path, parameters, values):
    file = open(work_path + "/exe/nomfinch.dat", 'w+')
    parameters = ["IN_BATIM", "ROOT", "ROOT_SRT", "SURF_DAT", "SURF_HDF", "DOMAIN", "IN_DAD3D", "OUT_DESF", "OUT_FIN",
                  "BOT_DAT", "BOT_HDF", "BOT_FIN", "AIRW_DAT", "AIRW_HDF", "AIRWFIN", "IN_MODEL", "IN_TIDES", "IN_TURB",
                  "TURBS_HDF", "DISPQUAL", "EUL_HDF", "EUL_FIN"]
    for parameter in parameters:
        line_creator(file, parameter, "1")
    file.close()
    return


