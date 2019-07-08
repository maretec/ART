Imports Mohid_Base
Module EnterDataIssues

    Sub Import_EnterDataProcess(ByVal Model_FileName_ON As Boolean, ByVal Model_FileName As String, ByVal TSSFile As String)
        Dim Found_TimeSerieConfig_Block As Boolean
        Dim Found_Property_Block As Boolean

        Dim Default_DB_FileName As String
        Dim Default_DB_TableName As String
        Dim Default_DB_InstantColumnName As String
        Dim Default_DB2_FileName As String
        Dim Default_DB2_TableName As String
        Dim Default_DB2_InstantColumnName As String

        Dim EnterData1 As New EnterData(TSSFile)

        With EnterData1
            If Model_FileName_ON = False Then
                .GetDataStr("MODEL_FILENAME", Model_FileName, .FromFile)
            End If

            .GetDataStr("DEFAULT_DB_FILENAME", Default_DB_FileName, .FromFile)
            .GetDataStr("DEFAULT_DB_TABLENAME", Default_DB_TableName, .FromFile)
            .GetDataStr("DEFAULT_DB_INSTANTCOLUMN_NAME", Default_DB_InstantColumnName, .FromFile)

            .GetDataStr("DEFAULT_DB2_FILENAME", Default_DB2_FileName, .FromFile)
            .GetDataStr("DEFAULT_DB2_TABLENAME", Default_DB2_TableName, .FromFile)
            .GetDataStr("DEFAULT_DB2_INSTANTCOLUMN_NAME", Default_DB2_InstantColumnName, .FromFile)

            Dim ReadTimeSeries_Count As Integer = 0
            Dim strKeywordValue As String

            ReDim Preserve Average(100, 100)
            ReDim Preserve Property_Name(100, 100)
            ReDim Preserve DB_ColumnName(100, 100)
            ReDim Preserve DB2_ColumnName(100, 100)
            ReDim Preserve Default_Value(100, 100)

            Found_TimeSerieConfig_Block = True

            Do
                'Extract  block
                .ExtractBlockFromBuffer("<BeginTimeSerieConfig>", "<EndTimeSerieConfig>", Found_TimeSerieConfig_Block)

                If Found_TimeSerieConfig_Block Then
                    Properties_Count = 0

                    ReadTimeSeries_Count = ReadTimeSeries_Count + 1

                    strKeywordValue = ""
                    .GetDataStr("DB_FILENAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        DB_FileName.Add(Default_DB_FileName)
                    Else
                        DB_FileName.Add(strKeywordValue)
                    End If

                    strKeywordValue = ""
                    .GetDataStr("DB_TABLENAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        DB_TableName.Add(Default_DB_TableName)
                    Else
                        DB_TableName.Add(strKeywordValue)

                    End If

                    strKeywordValue = ""
                    .GetDataStr("DB_INSTANTCOLUMN_NAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        DB_InstantColumnName.Add(Default_DB_InstantColumnName)
                    Else
                        DB_InstantColumnName.Add(strKeywordValue)
                    End If


                    strKeywordValue = ""
                    .GetDataStr("DB2_FILENAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        If Default_DB2_FileName = "" Then
                            DB2_FileName.Add(DB_FileName(ReadTimeSeries_Count))
                        Else
                            DB2_FileName.Add(Default_DB2_FileName)
                        End If
                    Else
                        DB2_FileName.Add(strKeywordValue)
                    End If

                    strKeywordValue = ""
                    .GetDataStr("DB2_TABLENAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        If Default_DB2_TableName = "" Then
                            DB2_TableName.Add(DB_TableName(ReadTimeSeries_Count))
                        Else
                            DB2_TableName.Add(Default_DB2_TableName)
                        End If
                    Else
                        DB2_TableName.Add(strKeywordValue)
                    End If

                    .GetDataStr("DB2_INSTANTCOLUMN_NAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        If Default_DB2_TableName = "" Then
                            DB2_InstantColumnName.Add(DB_InstantColumnName(ReadTimeSeries_Count))
                        Else
                            DB2_InstantColumnName.Add(Default_DB2_InstantColumnName)
                        End If
                    Else
                        DB2_InstantColumnName.Add(strKeywordValue)
                    End If

                    .GetDataStr("OUTPUT_FILENAME", strKeywordValue, .FromBlock)
                    Output_FileName.Add(strKeywordValue)

                    Found_Property_Block = True
                    Do
                        'Extract properties blocks
                        .ExtractBlockFromBlock("<BeginProperty>", "<EndProperty>", Found_Property_Block)

                        If Found_Property_Block Then

                            Properties_Count = Properties_Count + 1

                            .GetDataStr("PROPERTY_NAME", Property_Name(ReadTimeSeries_Count, Properties_Count), .FromBlockFromBlock)
                            .GetDataStr("DB_COLUMNAME", DB_ColumnName(ReadTimeSeries_Count, Properties_Count), .FromBlockFromBlock)
                            .GetDataStr("DB2_COLUMNAME", DB2_ColumnName(ReadTimeSeries_Count, Properties_Count), .FromBlockFromBlock)
                            .GetDataStr("DEFAULT_VALUE", Default_Value(ReadTimeSeries_Count, Properties_Count), .FromBlockFromBlock)

                            strKeywordValue = ""
                            .GetDataStr("AVERAGE", strKeywordValue, .FromBlock)
                            If strKeywordValue = "1" Then
                                Average(ReadTimeSeries_Count, Properties_Count) = True
                            Else
                                Average(ReadTimeSeries_Count, Properties_Count) = False
                            End If
                        End If

                    Loop Until Not Found_Property_Block

                    Properties_Number.Add(Properties_Count)
                End If
            Loop Until Not Found_TimeSerieConfig_Block
            TimeSeries_Count = ReadTimeSeries_Count
        End With
        Dim EnterData2 As New EnterData(Model_FileName)

        With EnterData2
            .GetDataTime("START", StartTime, .FromFile)
            .GetDataTime("END", EndTime, .FromFile)
        End With

        StartTime = StartTime.ToString("yyyy-MM-dd HH:00")
        EndTime = EndTime.AddHours(1).ToString("yyyy-MM-dd HH:00")

    End Sub

    Sub Export_EnterDataProcess(ByVal TimeSeries_Folder_ON As Boolean, ByVal TimeSeries_Folder As String, ByVal TSSFile As String)
        Dim Found_TimeSerieConfig_Block As Boolean

        Dim Default_DB_FileName As String
        Dim Default_DB_KeyTableName As String

        Dim Default_DB_I_ColumnName As String
        Dim Default_DB_J_ColumnName As String
        Dim Default_DB_K_ColumnName As String
        Dim Default_DB_Simulation_Name_ColumnName As String
        Dim Default_DB_Simulation_Dimensions_ColumnName As String
        Dim Default_DB_InstantColumnName As String

        Dim EnterData1 As New EnterData(TSSFile)

        With EnterData1
            If TimeSeries_Folder_ON = False Then
                .GetDataStr("TIMESERIES_FOLDER", TimeSeries_Folder, .FromFile)
            End If

            .GetDataStr("DEFAULT_DB_FILENAME", Default_DB_FileName, .FromFile)
            .GetDataStr("DEFAULT_DB_KEYTABLENAME", Default_DB_KeyTableName, .FromFile)
            .GetDataStr("DEFAULT_DB_I_COLUMN_NAME", Default_DB_I_ColumnName, .FromFile)
            .GetDataStr("DEFAULT_DB_J_COLUMN_NAME", Default_DB_J_ColumnName, .FromFile)
            .GetDataStr("DEFAULT_DB_K_COLUMN_NAME", Default_DB_K_ColumnName, .FromFile)
            .GetDataStr("DEFAULT_DB_SIMUL_COLUMN_NAME", Default_DB_Simulation_Name_ColumnName, .FromFile)
            .GetDataStr("DEFAULT_DB_DIM_COLUMN_NAME", Default_DB_Simulation_Dimensions_ColumnName, .FromFile)
            .GetDataStr("DEFAULT_DB_INSTANTCOLUMN_NAME", Default_DB_InstantColumnName, .FromFile)

            Dim ReadTimeSeries_Count As Integer = 0
            Found_TimeSerieConfig_Block = True
            Dim strKeywordValue As String
            Dim intKeywordValue As Integer
            Do
                'Extract  block
                .ExtractBlockFromBuffer("<BeginTimeSerieConfig>", "<EndTimeSerieConfig>", Found_TimeSerieConfig_Block)

                If Found_TimeSerieConfig_Block Then

                    ReadTimeSeries_Count = ReadTimeSeries_Count + 1

                    strKeywordValue = ""
                    .GetDataStr("DB_FILENAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        DB_FileName.Add(Default_DB_FileName)
                    Else
                        DB_FileName.Add(strKeywordValue)
                    End If

                    strKeywordValue = ""
                    .GetDataStr("DB_KEYTABLENAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        DB_KeyTableName.Add(Default_DB_KeyTableName)
                    Else
                        DB_KeyTableName.Add(strKeywordValue)
                    End If

                    strKeywordValue = ""
                    .GetDataStr("DB_I_COLUMN_NAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        DB_I_ColumnName.Add(Default_DB_I_ColumnName)
                    Else
                        DB_I_ColumnName.Add(strKeywordValue)
                    End If

                    strKeywordValue = ""
                    .GetDataStr("DB_J_COLUMN_NAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        DB_J_ColumnName.Add(Default_DB_J_ColumnName)
                    Else
                        DB_J_ColumnName.Add(strKeywordValue)
                    End If

                    strKeywordValue = ""
                    .GetDataStr("DB_K_COLUMN_NAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        DB_K_ColumnName.Add(Default_DB_K_ColumnName)
                    Else
                        DB_K_ColumnName.Add(strKeywordValue)
                    End If

                    strKeywordValue = ""
                    .GetDataStr("DB_SIMUL_COLUMN_NAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        DB_Simulation_Name_ColumnName.Add(Default_DB_Simulation_Name_ColumnName)
                    Else
                        DB_Simulation_Name_ColumnName.Add(strKeywordValue)
                    End If

                    strKeywordValue = ""
                    .GetDataStr("DB_DIM_COLUMN_NAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        DB_Simulation_Dimensions_ColumnName.Add(Default_DB_Simulation_Dimensions_ColumnName)
                    Else
                        DB_Simulation_Dimensions_ColumnName.Add(strKeywordValue)
                    End If

                    strKeywordValue = ""
                    .GetDataStr("DB_INSTANTCOLUMN_NAME", strKeywordValue, .FromBlock)
                    If strKeywordValue = "" Then
                        DB_InstantColumnName.Add(Default_DB_InstantColumnName)
                    Else
                        DB_InstantColumnName.Add(strKeywordValue)
                    End If

                    .GetDataStr("SIMULATION_NAME", strKeywordValue, .FromBlock)
                    Simulation_Name.Add(strKeywordValue)

                    .GetDataInteger("SIMULATION_DIMENSIONS", intKeywordValue, .FromBlock)
                    Simulation_Dimensions.Add(intKeywordValue)

                    .GetDataInteger("TS_I", intKeywordValue, .FromBlock)
                    TS_I.Add(intKeywordValue)

                    .GetDataInteger("TS_J", intKeywordValue, .FromBlock)
                    TS_J.Add(intKeywordValue)

                    .GetDataInteger("TS_K", intKeywordValue, .FromBlock)
                    TS_K.Add(intKeywordValue)

                    .GetDataStr("TS_FILENAME", strKeywordValue, .FromBlock)
                    TS_FileName.Add(strKeywordValue)

                End If
            Loop Until Not Found_TimeSerieConfig_Block
            TimeSeries_Count = ReadTimeSeries_Count
        End With
    End Sub

End Module
