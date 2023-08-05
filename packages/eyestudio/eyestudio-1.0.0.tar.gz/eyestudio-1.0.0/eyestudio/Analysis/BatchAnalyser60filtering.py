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
from Filters.Clearview import Clearview
from Filters.TobiiFixation import TobiiFixation
from Metrics.CompareWithStimulus import CompareWithStimulus
from Filtering.sgolay import savitzky_golay


# Prepare the algorithms and their parameters        
engine = Engine()

def filtering(data):
    # Filter x and y
    # new_data = copy(data)
    # for i in xrange(len(data)):
    #     new_data[i,1] = data[i-4:i+5,1].mean()
    #     new_data[i,2] = data[i-4:i+5,2].mean()
    #     
    #     print new_data[i,1]
    #return new_data
    
        
    #data = new_data
    data[:,1] = savitzky_golay(data[:,1], order=2)
    data[:,2] = savitzky_golay(data[:,2], order=2)
    return data

engine.filtering = filtering

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

# Make sure the metrics are imported
metric = CompareWithStimulus()

# Initialize the analysis
analyser = Analyser()

def foralgo(alg, thresholds):
    ps = []
    rs = []
    print alg
    for th in thresholds:
        print th
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
    
        analyser.analyse(engine, [engine.alg], [metric], "/Users/Gustav/Dropbox/Exjobbsanalys/NPZ/60")
        res = analyser.getResultsGroups('CompareWithStimulus')[0].getResultsList()[0].getData()
        precision, recall = res['Precision'], res['Recall']
    
        ps.append(precision)
        rs.append(recall)
        
    return ps, rs
    #print "%s, %s, %s" % (th, precision, recall)


thresholds = arange(0.0, 101.0, 50.0)

results = {
    'recall': {},
    'precision': {},
}


N = 26

setups = [
    ('ivt', arange(0.0, 400.1, 4.0*4)),
    ('idt', arange(0.0, 20.1, 0.2*4)),
]

for alg, thresholds in setups:
    assert len(thresholds) == N

for alg, thresholds in setups:
    ps, rs = foralgo(alg, thresholds)

    results['precision'][alg] = ps
    results['recall'][alg] = map(lambda x: 3/2.0 * (x - 1/3.0), rs)


def writefile(name):
    f = open('%s60filt.txt' % name, 'w')
    for i in xrange(N):
        p = results[name]
        f.write("%d, %s, %s\n" % (i, 
            p['ivt'][i],
            p['idt'][i]))
        #f.write("%d, %s\n" % (i, p['ivt'][i]))
    f.close()
    
writefile('precision')
writefile('recall')

#import pdb; pdb.set_trace()


# for metricName in analyser.getMetricNames():
#     self.resultsDialog.createBigDivider(metricName)
#     
#     for resGroup in analyser.getResultsGroups(metricName):
#         self.resultsDialog.createDivider(resGroup.getName())
#         self.resultsDialog.addResultsGroup(resGroup)
