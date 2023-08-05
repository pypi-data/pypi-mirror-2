#! /usr/bin/env python

# This script zips together a stimulus folder, a tsv folder and
# a npz folder.

# Framework
import sys
import os
import re

# Project
from Engine.Engine import Engine

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage:"
        print " Arranger.py [Stimulus folder] [TSV folder] [NPZ folder]"
        sys.exit(0)
    else:
        sti_folder = sys.argv[1]
        tsv_folder = sys.argv[2]
        npz_folder = sys.argv[3]
        
        # Start by creating folders for 60 and 120 Hz
        #for d in ["60", "120"]:
            
        
        if os.path.isdir(tsv_folder):
            files = []
            for fn in os.listdir(tsv_folder):
                name, ext = os.path.splitext(fn)
                if ext.lower() == '.tsv':
                    info = name.split('-')
                    subject = info[1]
                    stim_no = int(info[2])
                    freq = int(info[3])
                    
                    stim_file = os.path.join(sti_folder, 
                        "thesis{0}.stim.txt".format(stim_no)
                    )
                                        
                    engine = Engine()
                    engine.loadDataTSV(os.path.join(tsv_folder, fn))
                    engine.loadStimulusFromFile(stim_file)
                    
                    # Create output folder
                    try:
                        os.makedirs(os.path.join(npz_folder, str(freq)))
                    except:
                        pass

                    output_file = os.path.join(npz_folder, str(freq),
                        "{0}-{1}-{2}.npz".format(subject, stim_no, freq))
                    
                    engine.saveDataNPZ(output_file)
                    
                    