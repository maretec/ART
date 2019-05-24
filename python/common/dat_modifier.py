def line_creator(file, parameter, value):
    file.write('{0:30}{1}'.format(parameter, ": " + value + "\n"))


def date_to_mohid_date(date):
    mohid_date = str(date.year) + " " + str(date.month) + " " + str(date.day) + " " + str(0) + " " + \
                                                              str(0) + " " + str(0)
    return mohid_date
