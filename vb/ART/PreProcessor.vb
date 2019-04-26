Imports Mohid_Base

Public Class PreProcessor
    Dim PreProcessor_Name As String
    Dim PreProcessor_Exe As String
    Dim PreProcessor_InputFile As String
    Dim Preprocessor_MaxTime As Integer = 3600
    Dim Preprocessor_ScreenOutputToFile As Boolean = False
    Dim Preprocessor_ScreenOutputPath As String
    Dim Preprocessor_Arguments As String = ""
    Dim PreProcessor_HasTrigger As Boolean
    Dim PreProcessor_FlagForTriggerFile As String


    Public ReadOnly Property Name()
        Get
            Name = Me.PreProcessor_Name
        End Get
    End Property

    Public ReadOnly Property Exe()
        Get
            Exe = Me.PreProcessor_Exe
        End Get
    End Property

    Public ReadOnly Property InputFile()
        Get
            InputFile = Me.PreProcessor_InputFile
        End Get
    End Property

    Public ReadOnly Property MaxTime()
        Get
            MaxTime = Me.PreProcessor_MaxTime
        End Get
    End Property

    Public ReadOnly Property ScreenOutputToFile()
        Get
            ScreenOutputToFile = Me.Preprocessor_ScreenOutputToFile
        End Get
    End Property

    Public ReadOnly Property ScreenOutputPath()
        Get
            ScreenOutputPath = Me.Preprocessor_ScreenOutputPath
        End Get
    End Property
    Public ReadOnly Property Arguments()
        Get
            Arguments = Me.Preprocessor_Arguments
        End Get
    End Property
    Public ReadOnly Property HasTrigger()
        Get
            HasTrigger = Me.PreProcessor_HasTrigger
        End Get
    End Property
    Public Property FlagForTriggerFile() As String
        Get
            FlagForTriggerFile = Me.PreProcessor_FlagForTriggerFile
        End Get
        Set(ByVal value As String)
            Me.PreProcessor_FlagForTriggerFile = value
        End Set
    End Property

    Public Sub LoadData(ByVal ProjectFile As EnterData)
        ProjectFile.GetDataStr("NAME", Me.PreProcessor_Name, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("EXE", Me.PreProcessor_Exe, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("INPUT_FILE", Me.PreProcessor_InputFile, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("ARGUMENTS", Me.Preprocessor_Arguments, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataLog("HAS_TRIGGER", Me.PreProcessor_HasTrigger, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("MAX_TIME", Me.Preprocessor_MaxTime, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataLog("SCREEN_OUTPUT_TO_FILE", Me.Preprocessor_ScreenOutputToFile, EnterData.FromBlockFromBlock)
        If Me.Preprocessor_ScreenOutputToFile Then
            ProjectFile.GetDataStr("SCREEN_OUTPUT_PATH", Me.Preprocessor_ScreenOutputPath, EnterData.FromBlockFromBlock)
        End If

    End Sub
End Class
