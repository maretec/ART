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

def validatorYamlFile(yamlDict):
  validateYamlSection(yamlDict, 'artconfig', ['mainPath','startDate', 'endDate'])
  validateYamlSection(yamlDict, 'Mohid', [])
  for model in yamlDict['models']:
    validateYamlSection(yamlDict['models'], model, [])

def main():
  try:
    cfg = openYamlFile("default.yaml")
    validatorYamlFile(cfg)
  except ValueError as e:
    print(e)
    sys.exit()
    

if __name__== "__main__":
  main()