from logging import error
import common.yaml.yaml_lib as yaml_lib
import mohid.mohid_water as mohid_water
import mohid.mohid_land as mohid_land
import swan.swan as swan
import ww3.ww3 as ww3
import mohid.util.constants as self
import common.MailClient as mail
import datetime
import os.path
import sys

from pathlib import Path
import common.logger as logger


def open_and_validate_yaml(yaml):
    yaml_file = yaml_lib.open_yaml_file(sys.argv[1])
    # yaml_lib.validate_yaml_file(yaml)
    # yaml_lib.validate_date(yaml)
    #validate_path(yaml_file['ART'][''])

    return yaml_file


def get_log_file(yaml):
    now = datetime.datetime.now()
    now_str = now.strftime("%y-%m-%d_%H%M%S")
    file_path = "ART_" + now_str + ".log"
    folder_path = Path(yaml['ART']['PROJECT_PATH'] + "/Logs")

    if not folder_path.is_dir():
        os.makedirs(folder_path)

    return folder_path / file_path


class ART:
    def __init__(self, yaml):
        self.yaml = yaml
        self.log_path = get_log_file(yaml)
        self.mail = self.initialize_mail(yaml)
        if self.mail is not None:
            self.mail.attachment = self.log_path
        self.logger = logger.ArtLogger("ART", self.log_path)

    def initialize_mail(self, yaml):
        if 'EMAIL_NOTIFICATION' in yaml['ART'].keys() and yaml['ART']['EMAIL_NOTIFICATION']['ENABLE']:
            self.logger.info("Email Notification enabled.")
            self.logger.info("Sending notifications to: " + yaml['ART']['RECEIVERS'])
            return mail.MailClient(yaml['ART']['USER'], yaml['ART']['PASSWORD'], yaml['ART']['RECEIVERS'])

    def execute_module(self):
        try:
            if 'MODULE' in self.yaml['ART'].keys():
                modules = self.yaml['ART']['MODULE']
                if 'MOHID_WATER' in modules and modules['MOHID_WATER']:
                    self.logger.info("Starting MOHID Water module")
                    mohid = mohid_water.MohidWater(self)
                    mohid.execute()
                if 'MOHID_LAND' in modules and modules['MOHID_LAND']:
                    self.logger.info("Starting MOHID Land module")
                    mohid_land.execute(self)
                if 'SWAN' in modules and modules['SWAN']:
                    self.logger.info("Starting Swan module")
                    swan.execute(self)
                if 'WW3' in modules and modules['WW3']:
                    self.logger.info("Starting Wavewatch III module")
                    ww3.execute(self)
            else:
                self.logger.info("Module Keyword not found. Skipping Simulation...")
        except ValueError as e:
            self.logger.error(e.__str__())
            self.error_routine(e)

    def error_routine(self, error):
        if(self.mail != None):
            self.mail.send_not_ok_email(error.__str__())
        self.logger.info("ART IS EXITING WITH AN ERROR.")
        exit(0)

    def exit_routine(self):
        self.logger.info("------------- ART RUN FINISHED -------------")


def validate_path(path):
    return os.path.exists(path)


def main():
    yaml = open_and_validate_yaml(sys.argv[1])

    art = ART(yaml)
    art.execute_module()
    art.exit_routine()


if __name__ == "__main__":
    main()
