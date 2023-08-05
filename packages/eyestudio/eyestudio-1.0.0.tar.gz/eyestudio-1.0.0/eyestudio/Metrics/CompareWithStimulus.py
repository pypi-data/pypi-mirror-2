
# Project
from .Engine.Metric import Metric, MetricResults
from .Engine.Filter import Filter

# Framework
import sys
import numpy as np
from copy import copy

class CompareWithStimulus(Metric):
    """
    Compares with stimulus to see how close it came
    """
    def __init__(self):
        super(CompareWithStimulus, self).__init__()
    
    def checkDiffSq(self, engine, deltaFrames):
        '''
        Checks the difference between the stimulus and the point
        with a shift of 'deltaFrames' between them.
        It returns the squared difference.
        '''
        total = 0
        points = 0
        for i in xrange(len(engine.data)):
            rpos = engine.data[i,1:3]
            if rpos[0] < -30:
                continue
                
            t = engine.getTime(i)
            event = engine.stimulus.getEvent(t)
            
            if not event or not event.pos or not event.active:
                continue

            try:
                spos = engine.stimulus.getPosition(i-deltaFrames)
                points += 1
            except:
                spos = 0
                
            dvec = np.array([spos[0]-rpos[0], spos[1]-rpos[1]])
            d = np.dot(dvec, dvec)
            
            total += d
        if points == 0:
            print "Error: Analysis data must contain stimuli"
            sys.exit(0)
            
        return total/float(points)
    
    def framesDelay(self, engine, fr, to):
        # Binary search domain
        #fr = 0
        #to = 50

        if True: # Linear search
            scores = []
            for i in xrange(fr, to+1):
                tup = (self.checkDiffSq(engine, i), i)
                #print tup
                scores.append(tup)
            scores.sort()
            shift = scores[0][1]
        
        else: # Binary search
            iterations = 10
            while iterations > 0 and abs(fr-to) > 1:
                lower = (3 * fr + to)/4.0
                upper = (fr + 3 * to)/4.0
                middle = (fr + to)/2.0
                
                s1 = self.checkDiffSq(engine, lower)
                s2 = self.checkDiffSq(engine, upper)
                
                if s1 < s2:
                    to = middle
                else:
                    fr = middle
                    
                iterations -= 1
            shift = int(round((fr+to)/2.0))
        
        return shift
        
    
    def analyse(self, engine):
        
        # This should be made into a proper error message
        assert engine.hasStimulus()
        
        THRESHOLD = 20
        
        period = (engine.data[-1,0] - engine.data[0,0])/len(engine.data)
            
        # Temporary
        if period > 10: # 60 Hz
            fr = 13
            to = 17
        else:
            fr = 26
            to = 33
            
        deltaTime = period * self.framesDelay(engine, fr, to)
        
        # TODO: Do this automatically (it will be a bit slow though)
        engine.stimulus.setDeltaTime(-deltaTime)
        engine.stimulus.reInitPositions()
        num_events = engine.stimulus.numActiveEvents()
        
        #f = open("/Users/Gustav/Desktop/debug.txt", "w")

        events = {}

        active_fixations = set()
        
        # Problems with fixations across active regions
        # ----------------------------------------------------
        # If the subject does not blink between active regions
        # of the stimulus, then it can be a long fixation
        # spanning the whole blink. This reduces the score
        # because it can only be used for one stimuli region.
        # This is fixed (not too elegantly) looking through
        # the stimulus and inserting fixation breaks during
        # inactive regions.
        
        fixations = engine.getFixations()
        handledEvents = set()
        for i in xrange(len(engine.data)):
            t = engine.getTime(i)
            event = engine.stimulus.getEvent(t)
            if event and event not in handledEvents and not event.active:
                handledEvents.add(event)
                # Insert the break in the middle, there's no real reason
                # for this other than we don't want to get too close
                # to the edge and make a mistake. Especially since we have shifted
                # the stimulus.
                tmiddle = (2.0*t + event.duration_ms)/2.0
                j = int(tmiddle/period)
                break_i = None
                for k, fix in enumerate(fixations):
                    if j >= fix.start and j <= fix.end:
                        # Break into two
                        break_i = k
                        break
                    
                if break_i is not None:
                    fix = fixations[break_i]
                    del fixations[break_i]
                    fix1 = copy(fix)
                    fix1.end = j
                    fix2 = copy(fix)
                    fix2.start = j
                
                    fixations.insert(break_i, fix1)
                    fixations.insert(break_i+1, fix2)
                        
        # Iterate fixations
        for fixation in fixations:
            stims = {}
            
            #print "Fixation:", fixation.start, fixation.end
            
            # Iterate every frame in this fixation
            for i in xrange(fixation.start, fixation.end):
                t = engine.getTime(i)
                event = engine.stimulus.getEvent(t)
                
                if event and event.active and event.pos:
                    # Check stimulus position
                    try:
                        spos = engine.stimulus.getPosition(i)
                    except:
                        continue
                        
                    # Check if valid
                    if spos[0] < 0:
                        continue

                    rpos = fixation.pos

                    # Check distance between the fixation and the stimulus
                    dvec = np.array([spos[0]-rpos[0], spos[1]-rpos[1]])
                    d = np.sqrt(np.dot(dvec, dvec))
                    
                    # This set counts all fixations that have been
                    #  present during intervals with active stimulus
                    active_fixations.add(fixation)
                                        
                    # If it's close enough
                    if d <= THRESHOLD:
                        try:
                            stims[event] += 1
                        except:
                            stims[event] = 1
                            
                
            max_count = -1
            max_event = None
            for event, count in stims.items():
                if count > max_count:
                    max_count = count
                    max_event = event
            
            if max_event is not None:
                #total = fixation.end - fixation.start
            
                if max_event not in events:
                    # Add (stimulus, recall)
                    events[max_event] = []

                if max_count >= 0:
                    events[max_event].append((fixation, max_count))
                
        
        used_fixations = 0
        recall = 0.0
        for event, array in events.items():
            final_count = 0
            for fixation, max_count in array:
                if max_count > final_count:
                    final_count = max_count

            if final_count > 0:
                used_fixations += 1
                #print "recall:", event.pos, final_count, (final_count*1000.0/60.0), event.duration_ms
                recall += (final_count*period)/event.duration_ms
        
        # Normalize total recall with number active events
        recall /= float(num_events)
        
        #print "used", used_fixations
        
        num_fixations = len(active_fixations)
        if num_fixations > 0:
            precision = float(used_fixations)/num_fixations
        else:
            precision = 0
            
        #print 'recall', recall
            
        #print "EVENTS"
        #print events
    
        #meandist = check_d(0)
        #f.close()
        meandist = 0
        
        #fscore = 2.0 * recall * precision / (recall + precision)
       
        return {'recall': recall, 'precision': precision}

    def arrangeResults(self):
        res = {}
        res['recall'] = 0
        res['precision'] = 0
        #res['fscore'] = 0
        c = len(self.results)
        for subresults in self.results:
            res['recall'] += subresults['recall']
            res['precision'] += subresults['precision']
            #res['fscore'] += subresults['fscore']
            
        res['recall'] /= float(c)
        res['precision'] /= float(c)
        
        try:
            res['fscore'] = 2.0 * res['recall'] * res['precision'] / (res['recall'] + res['precision'])
        except ZeroDivisionError:
            res['fscore'] = 0
        
        return [
            # Present as bar chart and table
            MetricResults('barchart', 'Precision and recall', {
                    # 'recall': "%.2f%%" % (res['recall']*100),
                    # 'Used ratio': "%.2f%%" % (res['precision']*100),
                    'Precision': res['precision'],
                    'Recall': res['recall'],
                    #'F-score': res['fscore'],
                }
            ),
            MetricResults('table', 'Precision and recall', {
                    'Precision': "%.2f%%" % (res['precision']*100),
                    'Recall': "%.2f%%" % (res['recall']*100),
                    #'F-score': "%.2f%%" % (res['fscore']*100),
                }
            ),
        ]





