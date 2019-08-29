import os

valid = True
general_keys = ['artconfig', 'mohid', 'model', 'discharges', 'obc', 'meteo', 'model.dat', 'preprocessing', 'postprocessing']
artconfig_modules = ['mainPath', 'operationalMode', 'runPreProcessing', 'daysPerRun', 'refDaysToStart', 'numberOfRuns', 'module', 'runSimulation', 'startDate', 'endDate', 'ouputFile', 'outputFilePath', 'sendEmail', 'email']
mohid_modules = ['maxTime', 'exePath', 'outputToFile', 'outputFilePath', 'mpi']
mpi_modules = ['enable', 'numDomains', 'exePath', 'keepDecomposedFile', 'ddcComposerNumProcessors', 'joinerVersion']
model_modules = ['name', 'path', 'mpiProcessors', 'obc', 'meteo', 'gridFile', 'runId', 'DT', 'backupPath', 'storagePath', 'hasWaterProperties', 'hasSurfaceHDF', 'hasGOTM', 'hasOutputWindow', 'hasSolutionFromFile']
obc_modules = ['enable', 'modelName', 'simulatedDays']
meteo_modules = ['enable', 'modelName', 'simulatedDays', 'fileNameModel', 'workPath']

def validate(yaml):
    for i in general_keys:
        if i not in yaml.keys():
            valid = False

    for i in artconfig_modules:
        if i not in yaml['artconfig'].keys():
            valid = False

    if 'mohid' not in yaml.keys():
        valid = False

    if 'mpi' not in yaml['mohid']:
        valid = False

    for i in mpi_modules:
        if i not in yaml['mohid']['mpi'].keys():
            valid = False
    
    for i in mohid_modules:
        if i not in yaml['mohid'].keys():
            valid = False
    
    if 'model' not in yaml.keys():
        valid = False
    
    for i in model_modules:
        if i not in yaml['model'].keys():
            valid = False
    
    for i in obc_modules:
        if i not in yaml['model']['obc'].keys():
            valid = False
    
    for i in meteo_modules:
        if i not in yaml['model']['meteo'].keys():
            valid = False