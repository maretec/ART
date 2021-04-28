#//TODO UPDATE
'''
import os

general_keys = ['artconfig', 'mohidwater', 'model', 'preprocessing', 'postprocessing']
artconfig_modules = ['mainPath', 'operationalMode', 'runPreProcessing', 'daysPerRun', 'refDaysToStart', 'numberOfRuns', 'module', 'runSimulation', 'startDate', 'endDate', 'outputToFile', 'outputFilePath', 'sendEmail', 'email']
mohid_modules = ['maxTime', 'exePath', 'outputToFile', 'outputFilePath', 'mpi']
mpi_modules = ['enable', 'exePath', 'totalProcessors']
model_modules = ['name', 'path', 'gridFile', 'dt', 'storagePath', 'resultsList', 'hasSolutionFromFile', 'discharges', 'obc', 'meteo', 'model.dat']
discharges_modules = ['enable', 'path', 'dateFormat']
obc_modules = ['enable', 'fileType', 'simulatedDays', 'subFolders', 'dateInFileName', 'dateFormat', 'files', 'workPath']
meteo_modules = ['enable', 'models']
uniqueId_modules=['name', 'simulatedDays', 'fileNameFromModel', 'workPath', 'dateFormat', 'fileType']
modeldat_modules = ['MAXDT', 'GMTREFERENCE', 'DT_PREDICTION_INTERVAL']
name_of_block_modules_pre=['run', 'workingDirectory', 'datDateChange', 'configFilePath', 'exePath', 'flags', 'outputToFile', 'outputFilePath']
name_of_block_modules_post=['run', 'workingDirectory', 'datDateChange', 'configFilePath', 'exePath', 'flags', 'outputToFile', 'outputFilePath']

def check_unique_names(block):
    tmp=[]
    for i in block.keys():
        if i not in tmp:
            tmp.append(i)
        else:
            return False
    
    return True

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

    if yaml['artconfig']['runPreProcessing']:
        valid = yaml['preprocessing'].keys() != [] and yaml['postprocessing'].keys() != []
        if valid == False:
            return False

    valid = validatePath(yaml['artconfig']['mainPath'])
    if valid == False:
        return False

    if yaml['artconfig']['sendEmail']:
        valid = yaml['artconfig']['email'] != []

    return valid
    

def mohid_validation(yaml):
    valid = True
    for i in mohid_modules:
        if i not in yaml['mohidwater'].keys():
            valid = False

    for i in mpi_modules:
        if i not in yaml['mohidwater']['mpi'].keys():
            valid = False
    
    valid = validatePath(yaml['mohidwater']['exePath'])
    if valid == False:
        return False

    if yaml['mohidwater']['mpi']['enable']:
        valid = validatePath(yaml['mohidwater']['mpi']['exePath'])
    
    return valid


def model_validation(yaml):
    valid = True
    for i in model_modules:
        if i not in yaml['model'].keys():
            valid = False
    
    if valid == False:
        return False

    valid = validatePath(yaml['artconfig']['mainPath'] + yaml['model']['path'])

    return valid


def discharge_validation(yaml):    
    valid = True
    for i in discharges_modules:
        if i not in yaml['model']['discharge'].keys():
            valid = False

    if valid == False:
        return False

    valid = yaml['model']['discharges']['enable'] and validatePath(yaml['discharges']['path'])
    return valid


def obc_validation(yaml):
    valid = True
    for i in obc_modules:
        if i not in yaml['model']['obc'].keys():
            return False

    if yaml['model']['obc']['files'] == []:
        return False
        
    return valid


def meteo_validation(yaml):
    valid = True
    for i in meteo_modules:
        if i not in yaml['model']['meteo'].keys():
            valid = False
    
    for j in yaml['model']['meteo']['models'].keys():
        for k in uniqueId_modules:
            if k not in j.keys():
                valid = False
    
    return valid
    

def modeldat_validation(yaml):
    valid = True
    for i in modeldat_modules:
        if i not in yaml['model']['model.dat'].keys():
            valid = False
    
    return valid


def preprocessing_validation(yaml):
    valid = True
    if yaml['preprocessing'].keys() == []:
        return False
    
    for i in yaml['preprocessing'].keys():
        if yaml['postprocessing'][i]['datDateChange']:
            valid = validateFile(yaml['postprocessing'][i]['configFilePath'])
            if valid == False:
                return False

        for j in name_of_block_modules_pre:
            if j not in yaml['preprocessing'][i].keys():
                return False
    
    valid = check_unique_names(yaml['preprocessing'])
    if valid == False:
        return False

    valid = validateFile(yaml['preprocessing']['exePath'])
    return valid


def postprocessing_validation(yaml):
    valid = True
    if yaml['postprocessing'].keys() == []:
        return False

    for i in yaml['postprocessing'].keys():
        if yaml['postprocessing'][i]['datDateChange']:
            valid = validateFile(yaml['postprocessing'][i]['configFilePath'])
            if valid == False:
                return False

        for j in name_of_block_modules_pre:
            if j not in yaml['postprocessing'][i].keys():
                return False
    
    valid = check_unique_names(yaml['postprocessing'])
    if valid == False:
        return False

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

'''