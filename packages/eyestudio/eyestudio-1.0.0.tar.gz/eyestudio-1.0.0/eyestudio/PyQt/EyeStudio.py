
# Frameworks
import sys, os
from os.path import dirname, join
from PyQt4 import QtCore, QtGui

# Project
from EyeStudioUI import Ui_mainWindow
from ImportAnalysedUI import Ui_ImportAnalysedDialog
from .Engine.Engine import Engine
from EngineCanvas import EngineCanvas
from LabellingCanvas import LabellingCanvas
from ErrorConsole import ErrorConsole
from ParameterHandler import GetParameterHandler
from .Engine.Filter import Filter, STATE_NAMES
from SharedFunctions import sharedLoadWidgetList, sharedLoadGroupbox
from EyeAnalyser import EyeAnalyser

paramdict = {}

class EyeStudio(QtGui.QMainWindow):
    ANALYSIS = 0
    LABELLING = 1
    
    def __init__(self, engine=None, analyser=None):
        super(EyeStudio, self).__init__()

        if engine == None:
            self.engine = Engine()
        else:
            self.engine = engine

        self.analyser = analyser

        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        
        # Create the engine canvas
        self.ui.canvas = EngineCanvas(self, self.engine)
        self.ui.canvasLayout.addWidget(self.ui.canvas)
        # Create the labelling canvas
        self.ui.labellingCanvas = LabellingCanvas(self, self.engine)
        self.ui.labellingCanvasLayout.addWidget(self.ui.labellingCanvas)

        self.paramWidgetPointer = {}
        self.filterListPointer = {}

        # Direct stdout/stderr to the GUI
        sys.stdout = ErrorConsole(self.ui.errorConsole, sys.stdout)
        sys.stderr = ErrorConsole(self.ui.errorConsole, sys.stderr, QtGui.QColor(100,0,0))


        # TODO Find a permament solution for the not-loaded icon
        #pixmap = QtGui.QPixmap(32,32)
        #pixmap.fill()
        
        path = os.path.join(os.path.dirname(__file__), '../Resources', 'icon.png')
        
        self.whiteIcon = QtGui.QIcon(path)
        #self.whiteIcon = QtGui.QIcon(pixmap)

        # Icons
        self.icons = dict([
            (name, QtGui.QIcon(join(dirname(__file__), "../Resources/%s.png" % name)))
                for name in ['play', 'pause']])

        # Connect signals
        self.connect(self.ui.playButton, QtCore.SIGNAL('clicked()'), self.playPause)
        self.connect(self.ui.filterList, QtCore.SIGNAL('currentItemChanged(QListWidgetItem*,QListWidgetItem*)'), self.loadFilterItemWithPrevious)
        self.connect(self.ui.loadButton, QtCore.SIGNAL('clicked()'), self.loadAlgorithm)
        self.connect(self.ui.unloadButton, QtCore.SIGNAL('clicked()'), self.unloadAlgorithm)
        self.connect(self.ui.timeBar, QtCore.SIGNAL('valueChanged(int)'), self.timeBarMoved)
        self.connect(self.ui.importAnalysedDialog, QtCore.SIGNAL('clicked()'), self.importAnalysed)
        self.connect(self.ui.tabMenu, QtCore.SIGNAL('currentChanged(int)'), self.tabMenuChanged)  
        self.connect(self.ui.checkBoxZoom, QtCore.SIGNAL('stateChanged(int)'), self.checkBoxZoomChanged)  
        self.connect(self.ui.setSelection, QtCore.SIGNAL('clicked()'), self.setCurSelection)
        self.connect(self.ui.pushOpenAnalyser, QtCore.SIGNAL('clicked()'), self.switchToAnalyser)

        # Menu signals
        self.connect(self.ui.action_open, QtCore.SIGNAL('triggered()'), self.loadDataDialog)
        self.connect(self.ui.action_save, QtCore.SIGNAL('triggered()'), self.saveDataDialog)
        self.connect(self.ui.action_saveAs, QtCore.SIGNAL('triggered()'), self.saveAsDataDialog)
        self.connect(self.ui.action_importTSV, QtCore.SIGNAL('triggered()'), self.importDataDialog)
        self.connect(self.ui.action_importStimulus, QtCore.SIGNAL('triggered()'), self.importStimulusDialog)
        self.connect(self.ui.action_showHideErrorConsole, QtCore.SIGNAL('triggered()'), self.showHideErrorConsole)
        self.connect(self.ui.action_showHideOrdinals, QtCore.SIGNAL('triggered()'), self.showHideOrdinals)
        self.connect(self.ui.action_showHideTimeline, QtCore.SIGNAL('triggered()'), self.showHideLabellingCanvas)
        self.connect(self.ui.action_step1minus, QtCore.SIGNAL('triggered()'), lambda: self.step(-1))
        self.connect(self.ui.action_step1plus, QtCore.SIGNAL('triggered()'), lambda: self.step(1))
        self.connect(self.ui.action_step5minus, QtCore.SIGNAL('triggered()'), lambda: self.step(-5))
        self.connect(self.ui.action_step5plus, QtCore.SIGNAL('triggered()'), lambda: self.step(5))
        self.connect(self.ui.action_startSelection, QtCore.SIGNAL('triggered()'), self.startSelection)
        self.connect(self.ui.action_deselect, QtCore.SIGNAL('triggered()'), self.deselect)

        # Colour queue (this is the colours the algorithms get)
        self.algColours = [
            (255, 255, 0),
            (255, 0, 255),
            (100, 100, 255),
            (50, 255, 50),
            (255, 0, 0),
        ]
        self.loadedFiltersColours = {}
        
        # Label colours
        # self.labelColours = {
        #     Filter.FIXATION: (0, 0, 0),
        #     Filter.SACCADE: (128, 0, 0),
        #     Filter.SMOOTH_PURSUIT: (255, 0, 0),
        #     3: (255, 128, 0),
        #     4: (255, 255, 0),
        #     5: (125, 255, 0),
        #     6: (0, 255, 0),
        #     7: (0, 255, 128),
        # }


        self.labelColours = {
            Filter.FIXATION: (200, 200, 255),
            Filter.SACCADE: (255, 255, 140),
            Filter.SMOOTH_PURSUIT: (200, 255, 200),
            3: ()
        }

        self.loadFilterList()
        self.loadLabelList()
        
        # Time related
        self.timer = QtCore.QBasicTimer()
        self.isPaused = True
        self.tick = 0 # Just an auxilary variable
        self.frameRate = 30 # Hz
        self.showOrdinals = False
        self.zoomIn = False
        
        # If mode == LABELLING, it will be shown regardless
        self.showLabellingCanvas = False 
        
        self.loadedFilename = None # If this is set, then Save will not open a dialog
        
        # Set up Engine
        if len(sys.argv) >= 2:
            self.loadFileNPZ(sys.argv[1])
        
        self.groupboxes = {}
        
        # After data has loaded, we need to update some things
        self.updateTimeIndicator()
        self.updatePlayButton()

        # Hide 
        self.ui.errorConsoleFrame.hide()
        self.tabMenuChanged(0)
        self.selectingFrom = None

    def loadFileNPZ(self, filename):
        self.loadedFilename = filename
        self.engine.loadDataNPZ(self.loadedFilename)

        # TODO How to handle this?
        #self.setWindowTitle(QtGui.QApplication.translate("MainWindow - %s" % filename, "MainWindow - %s" % filename, None, QtGui.QApplication.UnicodeUTF8))

        #self.setObjectName(filename)        
        self.ui.canvas.update()
        self.ui.labellingCanvas.update()

    def startSelection(self):
        self.selectingFrom = self.engine.loop_count
        self.ui.labellingCanvas.update()

    def deselect(self):
        self.selectingFrom = None
        self.ui.labellingCanvas.update()

    def step(self, offset):
        '''Moves the current pointer this many steps'''
        
        self.engine.step(offset)
        self.ui.canvas.update()
        self.ui.labellingCanvas.update()
        self.updateTimeIndicator()

    def getMode(self):
        return self.mode

    def importAnalysed(self):
        ImportAnalysedDialog = QtGui.QDialog()
        ImportAnalysedDialog.setWindowTitle('Import Analysed Data') # TODO Doesn't work
        ui = Ui_ImportAnalysedDialog()
        ui.setupUi(ImportAnalysedDialog)
        for item in self.engine.results:
            ui.filterList.addItem(item)
        
        ImportAnalysedDialog.show()
        res = ImportAnalysedDialog.exec_()
        
        if res:
            selection = str(ui.filterList.currentItem().text())
            self.engine.setLabelsFromResults(selection)

    def showHideLabellingCanvas(self):
        self.showLabellingCanvas = not self.showLabellingCanvas
        if self.showLabellingCanvas:
            self.ui.labellingCanvasFrame.show()
            self.ui.labellingCanvasFrame.update()
        else:
            self.ui.labellingCanvasFrame.hide()

    def isLabellingCanvasShowing(self):
        if self.showLabellingCanvas:
            return True
        else:
            if self.mode == self.LABELLING:
                return True
            else:
                return False
                
    def tabMenuChanged(self, choice):
        if choice == 0:
            self.mode = self.ANALYSIS
        elif choice == 1:
            self.mode = self.LABELLING

        self.ui.canvas.update()

        if self.isLabellingCanvasShowing():
            self.ui.labellingCanvasFrame.show()
            self.ui.labellingCanvas.update()
        else:
            self.ui.labellingCanvasFrame.hide()
        
    def updateAll(self):
        self.updateTimeIndicator()
        self.updatePlayButton()
        self.ui.canvas.update()    
        self.ui.labellingCanvas.update()

    def start(self):
        if not self.isPaused:
            return
        self.isPaused = False
        self.timer.start(1000.0/self.frameRate, self)
        self.updatePlayButton()

    def pause(self):
        if self.isPaused:
            return
        self.isPaused = True
        self.timer.stop()
        self.updatePlayButton()

    def timerEvent(self, event):
        '''
        This is called by the timer after n:th ms (depending on setup)
        '''
        if event.timerId() == self.timer.timerId():
            self.doLoop()
            self.update()
        else:
            QtGui.QFrame.timerEvent(self, event)

    def doLoop(self):
        #if not self.engine.stepThrough():
        if not self.engine.playback(1000.0/self.frameRate):
            self.pause()
        # Don't update this too often or it might get slow
        self.tick += 1
        if self.tick > 5:
            self.updateTimeIndicator()
            self.tick = 0

    def playPause(self):
        if self.isPaused: 
            self.start()
        else:
            self.pause()
        self.updatePlayButton()

    def updatePlayButton(self):
        # Move to init
        self.ui.playButton.setIconSize(QtCore.QSize(40, 40))

        self.ui.playButton.setEnabled(bool(self.engine.dataReady()))
        self.ui.loadButton.setEnabled(bool(self.engine.dataReady() and self.engine.filterReady()))
        self.ui.unloadButton.setEnabled(bool(self.engine.dataReady() and self.engine.resultsReady()))

        icon = ['pause', 'play'][int(self.isPaused)]
        self.ui.playButton.setIcon(self.icons[icon])

    def updateTimeIndicator(self):
        '''
        Updates the time indicators (bar, text, etc. could be changed) with the current
        elapsed time.
        '''
        if self.engine.dataReady():
            self.ui.timeBar.setRange(0, self.engine.dataSize()-1)
            self.ui.timeBar.setValue(self.engine.loop_count)
            #progress = float(self.engine.loop_count) / float(self.engine.dataCount())
        self.updateTimeLabel()

    def updateTimeLabel(self):
        '''
        Set the time label to indicate the current time
        '''
        if self.engine.dataReady():
            now = self.engine.data[self.engine.loop_count,0]
        else:
            now = 0

        # Format the time
        milli = now%1000
        now = (now-milli)//1000
        seconds = now%60
        now = (now-seconds)//60
        minutes = now%60
        now = (now-minutes)//60
        hours = now

        self.ui.timeLabel.setText("%02d:%02d:%02d (%03d ms)" % (hours, minutes, seconds, milli))


    def timeBarMoved(self, pos):
        '''
        Time bar was moved by the user
        '''
        self.engine.setLoopCount(pos)
        self.ui.canvas.update() #<- TODO something to redraw the canvas even when it's stopped
        self.ui.labellingCanvas.update()
        self.updateTimeLabel()

    def loadGroupbox(self):
        return sharedLoadGroupbox(self, self.ui.groupBoxLayout, \
            self.groupboxes, self.engine, self.paramWidgetPointer)

    def loadFilterList(self):
        path = os.path.join(os.path.dirname(__file__), '../Filters')
        sharedLoadWidgetList(path, self.ui.filterList, self.filterListPointer, self.whiteIcon)
            
    def loadLabelList(self):
        '''
        Populate the labels list under "Labelling"
        '''
        self.ui.labelList.clear()
        self.labelListPointer = {}
        
        labels = STATE_NAMES
        for label, labelname in enumerate(labels):
            try:
                icon = self.getColourIcon(self.labelColours[label])
            except:
                icon = self.whiteIcon
            self.labelListPointer[label] = label
            self.ui.labelList.addItem(icon, labelname)
            
    def loadFilterItemWithPrevious(self, item, prev):
        ''' 
        The signal accepts a function that also takes the previous
        selection, we'll simply ignore this parameter.
        '''
        return self.loadFilterItem(item)
        
    def loadFilterItem(self, item):
        if item:
            s = item.className
            return self.loadFilter(s)

    def loadFilter(self, name):
        self.engine.setFilterByName(name)
        self.loadGroupbox()
        self.updatePlayButton()
        self.ui.canvas.update()
        self.ui.labellingCanvas.update()

    def loadAlgorithm(self):
        '''
        Runs the current algorithm with the current data and parameters
        '''
        
        # We cannot load more than we have colours for
        if len(self.algColours) > 0:            
            self.updateParameters() # from widgets

            self.engine.process()
            # Update button
            self.updatePlayButton()
            self.ui.canvas.update()
            self.ui.labellingCanvas.update()
            f = self.engine.getFilterName()

            # Pick colour
            if f not in self.loadedFiltersColours:
                self.loadedFiltersColours[f] = c = self.algColours.pop()
                # Create an icon with the same colour as the algorithm is given
                self.filterListPointer[f].setIcon(self.getColourIcon(c))
        
            self.filterListPointer[f].setText("%s [loaded]" % f)
            
    def getColourIcon(self, coltuple):
        ''' 
        This generates an icon representing the given colour 
        '''
        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtGui.QColor(*coltuple))
        return QtGui.QIcon(pixmap)

    def unloadAlgorithm(self):
        '''
        Unloads the algorithm.
        '''
        self.engine.removeResults()
        self.ui.canvas.update()
        self.ui.labellingCanvas.update()        
        f = self.engine.getFilterName()
        
        self.algColours.append(self.loadedFiltersColours[f])
        del self.loadedFiltersColours[f]

        self.filterListPointer[f].setIcon(self.whiteIcon)
        self.filterListPointer[f].setText("%s" % f)


    def updateParameters(self):
        '''
        This reads off the parameters from the widgets
        and stores it in the Filter object
        '''
        # Iterate parameters and then find widgets (could be done
        # in the opposite direction, but then we would have to do a similar
        # linear search through the parameters to figure what type it is)
        groupbox = self.groupboxes[self.engine.getFilterName()]
        for p in self.engine.alg.parameters():
            try:
                widget = self.paramWidgetPointer[self.engine.getFilterName(), p.name]
                handler = GetParameterHandler(p)
            except:
                print>>sys.stderr, "Could not find widget or unsupported type for %s" % p.name
                continue

            self.engine.alg.params[p.name] = handler.getValue(widget)

        # Temporary output
        print "Using the following parameters:"
        for name, value in self.engine.alg.params.items():
            print " - %s = %s" % (name, str(value))

    def setCurSelection(self):
        '''Sets the current selection to the label chosen in labelList'''
        
        print "currenIndex", self.ui.labelList.currentIndex()
        print self.labelListPointer
        
        label = self.labelListPointer[self.ui.labelList.currentIndex()]
        self.engine.setLabelRange(self.selectingFrom, None, label)
            
        # Finally, deselect
        self.selectingFrom = None
            
        self.ui.canvas.update()
        self.ui.labellingCanvas.update()

    def showHideErrorConsole(self):
        if self.ui.errorConsoleFrame.isHidden():
            self.ui.errorConsoleFrame.show()
        else:
            self.ui.errorConsoleFrame.hide()

    def showHideOrdinals(self):
        self.showOrdinals = not self.showOrdinals
        self.ui.labellingCanvas.update()

    def loadDataDialog(self):
        self.pause() # Is this needed?
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open data file', filter="Eye Studio file (*.npz)")
        if filename:
            self.loadedFilename = filename
            self.engine.loadDataNPZ(filename)
            self.updateAll()

    def saveDataDialog(self):
        if not self.loadedFilename:
            return self.saveAsDataDialog()
        else:
            self.engine.saveDataNPZ(self.loadedFilename)
            self.updateAll()
    
    def saveAsDataDialog(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, 'Save data file')        
        # This could be false from pressing cancel
        # If it is, we don't want to change self.loadedFilename
        if fn:
            self.loadedFilename = fn
            return self.saveDataDialog()

    def importDataDialog(self):
        self.pause() # Is this needed?
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Import data file', filter="TSV file (*.tsv)")
        if filename:
            self.engine.loadDataTSV(filename)
            self.updateAll()

    def importStimulusDialog(self):
        self.pause() # Is this needed?
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Import stimulus file', filter="Stimulus file (*.stim.txt)")
        if filename:
            self.engine.loadStimulusFromFile(filename)
            self.updateAll()
            
    def checkBoxZoomChanged(self, checked):
        self.zoomIn = checked
        self.ui.labellingCanvas.update()
            
    def switchToAnalyser(self):
        '''Opens Eye Analyser instead'''
        self.hide()
        if not self.analyser:
            self.analyser = EyeAnalyser(self.engine, studio=self)
            
        self.analyser.show()

class Main:	
    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        path = join(dirname(__file__), '../Resources/icon.png')
        app.setWindowIcon(QtGui.QIcon(path))

        studio = EyeStudio()
        studio.show()
        r = app.exec_()
        sys.exit(r)