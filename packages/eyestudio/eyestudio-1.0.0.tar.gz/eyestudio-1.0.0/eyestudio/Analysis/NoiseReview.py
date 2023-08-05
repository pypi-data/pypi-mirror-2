
from Engine.Engine import Engine
from copy import copy

engine = Engine()

from Filtering.sgolay import savitzky_golay




engine.loadDataNPZ("/Users/Gustav/Dropbox/Exjobbsanalys/NPZ/60/jesper-0-60.npz")
data = engine.data
    


# Prepare the algorithms and their parameters        
engine2 = Engine()

def filtering(data):
    order = 3
    data[:,1] = savitzky_golay(data[:,1], order=order, deriv=1)
    data[:,2] = savitzky_golay(data[:,2], order=order, deriv=1)
    return data

def filtering2(data):
    new_data = copy(data)
    for i in xrange(len(data)):
        new_data[i,1] = data[i-5:i+6,1].mean()
    return new_data

engine2.filtering = filtering

engine2.loadDataNPZ("/Users/Gustav/Dropbox/Exjobbsanalys/NPZ/60/jesper-0-60.npz")
filt = engine2.data
    
for i in xrange(100, 1000):
    #v = abs(data[i+1,1] - data[i,1])
    vf = abs(filt[i,1])
    #vf = abs(filt[i+1,1] - filt[i,1])
    
    print "%s, %s, %s" % (data[i,0], data[i,1], vf)