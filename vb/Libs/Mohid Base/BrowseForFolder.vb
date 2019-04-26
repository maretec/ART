Option Strict On
Option Explicit On 

Imports System
Imports System.Runtime.InteropServices
Imports System.Diagnostics
Imports System.Text

Public Class FolderBrowser
    Private Const BFFM_INITIALIZED As Integer = 1
    Private Const BFFM_SELCHANGED As Integer = 2
    Private Const BFFM_VALIDATEFAILED As Integer = 3
    Private Const BFFM_ENABLEOK As Integer = &H465
    Private Const BFFM_SETSELECTIONA As Integer = &H466
    Private Const BFFM_SETSTATUSTEXT As Integer = &H464

    Private Const BIF_RETURNONLYFSDIRS As Short = &H1S
    Private Const BIF_DONTGOBELOWDOMAIN As Short = &H2S
    Private Const BIF_STATUSTEXT As Short = &H4S
    Private Const BIF_RETURNFSANCESTORS As Short = &H8S
    Private Const BIF_EDITBOX As Short = &H10S
    Private Const BIF_VALIDATE As Short = &H20S
    Private Const BIF_USENEWUI As Short = &H40S
    Private Const BIF_BROWSEFORCOMPUTER As Short = &H1000S
    Private Const BIF_BROWSEFORPRINTER As Short = &H2000S
    Private Const BIF_BROWSEINCLUDEFILES As Short = &H4000S

    Private Const MAX_PATH As Short = 260

    Public Enum START_LOCATION
        SL_FLAG_CREATE = &H8000
        SL_FLAG_DONT_VERIFY = &H4000
        SL_ADMINTOOLS = &H30
        SL_ALTSTARTUP = &H1D
        SL_APPDATA = &H1A
        SL_BITBUCKET = &HA
        SL_COMMON_ADMINTOOLS = &H2F
        SL_COMMON_ALTSTARTUP = &H1D
        SL_COMMON_APPDATA = &H23
        SL_COMMON_DESKTOPDIRECTORY = &H19
        SL_COMMON_DOCUMENTS = &H2E
        SL_COMMON_FAVORITES = &H1F
        SL_COMMON_PROGRAMS = &H17
        SL_COMMON_STARTMENU = &H16
        SL_COMMON_STARTUP = &H18
        SL_COMMON_TEMPLATES = &H2D
        SL_CONTROLS = &H3
        SL_COOKIES = &H21
        SL_DESKTOP = &H0
        SL_DESKTOPDIRECTORY = &H10
        SL_DRIVES = &H11
        SL_FAVORITES = &H6
        SL_FONTS = &H14
        SL_HISTORY = &H22
        SL_INTERNET = &H1
        SL_INTERNET_CACHE = &H20
        SL_LOCAL_APPDATA = &H1C
        SL_MYPICTURES = &H27
        SL_NETHOOD = &H13
        SL_NETWORK = &H12
        SL_PERSONAL = &H5
        SL_PRINTERS = &H4
        SL_PRINTHOOD = &H1B
        SL_PROFILE = &H28
        SL_PROGRAM_FILES = &H26
        SL_PROGRAM_FILES_COMMON = &H2B
        SL_PROGRAM_FILES_COMMONX86 = &H2C
        SL_PROGRAM_FILESX86 = &H2A
        SL_PROGRAMS = &H2
        SL_RECENT = &H8
        SL_SENDTO = &H9
        SL_STARTMENU = &HB
        SL_STARTUP = &H7
        SL_SYSTEM = &H25
        SL_SYSTEMX86 = &H29
        SL_TEMPLATES = &H15
        SL_WINDOWS = &H24
    End Enum

    ' callback delegate
    Private Delegate Function BrowseCB(ByVal hWnd As IntPtr, _
                                   ByVal uMsg As Integer, _
                                   ByVal lParam As Integer, _
                                   ByVal lpData As Integer) As Integer

    Private Structure BROWSEINFO
        Dim hOwner As IntPtr
        Dim pidlRoot As Integer
        Dim pszDisplayName As String
        Dim lpszTitle As String
        Dim ulFlags As Integer
        Dim lpfn As BrowseCB
        Dim lParam As IntPtr
        Dim iImage As Integer
    End Structure

    <DllImport("ole32.dll")> _
    Private Shared Sub CoTaskMemFree(ByVal addr As IntPtr)
    End Sub

    <DllImport("user32.dll")> _
              Private Overloads Shared Function SendMessage(ByVal hWnd As IntPtr, ByVal uMsg As Integer, ByVal lParam As Integer, ByVal lpData As Integer) As Integer
    End Function

    <DllImport("user32.dll")> _
              Private Overloads Shared Function SendMessage(ByVal hWnd As IntPtr, ByVal uMsg As Integer, ByVal lParam As Integer, ByVal lpData As String) As Integer
    End Function

    <DllImport("shell32.dll", CharSet:=CharSet.Ansi)> _
    Private Shared Function SHBrowseForFolder(ByRef lpBrowseInfo As BROWSEINFO) As IntPtr
    End Function

    <DllImport("shell32.dll", CharSet:=CharSet.Ansi)> _
    Private Shared Function SHGetPathFromIDList(ByVal pidl As IntPtr, ByVal pszPath As StringBuilder) As Integer
    End Function

    <DllImport("shell32.dll", CharSet:=CharSet.Ansi)> _
    Private Shared Function SHGetSpecialFolderLocation(ByVal hWnd As IntPtr, ByVal nFolder As Integer, ByRef pidl As Integer) As Integer
    End Function

    Private m_BI As BROWSEINFO
    Private m_Init As Boolean
    Private m_NewUI As Boolean = False
    Private m_ShowStatus As Boolean = False

    Public Sub New(ByVal handle As IntPtr)
        m_BI.hOwner = handle
        m_BI.lpfn = AddressOf BrowseCallbackProc
    End Sub

    Public Overloads Function Browse() As String
        m_BI.pidlRoot = 0
        Return DoBrowse("")
    End Function

    Public Overloads Function Browse(ByVal startPath As String) As String
        m_BI.pidlRoot = 0
        Return DoBrowse(startPath)
    End Function

    Public Overloads Function Browse(ByVal SL As START_LOCATION) As String
        SHGetSpecialFolderLocation(m_BI.hOwner, SL, m_BI.pidlRoot)
        Return DoBrowse("")
    End Function

    Private Function DoBrowse(ByVal startPath As String) As String
        Dim result As IntPtr
        Dim sel As String

        m_BI.ulFlags = BIF_RETURNONLYFSDIRS
        If m_NewUI Then m_BI.ulFlags += BIF_USENEWUI
        If m_ShowStatus Then m_BI.ulFlags += BIF_STATUSTEXT

        m_BI.lParam = Marshal.StringToHGlobalAnsi(startPath)
        m_Init = True
        result = SHBrowseForFolder(m_BI)

        sel = GetFSPath(result)

        Call CoTaskMemFree(result)

        Return sel
    End Function

    Public Property Title() As String
        Get
            Return m_BI.lpszTitle
        End Get
        Set(ByVal Value As String)
            m_BI.lpszTitle = Value
        End Set
    End Property

    Public Function BrowseCallbackProc(ByVal hWnd As IntPtr, _
                                   ByVal uMsg As Integer, _
                                   ByVal lParam As Integer, _
                                   ByVal lpData As Integer) As Integer
        If uMsg = BFFM_INITIALIZED Then
            SendMessage(hWnd, BFFM_SETSELECTIONA, 1, lpData)
            m_Init = False
        ElseIf uMsg = BFFM_SELCHANGED And Not m_Init Then
            SendMessage(hWnd, BFFM_SETSTATUSTEXT, 0, GetFSPath(New IntPtr(lParam)))
        End If
    End Function

    Private Function GetFSPath(ByVal pidl As IntPtr) As String
        Dim sb As New StringBuilder(MAX_PATH)

        If pidl.Equals(IntPtr.Zero) Then
            Return ""
        Else
            If SHGetPathFromIDList(pidl, sb) = 1 Then
                Return sb.ToString()
            End If
        End If
    End Function

    Public Property NewUI() As Boolean
        Get
            Return m_NewUI
        End Get
        Set(ByVal Value As Boolean)
            m_NewUI = Value
        End Set
    End Property

    Public Property ShowStatus() As Boolean
        Get
            Return m_ShowStatus
        End Get
        Set(ByVal Value As Boolean)
            m_ShowStatus = Value
        End Set
    End Property

End Class

