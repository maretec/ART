from pathlib import Path
from shutil import copy
from common import logger
import mohid.util.constants as static
import mohid.util.file_modifier as file_modifier
import datetime
import glob
import os.path
import common.pre_processing as pre_processing
import common.post_processing as post_processing
import mohid.util.folder_utils as folder_utils
import mohid.util.mohid_utils as mohid_utils
import subprocess
import time
import multiprocessing
import threading


class MohidWater:
    def __init__(self, art):
        self.logger = art.logger
        self.yaml = art.yaml
        self.global_initial_date = None
        self.global_final_date = None
        self.number_of_runs = None
        self.current_initial_date = None
        self.current_final_date = None

    def execute(self):
        self.running_mode()
        artconfig_keys = self.yaml['ART'].keys()
        simulation_keys = self.yaml['SIMULATION'].keys()
        days_run = 0
        if 'OPERATIONAL_MODE' in self.yaml['SIMULATION'].keys() and self.yaml['SIMULATION']['OPERATIONAL_MODE']:
            self.logger.info("Running Mohid Water in Operational Mode")
            today = datetime.datetime.today()
            # Time needs to start on hour 00:00:00 otherwise will start the models at the wrong time
            today = today.replace(minute=00, hour=00, second=00)
            self.global_initial_date = today + datetime.timedelta(days=self.yaml['SIMULATION']['REF_DAYS_TO_START'])

            for i in range(1, self.number_of_runs + 1):
                self.current_initial_date = self.global_initial_date + datetime.timedelta(days=i - 1)
                self.current_final_date = self.current_initial_date + datetime.timedelta(
                    days=self.yaml['SIMULATION']['DAYS_PER_RUN'])

                self.logger.info("========================================")
                self.logger.info("STARTING FORECAST ( " + str(i) + " of " + str(self.number_of_runs) + " )")
                self.logger.info("========================================")

                if 'PRE_PROCESSING' in artconfig_keys and self.yaml['ART']['PRE_PROCESSING']:
                    self.logger.info("Executing Pre Processing")
                    pre_processing.execute(self.yaml, logger)
                if 'RUN_SIMULATION' in artconfig_keys and self.yaml['ART']['RUN_SIMULATION']:
                    self.process_models(days_run)
                if 'POST_PROCESSING' in artconfig_keys and self.yaml['ART']['POST_PROCESSING']:
                    self.logger.info("Executing Post Processing")
                    thread = threading.Thread(target=post_processing.execute, args=(self,))
                    thread.start()
        else:
            if 'MONTH_MODE' in simulation_keys and self.yaml['SIMULATION']['MONTH_MODE']:
                self.logger.info("Month mode activated. Time skips will be of 1 month each.")
                self.current_initial_date = self.global_initial_date.replace(minute=00, hour=00, second=00)

                if self.current_initial_date.month == 12:
                    self.current_final_date = self.global_initial_date.replace(day=1, month=1,
                                                                               year=self.global_initial_date.year + 1,
                                                                               minute=00, hour=00, second=00)
                else:
                    self.current_final_date = self.global_initial_date.replace(day=1,
                                                                               month=self.global_initial_date.month + 1,
                                                                               minute=00, hour=00, second=00)
            else:
                self.current_initial_date = self.global_initial_date.replace(minute=00, hour=00, second=00)
                self.current_final_date = self.global_initial_date + datetime.timedelta(
                    days=self.yaml['SIMULATION']['DAYS_PER_RUN'])
            if(self.current_final_date <= self.global_final_date.replace(minute=00, hour=00, second=00)):

                while self.current_final_date <= self.global_final_date.replace(minute=00, hour=00, second=00):
                    self.logger.info("========================================")
                    self.logger.info("STARTING FORECAST (" + self.current_initial_date.strftime("%Y-%m-%d") + " to " +
                                    self.current_final_date.strftime("%Y-%m-%d") + ")")
                    self.logger.info("========================================")
                    if 'RUN_PREPROCESSING' in artconfig_keys and self.yaml['ART']['RUN_PREPROCESSING']:
                        self.logger.info("Executing Pre Processing")
                        pre_processing.execute(self.yaml)
                    if self.yaml['ART']['RUN_SIMULATION']:
                        self.process_models(days_run)
                    if 'RUN_POSTPROCESSING' in artconfig_keys and self.yaml['ART']['RUN_POSTPROCESSING']:
                        post_processing.execute(self.yaml)
                        self.logger.info("Executing Post Processing")
                    if 'RUN_TWICE' in self.yaml['ART'].keys() and self.yaml['ART']['RUN_TWICE']:
                        # Only run next day after repeating current day. Useful for up-scaling
                        days_run += 1
                        if days_run == 1:
                            self.current_initial_date = self.current_initial_date + datetime.timedelta(
                                days=self.yaml['SIMULATION']['DAYS_PER_RUN'])
                            self.current_final_date = self.current_final_date + datetime.timedelta(
                                days=self.yaml['SIMULATION']['DAYS_PER_RUN'])
                        elif days_run == 2:
                            days_run = 0
                    if self.yaml['SIMULATION']['MONTH_MODE']:
                        self.current_initial_date = self.current_final_date
                        if self.current_initial_date.month == 12:
                            self.current_final_date = self.current_initial_date.replace(day=1, month=1,
                                                                                        year=self.current_initial_date.year + 1,
                                                                                        minute=00, hour=00, second=00)
                        else:
                            self.current_final_date = self.current_initial_date.replace(day=1,
                                                                                        month=self.current_initial_date.month + 1,
                                                                                        minute=00, hour=00, second=00)
                    else:
                        self.current_initial_date = self.current_initial_date + datetime.timedelta(
                            days=self.yaml['SIMULATION']['DAYS_PER_RUN'])
                        self.current_final_date = self.current_final_date + datetime.timedelta(
                            days=self.yaml['SIMULATION']['DAYS_PER_RUN'])
            else:
                self.logger.error("Time Date range is not big enough for a month run.")
            return None

    '''
    Main cycle for the ART run. It has all the functions that are needed for a project.
    '''

    def process_models(self, days_run: int) :
        main_path = Path(self.yaml['MOHID_WATER']['MAIN_PATH'])
        days_per_run = self.yaml['SIMULATION']['DAYS_PER_RUN']
        self.check_triggers(days_run, self.yaml['SIMULATION']['DAYS_PER_RUN'])
        mohid_water_config = self.yaml['MOHID_WATER']
        mohid_water_models = mohid_water_config['MODELS']
        for model in mohid_water_models.keys():
            folder_utils.create_model_folder_structure(self.yaml, mohid_water_models[model])
            self.change_model_dat(mohid_water_models[model], main_path)
            self.gather_boundary_conditions(mohid_water_models[model], main_path)
            self.gather_restart_files(mohid_water_models[model], main_path)

            #TODO fix meteo
            if 'METEO' in mohid_water_models[model].keys():
                for meteo_model in mohid_water_models[model]['METEO']['MODELS'].keys():
                    if 'ENABLE' in mohid_water_models[model]['METEO']['MODELS'][meteo_model].keys() \
                            and mohid_water_models[model]['METEO'][meteo_model]['MODELS']['ENABLE']:
                        self.get_meteo_file(mohid_water_models[model]['METEO']['MODELS'][meteo_model])

            if 'DISCHARGES' in mohid_water_models[model].keys():
                for discharge in mohid_water_models[model]['DISCHARGES'].keys():
                    if 'ENABLE' in mohid_water_models[model]['DISCHARGES'][discharge].keys() \
                            and mohid_water_models[model]['DISCHARGES'][discharge]['ENABLE']:
                        self.gather_discharges_files(mohid_water_models[model])

        self.write_trigger(self.yaml['MOHID_WATER']['MAIN_PATH'],
                          days_per_run, stage="Running")
        self.run_mohid()
        self.backup_simulation()
        self.write_trigger(self.yaml['MOHID_WATER']['MAIN_PATH'],
                           days_per_run, stage="Finished")

    def running_mode(self):
        if 'SIMULATION' not in self.yaml:
            raise ValueError("SIMULATION key not defined in yaml configuration file.")
        simulation_keys = self.yaml['SIMULATION'].keys()
        if 'OPERATIONAL_MODE' in simulation_keys and self.yaml['SIMULATION']['OPERATIONAL_MODE']:
            self.logger.info("Running in Operational Mode")
            today = datetime.datetime.today()
            self.global_initial_date = today + datetime.timedelta(days=self.yaml['SIMULATION']['REF_DAYS_TO_START'])
            self.global_final_date = (today + datetime.timedelta(days=self.yaml['SIMULATION']['NUMBER_OF_RUNS'])
                                      + datetime.timedelta(days=self.yaml['SIMULATION']['DAYS_PER_RUN'] - 1))
            self.number_of_runs = self.yaml['SIMULATION']['NUMBER_OF_RUNS']
            initial_date = self.global_initial_date
            final_date = initial_date + datetime.timedelta(days=self.yaml['SIMULATION']['DAYS_PER_RUN'])
            self.logger.info("Initial Date : " + initial_date.strftime(static.DATE_FORMAT))
            self.logger.info("Final Date: " + final_date.strftime(static.DATE_FORMAT))
            self.logger.info("Number of runs : " + str(self.number_of_runs))
        elif 'OPERATIONAL_MODE' in simulation_keys:
            try:
                self.logger.info("Running in Normal Mode")
                self.global_initial_date = datetime.datetime.strptime(self.yaml['SIMULATION']['START_DATE'],
                                                                      static.DATE_FORMAT)
                self.global_final_date = datetime.datetime.strptime(self.yaml['SIMULATION']['END_DATE'],
                                                                    static.DATE_FORMAT)

                difference = self.global_final_date - self.global_initial_date
                self.number_of_runs = difference.days
            except KeyError:
                self.logger.warning("KeyError")
                self.number_of_runs = 1
                global_initial_date = datetime.datetime.today()
                global_final_date = global_initial_date + datetime.timedelta(
                    days=self.yaml['SIMULATION']['DAYS_PER_RUN'])
                self.global_initial_date = datetime.datetime.strftime(datetime.datetime.today(), static.DATE_FORMAT)
                self.global_final_date = datetime.datetime.strftime(global_final_date, static.DATE_FORMAT)
            finally:
                self.logger.info("Global Initial Date : " + self.global_initial_date.strftime(static.DATE_FORMAT))
                self.logger.info("Global Final Date : " + self.global_final_date.strftime(static.DATE_FORMAT))
                self.logger.info("Number of runs : " + str(self.number_of_runs))
        else:
            raise ValueError("OPERATIONAL_MODE keyword must be defined in yaml file.")

    def run_mohid(self):
        output_file_name = Path(self.yaml['MOHID_WATER']['TREE_PATH'] + "MOHID_RUN_" + self.current_initial_date.strftime("%Y-%m-%d") + ".log")
        output_file = open(output_file_name, "w+")
        exe_path = Path(self.yaml['MOHID_WATER']['EXE_PATH'])
        tree_path = Path(self.yaml['MOHID_WATER']['TREE_PATH'])

        if 'MPI' in self.yaml['MOHID_WATER'].keys() and self.yaml['MOHID_WATER']['MPI']['ENABLE']:
            self.logger.info("Starting MOHID MPI")
            # cwd is the working directory where the command will execute. stdout is the output file of the command
            if 'EXE_PATH' in self.yaml['MOHID_WATER']['MPI']:
                mpi_exe_path = Path(self.yaml['MOHID_WATER']['MPI']['EXE_PATH'])
            else:
                mpi_exe_path = "mpiexec"
                self.logger.info(
                    "Executable information for MPI missing. Defaulting to main EXE: " + exe_path.__str__())
            # subprocess.run([mpi_exe_path.__str__(), "-np", str(self.yaml['MOHID_WATER']['MPI']['TOTAL_PROCESSORS']),
                            # str(exe_path), "&"], cwd=os.path.dirname(self.yaml['MOHID_WATER']['EXE_PATH']),
                           # stdout=output_file)
            subprocess.run([mpi_exe_path.__str__(), "-np", str(self.yaml['MOHID_WATER']['MPI']['TOTAL_PROCESSORS']),
                            str(exe_path), "&"], cwd=os.path.dirname(self.yaml['MOHID_WATER']['TREE_PATH']),
                           stdout=output_file)
            output_file.close()

            # Mohid always writes these strings in the last lines of the logs. We use it to verify that run was
            # successful
            if not mohid_utils.verify_run(output_file_name, ['Program Mohid Water successfully terminated',
                                                             'Program Mohid Land successfully terminated']):
                self.logger.info("MOHID RUN NOT SUCCESSFUL")
                raise ValueError("MOHID RUN NOT SUCCESSFUL")
            else:
                self.logger.info("MOHID RUN successful")

            # DDC is ran when an MPI run is done to join all the results into a single one.
            ddc_output_filename = "DDC_" + self.current_initial_date.strftime("%Y-%m-%d") + ".log"
            mohid_ddc_output_log = open(ddc_output_filename, "w+")
            # subprocess.run(["MohidDDC.exe", str(exe_path), "&"], cwd=os.path.dirname(self.yaml['MOHID_WATER']['EXE_PATH']),
                           # stdout=mohid_ddc_output_log)
            subprocess.run(["MohidDDC.exe", str(exe_path), "&"], cwd=os.path.dirname(self.yaml['MOHID_WATER']['TREE_PATH']),
                           stdout=mohid_ddc_output_log)
            mohid_ddc_output_log.close()
            if not mohid_utils.verify_run(ddc_output_filename, ["Program MohidDDC successfully terminated"]):
                self.logger.info("MohidDDC NOT SUCCESSFUL")
                raise ValueError("MohidDDC NOT SUCCESSFUL")
            else:
                self.logger.info("MohidDDC successful")
        else:
            self.logger.info("Starting MOHID run")
            # cwd is the working directory where the command will execute. stdout is the output file of the command
            # subprocess.run([str(exe_path), "&"], cwd=os.path.dirname(self.yaml['MOHID_WATER']['EXE_PATH']),
                           # stdout=output_file)
            subprocess.run([str(exe_path), "&"], cwd=os.path.dirname(self.yaml['MOHID_WATER']['TREE_PATH']),
                           stdout=output_file)
            output_file.close()

            if not mohid_utils.verify_run(output_file_name, ['Program Mohid Water successfully terminated',
                                                             'Program Mohid Land successfully terminated']):
                self.logger.info("MOHID RUN NOT SUCCESSFUL")
                raise ValueError("MOHID RUN NOT SUCCESSFUL")
            else:
                self.logger.info("MOHID RUN successful")

    '''
    MOHID needs the file model.dat to be changed, especially START and END times.
    This function changes that file in each iteration to update START and END and other parameters that can be defined
    in the yaml config file.
    It receives the yaml object and the 'model' dictionary which is in 'mohidwater' dictionary.
    '''

    def change_model_dat(self, model, main_path: Path):
        self.logger.info("Creating new model file for model: " + model['NAME'])
        keys = model.keys()
        path = main_path / model['PATH'] / "data/"
        path = path.expanduser()
        if not os.path.isdir(path):
            self.logger.info("Path for model folder does not exist.")
            self.logger.info("Check path parameters in the yaml file. Exiting ART.")
            raise ValueError("Path for model folder does not exist.")

        file_path = Path(path, "Model_1.dat")
        
        if not file_path.is_file():
            raise ValueError("File " + str(file_path) + " does not exist.")
        
        file_modifier.modify_start_dat_date(file_path, file_modifier.date_to_mohid_date(self.current_initial_date), self.logger)
        self.logger.info("Changed START of " + str(file_path) + " to " +
                         file_modifier.date_to_mohid_date(self.current_initial_date))
        file_modifier.modify_end_dat_date(file_path, file_modifier.date_to_mohid_date(self.current_final_date), self.logger)
        self.logger.info("Changed END of " + str(file_path) + " to " +
                         file_modifier.date_to_mohid_date(self.current_final_date))
        file_modifier.modify_line(file_path, "DT", str(model['DT']), self.logger)
        if 'OPENMP' in self.yaml['MOHID_WATER'].keys() and self.yaml['MOHID_WATER']['OPENMP']['ENABLE']:
            if 'TOTAL_PROCESSORS' in self.yaml['MOHID_WATER']['OPENMP']:
                num_omp_processors = self.yaml['MOHID_WATER']['OPENMP']['TOTAL_PROCESSORS']
            else:
                self.logger.info("NUM_PROCESSORS not defined. model will use max threads available")
                num_omp_processors = multiprocessing.cpu_count()
            file_modifier.modify_line(file_path, "OPENMP_NUM_THREADS", str(num_omp_processors), self.logger)
        if 'mohidwater.dat' in keys:
            for key in model['mohidwater.dat'].keys():
                file_modifier.modify_line(file_path, key, model['mohidwater.dat'][key], self.logger)
        self.logger.info("Model " + model['NAME'] + " .dat file was created.")
        return

    def gather_boundary_conditions(self, model: dict, main_path: Path):
        """
        Gathers boundary conditions for each model in the model block if the 'obc' dictionary has the parameter 'enable'
        and if it is a different value from 0. The user can define the file type and the date format. It copies the
        files the user defined in the list 'files' in the yaml file.
        """
        model_keys = model.keys()
        if 'OBC' in model_keys:
            for obc_model in model['OBC']:
                if 'ENABLE' in model['OBC'][obc_model].keys() and model['OBC'][obc_model]['ENABLE']:
                    self.logger.info("OBC flag enabled")
                    self.logger.info("Gathering Boundary Condition for " + model['NAME'])
                    obc_keys = model['OBC'][obc_model].keys()

                    simulations_available = self.yaml['SIMULATION']['DAYS_PER_RUN'] - model['OBC'][obc_model][
                        'SIMULATED_DAYS']
                    folder_label = "GeneralData/BoundaryConditions/Hydrodynamics/"

                    date_format = "%Y-%m-%d"
                    if 'DATE_FORMAT' in obc_keys:
                        date_format = model['OBC'][obc_model]['DATE_FORMAT']

                    file_type = "hdf5"
                    if 'FILE_TYPE' in obc_keys:
                        file_type = model['OBC'][obc_model]['FILE_TYPE']
                    if 'NAME' in obc_keys:
                        obc_folder = model['OBC'][obc_model]['NAME']
                        user_dest_filename = model['OBC'][obc_model]['NAME']
                    else:
                        raise ValueError("NAME Keyword in OBC level must be defined.")
                    self.logger.info("Boundary Conditions File Type: " + file_type)

                    for n in range(0, simulations_available - 1, -1):
                        obc_initial_date = self.current_initial_date + datetime.timedelta(days=n)
                        obc_final_date = self.current_final_date + datetime.timedelta(days=n)

                        obc_initial_date_str = obc_initial_date.strftime(date_format)
                        obc_final_date_str = obc_final_date.strftime(date_format)

                        if 'WORK_PATH' in model['OBC'][obc_model].keys():
                            work_path = Path(model['OBC'][obc_model]['WORK_PATH'])
                        else:
                            self.logger.error("WORK_PATH NOT DEFINED INSIDE THE OBC MODEL: " + obc_model)
                            raise ValueError("WORK_PATH keyword must be defined inside OBC model: " + obc_model)
                        '''
                        if 'HAS_SOLUTION_FROM_FILE' it needs to get the OBC files from a "parent" model, and needs to follow the structure
                        we use to backup our results.
                        '''
                        if 'HAS_SOLUTION_FROM_FILE' in model_keys and model['HAS_SOLUTION_FROM_FILE']:
                            obc_initial_date = self.current_initial_date + datetime.timedelta(days=n)
                            obc_final_date = self.current_final_date + datetime.timedelta(days=simulations_available)

                            obc_initial_date_str = obc_initial_date.strftime(date_format)
                            obc_final_date_str = obc_final_date.strftime(date_format)

                            self.logger.info("OBC Initial Date: " + obc_initial_date_str)
                            self.logger.info("OBC Final Date: " + obc_final_date_str)

                            obc_string = obc_initial_date_str + "_" + obc_final_date_str + "/"
                            folder_source = work_path / obc_string

                            for obc_file in model['OBC'][obc_model]['FILES']:
                                obc_files_string = obc_file + "." + file_type
                                file_source = folder_source / obc_files_string

                                if os.path.isfile(file_source):
                                    dest_folder = main_path / folder_label / obc_folder / "/"
                                    if not os.path.isdir(dest_folder):
                                        os.makedirs(dest_folder)
                                    else:
                                        file_string = obc_file + "." + file_type
                                        file_destination = dest_folder / file_string
                                        copy(file_source, file_destination)
                                        self.logger.info("Copying OBC from " + file_source + " to " + file_destination)

                        else:
                            '''
                            SUB_FOLDERS within the WORKPATH for the OBC files. They can be subdivided with year, month and year.
                            '''
                            if 'SUBFOLDERS' in obc_keys:
                                if model['OBC'][obc_model]['SUBFOLDERS'] == 1:
                                    path_string = str(obc_initial_date.year) + "/"
                                elif model['OBC'][obc_model]['SUBFOLDERS'] == 2:
                                    path_string = str(obc_initial_date.year) + "/" + str(obc_initial_date.month)
                                elif model['OBC'][obc_model]['SUBFOLDERS'] == 3:
                                    path_string = str(obc_initial_date.year) + "/" + str(obc_initial_date.month) + "/" + \
                                                  str(obc_initial_date.days) + "/"
                                elif model['OBC'][obc_model]['SUBFOLDERS'] == 4:
                                    path_string = obc_initial_date_str + "_" + obc_final_date_str + "/"
                                else:
                                    raise ValueError("SUBFOLDER keyword must be within the defined bonds (1-4)")
                                work_path = work_path / path_string

                                for file in model['OBC'][obc_model]['FILES']:
                                    if model['OBC'][obc_model]['SUBFOLDERS'] == 4:
                                        file_string = file + "." + file_type
                                        file_source = work_path / file_string
                                        filename = file
                                    else:
                                        filename = mohid_utils.create_file_name_with_date(file, obc_initial_date,
                                                                                          obc_final_date)
                                        file_string = filename + "." + file_type
                                        file_source = work_path / file_string

                                    if model['OBC'][obc_model]['SUBFOLDERS'] == 0:
                                        filename = user_dest_filename

                                    if os.path.isfile(file_source):
                                        dest_folder_extra_string = folder_label + obc_folder + "/"
                                        dest_folder = main_path / dest_folder_extra_string

                                        if not os.path.isdir(dest_folder):
                                            os.makedirs(dest_folder)
                                        else:
                                            file_destination_extra = filename + "." + file_type
                                            file_destination = dest_folder / file_destination_extra
                                            copy(file_source, file_destination)
                                            self.logger.info(
                                                "Copying OBC from " + str(file_source) + " to " + str(file_destination))
                                    else:
                                        self.logger.info("File " + str(file_source) + " does not exist ")

    def get_meteo_file(self, model: dict):
        model_keys = model.keys()
        if 'METEO' in model_keys and model['METEO']['ENABLE']:
            self.logger.info("Gathering Meteo Files")

            meteo_models_keys = model['METEO']['MODELS'].keys()

            for meteo_model in meteo_models_keys:
                meteo_keys = model['METEO']['MODELS'][meteo_model].keys()

                date_format = "%Y-%m-%d"
                if 'DATE_FORMAT' in meteo_keys:
                    date_format = model['METEO'][meteo_model]['DATE_FORMAT']

                meteo_initial_date: str = self.current_initial_date.strftime(date_format)
                if 'SIMULATED_DAYS' in meteo_keys:
                    meteo_final_date = self.current_initial_date + datetime.timedelta(days=model['METEO']['MODELS']
                    [meteo_model]['SIMULATED_DAYS'])
                    meteo_final_date = meteo_final_date.strftime(date_format)
                else:
                    meteo_final_date = self.current_final_date.strftime(date_format)

                self.logger.info("Meteo Initial Date: " + meteo_initial_date)
                self.logger.info("Meteo Final Date: " + meteo_final_date)

                file_type = "hdf5"
                if 'FILE_TYPE' in meteo_keys:
                    file_type = model['METEO']['MODELS'][meteo_model]['FILE_TYPE']

                if 'FILENAME_FROM_MODEL' in meteo_keys and model['METEO']['MODELS'][meteo_model]['FILENAME_FROM_MODEL']:
                    self.logger.info("Meteo: fileNameFromModel flag enabled")

                    meteo_sufix = model['METEO']['MODELS'][meteo_model]['NAME']
                    self.logger.info("Meteo sufix: " + meteo_sufix)
                    meteo_work_path = Path(model['METEO']['MODELS'][meteo_model]['WORKPATH'])
                    meteo_date_string = model['METEO']['MODELS'][meteo_model]['NAME'] + "_" + model['NAME'] + "_" + \
                                        meteo_initial_date + "_" + meteo_final_date + "." + file_type
                    meteo_file_source = meteo_work_path / meteo_date_string
                    self.logger.info("Meteo Source File: " + meteo_file_source)
                else:
                    meteo_work_path = Path(model['METEO']['MODELS'][meteo_model]['WORKPATH'])
                    meteo_date_string = "meteo" + "_" + meteo_initial_date + "_" + meteo_final_date + "." + file_type

                    meteo_file_source = meteo_work_path / meteo_date_string
                    self.logger.info("Meteo Source File: " + meteo_file_source)

                if os.path.isfile(meteo_file_source):
                    main_path = Path(self.yaml['MOHID_WATER']['MAIN_PATH'])
                    model_path_string = "GeneralData/BoundaryConditions/Atmosphere/" + model['NAME'] + "/" + \
                                        model['METEO']['MODELS'][meteo_model]['NAME'] + "/"
                    meteo_file_dest_folder = main_path / model_path_string

                    if not os.path.isdir(meteo_file_dest_folder):
                        os.makedirs(meteo_file_dest_folder)

                    model_string = model['METEO']['MODELS'][meteo_model]['NAME'] + "_" + model['NAME'] + "." + file_type
                    meteo_file_dest = meteo_file_dest_folder / model_string
                    self.logger.info("Meteo Destination File: " + meteo_file_dest)

                    copy(meteo_file_source, meteo_file_dest)
                    self.logger.info("Copied meteo file from " + meteo_file_source + " to " + meteo_file_dest)
                    return
                else:
                    continue

    def gather_restart_files(self, model: dict, main_path:Path):
        """
        Gets restart files from previous run. These files need to be put in /res folder of the project you're trying to
        run.
        """
        self.logger.info("Gathering the restart files for model: " + model['NAME'])
        
        date_format = "%Y-%m-%d"
        if 'dateFormat' in self.yaml['MOHID_WATER'].keys():
            date_format = self.yaml['MOHID_WATER']['DATE_FORMAT']

        previous_init_date = self.current_initial_date - datetime.timedelta(days=1)
        previous_final_date = previous_init_date + datetime.timedelta(days=self.yaml['SIMULATION']['DAYS_PER_RUN'])
        self.logger.info("Restart Files Initial Day: " + previous_init_date.strftime(date_format))
        self.logger.info("Restart Files Final Day: " + previous_final_date.strftime(date_format))

        base_fin_path = Path(model['STORAGE_PATH'])
        date_fin_path = "Restart/" + previous_init_date.strftime(date_format) + "_" + \
                        previous_final_date.strftime(date_format) + "/"
        path_fin_files = base_fin_path / date_fin_path

        self.logger.info("Source Restart Files: " + path_fin_files.__str__())

        if not os.path.isdir(path_fin_files):
            self.logger.info("Restart folder " + path_fin_files.__str__() + "does not exist.")
            return

        restart_model_path = model['PATH'] + "res/"
        restart_files_dest = main_path / restart_model_path
        if not os.path.isdir(restart_files_dest):
            os.makedirs(restart_files_dest)

        # glob creates a list with all files that match the regex expression
        fin_files = glob.glob(path_fin_files.__str__() + r"/*.fin")
        fin5_files = glob.glob(path_fin_files.__str__() + r"/*.fin5")
        for file in fin_files:
            # the nomfich.dat file for mohidwater is not changed and when a restart file is generated it ends with _1.fin
            # and because of that an input restart file needs to finish with _0.fin. So we simply change it when we copy it.
            file_destination_partial = os.path.split(file)[1].split("_")[0] + "_0.fin"
            file_destination = restart_files_dest / file_destination_partial
            self.logger.info("Restart Files: Copying " + str(file) + " to " + str(file_destination))
            copy(file, file_destination)
        for file in fin5_files:
            file_destination_partial = os.path.split(file)[1].split("_")[0] + "_0.fin5"
            file_destination = restart_files_dest / file_destination_partial
            self.logger.info("Restart Files: Copying " + str(file) + " to " + str(file_destination))
            copy(file, file_destination)

    def gather_discharges_files(self, model):
        self.logger.info("Gathering Discharges Files for model " + model['NAME'])
        main_path = Path(self.yaml['artconfig']['mainPath'])

        for discharge in model['DISCHARGES']:
            self.logger.info("Gathering Discharge Files for discharge block" + str(discharge))
            date_format = "%Y-%m-%d"
            if 'dateFormat' in model['DISCHARGES'][discharge].keys():
                date_format = model['DISCHARGES'][discharge]['DATE_FORMAT']

            discharge_base_path = Path(model['DISCHARGES'][discharge]['PATH'])
            path_discharges_files_partial = self.current_initial_date.strftime(date_format) + "_" + \
                                            self.current_final_date.strftime(date_format) + "/"
            path_discharges_files = discharge_base_path / path_discharges_files_partial

            self.logger.info("Source Discharges Files " + str(path_discharges_files))

            file_destination_path_end = "GeneralData/BoundaryConditions/Discharges/" + model['NAME'] + "/"
            file_destination = main_path / file_destination_path_end

            self.logger.info("Discharges Files Destination " + str(file_destination))

            files = glob.glob(path_discharges_files + "*.*")

            if not os.path.isdir(file_destination):
                os.makedirs(file_destination)

            for file in files:
                file_destination_string = os.path.split(file)[1]
                file_destination = file_destination / file_destination_string
                self.logger.info("Discharges: Copying " + str(file) + " to " + str(file_destination))
                copy(file, file_destination)

    def check_triggers(self, days_run: int, days_per_run: int):
        """ Receives a yaml config file with only the trigger subtree and checks the trigger entries for correct
        configuration. Checks for dependencies within the models. The execution is never interrupted by this function,
        any errors found are reported in the logger.
        """
        if 'TRIGGER' in self.yaml['MOHID_WATER'] and self.yaml['MOHID_WATER']['TRIGGER']['ENABLE']:
            trigger_config = self.yaml['MOHID_WATER']['TRIGGER']
            if 'CHECK_ALL' in trigger_config:
                check = trigger_config['CHECK_ALL']
            else:
                check = True

            if days_run == 0 or check:

                if 'FOLDERS_TO_WATCH' in self.yaml:
                    folders = trigger_config['FOLDERS_TO_WATCH']
                else:
                    folders = None
                    self.logger.info("No folders to watch on triggers FOLDER_TO_WATCH parameter is empty.")

                if trigger_config['TRIGGER_MAX_WAIT'] in self.yaml:
                    timer = trigger_config['TRIGGER_MAX_WAIT'] * 3600
                else:
                    timer = static.DEFAULT_MAX_WAIT * 3600
                    self.logger.info(
                        "No waiting time on triggers TRIGGER_MAX_WAIT parameter is empty. Assigning default "
                        "max wait time of 6 hours.")

                if 'TRIGGER_POLLING_RATE' in trigger_config:
                    rate = trigger_config['TRIGGER_POLLING_RATE']
                else:
                    rate = static.DEFAULT_POLLING_RATE
                    self.logger.info(
                        "No polling rate on triggers. TRIGGER_POLLING_RATE is empty. Assigning "
                        "default polling rate of 120 seconds.")
                date_format = "%Y-%m-%d"
                initial_date = self.current_initial_date.strftime(date_format)
                tmp_date = self.current_initial_date + datetime.timedelta(days_per_run)
                final_date = tmp_date.strftime(date_format)
                if folders:
                    for folder in folders:
                        file = folder + initial_date + "_" + final_date + ".dat"
                        while not os.path.exists(file):
                            self.logger.info("Waiting for Trigger file to be created in watch folder")
                            time.sleep(rate)
                            timer = timer - rate
                            if timer < 0:
                                self.logger.info("Reached max waiting time while trying to find file " + str(file) + ". Resuming \
                                 execution without the file...")
                                return

                        finished = False
                        self.logger.info("Checking Trigger file status - will advance when becomes Finished")
                        while not finished:
                            f = open(file, 'r')
                            for line in f.readlines():
                                if line.startswith("STATUS"):
                                    if "FINISHED" in line:
                                        finished = True
                                        self.logger.info("File " + str(file) + " found with status FINISHED.")
                            f.close()
                            if not finished:
                                time.sleep(
                                    rate * 2)  # rate is doubled to prevent file error with several opens and closes
                                timer = timer - rate * 2
                                if timer < 0:
                                    self.logger.info("Reached max waiting time while waiting for file " + file + " to change \
                                     status to finished. Resuming execution without the correct status on this file...")
                                    return

    def write_trigger(self, main_path: Path, days_per_run, stage):
        """ Receives a yaml config file with only the trigger subtree and writes the trigger file.
        The execution is never interrupted by this function, any errors found are reported in the logger.
        """
        if 'TRIGGER' in self.yaml['MOHID_WATER'] and self.yaml['MOHID_WATER']['TRIGGER']['ENABLE']:
            trigger_config = self.yaml['MOHID_WATER']['TRIGGER']
            if 'WRITE_TRIGGER' in trigger_config and trigger_config['WRITER_TRIGGER']:
                output_trigger = trigger_config['WRITER_TRIGGER']
                dest_folder = main_path / "Log/"
            else:
                output_trigger = False
                self.logger.info("Output trigger not set. WRITE_TRIGGER parameter is empty.")

            if output_trigger:
                date_format = "%Y-%m-%d"
                initial_date = self.current_initial_date.strftime(date_format)
                tmp_date = self.current_initial_date + datetime.timedelta(days_per_run)
                final_date = tmp_date.strftime(date_format)
                filename = initial_date + "_" + final_date + ".dat"
                filepath = dest_folder / filename

                now = datetime.datetime.now()
                system_time = now.strftime("%Y-%m-%d %H:%M")

                file = open(filepath, 'w')
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

                file.write(
                    'START                         : ' + file_modifier.date_to_mohid_date(self.current_initial_date))
                file.write(
                    'END                           : ' + file_modifier.date_to_mohid_date(self.current_final_date))
                file.write('\n')

                if stage == "Running":
                    file.write('STATUS                        : RUNNING')
                elif stage == "Finished":
                    file.write('STATUS                        : FINISHED')

                file.write('\n')
                file.write('SYSTEM TIME                   : ' + system_time)
                file.close()

    def backup_simulation(self):
        """
        Back ups all the results located in the res/ folder of the project. It ignores all the results before consolidation
        (those that start with "MPI_"). Copies all the consolidated .hdf5 files to the Results_HDF/ folder in the backup path
        that the user defined. And the same goes for the Restart, TimeSeries and Discharges files.
        """

        date_format = "%Y-%m-%d"
        if 'DATE_FORMAT' in self.yaml['MOHID_WATER'].keys():
            date_format = self.yaml['MOHID_WATER']['DATE_FORMAT']

        initial_date = self.current_initial_date.strftime(date_format)
        tmp_date = self.current_initial_date + datetime.timedelta(self.yaml['SIMULATION']['DAYS_PER_RUN'])
        final_date = tmp_date.strftime(date_format)

        main_path = Path(self.yaml['MOHID_WATER']['MAIN_PATH'])
        self.logger.info("Simulation Results Initial Date: " + initial_date)
        self.logger.info("Simulation Results Final Date: " + final_date)

       # for model in self.yaml.keys():
        for model in self.yaml['MOHID_WATER']['MODELS'].keys():
            model_keys = self.yaml['MOHID_WATER']['MODELS'][model].keys()
            results_path_end = self.yaml['MOHID_WATER']['MODELS'][model]["PATH"] + "res/"
            results_path = main_path / results_path_end

            generic_path = Path(self.yaml['MOHID_WATER']['MODELS'][model]['STORAGE_PATH'])
            date_path = initial_date + "_" + final_date + "/"
            restart_storage = generic_path / "Restart/" / date_path
            results_storage = generic_path / "Results_HDF/" / date_path
            time_series_storage = generic_path / "Results_TimeSeries/" / date_path
            discharges_storage = generic_path / "Discharges/" / date_path
            
            # if 'HAS_SOLUTION_FROM_FILE' not in model_keys or not self.yaml[model]['HAS_SOLUTION_FROM_FILE']:
            if 'HAS_SOLUTION_FROM_FILE' not in model_keys:
                fin_files = glob.glob(str(results_path) + "*_1.fin")
                fin5_files = glob.glob(str(results_path) + "*_1.fin5")
                fin_files = fin5_files + fin_files
                if len(fin_files) > 0:
                    if not os.path.isdir(restart_storage):
                        os.makedirs(restart_storage)
                    for file in fin_files:
                        if os.path.split(file)[1].startswith("MPI"):
                            continue
                        file_destination = restart_storage / os.path.split(file)[1]
                        self.logger.info("Backup Simulation Fin_files: Copying " + str(file) + " to " + str(file_destination))
                        copy(file, file_destination)

            hdf5_files = glob.glob(str(results_path) + "*.hdf5")
            if len(hdf5_files) > 0:
                if not os.path.isdir(results_storage):
                    os.makedirs(results_storage)

                # only backup specific result files
                if 'RESULTS_LIST' in model_keys:
                    for file in hdf5_files:
                        if os.path.split(file)[1].startswith("MPI"):
                            continue
                        file_name = os.path.split(file)[1]
                        name_array = file_name.split("_")
                        if len(name_array) > 2:
                            # Hydrodynamic_1_Surface becomes Hydrodynamic_Surface
                            file_name_copy = name_array[0] + "_" + name_array[2]
                        else:
                            file_type = name_array[-1].split(".")[1]
                            file_name_copy = name_array[0] + "." + file_type

                        # if the file_name is not in the RESULTS_LIST it will be ignored
                        if file_name not in self.yaml[model]['RESULTS_LIST']:
                            continue

                        file_destination = results_storage / file_name_copy
                        self.logger.info("Backup Simulation HDF Files: Copying " + str(file) + " to " + str(file_destination))
                        copy(file, file_destination)
                # defaults to backup all results files
                else:
                    for file in hdf5_files:
                        if os.path.split(file)[1].startswith("MPI"):
                            continue

                        file_name = os.path.split(file)
                        name_array = file_name.split("_")
                        if name_array > 2:
                            # Hydrodynamic_1_Surface becomes Hydrodynamic_Surface
                            file_name = name_array[0] + "_" + name_array[2]
                        else:
                            file_type = name_array[-1].split(".")[1]
                            file_name = name_array[0] + "." + file_type
                        file_destination = results_storage / file_name
                        self.logger.info("Backup Simulation HDF Files: Copying " + str(file) + " to " + str(file_destination))

                        copy(file, file_destination)

            time_series_files = glob.glob(str(results_path) + "Run1/*.*")
            if len(time_series_files) > 0:
                if not os.path.isdir(time_series_storage):
                    os.makedirs(time_series_storage)
                for file in time_series_files:
                    file_destination = time_series_storage / os.path.split(file)[1]
                    copy(file, file_destination)
