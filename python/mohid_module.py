import yaml_lib
import datetime
import logger
import os.path

logger = logger.ArtLogger("MOHID","log.txt")
DATE_FORMAT = '%Y %m %d %H %M %S'

def validate_date(yaml):
  logger.debug("Validating Dates")
  try:
    startDate = datetime.datetime.strptime(yaml['artconfig']['startDate'], DATE_FORMAT)
    endDate = datetime.datetime.strptime(yaml['artconfig']['endDate'], DATE_FORMAT)
    totalDays = yaml['artconfig']['daysPerRun'] * yaml['artconfig']['numberOfRuns']

    if startDate + datetime.timedelta(days= totalDays) > endDate:
      raise ValueError("artconfig: The number of daysPerRun (" + str(yaml['artconfig']['daysPerRun']) +
                       ") in conjunction with the numberOfRuns (" + str(yaml['artconfig']['numberOfRuns']) + ") plus the startDate of this run (" + str(startDate) +
                       ") would lead to a final date of simulation beyond the user-specified endDate (" + str(endDate) + ").")
    else:
      logger.debug("Date Validation : Success")
  except KeyError:
    logger.warning("Either startDate or endDate were not specified in the configuration file ")
    logger.warning("Will from now on assume that startDate is TODAY and a forecast of 3 days")

  return

def validate_path(path):
  return os.path.exists(path)

def running_mode(yaml):
  if not yaml['artconfig']['classicMode']:
    if yaml['artconfig']['forecastMode']:
      logger.debug("Running in Forecast Mode")
      today = datetime.datetime.today()
      global_initial_date = today + datetime.timedelta(days = yaml['artconfig']['refDayToStart'])
      global_final_date = (today + datetime.timedelta(days = yaml['artconfig']['numberOfRuns'])
                           + datetime.timedelta(days = yaml['artconfig']['daysPerRun'] - 1))

      initial_date = global_initial_date
      final_date = initial_date + datetime.timedelta(days = yaml['artconfig']['daysPerRun'])
      logger.debug("Initial Date : " + initial_date.strftime(DATE_FORMAT))
      logger.debug("Final Date: " + final_date.strftime(DATE_FORMAT))
      logger.debug("Number of runs : " + str(yaml['artconfig']['numberOfRuns']))
    elif not (yaml['artconfig']['forecastMode']):
      try:
        logger.debug("Running in Hindcast Mode")
        global_initial_date = datetime.datetime.strptime(yaml['artconfig']['startDate'], DATE_FORMAT)
        global_final_date = datetime.datetime.strptime(yaml['artconfig']['endDate'], DATE_FORMAT)

        difference = global_final_date - global_initial_date
        numberOfRuns = difference.days
      except KeyError:
        logger.warning("KeyError")
        numberOfRuns = 1
        global_initial_date = datetime.datetime.today()
        global_final_date = global_initial_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
      finally:
        logger.debug("Global Initial Date : " + global_initial_date.strftime(DATE_FORMAT))
        logger.debug("Global Final Date : " + global_final_date.strftime(DATE_FORMAT))
        logger.debug("Number of runs : " + str(numberOfRuns))
    else:
      raise ValueError("artconfig: forecastMode value needs to be either a number or true/false")
  elif yaml['artconfig']['classicMode']:
    logger.debug("Running in Classic Mode")
    numberOfRuns = 1
    try:
      global_initial_date = datetime.datetime.strptime(yaml['artconfig']['startDate'], DATE_FORMAT)
      global_final_date = datetime.datetime.strptime(yaml['artconfig']['endDate'], DATE_FORMAT)
    except KeyError:
      logger.warning("KeyError")
      numberOfRuns = 1
      global_initial_date = datetime.datetime.today()
      global_final_date = global_initial_date + datetime.timedelta(days=yaml['artconfig']['daysPerRun'])
    finally:
      logger.debug("Global Initial Date : " + global_initial_date.strftime(DATE_FORMAT))
      logger.debug("Global Final Date : " + global_final_date.strftime(DATE_FORMAT))
      logger.debug("Number of runs : " + str(numberOfRuns))

  else:
    raise ValueError("artconfig: classicMode value needs to be either a number or true/false")

def run_mohid(yaml):
  validate_date(yaml)
  validate_path(yaml['artconfig']['mainPath'])

yaml = yaml_lib.openYamlFile('../default.yaml')
run_mohid(yaml)
running_mode(yaml)
