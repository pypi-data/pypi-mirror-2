
# This file contains functions that are used by both EyeStudio and EyeAnalyser


# Frameworks
import sys, os
from PyQt4 import QtCore, QtGui

# Project
from ParameterHandler import GetParameterHandler

def sharedLoadWidgetList(path, listWidget, listPointer, defaultIcon):
    '''
    Populate the widget list from python files in a path
    '''
    listWidget.clear()
    listPointer.clear()

    filters = []
    excludeList = ['__init__']
    filterDir=os.listdir(path)
    for filename in filterDir:
        name, ext = os.path.splitext(filename)
        if ext.lower() == '.py' and name not in excludeList:
            filters.append(name)

    for filt in filters:
        # Change the name here
        name = filt
        item = QtGui.QListWidgetItem(defaultIcon, QtCore.QString(name), listWidget)
        item.className = filt # Store class name
        listPointer[filt] = item
        listWidget.addItem(item)

def sharedLoadGroupbox(parentWidget, layoutWidget, groupboxes, engine, widgetPointer):
    '''
    Loads the group box of the current filter
    '''
    # Hide all
    for gb in groupboxes.values():
        gb.hide()

    if engine.getFilterName() in groupboxes:
        groupboxes[engine.getFilterName()].show()
    else:
        gb = groupboxes[engine.getFilterName()] = QtGui.QGroupBox("Filter Settings")
        grid = QtGui.QGridLayout()

        params = engine.alg.parameters()
        for i, param in enumerate(params):
            # Add integer

            handler = GetParameterHandler(param) # construct because functions are not static

            try:
                handler = GetParameterHandler(param) # construct because functions are not static
            except:
                print>>sys.stderr, "Unsupported type %s" % repr(param.vartype)
                continue

            # Label
            label = QtGui.QLabel(parentWidget)
            label.setText(param.caption)
            #font = QtGui.QFont()
            #font.setPointSize(11)
            #label.setFont(font)

            grid.addWidget(label, i, 0)
            # Control
            control = handler.createWidget(parentWidget)
            if param.default != None:
                handler.setValue(control, param.default)

            widgetPointer[engine.getFilterName(), param.name] = control
            grid.addWidget(control, i, 1)
        
        
        gb.setLayout(grid)
        layoutWidget.insertWidget(0, gb)

def sharedGetParameters(paramWidgetPointer, parameters_dictionary):
    '''
    This function takes the Qt controls from a groupbox and converts them
    into a dictionary of parameters (settings).
    
    parameters_dictionary should be stored with the dictionary of the parameters
    specification for each. For instance, if the groupbox has 'A', 'B', 'C', then
    parameters_dictionary could look like this:
    {
        'A': [<Parameter>, <Parameter>],
        'B': [...],
        'C': [...]
    }
    This is important so that the results can be presented in the correct data types
    '''
    params = dict()
    
    # Iterate parameters and then find widgets (could be done
    # in the opposite direction, but then we would have to do a similar
    # linear search through the parameters to figure what type it is)
    
    for name, dic in parameters_dictionary.items():
        params[name] = dict()
        for p in dic:
            try:
                widget = paramWidgetPointer[name, p.name]
                handler = GetParameterHandler(p)
            except:
                print>>sys.stderr, "Could not find widget or unsupported type for %s" % p.name
                continue

            params[name][p.name] = handler.getValue(widget)    
    
    return params