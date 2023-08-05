
# Framework
import sys
import os
import re

# Project
from Engine.Engine import Engine

if __name__ == '__main__':
    engine = Engine()
    engine.loadDataNPZ('/Users/Gustav/Dropbox/Exjobbsanalys/NPZ/120/torb-1-120.npz')
    
    
    for i in xrange(len(engine.data)):
        print engine.data[i,0], engine.data[i,1]