Public Class ReadFile
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
    Friend WithEvents Label1 As System.Windows.Forms.Label
    Friend WithEvents txtFile As System.Windows.Forms.TextBox
    Friend WithEvents btnBrowse As System.Windows.Forms.Button
    Friend WithEvents OpenFileDialog As System.Windows.Forms.OpenFileDialog
    Friend WithEvents SaveFileDialog As System.Windows.Forms.SaveFileDialog
    <System.Diagnostics.DebuggerStepThrough()> Private Sub InitializeComponent()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.txtFile = New System.Windows.Forms.TextBox()
        Me.btnBrowse = New System.Windows.Forms.Button()
        Me.OpenFileDialog = New System.Windows.Forms.OpenFileDialog()
        Me.SaveFileDialog = New System.Windows.Forms.SaveFileDialog()
        Me.SuspendLayout()
        '
        'Label1
        '
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(144, 24)
        Me.Label1.TabIndex = 1
        Me.Label1.Text = "FileID"
        Me.Label1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'txtFile
        '
        Me.txtFile.Anchor = (System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right)
        Me.txtFile.BackColor = System.Drawing.Color.FromArgb(CType(255, Byte), CType(255, Byte), CType(192, Byte))
        Me.txtFile.Location = New System.Drawing.Point(80, 2)
        Me.txtFile.Name = "txtFile"
        Me.txtFile.Size = New System.Drawing.Size(168, 20)
        Me.txtFile.TabIndex = 2
        Me.txtFile.Text = "Filename"
        Me.txtFile.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'btnBrowse
        '
        Me.btnBrowse.Anchor = (System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right)
        Me.btnBrowse.Location = New System.Drawing.Point(256, 1)
        Me.btnBrowse.Name = "btnBrowse"
        Me.btnBrowse.TabIndex = 3
        Me.btnBrowse.Text = "Browse..."
        '
        'OpenFileDialog
        '
        Me.OpenFileDialog.RestoreDirectory = True
        Me.OpenFileDialog.Title = "Select File..."
        '
        'SaveFileDialog
        '
        Me.SaveFileDialog.Title = "Save file as.."
        '
        'ReadFile
        '
        Me.Controls.AddRange(New System.Windows.Forms.Control() {Me.btnBrowse, Me.txtFile, Me.Label1})
        Me.Name = "ReadFile"
        Me.Size = New System.Drawing.Size(336, 24)
        Me.ResumeLayout(False)

    End Sub

#End Region

    Dim lNewFile As Boolean
    Dim lNewFileDefaultName As String
    Dim Filter As String

    Public Event FileChanged(ByVal sender As System.Object, ByVal e As System.EventArgs)

    Public Property File() As String
        Get
            Return txtFile.Text
        End Get
        Set(ByVal Value As String)
            txtFile.Text = Value
        End Set
    End Property

    Public Property FileID() As String
        Get
            Return Label1.Text
        End Get
        Set(ByVal Value As String)
            Label1.Text = Value
        End Set
    End Property

    Public Property FileFilter() As String
        Get
            Return Filter
        End Get

        Set(ByVal Value As String)
            Filter = Value
        End Set

    End Property

    Public Property NewFile() As Boolean
        Get
            Return lNewFile
        End Get

        Set(ByVal Value As Boolean)
            lNewFile = Value
        End Set
    End Property

    Public Property NewFileDefaultName() As String
        Get
            If lNewFile Then
                Return lNewFileDefaultName
            Else
                Return NewFileDefaultName.Empty
            End If
        End Get

        Set(ByVal Value As String)
            lNewFileDefaultName = Value
        End Set
    End Property

    Private Sub btnBrowse_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnBrowse.Click

        If lNewFile Then
            SaveFileDialog.Filter = Filter
            SaveFileDialog.FileName = lNewFileDefaultName
            If SaveFileDialog.ShowDialog = Windows.Forms.DialogResult.OK Then
                txtFile.Text = SaveFileDialog.FileName
            End If
        Else
            OpenFileDialog.Filter = Filter
            If OpenFileDialog.ShowDialog = Windows.Forms.DialogResult.OK Then
                txtFile.Text = OpenFileDialog.FileName
            End If
        End If

    End Sub


    Private Sub txtFile_TextChanged(ByVal sender As Object, ByVal e As System.EventArgs) Handles txtFile.TextChanged
        RaiseEvent FileChanged(txtFile, Nothing)
    End Sub
End Class
