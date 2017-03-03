import sys
import os
import wx
import wx.grid as gridlib
import matplotlib
import numpy
from numpy import *
from expfiles import *
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

class DefaultFrame(wx.Frame):
    def __init__(self, parent, id, title):
        # First, call the base class' __init__ method to create the frame
        wx.Frame.__init__(self, parent, id, title)
        self.CenterOnScreen()
        self.SetBackgroundColour((232,239,252))
        
        # Setup our menu bar.
        menuBar = wx.MenuBar()

        # File Menu Bar
        menu1 = wx.Menu()
        menu1.Append(101, "New Experiment File", "")
        menu1.Append(102, "Open Experiment File", "")
        menu1.AppendSeparator()
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
        self.Bind(wx.EVT_MENU, self.menuPlot, id=201)
        self.Bind(wx.EVT_MENU, self.menuSpreadsheet, id=202)
        # Default greeting
        
        wx.StaticText(self, -1, "Welcome. To create a new experiment file, select File->New experiment file", (10,10))
        
    def menuNew(self, event):
        frame = NewFile(self, -1, "New experiment file")
        #self.DefaultFrame.Hide()
        frame.Show(True)
            
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
        frame = AnalyzeSettings(self, -1, "Plot File")
        frame.Show(True)
        
       
    def menuSpreadsheet(self, event):
        frame = SpreadsheetFrame(None, sys.stdout)
        frame.Show(True)
        
class AnalyzeSettings(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.SetBackgroundColour((232,239,252))
        global analyze_filepath
        # Select file
        selectFile = wx.Button(self, -1, "Select experiment file", (15, 10))
        self.Bind(wx.EVT_BUTTON, self.selectFileButton, selectFile)
        # Select node
        wx.StaticText(self, -1, "Node:", (15, 40))
        self.ch = wx.Choice(self, -1, (55, 40), choices = ['1'])
        # select log/bin
        
        # select range
        
        
    def selectFileButton(self, event):
        global analyze_filepath
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            analyze_filepath = dlg.GetPath()
            analyze_nnodes = expreader.get_number_of_nodes(analyze_filepath)
            analyze_menuchoices = 2
            while (analyze_menuchoices <= analyze_nnodes):
                self.ch.Append("%d" % analyze_menuchoices)
                analyze_menuchoices += 1
            sys.stdout.write('You selected %s\n' % dlg.GetPath())
            
        dlg.Destroy()
        
        
class PlotFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.SetBackgroundColour((232,239,252))
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        self.draw()
    
    def draw(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)
        
        
class NewFile(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.SetBackgroundColour((232,239,252))
        
        global numberOfNodes, nodePathList
        numberOfNodes = 1
        nodePathList = ['']
        # Description of file
        
        
        # Node select box
        wx.StaticText(self, -1, "New experiment file.", (15, 10))
        wx.StaticText(self, -1, "Node:", (15, 40))
        self.ch = wx.Choice(self, -1, (55, 40), choices = ['1'])
        self.Bind(wx.EVT_CHOICE, self.NodeSelect, self.ch)
        self.ch.SetStringSelection('1')
        # Add another node
        addNodeButton = wx.Button(self, -1, "Add another node", (100, 40))
        self.Bind(wx.EVT_BUTTON, self.AddNode, addNodeButton)
        # Delete node
        deleteNodeButton = wx.Button(self, -1, "Delete last node", (230, 40))
        self.Bind(wx.EVT_BUTTON, self.DeleteNode, deleteNodeButton)
        # Log and binary file select buttons
        logButton = wx.Button(self, -1, "Select log file", (15, 70))
        self.Bind(wx.EVT_BUTTON, self.OnLogButton, logButton)
        binaryButton = wx.Button(self, -1, "Select Binary file", (15, 100))
        self.Bind(wx.EVT_BUTTON, self.OnBinaryButton, binaryButton)
        # Size of files 
        self.file_size_log = wx.StaticText(self, wx.ID_ANY, "No file selected", (140, 75))
        self.file_size_bin = wx.StaticText(self, wx.ID_ANY, "No file selected", (140, 105))
        # Create experiment file buttons
        createFileButton = wx.Button(self, -1, "Save file as", (15,135))
        self.Bind(wx.EVT_BUTTON, self.createFile, createFileButton)
        
    def createFile(self, event):
        dlg = wx.FileDialog(
            self, message="Save File As",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=".h5",
            style=wx.SAVE
            )
        dlg.SetFilterIndex(2)
        
        if dlg.ShowModal() == wx.ID_OK:
            i = 0
            node_list = []
            while (i < numberOfNodes):
                node_list.append(node.Node(nodePathList[2*i], nodePathList[2*i+1]))
                i = i + 1
            
            expwriter.generate_experiment_file(dlg.GetPath(), node_list)
            print ( expreader.get_node_file(dlg.GetPath(), 1, True))
        
        dlg.Destroy()
        
    def DeleteNode(self, event):
        global numberOfNodes
        if numberOfNodes >= 2:
            numberOfNodes -= 1
            self.ch.Delete(numberOfNodes)
        
    def AddNode(self, event):
        global numberOfNodes
        numberOfNodes += 1
        self.ch.Append("%d" % numberOfNodes)
        
    def NodeSelect(self, event):
        global nodePathList
        selectedNode = int(event.GetString())
        currentIndex = 2*(selectedNode - 1)
        if (len(nodePathList) > currentIndex) and (nodePathList[currentIndex] != ''):
            self.file_size_log.SetLabel(str(os.path.getsize(nodePathList[2*(selectedNode - 1)])/1024) + " KB")
        else:
            self.file_size_log.SetLabel("No file selected")
        if (len(nodePathList) > currentIndex + 1) and (nodePathList[currentIndex + 1] != ''):
            self.file_size_bin.SetLabel(str(os.path.getsize(nodePathList[currentIndex + 1])/1024) + " KB")
        else:
            self.file_size_bin.SetLabel("No file selected")
        
    def OnLogButton(self, event):
        global nodePathList
        currentIndex = 2 * int(self.ch.GetCurrentSelection())
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            if len(nodePathList) == currentIndex:
                nodePathList.append(dlg.GetPath())
            elif len(nodePathList) >= currentIndex:
                nodePathList[currentIndex] = dlg.GetPath()
            else:
                while len(nodePathList) < currentIndex:
                    nodePathList.append("")
                nodePathList.append(dlg.GetPath())
            self.file_size_log.SetLabel(str(os.path.getsize(dlg.GetPath())/1024) + " KB")
            sys.stdout.write('You selected %s\n' % dlg.GetPath())
            
        dlg.Destroy()
        
    def OnBinaryButton(self, event):
        global nodePathList
        currentIndex = 2 * int(self.ch.GetCurrentSelection()) + 1
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            if len(nodePathList) == currentIndex:
                    nodePathList.append(dlg.GetPath())
            elif len(nodePathList) >= currentIndex:
                    nodePathList[currentIndex] = dlg.GetPath()
            else:
                while len(nodePathList) < currentIndex:
                    nodePathList.append("")
                nodePathList.append(dlg.GetPath())
            self.file_size_bin.SetLabel(str(os.path.getsize(dlg.GetPath())/1024) + " KB")
            sys.stdout.write('You selected %s\n' % dlg.GetPath())
            
        dlg.Destroy()
    
        
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
        frame = DefaultFrame(None, -1, "Wireless Control Lab Tools")
        frame.Show(True)

        # Tell wxWindows that this is our main window
        self.SetTopWindow(frame)

        # Return a success flag
        return True



app = MyApp(0)     # Create an instance of the application class
app.MainLoop()     # Tell it to start processing events




