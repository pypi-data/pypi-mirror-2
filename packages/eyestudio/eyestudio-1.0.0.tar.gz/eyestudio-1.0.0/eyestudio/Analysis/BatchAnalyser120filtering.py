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
from Filters.I_VT_SG import I_VT_SG
from Filters.Clearview import Clearview
from Filters.TobiiFixation import TobiiFixation
from Metrics.CompareWithStimulus import CompareWithStimulus
from Filtering.sgolay import savitzky_golay


# Prepare the algorithms and their parameters        
engine = Engine()

def sg(data):
    #data = new_data
    data[:,1] = savitzky_golay(data[:,1], order=4)
    data[:,2] = savitzky_golay(data[:,2], order=4)
    return data
    
def window(data):
    new_data = copy(data)
    for i in xrange(len(data)):
        new_data[i,1] = data[i-6:i+7,1].mean()
    return new_data
    
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
            engine.filtering = None
            engine.alg.params = {
                'threshold': th,
                'diffwith': 1,
                'dur_threshold': 100,
            }
        elif alg == 'ivt-sg':
            engine.alg = I_VT()
            engine.filtering = sg
            engine.alg.params = {
                'threshold': th,
                'diffwith': 1,
                'dur_threshold': 100,
            }
        elif alg == 'ivt-window':
            engine.alg = I_VT()
            engine.filtering = window
            engine.alg.params = {
                'threshold': th,
                'diffwith': 1,
                'dur_threshold': 100,
            }
        elif alg == 'ivt-sg2':
            engine.alg = I_VT_SG()
            engine.filtering = None # built-in
            engine.alg.params = {
                'threshold': th,
                'diffwith': 1,
                'dur_threshold': 100,
            }
    
        #/jesper-2-120.npz
        analyser.analyse(engine, [engine.alg], [metric], "/Users/Gustav/Dropbox/Exjobbsanalys/NPZ/120")
        res = analyser.getResultsGroups('CompareWithStimulus')[0].getResultsList()[0].getData()
        precision, recall = res['Precision'], res['Recall']
    
        ps.append(precision)
        rs.append(recall)
        
    return ps, rs
    #print "%s, %s, %s" % (th, precision, recall)


results = {
    'recall': {},
    'precision': {},
}

#ran = arange(0.0, 400.1, 4.0*100) #array([100.0, 200.0])#

ran = arange(0.0, 400.1, 400.0/35)
#ran = array([80, 90, 100, 110])

N = len(ran)

setups = [
    ('ivt', ran),
    ('ivt-sg2', ran),
    ('ivt-sg', ran),
    ('ivt-window', ran),
]

for alg, thresholds in setups:
    assert len(thresholds) == N

for alg, thresholds in setups:
    ps, rs = foralgo(alg, thresholds)

    results['precision'][alg] = ps
    results['recall'][alg] = map(lambda x: 3/2.0 * (x - 1/3.0), rs)
    
    print ps, rs
    
    #print results['recall']


def writefile(name):
    f = open('%s120ivt.txt' % name, 'w')
    for i in xrange(N):
        p = results[name]
        f.write("%d, %s, %s, %s, %s\n" % (i, 
            p['ivt'][i],
            p['ivt-sg'][i],
            p['ivt-sg2'][i],
            p['ivt-window'][i]))
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
