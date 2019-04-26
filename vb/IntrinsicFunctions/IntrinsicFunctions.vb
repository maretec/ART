Imports System.IO
Imports System.Threading
Imports Microsoft.Win32
Imports System.Text.RegularExpressions
Imports System.Net
Imports Mohid_Base
Imports System.Net.Mail
Imports IntrinsicFunctions
Imports System.Security.Cryptography
Imports System.Management
Imports System.Text


Public Class IntrinsicFunctions
    Private Shared RandomControl As Integer
    Private Shared FlagForTriggerFile As String
    Public Shared MailServer As String = "smtp.gmail.com"
    Public Shared MailSender As String = "ART for MOHID Water"
    Public Shared MailSenderAddress As String = "mailing.maretec@gmail.com"
    Public Shared TimeToWaitOnCopy As Integer = 0
    Public Shared IterationTimeOnCopy As Integer = 60
    Public Shared EmailsList() As String
    Private Shared LogFile As OutData
    Private Shared LogFileName As String
    Private Shared UserLicenseKey As String
    Private Shared DecryptedLicenseKey As String
    Private Shared PlainUserKey As String
    Public Shared AcceptableFailure As Boolean
    Private Shared EncryptionKey As String
    Public Shared License_TimePeriod As Double
    Public Shared License_SimulationType As String
    Public Shared InitialDateStr As String
    Public Shared FinalDateStr As String
    Public Shared InitialDate As Date
    Public Shared FinalDate As Date
    Public Shared NumberOfRuns As Integer = 1





    Public Shared Sub Read_Instrinsic_Variables(ByVal InputFile As EnterData, ByVal LogFile As OutData, ByVal LogFileName_ As String)

        Dim StartLine, EndLine, ListSize, i, iLine As Integer

        LogFileName = LogFileName_
        'rewind buffer, to be able to read input data file since the beginning
        InputFile.RewindBuffer(True)

        InputFile.GetDataStr("MAIL_SERVER", MailServer)
        InputFile.GetDataStr("MAIL_SENDER_NAME", MailSender)
        InputFile.GetDataStr("MAIL_SENDER_ADDRESS", MailSenderAddress)
        InputFile.GetDataStr("LICENSE_KEY", UserLicenseKey)
        InputFile.GetDataInteger("TIME_TO_WAIT_ON_COPY", TimeToWaitOnCopy)
        If TimeToWaitOnCopy > 0 Then
            InputFile.GetDataInteger("ITERATION_TIME_ON_COPY", IterationTimeOnCopy)
        End If
        Call Read_E_Mails_List(InputFile)

        DecryptedLicenseKey = Decrypt(UserLicenseKey)
        PlainUserKey = GetPlainLicenseKey()
        If DecryptedLicenseKey = PlainUserKey Then
            Call GetLicenseType()
            If ValidLicenseTimePeriod() = False Then
                Call UnSuccessfullEnd("Invalid License Key (time period expired)")
            End If
        Else
            '!!!!!!!!!!TO REMOVE!!!!!!!!!!!!!!!!!!!!
            '           Call UnSuccessfullEnd("Invalid License Key.")
            LogThis("Invalid License Key.")
        End If
    End Sub

    Private Shared Function GetExternalIp() As String
        Try
            Dim client As WebClient = New WebClient()
            client.Proxy = Nothing
            Dim ExternalIP As String
            ExternalIP = client.DownloadString("http://checkip.dyndns.org/")
            ExternalIP = (New Regex("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")) _
                         .Matches(ExternalIP)(0).ToString()
            Return ExternalIP
        Catch
            Return Nothing
        End Try
    End Function

    Public Shared Sub CheckLicenseStatus()
        '-------------------------Check Licence Status
        Dim r As New Random
        Dim Status As String
        RandomControl = r.Next()

        Dim registryKey As RegistryKey
        registryKey = Registry.LocalMachine
        Dim registrySubKey As RegistryKey

        registrySubKey = Registry.LocalMachine.OpenSubKey("SOFTWARE\ART\KEY", True)

        'the first run must create a key.
        If registrySubKey Is Nothing Then
            registrySubKey = registryKey.CreateSubKey("SOFTWARE\ART\KEY")
            registrySubKey.SetValue("ART_FIRSTRUN", Now.Date.ToString("yyyy-MM-dd"))
        End If

        ' to delete
        'If registrySubKey.GetValue("ART_FIRSTRUN") <> Nothing Then
        '    registryKey.DeleteSubKey("SOFTWARE\ART\KEY")
        'End If
        'End

        Dim FirstRun As Date

        Dim MyIP As String
        Dim AcceptedIPList As New Collection
        Dim LicenseStatus As String = "rejected"
        AcceptedIPList.Add("193.136.129.227")

        MyIP = GetExternalIp()

        If MyIP <> Nothing Then
            For Each IP In AcceptedIPList
                If IP = MyIP Then
                    LicenseStatus = "accepted"
                    registrySubKey.SetValue("ART_FIRSTRUN", "9999-01-01")
                    Exit For
                End If
            Next
            If LicenseStatus = "rejected" Then
                Status = "Unlicensed version (public IP not authorized)"
            End If
        Else ' if no internet is available, program runs
            LicenseStatus = "unknown"
            registrySubKey.SetValue("ART_FIRSTRUN", Now.Date.ToString("yyyy-MM-dd"))
        End If

        If registrySubKey.GetValue("ART_FIRSTRUN") Is Nothing Then
            'LogThis("ART is not able to change or check licence version")
            Status = "AcceptableFailure"
        Else
            FirstRun = registrySubKey.GetValue("ART_FIRSTRUN")

            ' program will stop if workstation has been more than one week without internet 
            If LicenseStatus = "unknown" Then
                If FirstRun > Now Then ' last run was with licence accepted
                    registrySubKey.SetValue("ART_FIRSTRUN", Now.Date.ToString("yyyy-MM-dd"))
                Else ' last run was already with licence unknown
                    If (Now - FirstRun).Days > 7 Then
                        Status = "Unlicensed version (public IP could not be verified for more than 7 days (" + (Now - FirstRun).Days.ToString + " days exactly)"
                    End If
                End If
            End If

        End If

        '--------------------------------------------

    End Sub

    Public Shared Sub FileCopy(ByVal SourceFileName As String, ByVal DestinationFileName As String, ByVal ErrorMessage As String, ByVal Critical As Boolean)
        Dim SuccessfullCopy As Boolean = False
        Dim StartingInstant As DateTime
        Dim ErrorInternalMessage As String = ""
        If TimeToWaitOnCopy > 0 Then
            StartingInstant = Now

            While Now < StartingInstant.AddSeconds(TimeToWaitOnCopy)
                Try
                    IO.File.Copy(SourceFileName, DestinationFileName, True)
                    SuccessfullCopy = True
                    Exit While
                Catch ex As Exception
                    ErrorInternalMessage = ex.Message
                    SuccessfullCopy = False
                    Thread.Sleep(IterationTimeOnCopy * 1000)
                End Try
            End While
            If SuccessfullCopy = False Then
                If Critical Then
                    UnSuccessfullEnd(ErrorMessage, ErrorInternalMessage)
                Else
                    LogThis(ErrorMessage)
                    AcceptableFailure = True
                End If
            End If
        Else
            Try
                IO.File.Copy(SourceFileName, DestinationFileName, True)
            Catch ex As Exception
                If Critical Then
                    UnSuccessfullEnd(ErrorMessage, ex.Message)
                Else
                    LogThis(ErrorMessage)
                    AcceptableFailure = True
                End If
            End Try
        End If
    End Sub

    Public Shared Sub UnSuccessfullEnd(ByVal Message As String, Optional ByVal MessageOnBody As String = "")

        LogThis(Message, MessageOnBody)

        LogThis("FAILURE OF TODAYS FORECAST!")

        Call CloseLogFile()
        If MessageOnBody = "" Then
            MessageOnBody = Now.ToString("yyyy-MM-dd HH-mm-ss")
        End If
        Call SendLogEmail(Message, MessageOnBody, False)

        If IO.File.Exists(FlagForTriggerFile) Then
            IO.File.Delete(FlagForTriggerFile)
        End If
        Environment.Exit(1)
    End Sub


    Public Shared Sub CloseLogFile()

        LogFile.Finish()

    End Sub

    Public Shared Sub LogThis(ByVal This As String, Optional ByVal AdditionalInformation As String = "", Optional ByVal LogFile_ As OutData = Nothing)

        Dim TimeStamp As String = Now.ToString("yyyy-MM-dd HH:mm:ss")
        Dim Message As String = TimeStamp + " -> " + This

        If Not LogFile_ Is Nothing Then
            LogFile = LogFile_
        End If

        Console.WriteLine(Message)
        LogFile.WriteDataLine(Message)

        If AdditionalInformation <> "" Then
            Console.WriteLine(TimeStamp + " -> (" + AdditionalInformation + ")")
            LogFile.WriteDataLine(TimeStamp + "   -> (" + AdditionalInformation + ")")
        End If

        LogFile.Flush()

    End Sub

    Public Shared Sub SendLogEmail(ByVal Subject As String, ByVal Body As String, ByVal Success As Boolean, Optional ByVal MOHID_Run_LogFile_FullPath As String = Nothing, Optional ByVal MOHID_Run_LogFile_FullPath_In_Network As String = Nothing)

        'create the mail message
        Dim mail As New MailMessage()

        'set the addresses
        mail.From = New MailAddress(MailSenderAddress, MailSender)
        For Each EmailAddress As String In EmailsList
            mail.To.Add(EmailAddress)
        Next

        'set the content
        If AcceptableFailure Then
            mail.Subject = Subject + " - Small failures - SEE LOG FILE"
        Else
            mail.Subject = Subject
        End If

        If FileInUse(LogFileName) Then
            Dim auxfile As String
            Dim stream_ As FileStream
            stream_ = New FileStream(LogFileName, FileMode.Open, FileAccess.Read, FileShare.ReadWrite)
            auxfile = Path.GetFileName(LogFileName)

            mail.Attachments.Add(New Attachment(stream_, auxfile))
        Else
            mail.Attachments.Add(New Attachment(LogFileName))
        End If

        If IO.File.Exists(MOHID_Run_LogFile_FullPath) And Not Success Then
            Dim mohid_run_file As IO.FileInfo = New IO.FileInfo(MOHID_Run_LogFile_FullPath)
            If mohid_run_file.Length < 100000 Then
                mail.Attachments.Add(New Attachment(MOHID_Run_LogFile_FullPath))
            Else
                Body = Body + vbCrLf + "Check Mohid Run log file in " + MOHID_Run_LogFile_FullPath_In_Network
            End If
            mohid_run_file = Nothing
        End If

        mail.Body = Body

        If Success Then
            If AcceptableFailure Then
                mail.Priority = MailPriority.High
            Else
                mail.Priority = MailPriority.Normal
            End If
        Else
            mail.Priority = MailPriority.High
        End If

        'send the message
        Dim smtp As New SmtpClient
        smtp.EnableSsl = True
        'Dim PassManager As New PM()
        '        smtp.Credentials = New System.Net.NetworkCredential(PassManager.Login, PassManager.Password)
        smtp.Credentials = New System.Net.NetworkCredential("mailing.maretec@gmail.com", "Maretec2004")
        smtp.Port = 587
        smtp.Host = MailServer.ToString
        smtp.DeliveryMethod = SmtpDeliveryMethod.Network
        Try
            smtp.Send(mail)
            mail.Attachments.Clear()
            mail.To.Clear()

        Catch ex As Exception
            Console.WriteLine(ex.Message.ToString())
        End Try


    End Sub

    Public Shared Sub SendEmail(ByVal Subject As String, ByVal Body As String, ByVal HighPriority As Boolean)

        'create the mail message
        Dim mail As New MailMessage()

        'set the addresses
        mail.From = New MailAddress(MailSenderAddress, MailSender)
        For Each EmailAddress As String In EmailsList
            mail.To.Add(EmailAddress)
        Next

        'set the content
        mail.Subject = Subject
        mail.Body = Body
        If HighPriority Then
            mail.Priority = MailPriority.High
        Else
            mail.Priority = MailPriority.Normal
        End If

        'send the message
        Dim smtp As New SmtpClient
        smtp.EnableSsl = True
        'Dim PassManager As New PM()
        '        smtp.Credentials = New System.Net.NetworkCredential(PassManager.Login, PassManager.Password)
        smtp.Credentials = New System.Net.NetworkCredential("mailing.maretec@gmail.com", "Maretec2004")
        smtp.Port = 587
        smtp.Host = MailServer.ToString
        smtp.DeliveryMethod = SmtpDeliveryMethod.Network
        Try
            smtp.Send(mail)
            mail.Attachments.Clear()
            mail.To.Clear()

        Catch ex As Exception
            Console.WriteLine(ex.Message.ToString())
        End Try


    End Sub

    Public Shared Sub Read_E_Mails_List(ByVal File As EnterData)

        Dim StartLine, EndLine, ListSize, i, iLine As Integer

        'rewind buffer, to be able to read input data file since the beginning
        File.RewindBuffer(True)
        File.ExtractBlockFromBuffer("<begin_out_email_list>", "<end_out_email_list>", EnterData.FromFile)

        File.GetReadingLimits(StartLine, EndLine, EnterData.FromBlock)

        ListSize = EndLine - StartLine - 2

        ReDim EmailsList(ListSize)
        i = 0
        For iLine = StartLine + 1 To EndLine - 1
            File.GetFullLine(iLine, EmailsList(i))
            i = i + 1
        Next

    End Sub
    Public Shared Function FileInUse(ByVal sFile As String) As Boolean
        If System.IO.File.Exists(sFile) Then
            Try
                Dim F As Short = FreeFile()
                FileOpen(F, sFile, OpenMode.Binary, OpenAccess.ReadWrite, OpenShare.LockReadWrite)
                FileClose(F)
            Catch
                Return True
            End Try
        End If
    End Function

    Private Shared Function Decrypt(ByVal cipherText As String) As String
        EncryptionKey = Right(cipherText, 16) + "ART"
        cipherText = Left(cipherText, cipherText.Length - 16)
        Dim cipherBytes As Byte() = Convert.FromBase64String(cipherText)
        Using encryptor As Aes = Aes.Create()
            Dim pdb As New Rfc2898DeriveBytes(EncryptionKey, New Byte() {&H49, &H76, &H61, &H6E, &H20, &H4D, _
             &H65, &H64, &H76, &H65, &H64, &H65, _
             &H76})
            encryptor.Key = pdb.GetBytes(32)
            encryptor.IV = pdb.GetBytes(16)
            Using ms As New MemoryStream()
                Using cs As New CryptoStream(ms, encryptor.CreateDecryptor(), CryptoStreamMode.Write)
                    cs.Write(cipherBytes, 0, cipherBytes.Length)
                    cs.Close()
                End Using
                cipherText = Encoding.Unicode.GetString(ms.ToArray())
            End Using
        End Using
        Return cipherText
    End Function

    Private Shared Function GetPlainLicenseKey()
        Dim ProcessorID As String
        Dim DiskDriveID As String
        Dim PlainKey As String
        Dim processor1 As New ManagementObjectSearcher("SELECT * FROM Win32_Processor")
        For Each processor_ In processor1.Get
            'stop_time = Now
            'elapsed_time = stop_time.Subtract(start_time)
            ProcessorID += processor_("ProcessorID").ToString
            'MsgBox("time elapsed2: " + elapsed_time.TotalSeconds.ToString("0.000000"))
            'MsgBox(processor_("ProcessorID").ToString())
            'Exit For
        Next

        Dim hdd As New ManagementObjectSearcher("SELECT * FROM Win32_DiskDrive WHERE DeviceID='\\\\.\\PHYSICALDRIVE0'")

        For Each hd In hdd.Get
            'DiskDriveID = hd("SerialNumber").ToString
            DiskDriveID = hd("SerialNumber").ToString.Replace(" ", "+")
            'MsgBox(hd("SerialNumber"))
            Exit For
        Next

        Dim SystemID As String
        Dim LicenseID As String
        Dim DecimalPart As Double
        Dim LengthToAdd As Integer
        Dim StringToAdd As String = ""
        SystemID = ProcessorID + DiskDriveID
        LicenseID = Left(EncryptionKey, 16)
        DecimalPart = Math.Abs(((Len(SystemID) + Len(LicenseID)) / 4) - Math.Round((Len(SystemID) + Len(LicenseID)) / 4, 0))

        If DecimalPart <> 0 Then
            LengthToAdd = (1 - DecimalPart) * 4

            For i = 1 To LengthToAdd
                StringToAdd += "1"
            Next
        End If

        PlainKey = ProcessorID + DiskDriveID + StringToAdd + Left(EncryptionKey, 16)
        Return PlainKey
    End Function

    Private Shared Sub GetLicenseType()
        Dim InputString As String = Mid(EncryptionKey, 15, 2)
        Dim SimulationType As String = Left(InputString, 1)
        Dim TimePeriod As String = Right(InputString, 1)

        Select Case SimulationType
            Case "1"
                License_SimulationType = "HINDCAST"
            Case "2"
                License_SimulationType = "HINDCAST/NOWCAST"
            Case "3"
                License_SimulationType = "HINDCAST/NOWCAST/FORECAST"
                '            Case Else
                '                UnSuccessfullEnd()
        End Select

        Select Case TimePeriod
            Case "1"
                License_TimePeriod = 90
            Case "2"
                License_TimePeriod = 180
            Case "3"
                License_TimePeriod = 365
            Case "4"
                License_TimePeriod = 100000000000
                'Case Else
                '     UnSuccessfullEnd()
        End Select

    End Sub

    Private Shared Function ValidLicenseTimePeriod()
        Dim InstantNow As DateTime = Now
        Dim InstantFromEncryptionKey As DateTime
        Dim InstantFromEncryptionKey_str As String = Left(EncryptionKey, 14)
        Dim Valid As Boolean = False
        InstantFromEncryptionKey = Left(InstantFromEncryptionKey_str, 4) + "-" + _
                                    Mid(InstantFromEncryptionKey_str, 5, 2) + "-" + _
                                    Mid(InstantFromEncryptionKey_str, 7, 2) + " " + _
                                    Mid(InstantFromEncryptionKey_str, 9, 2) + ":" + _
                                    Mid(InstantFromEncryptionKey_str, 11, 2) + ":" + _
                                    Mid(InstantFromEncryptionKey_str, 13, 2)
        If License_TimePeriod <= 1000 Then
            If InstantFromEncryptionKey.AddDays(License_TimePeriod) < Now Then
                Valid = False
            Else
                Valid = True
            End If
        Else
            Valid = True
        End If
        Return Valid
    End Function

    Private Shared Function ValidLicenseSimulationType()
        Dim Valid As Boolean = False
        Dim NowDate As Date = New Date(Now.Date.Year, Now.Date.Month, Now.Date.Day, 0, 0, 0)
        Select Case License_SimulationType
            Case "HINDCAST"
                If InitialDate < NowDate And FinalDate < NowDate Then
                    Valid = True
                Else
                    Valid = False
                End If
            Case "HINDCAST/NOWCAST"
                If FinalDate <= NowDate.AddDays(1) Then
                    Valid = True
                Else
                    Valid = False
                End If
            Case "HINDCAST/NOWCAST/FORECAST"
                Valid = True
        End Select


        Return Valid

    End Function
    Public Shared Sub StartingForecast(ByVal i As Integer)
        InitialDateStr = InitialDate.ToString("yyyy-MM-dd")
        FinalDateStr = FinalDate.ToString("yyyy-MM-dd")

        LogThis("----------------------------------------------------")
        LogThis("------------STARTING FORECAST (" + i.ToString + " of " + NumberOfRuns.ToString + " )-------------")
        LogThis("Forecast initial date : " + InitialDate.ToString("yyyy-MM-dd"))
        LogThis("Forecast final date : " + FinalDate.ToString("yyyy-MM-dd"))

        If ValidLicenseSimulationType() = False Then
            '!!!!!!!!!!TO REMOVE!!!!!!!!!!!!!!!!!!!!
            'UnSuccessfullEnd("License not valid - simulation period out of the scope of the license")

        End If

    End Sub


End Class
