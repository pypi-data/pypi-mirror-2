
# Project
from .Engine.Metric import Metric, MetricResults
from .Engine.Filter import Filter

class Histograms(Metric):
    """
    Checks the noise level, just for testing
    """
    def __init__(self):
        super(Histograms, self).__init__()
    
    
    def analyse(self, engine):
        fix_durs = list(engine.iterateStateDurations(Filter.FIXATION))
        sac_durs = list(engine.iterateStateDurations(Filter.SACCADE))
        
        return {'fixation_durations': fix_durs, 'saccadic_durations': sac_durs}

    def arrangeResults(self):
        res = {}
        res['fixation_durations'] = []
        res['saccadic_durations'] = []
        for subresults in self.results:
            res['fixation_durations'] += subresults['fixation_durations']
            res['saccadic_durations'] += subresults['saccadic_durations']
            #print "-- ", len(subresults['saccadic_durations'])
            #print "-: ", len(res['saccadic_durations'])

        #print res['saccadic_durations']
        # Filter too high durations
        #res['fixation_durations'] = filter(lambda x: x<1500, res['fixation_durations'])
        #res['saccadic_durations'] = filter(lambda x: x<400, res['saccadic_durations'])

        #print "LENGTH:", len(res['saccadic_durations'])
        
        return [
            MetricResults('histogram', 'Saccadic durations', {
                    'data': res['saccadic_durations'],
                    'bins': 400,
                    'xlabel': "Duration (ms)",
                    'ylabel': "Counts",
                }
            ),
            MetricResults('histogram', 'Fixation durations', {
                    'data': res['fixation_durations'],
                    'bins': 100,
                    'xlabel': "Duration (ms)",
                    'ylabel': "Counts",
                }
            ),
        ]





