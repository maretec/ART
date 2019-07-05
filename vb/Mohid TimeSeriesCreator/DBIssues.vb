Option Explicit On 
'Option Strict On
Imports System.Data.OleDb
Imports Mohid_Base
Module DBIssues
    Public PropertyValue(,,) As String
    Public MaxDate As Date
    Public Instant() As Date
    Public TotalInstants As Integer
    Public Sub ReadDB(ByVal TimeSerieID As Integer, ByVal Properties_Count As Integer)
        Dim SCONNECTION As String = "Provider=Microsoft.Jet.OLEDB.4.0;" & _
        "Data Source=" & DB_FileName(TimeSerieID) & ";Persist Security Info=False"

        Dim SCONNECTION2 As String = "Provider=Microsoft.Jet.OLEDB.4.0;" & _
        "Data Source=" & DB2_FileName(TimeSerieID) & ";Persist Security Info=False"

        Dim SQL_String As String = "SELECT * FROM " & DB_TableName(TimeSerieID) & _
                         " WHERE " & DB_InstantColumnName(TimeSerieID) & _
                         " >= #" & StartTime.ToString("yyyy-MM-dd HH:mm") & "# AND " & _
                         DB_InstantColumnName(TimeSerieID) & " <= #" & EndTime.ToString("yyyy-MM-dd HH:mm") & "# " & _
                         "order by " & DB_InstantColumnName(TimeSerieID)

        TotalInstants = 1 + DateDiff(DateInterval.Hour, StartTime.AddHours(StartTime.Hour), EndTime.AddHours(EndTime.Hour))
        Dim row As Integer
        ReDim Instant(TotalInstants)
        Dim PropertyID As Integer
        ReDim PropertyValue(TimeSerieID, Properties_Count, TotalInstants)


        Dim OleConn As New System.Data.OleDb.OleDbConnection(SCONNECTION)

        Instant(0) = StartTime.AddHours(-1).ToString("yyyy-MM-dd HH:mm")

        For row = 1 To TotalInstants

            Instant(row) = Instant(row - 1).AddHours(1)
            Try
                OleConn.Open()
            Catch myException As System.Exception
                MsgBox(myException.Message)
            End Try

            '!!!Attention!!! Next 8 lines are to be removed;it's used because of short-time predictions
            'from meteoIST (this line makes instant 24:00 = 23:00)
            'If row = TotalInstants And Instant(row - 1).Hour = 23 Then
            '    Dim SQL_CountLastInstant As String = "SELECT Count(*) FROM " & DB_TableName(TimeSerieID) & _
            '                      " WHERE " & DB_InstantColumnName(TimeSerieID) & _
            '                      " = #" & Instant(row).ToString("yyyy-MM-dd HH:mm") & "# "
            '    Dim objCmd_CountLastInstant As New OleDb.OleDbCommand(SQL_CountLastInstant, OleConn)
            '    Dim CountLastInstant As Integer = objCmd_CountLastInstant.ExecuteScalar
            '    If CountLastInstant = 0 Then Instant(row) = Instant(row - 1)
            'End If


            Dim SQL_CountIncisive As String = "SELECT Count(*) FROM " & DB_TableName(TimeSerieID) & _
                              " WHERE " & DB_InstantColumnName(TimeSerieID) & _
                              " = #" & Instant(row).ToString("yyyy-MM-dd HH:mm") & "# "
            Dim objCmd_CountIncisive As New OleDb.OleDbCommand(SQL_CountIncisive, OleConn)
            Dim CountIncisive As Integer = objCmd_CountIncisive.ExecuteScalar

            Dim SQL_Incisive As String = "SELECT * FROM " & DB_TableName(TimeSerieID) & _
                              " WHERE " & DB_InstantColumnName(TimeSerieID) & _
                              " = #" & Instant(row).ToString("yyyy-MM-dd HH:mm") & "# "
            Dim objCmd_Incisive As New OleDb.OleDbCommand(SQL_Incisive, OleConn)
            Dim Incisive As System.Data.OleDb.OleDbDataReader

            Incisive = objCmd_Incisive.ExecuteReader
            If CountIncisive = 1 Then
                While Incisive.Read

                    For PropertyID = 1 To Properties_Count
                        PropertyValue(TimeSerieID, PropertyID, row) = Incisive.Item(DB_ColumnName(TimeSerieID, PropertyID))
                    Next

                End While
                OleConn.Close()
                Console.Write(vbCrLf & Instant(row))
            Else
                OleConn.Close()

                Dim OleConn2 As New System.Data.OleDb.OleDbConnection(SCONNECTION2)
                OleConn2.Open()

                For PropertyID = 1 To Properties_Count
                    If Average(TimeSerieID, PropertyID) = True Then
                        PropertyValue(TimeSerieID, PropertyID, row) = GetAverage(TimeSerieID, PropertyID, row, OleConn2)
                    ElseIf Average(TimeSerieID, PropertyID) = False Then
                        PropertyValue(TimeSerieID, PropertyID, row) = GetLastValue(TimeSerieID, PropertyID, row, OleConn2)
                    End If
                Next

                OleConn2.Close()

                Console.Write(vbCrLf & Instant(row) & " (Using old values -- " & Property_Name(TimeSerieID, 1) & ": Last Value = " & MaxDate.ToString("yyyy-MM-dd HH:mm") & ")")
                'Console.Write(vbCrLf & Instant(row) & " (Using old values)")

            End If
        Next

    End Sub

    Private Function GetAverage(ByVal TimeSerieID As Integer, ByVal PropertyID As Integer, ByVal row As Integer, ByVal OleConn2 As OleDbConnection)

        Dim SQL_CountMax As String = "SELECT Count(*) FROM " & DB2_TableName(TimeSerieID) & _
                     " WHERE " & DB2_InstantColumnName(TimeSerieID) & _
                     " < #" & Instant(row).ToString("yyyy-MM-dd HH:mm") & "#  "
        Dim objCmd_CountMax As New OleDb.OleDbCommand(SQL_CountMax, OleConn2)
        Dim DB2_CountMaxDate As Integer = objCmd_CountMax.ExecuteScalar

        If DB2_CountMaxDate = 0 Then
            GetAverage = Default_Value(TimeSerieID, PropertyID)
        Else

            'Next > Most recent record for the same hour
            'Dim SQL_Max As String = "SELECT MAX(" & DB2_InstantColumnName(TimeSerieID) & ") FROM " & DB2_TableName(TimeSerieID) & _
            '             " WHERE HOUR(" & DB2_InstantColumnName(TimeSerieID) & ")" & _
            '             " = " & Hour(Instant(row)) & " AND " & DB2_InstantColumnName(TimeSerieID) & _
            '" <= #" & EndTime.ToString("yyyy-MM-dd HH:mm") & "#"

            Dim SQL_Max As String = "SELECT MAX(" & DB2_InstantColumnName(TimeSerieID) & ") FROM " & DB2_TableName(TimeSerieID) & _
                         " WHERE " & DB2_InstantColumnName(TimeSerieID) & _
                         " <= #" & EndTime.ToString("yyyy-MM-dd HH:mm") & "#"

            Dim objCmd_Max As New OleDb.OleDbCommand(SQL_Max, OleConn2)
            Dim DB2_MaxDate As Date

            Try
                DB2_MaxDate = objCmd_Max.ExecuteScalar
                MaxDate = DB2_MaxDate

            Catch myException As System.Exception
                MsgBox(myException.Message)
            End Try
            'Next > Average of last 3 days at the same time instant
            'Dim SQL_Average As String = "SELECT AVG(" & DB2_ColumnName(TimeSerieID, PropertyID) & ") FROM " & DB2_TableName(TimeSerieID) & _
            '             " WHERE  Hour(" & DB2_InstantColumnName(TimeSerieID) & ")" & _
            '             " = " & Hour(Instant(row)) & " AND " & _
            '             DB2_InstantColumnName(TimeSerieID) & " >= #" & DB2_MaxDate.AddDays(-2).ToShortDateString & "# "

            ' Next line code was replaced by last one. There was not a clear idea of what made next line to stop functioning
            'DB2_InstantColumnName(TimeSerieID) & " >= #" & DB2_MaxDate.AddDays(-2) & "# "

            'Next > average of last records of the last day
            Dim SQL_Average As String = "SELECT AVG(" & DB2_ColumnName(TimeSerieID, PropertyID) & ") FROM " & DB2_TableName(TimeSerieID) & _
             " WHERE  " & _
            DB2_InstantColumnName(TimeSerieID) & " >= #" & DB2_MaxDate.AddHours(-23).ToString("yyyy-MM-dd HH:mm") & "# "

            Dim objCmd_Avg As New OleDb.OleDbCommand(SQL_Average, OleConn2)
            Dim DB2_Value As Double
            Try

                DB2_Value = objCmd_Avg.ExecuteScalar()
            Catch myException As System.Exception
                MsgBox(myException.Message)
            End Try

            GetAverage = System.Math.Round(DB2_Value, 2)

        End If
    End Function
    Private Function GetLastValue(ByVal TimeSerieID As Integer, ByVal PropertyID As Integer, ByVal row As Integer, ByVal OleConn2 As OleDbConnection)

        Dim SQL_CountMax As String = "SELECT Count(*) FROM " & DB2_TableName(TimeSerieID) & _
                     " WHERE " & DB2_InstantColumnName(TimeSerieID) & _
                     " < #" & Instant(row).ToString("yyyy-MM-dd HH:mm") & "#  "
        Dim objCmd_CountMax As New OleDb.OleDbCommand(SQL_CountMax, OleConn2)
        Dim DB2_CountMaxDate As Integer = objCmd_CountMax.ExecuteScalar

        If DB2_CountMaxDate = 0 Then
            GetLastValue = Default_Value(TimeSerieID, PropertyID)
        Else
            Dim SQL_Max As String = "SELECT MAX(" & DB2_InstantColumnName(TimeSerieID) & ") FROM " & DB2_TableName(TimeSerieID) & _
                         " WHERE HOUR(" & DB2_InstantColumnName(TimeSerieID) & ")" & _
                         " = " & Hour(Instant(row)) & " AND " & DB2_InstantColumnName(TimeSerieID) & _
            " <= #" & EndTime.ToString("yyyy-MM-dd HH:mm") & "#"
            Dim objCmd_Max As New OleDb.OleDbCommand(SQL_Max, OleConn2)
            Dim DB2_MaxDate As Date

            Try
                DB2_MaxDate = objCmd_Max.ExecuteScalar
            Catch myException As System.Exception
                MsgBox(myException.Message)
            End Try

            Dim SQL_LastValue As String = "SELECT " & DB2_ColumnName(TimeSerieID, PropertyID) & " FROM " & DB2_TableName(TimeSerieID) & _
                         " WHERE  Hour(" & DB2_InstantColumnName(TimeSerieID) & ")" & _
                         " = " & Hour(Instant(row)) & " AND " & _
                         DB2_InstantColumnName(TimeSerieID) & " >= #" & DB2_MaxDate.ToShortDateString & "# "

            Dim objCmd_LastValue As New OleDb.OleDbCommand(SQL_LastValue, OleConn2)
            Dim DB2_Value As Double
            Try

                DB2_Value = objCmd_LastValue.ExecuteScalar()
            Catch myException As System.Exception
                MsgBox(myException.Message)
            End Try

            GetLastValue = System.Math.Round(DB2_Value, 2)




        End If
    End Function

    Public Sub WriteDB(ByVal TimeSerieID As Integer, ByVal Properties_Count As Integer)
        Dim SCONNECTION As String = "Provider=Microsoft.Jet.OLEDB.4.0;" & _
        "Data Source=" & DB_FileName(TimeSerieID) & ";Persist Security Info=False"
        Dim SCONNECTION2 As String = SCONNECTION
        Dim i As Long
        Dim n As Integer
        Dim DB_TableName_ As String
        Dim OleConn As New OleDbConnection(SCONNECTION)
        Dim OleConn2 As New OleDbConnection(SCONNECTION2)

        Dim SQL_TableName As String = "SELECT * FROM " & DB_KeyTableName(TimeSerieID) & _
                 " WHERE " & DB_I_ColumnName(TimeSerieID) & " = " & TS_I(TimeSerieID) & _
                 " AND " & DB_J_ColumnName(TimeSerieID) & " = " & TS_J(TimeSerieID) & _
                 " AND " & DB_K_ColumnName(TimeSerieID) & " = " & TS_K(TimeSerieID) & _
                 " AND " & DB_Simulation_Name_ColumnName(TimeSerieID) & " = '" & Simulation_Name(TimeSerieID) & "'" & _
                 " AND " & DB_Simulation_Dimensions_ColumnName(TimeSerieID) & " = " & Simulation_Dimensions(TimeSerieID)

        Dim objCmd_TableName As New OleDbCommand(SQL_TableName, OleConn)
        Dim TableName As OleDbDataReader

        Try
            OleConn.Open()

            TableName = objCmd_TableName.ExecuteReader()
            TableName.Read()
            DB_TableName_ = TableName("TS_NomeTabela")

            OleConn.Close()
        Catch myException As System.Exception
            MsgBox(myException.Message)
        End Try

        Dim CountOldRecords(TimeSerie.Size) As Integer
        Dim objCmd_CountOldRecords As New OleDbCommand()
        Try
            OleConn.Open()

            For i = 1 To TimeSerie.Size
                Dim SQL_CountOldRecords As String = "SELECT Count(*) FROM " & DB_TableName_ & _
                          " WHERE " & DB_InstantColumnName(TimeSerieID) & _
                          " =  #" & GetInstant(i).ToString("yyyy-MM-dd HH:mm:ss") & "# "

                objCmd_CountOldRecords.CommandText = SQL_CountOldRecords
                objCmd_CountOldRecords.Connection = OleConn
                objCmd_CountOldRecords.ExecuteScalar()

                CountOldRecords(i) = objCmd_CountOldRecords.ExecuteScalar

            Next

            OleConn.Close()
        Catch myException As System.Exception
            MsgBox(myException.Message)
        End Try

        Dim SQL_UpdateRecords As String
        Dim objCmd_UpdateRecords As New OleDb.OleDbCommand()
        Dim SQL_InsertNewRecords As String
        Dim objCmd_InsertNewRecords As New OleDb.OleDbCommand()

        OleConn.Open()
        OleConn2.Open()
        For i = 1 To TimeSerie.Size
            If CountOldRecords(i) <> 0 Then
                Try
                    SQL_UpdateRecords = "UPDATE " & DB_TableName_ & " SET "
                    For n = 8 To UBound(TimeSerie.PropName)
                        SQL_UpdateRecords += RemoveHyphens(TimeSerie.PropName(n)) & " = " & TimeSerie.ModelData(i, n)
                        If n <> UBound(TimeSerie.PropName) Then SQL_UpdateRecords += ","
                    Next
                    SQL_UpdateRecords += " WHERE Instante = #" & GetInstant(i).ToString("yyyy-MM-dd HH:mm:ss") & "#"

                    objCmd_UpdateRecords.CommandText = SQL_UpdateRecords
                    objCmd_UpdateRecords.Connection = OleConn
                    objCmd_UpdateRecords.ExecuteNonQuery()

                Catch myException As System.Exception
                    MsgBox(myException.Message)
                End Try
            ElseIf CountOldRecords(i) = 0 Then
                Try
                    SQL_InsertNewRecords = "INSERT INTO " & DB_TableName_ & " (Instante"
                    For n = 8 To UBound(TimeSerie.PropName)
                        SQL_InsertNewRecords += "," & RemoveHyphens(TimeSerie.PropName(n))
                    Next

                    SQL_InsertNewRecords += ") values (#" & GetInstant(i).ToString("yyyy-MM-dd HH:mm:ss") & "#,"
                    For n = 8 To UBound(TimeSerie.PropName) - 1
                        SQL_InsertNewRecords += TimeSerie.ModelData(i, n) & ", "
                    Next
                    SQL_InsertNewRecords += TimeSerie.ModelData(i, n) & ")"

                    objCmd_InsertNewRecords.CommandText = SQL_InsertNewRecords
                    objCmd_InsertNewRecords.Connection = OleConn
                    objCmd_InsertNewRecords.ExecuteNonQuery()
                Catch myException As System.Exception
                    MsgBox(myException.Message)
                End Try
            End If
        Next
        OleConn2.Close()
        OleConn.Close()

    End Sub
    Function RemoveHyphens(ByVal Property_ As String) As String
        RemoveHyphens = Replace(Property_, "-", "_")
    End Function
End Module

