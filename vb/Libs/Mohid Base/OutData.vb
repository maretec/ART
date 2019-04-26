Imports System.IO
Public Class OutData

    Dim AlignAt As Integer = 30
    Dim DataF As StreamWriter
    Private Const BlankLine As String = ""

    Public Sub New(ByVal FileName As String)
        MyBase.new()

        ' Create new File (note: False means that data will not be appended to file)
        DataF = New StreamWriter(FileName, False, System.Text.Encoding.Default)

    End Sub

    Public Sub WriteDataLine(ByVal value As String)

        DataF.WriteLine(value)

    End Sub

    Public Sub WriteDataLine(ByVal value As Single)

        DataF.WriteLine(value)

    End Sub

    Public Sub WriteDataLine(ByVal value As Double)

        DataF.WriteLine(value)

    End Sub

    Public Sub WriteDataLine(ByVal Keyword As String, ByVal value As String)

        Dim StringLength, NumberofSpaces As Integer

        StringLength = Len(Keyword)
        NumberofSpaces = AlignAt - StringLength

        DataF.WriteLine(Keyword & Space(NumberofSpaces) & ": " & value)

    End Sub

    Public Sub WriteDataLine(ByVal Keyword As String, ByVal value As Boolean)

        Dim StringLength, NumberofSpaces As Integer
        Dim AuxString As String

        StringLength = Len(Keyword)
        NumberofSpaces = AlignAt - StringLength

        If Not value Then
            AuxString = "0"
        ElseIf value Then
            AuxString = "1"
        End If

        DataF.WriteLine(Keyword & Space(NumberofSpaces) & ": " & AuxString)

    End Sub

    Public Sub WriteDataLine(ByVal Keyword As String, ByVal value As Integer)

        Dim StringLength, NumberofSpaces As Integer
        Dim AuxString As String

        StringLength = Len(Keyword)
        NumberofSpaces = AlignAt - StringLength
        AuxString = Str(value)

        DataF.WriteLine(Keyword & Space(NumberofSpaces) & ": " & AuxString)

    End Sub

    Public Sub WriteDataLine(ByVal Keyword As String, ByVal value As Single)

        Dim StringLength, NumberofSpaces As Integer
        Dim AuxString As String

        StringLength = Len(Keyword)
        NumberofSpaces = AlignAt - StringLength

        AuxString = Str(value)

        DataF.WriteLine(Keyword & Space(NumberofSpaces) & ": " & AuxString)

    End Sub
    Public Sub WriteDataLine(ByVal Keyword As String, ByVal value As Double)

        Dim StringLength, NumberofSpaces As Integer
        Dim AuxString As String

        StringLength = Len(Keyword)
        NumberofSpaces = AlignAt - StringLength

        AuxString = Str(value)

        DataF.WriteLine(Keyword & Space(NumberofSpaces) & ": " & AuxString)

    End Sub
    Public Sub WriteDataLine(ByVal Keyword As String, ByVal Time As Date)

        Dim StringLength, NumberofSpaces As Integer

        StringLength = Len(Keyword)
        NumberofSpaces = AlignAt - StringLength

        DataF.WriteLine(Keyword & Space(NumberofSpaces) & ": " & _
                        Time.Year.ToString + " " + Time.Month.ToString + " " + _
                        Time.Day.ToString + " " + Time.Hour.ToString + " " + _
                        Time.Minute.ToString + " " + Time.Second.ToString)

    End Sub

    Public Sub WriteBlankLine()

        DataF.WriteLine(BlankLine)

    End Sub
    Public Sub Finish()

        DataF.Close()

    End Sub

    Public Sub Flush()

        DataF.Flush()

    End Sub

End Class
