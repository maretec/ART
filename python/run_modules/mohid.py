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
import time

def create_folder_structure(yaml, model):
    model_path = yaml['ARTCONFIG']['MAIN_PATH'] + model['PATH']
    if not os.path.isdir(yaml['ARTCONFIG']['MAIN_PATH'] + "GeneralData/"):
        os.makedirs(yaml['ARTCONFIG']['MAIN_PATH'] + "GeneralData/Bathymetry")
        os.makedirs(yaml['ARTCONFIG']['MAIN_PATH'] + "GeneralData/BoundaryConditions")
        os.makedirs(yaml['ARTCONFIG']['MAIN_PATH'] + "GeneralData/TimeSeries")
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
        for i in range (-1, -100, -1):
            for message in messages:
                if message in lines[i]:
                    return True
    return False


def run_mohid(yaml):
    output_file_name = "MOHID_RUN_" + cfg.current_initial_date.strftime("%Y-%m-%d") + ".log"
    output_file = open(output_file_name, "w+")
    if 'MPI' in yaml['MOHID'].keys() and yaml['MOHID']['MPI']['ENABLE']:
        static.logger.info("Starting MOHID MPI")
        #cwd is the working directory where the command will execute. stdout is the output file of the command
        # subprocess.run(["mpiexec", "-np", str(yaml['MOHID']['MPI']['TOTAL_PROCESSORS']), "-f", "/opt/hosts",
                        # yaml['MOHID']['EXE_PATH'], "&"], cwd=os.path.dirname(yaml['MOHID']['EXE_PATH']),
                        # stdout=output_file)
        subprocess.run(["mpiexec", "-np", str(yaml['MOHID']['MPI']['TOTAL_PROCESSORS']),
                        yaml['MOHID']['EXE_PATH'], "&"], cwd=os.path.dirname(yaml['MOHID']['EXE_PATH']),
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
        # subprocess.run(["./MohidDDC.exe", "&"], cwd=os.path.dirname(yaml['MOHID']['EXE_PATH']), stdout=mohid_ddc_output_log)
        subprocess.run(["MohidDDC.exe", yaml['MOHID']['EXE_PATH'], "&"], cwd=os.path.dirname(yaml['MOHID']['EXE_PATH']), stdout=mohid_ddc_output_log)
        mohid_ddc_output_log.close()
        if not verify_run(ddc_output_filename, ["Program MohidDDC successfully terminated"]):
            static.logger.info("MohidDDC NOT SUCCESSFUL")
            raise ValueError("MohidDDC NOT SUCCESSFUL")
        else:
            static.logger.info("MohidDDC successful")
    else:
        static.logger.info("Starting MOHID run")
        #cwd is the working directory where the command will execute. stdout is the output file of the command
        subprocess.run([yaml['MOHID']['EXE_PATH'], "&"], cwd=os.path.dirname(yaml['MOHID']['EXE_PATH']),
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
    static.logger.info("Creating new model file for model: " + model['NAME'])
    keys = model.keys()
    path = yaml['ARTCONFIG']['MAIN_PATH'] + model['PATH'] + "data/"
    if not os.path.isdir(path):
        static.logger.info("Path for model folder does not exist.")
        static.logger.info("Check path parameters in the yaml file. Exiting ART.")
        exit(1)

    file_path = path + "Model_1.dat"
    file = open(file_path, 'w+')
    common.file_modifier.modify_start_dat_date(file, common.file_modifier.date_to_mohid_date(cfg.current_initial_date))
    static.logger.info("Changed START of " + str(file_path) + " to " +
                        common.file_modifier.date_to_mohid_date(cfg.current_initial_date))
    common.file_modifier.modify_end_dat_date(file, common.file_modifier.date_to_mohid_date(cfg.current_final_date))
    static.logger.info("Changed END of " + str(file_path) + " to " +
                        common.file_modifier.date_to_mohid_date(cfg.current_final_date))
    common.file_modifier.modify_line(file, "DT", str(model['DT']))
    if 'OPENMP' in yaml['MOHID'].keys() and yaml['MOHID']['OPENMP']['ENABLE']:
        if 'TOTAL_PROCESSORS' in yaml['MOHID']['OPENMP']:
            num_omp_processors = yaml['MOHID']['OPENMP']['TOTAL_PROCESSORS']
        else:
            static.logger.info("NUM_PROCESSORS not defined. model will use max threads available")
        common.file_modifier.modify_line(file, "OPENMP_NUM_THREADS", str(num_omp_processors))
    if 'mohid.dat' in keys:
        for key in model['mohid.dat'].keys():
            common.file_modifier.modify_line(file, key, model['mohid.dat'][key])
    static.logger.info("Model " + model['NAME'] + " .dat file was created.")
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
        filename = filename.replace("%mi", str(initial_date.month))
    if '%di' in filename:
       filename = filename.replace("%di", str(initial_date.day))
    if '%Yf' in filename:
        filename = filename.replace("%Yf", str(final_date.year))
    if '%mf' in filename:
        filename = filename.replace("%mf", str(final_date.month))
    if '%df' in filename:
        filename = filename.replace("%df", str(final_date.day))
    return filename

'''
Gathers boundary conditions for each model in the model block if the 'obc' dictionary has the parameter 'enable' and if
it is a different value from 0. The user can define the file type and the date format. It copies the files the user 
defined in the list 'files' in the yaml file.
'''
def gather_boundary_conditions(yaml, model):
    model_keys = model.keys()
    if 'OBC' in model_keys:
        for obc_model in model['OBC']:
            if 'ENABLE' in model['OBC'][obc_model].keys() and model['OBC'][obc_model]['ENABLE']:
                static.logger.info("OBC flag enabled")
                static.logger.info("Gathering Boundary Condition for " + model['NAME'])
                obc_keys = model['OBC'][obc_model].keys()

                simulations_available = yaml['ARTCONFIG']['DAYS_PER_RUN'] - model['OBC'][obc_model]['SIMULATED_DAYS']
                folder_label = "GeneralData/BoundaryConditions/Hydrodynamics/"

                date_format = "%Y-%m-%d"
                if 'DATE_FORMAT' in obc_keys:
                    date_format = model['OBC'][obc_model]['DATE_FORMAT']

                file_type = "hdf5"
                if 'FILE_TYPE' in obc_keys:
                    file_type = model['OBC'][obc_model]['FILE_TYPE']
                
                
                OBC_folder = model['NAME']
                if 'NAME' in obc_keys:
                    OBC_folder = model['OBC'][obc_model]['NAME']
                    user_dest_filename = model['OBC'][obc_model]['NAME']


                static.logger.debug("Boundary Conditions File Type: " + file_type)

                for n in range(0, simulations_available - 1, -1):
                    obc_initial_date = cfg.current_initial_date + datetime.timedelta(days=n)
                    obc_final_date = cfg.current_final_date + datetime.timedelta(days=n)

                    obc_initial_date_str = obc_initial_date.strftime(date_format)
                    obc_final_date_str = obc_final_date.strftime(date_format)

                    workpath = model['OBC'][obc_model]['WORK_PATH']

                    '''
                    if 'HAS_SOLUTION_FROM_FILE' it needs to get the OBC files from a "parent" model, and needs to follow the structure
                    we use to backup our results.
                    '''
                    if 'HAS_SOLUTION_FROM_FILE' in model_keys and model['HAS_SOLUTION_FROM_FILE']:
                        obc_initial_date = cfg.current_initial_date + datetime.timedelta(days=n)
                        obc_final_date = cfg.current_final_date + datetime.timedelta(days=simulations_available)

                        obc_initial_date_str = obc_initial_date.strftime(date_format)
                        obc_final_date_str = obc_final_date.strftime(date_format)

                        static.logger.info("OBC Initial Date: " + obc_initial_date_str)
                        static.logger.info("OBC Final Date: " + obc_final_date_str)

                        folder_source = workpath + obc_initial_date_str + "_" + obc_final_date_str + "/"

                        for obc_file in model['OBC'][obc_model]['FILES']:
                            file_source = folder_source + obc_file + "." + file_type


                            if os.path.isfile(file_source):
                                dest_folder = yaml['ARTCONFIG']['MAIN_PATH'] + folder_label + OBC_folder + "/"
                                if not os.path.isdir(dest_folder):
                                    os.makedirs(dest_folder)
                                else:
                                    file_destination = dest_folder + obc_file + "." + file_type
                                    copy(file_source, file_destination)
                                    static.logger.info("Copying OBC from " + file_source + " to " + file_destination)

                    else:
                        '''
                        SUB_FOLDERS within the WORKPATH for the OBC files. They can be subdivided with year, month and year.
                        '''
                        if 'SUBFOLDERS' in obc_keys:
                            if model['OBC'][obc_model]['SUBFOLDERS'] == 0:
                                workpath = workpath
                            elif model['OBC'][obc_model]['SUBFOLDERS'] == 1:
                                workpath = workpath + str(obc_initial_date.year) + "/"

                            elif model['OBC'][obc_model]['SUBFOLDERS'] == 2:
                                workpath = workpath + str(obc_initial_date.year) + "/" + str(obc_initial_date.month)

                            elif model['OBC'][obc_model]['SUBFOLDERS'] == 3:
                                workpath = workpath + str(obc_initial_date.year) + "/" + str(obc_initial_date.month) + "/" + \
                                    str(obc_initial_date.days) + "/"
                            elif model['OBC'][obc_model]['SUBFOLDERS'] == 4:
                                workpath = workpath + obc_initial_date_str + "_" + obc_final_date_str + "/"
                            for file in model['OBC'][obc_model]['FILES']:
                                if model['OBC'][obc_model]['SUBFOLDERS'] == 4:
                                    file_source = workpath + file + "." + file_type
                                    filename = file
                                else:
                                    filename = create_file_name_with_date(file, obc_initial_date, obc_final_date)
                                    file_source = workpath +  filename + "." + file_type

                                if model['OBC'][obc_model]['SUBFOLDERS'] == 0:
                                    filename = user_dest_filename

                                if os.path.isfile(file_source):
                                    dest_folder = yaml['ARTCONFIG']['MAIN_PATH'] + folder_label + OBC_folder + "/"
                                    if not os.path.isdir(dest_folder):
                                        os.makedirs(dest_folder)
                                    else:
                                        file_destination = dest_folder + filename + "." + file_type
                                        copy(file_source, file_destination)
                                        static.logger.info("Copying OBC from " + file_source + " to " + file_destination)
                                else:
                                    static.logger.info("File " + file_source + " does not exist ")

def get_meteo_file(yaml, model):
    model_keys = model.keys()
    if 'METEO' in model_keys and model['METEO']['ENABLE']:
        static.logger.info("Gathering Meteo Files")

        meteo_models_keys = model['METEO']['MODELS'].keys()

        for meteo_model in meteo_models_keys:
            meteo_keys = model['METEO']['MODELS'][meteo_model].keys()

            date_format = "%Y-%m-%d"
            if 'DATE_FORMAT' in meteo_keys:
                date_format = model['METEO'][meteo_model]['DATE_FORMAT']

            meteo_initial_date = cfg.current_initial_date.strftime(date_format)
            if 'SIMULATED_DAYS' in meteo_keys:
                meteo_final_date = cfg.current_initial_date + datetime.timedelta(days=model['METEO']['MODELS']
                    [meteo_model]['SIMULATED_DAYS'])
                meteo_final_date = meteo_final_date.strftime(date_format)
            else:
                meteo_final_date = cfg.current_final_date.strftime(date_format)

            static.logger.info("Meteo Initial Date: " + meteo_initial_date)
            static.logger.info("Meteo Final Date: " + meteo_final_date)

            file_type = "hdf5"
            if 'FILE_TYPE' in meteo_keys:
                file_type = model['METEO']['MODELS'][meteo_model]['FILE_TYPE']

            if 'FILENAME_FROM_MODEL' in meteo_keys and model['METEO']['MODELS'][meteo_model]['FILENAME_FROM_MODEL']:
                static.logger.info("Meteo: fileNameFromModel flag enabled")

                meteo_sufix = model['METEO']['MODELS'][meteo_model]['NAME']
                static.logger.info("Meteo sufix: " + meteo_sufix)
                meteo_file_source = model['METEO']['MODELS'][meteo_model]['WORKPATH'] + \
                    model['METEO']['MODELS'][meteo_model]['NAME'] + "_" + model['NAME'] + "_" + meteo_initial_date +\
                    "_" + meteo_final_date + "." + file_type
                static.logger.info("Meteo Source File: " + meteo_file_source)
            else:
                meteo_file_source = model['METEO']['MODELS'][meteo_model]['WORKPATH'] + \
                    "meteo" + "_" + meteo_initial_date \
                                    + "_" + meteo_final_date + "." + file_type
                static.logger.info("Meteo Source File: " + meteo_file_source)

            if os.path.isfile(meteo_file_source):
                meteo_file_dest_folder = yaml['ARTCONFIG']['MAIN_PATH'] + "GeneralData/BoundaryConditions/Atmosphere/" \
                    + model['NAME'] + "/" + model['METEO']['MODELS'][meteo_model]['NAME'] + "/"

                if not os.path.isdir(meteo_file_dest_folder):
                    os.makedirs(meteo_file_dest_folder)

                meteo_file_dest = meteo_file_dest_folder + model['METEO']['MODELS'][meteo_model]['NAME'] + "_" + \
                    model['NAME'] + "." + file_type
                static.logger.info("Meteo Destination File: " + meteo_file_dest)

                copy(meteo_file_source, meteo_file_dest)
                static.logger.info("Copied meteo file from " + meteo_file_source + " to " + meteo_file_dest)
                return
            else:
                continue

    #static.logger.info("get_meteo_file: Meteo file could not be found. Check yaml file for configuration errors.")
    #raise FileNotFoundError("get_meteo_file: Meteo file could not be found. Check yaml file for configuration " +
                            #"errors.")


'''
Gets restart files from previous run. These files need to be put in /res folder of the project you're trying to run.
'''
def gather_restart_files(yaml, model):
    static.logger.info("Gathering the restart files for model: " + model['NAME'])

    date_format = "%Y-%m-%d"
    if 'dateFormat' in yaml['MOHID'].keys():
        date_format = yaml['MOHID']['DATE_FORMAT']

    previous_init_date = cfg.current_initial_date - datetime.timedelta(days=1)
    previous_final_date = previous_init_date + datetime.timedelta(days=yaml['ARTCONFIG']['DAYS_PER_RUN'])
    static.logger.info("Restart Files Initial Day: " + previous_init_date.strftime(date_format))
    static.logger.info("Restart Files Final Day: " + previous_final_date.strftime(date_format))

    path_fin_files = model['STORAGE_PATH'] + "Restart/" + previous_init_date.strftime(date_format) + "_" + \
        previous_final_date.strftime(date_format) + "/"

    static.logger.info("Source Restart Files: " + path_fin_files)

    if not os.path.isdir(path_fin_files):
        static.logger.info("Restart folder " + path_fin_files + "does not exist.")
        return

    model_keys = model.keys()

    restart_files_dest = yaml['ARTCONFIG']['MAIN_PATH'] + model['PATH'] + "res/"
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
    static.logger.info("Gathering Discharges Files for model " + model['NAME'])

    for discharge in model['DISCHARGES']:
        static.logger.info("Gathering Discharge Files for discharge block" + discharge)
        date_format = "%Y-%m-%d"
        if 'dateFormat' in model['DISCHARGES'][discharge].keys():
            date_format = model['DISCHARGES'][discharge]['DATE_FORMAT']

        path_discharges_files = model['DISCHARGES'][discharge]['PATH'] + \
            cfg.current_initial_date.strftime(date_format) + "_" + \
            cfg.current_final_date.strftime(date_format) + "/"

        static.logger.info("Source Discharges Files " + path_discharges_files)


        file_destination = yaml['ARTCONFIG']['MAIN_PATH'] + \
            "GeneralData/BoundaryConditions/Discharges/" + model['NAME'] + "/"

        static.logger.info("Discharges Files Destination " +  file_destination)

        files = glob.glob(path_discharges_files + "*.*")

        if not os.path.isdir(file_destination):
            os.makedirs(file_destination)

        for file in files:
            file_destination = file_destination + os.path.split(file)[1]
            static.logger.info("Discharges: Copying " + file + " to " + file_destination)
            copy(file, file_destination)


def check_triggers(yaml, days_run, days_per_run):
    """ Receives a yaml config file with only the trigger subtree and checks the trigger entries for correct
    configuration. Checks for dependencies within the models. The execution is never interrupted by this function,
    any errors found are reported in the logger.
    """
    if yaml['ENABLE'] == 1 :
        if static.CHECK_ALL in yaml:
            check = yaml[static.CHECK_ALL]
        else:
            check = True

        if (days_run == 0 or check) :

            if static.FOLDERS_TO_WATCH in yaml:
                folders = yaml[static.FOLDERS_TO_WATCH]
            else:
                folders = None
                static.logger.info("No folders to watch on triggers. " + static.FOLDERS_TO_WATCH + " is empty.")

            if static.TRIGGER_MAX_WAIT in yaml:
                timer = yaml[static.TRIGGER_MAX_WAIT] * 3600
            else:
                timer = static.DEFAULT_MAX_WAIT*3600
                static.logger.info("No waiting time on triggers. " + static.TRIGGER_MAX_WAIT + "is empty. Assigning default "
                                                                                            "max wait time of 6 hours.")

            if static.TRIGGER_POLLING_RATE in yaml:
                rate = yaml[static.TRIGGER_POLLING_RATE]
            else:
                rate = static.DEFAULT_POLLING_RATE
                static.logger.info("No polling rate on triggers. " + static.TRIGGER_POLLING_RATE + " is empty. Assigning "
                                                                                                "default polling rate of "
                                                                                                "120 seconds.")
            date_format = "%Y-%m-%d"
            initial_date = cfg.current_initial_date.strftime(date_format)
            tmp_date = cfg.current_initial_date + datetime.timedelta(days_per_run)
            final_date = tmp_date.strftime(date_format)
            if folders:
                for folder in folders:
                    file = folder + initial_date + "_" + final_date + ".dat"
                    while not os.path.exists(file):
                        static.logger.info("waiting for Trigger file to be created in watch folder")
                        time.sleep(rate)
                        timer = timer - rate
                        if timer < 0:
                            static.logger.info("Reached max waiting time while trying to find file " + file + ". Resuming \
                             execution without the file...")
                            return

                    finished = False
                    static.logger.info("Checking Trigger file status - will advance when becomes Finished")
                    while not finished:
                        f = open(file, 'r')
                        for line in f.readlines():
                            if line.startswith("STATUS"):
                                if "FINISHED" in line:
                                    finished = True
                                    static.logger.info("File " + file + " found with status FINISHED.")
                        f.close()
                        if not finished:
                            time.sleep(rate * 2)  # rate is doubled to prevent file error with several opens and closes
                            timer = timer - rate * 2
                            if timer < 0:
                                static.logger.info("Reached max waiting time while waiting for file " + file + " to change \
                                 status to finished. Resuming execution without the correct status on this file...")
                                return

def write_trigger(yaml, main_path, days_per_run, stage):
    """ Receives a yaml config file with only the trigger subtree and writes the trigger file 
        .The execution is never interrupted by this function,any errors found are reported in the logger.
    """
    if yaml['ENABLE'] == 1:
        if static.WRITE_TRIGGER in yaml:
            output_trigger = yaml[static.WRITE_TRIGGER]
            dest_folder = main_path + "Log" + "/"
        else:
            output_trigger = False
            static.logger.info("Output trigger not set." + static.WRITE_TRIGGER + " is empty.")

        if output_trigger:
            date_format = "%Y-%m-%d"
            initial_date = cfg.current_initial_date.strftime(date_format)
            tmp_date = cfg.current_initial_date + datetime.timedelta(days_per_run)
            final_date = tmp_date.strftime(date_format)
            filename = dest_folder + initial_date + "_" + final_date + ".dat"

            now = datetime.datetime.now()
            system_time = now.strftime("%Y-%m-%d %H:%M")

            file = open(filename, 'w')
            file.write('\n')
            file.write('FILE AUTOMATICALLY GENERATED TO BE USED AS TRIGGER')
            file.write('\n')
            file.write('DO NOT EDIT, CHANGE, MOVE, DELETE THIS FILE!')
            file.write('\n')
            file.write('\n')

            if stage == "Running":
                file.write('MOHID is running for the following period:')
            elif stage == "Finished":
                file.write('MOHID forecast and backup finished for the following period:')

            file.write('START                         : ' + common.file_modifier.date_to_mohid_date(cfg.current_initial_date))
            file.write('END                           : ' + common.file_modifier.date_to_mohid_date(cfg.current_final_date))
            file.write('\n')

            if stage == "Running":
                file.write('STATUS                        : RUNNING')
            elif stage == "Finished":
                file.write('STATUS                        : FINISHED')

            file.write('\n')
            file.write('SYSTEM TIME                   : ' + system_time)
            file.close()
#----------------------------------------------------------------------------------------------------------------

'''
Back ups all the results located in the res/ folder of the project. It ignores all the results before consolidation 
(those that start with "MPI_"). Copies all the consolidated .hdf5 files to the Results_HDF/ folder in the backup path
that the user defined. And the same goes for the Restart, TimeSeries and Discharges files.
'''
def backup_simulation(yaml):
    date_format = "%Y-%m-%d"
    if 'DATE_FORMAT' in yaml['MOHID'].keys():
        date_format = yaml['MOHID']['DATE_FORMAT']

    initial_date = cfg.current_initial_date.strftime(date_format)
    tmp_date = cfg.current_initial_date + datetime.timedelta(yaml['ARTCONFIG']['DAYS_PER_RUN'])
    final_date = tmp_date.strftime(date_format)

    static.logger.info("Simulation Results Initial Date: " + initial_date)
    static.logger.info("Simulation Results Final Date: " + final_date)

    for model in yaml.keys():
        if model != "MOHID" and model != "ARTCONFIG" and model != "POSTPROCESSING"\
            and model != "PREPROCESSING" and model != "TRIGGER":

            model_keys = yaml[model].keys()
            mohid_keys = yaml['MOHID']
            results_path = yaml['ARTCONFIG']['MAIN_PATH'] + yaml[model]['PATH'] + "res/"

            generic_path = yaml[model]['STORAGE_PATH']
            date_path = initial_date + "_" + final_date + "/"
            restart_storage = generic_path + "Restart/" + date_path
            results_storage = generic_path + "Results_HDF/" + date_path
            time_series_storage = generic_path + "Results_TimeSeries/" + date_path
            discharges_storage = generic_path + "Discharges/" + date_path

            if 'HAS_SOLUTION_FROM_FILE' not in model_keys or not yaml[model]['HAS_SOLUTION_FROM_FILE']:
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
                if 'RESULTS_LIST' in model_keys:
                    for file in hdf5_files:
                        if os.path.split(file)[1].startswith("MPI"):
                            continue
                        file_name = os.path.split(file)[1]
                        name_array = file_name.split("_")
                        if len(name_array) > 2:
                            #Hydrodynamic_1_Surface becomes Hydrodynamic_Surface
                            file_name_copy = name_array[0] + "_" + name_array[2]
                        else:
                            file_type = name_array[-1].split(".")[1]
                            file_name_copy = name_array[0] + "." + file_type

                        #if the file_name is not in the RESULTS_LIST it will be ignored
                        if file_name not in yaml[model]['RESULTS_LIST']:
                            continue


                        file_destination = results_storage + file_name_copy
                        static.logger.info("Backup Simulation HDF Files: Copying " + file + " to " + file_destination)
                        copy(file, file_destination)
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
Main cycle for the ART run. It has all the functions that are needed for a project.
'''
def process_models(yaml, days_run):
    check_triggers(yaml['TRIGGER'], days_run, yaml['ARTCONFIG']['DAYS_PER_RUN'])
    for model in yaml.keys():
        if model != "ARTCONFIG" and model != "POSTPROCESSING" and model != "PREPROCESSING" and model != "MOHID" and model != "TRIGGER":
            #if 'METEO' in yaml[model].keys():
            create_folder_structure(yaml, yaml[model])
            change_model_dat(yaml, yaml[model])
            gather_boundary_conditions(yaml, yaml[model])
            gather_restart_files(yaml, yaml[model])

#              create_folder_structure(yaml, yaml[model])
#              gather_boundary_conditions(yaml, yaml[model])
#              change_model_dat(yaml, yaml[model])
#              gather_restart_files(yaml, yaml[model])

            if 'METEO' in yaml[model].keys():
                for meteo_model in yaml[model]['METEO']['MODELS'].keys():
                    if 'ENABLE' in yaml[model]['METEO']['MODELS'][meteo_model].keys()\
                    and yaml[model]['METEO'][meteo_model]['MODELS']['ENABLE']:
                        get_meteo_file(yaml, yaml[model]['METEO']['MODELS'][meteo_model])

            if 'DISCHARGES' in yaml[model].keys():
                for discharge in yaml[model]['DISCHARGES'].keys():
                    if 'ENABLE' in yaml[model]['DISCHARGES'][discharge].keys()\
                    and yaml[model]['DISCHARGES'][discharge]['ENABLE']:
                        gather_discharges_files(yaml, yaml[model])

    write_trigger(yaml['TRIGGER'], yaml['ARTCONFIG']['MAIN_PATH'], yaml['ARTCONFIG']['DAYS_PER_RUN'], stage = "Running")
    run_mohid(yaml)
    backup_simulation(yaml)
    write_trigger(yaml['TRIGGER'], yaml['ARTCONFIG']['MAIN_PATH'], yaml['ARTCONFIG']['DAYS_PER_RUN'], stage = "Finished")

def execute(yaml):
    artconfig_keys = yaml['ARTCONFIG'].keys()
    static.logger.info("Run MOHID enabled")
    #operational mode is used relative to the current day of the machine
    if yaml['ARTCONFIG']['OPERATIONAL_MODE']:
        days_run = 0
        today = datetime.datetime.today()
        #Time needs to start on hour 00:00:00 otherwise will start the models at the wrong time
        today = today.replace(minute=00, hour=00, second=00)
        cfg.global_initial_date = today + datetime.timedelta(days=yaml['ARTCONFIG']['REF_DAYS_TO_START'])
        for i in range(1, cfg.number_of_runs + 1):
            cfg.current_initial_date = cfg.global_initial_date + datetime.timedelta(days=i - 1)
            cfg.current_final_date = cfg.current_initial_date + datetime.timedelta(days=yaml['ARTCONFIG']['DAYS_PER_RUN'])
            static.logger.info("========================================")
            static.logger.info("STARTING FORECAST ( " + str(i) + " of " + str(cfg.number_of_runs) + " )")
            static.logger.info("========================================")
            if 'RUN_PREPROCESSING' in artconfig_keys and yaml['ARTCONFIG']['RUN_PREPROCESSING']:
                static.logger.info("Executing Pre Processing")
                pre_processing.execute(yaml)
            if yaml['ARTCONFIG']['RUN_SIMULATION']:
                process_models(yaml,days_run)
            if 'RUN_POSTPROCESSING' in artconfig_keys and yaml['ARTCONFIG']['RUN_POSTPROCESSING']:
                static.logger.info("Executing Post Processing")
                post_processing.execute(yaml)
    else:
        if 'MONTH_MODE' in artconfig_keys and yaml['ARTCONFIG']['MONTH_MODE']:
            static.logger.info("Month mode activated. Time skips will be of 1 month each.")
            cfg.current_initial_date = cfg.global_initial_date.replace(minute=00, hour=00, second=00)
            if cfg.current_initial_date.month == 12:
                cfg.current_final_date = cfg.global_initial_date.replace(day=1,month=1,year=cfg.global_initial_date.year+1, minute=00, hour=00, second=00)
            else:
                cfg.current_final_date = cfg.global_initial_date.replace(day=1,month=cfg.global_initial_date.month + 1, minute=00, hour=00, second=00)
        else:
            cfg.current_initial_date = cfg.global_initial_date.replace(minute=00, hour=00, second=00)
            cfg.current_final_date = cfg.global_initial_date + datetime.timedelta(days=yaml['ARTCONFIG']['DAYS_PER_RUN'])
            days_run = 0
        while cfg.current_final_date <= cfg.global_final_date.replace(minute=00, hour=00, second=00):
            static.logger.info("========================================")
            static.logger.info("STARTING FORECAST (" + cfg.current_initial_date.strftime("%Y-%m-%d") + " to " +
                               cfg.current_final_date.strftime("%Y-%m-%d") + ")")
            static.logger.info("========================================")
            if 'RUN_PREPROCESSING' in artconfig_keys and yaml['ARTCONFIG']['RUN_PREPROCESSING']:
                static.logger.info("Executing Pre Processing")
                pre_processing.execute(yaml)
            if yaml['ARTCONFIG']['RUN_SIMULATION']:
                process_models(yaml, days_run)
            if 'RUN_POSTPROCESSING' in artconfig_keys and yaml['ARTCONFIG']['RUN_POSTPROCESSING']:
                post_processing.execute(yaml)
                static.logger.info("Executing Post Processing")
            if 'RUN_TWICE' in yaml['ARTCONFIG'].keys() and yaml['ARTCONFIG']['RUN_TWICE'] == True :
                #Only run next day after repeating current day. Usefull for upscaling
                days_run += 1
                if days_run == 1:
                    cfg.current_initial_date = cfg.current_initial_date + datetime.timedelta(
                        days=yaml['ARTCONFIG']['DAYS_PER_RUN'])
                    cfg.current_final_date = cfg.current_final_date + datetime.timedelta(days=yaml['ARTCONFIG']['DAYS_PER_RUN'])
                elif days_run == 2:
                    days_run = 0
            if (yaml['ARTCONFIG']['MONTH_MODE']):
                cfg.current_initial_date = cfg.current_final_date
                if cfg.current_initial_date.month == 12:
                    cfg.current_final_date = cfg.current_initial_date.replace(day=1,month=1,year=cfg.current_initial_date.year+1, minute=00, hour=00, second=00)
                else:
                    cfg.current_final_date = cfg.current_initial_date.replace(day=1,month=cfg.current_initial_date.month + 1, minute=00, hour=00, second=00)
            else:
                cfg.current_initial_date = cfg.current_initial_date + datetime.timedelta(
                    days=yaml['ARTCONFIG']['DAYS_PER_RUN'])
                cfg.current_final_date = cfg.current_final_date + datetime.timedelta(days=yaml['ARTCONFIG']['DAYS_PER_RUN'])

    return None
