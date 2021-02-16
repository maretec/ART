import re
import common.constants as static


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
    text = file.read_text()
    lines = text.split("\n")
    for i in range(0, len(lines)):
        if re.search("^" + parameter, lines[i]):
            changed = True
            lines[i] = '{0:30}{1}'.format(parameter, ": " + new_value + "\n")
    if changed:
        static.logger.info("Modifying " + file.__str__() + " START value to " + new_value)
    else:
        static.logger.info("Missing " + parameter + " value in " + file.__str__())
        static.logger.info("Adding " + parameter + " VALUE to " + file.__str__() + " : " + new_value)
        lines.append('{0:30}{1}'.format(parameter, ": " + new_value + "\n"))
    text = "\n".join(lines)
    file.write_text(text)


def modify_end_dat_date(file, new_value):
    changed = False
    text = file.read_text()
    lines = text.split("\n")
    for i in range(0, len(lines)):
        if re.search("^END", lines[i]):
            changed = True
            lines[i] = '{0:30}{1}'.format("END", ": " + new_value + "\n")
    if changed:
        static.logger.info("Modifying " + file.__str__() + " END value to " + new_value)
    else:
        static.logger.info("Missing END value in " + file.__str__())
        static.logger.info("Adding END VALUE to " + file.__str__() + " : " + new_value)
        lines.append('{0:30}{1}'.format("END", ": " + new_value + "\n"))
    text = "\n".join(lines)
    file.write_text(text)


def modify_start_dat_date(file, new_value):
    changed = False
    text = file.read_text()
    lines = text.split("\n")
    for i in range(0, len(lines)):
        if re.search("^START", lines[i]):
            changed = True
            lines[i] = '{0:30}{1}'.format("START", ": " + new_value + "\n")
    if changed:
        static.logger.info("Modifying " + file.__str__() + " START value to " + new_value)
    else:
        static.logger.info("Missing START value in " + file.__str__())
        static.logger.info("Adding START VALUE to " + file.__str__() + " : " + new_value)
        lines.append('{0:30}{1}'.format("START", ": " + new_value + "\n"))
    text = "\n".join(lines)
    file.write_text(text)