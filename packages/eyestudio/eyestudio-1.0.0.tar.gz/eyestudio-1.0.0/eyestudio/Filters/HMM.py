# Framework
import numpy as np
from copy import copy
from math import log, sqrt, pi, exp, atan, degrees
import sys

# Project
from .Engine.Filter import Filter, Parameter

# Transition matrix
class HMM(Filter):
    '''2-state filter using HMM'''
    def __init__(self):
        super(HMM, self).__init__()
        
        # Number of states
        self.N = 2
        self.Mfixed = None
        
        self._reset_cache()
        self.init_values()
        
    def init_values(self):
        if self.Mfixed is not None:
            M = self.Mfixed
        else:
            M = np.array([
                [0.55, 0.45],
                [0.45, 0.55],
            ])

        self.mu = np.array([0.0, 100.0])
        self.sigma = np.array([5.0, 20.0])
        
        self.M = M

        # Initial state probabilities
        self.Pi = np.array([1/2.0, 1/2.0])
        

    def parameters(self):
        return [
            Parameter(name='threshold', caption='Threshold (deg/s)', vartype=float, default=77.0),
            Parameter(name='steepness', caption='Steepness', vartype=float, default=0.1),
            Parameter(name='dur_threshold', caption='Min dur [ms]', vartype=float, default=100.0),
        ]
    
    def feature(self, data, index):
        '''
        Returns the feature to represent the signal of the
        data at index.
        '''
        diff = 1
        try:
            dp = (data[index,1:3] - data[index+diff,1:3]).astype(float)
            dt = (data[index,0] - data[index+diff,0]) # [ms]
            v = dp/dt
        
            # Convert to degrees of visual angle
            d = np.sqrt(np.dot(v, v))
            theta = degrees(2.0 * atan(d/(2.0*data[index,3])))
            theta *= 1000.0 # [deg/s]

        except IndexError: # Clean this up
            theta = 0.0

        return theta
        
    def gaussian(self, feature, state):
        sigma, mu = self.sigma[state], self.mu[state]
        return 1.0/(sigma * sqrt(2 * pi)) * exp(-(feature - mu)**2 / (2 * sigma**2))
        
    # def determine_k(self, data, index):
    #     diff = 1
    #     try:
    #         dp = (data[index][1:] - data[index+diff][1:]).astype(float)
    #         dt = (data[index][0] - data[index+diff][0]) # [ms]
    #         v = dp/dt
    #     except IndexError: # Clean this up
    #         v = 0.0
    #      
    #     k = int(np.dot(v, v) > self.threshold_squared())
    #     return k
        
    def _cache_emission2(self, data):
        self.emission = np.zeros((len(data), self.N), float)
    
        for index in xrange(len(data)):
            for state in xrange(self.N):        
                v = self.feature(data, index)
                if self.N == 2:
                    mu1, si1 = self.mu[state], self.sigma[state]
                    mu2, si2 = self.mu[int(not state)], self.sigma[int(not state)]
            
                    def expo(mu, si):
                        return (v - mu)**2 / (2.0 * si**2)
            
                    try:
                        ret = 1.0/(1.0 + si1/si2 * exp(expo(mu1, si1) - expo(mu2, si2)))
                    except:
                        ret = 1e-20

                    self.emission[index, state] = ret


    def _cache_emission(self, data):
        self.emission = np.zeros((len(data), self.N), float)

        threshold = self.getParameter('threshold')
        steepness = self.getParameter('steepness')
        
        EPS = 1e-8
        for index in xrange(len(data)):
            v = self.feature(data, index)
            try:
                ret = 1.0/(1.0 + exp(steepness*(threshold-v)))
            except OverflowError:
                ret = 0.0
            ret = min(1.0-EPS, max(EPS, ret))
            
            self.emission[index, 1] = ret
            self.emission[index, 0] = 1.0 - ret
        
    def transition(self, state1, state2):
        return self.M[state1, state2]

    def process(self, data2, setFixation):

        self.init_values()
        
        data = copy(data2)
        # Fill in missing head distance data
        dist = 700
        
        for i in xrange(len(data)):
            if data[i,3] > 0:
                dist = data[i,3]
            else:
                data[i,3] = dist
                
        self.mu[1] = self.getParameter('threshold')
        
        # Train first
        if self.Mfixed is None:
            for i in xrange(4):
                def setFixationNull(*args): pass
                self.process_raw(data, setFixationNull)
                self.trainParameters(data)
                
        # What was the transition matrix, because this is all we're training
        #print self.M
        
        # self.M = np.array([
        #     [0.95, 0.05],
        #     [0.6, 0.4]
        # ])
        
        self.process_raw(data, setFixation)

    def process_raw(self, data, setFixation):
        
        if self.Pi[1] < 0.001:
            self.Pi[1] = 0.001
            self.Pi[0] = 1.0 - self.Pi[1]
        
        
        self._cache_emission(data)
        
        self.delta2layers = [[], []]

        # Initialization
        self.delta2layers[0] = np.array([0.0]*self.N)
        self.delta2layers[1] = np.array([0.0]*self.N)
        
        cur_delta = 0
        delta_t = self.delta2layers[cur_delta]
        
        # 1) Initialization:
        for i in xrange(self.N):
            delta_t[i] = log(self.Pi[i]) + log(self.emission[0, i])
        
        psi = np.array([0]*self.N).reshape(self.N, 1)
        
        dataSize = data.shape[0]
        for index in xrange(1, dataSize):
            # switches between 0 and 1
            cur_delta = int(not cur_delta)
            
            # Check if data point is valid
            if data[index,3] <= 0:
                continue
                
            delta_t = self.delta2layers[cur_delta]
            delta_last_t = self.delta2layers[int(not cur_delta)]
            
            psi_t = np.array([0]*self.N).reshape(self.N, 1)

            # Set new deltas
            for j in range(self.N):
                
                maxvalue = -1e10000000
                maxindex = None
                for i in xrange(self.N):
                    value = delta_last_t[i] + log(self.transition(i, j))
                    
                    #print value
                    if value > maxvalue:
                        maxvalue = value
                        maxindex = i

                # 2) Recursion
                delta_t[j] = maxvalue + log(self.emission[index, j])
                # if index < 10:
                #     print "Emission({0}, {1}) = {2}".format(index, j, self.emission(data, index, j))
                #print maxindex
                psi_t[j] = maxindex
                
            psi = np.hstack([psi, psi_t])
                
        # 3) Termination
        q_T_star = np.argmax(delta_t)
        
        p_T_star = delta_t[q_T_star]
        
        # 4) Path backtracking
        path = [q_T_star]
        for t in xrange(dataSize-1, 0, -1):
            q_t_star = psi[path[0], t]
            path.insert(0, q_t_star)
            
        # Path is our states
        last_state = None
        fixation_start = None
        for i, p in enumerate(path):
            # Implement miminum duration
            if p == Filter.FIXATION and last_state != p:
                fixation_start = i
            
            if p == Filter.SACCADE and last_state == Filter.FIXATION:
                dur = data[i, 0] - data[fixation_start, 0]
                if dur < self.getParameter('dur_threshold'):
                    for i in xrange(fixation_start, index):
                        setFixation(i, self.SACCADE)
                
            setFixation(i, p)
            
            last_state = p
                        
    def trainParameters(self, data):
        '''
        This model uses a data object to train parameters.
        The model is updated with the new parameters of
        one iteration. NOTE: This means that the function must
        be called several times to converge. TODO - This might
        change by letting this function take care of the convergence.
        
        References:
         Rabiner - 1989 - A Tutorial on Hidden Markov Models ...
         Salvucci - 1999 (PhD thesis)
        '''
        
        self._reset_cache()
        self._cache_emission(data)
        
        # Update initial conditions
        #print self.Pi
        new_Pi = copy(self.Pi)
        for i in xrange(self.N):
            
            #print "gamma", i, self._gamma(data, i, 0)
            new_Pi[i] = self._gamma(data, i, 0)
            
        #print "Pi", new_Pi
        
        # Update transition probabilities
        new_M = copy(self.M)
        for i in xrange(self.N):
            den = 0.0
            for t in xrange(len(data)-1):
                den += self._gamma(data, i, t)
            
            for j in xrange(self.N):
                num = 0.0
                
                for t in xrange(len(data)-1):
                    num += self._xi(data, i, j, t)
                    
                new_M[i,j] = num/den
            
        # Update emission probabilities
        new_mu = copy(self.mu)
        if False:
            for j in xrange(self.N):
                num = 0.0
                den = 0.0
                for t in xrange(len(data)):
                    g = self._gamma(data, j, t)
            
                    num += g * self.feature(data, t)
                    den += g
            
                new_mu[j] = num/den

        new_mu[1] = self.mu[1]

        new_sigma = copy(self.sigma)
        if False:
            for j in xrange(self.N):
                num = 0.0
                den = 0.0
                for t in xrange(len(data)):
                    g = self._gamma(data, j, t)
            
                    m = (self.feature(data, t) - self.mu[j])**2
                    num += g * sqrt(m)
                    den += g
            
                new_sigma[j] = sqrt(num/den)

        new_sigma[1] = self.sigma[1]
        
        if 0:
            print "---------------------"

            print "PI"
            print new_Pi
            print "M"
            print new_M
            print "mu"
            print new_mu
            print "sigma"
            print new_sigma
            #print "Change: {0:.4f}".format(change)
        
        self.Pi = new_Pi
        self.M = new_M
        self.mu = new_mu
        self.sigma = new_sigma
        
    def _reset_cache(self):
        # TODO - created a memoization decorator that handles this
        self._alpha_scaled = None
        self._beta_scaled = None
        self._scaling_factors = None
        self._xi_cache = dict()
        self._xi_numerator_cache = dict()
        self._xi_denominator_cache = dict()
        self._gamma_cache = dict()
                
    # Auxilary functions for trainParameters
    def _alpha(self, data, state, index):
        if self._alpha_scaled is None:
            self._calc_alphas(data)
        
        return self._alpha_scaled[index, state]

    def _calc_alphas(self, data):
        self._alpha_scaled = np.zeros((len(data), self.N), float)
        self._scaling_factors = np.zeros(len(data), float)
        
        alpha = self.Pi * self.emission[0]

        self._scaling_factors[0] = 1.0/np.sum(alpha)
        self._alpha_scaled[0] = alpha * self._scaling_factors[0]     
        for t in xrange(1, len(data)):
            alpha = np.dot(self._alpha_scaled[t - 1], self.M.T)
            alpha *= self.emission[t]
            self._scaling_factors[t] = 1/np.sum(alpha)
            self._alpha_scaled[t] = alpha * self._scaling_factors[t]
                        
    def _beta(self, data, state, index):
        if self._beta_scaled is None:
            self._calc_betas(data)
        
        return self._beta_scaled[index, state]

    def _calc_betas(self, data):
        self._beta_scaled = np.zeros((len(data), self.N), float)
        self._beta_scaled[-1] = np.ones(self.N) * self._scaling_factors[-1]
            
        for t in xrange(len(data)-2, -1, -1):
            beta = np.dot(self.emission[t + 1] * self._beta_scaled[t + 1], self.M.T)
            self._beta_scaled[t] = beta * self._scaling_factors[t]
        
    def _xi(self, data, i, j, index):
        if (i, j, index) in self._xi_cache:
            return self._xi_cache[i, j, index]
            
        ret = self._xi_numerator(data, i, j, index)#/self._xi_denominator(data, index)
            
        self._xi_cache[i, j, index] = ret
        return ret
        
    def _xi_numerator(self, data, i, j, index):
        if (i, j, index) in self._xi_numerator_cache:
            return self._xi_numerator_cache[i, j, index]

        ret = self._alpha(data, i, index) * \
            self.transition(i, j) * \
            self.emission[index + 1, j] * \
            self._beta(data, j, index + 1)
            
        self._xi_numerator_cache[i, j, index] = ret
        return ret
        
    def _xi_denominator(self, data, index):
        if index in self._xi_denominator_cache:
            return self._xi_denominator_cache[index]

        ret = 0.0
        for i in xrange(self.N):
            for j in xrange(self.N):
                ret += self._xi_numerator(data, i, j, index)
                
        self._xi_denominator_cache[index] = ret
        return ret
        
    def _gamma(self, data, state, index):
        if (state, index) in self._gamma_cache:
            return self._gamma_cache[state, index]
         
         
        # print "alpha", self._alpha(data, state, index)
        # print "beta", self._beta(data, state, index)
        num = self._alpha(data, state, index) * self._beta(data, state, index)
        #den = 0.0
        #for i in xrange(self.N):
        #   den += self._alpha(data, i, index) * self._beta(data, i, index) 
        
        den = self._scaling_factors[index]
            
        #print num, den
        #print "gamma", num, den
        ret = num/den
    
        self._gamma_cache[state, index] = ret
        return ret
    
    