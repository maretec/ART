Imports Mohid_Base
Imports System.IO
Module ReadWriteTextFiles
    Public Sub WriteTimeSerie(ByVal TimeSerieID As Integer, ByVal Properties_Count As Integer)
        Dim objFileStream As New FileStream(Output_FileName(TimeSerieID), FileMode.Create, FileAccess.ReadWrite, FileShare.Read)
        Dim objStreamWriter As New StreamWriter(objFileStream)
        Dim PropertyID As Integer
        Dim row As Integer
        objStreamWriter.WriteLine("!Time Series Automatically Created in " & Now.ToString("yyyy-MM-dd HH:mm") & " by MOHID TimeSeries Creator")
        objStreamWriter.WriteLine()

        objStreamWriter.Write("!Column_1 - Time")

        For PropertyID = 1 To Properties_Count
            objStreamWriter.Write("; Column_" & PropertyID + 1 & " - " & Property_Name(TimeSerieID, PropertyID))
        Next

        objStreamWriter.WriteLine()
        objStreamWriter.WriteLine()
        objStreamWriter.WriteLine("SERIE_INITIAL_DATA   : " & Year(Instant(1)) & " " & Month(Instant(1)) & " " & Day(Instant(1)) & " " & Hour(Instant(1)) & " " & Minute(Instant(1)) & " " & Second(Instant(1)))
        objStreamWriter.WriteLine("TIME_UNITS           : HOURS")
        objStreamWriter.WriteLine()
        objStreamWriter.WriteLine("<BeginTimeSerie>")

        Dim HourFromStart As Integer = -1
        For row = 1 To TotalInstants
            HourFromStart = HourFromStart + 1
            objStreamWriter.Write(HourFromStart.ToString)
            For PropertyID = 1 To Properties_Count

                objStreamWriter.Write("            " & PropertyValue(TimeSerieID, PropertyID, row) & "     ")
            Next
            objStreamWriter.Write(vbCrLf)
        Next

        objStreamWriter.WriteLine("<EndTimeSerie>")
        objStreamWriter.Close()
        objFileStream.Close()
    End Sub
    Public Sub ReadTimeSerie(ByVal TimeSeries_Folder As String, ByVal TimeSerieID As Integer, ByVal Properties_Count As Integer)

        Dim iProp As Integer
        Dim chConstants
        Dim iSerie, nSeries As Integer
        Dim iLine As Integer
        Dim TS_ColumnNames_List As New Collection()
        Try
            Dim TimeSerie1 As New ReadMohidTimeSerie(TimeSeries_Folder + "\" + TS_FileName(TimeSerieID))
            Timeserie = TimeSerie1
            Properties_Count = UBound(TimeSerie.PropName)
            'Fills List Box
            For iProp = 0 To UBound(TimeSerie.PropName) - 1
                TS_ColumnNames_List.Add(TimeSerie.PropName(iProp))
            Next


        Catch ex As Exception
            MsgBox("Invalid Time Serie File", MsgBoxStyle.OKOnly + MsgBoxStyle.Critical, "Error")
        End Try
    End Sub

    Public Function GetInstant(ByVal i As Long) As DateTime
        GetInstant = DateSerial(TimeSerie.ModelData(i, 2).ToString, _
        TimeSerie.ModelData(i, 3).ToString, TimeSerie.ModelData(i, 4).ToString) _
        + " " + TimeSerial(TimeSerie.ModelData(i, 5).ToString, _
        TimeSerie.ModelData(i, 6).ToString, TimeSerie.ModelData(i, 7).ToString)
    End Function

End Module
