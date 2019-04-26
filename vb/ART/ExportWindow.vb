Imports Mohid_Base

Public Class ExportWindow
    Dim Export_WindowID As String
    Dim Export_DestinationPath As String
    Dim Export_WaterProperties As Boolean = False
    Dim Export_Hydrodynamics As Boolean = False

    Public ReadOnly Property ID()
        Get
            ID = Me.Export_WindowID
        End Get
    End Property

    Public ReadOnly Property DestinationPath()
        Get
            DestinationPath = Me.Export_DestinationPath
        End Get
    End Property

    Public ReadOnly Property WaterProperties()
        Get
            WaterProperties = Me.Export_WaterProperties
        End Get
    End Property

    Public ReadOnly Property Hydrodynamics()
        Get
            Hydrodynamics = Me.Export_Hydrodynamics
        End Get
    End Property


    Public Sub LoadData(ByVal ProjectFile As EnterData)
        Dim beginreading, endreading As Integer
        ProjectFile.GetReadingLimits(beginreading, endreading, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("EXPORT_WINDOW_ID", Me.Export_WindowID, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("EXPORT_DESTINATION_PATH", Me.Export_DestinationPath, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("EXPORT_HYDRODYNAMICS", Me.Export_Hydrodynamics, EnterData.FromBlockFromBlock)
        ProjectFile.GetDataStr("EXPORT_WATERPROPERTIES", Me.Export_WaterProperties, EnterData.FromBlockFromBlock)
    End Sub
End Class
