#!/usr/bin/bash

artconfig_modules = ['mainPath', 'operationalMode', 'runPreProcessing', 'daysPerRun', 'refDaysToStart', 'numberOfRuns', 'module', 'runSimulation', 'startDate', 'endDate', 'ouputFile', 'outputFilePath', 'sendEmail', 'email']
mohid_modules = ['exePath', 'outputToFile', 'outputFilePath', 'mpi']
mpi_modules = ['enable', 'exePath', 'totalProcessors']
model_modules = ['name', 'path', 'gridFile', 'dt', 'storagePath']
discharges_modules = ['enable', 'path', 'dateFormat']
obc_modules = ['enable', 'suffix', 'hasSolutionFromFile', 'prefix', 'dateFormat', 'filetype', 'simulatedDays', 'subFolders', 'workPath']
meteo_modules = ['enable', 'models']
models_modules = ['uniqueId', 'name', 'simulatedDays', 'fileNameFromModel', 'workPath', 'dateFormat', 'fileType']
modeldat_modules = ['MAXDT', 'GMTREFERENCE', 'DT_PREDICTION_INTERVAL']
preprocessing_modules = ['name of block', 'run', 'datDateChange', 'configFilePath', 'exePath', 'flags', 'outputToFile', 'outputFilePath']
postprocessing_modules = ['name of block', 'run', 'datDateChange', 'configFilePath', 'exePath', 'flags', 'outputToFile', 'outputFilePath']

def create_artconfig_block(filename):
    filename.write("artconfig:")
    for i in artconfig_modules:
        filename.write("\t" + i + str(":"))

def create_mohid_block(filename):
    filename.write("mohid:")
    for i in mohid_modules:
        filename.write("\t" + i + str(":"))
    for i in mpi_modules:
        filename.write("\t\t" + i + str(":"))

def create_model_block(filename):
    filename.write("model:")
    for i in model_modules:
        filename.write("\t" + i + str(":"))

def create_discharges_block(filename):
    filename.write("discharges:")
    for i in discharges_modules:
        filename.write("\t" + i + str(":"))

def create_obc_block(filename):
    pass #ToDo this

def create_meteo_block(filename):
    filename.write("meteo:")
    for i in meteo_modules:
        filename.write("")

def create_model_dat_block(filename):


def create_preprocessing_block(filename):


def create_postprocessing_block(filename):




def create_yaml():
    filename = input("filename: ")
    f = open(filename, "w+")

    number_model_blocks = int(input("number of model blocks: "))
    number_preprocessing_blocks = int(input("number of preprocessing blocks: "))
    number_postprocessing_blocks = int(input("number of postprocessing blocks: "))

    create_artconfig_block(filename)
    create_mohid_block(filename)
    create_model_block(filename)
    create_discharges_block(filename)
    create_obc_block(filename)
    create_meteo_block(filename)
    create_model_dat_block(filename)
    create_preprocessing_block(filename)
    create_postprocessing_block(filename)
