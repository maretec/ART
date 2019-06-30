# ART

# YAML

---

All parameters values that have text should be surrounded with quotes.

**Example:**
`mainPath: "/ekman1raid/MARPOCS_LasPalmas/"`

## YAML Keywords

### artconfig

- `mainPath` - path to the main project, needs to exist.
- `operationalMode` - if set to `1` it sets ART mode to run as an operational model, it uses the current day on the machine and `refDaytoStart` to calculate the `startDate` and uses `daysPerRun` and `numberOfRuns` to calculate `endDate`.  If set to `0` or non existent it defaults to a single run (using `startDate` and `endDate` parameters instead of calulating them).
- `daysPerRun`
- `refDaytoStart` - reference day relative to current day on the machine. It sets the `startDate` for operationalMode.
- `numberOfRuns`
- `module` - defines which program ART is going to use to calculate the model. Allowed values: `mohid`, `ww3`, `wrf`.
- `runPreProcessing` - if set to `1` it will run all programs defined in the `preProcessing` block. If set to `0` or non existent it will default to not running them.
- `runSimulation`  - if set to `1` it will run the program specified in the `module` parameter. If set to `0` or non existent it will default to not running it.
- `runPostProcessing`  - if set to `1` it will run all programs defined in the `postProcessing` block. If set to `0` or non existent it will default to not running them.
- `startDate` - start date to calculcate model in a non-operational run, ignored if `operationalMode` is set.
- `endDate` - end date to calculcate model in a non-operational run, ignored if `operationalMode` is set.

### mohid

- `maxTime`
- `outputToFile`
- `outputFilePath`
- `exePath`

    ### mpi

    - `enable`
    - `numDomains`
    - `exePath`
    - `keepDecomposedFiles`
    - `ddcParserNumProcessors`
    - `ddcComposerNumProcessors`
    - `joinerVersion`

### model

- `name`
- `path` - path relative to mainPath
- `gridFile`
- `runId`
- `dt`
- `backupPath`
- `storagePath`
- `hasWaterProperties`
- `hasSurfaceHDF`
- `hasGOTM`
- `hasOutputWindow`
- `hasSolutionFromFile`
- `mpiProcessors`

    ### obc

    - `enable`
    - `fromMyOcean`
    - `simulatedDays`
    - `workPath`

    ### meteo

    - `enable`
    - `modelName`
    - `simulatedDays`
    - `fileNameFromModel`
    - `workPath`
