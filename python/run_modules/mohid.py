import common.yaml_lib as yaml_lib
import common.constants as static
import datetime
import os.path
import common.file_modifier


class Config:
    global_initial_date = None
    global_final_date = None
    number_of_runs = None
    meteo_location = None


config = Config()


def validate_path(path):
    return os.path.exists(path)


def running_mode(yaml):
    global config
    if not yaml['artconfig']['classicMode']:
        if yaml['artconfig']['forecastMode']:
            static.logger.debug("Running in Forecast Mode")
            today = datetime.datetime.today()
            config.global_initial_date = today + datetime.timedelta(days=yaml['artconfig']['refDayToStart'])
            config.global_final_date = (today + datetime.timedelta(days=yaml['artconfig']['numberOfRuns'])
                                        + datetime.timedelta(days=yaml['artconfig']['daysPerRun'] - 1))
            config.number_of_runs = yaml['artconfig']['numberOfRuns']
            initial_date = config.global_initial_date
            final_date = initial_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
            static.logger.debug("Initial Date : " + initial_date.strftime(static.DATE_FORMAT))
            static.logger.debug("Final Date: " + final_date.strftime(static.DATE_FORMAT))
            static.logger.debug("Number of runs : " + str(config.number_of_runs))
        elif not (yaml['artconfig']['forecastMode']):
            try:
                static.logger.debug("Running in Hindcast Mode")
                config.global_initial_date = datetime.datetime.strptime(yaml['artconfig']['startDate'],
                                                                        static.DATE_FORMAT)
                config.global_final_date = datetime.datetime.strptime(yaml['artconfig']['endDate'], static.DATE_FORMAT)

                difference = config.global_final_date - config.global_initial_date
                config.number_of_runs = difference.days
            except KeyError:
                static.logger.warning("KeyError")
                config.number_of_runs = 1
                global_initial_date = datetime.datetime.today()
                global_final_date = global_initial_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
            finally:
                static.logger.debug("Global Initial Date : " + config.global_initial_date.strftime(static.DATE_FORMAT))
                static.logger.debug("Global Final Date : " + config.global_final_date.strftime(static.DATE_FORMAT))
                static.logger.debug("Number of runs : " + str(config.number_of_runs))
        else:
            raise ValueError("artconfig: forecastMode value needs to be either a number or true/false")
    elif yaml['artconfig']['classicMode']:
        static.logger.debug("Running in Classic Mode")
        config.number_of_runs = 1
        try:
            global_initial_date = datetime.datetime.strptime(yaml['artconfig']['startDate'], static.DATE_FORMAT)
            global_final_date = datetime.datetime.strptime(yaml['artconfig']['endDate'], static.DATE_FORMAT)
        except KeyError:
            static.logger.warning("KeyError")
            config.number_of_runs = 1
            config.global_initial_date = datetime.datetime.today()
            config.global_final_date = config.global_initial_date + \
                                       datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
        finally:
            static.logger.debug("Global Initial Date : " + config.global_initial_date.strftime(static.DATE_FORMAT))
            static.logger.debug("Global Final Date : " + config.global_final_date.strftime(static.DATE_FORMAT))
            static.logger.debug("Number of runs : " + str(config.number_of_runs))
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
    static.logger.debug("Run MOHID enabled")
    global config
    yaml_lib.validate_date(yaml)
    validate_path(yaml['artconfig']['mainPath'])
    for i in range(1, config.number_of_runs+1):
        static.logger.info("========================================")
        static.logger.info("STARTING FORECAST ( " + str(i) + " of " + str(config.number_of_runs) + " )")
        static.logger.info("========================================")

        if yaml['artconfig']['runPreProcessing']:
            run_pre_processing()

    if 'mpi' in yaml['mohid'].keys() and yaml['mohid']['mpi']['enable']:
        mpi = yaml['mohid']['mpi']
        flags = " -np " + str(yaml['mohid']['models'][model]['mpiProcessors']) + " -f /opt/hosts " + \
                yaml['mohid']['exePath']
        static.logger.info("Starting MOHID MPI run of model: " + yaml['mohid']['models'][model]['name'])
        # subprocess.run([mpi['exePath'], flags])
        static.logger.info("MOHID MPI run finished")
    else:
        static.logger.info("Starting MOHID run of model " + yaml['mohid']['models'][model]['name'])
        # subprocess.run(yaml['mohid']['exePath'])
        static.logger.info("MOHID run finished")


def run_pre_processing():
    static.logger.debug("Pre Processing Enabled")


def process_models(yaml):
    static.logger.debug("Creating new model files")
    for model in yaml['mohid']['models']:
        gather_boundary_conditions(model)
        create_new_model_file(model)
        gather_restart_files(model)


def create_new_model_file(model):
    keys = model.keys()
    file = open(model['path'] + "data/Model_" + str(model['runId']) + ".dat", 'w+')
    common.file_modifier.line_creator(file, "START", common.file_modifier.date_to_mohid_date(config.global_initial_date))
    common.file_modifier.line_creator(file, "END", common.file_modifier.date_to_mohid_date(config.global_final_date))
    common.file_modifier.line_creator(file, "DT", str(model['DT']))
    common.file_modifier.line_creator(file, "VARIABLEDT", "")
    if "maxdt" in keys:
        common.file_modifier.line_creator(file, "MAXDT", str(model['maxdt']))
    common.file_modifier.line_creator(file, "GMTREFERENCE", str(0))
    # TODO OPENMP
    if "langrarian" in keys:
        common.file_modifier.line_creator(file, "LAGRANGIAN", str(1))
    # TODO WAVES
    static.logger.debug("Model " + model["name"] + " .dat file was created.")
    file.close()
    return


# TODO not copy but redo NOMFINCH.DAT line 724 of MainModule vb
# TODO verify obc and meteo block on verify yaml
def gather_boundary_conditions(mainPath, model):
    static.logger.info("Gathering boundary conditions for model " + model['name'] + ".")
    for meteos in model['meteo'].keys():
        if model['meteo'][meteos]['enable']:
            filename = mainPath + "/" + model['meteo'][meteos]['workPath'] + model['meteo'][meteos]['modelName']
            if not os.path.isfile(filename):
                static.logger.info("Could not find meteo file from Solution with name - " + model['name'] + ".")
            else:
                static.logger.info("Meteo file solution found " + model['name'] + ".")
                config.meteo_location = mainPath + "GeneralData/BoundaryConditions/Atmosphere/" + model['name'] + \
                                        "/" + model['meteo'][meteos]['modelName'] + "/" +\
                                        model['meteo'][meteos]['modelName'] + "_" + model['name'] + ".hdf5"

        if model['hasSolutionFromFile'] or (model.keys().contains("obc") and model['obc']['enable']):
            if model['obc'].keys().contains('fromMercator') and model['obc']['fromMercator']:
                print("obc from mercator")


def gather_restart_files(model):
    static.logger.info("Gathering the restart files for each model domain.")


def get_meteo_filename(model, name, extension=".hdf5"):
    model_name = model['modelName']
    simulated_days = -99
    meteo_final_date = ""

    if "simulatedDays" in model:
        simulated_days = model['simulatedDays']
    sufix = "TAGUS3D"

    if model['simulatedDays'] == -99:
        print("tmp")
        # TODO falta final_date sera global_final_date???
    else:
        initial_date = config.global_initial_date
        final_date = initial_date + datetime.timedelta(days=simulated_days)
        meteo_final_date = final_date.strftime(static.DATE_FOLDER_FORMAT)
    if model['fileNameFromModel']:
        sufix = model_name
        return (model['workPath'] + name + "_" + sufix + "_" + config.global_initial_date.strftime(static.DATE_FOLDER_FORMAT) +
                "_" + meteo_final_date + extension)
    elif model['genericFileName']:
        return (model['workPath'] + "meteo_" + config.global_initial_date.strftime(static.DATE_FOLDER_FORMAT) + "_" +
                meteo_final_date + extension)
    else:
        return None


def execute():
    return None