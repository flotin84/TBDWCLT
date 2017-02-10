import sys
import os
import wx
import wx.grid as gridlib

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        # First, call the base class' __init__ method to create the frame
        wx.Frame.__init__(self, parent, id, title)
        self.CenterOnScreen()
        
        # Setup our menu bar.
        menuBar = wx.MenuBar()

        # File Menu Bar
        menu1 = wx.Menu()
        menu1.Append(101, "New Experiment File", "")
        menu1.Append(102, "Open Experiment File", "")
        menu1.AppendSeparator()
        menu1.Append(103, "Save", "")
        menu1.Append(104, "Save As", "")
        menuBar.Append(menu1, "File")
        
        # Analyze Menu Bar
        menu2 = wx.Menu()
        menu2.Append(201, "Plot experiment file", "")
        menu2.Append(202, "Spreadsheet")
        menuBar.Append(menu2, "Analyze")
        
        self.SetMenuBar(menuBar)
        
        # Menu Events
        self.Bind(wx.EVT_MENU, self.menuNew, id=101)
        self.Bind(wx.EVT_MENU, self.menuOpen, id=102)
        self.Bind(wx.EVT_MENU, self.menuSave, id=103)
        self.Bind(wx.EVT_MENU, self.menuSaveAs, id=104)
        self.Bind(wx.EVT_MENU, self.menuPlot, id=201)
        self.Bind(wx.EVT_MENU, self.menuSpreadsheet, id=202)
        
        # Make a textbox in the screen
        #tc = wx.TextCtrl(self, -1, "Welcome", style=wx.TE_READONLY|wx.TE_MULTILINE)
        #self.tc = tc
        
        
    # Menu functions called on Menu Events
    def menuNew(self, event):
        numberOfNodes = 1
        # Node select box
        wx.StaticText(self, -1, "New experiment file.", (15, 10))
        wx.StaticText(self, -1, "Node:", (15, 40))
        self.ch = wx.Choice(self, -1, (55, 40), choices = ['1'])
        self.Bind(wx.EVT_CHOICE, self.NodeSelect, self.ch)
        # Add another node
        addNodeButton = wx.Button(self, -1, "Add another node", (55, 50))
        self.Bind(wx.EVT_BUTTON, self.AddNode, addNodeButton)
        # Log and binary file select buttons
        logButton = wx.Button(self, -1, "Select log file", (15, 70))
        self.Bind(wx.EVT_BUTTON, self.OnLogButton, logButton)
        binaryButton = wx.Button(self, -1, "Select Binary file", (15, 100))
        self.Bind(wx.EVT_BUTTON, self.OnBinaryButton, binaryButton)
        
    def AddNode(self, event):
        numberOfNodes = numberOfNodes + 1
        self.ch.Append("%d" % numberOfNodes)
        
    def NodeSelect(self, event):
        selectedNode = int(event.GetString())
        sys.stdout.write('You selected %d\n' % selectedNode)
        
    def OnLogButton(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            sys.stdout.write('You selected %s\n' % dlg.GetPath())
            
        dlg.Destroy()
        
    def OnBinaryButton(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            sys.stdout.write('You selected %s\n' % dlg.GetPath())
            
        dlg.Destroy()
    
    def menuOpen(self, event):
        self.tc.Remove(0, 100)
        self.tc.WriteText("File -> Open experiment file")
    
    def menuSave(self, event):
        self.tc.Remove(0, 100)
        self.tc.WriteText("File -> Save")
        
    def menuSaveAs(self, event):
        self.tc.Remove(0, 100)
        self.tc.WriteText("File -> Save As")
        
    def menuPlot(self, event):
        self.tc.Remove(0, 100)
        self.tc.WriteText("Analyze -> Plot")
       
    def menuSpreadsheet(self, event):
        frame = SpreadsheetFrame(None, sys.stdout)
        frame.Show(True)
        
class SpreadsheetFrame(wx.Frame):
    def __init__(self, parent, log):
      wx.Frame.__init__(self, parent, -1, "Spreadsheet Display", size=(640,480))
      self.grid = SimpleGrid(self, log)
      
class SimpleGrid(gridlib.Grid):
    def __init__(self, parent, log):
      gridlib.Grid.__init__(self, parent, -1)
      self.CreateGrid(1000, 5)
        
# Every wxWidgets application must have a class derived from wx.App
class MyApp(wx.App):

    # wxWindows calls this method to initialize the application
    def OnInit(self):

        # Create an instance of our customized Frame class
        frame = MyFrame(None, -1, "Wireless Control Lab Tools")
        frame.Show(True)

        # Tell wxWindows that this is our main window
        self.SetTopWindow(frame)

        # Return a success flag
        return True



app = MyApp(0)     # Create an instance of the application class
app.MainLoop()     # Tell it to start processing events




