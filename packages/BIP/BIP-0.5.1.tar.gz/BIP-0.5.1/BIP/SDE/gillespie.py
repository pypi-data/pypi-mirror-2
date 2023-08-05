# -*- coding:utf-8 -*-
#-----------------------------------------------------------------------------
# Name:        gillespie.py
# Project:  Bayesian-Inference
# Purpose:     
#
# Author:      Flávio Codeço Coelho<fccoelho@gmail.com>
#
# Created:     2008-11-26
# Copyright:   (c) 2008 by the Author
# Licence:     GPL
#-----------------------------------------------------------------------------
__docformat__ = "restructuredtext en"
from numpy.random import uniform, multinomial, exponential,random
from numpy import arange, array, empty,zeros,log, isnan, nanmax, nan_to_num
import time
import xmlrpclib
import pdb
import copy
from multiprocessing import Pool
try:
    from liveplots import xmlrpcserver as xmlrpc
    port = xmlrpc.rpc_plot(persist=0)
    server = xmlrpclib.ServerProxy('http://localhost:%s'%port, allow_none=True)
    viz = True
except:
    print "faio"
    viz = False
try:
    import psyco
    psyco.full()
except:
    pass
def dispatch(model):
    '''this function is necessary for paralelization'''
    model.server = server
    return model.GSSA()

class Model:
    def __init__(self,vnames,rates,inits, tmat,propensity):
        '''
        Class representing a Stochastic Differential equation.
        
        :Parameters:
            - `vnames`: list of strings
            - `rates`: list of fixed rate parameters
            - `inits`: list of initial values of variables. Must be integers
            - `tmat`: Transition matrix; numpy array with shape=(len(inits),len(propensity))
            - `propensity`: list of lambda functions of the form: lambda r,ini: some function of rates ans inits.
        '''
        #check types
        for i in inits:
            if not isinstance(i, int):
                i = int(i)
        for i in tmat.ravel():
            assert isinstance(i, int)
        self.vn = vnames
        self.rates = tuple(rates)
        self.inits = tuple(inits)
        self.tm = tmat
        self.pv = propensity#[compile(eq,'errmsg','eval') for eq in propensity]
        self.pvl = len(self.pv) #length of propensity vector
        self.pv0 = zeros(self.pvl,dtype=float)
        self.nvars = len(self.inits) #number of variables
        self.evseries = {} #dictionary with complete time-series for each event type.
        self.time = None
        self.tmax = None
        self.series = None
        self.steps = 0
        self.viz = False #if intermediate vizualization should be on
        
    
    def getStats(self):
        return self.time,self.series,self.steps, self.evseries
    
    def run(self, method='SSA', tmax=10, reps=1, viz=False, serial=False):
        '''
        Runs the model.
        
        :Parameters:
            - `method`: String specifying the solving algorithm. Currently only 'SSA'
            - `tmax`: duration of the simulation.
            - `reps`: Number of replicates.
            - `viz`: Boolean. Whether to show graph of each replicate during simulation
            - `serial`: Boolean. False to run replicate in parallel when more than one core is a vailable. True to run them serially (easier to debug).

        :Return:
            a numpy array of shape (reps,tmax,nvars)
        '''
        if viz: #only if Gnuplot.py is installed
            self.viz = viz
        self.tmax = tmax
        #self.res = zeros((tmax,self.nvars,reps),dtype=float)
        self.res = zeros((tmax,self.nvars),dtype=float)
        tvec = arange(tmax, dtype=int)
            
        if method =='SSA':
            if not serial:# Parallel version
                pool = Pool()
                res = pool.map(dispatch,[self]*reps, chunksize=10)
                self.res = array([i[0] for i in res])
                if reps == 0:
                    self.evseries = res[0][1]
                else:
                    self.evseries = [i[1] for i in res]
                pool.close()
                pool.join()
            else:# Serial
                res = map(dispatch,[self]*reps)
                self.res = array([i[0] for i in res])
                if reps == 0:
                    self.evseries = res[0][1]
                else:
                    self.evseries = [i[1] for i in res]
            
        elif method == 'SSAct':
            pass
        
        self.time = tvec
        self.series = self.res
        #self.steps=steps
    
    def GSSA(self):
        '''
        Gillespie Direct algorithm
        '''
        tmax = self.tmax
        ini = array(self.inits)
        #ini = copy.deepcopy(self.inits)
        r = array(self.rates)
        for i in r:
            if i<0:
                i=0
        pvi = self.pv #propensity functions
        tm = self.tm
        pv = self.pv0 #actual propensity values for each time step
        tc = 0
        evts = dict([(i, []) for i in xrange(len(self.pv))])
        self.steps = 0
        self.res[0,:]= ini
        for tim in xrange(1,tmax):
            while tc < tim:
                i=0
                a0=0.0
                for p in pvi:
                    pv[i] = p(r,ini)
                    a0+=pv[i]
                    i+=1
                tau = (-1/a0)*log(random())
                if pv.any():#no change in state is pv is all zeros
                    #~ try:
                    event = multinomial(1,pv/a0) # event which will happen on this iteration
                    #~ except ValueError:# as inst:#2.6 syntax
                        #~ #print inst
                        #~ print "pv: ",pv
                        #~ print "Rates: ", r
                        #~ print "State: ", ini
                        #~ print "Time Step: ",tim
                        #~ pdb.set_trace()
                        #~ #raise ValueError()
                    ini += tm[:,event.nonzero()[0][0]]
                    evts[event.nonzero()[0][0]].append(tc+tau)
                #print tc, ini
                tc += tau
                self.steps +=1
                if a0 == 0: break
            self.res[tim,:] = nan_to_num(ini)
            #self.evseries = evts
#            if a0 == 0: break
        if self.viz:
            #self.ser.clearFig()
            self.server.lines(self.res.T.tolist(),[],self.vn,"Single replica")
        return self.res,  evts


def p1(r,ini): return r[0]*ini[0]*ini[1]
def p2(r,ini): return r[1]*ini[1]

def main():
    vnames = ['S','I','R']
    ini= [500,1,0]
    rates = [.001,.1]
    tm = array([[-1,0],[1,-1],[0,1]])
    #prop=[lambda r, ini:r[0]*ini[0]*ini[1],lambda r,ini:r[0]*ini[1]]
    M = Model(vnames = vnames,rates = rates,inits=ini, tmat=tm,propensity=[p1,p2])
    t0=time.time()
    M.run(tmax=80,reps=100,viz=1,serial=1)
    print 'total time: ',time.time()-t0
    t,series,steps, evts = M.getStats()
    ser = series.mean(axis=0)
    #print len(evts), len(evts[0])
    from pylab import plot , show, legend
    plot(t,ser,'-.')
    legend(M.vn,loc=0)
    show()
    

if __name__=="__main__":
    #import cProfile
    #cProfile.run('main()',sort=1,filename='gillespie.profile')
    main()
