import common.constants as static
import datetime
import common.file_modifier
import os.path
import common.config as cfg
from shutil import copy2
import subprocess
import glob

def mpi_params(yaml_file):
    mohid = yaml_file['mohid']
    if 'mpi' in mohid.keys():
        if mohid['mpi']['enable']:
            exe_path = mohid['mpi']['exePath']
            keepDecomposedFiles = mohid['mpi']['keepDecomposedFiles']
            ddcParserNumProcessors = mohid['mpi']['ddcComposerNumProcessors']
            joinerVersion = mohid['mpi']['joinerVersion']


def run_mohid(yaml):
    if 'mpi' in yaml['mohid'].keys() and yaml['mohid']['mpi']['enable']:
        mpi = yaml['mohid']['mpi']
        flags = " -np " + str(yaml['mohid']['mpi']['totalProcessors']) + " -f /opt/hosts " + \
                yaml['mohid']['exePath']
        static.logger.info("Starting MOHID MPI")
        subprocess.run("mpiexec", flags)
        static.logger.info("MOHID MPI run finished")
    else:
        static.logger.info("Starting MOHID run")
        subprocess.run(yaml['mohid']['exePath'])
        static.logger.info("MOHID run finished")



def change_model_dat(yaml, model):
    static.logger.debug("Creating new model file for model: " + model['name'])
    keys = model.keys()
    path = yaml['artconfig']['mainPath'] + model['path'] + "data/"
    if not os.path.isdir(path):
        static.logger.debug("Path for model folder does not exist.")
        static.logger.debug("Check path parameters in the yaml file. Exiting ART.")
        exit(1)

    file_path = path + "Model_" + str(model['runId']) + ".dat"

    file = open(file_path, 'w+')
    common.file_modifier.line_creator(file, "START",
                                        common.file_modifier.date_to_mohid_date(cfg.current_initial_date))
    common.file_modifier.line_creator(file, "END", common.file_modifier.date_to_mohid_date(cfg.current_final_date))
    common.file_modifier.line_creator(file, "DT", str(model['dt']))
    if 'mohid.dat' in keys:
        for key in model['mohid.dat'].keys():
            common.file_modifier.line_creator(file, key, model['mohid.dat'][key])
    static.logger.debug("Model " + model["name"] + " .dat file was created.")
    file.close()
    return


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
                obc_initial_date = cfg.current_initial_date + datetime.timedelta(days=n)
                obc_final_date = cfg.current_initial_date + datetime.timedelta(days=simulations_available)

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
                obc_initial_date = cfg.current_initial_date + datetime.timedelta(days=n)
                obc_final_date = cfg.current_final_date + datetime.timedelta(days=simulations_available)

                obc_initial_date = obc_initial_date.strftime("%Y-%m-%d")
                obc_final_date = obc_final_date.strftime("%Y-%m-%d")

                hydro_source_path = model['obc']['workPath'] + str(obc_initial_date) + "_" + obc_final_date + "/" + \
                 "Hydrodynamic"
                water_source_path = model['obc']['workPath'] + str(obc_initial_date) + "_" + obc_final_date + "/" + \
                    "WaterProperties"

                if 'suffix' in obc_keys:
                    hydro_source_path += "_" + model['obc']['suffix']
                    water_source_path += "_" + model['obc']['suffix']

                hydro_source_path +=  "." + file_type
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

                        print(hydro_source_path)
                        print(water_source_path)
                        copy2(hydro_source_path, hydro_dest_file)
                        copy2(water_source_path, water_dest_file)
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
            
            meteo_initial_date = cfg.current_initial_date.strftime(date_format)
            meteo_final_date = None
            if 'simulatedDays' in meteo_keys:
                meteo_final_date = cfg.current_initial_date + datetime.timedelta(days=model['meteo']['models']
                [meteo_model]['simulatedDays'])
                meteo_final_date = meteo_final_date.strftime(date_format)
            else:
                meteo_final_date = cfg.current_final_date.strftime(date_format)
        
            file_type = "hdf5"
            if 'fileType' in meteo_keys:
                file_type = model['meteo']['models'][meteo_model]['fileType']

            meteo_sufix = "TAGUS3D"
            meteo_file_source = None
            if 'fileNameFromModel' in meteo_keys and model['meteo']['models'][meteo_model]['fileNameFromModel']:
                meteo_sufix = model['meteo']['models'][meteo_model]['name']
                meteo_file_source = model['meteo']['models'][meteo_model]['workPath'] + \
                    model['meteo']['models'][meteo_model]['name'] + "_" + model['name'] + "_" + meteo_initial_date + "_" + \
                    meteo_final_date + "." + file_type 
            else:
                meteo_file_source = model['meteo']['models'][meteo_model]['workPath'] + "meteo" + "_" + meteo_initial_date \
                    + "_" + meteo_final_date + "." + file_type
        
            print(meteo_file_source)
            if os.path.isfile(meteo_file_source):
                meteo_file_dest_folder = yaml['artconfig']['mainPath'] + "GeneralData/BoundaryConditions/Atmosphere/" + \
                    model['name'] + "/" + model['meteo']['models'][meteo_model]['name'] + "/"
                
                if not os.path.isdir(meteo_file_dest_folder):
                    os.makedirs(meteo_file_dest_folder)

                meteo_file_dest = meteo_file_dest_folder +  model['meteo']['models'][meteo_model]['name'] + "_" + \
                    model['name'] + "." + file_type
                    
                copy2(meteo_file_source,meteo_file_dest)
                static.logger.debug("Copied meteo file from " + meteo_file_source + " to " + meteo_file_dest)
                return
            else:
                continue
        
        static.logger.debug("get_meteo_file: Meteo file could not be found. Check yaml file for configuration errors.")
        raise FileNotFoundError("get_meteo_file: Meteo file could not be found. Check yaml file for configuration " +
            "errors.")
        

def gather_restart_files(yaml, model):
    static.logger.debug("Gathering the restart files for model: " + model['name'])
    previous_init_date = cfg.current_initial_date - datetime.timedelta(days=1)
    previous_final_date = previous_init_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])    
    path_fin_files = model['storagePath'] + "Restart/" + previous_init_date.strftime("%Y-%m-%d") + "_" + previous_final_date.strftime("%Y-%m-%d") + "/"

    if not os.path.isdir(path_fin_files):
        static.logger.debug("Restart folder: " + path_fin_files + "does not exist.")
        raise FileNotFoundError("Restart folder: " + path_fin_files + "does not exist.")
    
    model_keys = model.keys()

    restart_files_dest = yaml['mainPath'] + model['path'] + "res/"
    if not os.path.isdir(restart_files_dest):
        os.makedirs(restart_files_dest)

    if 'mpi' in model_keys and model['mpi']['enable']:
        print("None")
    else:
        if 'hasWaterProperties' in model_keys and model['hasWaterProperties']:
            water_properties_source = path_fin_files + "Hydrodynamic_1.fin"
            water_properties_dest = restart_files_dest  + "Hydrodynamic_0.fin" 
            copy2(water_properties_source, water_properties_dest)
        if 'hasGOTM' in model_keys and model['hasGOTM']:
            gotm_source = path_fin_files + "GOTM_1.fin"
            gotm_dest = restart_files_dest + "GOTM_0.fin"
            copy2(gotm_source, gotm_dest)
        if 'hasInterfacedSedimentWater' in model_keys and model['hasInterfacedSedimentWater']:
            interfaced_source = path_fin_files + "InterfaceSedimentWater_1.fin"
            interfaced_dest = restart_files_dest + "InterfaceSedimentWater_0.fin"
            copy2(interfaced_source, interfaced_dest)
        if 'hasHydrodynamics'in model_keys and model['hasHydrodynamics']:
            hydro_source = path_fin_files + "Hydrodynamic_1.fin"
            hydro_dest = restart_files_dest + "Hydrodynamic_0.fin"
            copy2(hydro_source, hydro_dest)


def backup_simulation(yaml):
    initial_date = cfg.current_initial_date.strftime("%Y-%m-%d")
    tmp_date = cfg.current_initial_date + datetime.timedelta(yaml['artconfig']['daysPerRun'])
    final_date = tmp_date.strftime("%Y-%m-%d")

    for model in yaml['mohid']['models']:
        
        backup_storage = yaml['mohid']['models'][model]['storagePath'] + "Restart/" + initial_date + "_" + final_date +"/"
      
        if not os.path.isdir(backup_storage):
            os.makedirs(backup_storage)

        model_keys = yaml['mohid']['models'][model].keys()
        mohid_keys = yaml['mohid']
        #TODO decide where has solution from file must be
        if 'hasSolutionFromFile' not in model_keys or not yaml['mohid']['models'][model]['hasSolutionFromFile']:
            if 'mpi' in mohid_keys:
                mpi_keys = yaml['mohid']['mpi'].keys()
                if 'enable' in mpi_keys and yaml['mohid']['enable']:
                    if 'keepDecomposedFiles' in mpi_keys and yaml['mohid']['mpi']['keepDecomposedFiles']:
                        for i in range(1, yaml['mohid']['models'][model]['numProcessors']):
                            results_path = yaml['artconfig']['mainPath'] + yaml['mohid']['models'][model]['path'] + "res/MPI_" + str(i) + "_"
                            backup_path = backup_storage + "MPI_" + str(i) + "_"
                            if 'hasHydrodynamics'in model_keys and yaml['mohid']['models'][model]['hasHydrodynamics']:
                                hydro_source = results_path + "Hydrodynamic_1.fin"
                                hydro_dest = backup_path + "Hydrodynamic_1.fin"
                                copy2(hydro_source, hydro_dest)
                            if 'hasWaterProperties' in model_keys and yaml['mohid']['models'][model]['hasWaterProperties']:
                                water_properties_source = results_path + "WaterProperties_1.fin"
                                water_properties_dest = backup_path  + "WaterProperties_1.fin" 
                                copy2(water_properties_source, water_properties_dest)
                            if 'hasGOTM' in model_keys and yaml['mohid']['models'][model]['hasGOTM']:
                                gotm_source = results_path + "GOTM_1.fin"
                                gotm_dest = backup_path + "GOTM_1.fin"
                                copy2(gotm_source, gotm_dest)
                            if 'hasInterfacedSedimentWater' in model_keys and yaml['mohid']['models'][model]['hasInterfacedSedimentWater']:
                                interfaced_source = results_path + "InterfaceSedimentWater_1.fin"
                                interfaced_dest = backup_path + "InterfaceSedimentWater_1.fin"
                                copy2(interfaced_source, interfaced_dest)  
            else:
                results_path = yaml['artconfig']['mainPath'] + yaml['mohid']['models'][model]['path'] + "res/"
                if 'hasHydrodynamics'in model_keys and yaml['mohid']['models'][model]['hasHydrodynamics']:
                    print('hasHydrodynamics')
                    hydro_source = results_path + "Hydrodynamic_1.fin"
                    hydro_dest = backup_storage + "Hydrodynamic_1.fin"
                    copy2(hydro_source, hydro_dest)
                if 'hasWaterProperties' in model_keys and yaml['mohid']['models'][model]['hasWaterProperties']:
                    water_properties_source = results_path + "WaterProperties_1.fin"
                    water_properties_dest = backup_storage  + "WaterProperties_1.fin" 
                    copy2(water_properties_source, water_properties_dest)
                if 'hasGOTM' in model_keys and yaml['mohid']['models'][model]['hasGOTM']:
                    gotm_source = results_path+ "GOTM_1.fin"
                    gotm_dest = backup_storage + "GOTM_1.fin"
                    copy2(gotm_source, gotm_dest)
                if 'hasInterfacedSedimentWater' in model_keys and yaml['mohid']['models'][model]['hasInterfacedSedimentWater']:
                    interfaced_source = results_path + "InterfaceSedimentWater_1.fin"
                    interfaced_dest = backup_path + "InterfaceSedimentWater_1.fin"
                    copy2(interfaced_source, interfaced_dest)  


def backup_simulation2(yaml):
    initial_date = cfg.current_initial_date.strftime("%Y-%m-%d")
    tmp_date = cfg.current_initial_date + datetime.timedelta(yaml['artconfig']['daysPerRun'])
    final_date = tmp_date.strftime("%Y-%m-%d")

    for model in yaml['mohid']['models']:
        
        storage = yaml['mohid']['models'][model]['storagePath'] + "Restart/" + initial_date + "_" + final_date +"/"
      
        

        model_keys = yaml['mohid']['models'][model].keys()
        mohid_keys = yaml['mohid']
        results_path = yaml['artconfig']['mainPath'] + yaml['mohid']['models'][model]['path'] + "res/"
        
        restart_storage = yaml['mohid']['models'][model]['storagePath'] + "Restart/" + initial_date + "_" + final_date +"/"
        results_storage = yaml['mohid']['models'][model]['storagePath'] + "Results_HDF/" + initial_date + "_" + final_date +"/"
        if not os.path.isdir(restart_storage):
            os.makedirs(restart_storage)
        if not os.path.isdir(results_storage):
            os.makedirs(results_storage)

        if 'hasSolutionFromFile' not in model_keys or not yaml['mohid']['models'][model]['hasSolutionFromFile']:
            fin_files = glob.glob(results_path+"*.fin")
            for file in fin_files:
                file_destination = restart_storage + os.path.split(file)[1]
                copy(file, file_destination)
    
        hdf5_files = glob.glob(results_path+"*.hdf5")
        for file in hdf5_files:
            file_destination = results_storage + os.path.split(file)[1]
            copy(file, file_destination)


def process_models(yaml):
    for model in yaml['mohid']['models']:
       # get_meteo_file(yaml, yaml['mohid']['models'][model])
        #gather_boundary_conditions(yaml, yaml['mohid']['models'][model])
        change_model_dat(yaml, yaml['mohid']['models'][model])
        #gather_restart_files(yaml, yaml['mohid']['models'][model])
    run_mohid(yaml)
    backup_simulation2(yaml)


def execute(yaml):
    static.logger.debug("Run MOHID enabled")
    if yaml['artconfig']['operationalMode']:
        cfg.global_initial_date = datetime.today() + datetime.time(days=yaml['artconfig']['refDayToStart'])
        for i in range(1, cfg.number_of_runs+1):
            cfg.current_initial_date = cfg.global_initial_date + datetime.timedelta(days=i-1)
            cfg.current_final_date = cfg.current_initial_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
            static.logger.info("========================================")
            static.logger.info("STARTING FORECAST ( " + str(i) + " of " + str(cfg.number_of_runs) + " )")
            static.logger.info("========================================")
            process_models(yaml)
    else:
        cfg.current_initial_date = cfg.global_initial_date
        cfg.current_final_date = cfg.current_initial_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
        static.logger.info("========================================")
        static.logger.info("STARTING FORECAST")
        static.logger.info("========================================")
        process_models(yaml)

    return None
