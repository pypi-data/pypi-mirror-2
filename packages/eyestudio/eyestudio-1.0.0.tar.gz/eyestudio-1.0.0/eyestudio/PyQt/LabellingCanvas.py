
# Frameworks
from PyQt4 import QtCore, QtGui
import copy

# Project
from .Engine.Engine import Engine
from .Engine.Filter import Filter

class LabellingCanvas(QtGui.QFrame):
    '''
    Labelling canvas will show a time-line and different information along it,
    namely labels and data information such as velocity (so that it's easier to
    see exactly where a fixation ends).
    '''
    def __init__(self, parent, engine):
        super(LabellingCanvas, self).__init__(parent)
        self.parent = parent
        self.engine = engine
        self.setStyleSheet("QWidget { background-color: #FFF; border: 1px solid #AAA }")
        self.axisColours = [(0,0,200), (0, 200, 0)]

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        zoom = False

        if self.engine.dataReady():
            if self.parent.zoomIn:
                magnitude = 10.0
                def getPixelpos(index, dim, rectClip):
                    point = self.engine.getGazePos(index)
                    center_point = self.engine.getGazePos(curpos)
                    t = (index-(curpos-halfwindow))*float(rectClip.width())/(halfwindow*2.0)
                    x = rectClip.height()*(0.5 - float(point[dim]-center_point[dim])*magnitude/self.engine.getScreenSize()[dim])
                    pixelpos = (t, x)
                    pixelpos = map(int, pixelpos)
                    return pixelpos
            else:
                def getPixelpos(index, dim, rectClip):
                    point = self.engine.getGazePos(index)
                    
                    t = (index-(curpos-halfwindow))*float(rectClip.width())/(halfwindow*2.0)
                    x = rectClip.height()*(1.0-float(point[dim])/(self.engine.getScreenSize()[dim]))
                    pixelpos = (t, x)
                    pixelpos = map(int, pixelpos)
                    return pixelpos
                
            rect = self.contentsRect()
                        
            # How many points should be drawn before and after the current?
            curpos = self.engine.loop_count
            halfwindow = 30
            
            middle = getPixelpos(curpos, 0, rect)

            # The points in the range
            it = xrange(max(0, curpos-halfwindow), min(self.engine.dataSize(), curpos+halfwindow+1))


            #
            #   Draw labels or states
            #
            height = 12
            bottomspace = 0
            if self.parent.mode == self.parent.LABELLING:
                clipRect = copy.copy(rect)
                clipRect.setTop(rect.bottom()-height+2)
                states = [(i, self.engine.getLabel(i-1)) for i in it]
                self.drawLabels(painter, clipRect, halfwindow, states)
                bottomspace += height
            elif self.parent.mode == self.parent.ANALYSIS:
                for i, name in enumerate(self.engine.getNamesOfFiltersWithResults()):
                    clipRect = copy.copy(rect)
                    clipRect.setTop(rect.bottom()-height*(i+1)+2)
                    clipRect.setBottom(rect.bottom()-height*(i))
                    states = [(i, self.engine.getState(i-1, name)) for i in it]
                    self.drawLabels(painter, clipRect, halfwindow, states)
                    
                    col = QtGui.QColor(*self.parent.loadedFiltersColours[name])
                    brush = QtGui.QBrush(col)
                    painter.fillRect(QtCore.QRect(2, clipRect.top()+2, height-4, height-4), brush)

                    bottomspace += height
                    
            # 
            #   Draw X and Y axis
            #
            
            clipTop = copy.copy(rect)
            clipTop.setBottom(rect.bottom()-bottomspace)
            # Set clipping to the top
            painter.setClipRect(clipTop)
                        
            for dim in xrange(2):
                col = QtGui.QColor(*(self.axisColours[dim]))
                painter.setPen(QtGui.QPen(col, 2, QtCore.Qt.SolidLine))
                lastpos = None
                for i in it:
                    pos = getPixelpos(i, dim, clipTop)
                    if lastpos != None:                
                        painter.drawLine(*(lastpos+pos))
                    lastpos = pos

            #
            #   Draw selection
            #   
            painter.setClipRect(rect)
            if self.parent.selectingFrom != None:
                # Mark the selection
                pos_from = getPixelpos(self.parent.selectingFrom, 0, rect)
                pos_to = getPixelpos(curpos, 0, rect)
                
                col = QtGui.QColor(0, 0, 0, 35)
                brush = QtGui.QBrush(col)
                painter.fillRect(QtCore.QRect(pos_from[0], rect.top(), pos_to[0]-pos_from[0], rect.height()+1), brush)
            
            #
            #   Draw a vertical line to indicate the current point
            #
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 1, QtCore.Qt.SolidLine))
            painter.drawLine(middle[0], rect.top(), middle[0], rect.bottom()+1)

    def drawLabels(self, painter, rect, halfwindow, states):
        '''
        Draw labels
        '''
        curpos = self.engine.loop_count
        
        def getPixelpos(index):
            t = (index-(curpos-halfwindow))*float(rect.width())/(halfwindow*2.0)
            return t
        last_ordinal = -1
        
        # Set clipping to the bottom
        if self.engine.hasLabelling():
            last_t = None
            for i, (label, ordinal) in states:
                
                t = getPixelpos(i)
                if last_t != None:
                    coltuple = None
                    try:
                        coltuple = self.parent.labelColours[label]
                    except KeyError:
                        pass

                    if coltuple != None:
                        painter.setClipRect(rect)
                        col = QtGui.QColor(*coltuple)
                        brush = QtGui.QBrush(col)
                        painter.fillRect(QtCore.QRect(last_t, rect.top(), t-last_t+1, rect.height()), brush)
                        
                    # Output the ordinal
                    # if self.parent.showOrdinals:
                    #     if ordinal != last_ordinal:
                    #         #print last_t[0]+5, clipBottom.top()
                    #         painter.setClipRect(rect)                        
                    #         painter.setPen(QtGui.QPen(QtGui.QColor(0x000), 1, QtCore.Qt.SolidLine))
                    #         painter.setFont(QtGui.QFont("Arial", 9))
                    #         painter.drawText(last_t+2, clipBottom.top()-2, str(ordinal))
                    #         last_ordinal = ordinal
                last_t = t
                
                    
                    