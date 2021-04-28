import yaml
import datetime
import python.mohid.util.constants as static
from pathlib import Path


def open_yaml_file(path):
    file_path = Path(path)

    with open(file_path, 'r') as yml_file:
        return yaml.safe_load(yml_file)


def validate_yaml_section(yaml_file, section_name, mandatory_list):
    mandatory_parameters = set(mandatory_list).difference(set(yaml_file[section_name]))
    if len(mandatory_parameters) != 0:
        raise ValueError("Missing mandatory parameter on " + section_name + ": " + str(mandatory_parameters) + ".")
    if None in list(yaml_file[section_name].values()):
        raise ValueError("Blank value on " + section_name + ".")


#TODO mohid validation
def validate_yaml_file(yaml_dict):
    validate_yaml_section(yaml_dict, 'ART', ['MAIN_PATH', 'START_DATE', 'END_DATE', 'RUN_PREPROCESSING', 'MODULE',\
                                                   'RUN_POSTPROCESSING'])
    if yaml_dict['ART']['MODULE'] == 'Mohid':
        validate_yaml_section(yaml_dict, 'Mohid', [])
        if 'MPI' in yaml_dict['MOHID_WATER']:
            validate_yaml_section(yaml_dict['MOHID_WATER'], 'MPI', [])
        for model in yaml_dict.keys():
            if model != 'MOHID_WATER' and model != 'PREPROCESSING' and model != 'POSTPROCESSING' and model != 'ART':
                validate_yaml_section(yaml_dict[model], model, [])


def validate_date(yaml):
    static.logger.debug("Validating Dates")
    try:
        start_date = datetime.datetime.strptime(yaml['SIMULATION']['START_DATE'], static.DATE_FORMAT)
        end_date = datetime.datetime.strptime(yaml['SIMULATION']['END_DATE'], static.DATE_FORMAT)
        total_days = yaml['SIMULATION']['DAYS_PER_RUN'] * yaml['SIMULATION']['NUMBER_OF_RUNS']

        if start_date + datetime.timedelta(days=total_days) > end_date:
            raise ValueError("artconfig: The number of daysPerRun (" + str(yaml['SIMULATION']['DAYS_PER_RUN']) +
                             ") in conjunction with the numberOfRuns (" + str(yaml['SIMULATION']['NUMBER_OF_RUNS']) +
                             ") plus the startDate of this run (" + str(start_date) +
                             ") would lead to a final date of simulation beyond the user-specified endDate + "
                             "(" + str(end_date) + ").")
        else:
            static.logger.debug("Date Validation : Success")
    except KeyError:
        static.logger.warning("Either startDate or endDate were not specified in the configuration file ")
        static.logger.warning("Will from now on assume that startDate is TODAY and a forecast of 3 days")

    return


def read_attribute(cfg, attribute):
    return cfg[attribute]