import common.yaml_lib as yaml_lib
import run_modules.mohid as mohid
import run_modules.ww3 as ww3
import run_modules.wrf as wrf


def main():
    yaml = yaml_lib.open_yaml_file('../default.yaml')

    # TODO validate sections
    yaml_lib.validate_yaml_file(yaml)

    if yaml['artconfig']['runSimulation']:
        module =  yaml['artconfig']['module']
        if module == "Mohid":
            mohid.execute()
        elif module == "WW3":
            ww3.execute()
        elif module == "WRF":
            wrf.execute()
        else:
            raise ValueError("No valid simulation module given.")


if __name__ == "__main__":
    main()
