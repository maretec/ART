Imports System.IO

Public Class EnterData

    Private Const Delimiter As String = ":"

    Public Const FromFile As Integer = 1
    Public Const FromBlock As Integer = 2
    Public Const FromBlockFromBlock As Integer = 3
    Public Const FromBlockFromBlockFromBlock As Integer = 4

    Private DataF As StreamReader
    Private BufferSize As Integer
    Private CurrentBufferLine As Integer
    Private CurrentInnerBlockLine_1 As Integer                  'From Block
    Private CurrentInnerBlockLine_2 As Integer                  'Block From Block
    Private CurrentInnerBlockLine_3 As Integer                  'Block From Block From Block
    Private FirstBlockBufferLine As Integer                     'From Block
    Private LastBlockBufferLine As Integer                      'From Block
    Private FirstBlockFromBlockBufferLine As Integer            'Block From Block
    Private LastBlockFromBlockBufferLine As Integer             'Block From Block
    Private FirstBlockFromBlockFromBlockBufferLine As Integer   'Block From Block From Block
    Private LastBlockFromBlockFromBlockBufferLine As Integer    'Block From Block From Block
    Private FullLine As String
    Private Buffer() As String
    Dim FS As FileStream

    Public Sub New(ByVal FileName As String)

        Dim BufferLine, i As Integer
        Dim AuxString As String
        Dim FoundTabsInFile As Boolean = False

        'Verifies if file exits. If not 
        If Not File.Exists(FileName) Then
            MsgBox("File " + FileName + " does not exists", MsgBoxStyle.Exclamation And MsgBoxStyle.OKOnly, "Error")
            Exit Sub
        End If

        'Opens file
        Dim FS As New FileStream(FileName, FileMode.Open, FileAccess.Read, FileShare.Read)
        DataF = New StreamReader(FS, System.Text.Encoding.Default)

        FullLine = DataF.ReadLine
        BufferSize = 1
        Do While Not FullLine Is Nothing
            FullLine = DataF.ReadLine
            BufferSize = BufferSize + 1
        Loop

        'check if file has at least one line to be read
        If BufferSize < 1 Then Exit Sub

        'allocate buffer
        ReDim Buffer(BufferSize)

        If BufferSize > 1000 Then

            DataF.BaseStream.Position = 0
            BufferLine = 1
            Buffer(BufferLine) = DataF.ReadLine
            Do While Not Buffer(BufferLine) Is Nothing
                BufferLine = BufferLine + 1
                Buffer(BufferLine) = DataF.ReadLine
            Loop

        Else

            DataF.BaseStream.Position = 0
            BufferLine = 1
            Buffer(BufferLine) = DataF.ReadLine
            Do While Not Buffer(BufferLine) Is Nothing
                BufferLine = BufferLine + 1
                AuxString = DataF.ReadLine
                If Not AuxString Is Nothing Then
                    'Search tabs ans replace with spaces
                    For i = 1 To AuxString.Length - 1
                        If AuxString.Chars(i).ToString = Chr(9) Then
                            AuxString = AuxString.Remove(i, 1)
                            AuxString = AuxString.Insert(i, Chr(32))
                            FoundTabsInFile = True
                        End If
                    Next
                End If
                Buffer(BufferLine) = AuxString
            Loop
        End If



        CurrentInnerBlockLine_1 = 0

        DataF.DiscardBufferedData()
        DataF.Close()
        FS.Close()

        If FoundTabsInFile Then MsgBox("Found tab formatting in data file.", MsgBoxStyle.Information + MsgBoxStyle.OKOnly, "Warning - Found tabs")

    End Sub

    Public Sub ExtractBlockFromBuffer(ByVal BlockBegin As String, _
                                      ByVal BlockEnd As String, _
                                      ByRef BlockFound As Boolean)
        'Local---------------------------------------------------
        Dim BlockBeginFound As Boolean
        Dim BlockEndFound As Boolean
        Dim BufferLine As Integer
        'Begin---------------------------------------------------

        BlockFound = False
        BlockBeginFound = False
        BlockEndFound = False
        FirstBlockBufferLine = 0
        LastBlockBufferLine = 0


        'Search the beginning of the block
        For BufferLine = CurrentInnerBlockLine_1 To BufferSize
            If (ScanLineForKeyword(Buffer(BufferLine), Trim(BlockBegin))) Then
                FirstBlockBufferLine = BufferLine 'first line <beginblock>
                BlockBeginFound = True
                Exit For
            End If
        Next BufferLine


        'Search the end of the block
        If BlockBeginFound Then
            For BufferLine = FirstBlockBufferLine To BufferSize
                If (ScanLineForKeyword(Buffer(BufferLine), Trim(BlockEnd))) Then
                    LastBlockBufferLine = BufferLine 'last line <endblock>
                    BlockEndFound = True
                    Exit For
                End If
            Next BufferLine
        End If

        'check if block limits were found
        If Not (BlockBeginFound And BlockEndFound) Then Exit Sub

        'To Not find the same Block 
        CurrentInnerBlockLine_1 = LastBlockBufferLine + 1
        CurrentInnerBlockLine_2 = FirstBlockBufferLine + 1
        'CurrentBufferLine = LastBlockBufferLine
        BlockFound = True

    End Sub

    Public Sub ExtractBlockFromBlock(ByVal BlockBegin As String, ByVal BlockEnd As String, ByRef BlockFound As Boolean)

        'Local---------------------------------------------------
        Dim BlockBeginFound As Boolean
        Dim BlockEndFound As Boolean
        Dim BufferLine As Integer
        'Begin---------------------------------------------------

        BlockFound = False
        BlockBeginFound = False
        BlockEndFound = False
        FirstBlockFromBlockBufferLine = 0
        LastBlockFromBlockBufferLine = 0

        'Search the beginning of the block
        For BufferLine = CurrentInnerBlockLine_2 To LastBlockBufferLine
            If (ScanLineForKeyword(Buffer(BufferLine), Trim(BlockBegin))) Then
                FirstBlockFromBlockBufferLine = BufferLine 'first line <beginblockfromblock>
                BlockBeginFound = True
                Exit For
            End If
        Next BufferLine

        'Search the end of the block
        If BlockBeginFound Then
            For BufferLine = FirstBlockFromBlockBufferLine To LastBlockBufferLine
                If (ScanLineForKeyword(Buffer(BufferLine), Trim(BlockEnd))) Then
                    LastBlockFromBlockBufferLine = BufferLine 'last line <endblockfromblock>
                    BlockEndFound = True
                    Exit For
                End If
            Next BufferLine
        End If

        'check if block was found
        If Not (BlockBeginFound And BlockEndFound) Then Exit Sub

        CurrentInnerBlockLine_2 = LastBlockFromBlockBufferLine + 1
        CurrentInnerBlockLine_3 = FirstBlockFromBlockBufferLine + 1
        BlockFound = True

    End Sub

    Public Sub ExtractBlockFromBlockFromBlock(ByVal BlockBegin As String, ByVal BlockEnd As String, ByRef BlockFound As Boolean)

        'Local---------------------------------------------------
        Dim BlockBeginFound As Boolean
        Dim BlockEndFound As Boolean
        Dim BufferLine As Integer
        'Begin---------------------------------------------------

        BlockFound = False
        BlockBeginFound = False
        BlockEndFound = False
        FirstBlockFromBlockFromBlockBufferLine = 0
        LastBlockFromBlockFromBlockBufferLine = 0

        'Search the beginning of the block
        For BufferLine = CurrentInnerBlockLine_3 To LastBlockFromBlockBufferLine
            If (ScanLineForKeyword(Buffer(BufferLine), Trim(BlockBegin))) Then
                FirstBlockFromBlockFromBlockBufferLine = BufferLine 'first line <beginblockfromblock>
                BlockBeginFound = True
                Exit For
            End If
        Next BufferLine

        'Search the end of the block
        If BlockBeginFound Then
            For BufferLine = FirstBlockFromBlockFromBlockBufferLine To LastBlockFromBlockBufferLine
                If (ScanLineForKeyword(Buffer(BufferLine), Trim(BlockEnd))) Then
                    LastBlockFromBlockFromBlockBufferLine = BufferLine 'last line <endblockfromblock>
                    BlockEndFound = True
                    Exit For
                End If
            Next BufferLine
        End If

        'check if block was found
        If Not (BlockBeginFound And BlockEndFound) Then Exit Sub

        CurrentInnerBlockLine_3 = LastBlockFromBlockFromBlockBufferLine + 1
        BlockFound = True

    End Sub

    Public Sub GetDataStr(ByVal Keyword As String, ByRef value As String, Optional ByVal ExtractType As Integer = 0, Optional ByRef flag As Integer = 0)

        'Local---------------------------------------------------
        Dim KeywordLine As Integer
        Dim AuxiliarString As String
        Dim ValueFound As Boolean
        Dim KeywordFound As Boolean

        'Begin---------------------------------------------------

        KeywordFound = False
        flag = 0

        Call GetKeywordLine(Keyword, ExtractType, KeywordLine, KeywordFound)

        If KeywordFound Then
            Call ScanLineForValue(Keyword, KeywordLine, ValueFound, value)
            flag = 1
        End If

    End Sub

    Public Sub GetDataReal(ByVal Keyword As String, ByRef value As Single, Optional ByVal ExtractType As Integer = 0, Optional ByRef flag As Integer = 0)

        'Local---------------------------------------------------
        Dim KeywordLine As Integer
        Dim AuxiliarString As String
        Dim ValueFound As Boolean
        Dim KeywordFound As Boolean
        Dim auxstring As String

        'Begin---------------------------------------------------

        KeywordFound = False
        flag = 0

        Call GetKeywordLine(Keyword, ExtractType, KeywordLine, KeywordFound)

        If KeywordFound Then
            Call ScanLineForValue(Keyword, KeywordLine, ValueFound, auxstring)
            flag = 1
            value = Val(auxstring)
        End If

    End Sub

    Public Sub GetDataInteger(ByVal Keyword As String, ByRef value As Integer, Optional ByVal ExtractType As Integer = 0, Optional ByRef flag As Integer = 0)

        'Local---------------------------------------------------
        Dim KeywordLine As Integer
        Dim AuxiliarString As String
        Dim ValueFound As Boolean
        Dim KeywordFound As Boolean
        Dim auxstring As String

        'Begin---------------------------------------------------

        KeywordFound = False
        flag = 0

        Call GetKeywordLine(Keyword, ExtractType, KeywordLine, KeywordFound)

        If KeywordFound Then
            Call ScanLineForValue(Keyword, KeywordLine, ValueFound, auxstring)
            flag = 1
            value = Convert.ToInt32(auxstring)
        End If

    End Sub

    Public Sub GetDataLog(ByVal Keyword As String, ByRef value As Boolean, Optional ByVal ExtractType As Integer = 0, Optional ByRef flag As Integer = 0)

        'Local---------------------------------------------------
        Dim KeywordLine As Integer
        Dim AuxiliarString As String
        Dim ValueFound As Boolean
        Dim KeywordFound As Boolean
        Dim auxstring As String

        'Begin---------------------------------------------------

        KeywordFound = False
        flag = 0

        Call GetKeywordLine(Keyword, ExtractType, KeywordLine, KeywordFound)

        If KeywordFound Then
            Call ScanLineForValue(Keyword, KeywordLine, ValueFound, auxstring)
        End If

        If (auxstring = "0") Then
            value = False
        ElseIf (auxstring = "1") Then
            value = True
        End If

        If KeywordFound Then flag = 1

    End Sub

    Public Sub GetDataTime(ByVal Keyword As String, ByRef value As Date, Optional ByVal ExtractType As Integer = 0, Optional ByRef flag As Integer = 0)

        'Local---------------------------------------------------
        Dim KeywordLine As Integer
        Dim BeginReading As Integer
        Dim EndReading As Integer
        Dim DateString As String
        Dim Year, Month, Day, Hour, Minutes, Seconds, Miliseconds As Integer
        Dim Aux, BufferVector() As Single

        'Begin---------------------------------------------------

        flag = 0

        Call GetDataStr(Keyword, DateString, ExtractType, flag)

        ExtractVectorFromString(DateString, BufferVector)

        Year = Int(BufferVector(0))
        Month = Int(BufferVector(1))
        Day = Int(BufferVector(2))
        Hour = Int(BufferVector(3))
        Minutes = Int(BufferVector(4))
        Seconds = Int(BufferVector(5))
        Aux = (BufferVector(5) - Int(BufferVector(5))) * 1000
        Miliseconds = Int(Aux)

        Dim NewValue As New Date(Year, Month, Day, Hour, Minutes, Seconds, Miliseconds)
        value = NewValue

    End Sub

    Public Sub GetDataLine(ByVal LineNumber As Integer, ByRef value As Double)

        value = Val(Buffer(LineNumber))

    End Sub

    Public Sub GetFullLine(ByVal LineNumber As Integer, ByRef value As String)

        value = Buffer(LineNumber)

    End Sub

    Public Sub GetReadingLimits(ByRef BeginReading As Integer, ByRef EndReading As Integer, ByVal ExtractType As Integer)

        Select Case ExtractType

            Case FromFile

                BeginReading = 0
                EndReading = BufferSize

            Case FromBlock

                BeginReading = FirstBlockBufferLine
                EndReading = LastBlockBufferLine

            Case FromBlockFromBlock

                BeginReading = FirstBlockFromBlockBufferLine
                EndReading = LastBlockFromBlockBufferLine

            Case FromBlockFromBlockFromBlock

                BeginReading = FirstBlockFromBlockFromBlockBufferLine
                EndReading = LastBlockFromBlockFromBlockBufferLine

            Case Else

                BeginReading = 0
                EndReading = BufferSize

        End Select

    End Sub

    Public Sub ExtractVectorFromString(ByVal StringRead As String, ByRef Vector() As Single)

        Dim Buffer() As String
        Dim CurrentPosition As Integer
        Dim ValuesNumber, Number As Integer

        ValuesNumber = 0

        Buffer = Split(StringRead, " ")
        For CurrentPosition = LBound(Buffer) To UBound(Buffer)
            If Buffer(CurrentPosition) <> Nothing Then
                ValuesNumber = ValuesNumber + 1
            End If
        Next CurrentPosition

        ReDim Vector(ValuesNumber - 1)

        Number = 0
        For CurrentPosition = LBound(Buffer) To UBound(Buffer)
            If Buffer(CurrentPosition) <> Nothing Then
                Vector(Number) = Val(Buffer(CurrentPosition))
                Number = Number + 1
            End If
        Next CurrentPosition

    End Sub

    Private Sub GetKeywordLine(ByVal Keyword As String, ByVal ExtractType As Integer, ByRef KeywordLine As Integer, ByRef KeywordFound As Boolean)

        Dim BufferLine As Integer
        Dim BeginReading As Integer
        Dim EndReading As Integer

        KeywordFound = False

        Call GetReadingLimits(BeginReading, EndReading, ExtractType)

        For BufferLine = BeginReading To EndReading
            If (ScanLineForKeyword(Buffer(BufferLine), Trim(Keyword))) Then
                KeywordLine = BufferLine
                KeywordFound = True
                Exit For
            End If
        Next BufferLine


    End Sub

    Private Function ScanLineForKeyword(ByRef FullLine As String, ByRef Keyword As String) As Boolean

        'Local---------------------------------------------------
        Dim KeywordFound As Boolean
        Dim StringBuffer() As String
        'Begin---------------------------------------------------

        ScanLineForKeyword = False

        If FullLine = Nothing Then Exit Function

        'if no delimiter is present then StringBuffer = FullLine
        StringBuffer = Split(FullLine, Delimiter)

        'If Not Trim(StringBuffer(0)).Equals(Keyword) Then Exit Function
        If Not (StringBuffer(0).Trim).Equals(Keyword) Then Exit Function


        ScanLineForKeyword = True

    End Function

    Private Sub ScanLineForValue(ByVal Keyword As String, ByVal LineToScan As Integer, ByRef ValueFound As Boolean, ByRef StringAfterDelimiter As String)

        'Local---------------------------------------------------
        Dim FullLine As String
        Dim DelimiterPosition As Integer

        'Begin---------------------------------------------------

        ValueFound = False
        DelimiterPosition = 0

        'select line form buffer
        FullLine = Trim(Buffer(LineToScan))

        'find delimiter position in string
        DelimiterPosition = InStr(FullLine, Delimiter)

        'select 256 character string after delimiter and trim it
        StringAfterDelimiter = Trim(Mid(FullLine, DelimiterPosition + 1, Len(FullLine)))

        If StringAfterDelimiter = Nothing Then Exit Sub

        ValueFound = True

    End Sub

    Public Sub RewindBuffer(Optional ByVal ResetInnerBlock As Boolean = True)

        CurrentBufferLine = 0
        If ResetInnerBlock Then
            CurrentInnerBlockLine_1 = 0
        End If

    End Sub

    Public Sub ExtractStringVectorFromString(ByVal StringRead As String, ByRef StringVector() As String)

        Dim Buffer() As String
        Dim CurrentPosition As Integer
        Dim NumberOfStrings, Number As Integer

        NumberOfStrings = 0

        Buffer = Split(StringRead, " ")

        For CurrentPosition = LBound(Buffer) To UBound(Buffer)
            If Buffer(CurrentPosition) <> Nothing Then
                NumberOfStrings = NumberOfStrings + 1
            End If
        Next

        ReDim StringVector(NumberOfStrings - 1)

        Number = 0

        For CurrentPosition = LBound(Buffer) To UBound(Buffer)
            If Buffer(CurrentPosition) <> Nothing Then
                StringVector(Number) = Buffer(CurrentPosition)
                Number = Number + 1
            End If
        Next

    End Sub

End Class
