import sys
import os
import wx
import wx.grid as gridlib
import matplotlib
import wx.dataview as dv
import numpy
import inspect
import re
from numpy import *
from expfiles import *
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt

# TODO:
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
        global analyzeframe
        analyzeframe = AnalyzeSettings(self, -1, "Plot File")
        analyzeframe.Show(True)
        
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
        wx.Frame.__init__(self, parent, id, title, size=(620, 375))
        self.SetBackgroundColour((232,239,252))
        
        self.fileDescript = wx.StaticText(self, -1, "", (15, 160))
        
        # Filter 
        filter = wx.StaticText(self, -1, "Filter data", (250, 10))
        filter.SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        
        # editable text boxes
        self.value = wx.TextCtrl(self, -1, "", size=(50,20), style = wx.TE_PROCESS_ENTER, pos = (430, 70))
        self.value.Enable(False)
        
        # choice for operation
        self.operation = wx.Choice(self, -1, (370, 70), choices = ['<', '>', '=', '<=', '>='])
        self.operation.Enable(False)
        self.column = wx.Choice(self, -1, (250, 70), choices = [])
        self.column.Enable(False)
        
        # label for text boxes and choice
        wx.StaticText(self, -1, "Column", (250, 48))
        wx.StaticText(self, -1, "Operation", (365, 48))
        wx.StaticText(self, -1, "Value", (435, 48))
        
        # list of filters
        self.filterList = dv.DataViewListCtrl(self, pos = (250, 105), size=(250, 200))
        self.filterList.AppendTextColumn('column', width = 75)
        self.filterList.AppendTextColumn('operation', width = 75)
        self.filterList.AppendTextColumn('value', width = 100)
        dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU(self.filterList, -1, self.rightClickFilterList)
        
        # add filter button
        self.addFilter = wx.Button(self, -1, "Add filter", (500, 67))
        self.Bind(wx.EVT_BUTTON, self.addFilterButton, self.addFilter)
        
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
        wx.StaticText(self, -1, "Y-Axis", (15, 75))
        self.columnChoice = wx.Choice(self, -1, (100, 75), choices = [])
        self.columnChoice.Enable(False)
        
        # x axis
        wx.StaticText(self, -1, "X-Axis", (15, 100))
        self.xaxisChoice = wx.Choice(self, -1, (100, 100), choices = ['Index'])
        self.xaxisChoice.Enable(False)

        # Bin choices
        wx.StaticText(self, -1, "Bin Choices", (15, 125))
        self.binChoice = wx.Choice(self, -1, (100, 125), choices = ['Ampiltude']) #,'Phase','I vs Q'])
        self.binChoice.Enable(False)
        
        # Plot or spreadsheet
        self.createPlot = wx.Button(self, -1, "Plot", (15, 155), (100, 65))
        self.Bind(wx.EVT_BUTTON, self.menuPlot, self.createPlot)
        self.createPlot.Enable(False)
        self.createSheet = wx.Button(self, -1, "Spreadsheet", (115, 155), (100, 65))
        self.Bind(wx.EVT_BUTTON, self.menuSpreadsheet, self.createSheet)
        self.createSheet.Enable(False)
        
        self.logBinChosen = 0
        self.nodeChosen = 0
        self.filterItemCount = 0
        
    def rightClickFilterList(self, event):
        self.rightclickitem = wx.dataview.DataViewEvent.GetItem(event)
        if (self.rightclickitem.IsOk()):
            global analyzeframe
            menu = wx.Menu()
            menu.Append(1, "delete")
            wx.EVT_MENU(menu, 1, self.deleteFilterMenuSelection)
            
            analyzeframe.PopupMenu(menu, event.GetPosition())
            menu.Destroy()
            
    def deleteFilterMenuSelection(self, event):
        self.filterList.DeleteItem(self.filterList.ItemToRow(self.rightclickitem))
        self.filterItemCount += -1
        
    def addFilterButton(self, event):
        value = float(self.value.GetValue())
        if (self.column.GetCurrentSelection() >= 0 and self.operation.GetCurrentSelection >= 0 and self.isfloat(self.value.GetValue())):
            data = [self.column.GetString(self.column.GetCurrentSelection()), self.operation.GetString(self.operation.GetCurrentSelection()), self.value.GetValue()]
            self.filterList.AppendItem(data)
            self.filterItemCount += 1
        
    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
        
        
    def enableAll(self):
        self.ch.Enable(True)
        self.nodeselect.Enable(True)
        text = expreader.get_exp_notes(self.analyze_filepath)
        text = re.sub("(.{64})", "\\1\n", text, 0, re.DOTALL)
        self.fileDescript.SetLabel(text)
        self.value.Enable(True)
        self.operation.Enable(True)
        
    def choiceEvent(self, event): 
        self.logBinChosen = 1
        if (self.nodeChosen == 1):
            self.createPlot.Enable(True)
            self.createSheet.Enable(True)
        if ((self.nodeselect.GetCurrentSelection() == 0) and (self.analyze_filepath != "")): #log
            dataframe = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), True)
            self.columnChoice.Clear()
            self.column.Clear()
            self.xaxisChoice.Clear()
            self.xaxisChoice.Append('Index')
            d_list = list(dataframe)
            for i in range(0, len(d_list)):
                self.columnChoice.Append(d_list[i])
                self.column.Append(d_list[i])
                self.xaxisChoice.Append(d_list[i])
            self.columnChoice.Enable(True)
            self.column.Enable(True)
            self.binChoice.Enable(False)
            self.xaxisChoice.Enable(True)
        else:
            self.columnChoice.Enable(False)
            self.column.Enable(False)
            self.xaxisChoice.Enable(False)
            self.binChoice.Enable(True)
            self.createPlot.Enable(True)
            
    def nodeSelectEvent(self, event):
        self.nodeChosen = 1
        if (self.logBinChosen == 1):
            self.createPlot.Enable(True)
            self.createSheet.Enable(True)
        if ((self.nodeselect.GetCurrentSelection() == 0) and (self.analyze_filepath != "")): #log
            dataframe = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), True)
            self.columnChoice.Clear()
            self.column.Clear()
            self.xaxisChoice.Clear()
            self.xaxisChoice.Append('Index')
            d_list = list(dataframe)
            for i in range(0, len(d_list)):
                self.columnChoice.Append(d_list[i])
                self.column.Append(d_list[i])
                self.xaxisChoice.Append(d_list[i])
            self.columnChoice.Enable(True)
            self.column.Enable(True)
            self.xaxisChoice.Enable(True)
        else:
            self.columnChoice.Enable(False)
            self.column.Enable(False)
            self.xaxisChoice.Enable(False)
    
    def menuSpreadsheet(self, event):
        if (self.nodeselect.GetCurrentSelection() == 0):
            df = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), True)

            # https://docs.scipy.org/doc/numpy/reference/generated/numpy.where.html
            
            
            frame = SpreadsheetFrame(None, -1, "Sheet Display", dataframe = df, columnIndex = self.columnChoice.GetCurrentSelection())
        else:
            frame = SpreadsheetFrame(None, -1, "Sheet Display", dataframe = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), False), columnIndex = -1)
            
        frame.Show(True)
    
    def menuPlot(self, event):
        if (self.nodeselect.GetCurrentSelection() == 0):
            df = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), True)
            
            # xaxis
            # dataframe.as_matrix(columns = dataframe.columns[columnIndex:columnIndex+1])
            differentAxis = 0
            xaxesIndex = 0
            if self.xaxisChoice.GetCurrentSelection() > 0:
                differentAxis = df[self.xaxisChoice.GetString(self.xaxisChoice.GetCurrentSelection())]
                xaxesIndex = 1
            
            numcols = 2 #0=data, 1=operation, 2=value
            data = 0
            operation = 1
            value = 2
            
            for row in range(self.filterItemCount): # Loop over all filters
                if (self.filterList.GetTextValue(row, data) == self.columnChoice.GetString(self.columnChoice.GetCurrentSelection())): # same data
                    op = self.filterList.GetTextValue(row, operation)
                    if op == '<':
                        df = df[df[self.filterList.GetTextValue(row, data)] < int(self.filterList.GetTextValue(row, value))]
                    elif op == '>':
                        df = df[df[self.filterList.GetTextValue(row, data)] > int(self.filterList.GetTextValue(row, value))]
                    elif op == '=':
                        df = df[df[self.filterList.GetTextValue(row, data)] == int(self.filterList.GetTextValue(row, value))]
                    elif op == '<=':
                        df = df[df[self.filterList.GetTextValue(row, data)] <= int(self.filterList.GetTextValue(row, value))]
                    elif op == '>=':
                        df = df[df[self.filterList.GetTextValue(row, data)] >= int(self.filterList.GetTextValue(row, value))]

                        
            frame = PlotFrame(None, -1, "Plot Display", dataframe = df, columnIndex = self.columnChoice.GetCurrentSelection(), xaxis = differentAxis, xaxisIndex = xaxesIndex, bintype = self.binChoice)
        else:
            frame = PlotFrame(None, -1, "Plot Display", dataframe = expreader.get_node_file(self.analyze_filepath, int(self.ch.GetCurrentSelection()), False), columnIndex = -1, xaxis = 0, xaxisIndex = 0, bintype = self.binChoice.GetCurrentSelection())
            
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
    def __init__(self, parent, id, title, dataframe, columnIndex, xaxis, xaxisIndex, bintype):
        self.dataframe = dataframe
        self.columnIndex = columnIndex
        if (columnIndex != -1):#log
            self.draw(numpyArray = dataframe.as_matrix(columns = dataframe.columns[columnIndex:columnIndex+1]), xaxis = xaxis, xaxisIndex = xaxisIndex)
            #sheet = SpreadsheetFrame(None, -1, "Sheet Display", dataframe, columnIndex)
        else: #bin
            #Amplitude
            if (bintype == 0):
                mpl.rcParams['agg.path.chunksize'] = 500
                numpyArrayReal = dataframe.astype(float)[::2]
                numpyArrayImaginary = dataframe.astype(float)[1::2]
                #numpyArray = numpy.absolute(numpyArrayReal*numpyArrayImaginary)
                self.draw(numpy.absolute(dataframe), xaxis=0, xaxisIndex=0)
                #self.draw(numpy.absolute(numpyArrayImaginary), xaxis=0, xaxisIndex=0)

            #Phase
            if (bintype == 1):
                numpyArrayReal = dataframe.astype(float)[::2]
                numpyArrayImaginary = dataframe.astype(float)[1::2]
                numpyArray = numpy.arctan(numpyArrayReal/numpyArrayImaginary)
                self.draw(numpyArray, xaxis=0, xaxisIndex=0)
            #I vs Q
            if (bintype == 2):
                numpyArrayReal = dataframe.astype(float)[::2]
                numpyArrayImaginary = dataframe.astype(float)[1::2]
                numpyArray = numpy.absolute(numpyArrayImaginary)
                self.draw(numpy.sqrt(numpyArray), xaxis=0, xaxisIndex=0)
    
    def draw(self, numpyArray, xaxis, xaxisIndex):
        def onclick(event):
            if event.dblclick:
                print(event.xdata, event.ydata)
                if (self.columnIndex != -1):
                    frame = SpreadsheetFrame(None, -1, "Sheet Display", self.dataframe, self.columnIndex)
                    frame.Show(True)
            
        fig = plt.figure(1)
        plt.subplot(111)
        if (xaxisIndex == 1):
            try:
                plt.plot(xaxis, numpyArray)
            except Exception:
                error = wx.MessageDialog(analyzeframe, 'Error: axis have different number of data points\nTry removing filter or filtering both sets of data',
                               'Error',
                               wx.OK
                               )
                error.ShowModal()
                error.Destroy()
                
        else:
            plt.plot(numpyArray)
        fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()
        #self.axes.plot(numpyArray
        
        
        

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
        if (len(self.nodePathList) > currentIndex + 1) and (self.nodePathList[currentIndex + 1] != ''):
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
                while len(self.nodePathList) < currentIndex:
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
            columnNames = list(dataframe)[columnIndex:columnIndex+1]
        else:
            numpyArray = dataframe.as_matrix()
            columnNames = list(dataframe)
            
        grid = Grid(panel, numpyArray, columnNames)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        panel.Layout()
      
class Grid(gridlib.Grid):
    #Copy code lifted from following link
    #http://stackoverflow.com/questions/28509629/work-with-ctrl-c-and-ctrl-v-to-copy-and-paste-into-a-wx-grid-in-wxpython

    def __init__(self, parent, data,columnNames):
        gridlib.Grid.__init__(self, parent, -1)
        table = DataTable(data)
        self.SetTable(table, True)
        
        print columnNames
        for i in range(len(columnNames)):
            #print self.GetColLabelValue(i) 
            print columnNames[i]
            self.SetColLabelValue(i, columnNames[i]) 
            #print table.GetColLabelValue(i)
            
        self.SetColLabelValue(0, "Custom")
        self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
            
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK,self.showPopupMenu)
        wx.EVT_KEY_DOWN(self, self.OnKey)
            
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
        self.SetColLabelValue(0, "Custom")
        
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
