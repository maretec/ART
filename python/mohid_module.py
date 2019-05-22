import yaml_lib
import datetime
import logger
import os.path
import subprocess


class Config:
    global_initial_date = None
    global_final_date = None
    number_of_runs = None


config = Config()

logger = logger.ArtLogger("MOHID", "log.txt")
DATE_FORMAT = '%Y %m %d %H %M %S'


def validate_date(yaml):
    logger.debug("Validating Dates")
    try:
        start_date = datetime.datetime.strptime(yaml['artconfig']['startDate'], DATE_FORMAT)
        end_date = datetime.datetime.strptime(yaml['artconfig']['endDate'], DATE_FORMAT)
        total_days = yaml['artconfig']['daysPerRun'] * yaml['artconfig']['numberOfRuns']

        if start_date + datetime.timedelta(days=total_days) > end_date:
            raise ValueError("artconfig: The number of daysPerRun (" + str(yaml['artconfig']['daysPerRun']) +
                             ") in conjunction with the numberOfRuns (" + str(yaml['artconfig']['numberOfRuns']) +
                             ") plus the startDate of this run (" + str(start_date) +
                             ") would lead to a final date of simulation beyond the user-specified endDate + "
                             "(" + str(end_date) + ").")
        else:
            logger.debug("Date Validation : Success")
    except KeyError:
        logger.warning("Either startDate or endDate were not specified in the configuration file ")
        logger.warning("Will from now on assume that startDate is TODAY and a forecast of 3 days")

    return


def validate_path(path):
    return os.path.exists(path)


def running_mode(yaml):
    if not yaml['artconfig']['classicMode']:
        if yaml['artconfig']['forecastMode']:
            logger.debug("Running in Forecast Mode")
            today = datetime.datetime.today()
            config.global_initial_date = today + datetime.timedelta(days=yaml['artconfig']['refDayToStart'])
            config.global_final_date = (today + datetime.timedelta(days=yaml['artconfig']['numberOfRuns'])
                                        + datetime.timedelta(days=yaml['artconfig']['daysPerRun'] - 1))

            initial_date = config.global_initial_date
            final_date = initial_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
            logger.debug("Initial Date : " + initial_date.strftime(DATE_FORMAT))
            logger.debug("Final Date: " + final_date.strftime(DATE_FORMAT))
            logger.debug("Number of runs : " + str(yaml['artconfig']['numberOfRuns']))
        elif not (yaml['artconfig']['forecastMode']):
            try:
                logger.debug("Running in Hindcast Mode")
                config.global_initial_date = datetime.datetime.strptime(yaml['artconfig']['startDate'], DATE_FORMAT)
                config.global_final_date = datetime.datetime.strptime(yaml['artconfig']['endDate'], DATE_FORMAT)

                difference = config.global_final_date - config.global_initial_date
                config.number_of_runs = difference.days
            except KeyError:
                logger.warning("KeyError")
                config.number_of_runs = 1
                global_initial_date = datetime.datetime.today()
                global_final_date = global_initial_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
            finally:
                logger.debug("Global Initial Date : " + config.global_initial_date.strftime(DATE_FORMAT))
                logger.debug("Global Final Date : " + config.global_final_date.strftime(DATE_FORMAT))
                logger.debug("Number of runs : " + str(config.number_of_runs))
        else:
            raise ValueError("artconfig: forecastMode value needs to be either a number or true/false")
    elif yaml['artconfig']['classicMode']:
        logger.debug("Running in Classic Mode")
        config.number_of_runs = 1
        try:
            global_initial_date = datetime.datetime.strptime(yaml['artconfig']['startDate'], DATE_FORMAT)
            global_final_date = datetime.datetime.strptime(yaml['artconfig']['endDate'], DATE_FORMAT)
        except KeyError:
            logger.warning("KeyError")
            config.number_of_runs = 1
            config.global_initial_date = datetime.datetime.today()
            config.global_final_date = Config.global_initial_date + \
                                       datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
        finally:
            logger.debug("Global Initial Date : " + config.global_initial_date.strftime(DATE_FORMAT))
            logger.debug("Global Final Date : " + config.global_final_date.strftime(DATE_FORMAT))
            logger.debug("Number of runs : " + str(config.number_of_runs))
    else:
        raise ValueError("artconfig: classicMode value needs to be either a number or true/false")


def mpi_params(yaml_file):
    mohid = yaml_file['mohid']
    if 'mpi' in mohid.keys():
        if mohid['mpi']['enable']:
            exe_path = mohid['mpi']['exePath']
            keepDecomposedFiles = mohid['mpi']['keepDecomposedFiles']
            ddcParserNumProcessors = mohid['mpi']['ddcComposerNumProcessors']
            joinerVersion = mohid['mpi']['joinerVersion']


def run_mohid(yaml, model):
    validate_date(yaml)
    validate_path(yaml['artconfig']['mainPath'])
    # HELP
    # for i in range(1, config.number_of_runs):
    #     logger.info("========================================")
    #     logger.info("STARTING FORECAST ( " + str(i) + " of " + str(Config.number_of_runs) + " )")
    #     logger.info("========================================")

    if 'mpi' in yaml['mohid'].keys() and yaml['mohid']['mpi']['enable']:
        mpi = yaml['mohid']['mpi']
        flags = " -np " + str(yaml['mohid']['models'][model]['mpiProcessors']) + " -f /opt/hosts " + \
                yaml['mohid']['exePath']
        logger.info("Starting MOHID MPI run of model: " + yaml['mohid']['models'][model]['name'])
        # subprocess.run([mpi['exePath'], flags])
        logger.info("MOHID MPI run finished")
    else:
        logger.info("Starting MOHID run of model " + yaml['mohid']['models'][model]['name'])
        # subprocess.run(yaml['mohid']['exePath'])
        logger.info("MOHID run finished")


# PSEUDO-MAIN


yaml = yaml_lib.open_yaml_file('../default.yaml')
running_mode(yaml)
models = yaml['mohid']['models'].keys()
models.reverse()
last_model = None
for model in models:
    last_model = model
    run_mohid(yaml, model)
