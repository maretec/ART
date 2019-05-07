import yaml_lib
import datetime
import logger
import os.path, subprocess

logger = logger.ArtLogger("mohid","log.txt")


def validate_date(yaml):
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


def validate_path(path):
    return os.path.exists(path)


def running_mode(yaml):
    if not yaml['artconfig']['classiMode']:
        if yaml['artconfig']['forecastMode']:
            today = datetime.datetime.today
            global_initial_date = today + datetime.timedelta(days = yaml['artconfig']['refDayToStart'])
            global_final_date = (today + datetime.timedelta(days = yaml['artconfig']['numberOfRuns'])
                                 + datetime.timedelta(days = yaml['artconfig']['daysPerRun']))

            initial_date = global_initial_date
            final_date = today + datetime.timedelta(days = yaml['artconfig']['daysPerRun'])
        elif not (yaml['artconfig']['forecastMode']):
            startDate = datetime.datetime.strptime(yaml['artconfig']['startDate'], '%Y %m %d %H %M %S')
            endDate = datetime.datetime.strptime(yaml['artconfig']['endDate'], '%Y %m %d %H %M %S')

            difference = endDate - startDate
            numberOfRuns = difference.days
        else:
            raise ValueError("artconfig: forecastMode value needs to be either a number or true/false")
    elif yaml['artconfig']['classicMode']:
        numberOfRuns = 1

        start_date = datetime.datetime.strptime(yaml['artconfig']['startDate'], '%Y %m %d %H %M %S')
        end_date = datetime.datetime.strptime(yaml['artconfig']['endDate'], '%Y %m %d %H %M %S')

        initial_date = start_date
        final_date = end_date
    else:
        raise ValueError("artconfig: classicMode value needs to be either a number or true/false")


def mpi_params(yaml_file):
    mohid = yaml_file['mohid']
    if 'mpi' in mohid.keys():
        if mohid['mpi']['enable']:
            exe_path = mohid['mpi']['exePath']
            keepDecomposedFiles = mohid['mpi']['keepDecomposedFiles']
            ddcParserNumProcessors = mohid['mpi']['ddcComposerNumProcessors']
            joinerVersion = mohid['mpi']['joinerVersion']


def run_mohid(yaml, model):
    validate_date(yaml)
    validate_path(yaml['artconfig']['mainPath'])
    if 'mpi' in yaml['mohid'].keys() and yaml['mohid']['mpi']['enable']:
        mpi = yaml['mohid']['mpi']
        flags = " -n " + str(yaml['mohid']['models'][model]['mpiProcessors']) + " -f /opt/hosts " +\
            yaml['mohid']['exePath']
        logger.log("Starting MOHID MPI run of model: " + yaml['mohid']['models'][model]['name'])
        subprocess.run([mpi['exePath'], flags])
        logger.log("MOHID MPI run finished")
    else:
        logger.log("Starting MOHID run of model " + yaml['mohid']['models'][model]['name'])
        subprocess.run(yaml['mohid']['exePath'])
        logger.log("MOHID run finished")



yaml = yaml_lib.open_yaml_file('default.yaml')
run_mohid(yaml, 'model1')