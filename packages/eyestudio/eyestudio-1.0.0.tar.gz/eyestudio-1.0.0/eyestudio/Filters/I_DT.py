
# Framework
import numpy as np
from math import tan, radians

# Project
from .Engine.Filter import Filter, Parameter

class I_DT(Filter):
    '''
    Velocity threshold filter adopted from Salvucci 2000
    '''
    def __init__(self):
        super(I_DT, self).__init__()
        
        self.state = None
        self.ordinal = 0
        self.last_state = None

    def parameters(self):
        return [
            Parameter(name='threshold', caption='Threshold [deg]', vartype=float, default=3.8),
            Parameter(name='dur_threshold', caption='Min dur [ms]', vartype=float, default=100.0),
        ]

    def process(self, data, setFixation):
        threshold = self.getParameter('threshold')
        durThreshold = self.getParameter('dur_threshold')
        c = len(data)
        # Create inital window of length durThreshold
        
        for i in xrange(c):
            setFixation(i, Filter.SACCADE)
        
        def threshold_mm():
            return 2 * headDistance * tan(radians(threshold / 2.0))
        
        headDistance = 700
        
        start = 0
        end = 0
        while end+1 < c:
            if data[start,3] > 0:
                headDistance = data[start,3]
            
            while end+1 < c and data[end+1,0] - data[start,0] < durThreshold:
                 end += 1

            if self.dispersion(data, start, end) < threshold_mm():
                while self.dispersion(data, start, end+1) < threshold_mm() and end+1 < c:
                    end += 1
                    
                # Mark all as fixations
                for i in xrange(start, end+1):
                    setFixation(i, Filter.FIXATION)
                
                # Reset (skip one to insert a saccade)
                end += 2
                start = end
            else:
                start += 1
        
    def dispersion(self, data, start, end):
        x, y = data[start:end+1,1], data[start:end+1,2]
        return (np.max(x) - np.min(x)) + (np.max(y) - np.min(y))