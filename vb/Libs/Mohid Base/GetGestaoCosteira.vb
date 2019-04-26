Imports Mohid_Base
Imports System.Data
Imports System.Windows.Forms
Imports Npgsql

Public Class frmAccessDataBase
    Inherits System.Windows.Forms.Form

#Region " Windows Form Designer generated code "

    Public Sub New()
        MyBase.New()

        'This call is required by the Windows Form Designer.
        InitializeComponent()

        'Add any initialization after the InitializeComponent() call

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
    Friend WithEvents OpenFileDialog1 As System.Windows.Forms.OpenFileDialog
    Friend WithEvents chkRestrictPromotor As System.Windows.Forms.CheckBox
    Friend WithEvents DataGridPromotores As System.Windows.Forms.DataGrid
    Friend WithEvents DateTimePicker1 As System.Windows.Forms.DateTimePicker
    Friend WithEvents DateTimePicker2 As System.Windows.Forms.DateTimePicker
    Friend WithEvents chkRestTime As System.Windows.Forms.CheckBox
    Friend WithEvents TabControl1 As System.Windows.Forms.TabControl
    Friend WithEvents TabPageRest As System.Windows.Forms.TabPage
    Friend WithEvents TabPageXYZ As System.Windows.Forms.TabPage
    Friend WithEvents MainMenu1 As System.Windows.Forms.MainMenu
    Friend WithEvents TabPageProps As System.Windows.Forms.TabPage
    Friend WithEvents ListViewProps As System.Windows.Forms.ListView
    Friend WithEvents ColumnHeaderID As System.Windows.Forms.ColumnHeader
    Friend WithEvents ColumnHeaderName As System.Windows.Forms.ColumnHeader
    Friend WithEvents btnExportXYZ As System.Windows.Forms.Button
    Friend WithEvents StatusBar1 As System.Windows.Forms.StatusBar
    Friend WithEvents STBarPanel As System.Windows.Forms.StatusBarPanel
    Friend WithEvents chkRestrictTipo As System.Windows.Forms.CheckBox
    Friend WithEvents DataGridTipos As System.Windows.Forms.DataGrid
    Friend WithEvents chkPromotorOnly As System.Windows.Forms.CheckBox
    Friend WithEvents GroupBox1 As System.Windows.Forms.GroupBox
    Friend WithEvents ProgressBar1 As System.Windows.Forms.ProgressBar
    Friend WithEvents btnExportTimeSeries As System.Windows.Forms.Button
    Friend WithEvents TabPagePoints As System.Windows.Forms.TabPage
    Friend WithEvents ListViewPoints As System.Windows.Forms.ListView
    Friend WithEvents ColumnHeader1 As System.Windows.Forms.ColumnHeader
    Friend WithEvents ColumnHeader2 As System.Windows.Forms.ColumnHeader
    Friend WithEvents chkPromotorOnlyPoints As System.Windows.Forms.CheckBox
    Friend WithEvents btnCheckAllPoints As System.Windows.Forms.Button
    Friend WithEvents btnUnCheckAllPoints As System.Windows.Forms.Button
    Friend WithEvents btnUnCheckAllParameters As System.Windows.Forms.Button
    Friend WithEvents btnCheckAllParameters As System.Windows.Forms.Button
    Friend WithEvents btnNext As System.Windows.Forms.Button
    Friend WithEvents BtnPrev As System.Windows.Forms.Button
    Friend WithEvents Label2 As System.Windows.Forms.Label
    Friend WithEvents Label3 As System.Windows.Forms.Label
    Friend WithEvents LabelPromotor As System.Windows.Forms.Label
    Friend WithEvents LabelPoints As System.Windows.Forms.Label
    Friend WithEvents LabelProps As System.Windows.Forms.Label
    Friend WithEvents LabelTime As System.Windows.Forms.Label
    Friend WithEvents btnExportStationTimeSeries As System.Windows.Forms.Button
    Friend WithEvents MenuItem1 As System.Windows.Forms.MenuItem
    Friend WithEvents mnuOpen As System.Windows.Forms.MenuItem
    Friend WithEvents mnuClose As System.Windows.Forms.MenuItem
    Friend WithEvents MenuItem4 As System.Windows.Forms.MenuItem
    Friend WithEvents mnuExit As System.Windows.Forms.MenuItem
    <System.Diagnostics.DebuggerStepThrough()> Private Sub InitializeComponent()
        Dim resources As System.Resources.ResourceManager = New System.Resources.ResourceManager(GetType(frmAccessDataBase))
        Me.OpenFileDialog1 = New System.Windows.Forms.OpenFileDialog
        Me.chkRestrictPromotor = New System.Windows.Forms.CheckBox
        Me.DataGridPromotores = New System.Windows.Forms.DataGrid
        Me.DateTimePicker1 = New System.Windows.Forms.DateTimePicker
        Me.chkRestTime = New System.Windows.Forms.CheckBox
        Me.DateTimePicker2 = New System.Windows.Forms.DateTimePicker
        Me.TabControl1 = New System.Windows.Forms.TabControl
        Me.TabPageRest = New System.Windows.Forms.TabPage
        Me.Label3 = New System.Windows.Forms.Label
        Me.Label2 = New System.Windows.Forms.Label
        Me.DataGridTipos = New System.Windows.Forms.DataGrid
        Me.chkRestrictTipo = New System.Windows.Forms.CheckBox
        Me.TabPageProps = New System.Windows.Forms.TabPage
        Me.btnUnCheckAllParameters = New System.Windows.Forms.Button
        Me.btnCheckAllParameters = New System.Windows.Forms.Button
        Me.chkPromotorOnly = New System.Windows.Forms.CheckBox
        Me.ListViewProps = New System.Windows.Forms.ListView
        Me.ColumnHeaderID = New System.Windows.Forms.ColumnHeader
        Me.ColumnHeaderName = New System.Windows.Forms.ColumnHeader
        Me.TabPagePoints = New System.Windows.Forms.TabPage
        Me.btnUnCheckAllPoints = New System.Windows.Forms.Button
        Me.btnCheckAllPoints = New System.Windows.Forms.Button
        Me.chkPromotorOnlyPoints = New System.Windows.Forms.CheckBox
        Me.ListViewPoints = New System.Windows.Forms.ListView
        Me.ColumnHeader1 = New System.Windows.Forms.ColumnHeader
        Me.ColumnHeader2 = New System.Windows.Forms.ColumnHeader
        Me.TabPageXYZ = New System.Windows.Forms.TabPage
        Me.LabelTime = New System.Windows.Forms.Label
        Me.LabelProps = New System.Windows.Forms.Label
        Me.LabelPoints = New System.Windows.Forms.Label
        Me.LabelPromotor = New System.Windows.Forms.Label
        Me.GroupBox1 = New System.Windows.Forms.GroupBox
        Me.btnExportStationTimeSeries = New System.Windows.Forms.Button
        Me.ProgressBar1 = New System.Windows.Forms.ProgressBar
        Me.btnExportXYZ = New System.Windows.Forms.Button
        Me.btnExportTimeSeries = New System.Windows.Forms.Button
        Me.MainMenu1 = New System.Windows.Forms.MainMenu
        Me.MenuItem1 = New System.Windows.Forms.MenuItem
        Me.mnuOpen = New System.Windows.Forms.MenuItem
        Me.mnuClose = New System.Windows.Forms.MenuItem
        Me.MenuItem4 = New System.Windows.Forms.MenuItem
        Me.mnuExit = New System.Windows.Forms.MenuItem
        Me.StatusBar1 = New System.Windows.Forms.StatusBar
        Me.STBarPanel = New System.Windows.Forms.StatusBarPanel
        Me.btnNext = New System.Windows.Forms.Button
        Me.BtnPrev = New System.Windows.Forms.Button
        CType(Me.DataGridPromotores, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.TabControl1.SuspendLayout()
        Me.TabPageRest.SuspendLayout()
        CType(Me.DataGridTipos, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.TabPageProps.SuspendLayout()
        Me.TabPagePoints.SuspendLayout()
        Me.TabPageXYZ.SuspendLayout()
        Me.GroupBox1.SuspendLayout()
        CType(Me.STBarPanel, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.SuspendLayout()
        '
        'OpenFileDialog1
        '
        Me.OpenFileDialog1.Filter = "Access Database|*mdb|All Files|*.*"
        Me.OpenFileDialog1.RestoreDirectory = True
        '
        'chkRestrictPromotor
        '
        Me.chkRestrictPromotor.Location = New System.Drawing.Point(8, 8)
        Me.chkRestrictPromotor.Name = "chkRestrictPromotor"
        Me.chkRestrictPromotor.Size = New System.Drawing.Size(88, 24)
        Me.chkRestrictPromotor.TabIndex = 6
        Me.chkRestrictPromotor.Text = "Promotor"
        '
        'DataGridPromotores
        '
        Me.DataGridPromotores.DataMember = ""
        Me.DataGridPromotores.HeaderForeColor = System.Drawing.SystemColors.ControlText
        Me.DataGridPromotores.Location = New System.Drawing.Point(96, 8)
        Me.DataGridPromotores.Name = "DataGridPromotores"
        Me.DataGridPromotores.Size = New System.Drawing.Size(464, 168)
        Me.DataGridPromotores.TabIndex = 10
        '
        'DateTimePicker1
        '
        Me.DateTimePicker1.CustomFormat = "dd-MMM-yyyy"
        Me.DateTimePicker1.Enabled = False
        Me.DateTimePicker1.Format = System.Windows.Forms.DateTimePickerFormat.Custom
        Me.DateTimePicker1.Location = New System.Drawing.Point(184, 336)
        Me.DateTimePicker1.Name = "DateTimePicker1"
        Me.DateTimePicker1.ShowUpDown = True
        Me.DateTimePicker1.Size = New System.Drawing.Size(104, 20)
        Me.DateTimePicker1.TabIndex = 12
        Me.DateTimePicker1.Value = New Date(2000, 1, 1, 0, 0, 0, 0)
        '
        'chkRestTime
        '
        Me.chkRestTime.Location = New System.Drawing.Point(8, 328)
        Me.chkRestTime.Name = "chkRestTime"
        Me.chkRestTime.Size = New System.Drawing.Size(72, 24)
        Me.chkRestTime.TabIndex = 13
        Me.chkRestTime.Text = "Time"
        '
        'DateTimePicker2
        '
        Me.DateTimePicker2.CustomFormat = "dd-MMM-yyyy"
        Me.DateTimePicker2.Enabled = False
        Me.DateTimePicker2.Format = System.Windows.Forms.DateTimePickerFormat.Custom
        Me.DateTimePicker2.Location = New System.Drawing.Point(400, 336)
        Me.DateTimePicker2.Name = "DateTimePicker2"
        Me.DateTimePicker2.ShowUpDown = True
        Me.DateTimePicker2.Size = New System.Drawing.Size(104, 20)
        Me.DateTimePicker2.TabIndex = 14
        Me.DateTimePicker2.Value = New Date(2005, 12, 31, 0, 0, 0, 0)
        '
        'TabControl1
        '
        Me.TabControl1.Controls.Add(Me.TabPageRest)
        Me.TabControl1.Controls.Add(Me.TabPageProps)
        Me.TabControl1.Controls.Add(Me.TabPagePoints)
        Me.TabControl1.Controls.Add(Me.TabPageXYZ)
        Me.TabControl1.Enabled = False
        Me.TabControl1.Location = New System.Drawing.Point(8, 8)
        Me.TabControl1.Name = "TabControl1"
        Me.TabControl1.SelectedIndex = 0
        Me.TabControl1.Size = New System.Drawing.Size(576, 392)
        Me.TabControl1.TabIndex = 8
        '
        'TabPageRest
        '
        Me.TabPageRest.Controls.Add(Me.Label3)
        Me.TabPageRest.Controls.Add(Me.Label2)
        Me.TabPageRest.Controls.Add(Me.DataGridTipos)
        Me.TabPageRest.Controls.Add(Me.chkRestrictTipo)
        Me.TabPageRest.Controls.Add(Me.DataGridPromotores)
        Me.TabPageRest.Controls.Add(Me.chkRestrictPromotor)
        Me.TabPageRest.Controls.Add(Me.chkRestTime)
        Me.TabPageRest.Controls.Add(Me.DateTimePicker1)
        Me.TabPageRest.Controls.Add(Me.DateTimePicker2)
        Me.TabPageRest.Location = New System.Drawing.Point(4, 22)
        Me.TabPageRest.Name = "TabPageRest"
        Me.TabPageRest.Size = New System.Drawing.Size(568, 366)
        Me.TabPageRest.TabIndex = 0
        Me.TabPageRest.Text = "Restrictions"
        '
        'Label3
        '
        Me.Label3.Location = New System.Drawing.Point(312, 336)
        Me.Label3.Name = "Label3"
        Me.Label3.Size = New System.Drawing.Size(80, 23)
        Me.Label3.TabIndex = 17
        Me.Label3.Text = "End"
        Me.Label3.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'Label2
        '
        Me.Label2.Location = New System.Drawing.Point(96, 336)
        Me.Label2.Name = "Label2"
        Me.Label2.Size = New System.Drawing.Size(80, 23)
        Me.Label2.TabIndex = 16
        Me.Label2.Text = "Start"
        Me.Label2.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'DataGridTipos
        '
        Me.DataGridTipos.DataMember = ""
        Me.DataGridTipos.HeaderForeColor = System.Drawing.SystemColors.ControlText
        Me.DataGridTipos.Location = New System.Drawing.Point(96, 184)
        Me.DataGridTipos.Name = "DataGridTipos"
        Me.DataGridTipos.Size = New System.Drawing.Size(464, 136)
        Me.DataGridTipos.TabIndex = 16
        '
        'chkRestrictTipo
        '
        Me.chkRestrictTipo.Location = New System.Drawing.Point(8, 184)
        Me.chkRestrictTipo.Name = "chkRestrictTipo"
        Me.chkRestrictTipo.Size = New System.Drawing.Size(88, 24)
        Me.chkRestrictTipo.TabIndex = 15
        Me.chkRestrictTipo.Text = "Tipo"
        '
        'TabPageProps
        '
        Me.TabPageProps.Controls.Add(Me.btnUnCheckAllParameters)
        Me.TabPageProps.Controls.Add(Me.btnCheckAllParameters)
        Me.TabPageProps.Controls.Add(Me.chkPromotorOnly)
        Me.TabPageProps.Controls.Add(Me.ListViewProps)
        Me.TabPageProps.Location = New System.Drawing.Point(4, 22)
        Me.TabPageProps.Name = "TabPageProps"
        Me.TabPageProps.Size = New System.Drawing.Size(568, 366)
        Me.TabPageProps.TabIndex = 3
        Me.TabPageProps.Text = "Properties"
        '
        'btnUnCheckAllParameters
        '
        Me.btnUnCheckAllParameters.Location = New System.Drawing.Point(472, 328)
        Me.btnUnCheckAllParameters.Name = "btnUnCheckAllParameters"
        Me.btnUnCheckAllParameters.Size = New System.Drawing.Size(88, 23)
        Me.btnUnCheckAllParameters.TabIndex = 7
        Me.btnUnCheckAllParameters.Text = "Uncheck All..."
        '
        'btnCheckAllParameters
        '
        Me.btnCheckAllParameters.Location = New System.Drawing.Point(472, 296)
        Me.btnCheckAllParameters.Name = "btnCheckAllParameters"
        Me.btnCheckAllParameters.Size = New System.Drawing.Size(88, 23)
        Me.btnCheckAllParameters.TabIndex = 6
        Me.btnCheckAllParameters.Text = "Check All..."
        '
        'chkPromotorOnly
        '
        Me.chkPromotorOnly.Checked = True
        Me.chkPromotorOnly.CheckState = System.Windows.Forms.CheckState.Checked
        Me.chkPromotorOnly.Enabled = False
        Me.chkPromotorOnly.Location = New System.Drawing.Point(456, 16)
        Me.chkPromotorOnly.Name = "chkPromotorOnly"
        Me.chkPromotorOnly.Size = New System.Drawing.Size(104, 72)
        Me.chkPromotorOnly.TabIndex = 1
        Me.chkPromotorOnly.Text = "Selected Promotor only"
        '
        'ListViewProps
        '
        Me.ListViewProps.CheckBoxes = True
        Me.ListViewProps.Columns.AddRange(New System.Windows.Forms.ColumnHeader() {Me.ColumnHeaderID, Me.ColumnHeaderName})
        Me.ListViewProps.Location = New System.Drawing.Point(8, 8)
        Me.ListViewProps.Name = "ListViewProps"
        Me.ListViewProps.Size = New System.Drawing.Size(432, 352)
        Me.ListViewProps.TabIndex = 0
        Me.ListViewProps.View = System.Windows.Forms.View.Details
        '
        'ColumnHeaderID
        '
        Me.ColumnHeaderID.Text = "ID"
        Me.ColumnHeaderID.Width = 100
        '
        'ColumnHeaderName
        '
        Me.ColumnHeaderName.Text = "Name"
        Me.ColumnHeaderName.Width = 327
        '
        'TabPagePoints
        '
        Me.TabPagePoints.Controls.Add(Me.btnUnCheckAllPoints)
        Me.TabPagePoints.Controls.Add(Me.btnCheckAllPoints)
        Me.TabPagePoints.Controls.Add(Me.chkPromotorOnlyPoints)
        Me.TabPagePoints.Controls.Add(Me.ListViewPoints)
        Me.TabPagePoints.Location = New System.Drawing.Point(4, 22)
        Me.TabPagePoints.Name = "TabPagePoints"
        Me.TabPagePoints.Size = New System.Drawing.Size(568, 366)
        Me.TabPagePoints.TabIndex = 4
        Me.TabPagePoints.Text = "Points"
        '
        'btnUnCheckAllPoints
        '
        Me.btnUnCheckAllPoints.Location = New System.Drawing.Point(472, 328)
        Me.btnUnCheckAllPoints.Name = "btnUnCheckAllPoints"
        Me.btnUnCheckAllPoints.Size = New System.Drawing.Size(88, 23)
        Me.btnUnCheckAllPoints.TabIndex = 5
        Me.btnUnCheckAllPoints.Text = "Uncheck All..."
        '
        'btnCheckAllPoints
        '
        Me.btnCheckAllPoints.Location = New System.Drawing.Point(472, 296)
        Me.btnCheckAllPoints.Name = "btnCheckAllPoints"
        Me.btnCheckAllPoints.Size = New System.Drawing.Size(88, 23)
        Me.btnCheckAllPoints.TabIndex = 4
        Me.btnCheckAllPoints.Text = "Check All..."
        '
        'chkPromotorOnlyPoints
        '
        Me.chkPromotorOnlyPoints.Checked = True
        Me.chkPromotorOnlyPoints.CheckState = System.Windows.Forms.CheckState.Checked
        Me.chkPromotorOnlyPoints.Enabled = False
        Me.chkPromotorOnlyPoints.Location = New System.Drawing.Point(456, 15)
        Me.chkPromotorOnlyPoints.Name = "chkPromotorOnlyPoints"
        Me.chkPromotorOnlyPoints.Size = New System.Drawing.Size(104, 72)
        Me.chkPromotorOnlyPoints.TabIndex = 3
        Me.chkPromotorOnlyPoints.Text = "Selected Promotor only"
        '
        'ListViewPoints
        '
        Me.ListViewPoints.CheckBoxes = True
        Me.ListViewPoints.Columns.AddRange(New System.Windows.Forms.ColumnHeader() {Me.ColumnHeader1, Me.ColumnHeader2})
        Me.ListViewPoints.Location = New System.Drawing.Point(8, 8)
        Me.ListViewPoints.Name = "ListViewPoints"
        Me.ListViewPoints.Size = New System.Drawing.Size(432, 352)
        Me.ListViewPoints.TabIndex = 2
        Me.ListViewPoints.View = System.Windows.Forms.View.Details
        '
        'ColumnHeader1
        '
        Me.ColumnHeader1.Text = "ID"
        Me.ColumnHeader1.Width = 100
        '
        'ColumnHeader2
        '
        Me.ColumnHeader2.Text = "Name"
        Me.ColumnHeader2.Width = 327
        '
        'TabPageXYZ
        '
        Me.TabPageXYZ.Controls.Add(Me.LabelTime)
        Me.TabPageXYZ.Controls.Add(Me.LabelProps)
        Me.TabPageXYZ.Controls.Add(Me.LabelPoints)
        Me.TabPageXYZ.Controls.Add(Me.LabelPromotor)
        Me.TabPageXYZ.Controls.Add(Me.GroupBox1)
        Me.TabPageXYZ.Location = New System.Drawing.Point(4, 22)
        Me.TabPageXYZ.Name = "TabPageXYZ"
        Me.TabPageXYZ.Size = New System.Drawing.Size(568, 366)
        Me.TabPageXYZ.TabIndex = 1
        Me.TabPageXYZ.Text = "Query / Data Files"
        '
        'LabelTime
        '
        Me.LabelTime.Font = New System.Drawing.Font("Microsoft Sans Serif", 8.25!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LabelTime.ForeColor = System.Drawing.Color.Blue
        Me.LabelTime.Location = New System.Drawing.Point(16, 48)
        Me.LabelTime.Name = "LabelTime"
        Me.LabelTime.Size = New System.Drawing.Size(248, 23)
        Me.LabelTime.TabIndex = 13
        Me.LabelTime.Text = "Label1"
        Me.LabelTime.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'LabelProps
        '
        Me.LabelProps.Font = New System.Drawing.Font("Microsoft Sans Serif", 8.25!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LabelProps.ForeColor = System.Drawing.Color.Blue
        Me.LabelProps.Location = New System.Drawing.Point(16, 112)
        Me.LabelProps.Name = "LabelProps"
        Me.LabelProps.Size = New System.Drawing.Size(248, 23)
        Me.LabelProps.TabIndex = 12
        Me.LabelProps.Text = "Label1"
        Me.LabelProps.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'LabelPoints
        '
        Me.LabelPoints.Font = New System.Drawing.Font("Microsoft Sans Serif", 8.25!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LabelPoints.ForeColor = System.Drawing.Color.Blue
        Me.LabelPoints.Location = New System.Drawing.Point(16, 80)
        Me.LabelPoints.Name = "LabelPoints"
        Me.LabelPoints.Size = New System.Drawing.Size(248, 23)
        Me.LabelPoints.TabIndex = 11
        Me.LabelPoints.Text = "Label1"
        Me.LabelPoints.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'LabelPromotor
        '
        Me.LabelPromotor.Font = New System.Drawing.Font("Microsoft Sans Serif", 8.25!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LabelPromotor.ForeColor = System.Drawing.Color.Blue
        Me.LabelPromotor.Location = New System.Drawing.Point(16, 16)
        Me.LabelPromotor.Name = "LabelPromotor"
        Me.LabelPromotor.Size = New System.Drawing.Size(248, 23)
        Me.LabelPromotor.TabIndex = 10
        Me.LabelPromotor.Text = "Label1"
        Me.LabelPromotor.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'GroupBox1
        '
        Me.GroupBox1.Controls.Add(Me.btnExportStationTimeSeries)
        Me.GroupBox1.Controls.Add(Me.ProgressBar1)
        Me.GroupBox1.Controls.Add(Me.btnExportXYZ)
        Me.GroupBox1.Controls.Add(Me.btnExportTimeSeries)
        Me.GroupBox1.Location = New System.Drawing.Point(16, 192)
        Me.GroupBox1.Name = "GroupBox1"
        Me.GroupBox1.Size = New System.Drawing.Size(256, 152)
        Me.GroupBox1.TabIndex = 9
        Me.GroupBox1.TabStop = False
        Me.GroupBox1.Text = "Write Data Files"
        '
        'btnExportStationTimeSeries
        '
        Me.btnExportStationTimeSeries.Location = New System.Drawing.Point(8, 88)
        Me.btnExportStationTimeSeries.Name = "btnExportStationTimeSeries"
        Me.btnExportStationTimeSeries.Size = New System.Drawing.Size(128, 23)
        Me.btnExportStationTimeSeries.TabIndex = 10
        Me.btnExportStationTimeSeries.Text = "Time Series by station"
        '
        'ProgressBar1
        '
        Me.ProgressBar1.Location = New System.Drawing.Point(8, 120)
        Me.ProgressBar1.Name = "ProgressBar1"
        Me.ProgressBar1.Size = New System.Drawing.Size(240, 23)
        Me.ProgressBar1.TabIndex = 9
        '
        'btnExportXYZ
        '
        Me.btnExportXYZ.Location = New System.Drawing.Point(8, 24)
        Me.btnExportXYZ.Name = "btnExportXYZ"
        Me.btnExportXYZ.Size = New System.Drawing.Size(128, 23)
        Me.btnExportXYZ.TabIndex = 7
        Me.btnExportXYZ.Text = "XYZ..."
        '
        'btnExportTimeSeries
        '
        Me.btnExportTimeSeries.Location = New System.Drawing.Point(8, 56)
        Me.btnExportTimeSeries.Name = "btnExportTimeSeries"
        Me.btnExportTimeSeries.Size = New System.Drawing.Size(128, 23)
        Me.btnExportTimeSeries.TabIndex = 8
        Me.btnExportTimeSeries.Text = "Time Series"
        '
        'MainMenu1
        '
        Me.MainMenu1.MenuItems.AddRange(New System.Windows.Forms.MenuItem() {Me.MenuItem1})
        '
        'MenuItem1
        '
        Me.MenuItem1.Index = 0
        Me.MenuItem1.MenuItems.AddRange(New System.Windows.Forms.MenuItem() {Me.mnuOpen, Me.mnuClose, Me.MenuItem4, Me.mnuExit})
        Me.MenuItem1.Text = "File"
        '
        'mnuOpen
        '
        Me.mnuOpen.Index = 0
        Me.mnuOpen.Text = "Load Database"
        '
        'mnuClose
        '
        Me.mnuClose.Enabled = False
        Me.mnuClose.Index = 1
        Me.mnuClose.Text = "Close"
        '
        'MenuItem4
        '
        Me.MenuItem4.Index = 2
        Me.MenuItem4.Text = "-"
        '
        'mnuExit
        '
        Me.mnuExit.Index = 3
        Me.mnuExit.Text = "Exit"
        '
        'StatusBar1
        '
        Me.StatusBar1.Location = New System.Drawing.Point(0, 437)
        Me.StatusBar1.Name = "StatusBar1"
        Me.StatusBar1.Panels.AddRange(New System.Windows.Forms.StatusBarPanel() {Me.STBarPanel})
        Me.StatusBar1.ShowPanels = True
        Me.StatusBar1.Size = New System.Drawing.Size(592, 22)
        Me.StatusBar1.TabIndex = 9
        '
        'STBarPanel
        '
        Me.STBarPanel.AutoSize = System.Windows.Forms.StatusBarPanelAutoSize.Spring
        Me.STBarPanel.Text = "Select File -> Open to open an exiting Data Base"
        Me.STBarPanel.Width = 576
        '
        'btnNext
        '
        Me.btnNext.Location = New System.Drawing.Point(504, 408)
        Me.btnNext.Name = "btnNext"
        Me.btnNext.TabIndex = 10
        Me.btnNext.Text = "Next ->"
        '
        'BtnPrev
        '
        Me.BtnPrev.Location = New System.Drawing.Point(424, 408)
        Me.BtnPrev.Name = "BtnPrev"
        Me.BtnPrev.TabIndex = 11
        Me.BtnPrev.Text = "<- Previous"
        '
        'frmAccessDataBase
        '
        Me.AutoScaleBaseSize = New System.Drawing.Size(5, 13)
        Me.ClientSize = New System.Drawing.Size(592, 459)
        Me.Controls.Add(Me.BtnPrev)
        Me.Controls.Add(Me.btnNext)
        Me.Controls.Add(Me.StatusBar1)
        Me.Controls.Add(Me.TabControl1)
        Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
        Me.Icon = CType(resources.GetObject("$this.Icon"), System.Drawing.Icon)
        Me.Menu = Me.MainMenu1
        Me.Name = "frmAccessDataBase"
        Me.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        Me.Text = "Get ""Gestão Costeira"" Data"
        CType(Me.DataGridPromotores, System.ComponentModel.ISupportInitialize).EndInit()
        Me.TabControl1.ResumeLayout(False)
        Me.TabPageRest.ResumeLayout(False)
        CType(Me.DataGridTipos, System.ComponentModel.ISupportInitialize).EndInit()
        Me.TabPageProps.ResumeLayout(False)
        Me.TabPagePoints.ResumeLayout(False)
        Me.TabPageXYZ.ResumeLayout(False)
        Me.GroupBox1.ResumeLayout(False)
        CType(Me.STBarPanel, System.ComponentModel.ISupportInitialize).EndInit()
        Me.ResumeLayout(False)

    End Sub

#End Region

    'Dim Connection As New OleDb.OleDbConnection
    Dim Connection As New NpgsqlConnection
    Public XYZFiles As New Collection
    Public TimeSeries As New Collection

    Private Sub mnuOpen_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles mnuOpen.Click
        Dim SQL As String

        Try
            '  If Me.OpenFileDialog1.ShowDialog = DialogResult.OK Then
            'Connection.ConnectionString = "PROVIDER=Microsoft.Jet.OLEDB.4.0;Data Source = " + OpenFileDialog1.FileName
            Connection.ConnectionString = "Server=192.168.20.45;Port=5432; User Id=webgc; Password=gestaocosteira; Database=gc;"
            Connection.Open()

            'Gets Names of properties and populates list view
            UpdateParameterListView()

            'Gets names of points and populates list view
            UpdatePointsListView()

            'Gets Name of Promotores and populates data grid
            SQL = "SELECT Promotores.Promotor_ID, Promotores.Nome FROM Promotores"
            '                Dim DataAdapter1 As New OleDb.OleDbDataAdapter(SQL, Connection)
            Dim DataAdapter1 As New NpgsqlDataAdapter(SQL, Connection)
            Dim DS1 As New DataTable
            DataAdapter1.Fill(DS1)
            DataGridPromotores.DataSource = DS1

            'Gets Tipo Campaign and populates data grid
            SQL = "SELECT TiposCampanha.TipoCampanha_ID, TiposCampanha.Nome FROM TiposCampanha"
            'Dim DataAdapter2 As New OleDb.OleDbDataAdapter(SQL, Connection)
            Dim DataAdapter2 As New NpgsqlDataAdapter(SQL, Connection)
            Dim DS2 As New DataTable
            DataAdapter2.Fill(DS2)
            DataGridTipos.DataSource = DS2

            ' End If

            Me.STBarPanel.Text = "Database " + Connection.Database.ToString + " loaded"
            Me.BtnPrev.Enabled = True
            Me.btnNext.Enabled = True
            Me.TabControl1.Enabled = True
            Me.TabControl1.SelectedIndex = 0
            Me.mnuOpen.Enabled = False
            Me.mnuClose.Enabled = True

        Catch ex As Exception
            MsgBox("Failed to open Database", MsgBoxStyle.Critical + MsgBoxStyle.OKOnly, "Error")
            MsgBox(ex.ToString)
            Me.STBarPanel.Text = "Failure to open DB"
            Me.BtnPrev.Enabled = False
            Me.btnNext.Enabled = False
            Me.TabControl1.Enabled = False
            Me.mnuOpen.Enabled = True
            Me.mnuClose.Enabled = False

        End Try
    End Sub

    Private Sub mnuClose_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles mnuClose.Click
        If Me.Connection.State = ConnectionState.Open Then
            Me.Connection.Close()
            Me.STBarPanel.Text = "Select File -> Load Database to load 'Gestao Costeira' Database"
            Me.BtnPrev.Enabled = False
            Me.btnNext.Enabled = False
            Me.TabControl1.Enabled = False
            Me.mnuOpen.Enabled = True
            Me.mnuClose.Enabled = False
        End If
    End Sub

    Private Sub mnuExit_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles mnuExit.Click
        Me.Close()
        Me.Finalize()
    End Sub

    Private Sub frmAccessDataBase_Closing(ByVal sender As Object, ByVal e As System.ComponentModel.CancelEventArgs) Handles MyBase.Closing
        If Me.Connection.State = ConnectionState.Open Then
            Connection.Close()
        End If
    End Sub

    'Populates list view with all avaliable parameters or, optional, with all parameters belonging to one promotor
    Private Sub UpdateParameterListView()

        If Me.Connection.State = ConnectionState.Open Then
            Dim SQL As String

            ListViewProps.Items.Clear()

            SQL = "SELECT Parametros.Parametro_ID, Parametros.Nome FROM Parametros"

            If Me.chkPromotorOnly.Checked And Me.chkPromotorOnly.Enabled Then
                SQL = "SELECT Parametros.Parametro_ID, Parametros.Nome FROM Parametros INNER JOIN "
                SQL += "Params_Promotores ON Parametros.Parametro_ID = Params_Promotores.Parametro_ID "
                SQL += "WHERE Params_Promotores.Promotor_ID = " + Me.DataGridPromotores.Item(DataGridPromotores.CurrentRowIndex, 0).ToString
            End If

            SQL += " ORDER BY Parametros.Nome"

            Try
                Dim DataAdapter2 As New NpgsqlDataAdapter(SQL, Connection)
                '                Dim DataAdapter2 As New OleDb.OleDbDataAdapter(SQL, Connection)
                Dim DS2 As New DataTable
                DataAdapter2.Fill(DS2)
                For Each CurrRow As DataRow In DS2.Rows
                    Dim LVItem As New ListViewItem(New String() {CType(CurrRow.Item(0), String), CurrRow.Item(1)})
                    Me.ListViewProps.Items.Add(LVItem)
                Next
            Catch ex As Exception
                MsgBox(ex.ToString)
            End Try
        End If
    End Sub

    Private Sub UpdatePointsListView()

        If Me.Connection.State = ConnectionState.Open Then
            Dim SQL As String

            ListViewPoints.Items.Clear()

            SQL = "SELECT Pontos.Ponto_ID, Pontos.Nome FROM Pontos"

            If Me.chkPromotorOnlyPoints.Checked And Me.chkPromotorOnlyPoints.Enabled Then
                SQL = "SELECT DISTINCT Amostras.Ponto_ID, Pontos.Nome FROM Amostras INNER JOIN "
                SQL += "Pontos ON Amostras.Ponto_ID = Pontos.Ponto_ID"
                SQL += " WHERE Amostras.Promotor_ID = " + Me.DataGridPromotores.Item(DataGridPromotores.CurrentRowIndex, 0).ToString
            End If

            SQL += " ORDER BY Pontos.Nome"

            Try
                Dim DataAdapter As New NpgsqlDataAdapter(SQL, Connection)
                'Dim DataAdapter As New OleDb.OleDbDataAdapter(SQL, Connection)
                Dim DS As New DataTable
                DataAdapter.Fill(DS)
                For Each CurrRow As DataRow In DS.Rows
                    Dim LVItem As New ListViewItem(New String() {CType(CurrRow.Item(0), String), CurrRow.Item(1)})
                    Me.ListViewPoints.Items.Add(LVItem)
                Next
            Catch ex As Exception
                MsgBox(ex.ToString)
            End Try
        End If
    End Sub

    Private Sub chkRestTime_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles chkRestTime.CheckedChanged
        Me.DateTimePicker1.Enabled = Me.chkRestTime.Checked
        Me.DateTimePicker2.Enabled = Me.chkRestTime.Checked
    End Sub

    Private Sub chkRestrictPromotor_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles chkRestrictPromotor.CheckedChanged
        Me.chkPromotorOnly.Enabled = chkRestrictPromotor.Checked
        Me.chkPromotorOnlyPoints.Enabled = chkRestrictPromotor.Checked
        UpdateParameterListView()
        UpdatePointsListView()
    End Sub

    Private Sub chkPromotorOnly_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles chkPromotorOnly.CheckedChanged
        UpdateParameterListView()
    End Sub

    Private Sub chkPromotorOnlyPoints_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles chkPromotorOnlyPoints.CheckedChanged
        UpdatePointsListView()
    End Sub

    Private Sub BuildSQLQuery(ByRef SQL As String, Optional ByVal ParameterName As String = Nothing, Optional ByVal PointName As String = Nothing)

        SQL = "SELECT Pontos.LongitudeMilitar, Pontos.LatitudeMilitar, Analises.Valor, Pontos.Nome, Amostras.Data, Amostras.Hora, Amostras.Profundidade FROM "
        SQL += "Pontos, Analises, Amostras WHERE "
        SQL += "Pontos.Ponto_ID = Amostras.Ponto_ID AND "
        SQL += "Amostras.Amostra_ID = Analises.Amostra_ID"
        If Me.chkRestrictPromotor.Checked Then
            SQL += " AND Amostras.Promotor_ID = " + Me.DataGridPromotores.Item(DataGridPromotores.CurrentRowIndex, 0).ToString
        End If

        If Me.chkRestrictTipo.Checked Then
            SQL += " AND Amostras.TipoCampanha_ID = " + Me.DataGridTipos.Item(DataGridTipos.CurrentRowIndex, 0).ToString
        End If

        If Me.chkRestTime.Checked Then
            SQL += " AND Amostras.Data >= '" + Me.DateTimePicker1.Value.ToString("yyyy-MM-dd") + " 00:00'"
            SQL += " AND Amostras.Data <= '" + Me.DateTimePicker2.Value.ToString("yyyy-MM-dd") + " 23:59'"
        End If


        'Adds Parameter Name to generate XYZ data files
        If Not IsNothing(ParameterName) Then
            SQL += " AND Analises.Parametro_ID = " + Chr(39) + ParameterName + Chr(39)
        End If

        If Not IsNothing(PointName) Then
            SQL += " AND Pontos.Ponto_ID = " + PointName
            SQL += " ORDER BY Amostras.Data, Amostras.Hora"
        Else
            SQL += " ORDER BY Pontos.Nome"
        End If


    End Sub

    Private Sub BuildSQLQueryAmostras(ByRef SQLAmostra As String, Optional ByVal PointName As String = Nothing)

        SQLAmostra = "SELECT Amostras.Data, Amostras.Hora, Amostras.Amostra_ID, Promotores.Promotor_ID, TiposCampanha.TipoCampanha_ID, Pontos.Ponto_ID, Amostras.Profundidade FROM "
        SQLAmostra += "TiposCampanha INNER JOIN (Promotores INNER JOIN ("
        SQLAmostra += "Pontos INNER JOIN Amostras ON "
        SQLAmostra += "Pontos.Ponto_ID = Amostras.Ponto_ID) ON "
        SQLAmostra += "(Pontos.Promotor_ID = Promotores.Promotor_ID) AND"
        SQLAmostra += "(Promotores.Promotor_ID = Amostras.Promotor_ID)) ON "
        SQLAmostra += "TiposCampanha.TipoCampanha_ID = Amostras.TipoCampanha_ID WHERE "

        If Me.chkRestrictPromotor.Checked Then
            SQLAmostra += " Amostras.Promotor_ID = " + Me.DataGridPromotores.Item(DataGridPromotores.CurrentRowIndex, 0).ToString
        End If

        If Me.chkRestrictTipo.Checked Then
            SQLAmostra += " AND Amostras.TipoCampanha_ID = " + Me.DataGridTipos.Item(DataGridTipos.CurrentRowIndex, 0).ToString
        End If

        If Me.chkRestTime.Checked Then
            SQLAmostra += " AND Amostras.Data >= '" + Me.DateTimePicker1.Value.ToString("yyyy-MM-dd") + " 00:00'"
            SQLAmostra += " AND Amostras.Data <= '" + Me.DateTimePicker2.Value.ToString("yyyy-MM-dd") + " 23:59'"
        End If

        SQLAmostra += " AND Pontos.Ponto_ID = " + PointName
        SQLAmostra += " ORDER BY Amostras.Data, Amostras.Hora"

    End Sub

    Private Sub BuildSQLQueryParameters(ByRef SQLparameter As String, ByVal ParameterID As String, ByVal AmostraID As String)

        SQLparameter = "SELECT Analises.Valor, Analises.Parametro_ID, Analises.Amostra_ID FROM "
        SQLparameter += "Parametros INNER JOIN (Amostras INNER JOIN Analises ON Amostras.Amostra_ID = Analises.Amostra_ID) ON "
        SQLparameter += "Parametros.Parametro_ID = Analises.Parametro_ID WHERE ((("
        SQLparameter += "Parametros.Parametro_ID)= '" + ParameterID + "'"
        SQLparameter += ") AND ((Amostras.Amostra_ID)= " + AmostraID + "))"

    End Sub

    Private Sub btnExportXYZ_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnExportXYZ.Click

        If Me.ListViewProps.CheckedItems.Count = 0 Then
            MsgBox("No Properties selected", MsgBoxStyle.OKOnly + MsgBoxStyle.Critical, "Error")
            Exit Sub
        End If

        Dim FolderBrwse As New FolderBrowserDialog
        Dim SQL As String

        If FolderBrwse.ShowDialog() = DialogResult.OK Then

            Me.ProgressBar1.Minimum = 1
            Me.ProgressBar1.Maximum = Me.ListViewProps.CheckedItems.Count
            Me.ProgressBar1.Value = 1
            For Each LVItem As ListViewItem In Me.ListViewProps.CheckedItems

                BuildSQLQuery(SQL, LVItem.SubItems(0).Text)
                'Dim DataAdapter As New OleDb.OleDbDataAdapter(SQL, Connection)
                Dim DataAdapter As New NpgsqlDataAdapter(SQL, Connection)
                Dim DT As New DataTable
                DataAdapter.Fill(DT)

                Dim FileName As String = FolderBrwse.SelectedPath + "\" + LVItem.SubItems(1).Text + ".xyz"

                Dim OutPutFile As New OutData(FileName)
                OutPutFile.WriteDataLine("SQL_COMMAND", SQL)
                If Me.chkPromotorOnly.Checked Then
                    OutPutFile.WriteDataLine("PROMOTOR", Me.DataGridPromotores.Item(DataGridPromotores.CurrentRowIndex, 1).ToString)
                Else
                    OutPutFile.WriteDataLine("PROMOTOR", "ALL")
                End If
                If Me.chkRestrictTipo.Checked Then
                    OutPutFile.WriteDataLine("TYPE", Me.DataGridTipos.Item(DataGridTipos.CurrentRowIndex, 1).ToString)
                Else
                    OutPutFile.WriteDataLine("TYPE", "ALL")
                End If
                If Me.chkRestTime.Checked Then
                    OutPutFile.WriteDataLine("START", Me.DateTimePicker1.Value)
                    OutPutFile.WriteDataLine("END", Me.DateTimePicker2.Value)
                Else
                    OutPutFile.WriteDataLine("NO_TIME_RESTRICTION")
                End If

                OutPutFile.WriteDataLine("<begin_xyz>")
                For Each CurrRow As DataRow In DT.Rows

                    Dim PointToWrite As Boolean = False
                    For Each LVItemPoint As ListViewItem In Me.ListViewPoints.CheckedItems
                        If (LVItemPoint.SubItems(1).Text.Equals(CurrRow.Item(3).ToString)) Then
                            PointToWrite = True
                            Exit For
                        End If
                    Next
                    If PointToWrite Then
                        OutPutFile.WriteDataLine(CurrRow.Item(0).ToString + " " + _
                                                 CurrRow.Item(1).ToString + " " + _
                                                 CurrRow.Item(2).ToString + " " + _
                                                 CurrRow.Item(3).ToString)
                    End If
                Next
                OutPutFile.WriteDataLine("<end_xyz>")
                OutPutFile.Finish()
                Me.XYZFiles.Add(FileName)
                Me.ProgressBar1.PerformStep()
            Next

            MsgBox("XYZ Files written", MsgBoxStyle.OKOnly + MsgBoxStyle.Information, "Information")
            Me.ProgressBar1.Minimum = 0
            Me.ProgressBar1.Value = 0
        End If

    End Sub

    Private Sub btnExportTimeSeries_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnExportTimeSeries.Click

        If Me.ListViewProps.CheckedItems.Count = 0 Then
            MsgBox("No Properties selected", MsgBoxStyle.OKOnly + MsgBoxStyle.Critical, "Error")
            Exit Sub
        End If

        If Me.ListViewPoints.CheckedItems.Count = 0 Then
            MsgBox("No Points selected", MsgBoxStyle.OKOnly + MsgBoxStyle.Critical, "Error")
            Exit Sub
        End If

        Dim FolderBrwse As New FolderBrowserDialog
        Dim SQL As String

        If FolderBrwse.ShowDialog() = DialogResult.OK Then

            Me.ProgressBar1.Minimum = 1
            Me.ProgressBar1.Maximum = Me.ListViewProps.CheckedItems.Count
            Me.ProgressBar1.Value = 1
            For Each LVItemProp As ListViewItem In Me.ListViewProps.CheckedItems

                For Each LVItemPoint As ListViewItem In Me.ListViewPoints.CheckedItems

                    BuildSQLQuery(SQL, LVItemProp.SubItems(0).Text, LVItemPoint.SubItems(0).Text)
                    Dim DataAdapter As New NpgsqlDataAdapter(SQL, Connection)
                    'Dim DataAdapter As New OleDb.OleDbDataAdapter(SQL, Connection)
                    Dim DT As New DataTable
                    DataAdapter.Fill(DT)

                    Dim FileName As String = FolderBrwse.SelectedPath + "\" + LVItemPoint.SubItems(1).Text + "_" + LVItemProp.SubItems(1).Text + ".srd"
                    Dim OutPutFile As New OutData(FileName)
                    OutPutFile.WriteDataLine("SQL_COMMAND", SQL)
                    If Me.chkPromotorOnly.Checked Then
                        OutPutFile.WriteDataLine("PROMOTOR", Me.DataGridPromotores.Item(DataGridPromotores.CurrentRowIndex, 1).ToString)
                    Else
                        OutPutFile.WriteDataLine("PROMOTOR", "ALL")
                    End If
                    If Me.chkRestrictTipo.Checked Then
                        OutPutFile.WriteDataLine("TYPE", Me.DataGridTipos.Item(DataGridTipos.CurrentRowIndex, 1).ToString)
                    Else
                        OutPutFile.WriteDataLine("TYPE", "ALL")
                    End If
                    If Me.chkRestTime.Checked Then
                        OutPutFile.WriteDataLine("START", Me.DateTimePicker1.Value)
                        OutPutFile.WriteDataLine("END", Me.DateTimePicker2.Value)
                    Else
                        OutPutFile.WriteDataLine("NO_TIME_RESTRICTION")
                    End If

                    If DT.Rows.Count > 0 Then

                        OutPutFile.WriteDataLine("TIME_UNITS", "DAYS")
                        Dim InitialDate As Date = CType(DT.Rows(0).Item(4), Date).Date
                        InitialDate = InitialDate.AddHours(CType(DT.Rows(0).Item(5), Date).Hour)
                        InitialDate = InitialDate.AddMinutes(CType(DT.Rows(0).Item(5), Date).Minute)
                        InitialDate = InitialDate.AddSeconds(CType(DT.Rows(0).Item(5), Date).Second)

                        OutPutFile.WriteDataLine("SERIE_INITIAL_DATA", InitialDate)
                        OutPutFile.WriteDataLine("Days Year Month Day Hour Minute Second Depth " + LVItemProp.SubItems(1).Text.Replace(" ", "_"))
                        OutPutFile.WriteDataLine("<BeginTimeSerie>")
                        For Each CurrRow As DataRow In DT.Rows
                            Dim ActualDate As Date = CType(CurrRow.Item(4), Date).Date
                            ActualDate = ActualDate.AddHours(CType(CurrRow.Item(5), Date).Hour)
                            ActualDate = ActualDate.AddMinutes(CType(CurrRow.Item(5), Date).Minute)
                            ActualDate = ActualDate.AddSeconds(CType(CurrRow.Item(5), Date).Second)
                            Dim TimeSinceBeginning As TimeSpan = Date.op_Subtraction(ActualDate, InitialDate)
                            OutPutFile.WriteDataLine(TimeSinceBeginning.TotalDays.ToString + " " + _
                                                     ActualDate.Year.ToString + " " + _
                                                     ActualDate.Month.ToString + " " + _
                                                     ActualDate.Day.ToString + " " + _
                                                     ActualDate.Hour.ToString + " " + _
                                                     ActualDate.Minute.ToString + " " + _
                                                     ActualDate.Second.ToString + " " + _
                                                     CurrRow.Item("Profundidade").ToString + " " + _
                                                     CurrRow.Item(2).ToString)
                        Next
                        OutPutFile.WriteDataLine("<EndTimeSerie>")
                    End If

                    OutPutFile.Finish()
                    Me.TimeSeries.Add(FileName)

                Next
                Me.ProgressBar1.PerformStep()
            Next

            MsgBox("Time Series written", MsgBoxStyle.OKOnly + MsgBoxStyle.Information, "Information")
            Me.ProgressBar1.Minimum = 0
            Me.ProgressBar1.Value = 0
        End If
    End Sub

    Private Sub btnCheckAllParameters_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnCheckAllParameters.Click
        For Each LvItem As ListViewItem In Me.ListViewProps.Items
            LvItem.Checked = True
        Next
    End Sub

    Private Sub btnUnCheckAllParameters_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnUnCheckAllParameters.Click
        For Each LvItem As ListViewItem In Me.ListViewProps.Items
            LvItem.Checked = False
        Next
    End Sub

    Private Sub btnCheckAllPoints_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnCheckAllPoints.Click
        For Each LvItem As ListViewItem In Me.ListViewPoints.Items
            LvItem.Checked = True
        Next
    End Sub

    Private Sub btnUnCheckAllPoints_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnUnCheckAllPoints.Click
        For Each LvItem As ListViewItem In Me.ListViewPoints.Items
            LvItem.Checked = False
        Next
    End Sub

    Private Sub btnNext_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnNext.Click
        Me.TabControl1.SelectedIndex = Math.Min(Me.TabControl1.SelectedIndex + 1, Me.TabControl1.TabCount)
    End Sub

    Private Sub BtnPrev_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BtnPrev.Click
        Me.TabControl1.SelectedIndex = Math.Max(Me.TabControl1.SelectedIndex - 1, 0)
    End Sub

    Private Sub TabControl1_SelectedIndexChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TabControl1.SelectedIndexChanged
        If TabControl1.SelectedIndex = Me.TabControl1.TabCount - 1 Then
            Me.btnNext.Enabled = False
        Else
            Me.btnNext.Enabled = True
        End If

        If TabControl1.SelectedIndex = 0 Then
            Me.BtnPrev.Enabled = False
        Else
            Me.BtnPrev.Enabled = True
        End If

        'Updates information
        If TabControl1.SelectedIndex = Me.TabControl1.TabCount - 1 Then
            If Me.chkPromotorOnly.Checked Then
                Me.LabelPromotor.Text = "Promotor : " + Me.DataGridPromotores.Item(DataGridPromotores.CurrentRowIndex, 1).ToString
            Else
                Me.LabelPromotor.Text = "Promotor : All"
            End If
            If Me.chkRestTime.Checked Then
                Me.LabelTime.Text = "Time : " + Me.DateTimePicker1.Value.ToShortDateString + " to " + Me.DateTimePicker2.Value.ToShortDateString
            Else
                Me.LabelTime.Text = "Time : No Restriction"
            End If

            Me.LabelPoints.Text = "Nº Points : " + Me.ListViewPoints.CheckedItems.Count.ToString
            Me.LabelProps.Text = "Nº Properties : " + Me.ListViewProps.CheckedItems.Count.ToString

        End If



    End Sub

    Private Sub DataGridPromotores_MouseUp(ByVal sender As Object, ByVal e As System.Windows.Forms.MouseEventArgs) Handles DataGridPromotores.MouseUp
        Me.UpdateParameterListView()
        Me.UpdatePointsListView()
    End Sub

    Private Sub btnExportStationTimeSeries_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnExportStationTimeSeries.Click

        If Me.ListViewProps.CheckedItems.Count = 0 Then
            MsgBox("No Properties selected", MsgBoxStyle.OKOnly + MsgBoxStyle.Critical, "Error")
            Exit Sub
        End If

        If Me.ListViewPoints.CheckedItems.Count = 0 Then
            MsgBox("No Points selected", MsgBoxStyle.OKOnly + MsgBoxStyle.Critical, "Error")
            Exit Sub
        End If

        Dim FolderBrwse As New FolderBrowserDialog
        Dim SQLAmostra As String

        If FolderBrwse.ShowDialog() = DialogResult.OK Then

            Me.ProgressBar1.Minimum = 1
            Me.ProgressBar1.Maximum = Me.ListViewProps.CheckedItems.Count
            Me.ProgressBar1.Value = 1

            For Each LVItemPoint As ListViewItem In Me.ListViewPoints.CheckedItems

                'Lista de datas das amostras existentes em cada estação
                BuildSQLQueryAmostras(SQLAmostra, LVItemPoint.SubItems(0).Text)
                Dim DataAdapter As New NpgsqlDataAdapter(SQLAmostra, Connection)
                'Dim DataAdapter As New OleDb.OleDbDataAdapter(SQLAmostra, Connection)
                Dim DT As New DataTable
                DataAdapter.Fill(DT)

                'array de valores das análises de todos os parametros seleccionados
                Dim TotalDataArray(DT.Rows.Count - 1, Me.ListViewProps.CheckedItems.Count - 1) As String

                If DT.Rows.Count > 0 Then

                    'contador de tempo
                    Dim tempo As Integer
                    tempo = 0

                    For Each CurrDT As DataRow In DT.Rows
                        'contador de parametros
                        Dim i As Integer
                        i = 0

                        'Por linha (por cada data) procura na base de dados o valor dos parâmetros pretendidos e 
                        'coloca no sítio certo da matriz TotalDataArray
                        For Each LVItemProp As ListViewItem In Me.ListViewProps.CheckedItems

                            Dim SQLparameter As String

                            BuildSQLQueryParameters(SQLparameter, LVItemProp.SubItems(0).Text, CurrDT.Item(2))
                            '                            Dim DataParam As New OleDb.OleDbDataAdapter(SQLparameter, Connection)
                            Dim DataParam As New NpgsqlDataAdapter(SQLparameter, Connection)
                            Dim Param As New DataTable
                            DataParam.Fill(Param)

                            'Quando não existe: valor =-999
                            If Param.Rows.Count <> 0 Then
                                TotalDataArray(tempo, i) = Param.Rows(0).Item(0)
                            Else
                                TotalDataArray(tempo, i) = "-999"
                            End If
                            i = i + 1
                        Next
                        tempo = tempo + 1
                    Next

                End If

                Dim OutPutFile As New OutData(FolderBrwse.SelectedPath + "\" + LVItemPoint.SubItems(1).Text + "_bystation" + ".srd")

                If Me.chkPromotorOnly.Checked Then
                    OutPutFile.WriteDataLine("PROMOTOR", Me.DataGridPromotores.Item(DataGridPromotores.CurrentRowIndex, 1).ToString)
                Else
                    OutPutFile.WriteDataLine("PROMOTOR", "ALL")
                End If
                If Me.chkRestrictTipo.Checked Then
                    OutPutFile.WriteDataLine("TYPE", Me.DataGridTipos.Item(DataGridTipos.CurrentRowIndex, 1).ToString)
                Else
                    OutPutFile.WriteDataLine("TYPE", "ALL")
                End If
                If Me.chkRestTime.Checked Then
                    OutPutFile.WriteDataLine("START", Me.DateTimePicker1.Value)
                    OutPutFile.WriteDataLine("END", Me.DateTimePicker2.Value)
                Else
                    OutPutFile.WriteDataLine("NO_TIME_RESTRICTION")
                End If

                If DT.Rows.Count > 0 Then

                    OutPutFile.WriteDataLine("TIME_UNITS", "DAYS")
                    Dim InitialDate As Date = CType(DT.Rows(0).Item(0), Date).Date
                    InitialDate = InitialDate.AddHours(CType(DT.Rows(0).Item(1), Date).Hour)
                    InitialDate = InitialDate.AddMinutes(CType(DT.Rows(0).Item(1), Date).Minute)
                    InitialDate = InitialDate.AddSeconds(CType(DT.Rows(0).Item(1), Date).Second)

                    OutPutFile.WriteDataLine("SERIE_INITIAL_DATA", InitialDate)

                    Dim StringNameLine As String

                    StringNameLine = "Days Year Month Day Hour Minute Second Depth"

                    For Each LVItemProp As ListViewItem In Me.ListViewProps.CheckedItems

                        StringNameLine = StringNameLine + " " + LVItemProp.SubItems(1).Text.Replace(" ", "_")
                    Next

                    OutPutFile.WriteDataLine(StringNameLine)
                    OutPutFile.WriteDataLine("<BeginTimeSerie>")

                    'Contador de tempo
                    Dim data As Integer
                    data = 0

                    For Each CurrRow As DataRow In DT.Rows
                        Dim ActualDate As Date = CType(CurrRow.Item(0), Date).Date
                        ActualDate = ActualDate.AddHours(CType(CurrRow.Item(1), Date).Hour)
                        ActualDate = ActualDate.AddMinutes(CType(CurrRow.Item(1), Date).Minute)
                        ActualDate = ActualDate.AddSeconds(CType(CurrRow.Item(1), Date).Second)

                        Dim TimeSinceBeginning As TimeSpan = Date.op_Subtraction(ActualDate, InitialDate)

                        Dim StringDataLine As String

                        StringDataLine = TimeSinceBeginning.TotalDays.ToString + " " + _
                                             ActualDate.Year.ToString + " " + _
                                             ActualDate.Month.ToString + " " + _
                                             ActualDate.Day.ToString + " " + _
                                             ActualDate.Hour.ToString + " " + _
                                             ActualDate.Minute.ToString + " " + _
                                             ActualDate.Second.ToString + " " + _
                                             CurrRow.Item("Profundidade").ToString

                        'Contador de propriedades
                        Dim p As Integer
                        p = 0

                        While p < Me.ListViewProps.CheckedItems.Count
                            StringDataLine = StringDataLine + " " + TotalDataArray(data, p)
                            p = p + 1
                        End While
                        OutPutFile.WriteDataLine(StringDataLine)

                        data = data + 1
                    Next

                    OutPutFile.WriteDataLine("<EndTimeSerie>")

                End If
                OutPutFile.Finish()
            Next

            Me.ProgressBar1.PerformStep()

            MsgBox("Time Series written", MsgBoxStyle.OKOnly + MsgBoxStyle.Information, "Information")
            Me.ProgressBar1.Minimum = 0
            Me.ProgressBar1.Value = 0
        End If
    End Sub
End Class
