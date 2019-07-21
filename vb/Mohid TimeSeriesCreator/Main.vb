Imports Mohid_Base
Module Module1
    Public DB_FileName As New Collection()
    Public DB_TableName As New Collection()
    Public DB_KeyTableName As New Collection()
    Public DB_InstantColumnName As New Collection()
    Public DB_I_ColumnName As New Collection()
    Public DB_J_ColumnName As New Collection()
    Public DB_K_ColumnName As New Collection()
    Public DB_Simulation_Name_ColumnName As New Collection()
    Public DB_Simulation_Dimensions_ColumnName As New Collection()
    Public DB2_FileName As New Collection()
    Public DB2_TableName As New Collection()
    Public DB2_InstantColumnName As New Collection()
    Public Simulation_Name As New Collection()
    Public Simulation_Dimensions As New Collection()
    Public StartTime As Date
    Public EndTime As Date
    Public Average(,) As Boolean
    Public DB_ColumnName(,) As String
    Public TS_ColumnName(,) As String
    Public DB2_ColumnName(,) As String
    Public TimeSeries_Count As Integer = 1
    Public Properties_Count As Integer = 0
    Public Properties_Number As New Collection()
    Public Output_FileName As New Collection()
    Public TS_I As New Collection()
    Public TS_J As New Collection()
    Public TS_K As New Collection()
    Public TS_FileName As New Collection()
    Public Default_Value(,) As String
    Public Property_Name(,) As String
    Public TimeSerie As ReadMohidTimeSerie

    Sub Main()

        Dim Args() As String = GetCommandLineArgs()
        Dim HandleType As String = "Import"
        Dim SettingsFile As String = "TSImport.tss"
        Dim Model_FileName As String = Nothing
        Dim TimeSeries_Folder As String = Nothing
        Dim Model_FileName_ON As Boolean = True
        Dim TimeSeries_Folder_ON As Boolean = True
        Dim TimeSerieID As Integer

        If Args(0) <> "" Then
            HandleType = Args(0)
        End If

        If Args(1) <> "" Then
            SettingsFile = Args(1)
        End If



        If HandleType = "Import" Then

            If Args(2) <> "" Then
                Model_FileName = Args(2)
            Else
                Model_FileName_ON = False
            End If

            Call Import_EnterDataProcess(Model_FileName_ON, Model_FileName, SettingsFile)

            Console.Write("Creating Time Series.......")

            For TimeSerieID = 1 To TimeSeries_Count
                Call ReadDB(TimeSerieID, Properties_Number(TimeSerieID))
                Call WriteTimeSerie(TimeSerieID, Properties_Number(TimeSerieID))
                Console.Write(vbCrLf)
                Console.Write(TimeSerieID & " of " & TimeSeries_Count & " Time Series Done...")
            Next
        ElseIf HandleType = "Export" Then
            If Args(2) <> "" Then
                TimeSeries_Folder = Args(2)
            Else
                TimeSeries_Folder_ON = False
            End If

            Call Export_EnterDataProcess(TimeSeries_Folder_ON, TimeSeries_Folder, SettingsFile)

            Console.Write("Exporting Time Series.......")

            For TimeSerieID = 1 To TimeSeries_Count
                Call ReadTimeSerie(TimeSeries_Folder, TimeSerieID, Properties_Count)
                Call WriteDB(TimeSerieID, Properties_Count)
                Console.Write(vbCrLf)
                Console.Write(TS_FileName(TimeSerieID) & " (from Simulation " & Simulation_Name(TimeSerieID) & ") exported (" & TimeSerieID & "/" & TimeSeries_Count & ")...")
            Next

        End If

        Console.Write(vbCrLf)
        Console.Write("TimeSeries successfully finished his tasks.")

    End Sub
    Function GetCommandLineArgs() As String()

        ' Declare variables.
        Dim separators As String = " "
        Dim commands As String = Microsoft.VisualBasic.Command()
        Dim args(3) As String
        Dim pos0, pos1, pos2 As Integer
        Dim len0, len1, len2 As Integer
        Dim str0, str1, str2 As String

        str0 = "-a0="
        str1 = "-a1="
        str2 = "-a2="
        len0 = Len(str0)
        len1 = Len(str1)
        len2 = Len(str2)

        pos0 = InStr(commands, str0)
        pos1 = InStr(commands, str1)
        pos2 = InStr(commands, str2)


        If pos1 <> 0 And pos2 <> 0 Then
            args(0) = commands.Substring(pos0 + len0 - 1, pos1 - pos0 - len1 - 1)
            args(1) = commands.Substring(pos1 + len1 - 1, pos2 - pos1 - len2 - 1)
            args(2) = commands.Substring(pos2 + len2 - 1)
        ElseIf pos1 <> 0 And pos2 = 0 Then
            args(1) = commands.Substring(pos1 + len1 - 1)
            args(0) = commands.Substring(pos0 + len0 - 1, pos1 - pos0 - len1 - 1)
        ElseIf pos1 = 0 And pos2 <> 0 Then
            args(0) = commands.Substring(pos0 + len0 - 1, pos2 - pos0 - len2 - 1)
            args(2) = commands.Substring(pos2 + len2 - 1)
        End If


        Return args

    End Function

End Module
