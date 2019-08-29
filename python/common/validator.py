import os

general_keys = ['artconfig', 'mohid', 'model', 'discharges', 'obc', 'meteo', 'model.dat', 'preprocessing', 'postprocessing']
artconfig_modules = ['mainPath', 'operationalMode', 'runPreProcessing', 'daysPerRun', 'refDaysToStart', 'numberOfRuns', 'module', 'runSimulation', 'startDate', 'endDate', 'ouputFile', 'outputFilePath', 'sendEmail', 'email']
mohid_modules = ['exePath', 'outputToFile', 'outputFilePath', 'mpi']
mpi_modules = ['enable', 'exePath', 'totalProcessors']
model_modules = ['name', 'path', 'gridFile', 'dt', 'storagePath']
discharges_modules = ['enable', 'path', 'dateFormat']
obc_modules = ['enable', 'suffix', 'hasSolutionFromFile', 'prefix', 'dateFormat', 'filetype', 'simulatedDays', 'subFolders', 'workPath']
meteo_modules = ['enable']
models_modules = ['uniqueId', 'name', 'simulatedDays', 'fileNameFromModel', 'workPath', 'dateFormat', 'fileType']
modeldat_modules = ['MAXDT', 'GMTREFERENCE', 'DT_PREDICTION_INTERVAL']
preprocessing_modules = ['name of block', 'run', 'datDateChange', 'configFilePath', 'exePath', 'flags', 'outputToFile', 'outputFilePath']
postprocessing_modules = ['name of block', 'run', 'datDateChange', 'configFilePath', 'exePath', 'flags', 'outputToFile', 'outputFilePath']

def general_validation(yaml):
    valid = True
    for i in general_keys:
        if i not in yaml.keys():
            valid = False

    return valid


def artconfig_validation(yaml):
    valid = True
    for i in artconfig_modules:
        if i not in yaml['artconfig'].keys():
            valid = False

    return valid


def mohid_validation(yaml):
    valid = True
    for i in mohid_modules:
        if i not in yaml['mohid'].keys():
            valid = False

    for i in mpi_modules:
        if i not in yaml['mohid']['mpi'].keys():
            valid = False
    
    return valid


def discharge_validation(yaml):    
    valid = True
    for i in discharges_modules:
        if i not in yaml['discharge'].keys():
            valid = False

    return valid


def obc_validation(yaml):
    valid = True
    for i in obc_modules:
        if i not in yaml['obc'].keys():
            valid = False

    return valid


def meteo_validation(yaml):
    valid = True
    for i in meteo_modules:
        if i not in yaml['meteo'].keys():
            valid = False
    
    for i in model_modules:
        if i not in yaml['meteo']['models'].keys():
            valid = False
    
    return valid
    

def modeldat_validation(yaml):
    valid = True
    for i in modeldat_modules:
        if i not in yaml['model.dat'].keys():
            valid = False
    
    return valid


def preprocessing_validation(yaml):
    valid = True
    for i in preprocessing_modules:
        if i not in yaml['preprocessing'].keys():
            valid = False
    
    return valid


def postprocessing_validation(yaml):
    valid = True
    for i in postprocessing_modules:
        if i not in yaml['postprocessing'].keys():
            valid = False
    
    return valid

def validate_yaml(yaml):
    return general_validation(yaml) and\
    artconfig_validation(yaml) and\
    mohid_validation(yaml) and\
    discharge_validation(yaml) and\
    obc_validation(yaml) and\
    meteo_validation(yaml) and\
    modeldat_validation(yaml) and\
    preprocessing_validation(yaml) and\
    postprocessing_validation(yaml)