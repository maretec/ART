import yaml


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
    validate_yaml_section(yaml_dict, 'artconfig', ['mainPath','startDate', 'endDate', 'runPreProcessing','runMohid', 'runPostProcessing'])
    if yaml_dict['artconfig']['runMohid']:
        validate_yaml_section(yaml_dict, 'Mohid', [])
        if 'mpi' in yaml_dict['Mohid']:
            validate_yaml_section(yaml_dict['Mohid'], 'mpi',[])
        for model in yaml_dict['Mohid']['Models']:
            validate_yaml_section(yaml_dict['Mohid']['Models'], model, [])


def read_attribute(cfg, attribute):
    return cfg[attribute]
