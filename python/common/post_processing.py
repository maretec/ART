import subprocess
import mohid.util.file_modifier as file_modifier
import os
from pathlib import Path

PRE_PROCESSING_STRING = "Executing Post Processing module: "

def dat_date_change(file_path, logger, current_initial_date, current_final_date):
    file_modifier.modify_start_dat_date(file_path, file_modifier.date_to_mohid_date(current_initial_date), logger)
    file_modifier.modify_end_dat_date(file_path, file_modifier.date_to_mohid_date(current_final_date), logger)


def execute(yaml, logger, current_initial_date, current_final_date):
    for block in yaml['POSTPROCESSING']:
        block_keys = yaml['POSTPROCESSING'][block].keys()
        block_dict = yaml['POSTPROCESSING'][block]
        if 'RUN' in block_keys and block_dict['RUN']:
            if 'DAT_DATE_CHANGE' in block_keys and block_dict['DAT_DATE_CHANGE']:
                dat_date_change(Path(block_dict['CONFIG_FILEPATH']), logger, current_initial_date, current_final_date)
            if 'FLAGS' in block_keys:
                flags_array = block_dict['FLAGS'].split(" ")
                print(block_dict['FLAGS'])
                run_array = [block_dict['EXE_PATH']] + flags_array
                if 'OUTPUT_TO_FILE' in block_keys and block_dict['OUTPUT_TO_FILE']:
                    with open(block_dict['OUTPUT_FILEPATH'], 'w') as log:
                        subprocess.run(run_array, stdout=log, cwd=os.path.dirname(block_dict['EXE_PATH']))
                        log.close()
                else:
                    logger.info(PRE_PROCESSING_STRING + block_dict['EXE_PATH'])
                    subprocess.run(run_array, cwd=os.path.dirname(block_dict['FLAGS']))
            else:
                if 'OUTPUT_TO_FILE' in block_keys and block_dict['OUTPUT_TO_FILE']:
                    with open(block_dict['OUTPUT_FILEPATH'], 'w') as log:
                        logger.info(PRE_PROCESSING_STRING + block_dict['EXE_PATH'])
                        subprocess.run(block_dict['EXE_PATH'], stdout=log, cwd=os.path.dirname(block_dict['EXE_PATH']))
                        log.close()
                else:
                    logger.info(PRE_PROCESSING_STRING + block_dict['EXE_PATH'])
                    subprocess.run(block_dict['EXE_PATH'], cwd=os.path.dirname(block_dict['EXE_PATH']))

    return
