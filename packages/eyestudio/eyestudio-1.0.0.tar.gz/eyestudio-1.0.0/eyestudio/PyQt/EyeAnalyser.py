
# Frameworks
import sys
import os
from PyQt4 import QtCore, QtGui

# Project
from EyeAnalyserUI import Ui_mainWindow
from .Engine.Engine import Engine
from .Engine.Analyser import Analyser
from .Engine.Filter import Filter, STATE_NAMES
from SharedFunctions import sharedLoadWidgetList, sharedLoadGroupbox, sharedGetParameters
from ParameterHandler import GetParameterHandler
from AnalyserResults import AnalyserResults

class EyeAnalyser(QtGui.QMainWindow):
    def __init__(self, engine=None, studio=None):
        super(EyeAnalyser, self).__init__()

        self.engine = engine
        if self.engine == None:
            self.engine = Engine()
            
        self.studio = studio

        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        paths = [os.path.join(os.path.dirname(__file__), '../Resources', f) 
            for f in ['icon.png', 'selected.png']]
        self.whiteIcon = QtGui.QIcon(paths[0])
        self.loadedIcon = QtGui.QIcon(paths[1])
        
        self.filterListPointer = dict()
        self.metricListPointer = dict()
        self.groupboxes = dict()
        self.paramWidgetPointer = dict()
        self.addedAlgorithms = set()
        self.addedMetrics = set()
        self.groupboxes = dict()
        self.metricImports = dict()
        
        self.loadFilterList()
        self.loadMetricList()
        
        self.dataChoicesButtons = [self.ui.radioFolder, self.ui.radioSingle, self.ui.radioCurrent]

        # Connect signals
        self.connect(self.ui.filterList, QtCore.SIGNAL('currentItemChanged(QListWidgetItem*,QListWidgetItem*)'), self.loadFilterItemWithPrevious)
        self.connect(self.ui.filterList, QtCore.SIGNAL('itemChanged(QListWidgetItem*)'), self.loadFilterItem)
        self.connect(self.ui.pushFilterAdd, QtCore.SIGNAL('clicked()'), self.addAlgorithm)
        self.connect(self.ui.pushFilterRemove, QtCore.SIGNAL('clicked()'), self.removeAlgorithm)
        self.connect(self.ui.pushMetricAdd, QtCore.SIGNAL('clicked()'), self.addMetric)
        self.connect(self.ui.pushMetricRemove, QtCore.SIGNAL('clicked()'), self.removeMetric)
        self.connect(self.ui.pushSelectFolder, QtCore.SIGNAL('clicked()'), self.folderDialog)
        self.connect(self.ui.pushSelectSingle, QtCore.SIGNAL('clicked()'), self.singleFileDialog)
        self.connect(self.ui.pushOpenStudio, QtCore.SIGNAL('clicked()'), self.switchToStudio)
        self.connect(self.ui.pushAnalyse, QtCore.SIGNAL('clicked()'), self.analyse)
        for r in self.dataChoicesButtons:
            self.connect(r, QtCore.SIGNAL('toggled(bool)'), lambda x: self.updateDataChoices())

        # If data exists, then choose "current data" as selected option
        
        if studio and self.engine.dataReady():
            self.ui.radioCurrent.setChecked(True)
        else:
            self.ui.radioFolder.setChecked(True) # Default

        self.updateButtons()
        self.updateDataChoices()
        self.updateReturnToStudioButton()
        
        # TODO Temporary defaults
        #self.ui.radioSingle.setChecked(True)
        #self.ui.textSingle.setText("/Users/Gustav/Dropbox/Ollanta+Gustav/tobii/EyeStudio/test2.npz")
        #self.ui.radioCurrent.setChecked(True)
        
        # item = self.filterListPointer['I_VT']
        # self.ui.filterList.setCurrentItem(item)
        # self.loadFilter('I_VT')
        # self.addAlgorithm()
        # 
        # item2 = self.metricListPointer['CompareWithStimulus']
        # self.ui.metricList.setCurrentItem(item2)
        # self.addMetric()        
        
    def updateReturnToStudioButton(self):
        if self.studio:
            self.ui.pushOpenStudio.show()
        else:
            self.ui.pushOpenStudio.hide()
        #self.ui.pushOpenStudio.setEnabled(self.studio != None)
        
    def folderDialog(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, 'Open Directory', '', QtGui.QFileDialog.ShowDirsOnly)
        if path:
            self.ui.textFolder.setText(path)
    
    def singleFileDialog(self):
        path = QtGui.QFileDialog.getOpenFileName(self, 'Open data file', filter="Eye Studio file (*.npz)")
        if path:
            self.ui.textSingle.setText(path)

    def loadFilterList(self):
        path = os.path.join(os.path.dirname(__file__), '../Filters')
        sharedLoadWidgetList(path, self.ui.filterList, self.filterListPointer, self.whiteIcon)

    def loadFilterItemWithPrevious(self, item, prev):
        return self.loadFilterItem(item)

    def loadFilterItem(self, item):
        if item:
            s = item.className
            return self.loadFilter(s)

    def loadFilter(self, name):
        self.engine.setFilterByName(name)
        self.loadGroupbox()

    def loadMetricList(self):
        path = os.path.join(os.path.dirname(__file__), '../Metrics')
        sharedLoadWidgetList(path, self.ui.metricList, self.metricListPointer, self.whiteIcon)

    def loadGroupbox(self):
        return sharedLoadGroupbox(self, self.ui.groupBoxLayout, \
            self.groupboxes, self.engine, self.paramWidgetPointer)

    def addAlgorithm(self):
        '''
        Adds the selected algorithm to the list of analysed ones
        '''
        f = self.ui.filterList.currentItem().className
        try:
            self.addedAlgorithms.add(f)
        except:
            pass
        else:
            self.filterListPointer[f].setIcon(self.loadedIcon)
            self.filterListPointer[f].setText("%s [added]" % f)
            self.updateButtons()

    def removeAlgorithm(self):
        '''
        Unloads the algorithm.
        '''
        f = self.ui.filterList.currentItem().className
        try:
            self.addedAlgorithms.remove(f)
        except:
            pass
        else:
            self.filterListPointer[f].setIcon(self.whiteIcon)
            self.filterListPointer[f].setText("%s" % f)
            self.updateButtons()

    def addMetric(self):
        '''
        Adds the selected metric to the list of used ones
        '''
        f = self.ui.metricList.currentItem().className
        try:
            self.addedMetrics.add(f)
        except:
            pass
        else:
            self.metricListPointer[f].setIcon(self.loadedIcon)
            self.metricListPointer[f].setText("%s [added]" % f)
            self.updateButtons()

    def removeMetric(self):
        '''
        Unloads the metric.
        '''
        f = self.ui.metricList.currentItem().className
        try:
            self.addedMetrics.remove(f)
        except:
            pass
        else:
            self.metricListPointer[f].setIcon(self.whiteIcon)
            self.metricListPointer[f].setText("%s" % f)
            self.updateButtons()

    def dataHasChoice(self):
        c = False
        for r in self.dataChoicesButtons:
            c |= r.isChecked()
        return c

    def updateButtons(self):
        '''Mostly for the Analyse button, if that should show or not'''
        ok = True
        
        # At least one algortihm
        ok &= len(self.addedAlgorithms) > 0
        
        # A choice of data has been made
        ok &= self.dataHasChoice()
        
        # At least one metric
        ok &= len(self.addedMetrics) > 0
        
        self.ui.pushAnalyse.setEnabled(ok)
        
    def updateDataChoices(self):
        b = self.ui.radioFolder.isChecked()
        self.ui.textFolder.setEnabled(b)
        self.ui.pushSelectFolder.setEnabled(b)

        b = self.ui.radioSingle.isChecked()
        self.ui.textSingle.setEnabled(b)
        self.ui.pushSelectSingle.setEnabled(b)
        
        b = self.engine and self.engine.dataReady()
        if b:
            self.ui.radioCurrent.show()
        else:
            self.ui.radioCurrent.hide()
            
        
        self.updateButtons
        
    def getDatapath(self):
        '''Returns the selected data path'''
        if self.ui.radioFolder.isChecked():
            return str(self.ui.textFolder.text())
        elif self.ui.radioSingle.isChecked():
            return str(self.ui.textSingle.text())
        else:
            return None
        
    def analyse(self):
        # Prepare the algorithms and their parameters
        self.resultsDialog = AnalyserResults()
        self.resultsDialog.show()
                
        tempEngine = Engine()
        
        algsDict = {}
        parameter_dictionary = {}
        for algName in self.addedAlgorithms:
            tempEngine.setFilterByName(algName)
            algsDict[algName] = tempEngine.alg
            parameter_dictionary[tempEngine.getFilterName()] = tempEngine.alg.parameters()
        
        # Check settings
        params = sharedGetParameters(self.paramWidgetPointer, parameter_dictionary)
        
        # Set the parameters
        for algName, paramsDict in params.items():
            algsDict[algName].params = paramsDict
        
        algs = algsDict.values()    
        
        # Make sure the metrics are imported
        metrics = self.importMetrics()
        
        # Initialize the analysis
        analyser = Analyser()
        analyser.analyse(self.engine, algs, metrics, self.getDatapath())
        
        for metricName in analyser.getMetricNames():
            self.resultsDialog.createBigDivider(metricName)
            
            for resGroup in analyser.getResultsGroups(metricName):
                self.resultsDialog.createDivider(resGroup.getName())
                self.resultsDialog.addResultsGroup(resGroup)
        
        res = self.resultsDialog.exec_()
        if res:
            del self.resultsDialog
        
    def importMetrics(self):
        '''
        Imports and returns real metric objects from
        the set of strings self.addedMetrics
        '''
        self.metricImports = {} # Reset
        def showTraceback(): # TODO This appears in Engine too, find a better solution
            import traceback
            feedback = traceback.format_exc()
            print>>sys.stderr, "------------------------------------------"
            print>>sys.stderr, feedback

        for name in self.addedMetrics:
            if name not in self.metricImports:
                # Load metric file and see if it loads alright.
                try:
                    self.metricImports[name] = __import__('Metrics.%s' % (name), globals(), locals(), [name], -1)
                except Exception, e:
                    showTraceback()
                    return []

        
        # Now create instances and store in self.metrics
        metrics = []
        for name, package in self.metricImports.items():
            metrics.append(eval("package.%s()" % name))
        return metrics
        
    def switchToStudio(self):
        '''Opens Eye Analyser instead'''
        self.hide()
        if self.studio:
            self.studio.show()


class Main:	
    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon('Resources/icon.png'))

        studio = EyeAnalyser()
        studio.show()
        sys.exit(app.exec_())