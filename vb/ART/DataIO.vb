Imports System.IO
Imports Mohid_Base
Public Class DataIO
    Dim AlignAt As Integer = 30
    Private Const Delimiter As String = ":"
    Private ExtractType As Integer
    Public Sub ChangeStream(ByVal Keyword As String, ByVal NewValue As String, ByVal DataFile As String)
        Dim outstream As String

        outstream = NewDataLine(Keyword, NewValue)
        Call ChangeStream2(Keyword, DataFile, outstream)

    End Sub

    Public Sub ChangeStream(ByVal Keyword As String, ByVal NewValue As Date, ByVal DataFile As String)
        Dim outstream As String

        outstream = NewDataLine(Keyword, NewValue)
        Call ChangeStream2(Keyword, DataFile, outstream)

    End Sub
    Public Sub ChangeStream(ByVal Keyword As String, ByVal NewValue As Boolean, ByVal DataFile As String)
        Dim outstream As String

        outstream = NewDataLine(Keyword, NewValue)
        Call ChangeStream2(Keyword, DataFile, outstream)

    End Sub
    Public Sub ChangeStream(ByVal Keyword As String, ByVal NewValue As Integer, ByVal DataFile As String)
        Dim outstream As String

        outstream = NewDataLine(Keyword, NewValue)
        Call ChangeStream2(Keyword, DataFile, outstream)

    End Sub
    Public Sub ChangeStream(ByVal Keyword As String, ByVal NewValue As Single, ByVal DataFile As String)
        Dim outstream As String

        outstream = NewDataLine(Keyword, NewValue)
        Call ChangeStream2(Keyword, DataFile, outstream)

    End Sub

    Private Sub ChangeStream2(ByVal Keyword As String, ByVal DataFile As String, ByVal outstream As String)
        Dim KeywordLine As Integer
        Dim KeywordFound As Boolean
        Dim enterdata1 As New EnterData(DataFile)
        Dim BeginReading As Integer
        Dim EndReading As Integer
        Dim StreamBefore As String
        Dim StreamAfter As String
        Dim Stream As String
        Dim i As Integer
        Dim BufferBefore(), BufferAfter() As String
        Dim DataF As StreamWriter

        Call enterdata1.GetReadingLimits(BeginReading, EndReading, ExtractType)

        KeywordFound = False
        Call GetKeywordLine(DataFile, BeginReading, EndReading, Keyword, ExtractType, KeywordLine, KeywordFound)

        ReDim BufferBefore(KeywordLine)
        ReDim BufferAfter(EndReading - KeywordLine)

        For i = BeginReading To EndReading
            If i < KeywordLine Then
                enterdata1.GetFullLine(i, BufferBefore(i))
            ElseIf i > KeywordLine Then
                enterdata1.GetFullLine(i, BufferAfter(i - KeywordLine))
            End If
        Next

        StreamBefore = String.Join(vbCrLf, BufferBefore, 1, KeywordLine)
        StreamAfter = String.Join(vbCrLf, BufferAfter)

        Stream = StreamBefore + outstream + StreamAfter

        ' Create new File (note: False means that data will not be appended to file)
        DataF = New StreamWriter(DataFile, False, System.Text.Encoding.Default)
        DataF.Write(Stream)
        DataF.Close()
    End Sub
    Private Sub GetKeywordLine(ByVal DataFile As String, ByVal BeginReading As Integer, ByVal EndReading As Integer, ByVal Keyword As String, ByVal ExtractType As Integer, ByRef KeywordLine As Integer, ByRef KeywordFound As Boolean)
        Dim enterdata1 As New EnterData(DataFile)

        Dim Buffer() As String
        Dim BufferLine As Integer
        Dim i As Integer

        KeywordFound = False
        ReDim Buffer(EndReading)

        For i = BeginReading To EndReading
            enterdata1.GetFullLine(i, Buffer(i))
        Next


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

    Public Function NewDataLine(ByVal Keyword As String, ByVal value As String)

        Dim StringLength, NumberofSpaces As Integer

        StringLength = Len(Keyword)
        NumberofSpaces = AlignAt - StringLength

        NewDataLine = (Keyword & Space(NumberofSpaces) & ": " & value)

    End Function

    Public Function NewDataLine(ByVal Keyword As String, ByVal value As Boolean)

        Dim StringLength, NumberofSpaces As Integer
        Dim AuxString As String

        StringLength = Len(Keyword)
        NumberofSpaces = AlignAt - StringLength

        If Not value Then
            AuxString = "0"
        ElseIf value Then
            AuxString = "1"
        End If

        NewDataLine = (Keyword & Space(NumberofSpaces) & ": " & AuxString)

    End Function

    Public Function NewDataLine(ByVal Keyword As String, ByVal value As Integer)

        Dim StringLength, NumberofSpaces As Integer
        Dim AuxString As String

        StringLength = Len(Keyword)
        NumberofSpaces = AlignAt - StringLength
        AuxString = Str(value)

        NewDataLine = (Keyword & Space(NumberofSpaces) & ": " & AuxString)

    End Function

    Public Function NewDataLine(ByVal Keyword As String, ByVal value As Single)

        Dim StringLength, NumberofSpaces As Integer
        Dim AuxString As String

        StringLength = Len(Keyword)
        NumberofSpaces = AlignAt - StringLength

        AuxString = Str(value)

        NewDataLine = (Keyword & Space(NumberofSpaces) & ": " & AuxString)

    End Function

    Public Function NewDataLine(ByVal Keyword As String, ByVal Time As Date)

        Dim StringLength, NumberofSpaces As Integer

        StringLength = Len(Keyword)
        NumberofSpaces = AlignAt - StringLength

        NewDataLine = (Keyword & Space(NumberofSpaces) & ": " & _
                        Time.Year.ToString + " " + Time.Month.ToString + " " + _
                        Time.Day.ToString + " " + Time.Hour.ToString + " " + _
                        Time.Minute.ToString + " " + Time.Second.ToString)

    End Function


End Class
