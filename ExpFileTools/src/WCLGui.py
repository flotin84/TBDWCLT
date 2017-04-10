import sys
import os
import wx
import wx.grid as gridlib
import matplotlib
import numpy
import re
from numpy import *
from expfiles import *
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

# TODO:
# analyze needs range of coordinates
# modify needs to show description

class DefaultFrame(wx.Frame):
    def __init__(self, parent, id, title):
        # First, call the base class' __init__ method to create the frame
        wx.Frame.__init__(self, parent, id, title, size = (400,325))
        self.CenterOnScreen()
        self.SetBackgroundColour((232,239,252))
        
        # New file and analyze file buttons
        createExperimentFile = wx.Button(self, -1, "New experiment file", (15, 10), (350, 50))
        self.Bind(wx.EVT_BUTTON, self.menuNew, createExperimentFile)
        analyzeExperimentFile = wx.Button(self, -1, "Analyze experiment file", (15, 80), (350, 50))
        self.Bind(wx.EVT_BUTTON, self.menuAnalyze, analyzeExperimentFile)
        modifyExperimentFile = wx.Button(self, -1, "Modify experiment file", (15, 150), (350, 50))
        self.Bind(wx.EVT_BUTTON, self.menuModify, modifyExperimentFile)
        exportExperimentFile = wx.Button(self, -1, "Export experiment file", (15, 220), (350, 50))
        self.Bind(wx.EVT_BUTTON, self.menuExport, exportExperimentFile)
        
    def menuNew(self, event):
        frame = NewFile(self, -1, "New experiment file")
        frame.Show(True)
            
    def menuAnalyze(self, event):
        frame = AnalyzeSettings(self, -1, "Plot File")
        frame.Show(True)
        
    def menuModify(self, event):
        frame = ModifySettings(self, -1, "Modify file")
        frame.Show(True)

    def menuExport(self, event):
        frame = ExportSettings(self, -1, "Export file")
        frame.Show(True)
        
class ExportSettings(wx.Frame):
    
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.SetBackgroundColour((232,239,252))
        # Select file
        self.selectFile = wx.Button(self, -1, "Select experiment file", (15, 10))
        self.Bind(wx.EVT_BUTTON, self.selectFileButton, self.selectFile)
        
        # Select node
        wx.StaticText(self, -1, "Node:", (15, 40))
        self.nodeChoice = wx.Choice(self, -1, (55, 40), choices = ['1'])
        self.Bind(wx.EVT_CHOICE, self.nodeSelectEvent, self.nodeChoice)
        self.nodeChoice.Enable(False)
        
        # select log/bin
        wx.StaticText(self, -1, "Log/bin:",(100, 40))
        self.nodeselect = wx.Choice(self, -1, (150, 40), choices = ['log', 'bin'])
        self.Bind(wx.EVT_CHOICE, self.choiceEvent, self.nodeselect)
        self.export_filepath = ""
        self.nodeselect.Enable(False)

        # Export file
        self.exportFile = wx.Button(self, -1, "Export experiment file", (15, 70))
        self.Bind(wx.EVT_BUTTON, self.exportFileEvent, self.exportFile)
        self.exportFile.Enable(False)

        # log file size
        self.file_name_log = wx.StaticText(self, wx.ID_ANY, "", (160, 70))
        self.file_name_bin = wx.StaticText(self, wx.ID_ANY, "", (160, 90))
        
        

    def exportFileEvent(self, event):
        if self.isLog:
            dlg = wx.FileDialog(
                self, message="Save File As",
                defaultDir=os.getcwd(), 
                defaultFile=expreader.get_node_file_name(self.export_filepath, self.node, self.isLog),
                wildcard="log",
                style=wx.SAVE
                )
            dlg.SetFilterIndex(2)

            self.nodePathList = ['']

            currentIndex = 2 * int(self.nodeChoice.GetCurrentSelection()) + 1
            if dlg.ShowModal() == wx.ID_OK:
                if len(self.nodePathList) == currentIndex:
                    self.nodePathList.append(dlg.GetPath())
                elif len(self.nodePathList) >= currentIndex:
                    self.nodePathList[currentIndex] = dlg.GetPath()
                else:
                    while len(self.nodePathList) < currentIndex:
                        self.nodePathList.append("")
                    self.nodePathList.append(dlg.GetPath())
                i = 0
                node_list = []
            expexporter.export_log(self.export_filepath,dlg.GetPath(), self.node)

        else:
        
            dlg = wx.FileDialog(
                self, message="Save File As",
                defaultDir=os.getcwd(), 
                defaultFile=expreader.get_node_file_name(self.export_filepath, self.node, self.isLog),
                wildcard=".bin",
                style=wx.SAVE
                )
            dlg.SetFilterIndex(2)

            self.nodePathList = ['']

            currentIndex = 2 * int(self.nodeChoice.GetCurrentSelection()) + 1
            if dlg.ShowModal() == wx.ID_OK:
                if len(self.nodePathList) == currentIndex:
                    self.nodePathList.append(dlg.GetPath())
                elif len(self.nodePathList) >= currentIndex:
                    self.nodePathList[currentIndex] = dlg.GetPath()
                else:
                    while len(self.nodePathList) < currentIndex:
                        self.nodePathList.append("")
                    self.nodePathList.append(dlg.GetPath())
                i = 0
                node_list = []
            expexporter.export_bin(self.export_filepath,dlg.GetPath(), self.node)

        dlg.Destroy()
  
    def choiceEvent(self, event):
        self.node = int(self.nodeChoice.GetCurrentSelection())
        if ((self.nodeselect.GetCurrentSelection() == 0) and (self.export_filepath != "")): #log
            dataframe = expreader.get_node_file(self.export_filepath, int(self.nodeChoice.GetCurrentSelection()), True)
            self.isLog = True
            print self.isLog
        else: #bin
            dataframe = expreader.get_node_file(self.export_filepath, int(self.nodeChoice.GetCurrentSelection()), False)
            self.isLog = False
            print self.isLog
            
    def nodeSelectEvent(self, event):
        self.choiceEvent(event)

    #def enableAll(self):
     #   self.nodeChoice.Enable(True)

    def selectFileButton(self, event):
        self.node = 1 #initial value
        self.isLog = True #initial value
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.export_filepath = dlg.GetPath()
            export_nnodes = expreader.get_number_of_nodes(self.export_filepath)
            export_menuchoices = 2
            while (export_menuchoices <= export_nnodes):
                self.nodeChoice.Append("%d" % export_menuchoices)
                export_menuchoices += 1
            sys.stdout.write('You selected %s\n' % dlg.GetPath())
            self.nodeChoice.Enable(True)
            self.exportFile.Enable(True)
            self.nodeselect.Enable(True)
        #self.selectFile.SetLabel(self.export_filepath)
            
        dlg.Destroy()
        
    def nodeSelectEvent(self, event):
        nodeIndex = int(self.nodeChoice.GetCurrentSelection())
        # Log file name
        if (expreader.has_log_file(self.export_filepath, nodeIndex)):
            logFileName = expreader.get_node_file_name(self.export_filepath, nodeIndex, True)
            #self.file_name_log.SetLabel(logFileName)
            #self.addLogFile.SetLabel("Replace log file")
        else:
            self.file_name_log.SetLabel("No file")
        # bin file name
        if (expreader.has_bin_file(self.export_filepath, nodeIndex)):
            binFileName = expreader.get_node_file_name(self.export_filepath, nodeIndex, False)
            #self.file_name_bin.SetLabel(binFileName)
            #self.addBinFile.SetLabel("Replace bin file")
        else:
            self.file_name_bin.SetLabel("No file")
        
class ModifySettings(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.SetBackgroundColour((232,239,252))
        
        self.fileDescript = wx.StaticText(self, -1, "", (15, 140))
        
        
        # Select file
        selectFile = wx.Button(self, -1, "Select experiment file", (15, 10))
        self.Bind(wx.EVT_BUTTON, self.selectFileButton, selectFile)
        
        # Select node
        wx.StaticText(self, -1, "Node:", (15, 40))
        self.nodeChoice = wx.Choice(self, -1, (55, 40))
        self.nodeChoice.Enable(False)
        self.Bind(wx.EVT_CHOICE, self.nodeSelectEvent, self.nodeChoice)
        
        # add another node
        self.addNodeButton = wx.Button(self, -1, "Add another node", (230, 10))
        self.Bind(wx.EVT_BUTTON, self.AddNode, self.addNodeButton)
        self.addNodeButton.Enable(False)
        
        # delete node
        self.deleteNodeButton = wx.Button(self, -1, "Delete current node", (230, 40))
        self.deleteNodeButton.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.deleteNode, self.deleteNodeButton)
        
        # delete log file
        self.deleteLogButton = wx.Button(self, -1, "Delete log file", (15, 70))
        self.deleteLogButton.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.deleteLog, self.deleteLogButton)
        
        # select log file
        self.addLogFile = wx.Button(self, -1, "  Add log file  ", (130, 70))
        self.addLogFile.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.logFileAdd, self.addLogFile)
        
        # log file size
        self.file_name_log = wx.StaticText(self, wx.ID_ANY, "", (240, 75))
        
        # binary file size
        self.file_name_bin = wx.StaticText(self, wx.ID_ANY, "", (240, 105))
        
        # delete binary file
        self.deleteBinButton = wx.Button(self, -1, "Delete bin file", (15, 100))
        self.deleteBinButton.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.deleteBin, self.deleteBinButton) 
        
        # select binary file
        self.addBinFile = wx.Button(self, -1, "  Add bin file  ", (130, 100))
        self.addBinFile.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.binFileAdd, self.addBinFile)
        
    def deleteBin(self, event):
        # delete bin file of selected node
        expwriter.del_node_file(self.modify_filepath, self.nodeChoice.GetCurrentSelection(), False)
        # update the gui
        self.nodeSelectEvent(self)    
        
    def deleteLog(self, event):
        # delete log file of selected node
        expwriter.del_node_file(self.modify_filepath, self.nodeChoice.GetCurrentSelection(), True)
        # update the gui
        self.nodeSelectEvent(self)
        
        
    def logFileAdd(self, event):
        #add log file to selected node
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            expwriter.set_node_file(self.modify_filepath, self.nodeChoice.GetCurrentSelection(), dlg.GetPath(), True)
            #update the gui
            self.nodeSelectEvent(self)
    
    def binFileAdd(self, event):
        #add bin file to selected node
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            expwriter.set_node_file(self.modify_filepath, self.nodeChoice.GetCurrentSelection(), dlg.GetPath(), False)
            #update the gui
            self.nodeSelectEvent(self)
           
    def deleteNode(self, event):
        if (self.modify_nnodes != 0):
            expwriter.del_node(self.modify_filepath, self.nodeChoice.GetCurrentSelection())
            self.modify_nnodes -= 1
            if (self.nodeChoice.GetCurrentSelection >= 2):
                self.nodeChoice.SetSelection(self.nodeChoice.GetCurrentSelection() - 1)
                self.nodeChoice.Delete(self.nodeChoice.GetCurrentSelection() + 1)
            else:
                self.nodeChoice.Delete(self.nodeChoice.GetCurrentSelection())
    
    
    def enableAll(self):
        self.nodeChoice.Enable(True)
        self.addNodeButton.Enable(True)
        self.deleteNodeButton.Enable(True)
        self.addLogFile.Enable(True)
        self.deleteLogButton.Enable(True)
        self.deleteBinButton.Enable(True)
        self.addBinFile.Enable(True)
        text = expreader.get_exp_notes(self.modify_filepath)
        text = re.sub("(.{64})", "\\1\n", text, 0, re.DOTALL)
        self.fileDescript.SetLabel(text)
        
    def AddNode(self, event):
        self.modify_nnodes += 1
        self.nodeChoice.Append("%d" % self.modify_nnodes)
        self.nodeChoice.SetSelection(self.modify_nnodes - 1)
        self.nodeSelectEvent(self)
        expwriter.add_nodes(self.modify_filepath, node.Node())
                
        
    def selectFileButton(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.modify_filepath = dlg.GetPath()
            self.modify_nnodes = expreader.get_number_of_nodes(self.modify_filepath)
            modify_menuchoices = 1
            self.nodeChoice.Clear()
            while (modify_menuchoices <= self.modify_nnodes):
                self.nodeChoice.Append("%d" % modify_menuchoices)
                modify_menuchoices += 1
            sys.stdout.write('You selected %s\n' % dlg.GetPath())
            self.enableAll()
            
        dlg.Destroy()
        
    def nodeSelectEvent(self, event):
        nodeIndex = int(self.nodeChoice.GetCurrentSelection())
        # Log file name
        if (expreader.has_log_file(self.modify_filepath, nodeIndex)):
            logFileName = expreader.get_node_file_name(self.modify_filepath, nodeIndex, True)
            self.file_name_log.SetLabel(logFileName)
            self.addLogFile.SetLabel("Replace log file")
        else:
            self.file_name_log.SetLabel("No file")
            self.addLogFile.SetLabel("Add log file")
        # bin file name
        if (expreader.has_bin_file(self.modify_filepath, nodeIndex)):
            binFileName = expreader.get_node_file_name(self.modify_filepath, nodeIndex, False)
            self.file_name_bin.SetLabel(binFileName)
            self.addBinFile.SetLabel("Replace bin file")
        else:
            self.file_name_bin.SetLabel("No file")
            self.addBinFile.SetLabel("Add bin file")
        
        
class AnalyzeSettings(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.SetBackgroundColour((232,239,252))
        
        self.fileDescript = wx.StaticText(self, -1, "", (15, 160))
        
        # Select file
        selectFile = wx.Button(self, -1, "Select experiment file", (15, 10))
        self.Bind(wx.EVT_BUTTON, self.selectFileButton, selectFile)
        
        # Select node
        wx.StaticText(self, -1, "Node:", (15, 40))
        self.ch = wx.Choice(self, -1, (55, 40), choices = ['1'])
        self.Bind(wx.EVT_CHOICE, self.nodeSelectEvent, self.ch)
        self.ch.Enable(False)
        
        # select log/bin
        wx.StaticText(self, -1, "Log/bin:",(100, 40))
        self.nodeselect = wx.Choice(self, -1, (150, 40), choices = ['log', 'bin'])
        self.Bind(wx.EVT_CHOICE, self.choiceEvent, self.nodeselect)
        self.nodeselect.Enable(False)
        
        # log column select
        wx.StaticText(self, -1, "Select column", (15, 75))
        self.columnChoice = wx.Choice(self, -1, (100, 75), choices = [])
        self.columnChoice.Enable(False)
        
        # Plot or spreadsheet
        self.createPlot = wx.Button(self, -1, "Plot", (15, 120), (100, 40))
        self.Bind(wx.EVT_BUTTON, self.menuPlot, self.createPlot)
        self.createPlot.Enable(False)
        self.createSheet = wx.Button(self, -1, "Spreadsheet", (115, 120), (100, 40))
        self.Bind(wx.EVT_BUTTON, self.menuSpreadsheet, self.createSheet)
        self.createSheet.Enable(False)
        
        self.logBinChosen = 0
        self.nodeChosen = 0
        
    def enableAll(self):
        self.ch.Enable(True)
        self.nodeselect.Enable(True)
        text = expreader.get_exp_notes(self.analyze_filepath)
        text = re.sub("(.{64})", "\\1\n", text, 0, re.DOTALL)
        self.fileDescript.SetLabel(text)
        
    def choiceEvent(self, event): 
        self.logBinChosen = 1
        if (self.nodeChosen == 1):
            self.createPlot.Enable(True)
            self.createSheet.Enable(True)
        if ((self.nodeselect.GetCurrentSelection() == 0) and (self.analyze_filepath != "")): #log
            dataframe = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), True)
            self.columnChoice.Clear()
            d_list = list(dataframe)
            for i in range(0, len(d_list)):
                self.columnChoice.Append(d_list[i])
            self.columnChoice.Enable(True)
        else:
            self.columnChoice.Enable(False)
            
    def nodeSelectEvent(self, event):
        self.nodeChosen = 1
        if (self.logBinChosen == 1):
            self.createPlot.Enable(True)
            self.createSheet.Enable(True)
        if ((self.nodeselect.GetCurrentSelection() == 0) and (self.analyze_filepath != "")): #log
            dataframe = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), True)
            self.columnChoice.Clear()
            d_list = list(dataframe)
            for i in range(0, len(d_list)):
                self.columnChoice.Append(d_list[i])
            self.columnChoice.Enable(True)
        else:
            self.columnChoice.Enable(False)
    
    def menuSpreadsheet(self, event):
        if (self.nodeselect.GetCurrentSelection() == 0):
            frame = SpreadsheetFrame(None, -1, "Sheet Display", dataframe = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), True), columnIndex = self.columnChoice.GetCurrentSelection())
        else:
            frame = SpreadsheetFrame(None, -1, "Sheet Display", dataframe = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), False), columnIndex = -1)
            
        frame.Show(True)
    
    def menuPlot(self, event):
        if (self.nodeselect.GetCurrentSelection() == 0):
            frame = PlotFrame(None, -1, "Plot Display", dataframe = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), True), columnIndex = self.columnChoice.GetCurrentSelection())
        else:
            frame = PlotFrame(None, -1, "Plot Display", dataframe = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), False), columnIndex = -1)
            
        frame.Show(True)
        
    def selectFileButton(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.analyze_filepath = dlg.GetPath()
            self.analyze_nnodes = expreader.get_number_of_nodes(self.analyze_filepath)
            analyze_menuchoices = 2
            while (analyze_menuchoices <= self.analyze_nnodes):
                self.ch.Append("%d" % analyze_menuchoices)
                analyze_menuchoices += 1
            sys.stdout.write('You selected %s\n' % dlg.GetPath())
            self.enableAll()
            
        dlg.Destroy()
        
        
class PlotFrame(wx.Frame):
    def __init__(self, parent, id, title, dataframe, columnIndex):
        wx.Frame.__init__(self, parent, id, title)
        self.SetBackgroundColour((232,239,252))
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        if (columnIndex != -1):
            self.draw(numpyArray = dataframe.as_matrix(columns = dataframe.columns[columnIndex:columnIndex+1]))
        else: #bin
            self.draw(numpyArray = dataframe.as_matrix())
        
    
    def draw(self, numpyArray):
        self.axes.plot(numpyArray)
        
        
class NewFile(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size = (475, 350))
        self.SetBackgroundColour((232,239,252))

        self.numberOfNodes = 1
        self.nodePathList = []
        # Description of file
        wx.StaticText(self, -1, "Description of file:", (15, 8))
        self.fileDescription = wx.TextCtrl(self, -1, "", size=(200, 100), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos = (15, 25))
        # master/slave type
        self.masterSlaveChoice = wx.Choice(self, -1, (95, 140), choices = ['master', 'slave'])
        # Node select box
        wx.StaticText(self, -1, "Node:", (15, 140))
        self.ch = wx.Choice(self, -1, (55, 140), choices = ['1'])
        self.Bind(wx.EVT_CHOICE, self.NodeSelect, self.ch)
        self.ch.SetStringSelection('1')
        # Add another node
        addNodeButton = wx.Button(self, -1, "Add another node", (180, 140))
        self.Bind(wx.EVT_BUTTON, self.AddNode, addNodeButton)
        # Delete node
        deleteNodeButton = wx.Button(self, -1, "Delete last node", (310, 140))
        self.Bind(wx.EVT_BUTTON, self.DeleteNode, deleteNodeButton)
        # Log and binary file select buttons
        logButton = wx.Button(self, -1, "Select log file", (15, 170))
        self.Bind(wx.EVT_BUTTON, self.OnLogButton, logButton)
        binaryButton = wx.Button(self, -1, "Select Binary file", (15, 200))
        self.Bind(wx.EVT_BUTTON, self.OnBinaryButton, binaryButton)
        # Size of files 
        self.file_size_log = wx.StaticText(self, wx.ID_ANY, "No file selected", (140, 175))
        self.file_size_bin = wx.StaticText(self, wx.ID_ANY, "No file selected", (140, 205))
        # Create experiment file buttons
        createFileButton = wx.Button(self, -1, "Save file as", (15, 235))
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
            
            while (i < self.numberOfNodes):
                if (self.masterSlaveChoice.GetCurrentSelection() == 0):
                    node_list.append(node.Node(self.nodePathList[2*i], self.nodePathList[2*i+1], 'master'))
                else:
                    node_list.append(node.Node(self.nodePathList[2*i], self.nodePathList[2*i+1]))
                i = i + 1
            
            expwriter.generate_experiment_file(dlg.GetPath(), node_list, self.fileDescription.GetValue())
            #print expreader.get_exp_notes(dlg.GetPath())
            #print ( expreader.get_node_file(dlg.GetPath(), 1, True))
        
        dlg.Destroy()
        
    def DeleteNode(self, event):
        if self.numberOfNodes >= 2:
            self.numberOfNodes -= 1
            self.ch.Delete(self.numberOfNodes)
        
    def AddNode(self, event):
        self.numberOfNodes += 1
        self.ch.Append("%d" % self.numberOfNodes)
        
    def NodeSelect(self, event):
        selectedNode = int(event.GetString())
        currentIndex = 2*(selectedNode - 1)
        if (len(self.nodePathList) > currentIndex) and (self.nodePathList[currentIndex] != ''):
            self.file_size_log.SetLabel(str(os.path.getsize(self.nodePathList[2*(selectedNode - 1)])/1024) + " KB, %s" % self.nodePathList[2*(selectedNode - 1)])
        else:
            self.file_size_log.SetLabel("No file selected")
        if (len(nodePathList) > currentIndex + 1) and (self.nodePathList[currentIndex + 1] != ''):
            self.file_size_bin.SetLabel(str(os.path.getsize(self.nodePathList[currentIndex + 1])/1024) + " KB, %s" % self.nodePathList[currentIndex + 1])
        else:
            self.file_size_bin.SetLabel("No file selected")
        
    def OnLogButton(self, event):
        currentIndex = 2 * int(self.ch.GetCurrentSelection())
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            if len(self.nodePathList) == currentIndex:
                self.nodePathList.append(dlg.GetPath())
                self.nodePathList.append('')
            elif len(self.nodePathList) >= currentIndex:
                self.nodePathList[currentIndex] = dlg.GetPath()
            else:
                while len(self.nodePathList) < currentIndex:
                    self.nodePathList.append("")
                self.nodePathList.append(dlg.GetPath())
            self.file_size_log.SetLabel(str(os.path.getsize(dlg.GetPath())/1024) + " KB, %s" % dlg.GetPath())
            print('You selected %s\n' % dlg.GetPath())
            
        dlg.Destroy()
        
    def OnBinaryButton(self, event):
        currentIndex = 2 * int(self.ch.GetCurrentSelection()) + 1
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            if len(self.nodePathList) == currentIndex:
                    self.nodePathList.append(dlg.GetPath())
            elif len(self.nodePathList) >= currentIndex:
                    self.nodePathList[currentIndex] = dlg.GetPath()
            else:
                while len(nodePathList) < currentIndex:
                    self.nodePathList.append("")
                self.nodePathList.append(dlg.GetPath())
            self.file_size_bin.SetLabel(str(os.path.getsize(dlg.GetPath())/1024) + " KB, %s" % dlg.GetPath())
            print('You selected %s\n' % dlg.GetPath())
            
        dlg.Destroy()
    
class SpreadsheetFrame(wx.Frame):
    def __init__(self, parent, id, title, dataframe, columnIndex):
        wx.Frame.__init__(self, parent, -1, "Spreadsheet Display", size=(640,480))
        self.SetBackgroundColour((232,239,252))
        panel = wx.Panel(self, -1)
        if (columnIndex != -1):
            numpyArray = dataframe.as_matrix(columns = dataframe.columns[columnIndex:columnIndex+1])
        else:
            numpyArray = dataframe.as_matrix()
            
        grid = Grid(panel, numpyArray)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        panel.Layout()
      
class Grid(gridlib.Grid):
    #Copy code lifted from following link
    #http://stackoverflow.com/questions/28509629/work-with-ctrl-c-and-ctrl-v-to-copy-and-paste-into-a-wx-grid-in-wxpython

    def __init__(self, parent, data):
        gridlib.Grid.__init__(self, parent, -1)
        wx.EVT_KEY_DOWN(self, self.OnKey)
        table = DataTable(data)
        self.SetTable(table, True)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK,self.showPopupMenu)
              
    def OnKey(self, event):
        # If Ctrl+C is pressed...
        if event.ControlDown() and event.GetKeyCode() == 67:
            self.Copy(event)
    
    def getSelectionDimension(self):
        if not self.IsSelection():
            rows = 0
            cols = 0
        elif self.GetSelectionBlockTopLeft() == []:
            rows = 1
            cols = 1
        else:
            rows = self.GetSelectionBlockBottomRight()[0][0] - self.GetSelectionBlockTopLeft()[0][0] + 1
            cols = self.GetSelectionBlockBottomRight()[0][1] - self.GetSelectionBlockTopLeft()[0][1] + 1
        return(rows, cols)
    
    def Copy(self, event):
        rows, cols = self.getSelectionDimension()
        if (rows == 0 and cols ==0):
            return
        iscell = (rows == 1 and cols == 1)
            
        # data variable contain text that must be set in the clipboard
        data = ''
        # For each cell in selected range append the cell value in the data variable
        # Tabs '\t' for cols and '\r' for rows
        for r in range(rows):
            for c in range(cols):
                if iscell:
                    data += str(self.GetCellValue(self.GetGridCursorRow() + r, self.GetGridCursorCol() + c))
                else:
                    data += str(self.GetCellValue(self.GetSelectionBlockTopLeft()[0][0] + r, self.GetSelectionBlockTopLeft()[0][1] + c))
                if c < cols - 1:
                    data += '\t'
            data += '\n'
        clipboard = wx.TextDataObject()
        # Set data object value
        clipboard.SetText(data)
        # Put the data in the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")
    
    
    def showPopupMenu(self, event):       
        menu = wx.Menu()
        copyOption = menu.Append(wx.ID_ANY,text="Copy")
        self.Bind(wx.EVT_MENU, self.Copy, copyOption)
        if not self.IsSelection():
            copyOption.Enable(False)
        
        self.PopupMenu(menu)
        menu.Destroy()

            
class DataTable(gridlib.PyGridTableBase):
    def __init__(self, data):
        gridlib.PyGridTableBase.__init__(self)
        self.data = data
        
    def GetNumberRows(self):
        return self.data.shape[0]
        
    def GetNumberCols(self):
        return self.data.shape[1]
        
    def GetValue(self, row, col):
        return self.data[row][col]
        
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