import common.constants as static
import datetime
import common.file_modifier
import os.path
import common.config as cfg



def mpi_params(yaml_file):
    mohid = yaml_file['mohid']
    if 'mpi' in mohid.keys():
        if mohid['mpi']['enable']:
            exe_path = mohid['mpi']['exePath']
            keepDecomposedFiles = mohid['mpi']['keepDecomposedFiles']
            ddcParserNumProcessors = mohid['mpi']['ddcComposerNumProcessors']
            joinerVersion = mohid['mpi']['joinerVersion']


def create_model_dat(yaml, config):
    file = open(yaml['artconfig']['mainPath'] + "data/model.dat", "w+")
    common.file_modifier.line_creator(file, "START",
                                      common.file_modifier.date_to_mohid_date(config.global_initial_date))
    common.file_modifier.line_creator(file, "END",
                                      common.file_modifier.date_to_mohid_date(config.global_final_date))

    return None


def operational_mode():
    return


def no_operational_mode(yaml):
    path = yaml['artconfig']['mainPath'] + "data/model.dat"
    if os.path.isfile(path):
        common.file_modifier.modify_line(path, "START",
                                         common.file_modifier.date_to_mohid_date(cfg.global_initial_date))
        common.file_modifier.modify_line(path, "END",
                                         common.file_modifier.date_to_mohid_date(config.global_final_date))
    else:
        create_model_dat(yaml)
    return


def run_mohid(yaml, model):
    static.logger.debug("Run MOHID enabled")
    for i in range(1, cfg.number_of_runs+1):
        static.logger.info("========================================")
        static.logger.info("STARTING FORECAST ( " + str(i) + " of " + str(cfg.number_of_runs) + " )")
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
    common.file_modifier.line_creator(file, "START", common.file_modifier.date_to_mohid_date(cfg.global_initial_date))
    common.file_modifier.line_creator(file, "END", common.file_modifier.date_to_mohid_date(cfg.global_final_date))
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
                cfg.meteo_location = mainPath + "GeneralData/BoundaryConditions/Atmosphere/" + model['name'] + \
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
        initial_date = cfg.global_initial_date
        final_date = initial_date + datetime.timedelta(days=simulated_days)
        meteo_final_date = final_date.strftime(static.DATE_FOLDER_FORMAT)
    if model['fileNameFromModel']:
        sufix = model_name
        return (model['workPath'] + name + "_" + sufix + "_" + cfg.global_initial_date.strftime(static.DATE_FOLDER_FORMAT) +
                "_" + meteo_final_date + extension)
    elif model['genericFileName']:
        return (model['workPath'] + "meteo_" + cfg.global_initial_date.strftime(static.DATE_FOLDER_FORMAT) + "_" +
                meteo_final_date + extension)
    else:
        return None


def execute(yaml):
    if 'operationalMode' not in yaml['artconfig'] or yaml['artconfig']['operationalMode'] == 0:
        no_operational_mode(yaml)
    else:
        operational_mode()
    return None
