import yaml
import datetime
import common.constants as static


def open_yaml_file(path):
    with open(path, 'r') as yml_file:
        return yaml.safe_load(yml_file)


def validate_yaml_section(yaml_file, section_name, mandatory_list):
    mandatory_parameters = set(mandatory_list).difference(set(yaml_file[section_name]))
    if len(mandatory_parameters) != 0:
        raise ValueError("Missing mandatory parameter on " + section_name + ": " + str(mandatory_parameters) + ".")
    if None in list(yaml_file[section_name].values()):
        raise ValueError("Blank value on " + section_name + ".")


def validate_yaml_file(yaml_dict):
    validate_yaml_section(yaml_dict, 'artconfig', ['mainPath', 'startDate', 'endDate', 'runPreProcessing', 'runMohid',
                                                   'runPostProcessing'])
    if yaml_dict['artconfig']['runMohid']:
        validate_yaml_section(yaml_dict, 'Mohid', [])
        if 'mpi' in yaml_dict['Mohid']:
            validate_yaml_section(yaml_dict['Mohid'], 'mpi', [])
        for model in yaml_dict['Mohid']['Models']:
            validate_yaml_section(yaml_dict['Mohid']['Models'], model, [])


def validate_date(yaml):
    static.logger.debug("Validating Dates")
    try:
        start_date = datetime.datetime.strptime(yaml['artconfig']['startDate'], static.DATE_FORMAT)
        end_date = datetime.datetime.strptime(yaml['artconfig']['endDate'], static.DATE_FORMAT)
        total_days = yaml['artconfig']['daysPerRun'] * yaml['artconfig']['numberOfRuns']

        if start_date + datetime.timedelta(days=total_days) > end_date:
            raise ValueError("artconfig: The number of daysPerRun (" + str(yaml['artconfig']['daysPerRun']) +
                             ") in conjunction with the numberOfRuns (" + str(yaml['artconfig']['numberOfRuns']) +
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


