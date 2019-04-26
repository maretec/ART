Imports Mohid_Base

Public Class PostProcessor
    Dim PostProcessor_Name As String
    Dim PostProcessor_Exe As String
    Dim PostProcessor_InputFile As String
    Dim Postprocessor_MaxTime As Integer = 3600
    Dim Postprocessor_ScreenOutputToFile As Boolean = False
    Dim Postprocessor_ScreenOutputPath As String
    Dim Postprocessor_Arguments As String = ""
    Dim Postprocessor_ExecuteAfterModelRun As Boolean = False
    Dim Postprocessor_ModelWorkPath As String
    Dim PostProcessor_HasTrigger As Boolean
    Dim PostProcessor_FlagForTriggerFile As String

    Public ReadOnly Property Name()
        Get
            Name = Me.PostProcessor_Name
        End Get
    End Property

    Public ReadOnly Property Exe()
        Get
            Exe = Me.PostProcessor_Exe
        End Get
    End Property

    Public ReadOnly Property InputFile()
        Get
            InputFile = Me.PostProcessor_InputFile
        End Get
    End Property
    Public ReadOnly Property MaxTime()
        Get
            MaxTime = Me.PostProcessor_MaxTime
        End Get
    End Property

    Public ReadOnly Property ScreenOutputToFile()
        Get
            ScreenOutputToFile = Me.Postprocessor_ScreenOutputToFile
        End Get
    End Property

    Public ReadOnly Property ScreenOutputPath()
        Get
            ScreenOutputPath = Me.Postprocessor_ScreenOutputPath
        End Get
    End Property

    Public ReadOnly Property Arguments()
        Get
            Arguments = Me.PostProcessor_Arguments
        End Get
    End Property

    Public ReadOnly Property HasTrigger()
        Get
            HasTrigger = Me.PostProcessor_HasTrigger
        End Get
    End Property
    Public Property FlagForTriggerFile() As String
        Get
            FlagForTriggerFile = Me.PostProcessor_FlagForTriggerFile
        End Get
        Set(ByVal value As String)
            Me.PostProcessor_FlagForTriggerFile = value
        End Set
    End Property

    Public ReadOnly Property ExecuteAfterModelRun()
        Get
            ExecuteAfterModelRun = Me.Postprocessor_ExecuteAfterModelRun
        End Get
    End Property

    Public ReadOnly Property ModelWorkPath()
        Get
            ModelWorkPath = Me.Postprocessor_ModelWorkPath
        End Get
    End Property

    Public Sub LoadData(ByVal ProjectFile As EnterData)
        ProjectFile.GetDataStr("NAME", Me.PostProcessor_Name, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("EXE", Me.PostProcessor_Exe, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("INPUT_FILE", Me.PostProcessor_InputFile, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("ARGUMENTS", Me.Postprocessor_Arguments, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataLog("HAS_TRIGGER", Me.PostProcessor_HasTrigger, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("MAX_TIME", Me.Postprocessor_MaxTime, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataLog("SCREEN_OUTPUT_TO_FILE", Me.Postprocessor_ScreenOutputToFile, EnterData.FromBlockFromBlock)
        If Me.Postprocessor_ScreenOutputToFile Then
            ProjectFile.GetDataStr("SCREEN_OUTPUT_PATH", Me.Postprocessor_ScreenOutputPath, EnterData.FromBlockFromBlock)
        End If
        ProjectFile.GetDataLog("EXECUTE_AFTER_MODEL_RUN", Me.Postprocessor_ExecuteAfterModelRun, EnterData.FromBlockFromBlock)
        If Me.Postprocessor_ExecuteAfterModelRun Then
            ProjectFile.GetDataStr("MODEL_WORKING_PATH", Me.Postprocessor_ModelWorkPath, EnterData.FromBlockFromBlock)
        End If
    End Sub
End Class
