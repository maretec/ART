import subprocess
import common.file_modifier as file_modifier
import common.config as cfg


def dat_date_change(filePath):
  file_modifier.modify_line(filePath, "START", cfg.current_initial_date)
  file_modifier.modify_line(filePath, "END", cfg.current_final_date)

def execute(yaml):
  
  for block in yaml['postProcessing']:
    block_keys = yaml['postProcessing']['block'].keys()
    block_dict = yaml['postProcessing']['block']
    if block_dict['run']:
      if 'datDataChange' in  block_keys and block_dict['datDataChange']:
        dat_date_change(block_dict['configFilePath'])
      if 'flags' in block_keys:
        flags_array = block_dict['flags'].split(" ") 
        run_array = [block_dict['exePath']] + flags_array
        if 'outputToFile' in block_keys and block_dict['outputToFile']:
          with open(block_dict['outputFilePath'], 'w') as log:
            subprocess.run(run_array, stdout=log)
            log.close()
      else:
        if 'outputToFile' in block_keys and block_dict['outputToFile']:
         with open(block_dict['outputFilePath'], 'w') as log:
            subprocess.run(run_array, stdout=log)
            log.close()
        else:
          subprocess.run(block_dict['exePath'])

  return  