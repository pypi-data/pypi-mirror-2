#! /usr/bin/env python

# Framework
import sys
import os
import re
from numpy import arange, array
from copy import copy

# Project
from Engine.Engine import Engine
from Engine.Analyser import Analyser
from Filters.I_VT import I_VT
from Filters.I_DT import I_DT
from Filters.HMM import HMM
from Filters.Clearview import Clearview
from Filters.TobiiFixation import TobiiFixation
from Metrics.Histograms import Histograms
from Filtering.sgolay import savitzky_golay


# Prepare the algorithms and their parameters        
engine = Engine()

def filtering(data):
    # Filter x and y
    new_data = copy(data)
    for i in xrange(len(data)):
        new_data[i,1] = data[i-4:i+5,1].mean()
        new_data[i,2] = data[i-4:i+5,2].mean()
        
        #print new_data[i,1]
        
    
        
    #data = new_data
    #data[:,1] = savitzky_golay(data[:,1])
    #data[:,2] = savitzky_golay(data[:,2])
    return new_data

engine.filtering = None

# algsDict = {}
# parameter_dictionary = {}
# for algName in self.addedAlgorithms:
#     tempEngine.setFilterByName(algName)
#     algsDict[algName] = tempEngine.alg
#     parameter_dictionary[tempEngine.getFilterName()] = tempEngine.alg.parameters()

# Check settings
#params = sharedGetParameters(self.paramWidgetPointer, parameter_dictionary)

# Set the parameters
#for algName, paramsDict in params.items():
#    algsDict[algName].params = paramsDict

ivt = I_VT()
idt = I_DT()
cv = Clearview()
tff = TobiiFixation()
hmm = HMM()

# Make sure the metrics are imported
metric = Histograms()

# Initialize the analysis
analyser = Analyser()

def foralgo(alg, th):
    if alg == 'ivt':
        engine.alg = I_VT()
        engine.alg.params = {
            'threshold': th,
            'diffwith': 1,
            'dur_threshold': 100,
        }
    elif alg == 'idt':
        engine.alg = I_DT()
        engine.alg.params = {
            'threshold': th,
            'dur_threshold': 100,
        }
    elif alg == 'cv':
        engine.alg = Clearview()
        engine.alg.params = {
            'radius': th,
            'minduration': 100,
        }
    elif alg == 'tff':
        engine.alg = TobiiFixation()
        engine.alg.params = {
            'threshold': th,
            'windowsize': 4,
            'interpolatewindow': 100,
        }
    elif alg == 'hmm':
        engine.alg = HMM()
        engine.alg.params = {
            'threshold': th,
            'steepness': 1/10.0,
            'dur_threshold': 100.0,
        }

    analyser.analyse(engine, [engine.alg], [metric], 
        "/Users/Gustav/Dropbox/Exjobbsanalys/NPZ/120") # /gustav-2-60.npz
    res = analyser.getResultsGroups('Histograms')[0].getResultsList()[0].getData()
    
    return res['data']
    #print "%s, %s, %s" % (th, precision, recall)


#thresholds = arange(0.0, 101.0, 50.0)

results = {
    'recall': {},
    'precision': {},
}


setups = {
    'ivt': 8.0 * 17.5,
    'idt': 0.4 * 8,
    'cv': 1.34 * 7,
    'tff': 2.2 * 3,
    'hmm': 8.0 * 12.5,
}

def savealgorithm(alg):
    res = foralgo(alg, setups[alg])
    f = open('saccades120%s.txt' % alg, 'w')
    
    bins = {}
    period = (1000.0/120)
    for dur in res:
        bin = (round(dur/period)-0.5)*period
        if bin in bins:
            bins[bin] += 1
        else:
            bins[bin] = 1
        
        
    for bin, count in bins.items():
        f.write('%s %s\n' % (bin, count))
    
    #for length, count in res.items():
    #for dur in res:
        #f.write('%s %s\n' % (length, count))
    #    f.write("%s\n" % (dur))
    #f.close()

for alg in setups:
	savealgorithm(alg)

#import pdb; pdb.set_trace()


# for metricName in analyser.getMetricNames():
#     self.resultsDialog.createBigDivider(metricName)
#     
#     for resGroup in analyser.getResultsGroups(metricName):
#         self.resultsDialog.createDivider(resGroup.getName())
#         self.resultsDialog.addResultsGroup(resGroup)
