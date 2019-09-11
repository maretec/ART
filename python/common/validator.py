import os

general_keys = ['artconfig', 'mohid', 'model', 'discharges', 'obc', 'meteo', 'model.dat', 'preprocessing', 'postprocessing']
artconfig_modules = ['mainPath', 'operationalMode', 'runPreProcessing', 'daysPerRun', 'refDaysToStart', 'numberOfRuns', 'module', 'runSimulation', 'startDate', 'endDate', 'outputToFile', 'outputFilePath', 'sendEmail', 'email']
mohid_modules = ['maxTime', 'exePath', 'outputToFile', 'outputFilePath', 'mpi']
mpi_modules = ['enable', 'exePath', 'totalProcessors']
model_modules = ['name', 'path', 'gridFile', 'dt', 'storagePath', 'resultsList']
discharges_modules = ['enable', 'path', 'dateFormat']
obc_modules = ['enable', 'fileType', 'simulatedDays', 'subFolders', 'dateInFileName', 'files', 'workPath']
meteo_modules = ['enable', 'models']
models_modules = ['#put meteo model Id here']
uniqueId_modules=['name', 'simulatedDays', 'fileNameFromModel', 'workPath', 'dateFormat', 'fileType']
modeldat_modules = ['MAXDT', 'GMTREFERENCE', 'DT_PREDICTION_INTERVAL']
name_of_block_modules_pre=['run', 'datDateChange', 'configFilePath', 'exePath', 'flags', 'outputToFile', 'outputFilePath']
name_of_block_modules_post=['run', 'datDateChange', 'configFilePath', 'exePath', 'flags', 'outputToFile', 'outputFilePath']

def validatePath(path):
    return path != None and os.path.exists(path) and path[-1] == "/"

def validateFile(path):
    return  path != None and os.path.isfile(path) and path[-1] == "/"

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

    valid = validatePath(yaml['artconfig']['mainPath'])

    if yaml['artconfig']['sendEmail']:
        valid = yaml['artconfig']['email'] != []

    return valid
    

def mohid_validation(yaml):
    valid = True
    for i in mohid_modules:
        if i not in yaml['mohid'].keys():
            valid = False

    for i in mpi_modules:
        if i not in yaml['mohid']['mpi'].keys():
            valid = False
    
    valid = validatePath(yaml['mohid']['exePath'])

    if yaml['mohid']['mpi']['enable']:
        valid = validatePath(yaml['mohid']['mpi']['exePath'])
    
    return valid


def model_validation(yaml):
    valid = True
    for i in model_modules:
        if i not in yaml['model'].keys():
            valid = False
    
    valid = validatePath(yaml['artconfig']['mainPath'] + yaml['model']['path'])

    return valid


def discharge_validation(yaml):    
    valid = True
    for i in discharges_modules:
        if i not in yaml['discharge'].keys():
            valid = False

    valid = yaml['discharges']['enable'] and validatePath(yaml['discharges']['path'])
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
    valid = yaml['preprocessing'].keys() != []
    for i in yaml['preprocessing'].keys():
        if yaml['postprocessing'][i]['datDateChange']:
            valid = validateFile(yaml['postprocessing'][i]['configFilePath'])
        for j in name_of_block_modules_pre:
            if j not in yaml['preprocessing'][i].keys():
                valid = False
    
    valid = validateFile(yaml['preprocessing']['exePath'])
    return valid


def postprocessing_validation(yaml):
    valid = True
    valid = yaml['postprocessing'].keys() != []
    for i in yaml['postprocessing'].keys():
        if yaml['postprocessing'][i]['datDateChange']:
            valid = validateFile(yaml['postprocessing'][i]['configFilePath'])
        for j in name_of_block_modules_pre:
            if j not in yaml['postprocessing'][i].keys():
                valid = False
    
    valid = validateFile(yaml['postprocessing']['exePath'])
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