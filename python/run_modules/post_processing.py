import subprocess
import common.file_modifier as file_modifier
import common.config as cfg
import os
import common.constants as static



def dat_date_change(filePath):
  file_modifier.modify_line(filePath, "START", file_modifier.date_to_mohid_date(cfg.current_initial_date))
  file_modifier.modify_line(filePath, "END", file_modifier.date_to_mohid_date(cfg.current_final_date))

def execute(yaml):
  for block in yaml['postProcessing']:
    block_keys = yaml['postProcessing'][block].keys()
    block_dict = yaml['postProcessing'][block]
    if block_dict['run']:
      if 'datDateChange' in  block_keys and block_dict['datDateChange']:
        dat_date_change(block_dict['configFilePath'])
      if 'flags' in block_keys:
        flags_array = block_dict['flags'].split(" ") 
        run_array = [block_dict['exePath']] + flags_array
        print(run_array)
        if 'outputToFile' in block_keys and block_dict['outputToFile']:
          with open(block_dict['outputFilePath'], 'w') as log:
            subprocess.run(run_array, stdout=log, cwd=block_dict['workingDirectory'])
            log.close()
        else:
          subprocess.run(run_array, cwd=block_dict['workingDirectory'])
      else:
        if 'outputToFile' in block_keys and block_dict['outputToFile']:
         with open(block_dict['outputFilePath'], 'w') as log:
            static.logger.info("Executing Post Processing module: " +  block_dict['exePath'])
            subprocess.run(block_dict['exePath'], stdout=log, cwd=block_dict['workingDirectory'])
            log.close()
        else:
          static.logger.info("Executing Post Processing module: " +  block_dict['exePath'])
          subprocess.run(block_dict['exePath'], cwd=block_dict['workingDirectory'])

  return  