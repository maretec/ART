# ART

[Roadmap](https://www.notion.so/ad599eeba2794af4b7fd8d736d37ff5a)

# YAML

---

All parameters values that have text should be surrounded with quotes.
****`mainPath: "/ekman1raid/MARPOCS_LasPalmas/"`

All paths to folders should end on a dash.                                                                    `mainPath: "/ekman1raid/MARPOCS_LasPalmas/"`

## YAML Keywords

### artconfig

- `mainPath` - MANDATORY - path to the main project, needs to exist.
- `operationalMode` - if set to `1` it sets ART mode to run as an operational model, it uses the current day on the machine and `refDaytoStart` to calculate the `startDate` and uses `daysPerRun` and `numberOfRuns` to calculate `endDate`.  If set to `0` or non existent it defaults to a single run (using `startDate` and `endDate` parameters instead of calulating them).
- `runPreProcessing` - if set to `1` it will run all programs defined in the `preProcessing` block. If set to `0` or non existent it will default to not running them.
- `daysPerRun`
- `refDaytoStart` - reference day relative to current day on the machine. It sets the `startDate` for operationalMode.
- `numberOfRuns`
- `module` - defines which program ART is going to use to calculate the model. Allowed values: `mohid`, `ww3`, `wrf`.
- `runSimulation`  - if set to `1` it will run the program specified in the `module` parameter. If set to `0` or non existent it will default to not running it.
- `runSimulation`  - if set to `1` it will run all programs defined in the `postProcessing` block. If set to `0` or non existent it will default to not running them.
- `startDate` - start date to calculcate model in a non-operational run, ignored if `operationalMode` is set.
- `endDate` - end date to calculcate model in a non-operational run, ignored if `operationalMode` is set.
- `outputToFile` - if set to `1` it will redirect the output of the console (ART) to a file specified by `outputFilePath` parameter. If `0` or non existent it will only output to the console where it is running.bh
- `outputFilePath` - specifies the file path for which ART will output. If non existent and `outputFile` is set to `1` it will default to the path where ART is running.
- `sendEmail` - if set to 1 it will enable sending emails upon the completion of MOHID runs. If 0 it disables that option.
- `email` - list of strings that specify the address(es) of the person the email is sent to. If `sendEmail` is set to 1, it has to exist, and it has to be non-empty.

### mohid

- `maxTime` - maximum time allowed for MOHID to run, if non existent it will default to `40000`.
- `exePath` - MANDATORY - specifies the path to where the MOHID execution file is.

    `outputToFile` - if set to `1` it will redirect the output of MOHID to a file specified by `outputFilePath` parameter. If `0` or non existent it will only output to the console where it is running.

    `outputFilePath` - specifies the file path for which MOHID will output. If non existent and `outputFile` is set to `1` it will default to the path where MOHID is running.

    ### mpi

    - `enable` - if set to `1` it will enable MPI on current run. If `0` or non existent it will default to ignore all the `mpi` block
    - `exePath` - MANDATORY IF `enable`- specifies the path to where the MOHID execution file is.
    - `totalProcessors` - number of total processors cores that mpi will use

### model

- `name`
- `path` - path relative to mainPath
- `dt`
- `storagePath`
- `resultsList` - defined as a list `['Hydrodynamic_surface', 'WaterProperties']`. When used makes so that the Backup of the results is only made if the file name is in the list. If this parameter is not present the behavior will default to backup all files.
- `hasSolutionFromFile`

### discharges

- `enable`
- `path`
- `dateFormat`

### obc

- `enable`
- `fileType` - file type of the obc file (usually hdf5 or netcdf). When not defined it defaults to `hdf5`.
- `simulatedDays`
- `subFolders` - if set to `1` it searches it assumes that OBC workpath is structured with subfolders for `year` if set to `2` it has subfolders `month` and `year` and if set to `3` it has `year` , `month`, and `day`. If `0` or non defined it defaults to assuming no structure inside OBC workpath.
- `dateInFileName` -  if set to `1` assumes date is in the files' names (uses `dateFormat`). If `0` or non defined it defaults to not having date on the obc files.
- `dateFormat` - determines the date format for the obc files' names. If not defined it defaults to `YYYYMMDD`
- `files` - list of files you want from the OBC workpath `['Hydrodynamic', 'WaterProperties']` it can be costumized with date variables `%Yi, %Mi, %di` for initial year, initial month and initial day and also  `%Yf, %Mf, %df` for final year, final month and final day.

    Example:
    `['Hydrodynamic_%Yi-%Mi-%di']` will become `Hydrodynamic_2019-09-12`.

- `workPath`

### meteo

- `enable`

    ### models

       uniqueId

    - `name`
    - `simulatedDays`
    - `fileNameFromModel`
    - `workPath`
    - `dateFormat`
    - `fileType`

### model.dat

Arguments used here will be put or changed in the model.dat of its domain.

- `MAXDT`
- `GMTREFERENCE`
- `DT_PREDICTION_INTERVAL`

### preprocessing:

- `name of block` - must be unique within the preprocessing block
    - `run`
    - `workingDirectory` - sets the workingDirectory of the Pre Processing tool the one desired.
    - `datDateChange` - if the .dat of the script needs to change it START and END set this parameter to `1` and define `configFilePath`.
    - `configFilePath` - path to where the .dat file is. Only necessary when `datDateChange` is enabled.
    - `exePath` - mandatory - path to the executable that you want to run before the simutaltion
    - `flags` - any flags or arguments you must give in the command line to the executable

        ex. `ls -l -a /samba/lusitania` → flags: "-l -a /samba/lusitania"

    - `outputToFile`
    - `outputFilePath`

### postprocessing:

- `name of block` - must be unique within the preprocessing block
    - `run`
    - `workingDirectory` - sets the workingDirectory of the postProcessing tool the one desired.
    - `datDateChange` - if the .dat of the script needs to change it START and END set this parameter to `1` and define `configFilePath`.
    - `configFilePath` - path to where the .dat file is. Only necessary when `datDateChange` is enabled.
    - `exePath` - mandatory - path to the executable that you want to run after the simutaltion. Can also be used to run a shell command such as `ls`. If you want to run a script such as `flags` parameter.
        - Example: `exePath` : `python3` ; `flags` :`/pathToScript/script.py`
    - `flags` - any flags or arguments you must give in the command line to the executable

        ex. `ls -l -a /samba/lusitania` → flags: "-l -a /samba/lusitania"

    - `outputToFile`
    - `outputFilePath`

# MOHID Keywords (nomfich.dat)

---

### Common

- `ROOT`
- `ROOT_SRT`
- `SURF_DAT`
- `SURF_HDF`
- `DOMAIN`
- `WQDATA`
- MOHIDWater
    - `IN_BATIM`
    - `AIRW_DAT`
    - `AIRW_HDF`
    - `AIRW_FIN`
    - `AIRW_INI`
    - `BOT_DAT`
    - `BOT_HDF`
    - `BOT_FIN`
    - `BOT_INI`
    - `IN_DAD3D`
    - `OUT_DESF`
    - `OUT_FIN`
    - `IN_CNDI`
    - `IN_TURB`
    - `TURB_HDF`
    - `DISPQUAL`
    - `EUL_HDF`
    - `EUL_FIN`
    - `EUL_INI`
    - `PARTIC_DATA`
    - `PARTIC_HDF`
    - `PARTIC_FIN`
    - `PARTIC_INI`
    - `FREE_DAT`
    - `DISCHARG`
    - `BENTHOS_DATA`
    - `ASSIMILA_DAT`
    - `ASSIMILA_HDF`
    - `TURBO_GOTM`
    - `TURBO_FIN`
    - `TURBO_INI`
- MOHIDLand
    - `IN_BASIN`
    - `BASIN_DATA`
    - `BASIN_HDF`
    - `BASIN_FIN`
    - `BASIN_INI`
    - `BASIN_GEOMETRY`
    - `DRAINAGE_NETWORK`
    - `DRAINAGE_NETWORK_HDF`
    - `DRAINAGE_NETWORK_FIN`
    - `DRAINAGE_NETWORK_INI`
    - `POROUS_DATA`
    - `POROUS_HDF`
    - `POROUS_FIN`
    - `POROUS_INI`
    - `POROUS_ASC`
    - `RUNOFF_DATA`
    - `RUNOFF_HDF`
    - `RUNOFF_FIN`
    - `RUNOFF_INI`
    - `VEGETATION_DATA`
    - `VEGETATION_HDF`
    - `VEGETATION_FIN`
    - `VEGETATION_INI`
    - `RUNOFF_PROP_DATA`
    - `RUNOFF_PROP_HDF`
    - `RUNOFF_PROP_FIN`
    - `RUNOFF_PROP_INI`
    - `POROUS_PROP_DATA`
    - `POROUS_PROP_HDF`
    - `POROUS_PROP_FIN`
    - `POROUS_PROP_INI`
    - `SQ_DATA`
    - `DT_LOG`

[To-do's](https://www.notion.so/e2714efe0cca4d449fdf953c6c207cfc)
