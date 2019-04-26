Imports IntrinsicFunctions
Imports Mohid_Base

Public Class Model

    Dim ModelNeedsMeteo As Boolean
    Dim ModelNeedsMeteo2 As Boolean
    Dim ModelNeedsMeteo3 As Boolean
    Dim ModelNeedsOBC As Boolean
    Dim ModelOBCFromMercator As Boolean
    Dim ModelOBCFromMyOcean As Boolean
    Dim ModelName As String
    Dim ModelPath As String
    Dim ModelGridFile As String
    Dim ModelOBCWorkPath As String
    Dim ModelOBCSimulatedDays As Integer
    Dim ModelMeteoSimulatedDays As Integer
    Dim ModelMeteo2SimulatedDays As Integer
    Dim ModelMeteo3SimulatedDays As Integer
    Dim ModelMeteoWorkPath As String
    Dim ModelMeteo2WorkPath As String
    Dim ModelMeteo3WorkPath As String
    Dim ModelMeteoModelName As String
    Dim ModelMeteo2ModelName As String
    Dim ModelMeteo3ModelName As String
    Dim ModelBoundaryFile_Suffix As String
    Dim ModelMeteoFileName_fromModel As Boolean
    Dim ModelMeteo2FileName_fromModel As Boolean
    Dim ModelMeteo3FileName_fromModel As Boolean
    Dim ModelMeteoGenericFileName As Boolean
    Dim ModelMeteo2GenericFileName As Boolean
    Dim ModelMeteo3GenericFileName As Boolean
    Dim ModelRunID As Integer
    Dim ModelTimeStep As Single
    Dim ModelBackUpPath As String
    Dim ModelStoragePath As String
    Dim ModelHasSolutionFromFile As Boolean
    Dim ModelHasWaterProperties As Boolean
    Dim ModelHasLagrangian As Boolean
    Dim ModelHasGOTM As Boolean
    Dim ModelHasVariableDT As Boolean
    Dim ModelMaxDT As Single
    Dim ModelHasAtmosphere As Boolean
    Dim ModelHasInterfaceSedimentWater As Boolean
    Dim ModelHasSurfaceHDF As Boolean
    Dim ModelHasFreeVerticalMovement As Boolean
    Dim ModelHasLife As Boolean
    Dim ModelHasOutputWindow As Boolean
    Dim ModelExportOutputWindow As Boolean
    Dim ModelHasDischarge As Boolean
    Dim ModelHasDischarges As Boolean
    Dim ModelHasDischarges_ets As Boolean
    Dim ModelHasDischarges_srn As Boolean
    Dim ModeletsSimulatedDays As Integer
    Dim ModelsrnSimulatedDays As Integer
    Dim ModelHasWaves As Boolean
    Dim ModelHasHydrodynamics As Boolean = True

    '----------MPI
    Dim ModelMPI_Num_Processors As Integer

    '----------MOHID Land
    Dim ModelHasBasin As Boolean
    Dim ModelHasDrainageNetwork As Boolean
    Dim ModelHasPorousMedia As Boolean
    Dim ModelHasPorousMediaProperties As Boolean
    Dim ModelHasRunoff As Boolean
    Dim ModelHasRunoffProperties As Boolean
    Dim ModelHasVegetation As Boolean
    Dim ModelHasReservoirs As Boolean
    Dim ModelHasIrrigation As Boolean
    '----------MOHID Land

    'WW3
    Dim ModelHasFather As Boolean
    Dim ModelFatherWorkPath As String
    Dim ModelHasCurrents As Boolean
    Dim ModelCurrentsWorkPath As String
    Dim ModelCurrentsModelName As String
    Dim ModelCurrentsSimulatedDays As Integer
    Dim ModelHasWaterLevel As Boolean
    Dim ModelWaterLevelModelName As String
    Dim ModelWaterLevelSimulatedDays As Integer
    Dim ModelWaterLevelWorkPath As String
    Dim ModelDischargesWorkPath As String
    Dim ModelDischarges_ets_WorkPath As String
    Dim ModelDischarges_ets_ModelName As String
    Dim ModelDischarges_srn_WorkPath As String
    Dim ModelDischarges_srn_ModelName As String
    Dim ModelDischargeDatabase As String
    Dim ModelDischargeFile As String
    Dim ModelDischargesList As New Collection
    Dim ModelGatherRestartFiles As Boolean
    Dim ModelOutputWindows As New Collection
    'Dim ModelMeteoFile As String
    'Dim ModelDischargeFiles As Collection
    'Public Property MeteoFile() As String
    '    Get
    '        MeteoFile = Me.ModelMeteoFile
    '    End Get
    '    Set(ByVal value As String)
    '        Me.ModelMeteoFile = value
    '    End Set
    'End Property

    'Public Property DischargeFiles() As Collection
    '    Get
    '        DischargeFiles = Me.ModelDischargeFiles
    '    End Get
    '    Set(ByVal value As Collection)
    '        Me.ModelDischargeFiles = value
    '    End Set
    'End Property
    'WRF
    Dim ModelWRFResultFileName As String
    Public ReadOnly Property Name()
        Get
            Name = Me.ModelName
        End Get
    End Property
    Public ReadOnly Property Path()
        Get
            Path = Me.ModelPath
        End Get
    End Property
    Public ReadOnly Property HasMeteo()
        Get
            HasMeteo = Me.ModelNeedsMeteo
        End Get
    End Property
    Public ReadOnly Property HasMeteo2()
        Get
            HasMeteo2 = Me.ModelNeedsMeteo2
        End Get
    End Property
    Public ReadOnly Property HasMeteo3()
        Get
            HasMeteo3 = Me.ModelNeedsMeteo3
        End Get
    End Property
    Public ReadOnly Property HasOBC()
        Get
            HasOBC = Me.ModelNeedsOBC
        End Get
    End Property
    Public ReadOnly Property GridFile()
        Get
            GridFile = Me.ModelGridFile
        End Get
    End Property
    Public ReadOnly Property OBCWorkPath()
        Get
            OBCWorkPath = Me.ModelOBCWorkPath
        End Get
    End Property
    Public ReadOnly Property OBCFromMercator()
        Get
            OBCFromMercator = Me.ModelOBCFromMercator
        End Get
    End Property
    Public ReadOnly Property OBCFromMyOcean()
        Get
            OBCFromMyOcean = Me.ModelOBCFromMyOcean
        End Get
    End Property
    Public ReadOnly Property OBCSimulatedDays()
        Get
            OBCSimulatedDays = Me.ModelOBCSimulatedDays
        End Get
    End Property
    Public ReadOnly Property MeteoSimulatedDays()
        Get
            MeteoSimulatedDays = Me.ModelMeteoSimulatedDays
        End Get
    End Property
    Public ReadOnly Property Meteo2SimulatedDays()
        Get
            Meteo2SimulatedDays = Me.ModelMeteo2SimulatedDays
        End Get
    End Property
    Public ReadOnly Property Meteo3SimulatedDays()
        Get
            Meteo3SimulatedDays = Me.ModelMeteo3SimulatedDays
        End Get
    End Property
    Public ReadOnly Property BoundaryFile_Suffix()
        Get
            BoundaryFile_Suffix = Me.ModelBoundaryFile_Suffix
        End Get
    End Property

    Public ReadOnly Property MeteoWorkPath()
        Get
            MeteoWorkPath = Me.ModelMeteoWorkPath
        End Get
    End Property
    Public ReadOnly Property Meteo2WorkPath()
        Get
            Meteo2WorkPath = Me.ModelMeteo2WorkPath
        End Get
    End Property
    Public ReadOnly Property Meteo3WorkPath()
        Get
            Meteo3WorkPath = Me.ModelMeteo3WorkPath
        End Get
    End Property
    Public ReadOnly Property MeteoModelName()
        Get
            MeteoModelName = Me.ModelMeteoModelName
        End Get
    End Property
    Public ReadOnly Property Meteo2ModelName()
        Get
            Meteo2ModelName = Me.ModelMeteo2ModelName
        End Get
    End Property
    Public ReadOnly Property Meteo3ModelName()
        Get
            Meteo3ModelName = Me.ModelMeteo3ModelName
        End Get
    End Property
    Public ReadOnly Property CurrentsModelName()
        Get
            CurrentsModelName = Me.ModelCurrentsModelName
        End Get
    End Property
    Public ReadOnly Property WaterLevelModelName()
        Get
            WaterLevelModelName = Me.ModelWaterLevelModelName
        End Get
    End Property
    Public ReadOnly Property MeteoFileName_fromModel()
        Get
            MeteoFileName_fromModel = Me.ModelMeteoFileName_fromModel
        End Get
    End Property
    Public ReadOnly Property Meteo2FileName_fromModel()
        Get
            Meteo2FileName_fromModel = Me.ModelMeteo2FileName_fromModel
        End Get
    End Property
    Public ReadOnly Property Meteo3FileName_fromModel()
        Get
            Meteo3FileName_fromModel = Me.ModelMeteo3FileName_fromModel
        End Get
    End Property
    Public ReadOnly Property MeteoGenericFileName()
        Get
            MeteoGenericFileName = Me.ModelMeteoGenericFileName
        End Get
    End Property
    Public ReadOnly Property Meteo2GenericFileName()
        Get
            Meteo2GenericFileName = Me.ModelMeteo2GenericFileName
        End Get
    End Property
    Public ReadOnly Property Meteo3GenericFileName()
        Get
            Meteo3GenericFileName = Me.ModelMeteo3GenericFileName
        End Get
    End Property
    Public ReadOnly Property RunID()
        Get
            RunID = Me.ModelRunID
        End Get
    End Property
    Public ReadOnly Property TimeStep()
        Get
            TimeStep = Me.ModelTimeStep
        End Get
    End Property
    Public ReadOnly Property BackUpPath()
        Get
            BackUpPath = Me.ModelBackUpPath
        End Get
    End Property
    Public ReadOnly Property StoragePath()
        Get
            StoragePath = Me.ModelStoragePath
        End Get
    End Property
    Public ReadOnly Property HasVariableDT()
        Get
            HasVariableDT = Me.ModelHasVariableDT
        End Get
    End Property
    Public ReadOnly Property MaxDT()
        Get
            MaxDT = Me.ModelMaxDT
        End Get
    End Property
    Public ReadOnly Property HasSolutionFromFile()
        Get
            HasSolutionFromFile = Me.ModelHasSolutionFromFile
        End Get
    End Property
    Public ReadOnly Property HasWaterProperties()
        Get
            HasWaterProperties = Me.ModelHasWaterProperties
        End Get
    End Property
    Public ReadOnly Property HasLagrangian()
        Get
            HasLagrangian = Me.ModelHasLagrangian
        End Get
    End Property
    Public ReadOnly Property HasGOTM()
        Get
            HasGOTM = Me.ModelHasGOTM
        End Get
    End Property
    Public ReadOnly Property HasInterfaceSedimentWater()
        Get
            HasInterfaceSedimentWater = Me.ModelHasInterfaceSedimentWater
        End Get
    End Property
    Public ReadOnly Property HasAtmosphere()
        Get
            HasAtmosphere = Me.ModelHasAtmosphere
        End Get
    End Property

    Public ReadOnly Property HasSurfaceHDF()
        Get
            HasSurfaceHDF = Me.ModelHasSurfaceHDF
        End Get
    End Property

    Public ReadOnly Property HasOutputWindow()
        Get
            HasOutputWindow = Me.ModelHasOutputWindow
        End Get
    End Property

    Public ReadOnly Property ExportOutputWindow()
        Get
            ExportOutputWindow = Me.ModelExportOutputWindow
        End Get
    End Property

    Public ReadOnly Property HasDischarge()
        Get
            HasDischarge = Me.ModelHasDischarge
        End Get
    End Property
    Public ReadOnly Property HasDischarges()
        Get
            HasDischarges = Me.ModelHasDischarges
        End Get
    End Property
    Public ReadOnly Property HasDischarges_ets()
        Get
            HasDischarges_ets = Me.ModelHasDischarges_ets
        End Get
    End Property
    Public ReadOnly Property HasDischarges_srn()
        Get
            HasDischarges_srn = Me.ModelHasDischarges_srn
        End Get
    End Property
    Public ReadOnly Property etsSimulatedDays()
        Get
            etsSimulatedDays = Me.ModeletsSimulatedDays
        End Get
    End Property
    Public ReadOnly Property srnSimulatedDays()
        Get
            srnSimulatedDays = Me.ModelsrnSimulatedDays
        End Get
    End Property
    Public ReadOnly Property HasWaves()
        Get
            HasWaves = Me.ModelHasWaves
        End Get
    End Property
    Public ReadOnly Property HasHydrodynamics()
        Get
            HasHydrodynamics = Me.ModelHasHydrodynamics
        End Get
    End Property
    '---------MOHID Land
    Public ReadOnly Property HasBasin()
        Get
            HasBasin = Me.ModelHasBasin
        End Get
    End Property
    Public ReadOnly Property HasDrainageNetwork()
        Get
            HasDrainageNetwork = Me.ModelHasDrainageNetwork
        End Get
    End Property
    Public ReadOnly Property HasPorousMedia()
        Get
            HasPorousMedia = Me.ModelHasPorousMedia
        End Get
    End Property
    Public ReadOnly Property HasPorousMediaProperties()
        Get
            HasPorousMediaProperties = Me.ModelHasPorousMediaProperties
        End Get
    End Property
    Public ReadOnly Property HasRunoff()
        Get
            HasRunoff = Me.ModelHasRunoff
        End Get
    End Property
    Public ReadOnly Property HasRunoffProperties()
        Get
            HasRunoffProperties = Me.ModelHasRunoffProperties
        End Get
    End Property
    Public ReadOnly Property HasVegetation()
        Get
            HasVegetation = Me.ModelHasVegetation
        End Get
    End Property
    Public ReadOnly Property HasReservoirs()
        Get
            HasReservoirs = Me.ModelHasReservoirs
        End Get
    End Property
    Public ReadOnly Property HasIrrigation()
        Get
            HasIrrigation = Me.ModelHasIrrigation
        End Get
    End Property
    '---------MOHID Land
    '---------MPI
    Public ReadOnly Property MPI_Num_Processors()
        Get
            MPI_Num_Processors = Me.ModelMPI_Num_Processors
        End Get
    End Property

    '---------WW3
    Public ReadOnly Property HasFather()
        Get
            HasFather = Me.ModelHasFather
        End Get
    End Property

    Public ReadOnly Property FatherWorkPath()
        Get
            FatherWorkPath = Me.ModelFatherWorkPath
        End Get
    End Property

    Public ReadOnly Property HasCurrents()
        Get
            HasCurrents = Me.ModelHasCurrents
        End Get
    End Property

    Public ReadOnly Property CurrentsWorkPath()
        Get
            CurrentsWorkPath = Me.ModelCurrentsWorkPath
        End Get
    End Property
    Public ReadOnly Property CurrentsSimulatedDays()
        Get
            CurrentsSimulatedDays = Me.ModelCurrentsSimulatedDays
        End Get
    End Property
    Public ReadOnly Property HasWaterLevel()
        Get
            HasWaterLevel = Me.ModelHasWaterLevel
        End Get
    End Property
    Public ReadOnly Property WaterLevelWorkPath()
        Get
            WaterLevelWorkPath = Me.ModelWaterLevelWorkPath
        End Get
    End Property
    Public ReadOnly Property WaterLevelSimulatedDays()
        Get
            WaterLevelSimulatedDays = Me.ModelWaterLevelSimulatedDays
        End Get
    End Property
    '---------WW3
    Public ReadOnly Property DischargesWorkPath()
        Get
            DischargesWorkPath = Me.ModelDischargesWorkPath
        End Get
    End Property
    Public ReadOnly Property Discharges_ets_WorkPath()
        Get
            Discharges_ets_WorkPath = Me.ModelDischarges_ets_WorkPath
        End Get
    End Property
    Public ReadOnly Property Discharges_ets_ModelName()
        Get
            Discharges_ets_ModelName = Me.ModelDischarges_ets_ModelName
        End Get
    End Property
    Public ReadOnly Property Discharges_srn_WorkPath()
        Get
            Discharges_srn_WorkPath = Me.ModelDischarges_srn_WorkPath
        End Get
    End Property
    Public ReadOnly Property Discharges_srn_ModelName()
        Get
            Discharges_srn_ModelName = Me.ModelDischarges_srn_ModelName
        End Get
    End Property


    Public ReadOnly Property DischargeDatabase()
        Get
            DischargeDatabase = Me.ModelDischargeDatabase
        End Get
    End Property
    Public ReadOnly Property DischargeFile()
        Get
            DischargeFile = Me.ModelDischargeFile
        End Get
    End Property

    Public ReadOnly Property DichargesList()
        Get
            DichargesList = Me.ModelDischargesList
        End Get
    End Property

    Public ReadOnly Property GatherRestartFiles()
        Get
            GatherRestartFiles = Me.ModelGatherRestartFiles
        End Get
    End Property

    Public ReadOnly Property ExportWindows()
        Get
            ExportWindows = Me.ModelOutputWindows
        End Get
    End Property

    Public ReadOnly Property WRFResultFileName()
        Get
            WRFResultFileName = Me.ModelWRFResultFileName
        End Get
    End Property

    Public Sub LoadData(ByVal ProjectFile As EnterData)
        ProjectFile.GetDataStr("NAME", Me.ModelName, EnterData.FromBlock)
        ProjectFile.GetDataStr("PATH", Me.ModelPath, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_OBC", Me.ModelNeedsOBC, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_SOLUTION_FROM_FILE", Me.ModelHasSolutionFromFile, EnterData.FromBlock)
        If Me.ModelNeedsOBC Then
            ProjectFile.GetDataLog("OBC_FROM_MERCATOR", Me.ModelOBCFromMercator, EnterData.FromBlock)
            ProjectFile.GetDataLog("OBC_FROM_MYOCEAN", Me.ModelOBCFromMyOcean, EnterData.FromBlock)
            ProjectFile.GetDataStr("OBC_WORK_PATH", Me.ModelOBCWorkPath, EnterData.FromBlock)
            Dim intKeyword As Integer = -99
            ProjectFile.GetDataInteger("OBC_SIMULATED_DAYS", intKeyword, EnterData.FromBlock)
            If intKeyword <= 0 Then
                Me.ModelOBCSimulatedDays = 3
            Else
                Me.ModelOBCSimulatedDays = intKeyword
            End If
            ProjectFile.GetDataStr("HDFREAD_SUFFIX", Me.ModelBoundaryFile_Suffix, EnterData.FromBlock)
            If Me.ModelBoundaryFile_Suffix = "" Then Me.ModelBoundaryFile_Suffix = "_w1"
        Else
            If Me.ModelHasSolutionFromFile Then
                ProjectFile.GetDataStr("IMPOSED_SOLUTION_WORK_PATH", Me.ModelOBCWorkPath, EnterData.FromBlock)
                Dim intKeyword As Integer = -99
                ProjectFile.GetDataInteger("IMPOSED_SOLUTION_SIMULATED_DAYS", intKeyword, EnterData.FromBlock)
                If intKeyword <= 0 Then
                    Me.ModelOBCSimulatedDays = 3
                Else
                    Me.ModelOBCSimulatedDays = intKeyword
                End If
                ProjectFile.GetDataStr("HDFREAD_SUFFIX", Me.ModelBoundaryFile_Suffix, EnterData.FromBlock)
                If Me.ModelBoundaryFile_Suffix = "" Then Me.ModelBoundaryFile_Suffix = ""
            End If
        End If
        ProjectFile.GetDataLog("MODEL_HAS_METEO", Me.ModelNeedsMeteo, EnterData.FromBlock)
        If Me.ModelNeedsMeteo Then
            ProjectFile.GetDataStr("METEO_WORK_PATH", Me.ModelMeteoWorkPath, EnterData.FromBlock)
            ProjectFile.GetDataStr("METEO_MODEL_NAME", Me.ModelMeteoModelName, EnterData.FromBlock)

            If Me.ModelMeteoModelName = "" Then
                If InStr(Me.ModelMeteoWorkPath, "WRF") > 0 Then
                    Me.ModelMeteoModelName = "WRF"
                ElseIf InStr(Me.ModelMeteoWorkPath, "MM5") > 0 Then
                    Me.ModelMeteoModelName = "MM5"
                ElseIf InStr(Me.ModelMeteoWorkPath, "GFS") > 0 Then
                    Me.ModelMeteoModelName = "GFS"
                End If
            End If

            ProjectFile.GetDataLog("METEO_GENERIC_FILENAME", Me.ModelMeteoGenericFileName, EnterData.FromBlock)


            Dim bolKeyword As Boolean = False
            ProjectFile.GetDataLog("METEO_FILENAME_FROM_MODEL", bolKeyword, EnterData.FromBlock)
            Me.ModelMeteoFileName_fromModel = bolKeyword

            Dim intKeyword As Integer = -99

            ProjectFile.GetDataInteger("METEO_SIMULATED_DAYS", intKeyword, EnterData.FromBlock)
            If intKeyword <= 0 Then
                Me.ModelMeteoSimulatedDays = -99
            Else
                Me.ModelMeteoSimulatedDays = intKeyword
            End If
        End If
        ProjectFile.GetDataLog("MODEL_HAS_METEO2", Me.ModelNeedsMeteo2, EnterData.FromBlock)
        If Me.ModelNeedsMeteo2 Then
            ProjectFile.GetDataStr("METEO2_WORK_PATH", Me.ModelMeteo2WorkPath, EnterData.FromBlock)
            ProjectFile.GetDataStr("METEO2_MODEL_NAME", Me.ModelMeteo2ModelName, EnterData.FromBlock)
            Dim bolKeyword As Boolean = False
            ProjectFile.GetDataLog("METEO2_FILENAME_FROM_MODEL", bolKeyword, EnterData.FromBlock)
            Me.ModelMeteo2FileName_fromModel = bolKeyword

            Dim intKeyword As Integer = -99

            ProjectFile.GetDataLog("METEO2_GENERIC_FILENAME", Me.ModelMeteo2GenericFileName, EnterData.FromBlock)

            ProjectFile.GetDataInteger("METEO2_SIMULATED_DAYS", intKeyword, EnterData.FromBlock)
            If intKeyword <= 0 Then
                Me.ModelMeteo2SimulatedDays = -99
            Else
                Me.ModelMeteo2SimulatedDays = intKeyword
            End If
        End If
        ProjectFile.GetDataLog("MODEL_HAS_METEO3", Me.ModelNeedsMeteo3, EnterData.FromBlock)
        If Me.ModelNeedsMeteo3 Then
            ProjectFile.GetDataStr("METEO3_WORK_PATH", Me.ModelMeteo3WorkPath, EnterData.FromBlock)
            ProjectFile.GetDataStr("METEO3_MODEL_NAME", Me.ModelMeteo3ModelName, EnterData.FromBlock)
            Dim bolKeyword As Boolean = False
            ProjectFile.GetDataLog("METEO3_FILENAME_FROM_MODEL", bolKeyword, EnterData.FromBlock)
            Me.ModelMeteo3FileName_fromModel = bolKeyword

            Dim intKeyword As Integer = -99

            ProjectFile.GetDataLog("METEO3_GENERIC_FILENAME", Me.ModelMeteo3GenericFileName, EnterData.FromBlock)

            ProjectFile.GetDataInteger("METEO3_SIMULATED_DAYS", intKeyword, EnterData.FromBlock)
            If intKeyword <= 0 Then
                Me.ModelMeteo3SimulatedDays = -99
            Else
                Me.ModelMeteo3SimulatedDays = intKeyword
            End If
        End If
        ProjectFile.GetDataStr("GRID_FILE", Me.ModelGridFile, EnterData.FromBlock)
        ProjectFile.GetDataInteger("MODEL_RUN_ID", Me.ModelRunID, EnterData.FromBlock)
        ProjectFile.GetDataLog("VARIABLE_DT", Me.ModelHasVariableDT, EnterData.FromBlock)
        If Me.ModelHasVariableDT Then
            ProjectFile.GetDataReal("MAXDT", Me.ModelMaxDT, EnterData.FromBlock)
        End If
        ProjectFile.GetDataReal("DT", Me.ModelTimeStep, EnterData.FromBlock)
        ProjectFile.GetDataStr("BACKUP_PATH", Me.ModelBackUpPath, EnterData.FromBlock)
        ProjectFile.GetDataStr("STORAGE_PATH", Me.ModelStoragePath, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_HYDRODYNAMICS", Me.ModelHasHydrodynamics, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_WATERPROPERTIES", Me.ModelHasWaterProperties, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_ATMOSPHERE", Me.ModelHasAtmosphere, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_LAGRANGIAN", Me.ModelHasLagrangian, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_GOTM", Me.ModelHasGOTM, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_INTERFACESEDIMENTWATER", Me.ModelHasInterfaceSedimentWater, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_SURFACE_HDF", Me.ModelHasSurfaceHDF, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_OUTPUT_WINDOW", Me.ModelHasOutputWindow, EnterData.FromBlock)
        If Me.ModelHasOutputWindow Then
            '            ProjectFile.GetDataLog("MODEL_EXPORT_OUTPUT_WINDOW", Me.ModelExportOutputWindow, EnterData.FromBlock)
        End If
        ProjectFile.GetDataLog("MODEL_HAS_DISCHARGES", Me.ModelHasDischarges, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_DISCHARGES_ETS", Me.ModelHasDischarges_ets, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_DISCHARGES_SRN", Me.ModelHasDischarges_srn, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_WAVES", Me.ModelHasWaves, EnterData.FromBlock)

        '----------------MPI
        ProjectFile.GetDataInteger("MPI_NUM_PROCESSORS", Me.ModelMPI_Num_Processors, EnterData.FromBlock)

        '----------------MOHID LAND
        ProjectFile.GetDataLog("MODEL_HAS_BASIN", Me.ModelHasBasin, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_DRAINAGE_NETWORK", Me.ModelHasDrainageNetwork, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_POROUS_MEDIA", Me.ModelHasPorousMedia, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_POROUS_MEDIA_PROPERTIES", Me.ModelHasPorousMediaProperties, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_RUNOFF", Me.ModelHasRunoff, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_RUNOFF_PROPERTIES", Me.ModelHasRunoffProperties, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_VEGETATION", Me.ModelHasVegetation, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_RESERVOIRS", Me.ModelHasReservoirs, EnterData.FromBlock)
        ProjectFile.GetDataLog("MODEL_HAS_IRRIGATION", Me.ModelHasIrrigation, EnterData.FromBlock)
        '----------------MOHID LAND

        '----------------WW3
        ProjectFile.GetDataLog("MODEL_HAS_FATHER", Me.ModelHasFather, EnterData.FromBlock)
        If Me.ModelHasFather = True Then
            ProjectFile.GetDataStr("MODEL_FATHER_WORK_PATH", Me.ModelFatherWorkPath, EnterData.FromBlock)
            ProjectFile.GetDataStr("MODEL_FATHER_ID", Me.ModelBoundaryFile_Suffix, EnterData.FromBlock)
        End If
        ProjectFile.GetDataLog("MODEL_HAS_CURRENTS", Me.ModelHasCurrents, EnterData.FromBlock)
        If Me.ModelHasCurrents = True Then

            ProjectFile.GetDataStr("CURRENTS_WORK_PATH", Me.ModelCurrentsWorkPath, EnterData.FromBlock)
            ProjectFile.GetDataStr("CURRENTS_MODEL_NAME", Me.ModelCurrentsModelName, EnterData.FromBlock)
            ProjectFile.GetDataStr("CURRENTS_SIMULATED_DAYS", Me.ModelCurrentsSimulatedDays, EnterData.FromBlock)

        End If
        ProjectFile.GetDataLog("MODEL_HAS_WATERLEVEL", Me.ModelHasWaterLevel, EnterData.FromBlock)
        If Me.ModelHasWaterLevel = True Then
            ProjectFile.GetDataStr("WATERLEVEL_WORK_PATH", Me.ModelWaterLevelWorkPath, EnterData.FromBlock)
            ProjectFile.GetDataStr("WATERLEVEL_MODEL_NAME", Me.ModelWaterLevelModelName, EnterData.FromBlock)
            ProjectFile.GetDataStr("WATERLEVEL_SIMULATED_DAYS", Me.ModelWaterLevelSimulatedDays, EnterData.FromBlock)
        End If
        '----------------WW3

        '----------------WRF

        ''----------------WRF
        'If Run_WRF = True Then
        '    Dim ModelIDString As String = Me.ModelRunID.ToString("00")
        '    Me.ModelWRFResultFileName = "wrfout_d" + ModelIDString + "_" + InitialDate.ToString("yyyy-MM-dd_HH" + "" + "mm" + "" + "ss")

        'End If

        If Me.ModelHasDischarges Then
            ProjectFile.GetDataStr("DISCHARGES_WORK_PATH", Me.ModelDischargesWorkPath, EnterData.FromBlock)
        End If
        If Me.ModelHasDischarges_ets Then
            ProjectFile.GetDataStr("DISCHARGES_ETS_WORK_PATH", Me.ModelDischarges_ets_WorkPath, EnterData.FromBlock)
            ProjectFile.GetDataStr("DISCHARGES_ETS_MODEL_NAME", Me.ModelDischarges_ets_ModelName, EnterData.FromBlock)
            Dim intKeyword As Integer = -99
            ProjectFile.GetDataInteger("ETS_SIMULATED_DAYS", intKeyword, EnterData.FromBlock)
            If intKeyword <= 0 Then
                Me.ModeletsSimulatedDays = 3
            Else
                Me.ModeletsSimulatedDays = intKeyword
            End If
        End If
        If Me.ModelHasDischarges_srn Then
            ProjectFile.GetDataStr("DISCHARGES_SRN_WORK_PATH", Me.ModelDischarges_srn_WorkPath, EnterData.FromBlock)
            ProjectFile.GetDataStr("DISCHARGES_SRN_MODEL_NAME", Me.ModelDischarges_srn_ModelName, EnterData.FromBlock)
            Dim intKeyword As Integer = -99
            ProjectFile.GetDataInteger("SRN_SIMULATED_DAYS", intKeyword, EnterData.FromBlock)
            If intKeyword <= 0 Then
                Me.ModelsrnSimulatedDays = 3
            Else
                Me.ModelsrnSimulatedDays = intKeyword
            End If
        End If
        ProjectFile.GetDataLog("MODEL_HAS_DISCHARGE", Me.ModelHasDischarge, EnterData.FromBlock)
        ProjectFile.GetDataStr("DISCHARGE_DATABASE", Me.ModelDischargeDatabase, EnterData.FromBlock)
        ProjectFile.GetDataStr("DISCHARGE_FILE", Me.ModelDischargeFile, EnterData.FromBlock)

        Me.ModelGatherRestartFiles = True
        ProjectFile.GetDataLog("GATHER_RESTART_FILES", Me.ModelGatherRestartFiles, EnterData.FromBlock)

        'If Me.ModelHasDischarges Then
        '    ProjectFile.GetDataStr("DISCHARGES_CONFIG_FILE", Me.ModelDischargesConfigFile, EnterData.FromBlock)
        '    'Call Read_Discharges_List(ProjectFile)

        '    Call Read_Discharges_List(DischargesConfigFile)
        'End If




    End Sub

    Public Sub SetWRFResultFileName()
        '----------------WRF
        If Run_WRF = True Then
            Dim ModelIDString As String = Me.ModelRunID.ToString("00")
            Me.ModelWRFResultFileName = "wrfout_d" + ModelIDString + "_" + InitialDate.ToString("yyyy-MM-dd_HH" + "" + "mm" + "" + "ss")

        End If

    End Sub

    Private Sub Read_ExportOutputWindow_List(ByVal File As EnterData)


    End Sub
    Public Sub Read_Discharges_List(ByVal DischargesConfigFilename As String)

        Dim BlockFound As Boolean = False
        Dim StartLine, EndLine, ListSize, i, iLine As Integer

        Dim DischargesConfigFile As String = System.IO.Path.Combine(Me.DischargesWorkPath, DischargesConfigFilename)
        Dim File As New EnterData(DischargesConfigFile)

        'Extracts first block
        File.ExtractBlockFromBuffer("<BeginTimeSerieConfig>", "<EndTimeSerieConfig>", BlockFound)

        If Not BlockFound Then
            UnSuccessfullEnd("No timeseries found in discharge config file: " + File.ToString)
        End If

        Dim filename, folder, fullname As String
        Do While BlockFound
            If BlockFound Then
                filename = ""
                folder = ""
                fullname = ""
                File.GetDataStr("OUTPUT_FILENAME", filename, EnterData.FromBlock)
                'File.GetDataStr("OUTPUT_FOLDER", folder, EnterData.FromBlock)
                'fullname = System.IO.Path.Combine(folder, filename)
                'If fullname = "" Then
                '    Call UnSuccessfullEnd("No output file defined for discharge in discharge config file: " + File.ToString)
                'End If

                Me.ModelDischargesList.Add(filename)

            End If
            File.ExtractBlockFromBuffer("<BeginTimeSerieConfig>", "<EndTimeSerieConfig>", BlockFound)
        Loop

    End Sub
    'Public Sub Read_Discharges_List_(ByVal File As EnterData)
    '    Dim BlockFound As Boolean = False
    '    Dim StartLine, EndLine, ListSize, i, iLine As Integer

    '    File.ExtractBlockFromBlock("<<begin_discharges_list>>", "<<end_discharges_list>>", BlockFound)
    '    If BlockFound Then
    '        File.GetReadingLimits(StartLine, EndLine, EnterData.FromBlockFromBlock)

    '        ListSize = EndLine - StartLine - 2

    '        ReDim DischargesList(ListSize)
    '        i = 0
    '        For iLine = StartLine + 1 To EndLine - 1
    '            File.GetFullLine(iLine, DischargesList(i))
    '            i = i + 1
    '        Next
    '        If DischargesList.Length = 0 Then
    '            ' erro
    '            Call UnSuccessfullEnd("No files defined for discharges.")
    '        End If
    '    Else
    '        ' erro
    '        Call UnSuccessfullEnd("No files defined for discharges (Block <<begin_discharges_list>> / <<end_discharges_list>> is missing")

    '    End If
    'End Sub

End Class
