Imports System.IO
Imports Mohid_Base
Imports System.Net.Mail
Imports System.Timers
Imports System.Threading
Imports IntrinsicFunctions

Module ModuleLaunchProcess
    Sub LaunchProcess(ByVal processor_, ByVal SoftwareLabel)
        Dim Processor_exe As Process = New Process
        Dim stringOutput As String = ""

        With Processor_exe

            Try

                .StartInfo.FileName = processor_.exe
                If processor_.Arguments <> "" Then
                    .StartInfo.Arguments = processor_.Arguments
                End If
                .StartInfo.WorkingDirectory = Directory.GetParent(processor_.exe).ToString
                .StartInfo.WindowStyle = ProcessWindowStyle.Normal


                If processor_.ScreenOutputToFile = True Then
                    .StartInfo.UseShellExecute = False
                    .StartInfo.RedirectStandardOutput = True
                    Dim aux_path As String
                    If processor_.ScreenOutputPath = Nothing Then
                        aux_path = .StartInfo.WorkingDirectory
                    Else
                        aux_path = processor_.ScreenOutputPath
                    End If

                    Dim fileToSave As New StreamWriter(Path.Combine(aux_path, ("(" + SoftwareLabel + ")" + processor_.Name.ToString)) + "_" + _
                                                       Now.ToString("yyyy-MM-dd_HHmmss") + ".log")
                    fileToSave.AutoFlush = True

                    LogThis("Executing Tool: " + processor_.Name + "...")
                    .Start()

                    While Not .StandardOutput.EndOfStream
                        stringOutput = .StandardOutput.ReadLine
                        fileToSave.WriteLine(stringOutput)
                    End While
                    fileToSave.Close()
                Else
                    LogThis("Executing Tool: " + processor_.Name + "...")
                    .Start()
                End If

                .WaitForExit(1000 * processor_.MaxTime)
                If Not .HasExited Then
                    .Kill()
                End If
            Catch ex As Exception
                Call UnSuccessfullEnd("Batch file: " + processor_.exe + " could not be executed.")
            End Try
        End With

        LogThis("Done!")
    End Sub

End Module
