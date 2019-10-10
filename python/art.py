import common.yaml_lib as yaml_lib
import run_modules.mohid as mohid
import run_modules.ww3 as ww3
import run_modules.wrf as wrf

import common.constants as static
import common.config as cfg
import datetime
import os.path
import sys


def validate_path(path):
    return os.path.exists(path)


def main():


    yaml = yaml_lib.open_yaml_file(sys.argv[1])

    #yaml_lib.validate_yaml_file(yaml)
    #yaml_lib.validate_date(yaml)
    validate_path(yaml['ARTCONFIG']['MAIN_PATH'])

    artconfig_keys = yaml['ARTCONFIG'].keys()

    running_mode(yaml)
            
    module = yaml['ARTCONFIG']['MODULE']
    if module == "mohid" or module == "Mohid":
        mohid.execute(yaml)
    elif module == "WW3":
        ww3.execute(yaml)
    elif module == "WRF":
        wrf.execute(yaml)
    else:
        raise ValueError("No valid simulation module given.")
        
    print("------------- ART RUN FINISHED -------------")


def running_mode(yaml):
    if yaml['ARTCONFIG']['OPERATIONAL_MODE']:
        static.logger.debug("Running in Operational Mode")
        today = datetime.datetime.today()
        cfg.global_initial_date = today + datetime.timedelta(days=yaml['ARTCONFIG']['REF_DAYS_TO_START'])
        cfg.global_final_date = (today + datetime.timedelta(days=yaml['ARTCONFIG']['NUMBER_OF_RUNS'])
                                    + datetime.timedelta(days=yaml['ARTCONFIG']['DAYS_PER_RUN'] - 1))
        cfg.number_of_runs = yaml['ARTCONFIG']['NUMBER_OF_RUNS']
        initial_date = cfg.global_initial_date
        final_date = initial_date + datetime.timedelta(days=yaml['ARTCONFIG']['DAYS_PER_RUN'])
        static.logger.debug("Initial Date : " + initial_date.strftime(static.DATE_FORMAT))
        static.logger.debug("Final Date: " + final_date.strftime(static.DATE_FORMAT))
        static.logger.debug("Number of runs : " + str(cfg.number_of_runs))
    elif not (yaml['ARTCONFIG']['OPERATIONAL_MODE']):
        try:
            static.logger.debug("Running in Normal Mode")
            cfg.global_initial_date = datetime.datetime.strptime(yaml['ARTCONFIG']['START_DATE'],
                                                                    static.DATE_FORMAT)
            cfg.global_final_date = datetime.datetime.strptime(yaml['ARTCONFIG']['END_DATE'], static.DATE_FORMAT)

            difference = cfg.global_final_date - cfg.global_initial_date
            cfg.number_of_runs = difference.days
        except KeyError:
            static.logger.warning("KeyError")
            cfg.number_of_runs = 1
            global_initial_date = datetime.datetime.today()
            global_final_date = global_initial_date + datetime.timedelta(days=yaml['ARTCONFIG']['DAYS_PER_RUN'])
            cfg.global_initial_date = datetime.datetime.strftime(datetime.datetime.today(), static.DATE_FORMAT)
            cfg.global_final_date = datetime.datetime.strftime(global_final_date, static.DATE_FORMAT)
        finally:
            static.logger.debug("Global Initial Date : " + cfg.global_initial_date.strftime(static.DATE_FORMAT))
            static.logger.debug("Global Final Date : " + cfg.global_final_date.strftime(static.DATE_FORMAT))
            static.logger.debug("Number of runs : " + str(cfg.number_of_runs))
    else:
        raise ValueError("artconfig: forecastMode value needs to be either a number or true/false")


if __name__ == "__main__":
    main()
