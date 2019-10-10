artconfig_modules = ['MAIN_PATH', 'OPERATIONAL_MODE', 'RUN_PRE_PROCESSING', 'DAYS_PER_RUN', 'REF_DAYS_TO_START', 'NUMBER_OF_RUNS', 'MODULE', 'RUN_SIMULATION', 'START_DATE', 'END_DATE', 'OUTPUT_TO_FILE', 'OUTPUT_FILEPATH', 'SEND_EMAIL', 'EMAIL']
mohid_modules = ['MAX_TIME', 'EXE_PATH', 'OUTPUT_TO_FILE', 'OUTPUT_FiLE_PATH', 'MPI']
mpi_modules = ['ENABLE', 'EXE_PATH', 'TOTAL_PROCESSORS']
model_modules = ['NAME', 'PATH', 'GRID_FILE', 'DT', 'STORAGE_PATH', 'RESULTS_LIST', 'HAS_SOLUTION_FROM_FILE']
discharges_modules = ['ENABLE', 'PATH', 'DATE_FORMAT']
obc_modules = ['ENABLE', 'FILE_TYPE', 'SIMULATED_DAYS', 'SUB_FOLDERS', 'DATE_IN_FILENAME', 'DATE_FORMAT', 'FILES', 'WORK_PATH']
meteo_modules = ['ENABLE', 'MODELS']
models_modules = ['#put meteo model Id here']
uniqueId_modules=['NAME', 'SIMULATED_DAYS', 'FILENAME_FROM_MODEL', 'WORK_PATH', 'DATE_FORMAT', 'FILE_TYPE']
modeldat_modules = ['MAXDT', 'GMTREFERENCE', 'DT_PREDICTION_INTERVAL']
preprocessing_modules = ['#name of block']
name_of_block_modules_pre=['RUN', 'DAT_DATE_CHANGE', 'WORKING_DIRECTORY', 'CONFIG_FILEPATH', 'EXE_PATH', 'FLAGS', 'OUTPUT_TO_FILE', 'OUTPUT_FILEPATH']
postprocessing_modules = ['#name of block']
name_of_block_modules_post=['RUN', 'DAT_DATE_CHANGE', 'WORKING_DIRECTORY', 'CONFIG_FILEPATH', 'EXE_PATH', 'FLAGS', 'OUTPUT_TO_FILE', 'OUTPUT_FILEPATH']

def create_artconfig_block(filename):
    filename.write("ARTCONFIG:\n")
    for i in artconfig_modules:
        filename.write("  " + i + ":\n")

def create_mohid_block(filename):
    filename.write("MOHID:\n")
    for i in mohid_modules:
        filename.write("  " + i + ":\n")
    for i in mpi_modules:
        filename.write("    " + i + ":\n")

def create_model_block(filename):
    filename.write("MODEL:\n")
    for i in model_modules:
        filename.write("  " + i + ":\n")

def create_discharges_block(filename):
    filename.write("  DISCHARGES:\n")
    for i in discharges_modules:
        filename.write("    " + i + ":\n")

def create_obc_block(filename):
    filename.write("  OBC:\n")
    for i in obc_modules:
        if i == "files":
            filename.write("    " + i + ": [<write list of files you want from the OBC workpath (e.g. ['Hydrodynamic', 'WaterProperties']). Different files require a new list>]\n")
        filename.write("    " + i + ":\n")

def create_meteo_block(filename, n):
    filename.write("  METEO:\n")
    for i in meteo_modules:
        filename.write("    " + i + ":\n")
    for _ in range(n):
        filename.write("      " + models_modules[0] + ":\n")
        for i in uniqueId_modules:
            filename.write("        " + i + ":\n")

def create_model_dat_block(filename):
    filename.write("  MODEL.DAT:\n")
    for i in modeldat_modules:
        filename.write("    " + i + ":\n")

def create_preprocessing_block(filename, n):
    filename.write("PREPROCESSING:\n")
    for i in range(n):
        filename.write("  " + preprocessing_modules[0] + ":\n")
        for i in name_of_block_modules_pre:
            filename.write("    " + i + ":\n")

def create_postprocessing_block(filename, n):
    filename.write("POSTPROCESSING:\n")
    for i in range(n):
        filename.write("  " + postprocessing_modules[0] + ":\n")
        for i in name_of_block_modules_post:
            filename.write("    " + i + ":\n")

def create_yaml():
    filename = input("FILENAME: ")
    f1 = filename + ".yaml"
    f = open(f1, "w+")

    number_model_blocks = int(input("NUMBER OF MODEL BLOCKS: "))
    number_model_meteo_blocks = []
    
    for i in range(number_model_blocks):
        t = int(input("NUMBER OF METEO BLOCKS FOR MODEL BLOCK NR." + str(i+1) + " : "))
        number_model_meteo_blocks.append(t)

    number_preprocessing_blocks = int(input("NUMBER OF PREPROCESSING BLOCKS: "))
    number_postprocessing_blocks = int(input("NUMBER OF POSTPROCESSING BLOCKS: "))

    create_artconfig_block(f)
    create_mohid_block(f)
    create_model_block(f)
    create_discharges_block(f)
    create_obc_block(f)
    create_meteo_block(f, number_model_blocks)
    create_model_dat_block(f)
    create_preprocessing_block(f, number_preprocessing_blocks)
    create_postprocessing_block(f, number_postprocessing_blocks)

create_yaml()