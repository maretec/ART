import subprocess
import common.file_modifier as file_modifier
import common.config as cfg
import os
import common.constants as static



def dat_date_change(filePath):
  file_modifier.modify_line(filePath, "START", file_modifier.date_to_mohid_date(cfg.current_initial_date))
  file_modifier.modify_line(filePath, "END", file_modifier.date_to_mohid_date(cfg.current_final_date))

def execute(yaml):
  for block in yaml['preProcessing']:
    block_keys = yaml['preProcessing'][block].keys()
    block_dict = yaml['preProcessing'][block]
    if block_dict['run']:
      if 'datDateChange' in  block_keys and block_dict['datDateChange']:
        dat_date_change(block_dict['configFilePath'])
      if 'flags' in block_keys:
        flags_array = block_dict['flags'].split(" ")
        print(block_dict['flags'])
        run_array = [block_dict['exePath']] + flags_array
        if 'outputToFile' in block_keys and block_dict['outputToFile']:
          with open(block_dict['outputFilePath'], 'w') as log:
            subprocess.run(run_array, stdout=log, cwd=os.path.dirname(block_dict['exePath']))
            log.close()
        else:
          static.logger.info("Executing Pre Processing module: " +  block_dict['exePath'])
          subprocess.run(run_array, cwd=os.path.dirname(block_dict['flags']))
      else:
        if 'outputToFile' in block_keys and block_dict['outputToFile']:
         with open(block_dict['outputFilePath'], 'w') as log:
            static.logger.info("Executing Pre Processing module: " +  block_dict['exePath'])
            subprocess.run(block_dict['exePath'], stdout=log, cwd=os.path.dirname(block_dict['exePath']))
            log.close()
        else:
          static.logger.info("Executing Pre Processing module: " +  block_dict['exePath'])
          subprocess.run(block_dict['exePath'], cwd=os.path.dirname(block_dict['exePath']))

  return  