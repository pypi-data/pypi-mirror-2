
# Framework
import numpy as np
from math import degrees, atan

# Project
from .Engine.Filter import Filter, Parameter

class I_VT(Filter):
    '''
    Velocity threshold filter adopted from Salvucci 2000
    '''
    def __init__(self):
        super(I_VT, self).__init__()
        
        self.state = None
        self.last_state = None

    def parameters(self):
        return [
            Parameter(name='threshold', caption='Threshold [deg/s]', vartype=float, default=77.0),
            Parameter(name='diffwith', caption='Dist with', vartype=dict, varinfo={-1: 'Prev', 1: 'Next'}, default=1),
            Parameter(name='dur_threshold', caption='Min dur [ms]', vartype=float, default=100.0),
        ]

    def process(self, data, setFixation):
        thresh = self.getParameter('threshold')
        minTime = self.getParameter('dur_threshold')
        headDistance = 700
        
        fixationStart = 0
        for index in xrange(data.shape[0]):
            gazepoint = data[index,1:3]
            time = data[index,0]
            v = np.array([0,0])
            diff = self.getParameter('diffwith')
            
            if data[index,3] > 0:
                headDistance = data[index,3]
            
            if index+diff >= 0 and index+diff < data.shape[0]: # Next point
                # Notice the order doesn't matter, because negative time will correct it anyway
                dp = (data[index,1:3] - data[index+diff,1:3]).astype(float)
                dt = (data[index,0] - data[index+diff,0]) # [ms]
                v = dp/dt
            
                # Convert to degrees of visual angle
                d = np.sqrt(np.dot(v, v))
                theta = degrees(2.0 * atan(d/(2.0*headDistance)))
                theta *= 1000.0 # [deg/s]
             
            # TODO Store the square of that value in some preprocess function to avoid the norm
            #time_ok = fixationStart is None or time >= lastFixationTime + minTime
            
            if theta < thresh:
                self.state = Filter.FIXATION
                
                if self.last_state != self.state:
                    fixationStart = index
            else:
                if self.last_state == Filter.FIXATION:
                    # Check if it's long enough
                    dur = data[index,0] - data[fixationStart,0]
                    if dur < minTime:
                        # Make all into saccades again
                        for i in xrange(fixationStart, index):
                            setFixation(i, self.SACCADE)
                
                self.state = Filter.SACCADE
            
            self.last_state = self.state        
            setFixation(index, self.state)
