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
    for model in yaml['mohid']['models']:
        get_meteo_file(yaml, model)
        gather_boundary_conditions(yaml, model)
        change_model_dat(yaml, model)
        gather_restart_files(yaml, model)
        run_mohid(yaml, model)


def change_model_dat(yaml, model):
    static.logger.debug("Creating new model file for model: " + model['name'])
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
    if 'obc' in model_keys and 'enable' in model['obc'].keys() and model['obc']['enable']:
        static.logger.debug("Gathering boundary conditions for " + model['name'])
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
                obc_initial_date = cfg.global_initial_date + datetime.timedelta(days=n)
                obc_final_date = cfg.global_initial_date + datetime.timedelta(days=simulations_available)

                obc_initial_date = obc_initial_date.strftime(date_format)
                obc_final_date = obc_final_date.strftime(date_format)

                obc_source_path = model['obc']['workPath'] + model['obc']['prefix'] + "_" + model['name'] + obc_initial_date \
                    + "_" + obc_final_date + "." + file_type

                if os.path.isfile(obc_source_path):
                    obc_dest_folder = yaml['artconfig']['mainPath'] + folder_label + model['name'] + "/"
                    if os.path.isdir(obc_dest_folder):
                        obc_dest_file = obc_dest_folder + model['obc']['prefix'] + "_" + model['name'] + "." + file_type
                        copy2(obc_source_path, obc_dest_file)
                    else:
                        static.logger.debug("Destination folder for OBC files not found: " + obc_dest_folder)
                        raise FileNotFoundError("Destination folder for OBC files not found: " + obc_dest_folder)
                else:
                    static.logger.debug("Source file for OBC file not found: " + obc_source_path)
                    raise FileNotFoundError("Source file for OBC file not found: " + obc_source_path)

        elif 'hasSolutionFromFile' in obc_keys and model['obc']['hasSolutionFromFile']:
            for n in range(0, simulations_available - 1, -1):
                obc_initial_date = cfg.global_initial_date + datetime.timedelta(days=n)
                obc_final_date = cfg.global_final_date + datetime.timedelta(days=simulations_available)

                
                obc_initial_date = obc_initial_date.strftime(date_format)
                obc_final_date = obc_final_date.strftime(date_format)

                hydro_source_path = model['obc']['workPath'] + obc_initial_date + "_" + obc_final_date + "/" + \
                 "Hydrodynamic"
                water_source_path = model['obc']['workPath'] + obc_initial_date + "_" + obc_final_date + "/" + \
                    "WaterProperties"

                if 'suffix' in obc_keys:
                    hydro_source_path += "_" + model['obc']['suffix']
                    water_source_path += "_" + model['obc']['suffix']

                hydro_source_path +=  "." + file_type
                water_source_path += "." + file_type
               

                if os.path.isfile(hydro_source_path):
                    if os.path.isfile(water_source_path):
                        dest_folder = yaml['artconfig']['mainPath'] + folder_label + model['name']
                        if os.path.isdir(dest_folder):
                            hydro_dest_file = dest_folder + "/Hydrodynamic" 
                            water_dest_file = dest_folder + "/WaterProperties"

                            if 'suffix' in obc_keys:
                                hydro_dest_file += "_" + model['obc']['suffix']
                                water_dest_file += "_" + model['obc']['suffix'] 
                            
                            hydro_dest_file += "." + file_type
                            water_dest_file += "." + file_type

                            print(hydro_source_path)
                            print(water_source_path)
                            copy2(hydro_source_path, hydro_dest_file)
                            copy2(water_source_path, water_dest_file)
                        else:
                            #TODO create folder if do not exist
                            static.logger.debug("Folder for Hydrodynamic/Waterproperties file does not exist: " + 
                            dest_folder)
                            raise FileNotFoundError("Folder for Hydrodynamic/Waterproperties file does not exist: " + 
                            dest_folder)
                    else:
                        static.logger.debug("gather_boundary_conditions: File " + water_source_path + " does not exist.")
                else:
                    static.logger.debug("gather_boundary_conditions: File " + hydro_source_path + " does not exist. ")


def get_meteo_file(yaml, model):
    model_keys = model.keys()
    if 'meteo' in model_keys and model['meteo']['enable']:
        meteo_models_keys = model['meteo']['models'].keys()

        for meteo_model in meteo_models_keys:
            meteo_keys = model['meteo']['models'][meteo_model].keys()

            date_format = "%Y-%m-%d"
            if 'dateFormat' in meteo_keys:
                date_format = model['meteo'][meteo_model]['dateFormat']
            
            meteo_initial_date = cfg.global_initial_date.strftime(date_format)
            meteo_final_date = None
            if 'simulatedDays' in meteo_keys:
                meteo_final_date = cfg.global_initial_date + datetime.timedelta(days=model['meteo']['models']
                [meteo_model]['simulatedDays'])
                meteo_final_date = meteo_final_date.strftime(date_format)
            else:
                meteo_final_date = cfg.global_final_date.strftime(date_format)
        
            file_type = "hdf5"
            if 'fileType' in meteo_keys:
                file_type = model['meteo']['models'][meteo_model]['fileType']

            meteo_sufix = "TAGUS3D"
            meteo_file_source = None
            if 'fileNameFromModel' in meteo_keys and model['meteo']['models'][meteo_model]['fileNameFromModel']:
                meteo_sufix = model['meteo']['models'][meteo_model]['name']
                meteo_file_source = model['meteo']['models'][meteo_model]['workPath'] + \
                    model['meteo']['models'][meteo_model]['name'] + "_" + meteo_sufix + "_" + meteo_initial_date + "_" + \
                    meteo_final_date + "." + file_type 
            else:
                meteo_file_source = model['meteo']['models'][meteo_model]['workPath'] + "meteo" + "_" + meteo_initial_date \
                    + "_" + meteo_final_date + "." + file_type
        
            if os.path.isfile(meteo_file_source):
                meteo_file_dest_folder = yaml['artconfig']['mainPath'] + "GeneralData/BoundaryConditions/Atmosphere/" + \
                model['name'] + "/" + model['meteo']['models'][meteo_model] + "/"
                
                if not os.path.isdir(meteo_file_dest_folder):
                    os.makedirs(meteo_file_dest_folder)

                meteo_file_dest = meteo_file_dest_folder +  model['meteo'][meteo_model] + "_" + model['name'] + \
                    "." + file_type

                copy2(meteo_file_source,meteo_file_dest)
                static.logger.debug("Copied meteo file from " + meteo_file_source + " to " + meteo_file_dest)
                return
            else:
                continue
        
        static.logger.debug("get_meteo_file: No meteo file could be find. Check yaml file for configuration errors.")
        raise FileNotFoundError("get_meteo_file: No meteo file could be find. Check yaml file for configuration" +
            "errors.")
        
def execute(yaml):
    get_meteo_file(yaml, yaml['mohid']['models']['model1'])
    gather_boundary_conditions(yaml, yaml['mohid']['models']['model1'])
    return None
