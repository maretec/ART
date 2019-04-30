import logging

class ArtLogger:
  def __init__(self, name, logFile):
    self.logFile = logFile
    logging.basicConfig(filename=self.logFile,
                        filemode='a',
                        format='%(asctime)s\t%(name)s\t%(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)
    self.logger = logging.getLogger(name)

  def log(self, message):
    self.logger.debug(message)