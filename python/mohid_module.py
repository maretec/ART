import yaml_lib
import datetime
import logger
import os.path
import subprocess
import common.dat_modifier


class Config:
    global_initial_date = None
    global_final_date = None
    number_of_runs = None
    meteo_location = None


logger = logger.ArtLogger("MOHID", "log.txt")

DATE_FORMAT = '%Y %m %d %H %M %S'
DATE_FOLDER_FORMAT = '%Y-%m-%d'

config = Config()


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
    global config
    if not yaml['artconfig']['classicMode']:
        if yaml['artconfig']['forecastMode']:
            logger.debug("Running in Forecast Mode")
            today = datetime.datetime.today()
            config.global_initial_date = today + datetime.timedelta(days=yaml['artconfig']['refDayToStart'])
            config.global_final_date = (today + datetime.timedelta(days=yaml['artconfig']['numberOfRuns'])
                                        + datetime.timedelta(days=yaml['artconfig']['daysPerRun'] - 1))
            config.number_of_runs = yaml['artconfig']['numberOfRuns']
            initial_date = config.global_initial_date
            final_date = initial_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
            logger.debug("Initial Date : " + initial_date.strftime(DATE_FORMAT))
            logger.debug("Final Date: " + final_date.strftime(DATE_FORMAT))
            logger.debug("Number of runs : " + str(config.number_of_runs))
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
            config.global_final_date = config.global_initial_date + \
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
    logger.debug("Run MOHID enabled")
    global config
    validate_date(yaml)
    validate_path(yaml['artconfig']['mainPath'])
    for i in range(1, config.number_of_runs+1):
        logger.info("========================================")
        logger.info("STARTING FORECAST ( " + str(i) + " of " + str(config.number_of_runs) + " )")
        logger.info("========================================")

        if yaml['artconfig']['runPreProcessing']:
            run_pre_processing()

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


def run_pre_processing():
    logger.debug("Pre Processing Enabled")


def process_models(yaml):
    logger.debug("Creating new model files")
    for model in yaml['mohid']['models']:
        gather_boundary_conditions(model)
        create_new_model_file(model)
        gather_restart_files(model)


def create_new_model_file(model):
    keys = model.keys()
    file = open(model['path'] + "data/Model_" + str(model['runId']) + ".dat", 'w+')
    common.dat_modifier.line_creator(file, "START", common.dat_modifier.date_to_mohid_date(config.global_initial_date))
    common.dat_modifier.line_creator(file, "END", common.dat_modifier.date_to_mohid_date(config.global_final_date))
    common.dat_modifier.line_creator(file, "DT", str(model['DT']))
    common.dat_modifier.line_creator(file, "VARIABLEDT", "")
    if "maxdt" in keys:
        common.dat_modifier.line_creator(file, "MAXDT", str(model['maxdt']))
    common.dat_modifier.line_creator(file, "GMTREFERENCE", str(0))
    # TODO OPENMP
    if "langrarian" in keys:
        common.dat_modifier.line_creator(file, "LAGRANGIAN", str(1))
    # TODO WAVES
    logger.debug("Model " + model["name"] + " .dat file was created.")
    file.close()
    return


# TODO not copy but redo NOMFINCH.DAT
# TODO verify obc and meteo block on verify yaml
def gather_boundary_conditions(mainPath, model):
    logger.info("Gathering boundary conditions for model " + model['name'] + ".")
    for meteos in model['meteo'].keys():
        if model['meteo'][meteos]['enable']:
            filename = mainPath + "/" + model['meteo'][meteos]['workPath'] + model['meteo'][meteos]['modelName']
            if not os.path.isfile(filename):
                logger.info("Could not find meteo file from Solution with name - " + model['name'] + ".")
            else:
                logger.info("Meteo file solution found " + model['name'] + ".")
                config.meteo_location = mainPath + "GeneralData/BoundaryConditions/Atmosphere/" + model['name'] + \
                                        "/" + model['meteo'][meteos]['modelName'] + "/" +\
                                        model['meteo'][meteos]['modelName'] + "_" + model['name'] + ".hdf5"

        if model['hasSolutionFromFile'] or (model.keys().contains("obc") and model['obc']['enable']):
            if model['obc'].keys().contains('fromMercator') and model['obc']['fromMercator']:
                print("obc from mercator")


def gather_restart_files(model):
    logger.info("Gathering the restart files for each model domain.")


def get_meteo_filename(model, extension=".hdf5"):
    model_name = model['modelName']
    simulated_days = -99
    meteo_final_date = ""

    if model.keys().contains("simulatedDays"):
        simulated_days = model['simulatedDays']
    sufix = "TAGUS3D"

    if model['simulatedDays'] == -99:
        print("tmp")
        # TODO falta final_date sera global_final_date???
    else:
        initial_date = config.global_initial_date
        final_date = initial_date + datetime.timedelta(days=simulated_days)
        meteo_final_date = final_date.strftime(DATE_FOLDER_FORMAT)
    if model['fileNameFromModel']:
        sufix = model_name
        print(model['workPath'] + model + "_" + sufix + "_" + config.global_initial_date + "_" + meteo_final_date +
              extension)
    elif model['genericFileName']:
        print(model['workPath'] + "meteo_" + config.global_initial_date + "_" + meteo_final_date + extension)


# PSEUDO-MAIN

def main():
    yaml = yaml_lib.open_yaml_file('../default.yaml')
    running_mode(yaml)
    models = yaml['mohid']['models'].keys()
    #models.reverse()
    last_model = None
    for model in models:
        last_model = model
        create_new_model_file(yaml['mohid']['models'][model])
        #if yaml['artconfig']['runMohid']:
         #   run_mohid(yaml, model)


if __name__ == "__main__":
    main()
