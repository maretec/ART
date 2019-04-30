import yaml_lib
import datetime
import logger

logger = logger.ArtLogger("mohid","log.txt")

def validateDate(yaml):
  startDate = datetime.datetime.strptime(yaml['artconfig']['startDate'], '%Y %m %d %H %M %S')
  endDate = datetime.datetime.strptime(yaml['artconfig']['endDate'], '%Y %m %d %H %M %S')
  totalDays = yaml['artconfig']['daysPerRun'] * yaml['artconfig']['numberOfRuns']
  
  if startDate + datetime.timedelta(days= totalDays) > endDate:
    raise ValueError("artconfig: The number of daysPerRun (" + str(yaml['artconfig']['daysPerRun']) + 
    ") in conjunction with the numberOfRuns (" + str(yaml['artconfig']['numberOfRuns']) + ") plus the startDate of this run (" + str(startDate) + 
    ") would lead to a final date of simulation beyond the user-specified endDate (" + str(endDate) + ").")
  else:
    logger.log("all gucci")
  return

def runMohid(yaml):
  validateDate(yaml)
validateDate(yaml_lib.openYamlFile("default.yaml"))
