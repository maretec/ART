Imports Mohid_Base
Public Class ReadMohidTimeSerie

    Public ModelData(,) As Single
    Public ResidualData() As Single
    Public PropName() As String
    Public PropUnits() As String
    Public TimeYears() As Single
    Public TimeMonths() As Single
    Public TimeDays() As Single
    Public TimeHours() As Single
    Public TimeMinutes() As Single
    Public TimeSeconds() As Single
    Public DateTime() As DateTime
    Public LocI, LocJ, LocK As Single
    Public InitialDate, EndDate As DateTime
    Public TimeUnits As String
    Public Size As Long
    Public HaveHeaderData As Boolean
    Private HasLocation As Boolean

    Public Sub New(ByVal FileName As String)

        Dim EnterData As New EnterData(FileName)
        Dim Found As Boolean
        Dim BeginBuffer, EndBuffer, DummyBuffer As Integer
        Dim BufferLine As String
        Dim i, j, NColumns, flag As Integer
        Dim BufferVector() As Single
        Dim AuxName(), AuxString As String

        With EnterData

            'Looks for the header block
            .ExtractBlockFromBuffer("<BeginTimeSerieHeader>", "<EndTimeSerieHeader>", Found)

            If Found Then
                HaveHeaderData = True
                .GetReadingLimits(BeginBuffer, EndBuffer, .FromBlock)

                .GetFullLine(BeginBuffer + 1, BufferLine)
                .ExtractVectorFromString(BufferLine, BufferVector)
                ReDim PropName(UBound(BufferVector))
                ReDim PropUnits(UBound(BufferVector))
                .GetFullLine(BeginBuffer + 1, BufferLine)
                .ExtractStringVectorFromString(BufferLine, PropName)
                If (EndBuffer - BeginBuffer = 3) Then
                    .GetFullLine(BeginBuffer + 2, BufferLine)
                    .ExtractStringVectorFromString(BufferLine, PropUnits)
                End If
                .RewindBuffer()
            Else
                HaveHeaderData = False
            End If


            'Extract data
            .ExtractBlockFromBuffer("<BeginTimeSerie>", "<EndTimeSerie>", Found)
            .GetReadingLimits(BeginBuffer, EndBuffer, .FromBlock)

            'Enables to open time serie without blck ending "<EndTimeSerie>"
            If Not Found Then
                .GetReadingLimits(DummyBuffer, EndBuffer, .FromFile)
                MsgBox("This time serie file was not closed by Mohid.", MsgBoxStyle.Information + MsgBoxStyle.OKOnly, "Unclosed time serie")
            End If

            .GetFullLine(BeginBuffer + 1, BufferLine)
            .ExtractVectorFromString(BufferLine, BufferVector)
            NColumns = UBound(BufferVector)

            Size = EndBuffer - BeginBuffer - 1

            'Reads old fashion time series header
            If Not HaveHeaderData Then
                ReDim PropName(NColumns)
                .GetFullLine(BeginBuffer - 1, BufferLine)
                .ExtractStringVectorFromString(BufferLine, PropName)
            End If


            ReDim ModelData(Me.Size - 1, NColumns)
            For i = 0 To ModelData.GetUpperBound(0)
                .GetFullLine(BeginBuffer + 1 + i, BufferLine)
                .ExtractVectorFromString(BufferLine, BufferVector)
                For j = 0 To NColumns
                    ModelData(i, j) = BufferVector(j)
                Next j
            Next i

            'Initial date (Keyword = 'SERIE_INITIAL_DATA')
            Dim Year, Month, Day, Hour, Minutes, Seconds, Miliseconds As Integer
            Dim Aux As Single

            .GetDataTime("SERIE_INITIAL_DATA", InitialDate, .FromFile, flag)

            'Time Units (Keyword = 'TIME_UNITS')
            .GetDataStr("TIME_UNITS", TimeUnits, .FromFile, flag)

            'LOCALIZATION_I
            'LOCALIZATION_J
            'LOCALIZATION_K
            .GetDataReal("LOCALIZATION_I", LocI, .FromFile, flag)
            If flag = 1 Then
                .GetDataReal("LOCALIZATION_J", LocJ, .FromFile, flag)
                .GetDataReal("LOCALIZATION_K", LocK, .FromFile, flag)
                HasLocation = True
            Else
                HasLocation = False
            End If

            ReDim DateTime(Me.Size - 1)

            Select Case TimeUnits
                Case "YEARS"
                    For i = 0 To DateTime.GetUpperBound(0)
                        DateTime(i) = InitialDate.AddYears(ModelData(i, 0))
                    Next
                Case "MONTHS"
                    For i = 0 To DateTime.GetUpperBound(0)
                        DateTime(i) = InitialDate.AddMonths(ModelData(i, 0))
                    Next
                Case "DAYS"
                    For i = 0 To DateTime.GetUpperBound(0)
                        DateTime(i) = InitialDate.AddDays(ModelData(i, 0))
                    Next
                Case "HOURS"
                    For i = 0 To DateTime.GetUpperBound(0)
                        DateTime(i) = InitialDate.AddHours(ModelData(i, 0))
                    Next
                Case "MINUTES"
                    For i = 0 To DateTime.GetUpperBound(0)
                        DateTime(i) = InitialDate.AddMinutes(ModelData(i, 0))
                    Next
                Case "SECONDS"
                    For i = 0 To DateTime.GetUpperBound(0)
                        DateTime(i) = InitialDate.AddSeconds(ModelData(i, 0))
                    Next
            End Select

            ReDim TimeDays(Me.Size - 1)
            ReDim TimeHours(Me.Size - 1)
            ReDim TimeMinutes(Me.Size - 1)
            ReDim TimeSeconds(Me.Size - 1)

            For i = 1 To Me.Size - 1
                TimeSeconds(i) = DateDiff(DateInterval.Second, InitialDate, DateTime(i))
                TimeMinutes(i) = TimeSeconds(i) / 60
                TimeHours(i) = TimeMinutes(i) / 60
                TimeDays(i) = TimeHours(i) / 24
            Next

            EndDate = DateTime(Me.Size - 1)

            'Looks for the header block
            .ExtractBlockFromBuffer("<BeginResidual>", "<BeginResidual>", Found)

            If Found Then
                ReDim ResidualData(NColumns)
                .GetReadingLimits(BeginBuffer, EndBuffer, .FromBlock)
                .GetFullLine(BeginBuffer + 1, BufferLine)
                .ExtractVectorFromString(BufferLine, BufferVector)
                For i = 0 To UBound(BufferVector)
                    ResidualData(i) = Val(BufferVector(i))
                Next

            End If




        End With
    End Sub

    Public Sub SaveTimeSerie(ByVal OutFile As OutData)

        OutFile.WriteDataLine("SERIE_INITIAL_DATA", InitialDate)
        OutFile.WriteDataLine("TIME_UNITS", TimeUnits)
        If HasLocation Then
            OutFile.WriteDataLine("LOCALIZATION_I", LocI)
            OutFile.WriteDataLine("LOCALIZATION_J", LocJ)
            OutFile.WriteDataLine("LOCALIZATION_K", LocK)
        End If

        OutFile.WriteBlankLine()
        OutFile.WriteDataLine("<BeginTimeSerieHeader>")
        For i As Integer = 0 To ModelData.GetUpperBound(0)
            Dim LineString As String = ""
            For j As Integer = 0 To ModelData.GetUpperBound(1)
                LineString += " " + ModelData(i, j).ToString
            Next
            OutFile.WriteDataLine(LineString)
        Next

        OutFile.WriteDataLine("<EndTimeSerieHeader>")

    End Sub

    Public Sub GetTimeSeriesValue(ByVal CurrentTime As Date, ByVal DataColumn As Integer, ByRef Time1 As Date, _
                                  ByRef Value1 As Single, ByRef Time2 As Date, ByRef Value2 As Single)

        Dim CurrentIndex As Integer = 1
        Do While Date.op_LessThan(DateTime(CurrentIndex), CurrentTime)
            CurrentIndex += 1

            'Last Instant
            If CurrentIndex = Me.Size Then
                CurrentIndex = Me.Size - 1
                Exit Do
            End If
        Loop

        Time1 = DateTime(CurrentIndex - 1)
        Value1 = ModelData(CurrentIndex - 1, DataColumn)

        Time2 = DateTime(CurrentIndex)
        Value2 = ModelData(CurrentIndex, DataColumn)

    End Sub
End Class
