import common.constants as static
import datetime
import common.file_modifier
import os.path
import common.config as cfg
from shutil import copy2
import subprocess
import glob
import run_modules.pre_processing as pre_processing
import run_modules.post_processing as post_processing


def create_folder_structure(yaml, model):
    model_path = yaml['artconfig']['mainPath'] + model["path"]
    if not os.path.isdir(yaml['artconfig']['mainPath'] + "GeneralData/"):
        os.makedirs(yaml['artconfig']['mainPath'] + "GeneralData/Bathymetry")
        os.makedirs(yaml['artconfig']['mainPath'] + "GeneralData/BoundaryConditions")
        os.makedirs(yaml['artconfig']['mainPath'] + "GeneralData/TimeSeries")
    if not os.path.isdir(model_path + "res/"):
        os.makedirs(model_path + "res/Run1/")
    if not os.path.isdir(model_path + "data/"):
        os.makedirs(model_path + "data/")
    if not os.path.isdir(model_path + "exe/"):
        os.makedirs(model_path + "exe/")


def run_mohid(yaml):
    if 'mpi' in yaml['mohid'].keys() and yaml['mohid']['mpi']['enable']:
        static.logger.info("Starting MOHID MPI")
        return_object =  subprocess.run(["mpiexec", "-np", str(yaml['mohid']['mpi']['totalProcessors']), "-f", "/opt/hosts",
                        yaml['mohid']['exePath']], cwd=os.path.dirname(yaml['mohid']['exePath']), shell=False)
        return_object.check_returncode()
        return_object = subprocess.run("./MohidDDC.exe", cwd=os.path.dirname(yaml['mohid']['exePath']))
        return_object.check_returncode()
        static.logger.info("MOHID MPI run finished")
    else:
        static.logger.info("Starting MOHID run")
        return_object = subprocess.run(yaml['mohid']['exePath'], cwd=os.path.dirname(yaml['mohid']['exePath']), 
        shell=False)
        return_object.check_returncode()
        static.logger.info("MOHID run finished")


def change_model_dat(yaml, model):
    static.logger.info("Creating new model file for model: " + model['name'])
    keys = model.keys()
    path = yaml['artconfig']['mainPath'] + model['path'] + "data/"
    if not os.path.isdir(path):
        static.logger.info("Path for model folder does not exist.")
        static.logger.info("Check path parameters in the yaml file. Exiting ART.")
        exit(1)

    file_path = path + "Model_1.dat"
    file = open(file_path, 'w+')
    common.file_modifier.modify_line(file, "START",
                                      common.file_modifier.date_to_mohid_date(cfg.current_initial_date))
    static.logger.info("Changed START of " + str(file_path) + " to " +
                        common.file_modifier.date_to_mohid_date(cfg.current_initial_date))
    common.file_modifier.modify_line(file, "END", common.file_modifier.date_to_mohid_date(cfg.current_final_date))
    static.logger.info("Changed END of " + str(file_path) + " to " +
                        common.file_modifier.date_to_mohid_date(cfg.current_final_date))
    common.file_modifier.modify_line(file, "DT", str(model['dt']))
    if 'mohid.dat' in keys:
        for key in model['mohid.dat'].keys():
            common.file_modifier.modify_line(file, key, model['mohid.dat'][key])
    static.logger.info("Model " + model["name"] + " .dat file was created.")
    file.close()
    return


def gather_boundary_conditions(yaml, model):
    model_keys = model.keys()
    if 'obc' in model_keys and 'enable' in model['obc'].keys() and model['obc']['enable']:
        static.logger.info("OBC flag enabled")
        static.logger.info("Gathering Boundary Conditions for " + model['name'])
        obc_keys = model['obc'].keys()

        simulations_available = yaml['artconfig']['daysPerRun'] - model['obc']['simulatedDays']
        folder_label = "GeneralData/BoundaryConditions/Hydrodynamics/"

        date_format = "%Y-%m-%d"
        if 'dateFormat' in obc_keys:
            date_format = model['obc']['dateFormat']

        file_type = "hdf5"
        if 'fileType' in obc_keys:
            file_type = model['obc']['fileType']
        static.logger.debug("Boundary Conditions File Type: " + file_type)

        if 'hasSolutionFromFile' not in obc_keys or 'hasSolutionFromFile' in obc_keys and not \
                model['obc']['hasSolutionFromFile']:
            for n in range(0, simulations_available - 1, -1):
                obc_initial_date = cfg.current_initial_date + datetime.timedelta(days=n)
                obc_final_date = cfg.current_initial_date + datetime.timedelta(days=simulations_available)

                obc_initial_date = obc_initial_date.strftime(date_format)
                obc_final_date = obc_final_date.strftime(date_format)

               

                obc_source_path = model['obc']['workPath'] + model['obc']['prefix'] + "_" + model[
                    'name'] + obc_initial_date + "_" + obc_final_date + "." + file_type

                static.logger.info("OBC Source Path: " + obc_source_path)

                if os.path.isfile(obc_source_path):
                    obc_dest_folder = yaml['artconfig']['mainPath'] + folder_label + model['name'] + "/"
                    if not os.path.isdir(obc_dest_folder):
                        os.path.makedirs(obc_dest_folder)
                    obc_dest_file = obc_dest_folder + model['obc']['prefix'] + "_" + model['name'] + "." + file_type
                    static.logger.info("OBC File Destination: " + obc_dest_file)
                    copy2(obc_source_path, obc_dest_file)   
                else:
                    static.logger.info("Source files for OBC file not found: " + obc_source_path)
                    raise FileNotFoundError("Source file for OBC file not found: " + obc_source_path)

        elif 'hasSolutionFromFile' in obc_keys and model['obc']['hasSolutionFromFile']:
            static.logger.info("HasSolutionFromFile flag enabled")
            for n in range(0, simulations_available - 1, -1):
                obc_initial_date = cfg.current_initial_date + datetime.timedelta(days=n)
                obc_final_date = cfg.current_final_date + datetime.timedelta(days=simulations_available)

                obc_initial_date = obc_initial_date.strftime(date_format)
                obc_final_date = obc_final_date.strftime(date_format)

                static.logger.info("OBC Initial Date: " + obc_initial_date)
                static.logger.info("OBC Final Date: " + obc_final_date)

                hydro_source_path = model['obc']['workPath'] + str(obc_initial_date) + "_" + obc_final_date + "/" + \
                    "Hydrodynamic"
                water_source_path = model['obc']['workPath'] + str(obc_initial_date) + "_" + obc_final_date + "/" + \
                    "WaterProperties"

                if 'suffix' in obc_keys:
                    hydro_source_path += "_" + model['obc']['suffix']
                    water_source_path += "_" + model['obc']['suffix']

                hydro_source_path += "." + file_type
                water_source_path += "." + file_type

                if os.path.isfile(hydro_source_path):
                    if os.path.isfile(water_source_path):
                        dest_folder = yaml['artconfig']['mainPath'] + folder_label + model['name']
                        if not os.path.isdir(dest_folder):
                            os.makedirs(dest_folder)
                        hydro_dest_file = dest_folder + "/Hydrodynamic"
                        water_dest_file = dest_folder + "/WaterProperties"

                        if 'suffix' in obc_keys:
                            hydro_dest_file += "_" + model['obc']['suffix']
                            water_dest_file += "_" + model['obc']['suffix']

                        hydro_dest_file += "." + file_type
                        water_dest_file += "." + file_type

                        copy2(hydro_source_path, hydro_dest_file)
                        copy2(water_source_path, water_dest_file)
                    else:
                        static.logger.info(
                            "gather_boundary_conditions: File " + water_source_path + " does not exist.")
                else:
                    static.logger.info("gather_boundary_conditions: File " + hydro_source_path + " does not exist. ")


def get_meteo_file(yaml, model):
    model_keys = model.keys()
    if 'meteo' in model_keys and model['meteo']['enable']:
        static.logger.info("Gathering Meteo Files")
               
        meteo_models_keys = model['meteo']['models'].keys()

        for meteo_model in meteo_models_keys:
            meteo_keys = model['meteo']['models'][meteo_model].keys()

            date_format = "%Y-%m-%d"
            if 'dateFormat' in meteo_keys:
                date_format = model['meteo'][meteo_model]['dateFormat']

            meteo_initial_date = cfg.current_initial_date.strftime(date_format)
            if 'simulatedDays' in meteo_keys:
                meteo_final_date = cfg.current_initial_date + datetime.timedelta(days=model['meteo']['models']
                    [meteo_model]['simulatedDays'])
                meteo_final_date = meteo_final_date.strftime(date_format)
            else:
                meteo_final_date = cfg.current_final_date.strftime(date_format)

            static.logger.info("Meteo Initial Date: " + meteo_initial_date)
            static.logger.info("Meteo Final Date: " + meteo_final_date)


            file_type = "hdf5"
            if 'fileType' in meteo_keys:
                file_type = model['meteo']['models'][meteo_model]['fileType']

            if 'fileNameFromModel' in meteo_keys and model['meteo']['models'][meteo_model]['fileNameFromModel']:
                static.logger.info("Meteo: fileNameFromModel flag enabled")

                meteo_sufix = model['meteo']['models'][meteo_model]['name']
                static.logger.info("Meteo sufix: " + meteo_sufix)
                meteo_file_source = model['meteo']['models'][meteo_model]['workPath'] + \
                    model['meteo']['models'][meteo_model]['name'] + "_" + model['name'] + "_" + meteo_initial_date +\
                    "_" + meteo_final_date + "." + file_type
                static.logger.info("Meteo Source File: " + meteo_file_source)
            else:
                meteo_file_source = model['meteo']['models'][meteo_model][
                                        'workPath'] + "meteo" + "_" + meteo_initial_date \
                                    + "_" + meteo_final_date + "." + file_type
                static.logger.info("Meteo Source File: " + meteo_file_source)

            if os.path.isfile(meteo_file_source):
                meteo_file_dest_folder = yaml['artconfig']['mainPath'] + "GeneralData/BoundaryConditions/Atmosphere/" \
                    + model['name'] + "/" + model['meteo']['models'][meteo_model]['name'] + "/"

                if not os.path.isdir(meteo_file_dest_folder):
                    os.makedirs(meteo_file_dest_folder)

                meteo_file_dest = meteo_file_dest_folder + model['meteo']['models'][meteo_model]['name'] + "_" + \
                    model['name'] + "." + file_type
                static.logger.info("Meteo Destination File: " + meteo_file_dest)

                copy2(meteo_file_source, meteo_file_dest)
                static.logger.info("Copied meteo file from " + meteo_file_source + " to " + meteo_file_dest)
                return
            else:
                continue

        static.logger.info("get_meteo_file: Meteo file could not be found. Check yaml file for configuration errors.")
        raise FileNotFoundError("get_meteo_file: Meteo file could not be found. Check yaml file for configuration " +
                                "errors.")


def gather_restart_files(yaml, model):
    static.logger.info("Gathering the restart files for model: " + model['name'])

    date_format = "%Y-%m-%d"
    if 'dateFormat' in yaml['mohid'].keys():
        date_format = yaml['mohid']['dateFormat']

    previous_init_date = cfg.current_initial_date - datetime.timedelta(days=1)
    previous_final_date = previous_init_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
    static.logger.info("Restart Files Initial Day: " + previous_init_date.strftime(date_format))
    static.logger.info("Restart Files Final Day: " + previous_final_date.strftime(date_format))

    path_fin_files = model['storagePath'] + "Restart/" + previous_init_date.strftime(date_format) + "_" + \
        previous_final_date.strftime(date_format) + "/"

    static.logger.info("Source Restart Files: " + path_fin_files)

    if not os.path.isdir(path_fin_files):
        static.logger.info("Restart folder " + path_fin_files + "does not exist.")
        return

    model_keys = model.keys()

    restart_files_dest = yaml['artconfig']['mainPath'] + model['path'] + "res/"
    if not os.path.isdir(restart_files_dest):
        os.makedirs(restart_files_dest)

    fin_files = glob.glob(path_fin_files + "*.fin")
    fin5_files = glob.glob(path_fin_files + "*.fin5")
    for file in fin_files:
        file_destination = restart_files_dest + os.path.split(file)[1].split("_")[0] + "_0.fin"
        static.logger.info("Restart Files: Copying " + file + " to " + file_destination)
        copy2(file, file_destination)
    for file in fin5_files:
        static.logger.info(file)
        file_destination = restart_files_dest + os.path.split(file)[1].split("_")[0] + "_0.fin5"
        static.logger.info("Restart Files: Copying " + file + " to " + file_destination)
        copy2(file, file_destination)


def gather_discharges_files(yaml, model):
    static.logger.info("Gathering Discharges Files for model " + model['name'])

    date_format = "%Y-%m-%d"
    if 'dateFormat' in model['discharges'].keys():
        date_format = model['discharges']['dateFormat']

    path_discharges_files = model['discharges']['path'] + cfg.current_initial_date.strftime(date_format) + "_" + \
        cfg.current_final_date.strftime(date_format) + "/"
    
    static.logger.info("Source Discharges Files " + path_discharges_files)


    file_destination = yaml['artconfig']['mainPath'] + "GeneralData/BoundaryConditions/Discharges/" + model[
        'name'] + "/"
    
    static.logger.info("Discharges Files Destination " +  file_destination)

    files = glob.glob(path_discharges_files + "*.*")

    if not os.path.isdir(file_destination):
        os.makedirs(file_destination)

    for file in files:
        file_destination = file_destination + os.path.split(file)[1]
        static.logger.info("Discharges: Copying " + file + " to " + file_destination)
        copy2(file, file_destination)


def backup_simulation(yaml):
    date_format = "%Y-%m-%d"
    if 'dateFormat' in yaml['mohid'].keys():
        date_format = yaml['mohid']['dateFormat']

    initial_date = cfg.current_initial_date.strftime(date_format)
    tmp_date = cfg.current_initial_date + datetime.timedelta(yaml['artconfig']['daysPerRun'])
    final_date = tmp_date.strftime(date_format)

    static.logger.info("Simulation Results Initial Date: " + initial_date)
    static.logger.info("Simulation Results Final Date: " + final_date)

    for model in yaml['mohid']['models']:
        storage = yaml['mohid']['models'][model]['storagePath'] + "Restart/" + initial_date + "_" + final_date + "/"

        model_keys = yaml['mohid']['models'][model].keys()
        mohid_keys = yaml['mohid']
        results_path = yaml['artconfig']['mainPath'] + yaml['mohid']['models'][model]['path'] + "res/"

        generic_path = yaml['mohid']['models'][model]['storagePath']
        date_path = initial_date + "_" + final_date + "/"
        restart_storage = generic_path + "Restart/" + date_path
        results_storage = generic_path + "Results_HDF/" + date_path
        time_series_storage = generic_path + "Results_TimeSeries/" + date_path
        discharges_storage = generic_path + "Discharges/" + date_path

        if 'hasSolutionFromFile' not in model_keys or not yaml['mohid']['models'][model]['hasSolutionFromFile']:
            fin_files = glob.glob(results_path + "*_1.fin")
            fin5_files = glob.glob(results_path + "*_1.fin5")
            fin_files = fin5_files + fin_files
            if len(fin_files) > 0:
                if not os.path.isdir(restart_storage):
                    os.makedirs(restart_storage)
                for file in fin_files:
                    if os.path.split(file)[1].startswith("MPI"):
                        continue
                    file_destination = restart_storage + os.path.split(file)[1]
                    static.logger.info("Backup Simulation Fin_files: Copying " + file + " to " + file_destination)
                    copy2(file, file_destination)

        hdf5_files = glob.glob(results_path + "*.hdf5")
        if len(hdf5_files) > 0:
            if not os.path.isdir(results_storage):
                os.makedirs(results_storage)
            for file in hdf5_files:
                if os.path.split(file)[1].startswith("MPI"):
                    continue
                file_destination = results_storage + os.path.split(file)[1]
                static.logger.info("Backup Simulation HDF Files: Copying " + file + " to " + file_destination)

                copy2(file, file_destination)

        time_series_files = glob.glob(results_path + "Run1/*.*")
        if len(time_series_files) > 0:
            if not os.path.isdir(time_series_storage):
                os.makedirs(time_series_storage)
            for file in time_series_files:
                file_destination = time_series_storage + os.path.split(file)[1]
                copy2(file, file_destination)


def process_models(yaml):
    for model in yaml['mohid']['models']:
        create_folder_structure(yaml, yaml['mohid']['models'][model])
        get_meteo_file(yaml, yaml['mohid']['models'][model])
        gather_boundary_conditions(yaml, yaml['mohid']['models'][model])
        change_model_dat(yaml, yaml['mohid']['models'][model])
        gather_restart_files(yaml, yaml['mohid']['models'][model])
        if 'discharges' in yaml['mohid']['models'][model].keys() and 'enable' in \
                yaml['mohid']['models'][model]['discharges'].keys() and \
                yaml['mohid']['models'][model]['discharges']['enable']:
            gather_discharges_files(yaml, yaml['mohid']['models'][model])
    run_mohid(yaml)
    backup_simulation(yaml)


def execute(yaml):
    artconfig_keys = yaml['artconfig'].keys()
    static.logger.info("Run MOHID enabled")
    if yaml['artconfig']['operationalMode']:
        today = datetime.datetime.today()
        today = today.replace(minute=00, hour=00, second=00)
        cfg.global_initial_date = today + datetime.timedelta(days=yaml['artconfig']['refDayToStart'])
        for i in range(1, cfg.number_of_runs + 1):
            cfg.current_initial_date = cfg.global_initial_date + datetime.timedelta(days=i - 1)
            cfg.current_final_date = cfg.current_initial_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
            static.logger.info("========================================")
            static.logger.info("STARTING FORECAST ( " + str(i) + " of " + str(cfg.number_of_runs) + " )")
            static.logger.info("========================================")
            if 'runPreProcessing' in artconfig_keys and yaml['artconfig']['runPreProcessing']:
                static.logger.info("Executing Pre Processing")
                pre_processing.execute(yaml)
            if yaml['artconfig']['runSimulation']:
                process_models(yaml)
            if 'runPostProcessing' in artconfig_keys and yaml['artconfig']['runPostProcessing']:
                static.logger.info("Executing Post Processing")
                post_processing.execute(yaml)
    else:
        cfg.current_initial_date = cfg.global_initial_date.replace(minute=00, hour=00, second=00)
        cfg.current_final_date = cfg.global_initial_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
        while cfg.current_final_date <= cfg.global_final_date.replace(minute=00, hour=00, second=00):
            static.logger.info("========================================")
            static.logger.info("STARTING FORECAST (" + cfg.current_initial_date.strftime("%Y-%m-%d") + " to " +
                               cfg.current_final_date.strftime("%Y-%m-%d") + ")")
            static.logger.info("========================================")
            if 'runPreProcessing' in artconfig_keys and yaml['artconfig']['runPreProcessing']:
                static.logger.info("Executing Pre Processing")
                pre_processing.execute(yaml)
            if yaml['artconfig']['runSimulation']:
                process_models(yaml)
            if 'runPostProcessing' in artconfig_keys and yaml['artconfig']['runPostProcessing']:
                post_processing.execute(yaml)
                static.logger.info("Executing Post Processing")
            cfg.current_initial_date = cfg.current_initial_date + datetime.timedelta(
                days=yaml['artconfig']['daysPerRun'])
            cfg.current_final_date = cfg.current_final_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])

    return None
