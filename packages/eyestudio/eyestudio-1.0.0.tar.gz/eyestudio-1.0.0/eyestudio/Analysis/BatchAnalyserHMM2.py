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
from Filters.HMM3 import HMM3
from Filters.Clearview import Clearview
from Filters.TobiiFixation import TobiiFixation
from Metrics.CompareWithStimulus import CompareWithStimulus
from Filtering.sgolay import savitzky_golay


# Prepare the algorithms and their parameters        
engine = Engine()

def filtering(data):
    # Filter x and y
    new_data = copy(data)
    for i in xrange(len(data)):
        new_data[i,1] = data[i-4:i+5,1].mean()
        new_data[i,2] = data[i-4:i+5,2].mean()
        
        print new_data[i,1]
        
    
        
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

hmm = HMM()

# Make sure the metrics are imported
metric = CompareWithStimulus()

# Initialize the analysis
analyser = Analyser()

def foralgo(alg, thresholds):
    ps = []
    rs = []
    print alg
    for th in thresholds:
        #print th
        if alg == 'hmm1':
            engine.alg = HMM3()
            engine.alg.params = {
                'threshold': th,
                'steepness': 1/10.0,
                'dur_threshold': 100.0
            }
        elif alg == 'hmm2':
            engine.alg = HMM()
            engine.alg.params = {
                'threshold': th,
                'steepness': 1/15.0,
                'dur_threshold': 100.0
            }
        elif alg == 'hmm3':
            engine.alg = HMM()
            engine.alg.Mfixed = array([[0.9, 0.1], [0.5, 0.5]])
            engine.alg.params = {
                'threshold': th,
                'steepness': 1/10.0,
                'dur_threshold': 100.0
            }
        elif alg == 'hmm4':
            engine.alg = HMM()
            engine.alg.Mfixed = array([[0.8, 0.2], [0.5, 0.5]])
            engine.alg.params = {
                'threshold': th,
                'steepness': 1/10.0,
                'dur_threshold': 100.0
            }

        analyser.analyse(engine, [engine.alg], [metric], "/Users/Gustav/Dropbox/Exjobbsanalys/NPZ/60")
        res = analyser.getResultsGroups('CompareWithStimulus')[0].getResultsList()[0].getData()
        precision, recall = res['Precision'], res['Recall']
    
        recall = 3/2.0 * (recall - 1/3.0)
        
        ps.append(precision)
        rs.append(recall)
        
        print th, precision, recall
        
    return ps, rs
    #print "%s, %s, %s" % (th, precision, recall)


thresholds = arange(0.0, 101.0, 50.0)

results = {
    'recall': {},
    'precision': {},
}

#N = 51

#ran = arange(0.0, 400.1, 2*4.0)
#ran = array([70.0])
ran = array([50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0])
setups = [
    ('hmm1', ran),
    # ('hmm2', ran),
    # ('hmm3', ran),
    # ('hmm4', ran),
]

N = len(ran)

for alg, thresholds in setups:
    assert len(thresholds) == N

for alg, thresholds in setups:
    ps, rs = foralgo(alg, thresholds)

    results['precision'][alg] = ps
    results['recall'][alg] = rs

def writefile(name):
    f = open('%shmm2-60.txt' % name, 'w')
    for i in xrange(N):
        p = results[name]
        if 0:
            f.write("%d, %s, %s, %s, %s\n" % (i, 
                p['hmm1'][i],
                p['hmm2'][i],
                p['hmm3'][i],
                p['hmm4'][i]))
        else:
            f.write("%d, %s\n" % (i, 
                p['hmm1'][i]))
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
