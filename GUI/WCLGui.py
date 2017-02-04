import sys
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
        tc = wx.TextCtrl(self, -1, "Welcome", style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.tc = tc
        
        
    # Menu functions called on Menu Events
    def menuNew(self, event):
        self.tc.Remove(0, 100)
        self.tc.WriteText("File -> New experiment file")
    
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




