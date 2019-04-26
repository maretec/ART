Imports System.Math
Imports System.Drawing
Public Class GlobalFunctions

    Public Const FillValueReal As Single = -9.9E+15
    Public Const FillValueInt As Long = -9.9E+15

    Public Shared Sub RotateAndTranslatePoint(ByVal OriginX As Single, ByVal OriginY As Single, ByVal Alpha As Single, ByRef Point As PointF)

        'Local-----------------------------------------------------------------
        Dim Radianos, A11, A12, A21, A22, X_TEMP, Y_TEMP As Double

        '
        If (Alpha = 0.0) Then
            Point.X = Point.X + OriginX
            Point.Y = Point.Y + OriginY
        Else
            Radianos = Alpha * Math.PI / 180.0
            A11 = Cos(Radianos)
            A12 = -Cos(Math.PI / 2.0 - Radianos)
            A21 = Sin(Radianos)
            A22 = Sin(Math.PI / 2.0 - Radianos)
            X_TEMP = OriginX + A11 * Point.X + A12 * Point.Y
            Y_TEMP = OriginY + A21 * Point.X + A22 * Point.Y

            Point.X = CType(X_TEMP, Single)
            Point.Y = CType(Y_TEMP, Single)

        End If

    End Sub

    'Public Shared Function RainbowColor(ByVal Value As Single, _
    '                                    ByVal MinValue As Single, ByVal MaxValue As Single, _
    '                                    ByVal AlphaValue As Single) As Color

    '    Dim Red, Green, Blue As Single
    '    Dim dRange As Single
    '    Dim lInf1, lInf2, lInf3, lInf4 As Single
    '    Dim lSup1, lSup2, lSup3, lSup4 As Single

    '    AlphaValue = AlphaValue * 255

    '    If (Value < MinValue) Then
    '        RainbowColor = Color.FromArgb(CInt(AlphaValue), 0, 0, 0)
    '        Exit Function
    '    ElseIf (Value > MaxValue) Then
    '        RainbowColor = Color.FromArgb(CInt(AlphaValue), 255, 255, 255)
    '        Exit Function
    '    End If

    '    If MinValue = MaxValue Then
    '        RainbowColor = Color.Blue
    '        Exit Function
    '    End If

    '    'Computes the drange
    '    dRange = (MaxValue - MinValue) / 4.0

    '    lInf1 = MinValue
    '    lSup1 = lInf1 + dRange

    '    lInf2 = lSup1
    '    lSup2 = lInf2 + dRange

    '    lInf3 = lSup2
    '    lSup3 = lInf3 + dRange

    '    lInf4 = lSup3
    '    lSup4 = lInf4 + dRange

    '    If (Value >= lInf1 And Value < lSup1) Then

    '        '!Interpolates(Blue(0, 0, 1) / Cyan(0, 1, 1))
    '        Red = 0.0
    '        Green = (Value - lInf1) / dRange
    '        Blue = 1.0

    '    ElseIf (Value >= lInf2 And Value < lSup2) Then

    '        '!Interpolates(Cyan(0, 1, 1) / Green(0, 1, 0))
    '        Red = 0.0
    '        Green = 1.0
    '        Blue = 1.0 - (Value - lInf2) / dRange

    '    ElseIf (Value >= lInf3 And Value < lSup3) Then

    '        '!Interpolates(Green(0, 1, 0) / Yellow(1, 1, 0))
    '        Red = (Value - lInf3) / dRange
    '        Green = 1.0
    '        Blue = 0.0

    '    Else

    '        '!Interpolates(Yellow(1, 1, 0) / Red(1, 0, 0))
    '        Red = 1.0
    '        Green = 1.0 - (Value - lInf4) / dRange
    '        Blue = 0.0

    '    End If

    '    RainbowColor = Color.FromArgb(AlphaValue, Red * 255, Green * 255, Blue * 255)

    'End Function

    Public Shared Function ExtractNameFromFullPath(ByVal FullPath As String) As String

        ExtractNameFromFullPath = Mid(FullPath, InStrRev(FullPath, "\") + 1, Len(FullPath) - InStrRev(FullPath, "\"))

    End Function

    Public Shared Function LinearInterpolation(ByVal x1 As Single, ByVal y1 As Single, ByVal x2 As Single, ByVal y2 As Single, ByVal xc As Single) As Single

        Dim dist1, dist2 As Single

        If (x2 > x1) Then
            dist1 = xc - x1
            dist2 = x2 - xc
        Else
            dist1 = xc - x2
            dist2 = x1 - xc
        End If
        Return (dist2 * y1 + dist1 * y2) / (dist1 + dist2)

    End Function

    Public Shared Function LogaritmicInterpolation(ByVal x1 As Single, ByVal y1 As Single, ByVal x2 As Single, ByVal y2 As Single, ByVal xc As Single) As Single

        Dim dist1, dist2 As Single

        If x1 <= 0 Or x2 <= 0 Then Exit Function

        If (x2 > x1) Then
            dist1 = Log(xc) - Log(x1)
            dist2 = Log(x2) - Log(xc)
        Else
            dist1 = Log(xc) - Log(x2)
            dist2 = Log(x1) - Log(xc)
        End If
        Return (dist2 * y1 + dist1 * y2) / (dist1 + dist2)


    End Function

    Public Shared Function InterpolateCenterToVertex(ByVal CenterMatrix(,) As Single, ByVal MapMatrix(,) As Boolean, _
                                                     Optional ByVal FillValueMin As Single = Single.MinValue, _
                                                     Optional ByVal FillValueMax As Single = Single.MaxValue) As Single(,)

        'Gets(Size)
        Dim IUB As Integer = CenterMatrix.GetUpperBound(0)
        Dim JUB As Integer = CenterMatrix.GetUpperBound(1)
        Dim i, j As Integer
        Dim Sumpoints As Single
        Dim Value As Single
        Dim HaveLand As Boolean

        Dim VertexMatrix(IUB + 1, JUB + 1) As Single

        For i = 0 To IUB + 1
            For j = 0 To JUB + 1

                Sumpoints = 0
                Value = 0.0
                HaveLand = False

                '(i, j)
                If (i <= IUB And j <= JUB) Then
                    If (CenterMatrix(i, j) > FillValueMin And CenterMatrix(i, j) < FillValueMax) Then
                        Sumpoints = Sumpoints + 1
                        Value = Value + CenterMatrix(i, j)
                    End If
                End If

                '(i-1, j)
                If (i > 0 And j <= JUB) Then
                    If (CenterMatrix(i - 1, j) > FillValueMin And CenterMatrix(i - 1, j) < FillValueMax) Then
                        Sumpoints = Sumpoints + 1
                        Value = Value + CenterMatrix(i - 1, j)
                    End If
                End If

                '(i-1, j-1)
                If (i > 0 And j > 0) Then
                    If (CenterMatrix(i - 1, j - 1) > FillValueMin And CenterMatrix(i - 1, j - 1) < FillValueMax) Then
                        Sumpoints = Sumpoints + 1
                        Value = Value + CenterMatrix(i - 1, j - 1)
                    End If
                End If

                '(i, j-1)
                If (j > 0 And i <= IUB) Then
                    If (CenterMatrix(i, j - 1) > FillValueMin And CenterMatrix(i, j - 1) < FillValueMax) Then
                        Sumpoints = Sumpoints + 1
                        Value = Value + CenterMatrix(i, j - 1)
                    End If
                End If

                If (i = IUB + 1) Then
                    If (j <= JUB) Then
                        If (CenterMatrix(i - 1, j) > FillValueMin And CenterMatrix(i - 1, j) < FillValueMax) Then
                            Sumpoints = Sumpoints + 1
                            Value = Value + CenterMatrix(i - 1, j)
                        End If
                    End If
                    If (j > 0) Then
                        If (CenterMatrix(i - 1, j - 1) > FillValueMin And CenterMatrix(i - 1, j - 1) < FillValueMax) Then
                            Sumpoints = Sumpoints + 1
                            Value = Value + CenterMatrix(i - 1, j - 1)
                        End If
                    End If
                End If

                If (j = JUB + 1) Then
                    If (i <= IUB) Then
                        If (CenterMatrix(i, j - 1) > FillValueMin And CenterMatrix(i, j - 1) < FillValueMax) Then
                            Sumpoints = Sumpoints + 1
                            Value = Value + CenterMatrix(i, j - 1)
                        End If
                    End If
                    If (i > 0) Then
                        If (CenterMatrix(i - 1, j - 1) > FillValueMin And CenterMatrix(i - 1, j - 1) < FillValueMax) Then
                            Sumpoints = Sumpoints + 1
                            Value = Value + CenterMatrix(i - 1, j - 1)
                        End If
                    End If
                End If

                If (Sumpoints > 0) Then
                    VertexMatrix(i, j) = Value / Sumpoints
                Else
                    VertexMatrix(i, j) = Single.MinValue
                End If
            Next
        Next

        Return VertexMatrix
    End Function


End Class
