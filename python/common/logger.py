import logging


class ArtLogger:
    def __init__(self, name, log_file):
        self.log_file = log_file
        logging.basicConfig(filename=self.log_file,
                            filemode='a',
                            format='%(asctime)s ->  %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(name)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def info(self, message):
        self.logger.info(message)


