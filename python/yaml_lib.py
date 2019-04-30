import yaml
import sys

def openYamlFile(path):
  with open(path, 'r') as ymlfile:
    return (yaml.safe_load(ymlfile))

def validateYamlSection(dict, sectionName, mandatoryList):
  mandatoryParameters = set(mandatoryList).difference(set(dict[sectionName]))
  if len(mandatoryParameters) != 0:
    raise ValueError("Missing mandatory parameter on " + sectionName + ": " + str(mandatoryParameters) + ".")
  if None in list(dict[sectionName].values()):
    raise ValueError("Blank value on " + sectionName + ".")

def validateYamlFile(yamlDict):
  validateYamlSection(yamlDict, 'artconfig', ['mainPath','startDate', 'endDate', 'runPreProcessing','runMohid', 'runPostProcessing'])
  if yamlDict['artconfig']['runMohid']:
    validateYamlSection(yamlDict, 'Mohid', [])
    if 'mpi' in yamlDict['Mohid']:
          validateYamlSection(yamlDict['Mohid'], 'mpi',[])
    for model in yamlDict['Mohid']['Models']:
      validateYamlSection(yamlDict['Mohid']['Models'], model, [])