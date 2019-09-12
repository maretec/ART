# ART

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
- `gridFile` - path for the bathymetry file that will be used in the `IN_BATIM` field of the *nomfich.dat* file. If empty or non defined it will default to use the value already define in the *nomfich.dat* file.
- `dt`
- `storagePath`

### discharges

- `enable`
- `path`
- `dateFormat`

### obc

- `enable`
- `suffix` - defines the suffix of the obc file, it's case sensitive.
- `hasSolutionFromFile` -
- `prefix` - defines the prefix of the obc file, it's case sensitive.
- `dateFormat` - determines the date format for the obc files' names. If not defined it defaults to `YYYYMMDD`.
- `filetype` - file type of the obc file (usually hdf5 or netcdf). When not defined it defaults to `hdf5`.
- `simulatedDays`
- `subFolders` - if set to `1` it searches it assumes that OBC workpath is structured with subfolders for `year` and within those there are subfolders for `month`. If `0` or non defined it defaults to assuming no structure inside OBC workpath.
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
    - `datDateChange` - if the tool has a `START` and `END` based execution set this flag to `1` to make ART change the dates on the configuration of the tool.
    - `configFilePath`
    - `exePath` - mandatory - path to the executable that you want to run before the simutaltion
    - `flags` - any flags or arguments you must give in the command line to the executable

        ex. `ls -l -a /samba/lusitania` → flags: "-l -a /samba/lusitania"

    - `outputToFile`
    - `outputFilePath`

### postprocessing:

- `name of block` - must be unique within the preprocessing block
    - `run`
    - `datDateChange`
    - `configFilePath`
    - `exePath` - mandatory - path to the executable that you want to run after the simutaltion
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
