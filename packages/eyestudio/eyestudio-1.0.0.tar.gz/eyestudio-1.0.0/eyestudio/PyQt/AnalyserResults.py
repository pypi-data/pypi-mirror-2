
# Frameworks
import sys, os
from PyQt4 import QtCore, QtGui

# Project
from AnalyserResultsUI import Ui_AnalyserResults
from .Engine.Engine import Engine
from .Engine.Metric import GetMetricRenderer

class AnalyserResults(QtGui.QDialog):
    def __init__(self):
        super(AnalyserResults, self).__init__()
        
        self.ui = Ui_AnalyserResults()
        self.ui.setupUi(self)
        
        self.metricResults = []
        
        QtCore.QObject.connect(self.ui.pushClose, QtCore.SIGNAL("clicked()"), self.accept)
        QtCore.QObject.connect(self.ui.pushExport, QtCore.SIGNAL("clicked()"), self.export)
        
    def addResultsGroup(self, metricResultsGroup):
        '''Adds a MetricResultsGroup object'''
        self.createWidget(metricResultsGroup)

        self.metricResults.append(metricResultsGroup)
        
    def createDivider(self, name):
        widget = QtGui.QLabel(name, self)
        self.ui.resultsLayout.addWidget(widget)
        
        self.metricResults.append(":: {0} ::".format(name))
        
    def createBigDivider(self, name):
        widget = QtGui.QLabel(name, self)
        widget.setStyleSheet("background: #FFA;\n"
        "border: 1px solid #DD7;\n"
        "padding: 5px;")
        self.ui.resultsLayout.addWidget(widget)
        
        self.metricResults.append("{1}\n{0}\n{1}".format(name, "#"*80))
        
    def export(self):
        '''
        Exports the data. This is a very crude export function and will require
        the user to extract the data from a fairly messy file. If needed, update!
        '''
        fn = QtGui.QFileDialog.getSaveFileName(self, 'Export data file')        
        if fn:
            f = open(fn, 'w')
            #print "-- start ------------------------------"
            #f = sys.stdout
            for metricRes in self.metricResults:
                if isinstance(metricRes, str):
                    f.write(metricRes + "\n")
                else:
                    # f.write(str(metricRes.metricType) + "\n")
                    for metRes in metricRes.metricResultsList:
                        bar = "+" + "-"*50 + "+"
                        
                        f.write(bar + "\n")
                        f.write("|Metric type: {0}".format(metRes.metrictype).ljust(len(bar)-1)+"|\n")
                        f.write("|Name: {0}".format(metRes.name).ljust(len(bar)-1)+"|\n")
                        f.write("|Algorithm: {0}".format(metRes.algName).ljust(len(bar)-1)+"|\n")
                        f.write(bar + "\n")
                        
                        if isinstance(metRes.data, list):
                            f.write("\n".join(metRes.data))
                        elif isinstance(metRes.data, dict):
                            for key, value in metRes.data.items():
                                f.write("** %s **\n" % key)
                                if isinstance(value, list):
                                    f.write("\n".join([str(s) for s in value]) + "\n")
                                else:
                                    f.write(str(value) + "\n")
                        else:
                            f.write(str(metRes.data) + "\n")
                
            f.close()
            #print "-- closed -----------------------------"
            #return self.saveDataDialog()
        

    def createWidget(self, metricResultsGroup):
        renderer = GetMetricRenderer(metricResultsGroup)
        widget = renderer.createWidget(self)
        self.ui.resultsLayout.addWidget(widget)
        
#        for results in results_objects:
#            renderer = GetMetricRenderer(results)
#            widget = renderer.createWidget(self)
#            self.ui.resultsLayout.addWidget(widget)
            
            
            