Public Class ProgressBarForm
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
    Friend WithEvents ProgressBar As System.Windows.Forms.ProgressBar
    Friend WithEvents lblMessage As System.Windows.Forms.Label
    Friend WithEvents Label1 As System.Windows.Forms.Label
    <System.Diagnostics.DebuggerStepThrough()> Private Sub InitializeComponent()
        Me.ProgressBar = New System.Windows.Forms.ProgressBar()
        Me.lblMessage = New System.Windows.Forms.Label()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.SuspendLayout()
        '
        'ProgressBar
        '
        Me.ProgressBar.Location = New System.Drawing.Point(8, 48)
        Me.ProgressBar.Name = "ProgressBar"
        Me.ProgressBar.Size = New System.Drawing.Size(296, 32)
        Me.ProgressBar.Step = 1
        Me.ProgressBar.TabIndex = 0
        '
        'lblMessage
        '
        Me.lblMessage.Location = New System.Drawing.Point(8, 0)
        Me.lblMessage.Name = "lblMessage"
        Me.lblMessage.Size = New System.Drawing.Size(344, 40)
        Me.lblMessage.TabIndex = 1
        Me.lblMessage.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'Label1
        '
        Me.Label1.Location = New System.Drawing.Point(312, 56)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(40, 16)
        Me.Label1.TabIndex = 2
        Me.Label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'ProgressBarForm
        '
        Me.AutoScaleBaseSize = New System.Drawing.Size(5, 13)
        Me.ClientSize = New System.Drawing.Size(360, 88)
        Me.Controls.AddRange(New System.Windows.Forms.Control() {Me.Label1, Me.lblMessage, Me.ProgressBar})
        Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
        Me.MaximizeBox = False
        Me.Name = "ProgressBarForm"
        Me.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        Me.Text = "Progress..."
        Me.ResumeLayout(False)

    End Sub

#End Region

    Public Sub ShowMe()
        Me.Show()
    End Sub

    Public Sub PutMessage(ByVal mess() As Char)
        Dim message As String
        'convert mess to string so it is displayable
        message = New String(mess, 0, mess.Length())
        lblMessage.Text = mess
        Me.Refresh()
    End Sub

    Public Sub PutMessage(ByVal mess As String)
        lblMessage.Text = mess
        Me.Refresh()
    End Sub

    Public Sub ChangeBarValue(ByVal vall As Double, ByVal minVal As Double, ByVal maxVal As Double)
        Dim barValue As Integer
        ProgressBar.Minimum = 0
        ProgressBar.Maximum = 1000
        barValue = Int((vall - minVal) / (maxVal - minVal) * 1000)
        If (vall > maxVal) Then barValue = 1000
        If (vall < minVal) Then barValue = 0
        ProgressBar.Value = barValue
        ProgressBar.Update()

        Me.Label1.Text = (barValue / 10).ToString + "%"
    End Sub

    Public Sub GoodBye()
        Me.Close()
    End Sub

    Public Sub SetTitle(ByVal title As String)
        Me.Text = title
    End Sub

    Public Sub UpdateMe()
        ProgressBar.Update()
        Me.Refresh()
    End Sub

End Class
