
# Framework
from PyQt4 import QtGui

# Project
from .Engine.Filter import Parameter

# One can import both the dictionary and the function, the function is preferred though
#  but the dictionary can be extended externally.
PARAMETER_HANDLERS = {}
def GetParameterHandler(param):
    ''' param is a Parameter object '''
    return PARAMETER_HANDLERS[param.vartype](param) # Possibly make static

# Base classes
class ParameterHandler(object):
    '''
    Base class for handling a parameter through the widget interface.
    This should be derived to for instance ParameterInt to handle integers.
    '''
    def __init__(self, param):
        ''' 
        param is Parameter object 
        '''
        self.param = param
    
    def getParam(self):
        ''' Returns the Parameter object '''
        return self.param
    
    def getValue(self, widget):
        '''
        This takes a widget (whatever is corresponding to the type) and
        extracts the value and returns it with the right type.
        '''
        return None
        
    def setValue(self, widget, value):
        ''' Sets the value to the widget'''
        pass

    def createWidget(self):
        ''' Creates and returns a new widget '''
        return None

class RegisterParameterHandler(object):
    ''' Registers a handler for the type 'vartype' '''
    def __init__(self, vartype):
        self.vartype = vartype
        
    def __call__(self, handler):
        PARAMETER_HANDLERS[self.vartype] = handler
        return handler

# Supported Parameters
@RegisterParameterHandler(int)    
class __handler_int(ParameterHandler):
    def getValue(self, widget):
        return int(widget.text())
        
    def setValue(self, widget, value):
        widget.setText(repr(value))
    
    def createWidget(self, parent):
        return QtGui.QLineEdit(parent)

@RegisterParameterHandler(float)    
class __handler_float(ParameterHandler):
    def getValue(self, widget):
        return float(widget.text())
        
    def setValue(self, widget, value):
        widget.setText(repr(value))
    
    def createWidget(self, parent):
        return QtGui.QLineEdit(parent)
       
@RegisterParameterHandler(str)    
class __handler_string(ParameterHandler):
    def getValue(self, widget):
        return float(widget.text())
        
    def setValue(self, widget, value):
        widget.setText(value)
    
    def createWidget(self, parent):
        return QtGui.QLineEdit(parent)

      
@RegisterParameterHandler(dict)    
class __handler_dict(ParameterHandler):
    ''' For multiple choice, the key is the value it will return '''
    def __init__(self, param):
        ParameterHandler.__init__(self, param)
        self.index2value = []
    
    def getValue(self, widget):
        for i, v in enumerate(self.getParam().varinfo):
            if i == widget.currentIndex():
                return v
                
    def setValue(self, widget, value):
        for i, v in enumerate(self.getParam().varinfo):
            if v == value:
                widget.setCurrentIndex(i)
    
    def createWidget(self, parent):
        widget = QtGui.QComboBox(parent)
        for value, text in self.getParam().varinfo.items():
            widget.addItem(text)
        return widget
       
@RegisterParameterHandler(bool)       
class __handler_bool(ParameterHandler):
    def getValue(self, widget):
        return widget.isChecked()
        
    def setValue(self, widget, value):
        widget.setChecked(value)
        
    def createWidget(self, parent):
        return QtGui.QCheckBox(parent)
