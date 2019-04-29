import yaml
import sys


def openYamlFile(path):
  with open(path, 'r') as ymlfile:
    return (yaml.safe_load(ymlfile))

def validateArtConfig(artConfig):
  mandatoryParameters = set(['mainPath', 'startDate', 'endDate'])
  if set(mandatoryParameters).issubset(set(artConfig)):
    print(":)")
  else:
    raise ValueError("Missing mandatory parameter on artConfig: " + str(mandatoryParameters.difference(set(artConfig))) + ".")
  if None in list(artConfig.values()):
    raise ValueError("Blank value on artConfig.")

#-------------------------------- 
def validateMohidConfig(mohidConfig):
  mandatoryParameters = set(['mainPath', 'startDate', 'endDate'])
  if set(mandatoryParameters).issubset(set(mohidConfig)):
    print(":)")
  else:
    raise ValueError("Missing mandatory parameter on MohidConfig: " + str(mandatoryParameters.difference(set(mohidConfig))) + ".")
  if None in list(mohidConfig.values()):
    raise ValueError("Blank value on mohidConfig.")

def validateModel(model):
  mandatoryParameters = set(['mainPath', 'startDate', 'endDate'])
  if set(mandatoryParameters).issubset(set(model)):
    print(":)")
  else:
    raise ValueError("Missing mandatory parameter on Model: " + str(mandatoryParameters.difference(set(model))) + ".")
  if None in list(model.values()):
    raise ValueError("Blank value on Model.")

def validatorYamlFile(yamlDict):
  validateArtConfig(yamlDict['artconfig'])
  validateMohidConfig(yamlDict['Mohid'])
  for model in yamlDict['models']:
    validateModel(model)

def main():
  try:
    cfg = openYamlFile("default.yaml")
    validateArtConfig(cfg['artconfig'])
  except ValueError as e:
    print(e)
    sys.exit()
    

if __name__== "__main__":
  main()