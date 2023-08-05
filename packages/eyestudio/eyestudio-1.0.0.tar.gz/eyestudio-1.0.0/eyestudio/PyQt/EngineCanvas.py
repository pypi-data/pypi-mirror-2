
# Frameworks
from PyQt4 import QtCore, QtGui
from math import cos, sin

# Project
from .Engine.Engine import Engine
from .Engine.Stimulus import Stimulus

class EngineCanvas(QtGui.QFrame):
    def __init__(self, parent, engine):
        super(EngineCanvas, self).__init__(parent)
        self.parent = parent
        self.engine = engine
        self.setStyleSheet("QWidget { background-color: #001000; border: 1px solid #304030 }")
        self.ratio = 1.0
        self.showStimulus = True
    
    def getRatio(self):
        width, height = self.engine.getResolution()
        return float(height)/width
        
    def canvasRect(self):
        rect = self.contentsRect()
        buf = 10
        rect.setLeft(rect.left()+buf)
        rect.setRight(rect.right()-buf)
        rect.setTop(rect.top()+buf)
        rect.setBottom(rect.bottom()-buf)
        
        ratio = self.getRatio()
        
        y = int(rect.width() * ratio)
        if y <= rect.height():
            rect2 = QtCore.QRect(rect.left(), rect.center().y()-y/2, rect.width(), y)
        else:
            x = int(rect.height()/ratio)
            rect2 = QtCore.QRect(rect.center().x()-x/2, rect.top(), x, rect.height())
        
        return rect2
    
    def getPixelpos(self, rawpos, rect=None):
        '''
        Translate a gaze position to the appropriate pixel position for the
        current canvas.
        '''
        if not rect:
            rect = self.canvasRect()
        
        # Render the "engine" object
        pos = ( rect.left() + rawpos[0]/self.engine.screenSize[0]*rect.width(),
                rect.top() + rawpos[1]/self.engine.screenSize[1]*rect.height())

        pixelpos = map(int, pos)
        return pixelpos
        
    def getPixelposFromStimulus(self, rawpos, rect=None):
        '''
        The stimulus uses another way of representing position with origin in the middle
        of the screen and units in degrees.
        '''
        if not rect:
            rect = self.canvasRect()
        
        pos = ( rect.left() + rect.width() * rawpos[0] / self.engine.screenSize[0],
                rect.top() + rect.height() * rawpos[1] / self.engine.screenSize[1])
        
        return pos
        
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        qtcol = QtGui.QColor(0x000000)
        painter.setBrush(QtGui.QBrush(qtcol))
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        
        rect = self.canvasRect()
        if not self.engine.dataReady():
            painter.setFont(QtGui.QFont("Arial", 15))
        
            options = QtGui.QTextOption(QtCore.Qt.AlignCenter)
            painter.setPen(QtGui.QPen(QtGui.QColor(0xF0F0F0), 1, QtCore.Qt.SolidLine))
            painter.drawText(QtCore.QRectF(rect), "No data loaded", options)
        else:
            if self.showStimulus:
                self.drawStimulus(painter, rect)
            
            # Draw screen marker
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(QtGui.QPen(QtGui.QColor(0x5BAF94), 1, QtCore.Qt.DashLine))
            painter.drawRect(rect)

            
            if self.parent.getMode() == self.parent.ANALYSIS:
                # Loop them
                for filter_i, filterName in enumerate(self.engine.getNamesOfFiltersWithResults()):
                    if self.engine.resultsReady(filterName):
                        coltuple = self.parent.loadedFiltersColours[filterName]

                        frames = self.engine.getFrames(filterName)
                        self.drawLabels(painter, rect, frames, coltuple, disambig_id=filter_i)
            
            # For labelled data
            elif self.parent.getMode() == self.parent.LABELLING:
                coltuple = (100, 255, 255)
                if self.engine.hasLabelFrames():
                    self.drawLabels(painter, rect, self.engine.getLabelFrames(), coltuple)
                
                

            painter.setPen(QtGui.QPen(QtGui.QColor(0xF0F0F0), 2, QtCore.Qt.SolidLine))
            # Draw current gaze position marker
            pixelpos = self.getPixelpos(self.engine.getGazePos(), rect)
            r = 4
            painter.drawEllipse(pixelpos[0]-r, pixelpos[1]-r, r*2, r*2)
                
    def drawLabels(self, painter, rect, frames, coltuple, disambig_id=0):
        window = 50 # TODO Change to time
        now = self.engine.data[self.engine.loop_count,0] # TODO make nicer access, maybe function

        # Paint the results for this filter
        lastpos = None
        for i in xrange(self.engine.loop_count, max(-1,self.engine.loop_count-window), -1):
            # Draw fixation!
            fixation = self.engine.getFixationElapsed(i, frames)
            if fixation != None:
                pos = tuple(fixation[:2])
                if pos != lastpos:
                    #elapsed = fixation[2]
                    alpha = max(0, 255 - (now - self.engine.data[i,0])/3.0)

                    if now == self.engine.data[i,0]: # TODO Do nicer
                        col = QtGui.QColor(coltuple[0], coltuple[1], coltuple[2])
                        width = 2
                    else:
                        col = QtGui.QColor(coltuple[0]//2, coltuple[1]//2, coltuple[2]//2, alpha)
                        width = 1

                    painter.setPen(QtGui.QPen(col, width, QtCore.Qt.SolidLine))
                    fixationpos = self.getPixelpos(pos, rect)
                    painter.drawEllipse(fixationpos[0]-10, fixationpos[1]-10, 20, 20)
                
                    # Draw a line going out from the ellipse, this is so that two different
                    # circles from two different algorithms can be differentiated.
                    # The angle of the line is related to i
                    co, si = cos(disambig_id*0.4), sin(disambig_id*0.4)
                    for wi in [(-11, -20), (11, 20)]:
                        painter.drawLine(
                            fixationpos[0] + int(co*wi[0]), 
                            fixationpos[1] + int(si*wi[0]),
                            fixationpos[0] + int(co*wi[1]), 
                            fixationpos[1] + int(si*wi[1]),
                        )

                lastpos = pos
                
    def drawStimulus(self, painter, rect):
        """Draw stimulus"""
        # Draw stimulus
        showStimulus = True
        
        if showStimulus and self.engine.hasStimulus():
            # now = self.engine.getTime()
            pos = self.engine.getStimulus().getPosition(self.engine.loop_count)
            if pos != None:
                pixelpos = self.getPixelposFromStimulus(pos, rect)
                r = 10 # TODO Change to degrees of the angle
                qtcol = QtGui.QColor(0x777777)
                painter.setPen(QtGui.QPen(qtcol, 2, QtCore.Qt.SolidLine))
                painter.setBrush(QtGui.QBrush(qtcol))
                painter.drawEllipse(pixelpos[0]-r, pixelpos[1]-r, r*2, r*2)
        
        