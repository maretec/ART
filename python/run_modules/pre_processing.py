import subprocess
import common.file_modifier as file_modifier
import common.config as cfg
import os
import common.constants as static



def dat_date_change(filePath):
  file_modifier.modify_line(filePath, "START", file_modifier.date_to_mohid_date(cfg.current_initial_date))
  file_modifier.modify_line(filePath, "END", file_modifier.date_to_mohid_date(cfg.current_final_date))

def execute(yaml):
  for block in yaml['PREPROCESSING']:
    block_keys = yaml['PREPROCESSING'][block].keys()
    block_dict = yaml['PREPROCESSING'][block]
    if 'RUN' in block_keys and block_dict['RUN']:
      if 'DAT_DATE_CHANGE' in  block_keys and block_dict['DAT_DATE_CHANGE']:
        dat_date_change(block_dict['CONFIG_FILEPATH'])
      if 'FLAGS' in block_keys:
        flags_array = block_dict['FLAGS'].split(" ")
        print(block_dict['FLAGS'])
        run_array = [block_dict['EXE_PATH']] + flags_array
        if 'OUTPUT_TO_FILE' in block_keys and block_dict['OUPUT_TO_FILE']:
          with open(block_dict['OUTPUT_FILEPATH'], 'w') as log:
            subprocess.run(run_array, stdout=log, cwd=os.path.dirname(block_dict['EXE_PATH']))
            log.close()
        else:
          static.logger.info("Executing Pre Processing module: " +  block_dict['EXE_PATH'])
          subprocess.run(run_array, cwd=os.path.dirname(block_dict['FLAGS']))
      else:
        if 'OUTPUT_TO_FILE' in block_keys and block_dict['OUTPUT_TO_FILE']:
         with open(block_dict['OUTPUT_FILEPATH'], 'w') as log:
            static.logger.info("Executing Pre Processing module: " +  block_dict['EXE_PATH'])
            subprocess.run(block_dict['EXE_PATH'], stdout=log, cwd=os.path.dirname(block_dict['EXE_PATH']))
            log.close()
        else:
          static.logger.info("Executing Pre Processing module: " +  block_dict['EXE_PATH'])
          subprocess.run(block_dict['EXE_PATH'], cwd=os.path.dirname(block_dict['EXE_PATH']))

  return  