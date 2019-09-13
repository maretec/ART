import common.constants as static
import datetime
import common.file_modifier
import os.path
import common.config as cfg
from shutil import copy
import subprocess
import glob
import run_modules.pre_processing as pre_processing
import run_modules.post_processing as post_processing
import common.send_email as send_email


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


'''
Checks MOHID log to verify that the run was successful
'''
def verify_run(filename, messages):
    success_messages = ['Program Mohid Water successfully terminated', 'Program Mohid Water successfully terminated',  
    'Program MohidDDC successfully terminated']

    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        for i in range (-1, -21, -1):
            for message in messages:
                if message in lines[i]:
                    return True
    return False


def run_mohid(yaml):
    output_file_name = "MOHID_RUN_" + cfg.current_initial_date.strftime("%Y-%m-%d") + ".log"
    output_file = open(output_file_name, "w+")
    if 'mpi' in yaml['mohid'].keys() and yaml['mohid']['mpi']['enable']:
        static.logger.info("Starting MOHID MPI")
        #cwd is the working directory where the command will execute. stdout is the output file of the command
        subprocess.run(["mpiexec", "-np", str(yaml['mohid']['mpi']['totalProcessors']), "-f", "/opt/hosts",
                        yaml['mohid']['exePath']], cwd=os.path.dirname(yaml['mohid']['exePath']), 
                        stdout=output_file)
        output_file.close()

        #Mohid alwyas writes these strings in the last lines of the logs. We use it to verify that run was successful
        if not verify_run(output_file_name, ['Program Mohid Water successfully terminated', 
            'Program Mohid Land successfully terminated']):
            static.logger.info("MOHID RUN NOT SUCCESSFUL")
            raise ValueError("MOHID RUN NOT SUCCESSFUL")
        else:
            static.logger.info("MOHID RUN successful")

        #DDC is ran when an MPI run is done to join all the results into a single one.
        ddc_output_filename = "DDC_" + cfg.current_initial_date.strftime("%Y-%m-%d") + ".log"
        mohid_ddc_output_log = open(ddc_output_filename, "w+")
        subprocess.run("./MohidDDC.exe", cwd=os.path.dirname(yaml['mohid']['exePath']), stdout=mohid_ddc_output_log)
        mohid_ddc_output_log.close()
        if not verify_run(ddc_output_filename, ["Program MohidDDC successfully terminated"]):
            static.logger.info("MohidDDC NOT SUCCESSFUL")
            raise ValueError("MohidDDC NOT SUCCESSFUL")
        else:
            static.logger.info("MohidDDC successful")
    else:
        static.logger.info("Starting MOHID run")
        #cwd is the working directory where the command will execute. stdout is the output file of the command
        subprocess.run(yaml['mohid']['exePath'], cwd=os.path.dirname(yaml['mohid']['exePath']), 
        stdout=output_file)
        output_file.close()
    
        if not verify_run(output_file_name, ['Program Mohid Water successfully terminated', 
            'Program Mohid Land successfully terminated']):
            static.logger.info("MOHID RUN NOT SUCCESSFUL")
            raise ValueError("MOHID RUN NOT SUCCESSFUL")
        else:
            static.logger.info("MOHID RUN successful")


'''
MOHID needs the file model.dat to be changed, especially START and END times.
This function changes that file in each iteration to update START and END and other parameters that can be defined
in the yaml config file.
It receives the yaml object and the 'model' dictionary which is in 'mohid' dictionary.
'''
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


'''
Allows to create dynamic names for the files in static folders for OBC gathering.
Example: if given the datetime object that represents "2019-07-23" for initial_date and "2019-08-12" for final_date
it changes "Hydrodynamic_%Yi-%Mi-%di_%Yf-%Mf-%df" to "Hydrodynamic_2019-07-23_%2019-08-12"
'''
def create_file_name_with_date(filename, initial_date, final_date):
    if '%Yi' in filename:
        filename = filename.replace("%Yi", str(initial_date.year))
    if '%mi' in filename:
        filename = filename.replace("%Mi", str(initial_date.month))
    if '%di' in filename:
       filename = filename.replace("%di", str(initial_date.day))
    if '%Yf' in filename:
        filename = filename.replace("%Yf", str(final_date.year))
    if '%mi' in filename:
        filename = filename.replace("%Mf", str(final_date.month))
    if '%di' in filename:
        filename = filename.replace("%df", str(final_date.day))
    return filename

'''
Gathers boundary conditions for each model in the mohid block if the 'obc' dictionary has the parameter 'enable' and if
it is a different value from 0. The user can define the file type and the date format. It copies the files the user 
defined in the list 'files' in the yaml file.
'''
def gather_boundary_conditions(yaml, model):
    model_keys = model.keys()
    if 'obc' in model_keys and 'enable' in model['obc'].keys() and model['obc']['enable']:
        static.logger.info("OBC flag enabled")
        static.logger.info("Gathering Boundary Condition for " + model['name'])
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

        for n in range(0, simulations_available - 1, -1):
            obc_initial_date = cfg.current_initial_date + datetime.timedelta(days=n)
            obc_final_date = cfg.current_final_date + datetime.timedelta(days=n)

            obc_initial_date_str = obc_initial_date.strftime(date_format)
            obc_final_date_str = obc_final_date.strftime(date_format)

            workpath = model['obc']['workpath']

            '''
            if 'hasSolutionFromFile' it needs to get the OBC files from a "parent" model, and needs to follow the structure
            we use to backup our results. U
            '''
            if 'hasSolutionFromFile' in model_keys and model['hasSolutionFromFile']:
                obc_initial_date = cfg.current_initial_date + datetime.timedelta(days=n)
                obc_final_date = cfg.current_final_date + datetime.timedelta(days=simulations_available)

                obc_initial_date_str = obc_initial_date.strftime(date_format)
                obc_final_date_str = obc_final_date.strftime(date_format)

                static.logger.info("OBC Initial Date: " + obc_initial_date_str)
                static.logger.info("OBC Final Date: " + obc_final_date_str)
            
                folder_source = workpath + obc_initial_date_str + "_" + obc_final_date_str + "/"

                for file in model['obc']['files']:
                    file_source = folder_source + file + "." + file_type

                    if os.path.isfile(file_source):
                        dest_folder = yaml['artconfig']['mainPath'] + folder_label + model['name'] 
                        if not os.path.isdir(dest_folder):
                            os.makedirs(dest_folder)
                            file_destination = dest_folder + file + "." + file_type
                            copy(file_source, file_destination)
                            static.logger.info("Copying OBC from " + file_source + " to " + file_destination)
            else:
                '''
                subFolders within the workpath for the OBC files. They can be subdivided with year, month and year.
                '''
                if 'subFolders' in obc_keys and model['obc']['subFolders'] != 0:
                    if model['obc']['subFolders'] == 1:
                        workpath = workpath + str(obc_initial_date.year) + "/"
                    
                    elif model['obc']['subFolders'] == 2:
                        workpath = workpath + str(obc_initial_date.year) + "/" + str(obc_initial_date.month)

                    elif model['obc']['subFolders'] == 3:
                        workpath = workpath + str(obc_initial_date.year) + "/" + str(obc_initial_date.month) + "/" + \
                            str(obc_initial_date.days) + "/"
                    for file in model['obc']['files']:
                        filename = create_file_name_with_date(file, obc_initial_date, obc_final_date)
                        file_source = workpath +  filename + "." + file_type
                        if os.path.isfile(file_source):
                            dest_folder = yaml['artconfig']['mainPath'] + folder_label + model['name'] 
                            if not os.path.isdir(dest_folder):
                                os.makedirs(dest_folder)
                                file_destination = dest_folder + filename + "." + file_type
                                copy(file_source, file_destination)
                                static.logger.info("Copying OBC from " + file_source + " to " + file_destination)


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

                copy(meteo_file_source, meteo_file_dest)
                static.logger.info("Copied meteo file from " + meteo_file_source + " to " + meteo_file_dest)
                return
            else:
                continue

        static.logger.info("get_meteo_file: Meteo file could not be found. Check yaml file for configuration errors.")
        raise FileNotFoundError("get_meteo_file: Meteo file could not be found. Check yaml file for configuration " +
                                "errors.")


'''
Gets restart files from previous run. These files need to be put in /res folder of the project you're trying to run.
'''
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

    #glob creates a list with all files that match the regex experssion
    fin_files = glob.glob(path_fin_files + "*.fin")
    fin5_files = glob.glob(path_fin_files + "*.fin5")
    for file in fin_files:
        #the nomfich.dat file for mohid is not changed and when a restart file is generated it ends with _1.fin
        #and because of that an input restart file needs to finish with _0.fin. So we simply change it when we copy it.
        file_destination = restart_files_dest + os.path.split(file)[1].split("_")[0] + "_0.fin"
        static.logger.info("Restart Files: Copying " + file + " to " + file_destination)
        copy(file, file_destination)
    for file in fin5_files:
        file_destination = restart_files_dest + os.path.split(file)[1].split("_")[0] + "_0.fin5"
        static.logger.info("Restart Files: Copying " + file + " to " + file_destination)
        copy(file, file_destination)


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
        copy(file, file_destination)


'''
Backups all the results located in the res/ folder of the project. It ignores all the results before consolidation 
(those that start with "MPI_"). Copies all the consolidated .hdf5 files to the Results_HDF/ folder in the backup path
that the user defined. And the same goes for the Restart, TimeSeries and Discharges files.
'''
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
                    copy(file, file_destination)

        hdf5_files = glob.glob(results_path + "*.hdf5")
        if len(hdf5_files) > 0:
            if not os.path.isdir(results_storage):
                os.makedirs(results_storage)
           
           #only backup specific result files
            if 'resultList' in model_keys:
                for file in hdf5_files:
                    if os.path.split(file)[1].startswith("MPI"):
                        continue
                    file_name = os.path.split(file)[1]
                    name_array = file_name.split("_")
                    if name_array > 2:
                        #Hydrodynamic_1_Surface becomes Hydrodynamic_Surface
                        file_name = name_array[0] + "_" + name_array[2]
                    else:
                        file_type = name_array[-1].split(".")[1]
                        file_name = name_array[0] + "." + file_type

                    #if the file_name is not in the resultList it will be ignored
                    if file_name not in yaml['mohid']['models'][model]['resultList']:
                        continue

                    file_destination = results_storage + file_name
                    static.logger.info("Backup Simulation HDF Files: Copying " + file + " to " + file_destination)
            #defaults to backup all results files
            else:
                for file in hdf5_files:
                    if os.path.split(file)[1].startswith("MPI"):
                        continue
                    
                    file_name = os.path.split(file)
                    name_array = file_name.split("_")
                    if name_array > 2:
                        #Hydrodynamic_1_Surface becomes Hydrodynamic_Surface
                        file_name = name_array[0] + "_" + name_array[2]
                    else:
                        file_type = name_array[-1].split(".")[1]
                        file_name = name_array[0] + "." + file_type
                    file_destination = results_storage + file_name
                    static.logger.info("Backup Simulation HDF Files: Copying " + file + " to " + file_destination)

                    copy(file, file_destination)

        time_series_files = glob.glob(results_path + "Run1/*.*")
        if len(time_series_files) > 0:
            if not os.path.isdir(time_series_storage):
                os.makedirs(time_series_storage)
            for file in time_series_files:
                file_destination = time_series_storage + os.path.split(file)[1]
                copy(file, file_destination)


'''
Main cycle for the ART run. It has all the functions that are need for a project.
'''
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
    #run_mohid(yaml)
    backup_simulation(yaml)


def execute(yaml):
    artconfig_keys = yaml['artconfig'].keys()
    static.logger.info("Run MOHID enabled")
    #operational mode is used relative to the current day of the machine
    if yaml['artconfig']['operationalMode']:
        today = datetime.datetime.today()
        #Time needs to start on hour 00:00:00 otherwise will start the models at the wrong time
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
