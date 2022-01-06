import subprocess
import mohid.util.file_modifier as file_modifier
import mohid.util.config as cfg


POST_PROCESSING_STRING = "Executing Post Processing module: "

# modifies START and END parameter on .dat files.
def dat_date_change(file_path, logger):
    file_modifier.modify_start_dat_date(file_path, file_modifier.date_to_mohid_date(cfg.current_initial_date), logger)
    file_modifier.modify_end_dat_date(file_path, file_modifier.date_to_mohid_date(cfg.current_final_date), logger)


'''
Function to run post processing blocks. Exe path can be the path to a executable or a shell comand.
If the exe or command need any flags or arguments it can be given in flags parameter in the yaml file.
'''


def execute(yaml, logger):
    # each block has a unique name
    for block in yaml['postProcessing']:
        block_keys = yaml['postProcessing'][block].keys()
        block_dict = yaml['postProcessing'][block]
        if block_dict['run']:

            # Script config file needs to change START and END to the run time
            if 'datDateChange' in block_keys and block_dict['datDateChange']:
                dat_date_change(block_dict['configFilePath'], logger)
            # if the command/executable needs arguments/flags the argument for subprocess.run needs to be a list with
            # every argument separated. example ['ls', 'l'].

            if 'FLAGS' in block_keys:
                # flags are given in a single string, we must create a list with each argument/flag separated
                flags_array = block_dict['FLAGS'].split(" ")
                run_array = [block_dict['exePath']] + flags_array

                if 'outputToFile' in block_keys and block_dict['outputToFile']:
                    with open(block_dict['outputFilePath'], 'w') as log:
                        subprocess.run(run_array, stdout=log, cwd=block_dict['workingDirectory'])
                        log.close()
                else:
                    subprocess.run(run_array, cwd=block_dict['workingDirectory'])

            # First argument of subprocess.run can be just the command/path to executable as there is no need for a
            # list.
            else:
                if 'outputToFile' in block_keys and block_dict['outputToFile']:
                    with open(block_dict['outputFilePath'], 'w') as log:
                        logger.info( + block_dict['EXE_PATH'])
                        subprocess.run(block_dict['EXE_PATH'], stdout=log, cwd=block_dict['WORKING_DIRECTORY'])
                        log.close()
                else:
                    logger.info(POST_PROCESSING_STRING + block_dict['EXE_PATH'])
                    subprocess.run(block_dict['EXE_PATH'], cwd=block_dict['WORKING_DIRECTORY'])
    logger.info("Post Processing finished.")
