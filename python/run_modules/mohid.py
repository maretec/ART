import common.constants as static
import datetime
import common.file_modifier
import os.path
import common.config as cfg
from shutil import copy2

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
    for i in range(1, cfg.number_of_runs+1):
        static.logger.info("========================================")
        static.logger.info("STARTING FORECAST ( " + str(i) + " of " + str(cfg.number_of_runs) + " )")
        static.logger.info("========================================")

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


def process_models(yaml):
    static.logger.debug("Creating new model files")
    for model in yaml['mohid']['models']:
        gather_boundary_conditions(model)
        change_model_dat(yaml, model)
        gather_restart_files(model)
        run_mohid(yaml, model)


def change_model_dat(yaml, model):
    keys = model.keys()
    path = yaml['artconfig']['mainPath'] + model['path']
    if not os.path.isdir(path):
        static.logger.debug("Path for model folder does not exist.")
        static.logger.debug("Check path parameters in the yaml file. Exiting ART.")
        exit(1)

    file_path = path + "data/Model_" + str(model['runId']) + ".dat"
    if not os.path.isfile(file_path):
        file = open(file_path, 'w+')
        common.file_modifier.line_creator(file, "START",
                                          common.file_modifier.date_to_mohid_date(cfg.global_initial_date))
        common.file_modifier.line_creator(file, "END", common.file_modifier.date_to_mohid_date(cfg.global_final_date))
        common.file_modifier.line_creator(file, "DT", str(model['DT']))
        for key in model['mohid.dat'].keys():
            common.file_modifier.line_creator(file, key, model['mohid.dat'][key])
        static.logger.debug("Model " + model["name"] + " .dat file was created.")
    else:
        file = open(file_path, 'w+')
        common.file_modifier.modify_line(file, "START",
                                         common.file_modifier.date_to_mohid_date(cfg.global_initial_date))
        common.file_modifier.modify_line(file, "END",
                                         common.file_modifier.date_to_mohid_date(cfg.global_final_date))
        if 'dt' in model.keys():
            common.file_modifier.modify_line(file, "DT",
                                             model['dt'])
    file.close()
    return


# TODO not copy but redo NOMFINCH.DAT line 724 of MainModule vb
# TODO verify obc and meteo block on verify yaml
def gather_boundary_conditions(yaml, model):
    model_keys = model.keys()
    if 'obc' in model_keys and 'enable' in model['obc'].key() and model['obc']['enable']:
        static.logger.debug("Gathering boundary conditions for " + model['name'])
        obc_keys = model['obc'].keys()

        file_type = "hdf5"
        if 'fileType' in obc_keys:
            static.logger.debug("Boundary Conditions File Type: " + model['obc']['fileType'])
            file_type = model['obc']['fileType']

        simulations_available = yaml['artconfig']['daysPerRun'] - model['obc']['simulatedDays']
        for n in range(0, simulations_available + 1, -1):
            obc_initial_date = cfg.global_initial_date + datetime.timedelta(days=n)
            obc_final_date = cfg.global_initial_date + datetime.timedelta(days=simulations_available)

            folder_label = "BoundaryConditions/Hydrodynamics/"

            obc_source_path = model['obc']['workPath'] + model['obc']['suffix'] + "_" + model['name'] + obc_initial_date \
                + "_" + obc_final_date + "." + file_type

            if os.path.isfile(obc_source_path):
                obc_dest_folder = yaml['mainPath'] + "GeneralData/" + folder_label + model['name'] + "/"
                if os.path.isdir(obc_dest_folder):
                    obc_dest_file = obc_dest_folder + model['obc']['suffix'] + "_" + model['name'] + "." + file_type
                    copy2(obc_source_path, obc_dest_file)




    # initial_date
    # final_date
    # model_keys = model.keys()
    # static.logger.info("Gathering boundary conditions for model " + model['name'] + ".")
    # if 'obc' in model_keys and 'enable' in model['obc'].keys() and model['obc']['enable']:
    #     obc_keys = model['obc'].keys()
    #     fileType = "hdf5"
    #     #TODO initial date e final date devem depender da run em que vão
    #     if 'subFolders' in obc_keys and model['obc']['subFolders']:
    #         return
    #     if 'fileType' in obc_keys:
    #         fileType = model['obc']['fileType']
    #     else:
    #
    #         source_obc_path = model['obc']['workPath'] + model['obc']['suffix'] + "_" + model['name'] + \
    #              cfg.global_initial_date + "_" + cfg.global_final_date + "." + fileType
    #     if not os.path.isdir(mainPath + model['path'] + "GeneralData/" + "BoundaryConditions/Hydrodynamics/" +
    #                          model['name'] + "/"):
    #         os.mkdir(mainPath + model['path'] + "GeneralData/" + "BoundaryConditions/Hydrodynamics/" +
    #                          model['name'] + "/")
    #     target_file_path = mainPath + model['path'] + "GeneralData/" + "BoundaryConditions/Hydrodynamics/" + \
    #                        model['name'] + "/" + model['obc']['suffix'] + model['name'] + "." + fileType




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
    process_models(yaml)
    return None
