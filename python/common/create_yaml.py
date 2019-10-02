artconfig_modules = ['mainPath', 'operationalMode', 'runPreProcessing', 'daysPerRun', 'refDaysToStart', 'numberOfRuns', 'module', 'runSimulation', 'startDate', 'endDate', 'outputToFile', 'outputFilePath', 'sendEmail', 'email']
mohid_modules = ['maxTime', 'exePath', 'outputToFile', 'outputFilePath', 'mpi']
mpi_modules = ['enable', 'exePath', 'totalProcessors']
model_modules = ['name', 'path', 'gridFile', 'dt', 'storagePath', 'resultsList', 'hasSolutionFromFile']
discharges_modules = ['enable', 'path', 'dateFormat']
obc_modules = ['enable', 'fileType', 'simulatedDays', 'subFolders', 'dateInFileName', 'dateFormat', 'files', 'workPath']
meteo_modules = ['enable', 'models']
models_modules = ['#put meteo model Id here']
uniqueId_modules=['name', 'simulatedDays', 'fileNameFromModel', 'workPath', 'dateFormat', 'fileType']
modeldat_modules = ['MAXDT', 'GMTREFERENCE', 'DT_PREDICTION_INTERVAL']
preprocessing_modules = ['#name of block']
name_of_block_modules_pre=['run', 'datDateChange', 'workingDirectory', 'configFilePath', 'exePath', 'flags', 'outputToFile', 'outputFilePath']
postprocessing_modules = ['#name of block']
name_of_block_modules_post=['run', 'datDateChange', 'configFilePath', 'workingDirectory', 'exePath', 'flags', 'outputToFile', 'outputFilePath']

def create_artconfig_block(filename):
    filename.write("artconfig:\n")
    for i in artconfig_modules:
        filename.write("  " + i + ":\n")

def create_mohid_block(filename):
    filename.write("mohid:\n")
    for i in mohid_modules:
        filename.write("  " + i + ":\n")
    for i in mpi_modules:
        filename.write("    " + i + ":\n")

def create_model_block(filename):
    filename.write("model:\n")
    for i in model_modules:
        filename.write("  " + i + ":\n")

def create_discharges_block(filename):
    filename.write("  discharges:\n")
    for i in discharges_modules:
        filename.write("    " + i + ":\n")

def create_obc_block(filename):
    filename.write("  obc:\n")
    for i in obc_modules:
        if i == "files":
            filename.write("    " + i + ": [<write list of files you want from the OBC workpath (e.g. ['Hydrodynamic', 'WaterProperties']). Different files require a new list>]\n")
        filename.write("    " + i + ":\n")

def create_meteo_block(filename, n):
    filename.write("  meteo:\n")
    for i in meteo_modules:
        filename.write("    " + i + ":\n")
    for _ in range(n):
        filename.write("      " + models_modules[0] + ":\n")
        for i in uniqueId_modules:
            filename.write("        " + i + ":\n")

def create_model_dat_block(filename):
    filename.write("  model.dat:\n")
    for i in modeldat_modules:
        filename.write("    " + i + ":\n")

def create_preprocessing_block(filename, n):
    filename.write("preprocessing:\n")
    for i in range(n):
        filename.write("  " + preprocessing_modules[0] + ":\n")
        for i in name_of_block_modules_pre:
            filename.write("    " + i + ":\n")

def create_postprocessing_block(filename, n):
    filename.write("postprocessing:\n")
    for i in range(n):
        filename.write("  " + postprocessing_modules[0] + ":\n")
        for i in name_of_block_modules_post:
            filename.write("    " + i + ":\n")

def create_yaml():
    filename = input("filename: ")
    f1 = filename + ".yaml"
    f = open(f1, "w+")

    number_model_blocks = int(input("number of model blocks: "))
    number_preprocessing_blocks = int(input("number of preprocessing blocks: "))
    number_postprocessing_blocks = int(input("number of postprocessing blocks: "))

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