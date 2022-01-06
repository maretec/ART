'''
Checks MOHID log to verify that the run was successful
'''


def verify_run(filename, messages):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        for i in range(-1, -200, -1):
            for message in messages:
                if message in lines[i]:
                    return True
    return False

'''
Allows to create dynamic names for the files in static folders for OBC gathering.
Example: if given the datetime object that represents "2019-07-23" for initial_date and "2019-08-12" for final_date
it changes "Hydrodynamic_%Yi-%Mi-%di_%Yf-%Mf-%df" to "Hydrodynamic_2019-07-23_%2019-08-12"
'''


def create_file_name_with_date(filename, initial_date, final_date):
    if '%Yi' in filename:
        filename = filename.replace("%Yi", str(initial_date.year))
    if '%mi' in filename:
        filename = filename.replace("%mi", str(initial_date.month))
    if '%di' in filename:
        filename = filename.replace("%di", str(initial_date.day))
    if '%Yf' in filename:
        filename = filename.replace("%Yf", str(final_date.year))
    if '%mf' in filename:
        filename = filename.replace("%mf", str(final_date.month))
    if '%df' in filename:
        filename = filename.replace("%df", str(final_date.day))
    return filename
