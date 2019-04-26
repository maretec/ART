Public Class ReadValue
    Inherits System.Windows.Forms.UserControl

#Region " Windows Form Designer generated code "

    Public Sub New()
        MyBase.New()

        'This call is required by the Windows Form Designer.
        InitializeComponent()

        'Add any initialization after the InitializeComponent() call

    End Sub

    'UserControl overrides dispose to clean up the component list.
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
    Friend WithEvents txtValue As System.Windows.Forms.TextBox
    Friend WithEvents ErrorProvider1 As System.Windows.Forms.ErrorProvider
    Friend WithEvents Label1 As System.Windows.Forms.Label
    <System.Diagnostics.DebuggerStepThrough()> Private Sub InitializeComponent()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.txtValue = New System.Windows.Forms.TextBox()
        Me.ErrorProvider1 = New System.Windows.Forms.ErrorProvider()
        Me.SuspendLayout()
        '
        'Label1
        '
        Me.Label1.Location = New System.Drawing.Point(0, 1)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(136, 23)
        Me.Label1.TabIndex = 0
        Me.Label1.Text = "Text"
        Me.Label1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'txtValue
        '
        Me.txtValue.Anchor = (System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right)
        Me.txtValue.BackColor = System.Drawing.SystemColors.Info
        Me.txtValue.Location = New System.Drawing.Point(136, 2)
        Me.txtValue.Name = "txtValue"
        Me.txtValue.Size = New System.Drawing.Size(56, 20)
        Me.txtValue.TabIndex = 1
        Me.txtValue.Text = "0.0"
        Me.txtValue.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'ErrorProvider1
        '
        Me.ErrorProvider1.DataMember = Nothing
        '
        'ReadValue
        '
        Me.Controls.AddRange(New System.Windows.Forms.Control() {Me.txtValue, Me.Label1})
        Me.Name = "ReadValue"
        Me.Size = New System.Drawing.Size(216, 24)
        Me.ResumeLayout(False)

    End Sub

#End Region

    Private myLabel As String
    Private myValue As Single

    Public Property Value() As Single
        Get
            Return myValue
        End Get
        Set(ByVal RealValue As Single)
            myValue = RealValue
            Me.txtValue.Text = RealValue
        End Set
    End Property

    Public Property LabelText() As String
        Get
            Return Label1.Text
        End Get
        Set(ByVal Value As String)
            Label1.Text = Value
        End Set
    End Property


    Private Sub txtValue_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles txtValue.TextChanged
        myValue = Val(Me.txtValue.Text)
    End Sub

    Private Sub txtValue_Validating(ByVal sender As Object, ByVal e As System.ComponentModel.CancelEventArgs) Handles txtValue.Validating
        If Not IsNumeric(Me.txtValue.Text) Then
            Me.ErrorProvider1.SetError(Me.txtValue, "Not a numeric Value")
        Else
            Me.ErrorProvider1.SetError(Me.txtValue, "")
        End If
    End Sub


End Class
