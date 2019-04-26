Imports Microsoft.Win32

Public Class ProjectOptions
    Inherits System.Windows.Forms.Form

    Public Enum OpenMethods
        OpenText = 0
        OpenGUI = 1
    End Enum

    Public Enum RunNameTypes
        NameFromRunID
        NameFromStartDate
        NameFromStartDateEndDate
        NameFromStartDate_2
    End Enum

    Public Shared OpenMethod As OpenMethods = OpenMethods.OpenGUI
    Public Shared NameFromDefinition As RunNameTypes = RunNameTypes.NameFromRunID

    Private BaseKey As String = "Software\\Mohid"


#Region " Windows Form Designer generated code "

    Public Sub New()
        MyBase.New()

        'This call is required by the Windows Form Designer.
        InitializeComponent()

    End Sub

    'Form overrides dispose to clean up the component list.
    Protected Overloads Overrides Sub Dispose(ByVal disposing As Boolean)
        If disposing Then
            If Not (components Is Nothing) Then
                components.Dispose()
            End If
        End If
        MyBase.Dispose(disposing)
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    Friend WithEvents ButtonOK As System.Windows.Forms.Button
    Friend WithEvents ButtonCancel As System.Windows.Forms.Button
    Friend WithEvents ToolTip1 As System.Windows.Forms.ToolTip
    Friend WithEvents OpenFileDialog1 As System.Windows.Forms.OpenFileDialog
    Friend WithEvents TabControl1 As System.Windows.Forms.TabControl
    Friend WithEvents TabPage1 As System.Windows.Forms.TabPage
    Friend WithEvents TabPage2 As System.Windows.Forms.TabPage
    Friend WithEvents GroupBox1 As System.Windows.Forms.GroupBox
    Friend WithEvents RadioGUI As System.Windows.Forms.RadioButton
    Friend WithEvents RadioText As System.Windows.Forms.RadioButton
    Friend WithEvents GroupBox2 As System.Windows.Forms.GroupBox
    Friend WithEvents RadioRunStart As System.Windows.Forms.RadioButton
    Friend WithEvents RadioRunID As System.Windows.Forms.RadioButton
    Friend WithEvents RadioStartEndDate As System.Windows.Forms.RadioButton
    Friend WithEvents RadioRunStart_2 As System.Windows.Forms.RadioButton
    Friend WithEvents ReadFileMohidLand As Mohid_Base.ReadFile
    Friend WithEvents ReadFileMohidRiver As Mohid_Base.ReadFile
    Friend WithEvents ReadFileMohidPost As Mohid_Base.ReadFile
    Friend WithEvents ReadFileTimeSerieEditor As Mohid_Base.ReadFile
    Friend WithEvents ReadFileTriangulator As Mohid_Base.ReadFile
    Public WithEvents ReadFileMohidWater As Mohid_Base.ReadFile
    Friend WithEvents ReadFileDigitalTerrainCreator As Mohid_Base.ReadFile
    Friend WithEvents ReadFileBasinDelineator As Mohid_Base.ReadFile
    Friend WithEvents ReadFileTidalChart As Mohid_Base.ReadFile
    Friend WithEvents ReadFileAutoTimeSerie As Mohid_Base.ReadFile
    Friend WithEvents ReadFileTextEditor As Mohid_Base.ReadFile
    Friend WithEvents ReadFileZIP As Mohid_Base.ReadFile
    Friend WithEvents ReadFileToGIF As Mohid_Base.ReadFile
    Friend WithEvents txtTempDir As System.Windows.Forms.TextBox
    Friend WithEvents ReadFileGIS As Mohid_Base.ReadFile
    Friend WithEvents LabelTempDir As System.Windows.Forms.Label
    Friend WithEvents ButtonBrowseForTempFolder As System.Windows.Forms.Button
    Friend WithEvents ReadFileScheduler As Mohid_Base.ReadFile
    Friend WithEvents ReadConvertToHDF5 As Mohid_Base.ReadFile
    Friend WithEvents ReadFileMohidSoil As Mohid_Base.ReadFile
    Public WithEvents ReadFileMohidWaterMPI As Mohid_Base.ReadFile

    <System.Diagnostics.DebuggerStepThrough()> Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container()
        Dim resources As System.Resources.ResourceManager = New System.Resources.ResourceManager(GetType(ProjectOptions))
        Me.ButtonOK = New System.Windows.Forms.Button()
        Me.ButtonCancel = New System.Windows.Forms.Button()
        Me.ToolTip1 = New System.Windows.Forms.ToolTip(Me.components)
        Me.OpenFileDialog1 = New System.Windows.Forms.OpenFileDialog()
        Me.TabControl1 = New System.Windows.Forms.TabControl()
        Me.TabPage1 = New System.Windows.Forms.TabPage()
        Me.ReadFileMohidWaterMPI = New Mohid_Base.ReadFile()
        Me.ReadFileMohidSoil = New Mohid_Base.ReadFile()
        Me.ReadConvertToHDF5 = New Mohid_Base.ReadFile()
        Me.ReadFileScheduler = New Mohid_Base.ReadFile()
        Me.ReadFileGIS = New Mohid_Base.ReadFile()
        Me.ReadFileAutoTimeSerie = New Mohid_Base.ReadFile()
        Me.ReadFileTidalChart = New Mohid_Base.ReadFile()
        Me.ReadFileBasinDelineator = New Mohid_Base.ReadFile()
        Me.ReadFileDigitalTerrainCreator = New Mohid_Base.ReadFile()
        Me.ReadFileTriangulator = New Mohid_Base.ReadFile()
        Me.ReadFileTimeSerieEditor = New Mohid_Base.ReadFile()
        Me.ReadFileMohidPost = New Mohid_Base.ReadFile()
        Me.ReadFileMohidLand = New Mohid_Base.ReadFile()
        Me.ReadFileMohidRiver = New Mohid_Base.ReadFile()
        Me.ReadFileMohidWater = New Mohid_Base.ReadFile()
        Me.TabPage2 = New System.Windows.Forms.TabPage()
        Me.ReadFileZIP = New Mohid_Base.ReadFile()
        Me.ReadFileToGIF = New Mohid_Base.ReadFile()
        Me.ButtonBrowseForTempFolder = New System.Windows.Forms.Button()
        Me.LabelTempDir = New System.Windows.Forms.Label()
        Me.txtTempDir = New System.Windows.Forms.TextBox()
        Me.ReadFileTextEditor = New Mohid_Base.ReadFile()
        Me.GroupBox2 = New System.Windows.Forms.GroupBox()
        Me.RadioRunStart_2 = New System.Windows.Forms.RadioButton()
        Me.RadioStartEndDate = New System.Windows.Forms.RadioButton()
        Me.RadioRunStart = New System.Windows.Forms.RadioButton()
        Me.RadioRunID = New System.Windows.Forms.RadioButton()
        Me.GroupBox1 = New System.Windows.Forms.GroupBox()
        Me.RadioText = New System.Windows.Forms.RadioButton()
        Me.RadioGUI = New System.Windows.Forms.RadioButton()

        Me.TabControl1.SuspendLayout()
        Me.TabPage1.SuspendLayout()
        Me.TabPage2.SuspendLayout()
        Me.GroupBox2.SuspendLayout()
        Me.GroupBox1.SuspendLayout()
        Me.SuspendLayout()
        '
        'ButtonOK
        '
        Me.ButtonOK.DialogResult = System.Windows.Forms.DialogResult.OK
        Me.ButtonOK.Location = New System.Drawing.Point(120, 528)
        Me.ButtonOK.Name = "ButtonOK"
        Me.ButtonOK.TabIndex = 8
        Me.ButtonOK.Text = "OK"
        '
        'ButtonCancel
        '
        Me.ButtonCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
        Me.ButtonCancel.Location = New System.Drawing.Point(200, 528)
        Me.ButtonCancel.Name = "ButtonCancel"
        Me.ButtonCancel.TabIndex = 9
        Me.ButtonCancel.Text = "Cancel"
        '
        'OpenFileDialog1
        '
        Me.OpenFileDialog1.Filter = "Executable Files|*.exe|All Files|*.*"
        Me.OpenFileDialog1.Title = "Choose File..."
        '
        'TabControl1
        '
        Me.TabControl1.Controls.AddRange(New System.Windows.Forms.Control() {Me.TabPage1, Me.TabPage2})
        Me.TabControl1.Location = New System.Drawing.Point(8, 8)
        Me.TabControl1.Name = "TabControl1"
        Me.TabControl1.SelectedIndex = 0
        Me.TabControl1.Size = New System.Drawing.Size(376, 512)
        Me.TabControl1.TabIndex = 10
        '
        'TabPage1
        '
        Me.TabPage1.Controls.AddRange(New System.Windows.Forms.Control() {Me.ReadFileMohidRiver, Me.ReadFileMohidWaterMPI, Me.ReadFileMohidSoil, Me.ReadConvertToHDF5, Me.ReadFileScheduler, Me.ReadFileGIS, Me.ReadFileAutoTimeSerie, Me.ReadFileTidalChart, Me.ReadFileBasinDelineator, Me.ReadFileDigitalTerrainCreator, Me.ReadFileTriangulator, Me.ReadFileTimeSerieEditor, Me.ReadFileMohidPost, Me.ReadFileMohidLand, Me.ReadFileMohidWater})
        Me.TabPage1.Location = New System.Drawing.Point(4, 22)
        Me.TabPage1.Name = "TabPage1"
        Me.TabPage1.Size = New System.Drawing.Size(368, 486)
        Me.TabPage1.TabIndex = 0
        Me.TabPage1.Text = "Mohid Executables"
        '
        'ReadFileMohidWaterMPI
        '
        Me.ReadFileMohidWaterMPI.File = "Mohid_v4_MPI.exe"
        Me.ReadFileMohidWaterMPI.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileMohidWaterMPI.FileID = "Mohid Water MPI"
        Me.ReadFileMohidWaterMPI.Location = New System.Drawing.Point(8, 40)
        Me.ReadFileMohidWaterMPI.Name = "ReadFileMohidWaterMPI"
        Me.ReadFileMohidWaterMPI.NewFile = False
        Me.ReadFileMohidWaterMPI.NewFileDefaultName = ""
        Me.ReadFileMohidWaterMPI.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileMohidWaterMPI.TabIndex = 52
        '
        'ReadFileMohidSoil
        '
        Me.ReadFileMohidSoil.File = "Mohid_Soil.exe"
        Me.ReadFileMohidSoil.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileMohidSoil.FileID = "Mohid Soil"
        Me.ReadFileMohidSoil.Location = New System.Drawing.Point(8, 136)
        Me.ReadFileMohidSoil.Name = "ReadFileMohidSoil"
        Me.ReadFileMohidSoil.NewFile = False
        Me.ReadFileMohidSoil.NewFileDefaultName = ""
        Me.ReadFileMohidSoil.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileMohidSoil.TabIndex = 51
        '
        'ReadConvertToHDF5
        '
        Me.ReadConvertToHDF5.File = "ConvertToHDF5"
        Me.ReadConvertToHDF5.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadConvertToHDF5.FileID = "ConvertToHDF5"
        Me.ReadConvertToHDF5.Location = New System.Drawing.Point(8, 456)
        Me.ReadConvertToHDF5.Name = "ReadConvertToHDF5"
        Me.ReadConvertToHDF5.NewFile = False
        Me.ReadConvertToHDF5.NewFileDefaultName = ""
        Me.ReadConvertToHDF5.Size = New System.Drawing.Size(352, 24)
        Me.ReadConvertToHDF5.TabIndex = 49
        '
        'ReadFileScheduler
        '
        Me.ReadFileScheduler.File = "Mohid_Scheduler.exe"
        Me.ReadFileScheduler.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileScheduler.FileID = "Mohid Scheduler"
        Me.ReadFileScheduler.Location = New System.Drawing.Point(8, 264)
        Me.ReadFileScheduler.Name = "ReadFileScheduler"
        Me.ReadFileScheduler.NewFile = False
        Me.ReadFileScheduler.NewFileDefaultName = ""
        Me.ReadFileScheduler.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileScheduler.TabIndex = 48
        '
        'ReadFileGIS
        '
        Me.ReadFileGIS.File = "Mohid_GIS.exe"
        Me.ReadFileGIS.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileGIS.FileID = "Mohid GIS"
        Me.ReadFileGIS.Location = New System.Drawing.Point(8, 232)
        Me.ReadFileGIS.Name = "ReadFileGIS"
        Me.ReadFileGIS.NewFile = False
        Me.ReadFileGIS.NewFileDefaultName = ""
        Me.ReadFileGIS.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileGIS.TabIndex = 47
        '
        'ReadFileAutoTimeSerie
        '
        Me.ReadFileAutoTimeSerie.File = "Mohid_TimeSeriesCreator.exe"
        Me.ReadFileAutoTimeSerie.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileAutoTimeSerie.FileID = "TimeSeriesCreator"
        Me.ReadFileAutoTimeSerie.Location = New System.Drawing.Point(8, 424)
        Me.ReadFileAutoTimeSerie.Name = "ReadFileAutoTimeSerie"
        Me.ReadFileAutoTimeSerie.NewFile = False
        Me.ReadFileAutoTimeSerie.NewFileDefaultName = ""
        Me.ReadFileAutoTimeSerie.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileAutoTimeSerie.TabIndex = 46
        '
        'ReadFileTidalChart
        '
        Me.ReadFileTidalChart.File = "Mohid_Tidal_Chart.exe"
        Me.ReadFileTidalChart.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileTidalChart.FileID = "Tidal Chart Tool"
        Me.ReadFileTidalChart.Location = New System.Drawing.Point(8, 392)
        Me.ReadFileTidalChart.Name = "ReadFileTidalChart"
        Me.ReadFileTidalChart.NewFile = False
        Me.ReadFileTidalChart.NewFileDefaultName = ""
        Me.ReadFileTidalChart.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileTidalChart.TabIndex = 45
        '
        'ReadFileBasinDelineator
        '
        Me.ReadFileBasinDelineator.File = "BasinDelineator.exe"
        Me.ReadFileBasinDelineator.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileBasinDelineator.FileID = "Basin Delineator"
        Me.ReadFileBasinDelineator.Location = New System.Drawing.Point(8, 360)
        Me.ReadFileBasinDelineator.Name = "ReadFileBasinDelineator"
        Me.ReadFileBasinDelineator.NewFile = False
        Me.ReadFileBasinDelineator.NewFileDefaultName = ""
        Me.ReadFileBasinDelineator.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileBasinDelineator.TabIndex = 42
        '
        'ReadFileDigitalTerrainCreator
        '
        Me.ReadFileDigitalTerrainCreator.File = "CreateDigitalTerrain.exe"
        Me.ReadFileDigitalTerrainCreator.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileDigitalTerrainCreator.FileID = "Digital Terrain C."
        Me.ReadFileDigitalTerrainCreator.Location = New System.Drawing.Point(8, 328)
        Me.ReadFileDigitalTerrainCreator.Name = "ReadFileDigitalTerrainCreator"
        Me.ReadFileDigitalTerrainCreator.NewFile = False
        Me.ReadFileDigitalTerrainCreator.NewFileDefaultName = ""
        Me.ReadFileDigitalTerrainCreator.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileDigitalTerrainCreator.TabIndex = 41
        '
        'ReadFileTriangulator
        '
        Me.ReadFileTriangulator.File = "Triangulator.exe"
        Me.ReadFileTriangulator.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileTriangulator.FileID = "Triangulator"
        Me.ReadFileTriangulator.Location = New System.Drawing.Point(8, 296)
        Me.ReadFileTriangulator.Name = "ReadFileTriangulator"
        Me.ReadFileTriangulator.NewFile = False
        Me.ReadFileTriangulator.NewFileDefaultName = ""
        Me.ReadFileTriangulator.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileTriangulator.TabIndex = 40
        '
        'ReadFileTimeSerieEditor
        '
        Me.ReadFileTimeSerieEditor.File = "Mohid_Time_Serie_Editor.exe"
        Me.ReadFileTimeSerieEditor.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileTimeSerieEditor.FileID = "Time Series Editor"
        Me.ReadFileTimeSerieEditor.Location = New System.Drawing.Point(8, 200)
        Me.ReadFileTimeSerieEditor.Name = "ReadFileTimeSerieEditor"
        Me.ReadFileTimeSerieEditor.NewFile = False
        Me.ReadFileTimeSerieEditor.NewFileDefaultName = ""
        Me.ReadFileTimeSerieEditor.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileTimeSerieEditor.TabIndex = 39
        '
        'ReadFileMohidPost
        '
        Me.ReadFileMohidPost.File = "Mohid_Post.exe"
        Me.ReadFileMohidPost.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileMohidPost.FileID = "Post-Processor"
        Me.ReadFileMohidPost.Location = New System.Drawing.Point(8, 168)
        Me.ReadFileMohidPost.Name = "ReadFileMohidPost"
        Me.ReadFileMohidPost.NewFile = False
        Me.ReadFileMohidPost.NewFileDefaultName = ""
        Me.ReadFileMohidPost.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileMohidPost.TabIndex = 38
        '
        'ReadFileMohidLand
        '
        Me.ReadFileMohidLand.File = "Mohid_Land.exe"
        Me.ReadFileMohidLand.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileMohidLand.FileID = "Mohid Land"
        Me.ReadFileMohidLand.Location = New System.Drawing.Point(8, 72)
        Me.ReadFileMohidLand.Name = "ReadFileMohidLand"
        Me.ReadFileMohidLand.NewFile = False
        Me.ReadFileMohidLand.NewFileDefaultName = ""
        Me.ReadFileMohidLand.Size = New System.Drawing.Size(352, 25)
        Me.ReadFileMohidLand.TabIndex = 37
        '
        'ReadFileMohidWater
        '
        Me.ReadFileMohidWater.File = "Mohid_v4.exe"
        Me.ReadFileMohidWater.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileMohidWater.FileID = "Mohid Water"
        Me.ReadFileMohidWater.Location = New System.Drawing.Point(8, 8)
        Me.ReadFileMohidWater.Name = "ReadFileMohidWater"
        Me.ReadFileMohidWater.NewFile = False
        Me.ReadFileMohidWater.NewFileDefaultName = ""
        Me.ReadFileMohidWater.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileMohidWater.TabIndex = 36
        '
        'TabPage2
        '
        Me.TabPage2.Controls.AddRange(New System.Windows.Forms.Control() {Me.ReadFileZIP, Me.ReadFileToGIF, Me.ButtonBrowseForTempFolder, Me.LabelTempDir, Me.txtTempDir, Me.ReadFileTextEditor, Me.GroupBox2, Me.GroupBox1})
        Me.TabPage2.Location = New System.Drawing.Point(4, 22)
        Me.TabPage2.Name = "TabPage2"
        Me.TabPage2.Size = New System.Drawing.Size(368, 486)
        Me.TabPage2.TabIndex = 1
        Me.TabPage2.Text = "Data Files / Tools"
        '
        'ReadFileZIP
        '
        Me.ReadFileZIP.File = "zip.exe"
        Me.ReadFileZIP.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileZIP.FileID = "Zipper"
        Me.ReadFileZIP.Location = New System.Drawing.Point(8, 256)
        Me.ReadFileZIP.Name = "ReadFileZIP"
        Me.ReadFileZIP.NewFile = False
        Me.ReadFileZIP.NewFileDefaultName = ""
        Me.ReadFileZIP.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileZIP.TabIndex = 49
        '
        'ReadFileToGIF
        '
        Me.ReadFileToGIF.File = "2Gif.exe"
        Me.ReadFileToGIF.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileToGIF.FileID = "GIF Animator"
        Me.ReadFileToGIF.Location = New System.Drawing.Point(8, 224)
        Me.ReadFileToGIF.Name = "ReadFileToGIF"
        Me.ReadFileToGIF.NewFile = False
        Me.ReadFileToGIF.NewFileDefaultName = ""
        Me.ReadFileToGIF.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileToGIF.TabIndex = 48
        '
        'ButtonBrowseForTempFolder
        '
        Me.ButtonBrowseForTempFolder.Location = New System.Drawing.Point(280, 288)
        Me.ButtonBrowseForTempFolder.Name = "ButtonBrowseForTempFolder"
        Me.ButtonBrowseForTempFolder.TabIndex = 47
        Me.ButtonBrowseForTempFolder.Text = "Browse..."
        '
        'LabelTempDir
        '
        Me.LabelTempDir.Location = New System.Drawing.Point(8, 288)
        Me.LabelTempDir.Name = "LabelTempDir"
        Me.LabelTempDir.Size = New System.Drawing.Size(88, 24)
        Me.LabelTempDir.TabIndex = 46
        Me.LabelTempDir.Text = "Temp. Dir."
        Me.LabelTempDir.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'txtTempDir
        '
        Me.txtTempDir.Location = New System.Drawing.Point(104, 288)
        Me.txtTempDir.Name = "txtTempDir"
        Me.txtTempDir.Size = New System.Drawing.Size(168, 20)
        Me.txtTempDir.TabIndex = 45
        Me.txtTempDir.Text = "c:\temp"
        '
        'ReadFileTextEditor
        '
        Me.ReadFileTextEditor.File = "notepad.exe"
        Me.ReadFileTextEditor.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileTextEditor.FileID = "Text Editor"
        Me.ReadFileTextEditor.Location = New System.Drawing.Point(8, 192)
        Me.ReadFileTextEditor.Name = "ReadFileTextEditor"
        Me.ReadFileTextEditor.NewFile = False
        Me.ReadFileTextEditor.NewFileDefaultName = ""
        Me.ReadFileTextEditor.Size = New System.Drawing.Size(352, 24)
        Me.ReadFileTextEditor.TabIndex = 8
        '
        'GroupBox2
        '
        Me.GroupBox2.Controls.AddRange(New System.Windows.Forms.Control() {Me.RadioRunStart_2, Me.RadioStartEndDate, Me.RadioRunStart, Me.RadioRunID})
        Me.GroupBox2.Location = New System.Drawing.Point(8, 64)
        Me.GroupBox2.Name = "GroupBox2"
        Me.GroupBox2.Size = New System.Drawing.Size(352, 96)
        Me.GroupBox2.TabIndex = 7
        Me.GroupBox2.TabStop = False
        Me.GroupBox2.Text = "Default Run Name"
        '
        'RadioRunStart_2
        '
        Me.RadioRunStart_2.Location = New System.Drawing.Point(216, 56)
        Me.RadioRunStart_2.Name = "RadioRunStart_2"
        Me.RadioRunStart_2.Size = New System.Drawing.Size(104, 32)
        Me.RadioRunStart_2.TabIndex = 3
        Me.RadioRunStart_2.Text = "Start Date       (yyyyMMdd)"
        '
        'RadioStartEndDate
        '
        Me.RadioStartEndDate.Location = New System.Drawing.Point(8, 56)
        Me.RadioStartEndDate.Name = "RadioStartEndDate"
        Me.RadioStartEndDate.Size = New System.Drawing.Size(136, 24)
        Me.RadioStartEndDate.TabIndex = 2
        Me.RadioStartEndDate.Text = "Start Date - End Date"
        '
        'RadioRunStart
        '
        Me.RadioRunStart.Location = New System.Drawing.Point(216, 16)
        Me.RadioRunStart.Name = "RadioRunStart"
        Me.RadioRunStart.Size = New System.Drawing.Size(120, 32)
        Me.RadioRunStart.TabIndex = 1
        Me.RadioRunStart.Text = "Start Date               (dd - MMM - YYYY)"
        '
        'RadioRunID
        '
        Me.RadioRunID.Checked = True
        Me.RadioRunID.Location = New System.Drawing.Point(8, 16)
        Me.RadioRunID.Name = "RadioRunID"
        Me.RadioRunID.Size = New System.Drawing.Size(80, 24)
        Me.RadioRunID.TabIndex = 0
        Me.RadioRunID.TabStop = True
        Me.RadioRunID.Text = "Run_ + ID"
        '
        'GroupBox1
        '
        Me.GroupBox1.Controls.AddRange(New System.Windows.Forms.Control() {Me.RadioText, Me.RadioGUI})
        Me.GroupBox1.Location = New System.Drawing.Point(8, 8)
        Me.GroupBox1.Name = "GroupBox1"
        Me.GroupBox1.Size = New System.Drawing.Size(352, 48)
        Me.GroupBox1.TabIndex = 6
        Me.GroupBox1.TabStop = False
        Me.GroupBox1.Text = "Prefered open method"
        '
        'RadioText
        '
        Me.RadioText.Location = New System.Drawing.Point(216, 16)
        Me.RadioText.Name = "RadioText"
        Me.RadioText.Size = New System.Drawing.Size(80, 24)
        Me.RadioText.TabIndex = 1
        Me.RadioText.Text = "Text Editor"
        '
        'RadioGUI
        '
        Me.RadioGUI.Checked = True
        Me.RadioGUI.Location = New System.Drawing.Point(16, 16)
        Me.RadioGUI.Name = "RadioGUI"
        Me.RadioGUI.Size = New System.Drawing.Size(120, 24)
        Me.RadioGUI.TabIndex = 0
        Me.RadioGUI.TabStop = True
        Me.RadioGUI.Text = "GUI when possible"
        '
        'ReadFileMohidRiver
        '
        Me.ReadFileMohidRiver.File = "Mohid_River.exe"
        Me.ReadFileMohidRiver.FileFilter = "Executable file (*.exe)|*.exe|All files (*.*)|*.*"
        Me.ReadFileMohidRiver.FileID = "Mohid River"
        Me.ReadFileMohidRiver.Location = New System.Drawing.Point(8, 104)
        Me.ReadFileMohidRiver.Name = "ReadFileMohidRiver"
        Me.ReadFileMohidRiver.NewFile = False
        Me.ReadFileMohidRiver.NewFileDefaultName = ""
        Me.ReadFileMohidRiver.Size = New System.Drawing.Size(352, 25)
        Me.ReadFileMohidRiver.TabIndex = 53
        '
        'ProjectOptions
        '
        Me.AcceptButton = Me.ButtonOK
        Me.AutoScaleBaseSize = New System.Drawing.Size(5, 13)
        Me.CancelButton = Me.ButtonCancel
        Me.ClientSize = New System.Drawing.Size(394, 560)
        Me.Controls.AddRange(New System.Windows.Forms.Control() {Me.TabControl1, Me.ButtonCancel, Me.ButtonOK})
        Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
        Me.Icon = CType(resources.GetObject("$this.Icon"), System.Drawing.Icon)
        Me.MaximizeBox = False
        Me.Name = "ProjectOptions"
        Me.ShowInTaskbar = False
        Me.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
        Me.Text = "Options"
        Me.TopMost = True
        Me.TabControl1.ResumeLayout(False)
        Me.TabPage1.ResumeLayout(False)
        Me.TabPage2.ResumeLayout(False)
        Me.GroupBox2.ResumeLayout(False)
        Me.GroupBox1.ResumeLayout(False)
        Me.ResumeLayout(False)

    End Sub

#End Region

    Public Sub New(ByVal Path As String)

        MyBase.New()

        'This call is required by the Windows Form Designer.
        InitializeComponent()

        Dim regKey As RegistryKey
        Dim keyValue As String

        'Opens Registry Key
        keyValue = BaseKey
        regKey = Registry.LocalMachine.OpenSubKey(keyValue, False)

        If (Not regKey Is Nothing) Then

            'Mohid_GUI is not readed
            Me.ReadFileScheduler.File = regKey.GetValue("Mohid_Scheduler", "Mohid_Scheduler.exe")
            Me.ReadFileGIS.File = regKey.GetValue("Mohid_GIS", "Mohid_GIS.exe")
            Me.ReadFileBasinDelineator.File = regKey.GetValue("MohidBasinDelineator", "MohidBasinDelineator.exe")
            Me.ReadFileDigitalTerrainCreator.File = regKey.GetValue("MohidDigitalTerrainCreator", "MohidDigitalTerrain.exe")
            Me.ReadFileMohidLand.File = regKey.GetValue("MohidLand", "MohidLand.exe")
            Me.ReadFileMohidRiver.File = regKey.GetValue("MohidRiver", "MohidRiver.exe")
            Me.ReadFileMohidPost.File = regKey.GetValue("MohidPost", "MohidPost.exe")
            Me.ReadFileTidalChart.File = regKey.GetValue("MohidTidalChart", "MohidTidalChart.exe")
            Me.ReadFileTimeSerieEditor.File = regKey.GetValue("MohidTimeSerieEditor", "MohidTimeSerieEditor.exe")
            Me.ReadFileAutoTimeSerie.File = regKey.GetValue("MohidTimSeriePre", "MohidTimSeriePre.exe")
            Me.ReadFileTriangulator.File = regKey.GetValue("MohidTriangulator", "MohidTriangulator.exe")
            Me.ReadFileMohidWater.File = regKey.GetValue("MohidWater", "MohidWater.exe")
            Me.ReadFileMohidWaterMPI.File = regKey.GetValue("MohidWaterMPI", "MohidWaterMPI.exe")
            Me.ReadFileToGIF.File = regKey.GetValue("ToGif", "2Gif.exe")
            Me.ReadFileZIP.File = regKey.GetValue("ToZip", "Zip.exe")
            txtTempDir.Text = regKey.GetValue("TempDir", Path + "\temp")
            Me.ReadFileTextEditor.File = regKey.GetValue("TextEditor", "Notepad.exe")
            Me.ReadConvertToHDF5.File = regKey.GetValue("ConvertToHDF5", "MohidConvertToHDF5.exe")
            Me.ReadFileMohidSoil.File = regKey.GetValue("MohidSoil", "MohidSoil.exe")

            OpenMethod = Val(regKey.GetValue("OpenMethod", "0"))
            NameFromDefinition = Val(regKey.GetValue("RunNameDef", "0"))
            regKey.Close()
        End If

    End Sub


    Public ReadOnly Property MohidWater() As String
        Get
            Return ReadFileMohidWater.File
        End Get
    End Property

    Public ReadOnly Property MohidWaterMPI() As String
        Get
            Return ReadFileMohidWaterMPI.File
        End Get
    End Property


    Public ReadOnly Property MohidLand() As String
        Get
            Return ReadFileMohidLand.File
        End Get
    End Property

    Public ReadOnly Property MohidRiver() As String
        Get
            Return ReadFileMohidRiver.File
        End Get
    End Property

    Public ReadOnly Property MohidSoil() As String
        Get
            Return ReadFileMohidSoil.File
        End Get
    End Property

    Public ReadOnly Property MohidPost() As String
        Get
            Return ReadFileMohidPost.File
        End Get
    End Property

    Public ReadOnly Property MohidTimeSeriesEditor() As String
        Get
            Return ReadFileTimeSerieEditor.File
        End Get
    End Property

    Public ReadOnly Property MohidTimeSeriesCreator() As String
        Get
            Return Me.ReadFileAutoTimeSerie.File
        End Get
    End Property

    Public ReadOnly Property MohidTriangulator() As String
        Get
            Return ReadFileTriangulator.File
        End Get
    End Property

    Public ReadOnly Property MohidBasinDelineator() As String
        Get
            Return ReadFileBasinDelineator.File
        End Get
    End Property

    Public ReadOnly Property MohidDigitalTerrainCreator() As String
        Get
            Return ReadFileDigitalTerrainCreator.File
        End Get
    End Property

    Public ReadOnly Property MohidTidalChartTool() As String
        Get
            Return ReadFileTidalChart.File
        End Get
    End Property

    Public ReadOnly Property GifCreatorExe() As String
        Get
            Return ReadFileToGIF.File
        End Get
    End Property

    Public ReadOnly Property ZipCreatorExe() As String
        Get
            Return ReadFileZIP.File
        End Get
    End Property

    Public ReadOnly Property TextEditor() As String
        Get
            Return ReadFileTextEditor.File
        End Get
    End Property

    Public ReadOnly Property TempDir() As String
        Get
            Return Me.txtTempDir.Text
        End Get
    End Property

    Public ReadOnly Property MohidGIS() As String
        Get
            Return Me.ReadFileGIS.File
        End Get
    End Property

    Public ReadOnly Property MohidScheduler() As String
        Get
            Return Me.ReadFileScheduler.File
        End Get
    End Property

    Public ReadOnly Property MohidConvertToHDF5() As String
        Get
            Return Me.ReadConvertToHDF5.File
        End Get
    End Property

    Private Sub ProjectOptions_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load

        If OpenMethod = OpenMethods.OpenGUI Then
            Me.RadioGUI.Checked = True
        Else
            Me.RadioText.Checked = True
        End If

        Select Case NameFromDefinition
            Case RunNameTypes.NameFromRunID
                Me.RadioRunID.Checked = True
            Case RunNameTypes.NameFromStartDate
                Me.RadioRunStart.Checked = True
            Case RunNameTypes.NameFromStartDateEndDate
                Me.RadioStartEndDate.Checked = True
            Case RunNameTypes.NameFromStartDate_2
                Me.RadioRunStart_2.Checked = True
            Case Else
                Me.RadioRunID.Checked = True
        End Select

    End Sub

    Private Sub ButtonOK_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles ButtonOK.Click

        If Me.RadioGUI.Checked Then
            OpenMethod = OpenMethods.OpenGUI
        Else
            OpenMethod = OpenMethods.OpenText
        End If

        If Me.RadioRunID.Checked Then
            NameFromDefinition = RunNameTypes.NameFromRunID
        ElseIf Me.RadioRunStart.Checked Then
            NameFromDefinition = RunNameTypes.NameFromStartDate
        ElseIf Me.RadioRunStart_2.Checked Then
            NameFromDefinition = RunNameTypes.NameFromStartDate_2
        Else
            NameFromDefinition = RunNameTypes.NameFromStartDateEndDate
        End If

        Dim regKey As RegistryKey
        Dim keyValue As String

        'Opens Registry Key
        keyValue = BaseKey
        regKey = Registry.LocalMachine.OpenSubKey(keyValue, True)

        If (Not regKey Is Nothing) Then

            'Mohid_GUI is not readed
            regKey.SetValue("Mohid_Scheduler", Me.ReadFileScheduler.File)
            regKey.SetValue("Mohid_GIS", Me.ReadFileGIS.File)
            regKey.SetValue("MohidBasinDelineator", Me.ReadFileBasinDelineator.File)
            regKey.SetValue("MohidDigitalTerrainCreator", Me.ReadFileDigitalTerrainCreator.File)
            regKey.SetValue("MohidLand", Me.ReadFileMohidLand.File)
            regKey.SetValue("MohidRiver", Me.ReadFileMohidRiver.File)
            regKey.SetValue("MohidPost", Me.ReadFileMohidPost.File)
            regKey.SetValue("MohidTidalChart", Me.ReadFileTidalChart.File)
            regKey.SetValue("MohidTimeSerieEditor", Me.ReadFileTimeSerieEditor.File)
            regKey.SetValue("MohidTimSeriePre", Me.ReadFileAutoTimeSerie.File)
            regKey.SetValue("MohidTriangulator", Me.ReadFileTriangulator.File)
            regKey.SetValue("MohidWater", Me.ReadFileMohidWater.File)
            regKey.SetValue("MohidWaterMPI", Me.ReadFileMohidWaterMPI.File)
            regKey.SetValue("ToGif", Me.ReadFileToGIF.File)
            regKey.SetValue("ToZip", Me.ReadFileZIP.File)
            regKey.SetValue("TempDir", txtTempDir.Text)
            regKey.SetValue("TextEditor", Me.ReadFileTextEditor.File)
            regKey.SetValue("ConvertToHDF5", Me.ReadConvertToHDF5.File)
            regKey.SetValue("MohidSoil", Me.ReadFileMohidSoil.File)
            regKey.SetValue("OpenMethod", Str(OpenMethod))
            regKey.SetValue("RunNameDef", Str(NameFromDefinition))
            regKey.Close()

        Else
            regKey = Registry.LocalMachine.CreateSubKey(keyValue)
            Dim MsgBoxResult As MsgBoxResult
            MsgBox("No registry key was found. Do you wish to register current options?", MsgBoxStyle.YesNoCancel, "Register Settings")
            If MsgBoxResult = MsgBoxResult.Yes Then

                regKey.SetValue("Mohid_Scheduler", Me.ReadFileScheduler.File)
                regKey.SetValue("Mohid_GIS", Me.ReadFileGIS.File)
                regKey.SetValue("MohidBasinDelineator", Me.ReadFileBasinDelineator.File)
                regKey.SetValue("MohidDigitalTerrainCreator", Me.ReadFileDigitalTerrainCreator.File)
                regKey.SetValue("MohidLand", Me.ReadFileMohidLand.File)
                regKey.SetValue("MohidRiver", Me.ReadFileMohidRiver.File)
                regKey.SetValue("MohidPost", Me.ReadFileMohidPost.File)
                regKey.SetValue("MohidTidalChart", Me.ReadFileTidalChart.File)
                regKey.SetValue("MohidTimeSerieEditor", Me.ReadFileTimeSerieEditor.File)
                regKey.SetValue("MohidTimSeriePre", Me.ReadFileAutoTimeSerie.File)
                regKey.SetValue("MohidTriangulator", Me.ReadFileTriangulator.File)
                regKey.SetValue("MohidWater", Me.ReadFileMohidWater.File)
                regKey.SetValue("MohidWaterMPI", Me.ReadFileMohidWaterMPI.File)
                regKey.SetValue("ToGif", Me.ReadFileToGIF.File)
                regKey.SetValue("ToZip", Me.ReadFileZIP.File)
                regKey.SetValue("TempDir", txtTempDir.Text)
                regKey.SetValue("TextEditor", Me.ReadFileTextEditor.File)
                regKey.SetValue("ConvertToHDF5", Me.ReadConvertToHDF5.File)
                regKey.SetValue("MohidSoil", Me.ReadFileMohidSoil.File)
                regKey.SetValue("OpenMethod", Str(OpenMethod))
                regKey.SetValue("RunNameDef", Str(NameFromDefinition))
                regKey.Close()
            End If

        End If

    End Sub

    Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs)

        Dim oBrowse As FolderBrowser = New FolderBrowser(Me.Handle)
        Dim AuxDir As String

        oBrowse.Title = "Choose the Temporary directory"
        oBrowse.NewUI = True
        oBrowse.ShowStatus = True
        AuxDir = oBrowse.Browse(oBrowse.START_LOCATION.SL_DRIVES)

        If (AuxDir <> "") Then
            Me.txtTempDir.Text = AuxDir
        End If

    End Sub


    Private Sub ButtonBrowseForTempFolder_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles ButtonBrowseForTempFolder.Click

        Dim oBrowse As FolderBrowser = New FolderBrowser(Me.Handle)
        Dim AuxDir As String

        oBrowse.Title = "Choose the Temporary directory"
        oBrowse.NewUI = True
        oBrowse.ShowStatus = True
        AuxDir = oBrowse.Browse(oBrowse.START_LOCATION.SL_DRIVES)

        If (AuxDir <> "") Then
            Me.txtTempDir.Text = AuxDir
        End If


    End Sub


End Class
