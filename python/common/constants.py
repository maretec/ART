import common.logger as logger
from datetime import datetime

DATE_FORMAT = '%Y %m %d %H %M %S'
DATE_FOLDER_FORMAT = '%Y-%m-%d'

now = datetime.now()
now_str = now.strftime("%y-%m-%d_%H%M%S")

logger = logger.ArtLogger("ART", "ART_" + now_str + ".log")
WRITE_TRIGGER = "WRITE_TRIGGER"
FOLDERS_TO_WATCH = "FOLDERS_TO_WATCH"
TRIGGER_MAX_WAIT = "TRIGGER_MAX_WAIT"
DEFAULT_MAX_WAIT = 6
TRIGGER_POLLING_RATE = "TRIGGER_POLLING_RATE"
DEFAULT_POLLING_RATE = 120
MODEL_TO_CHECK_BACKUP = "MODEL_TO_CHECK_BACKUP"
CHECK_ALL             = True
