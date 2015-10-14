import numpy as np
#import json
#from scipy.optimize import minimize_scalar


### Basic data types and updates:
def count(current, update=None, default={'n':0,'_t':"count"}):
    """ A function to update or create data of type count
    
    :param dict current: dict of the current value / count
    :param int / string update: number to add to current count
    :default dict: The default value of the count
    :returns dict: The updated count
    """
    # Initialize a count if the passed objects isn't a proprotion:    
    if current.get('_t', None) != "count":
        current = default.copy()
    # Update the count
    if not update is None:
        current['n'] = int(current['n']) + update
    return(current) 


def proportion(current, update=None, default={'p':.5,'n':2,'_t':"proportion"}):
    # Initialize a proportion if the passed objects isn't a proprotion:    
    if current.get('_t', None) != "proportion":
        current = default.copy()
    # Update the proprotion
    if not update is None:
        current['n'] = int(current['n']) + 1
        current['p'] = float(current['p']) + ( (update - float(current['p'])) / current['n'])
    return(current) 
    

def mean(current, update=None, default={'m':0,'n':0,'_t':"mean"}, value_only=False):
    # Initialize a proportion if the passed objects isn't a proprotion:    
    if current.get('_t', None) != "mean":
        current = default.copy()
    # Update the proprotion
    if not update is None:
        current['n'] = int(current['n']) + 1
        current['m'] = float(current['m']) + ( (update - float(current['m'])) / current['n'])
    if value_only:
        return float(current['m'])
    return current 



# The update function
def update(func, *args):
    """ An update mapping function. Useful for using functions such as count
    and mean.
    
    :param function func: The function to be computed.
    :param args args: The arguments needed for the function.
    :returns * out: Anything that the used functions outputs will be returned.
    """
    out = func(*args)
    return out
  
  
# Agrregate functions:
def sum_count(obj):
    sum = 0
    for key in obj:
        sum =  sum + int(obj[key].get("n",0))
    return sum
 

def max_proportion(obj, k=1, value=True):    
    if len(obj) < k:
        return np.random.randint(1,k+1)
        
    max = 0
    choice = None
    for key in obj:
        if float(obj[key].get("p",0)) > max:
            max = float(obj[key].get("p",0))
            if value:
                choice = key.rpartition(':')[2]
            else:
                choice = key
    return choice


# Thompson sampling bernoulli bandit
def bernbandit_thompson(obj, k=1, value = True):
    if len(obj) < k:
        return np.random.randint(1,k+1)
        
    min = 0
    choice = None
    for key in obj:
        draw = bernbandit_thompson_draw(obj[key])
        if draw > min:
            min = draw
            if value:
                choice = key.rpartition(':')[2]
            else:
                choice = key
    return(choice)
            

def bernbandit_thompson_draw(obj):
    if obj['_t'] == "proportion":
        a = float(obj['p']) * int(obj['n'])
        b = int(obj['n']) - a
        return np.random.beta(a,b)
    else:
        return False        # Should fail gracefully


#
#def reg_log_sgd(x, y, beta, gamma=.1, mu=.01, intercept=False):
#    """ Computes an update for a regularized logistic regression for 
#    k predictors (not specified explicitly)
#    With mu=0 there is no penalty
#    
#    Input arguments:
#    x: Feature vector (vector of length k)
#    y: Observation {0,1} (scalar)
#    beta: current state of model params (vector of length k)
#    gamma: learn rate
#    mu: ridge penalty
#    intercept:If true also penalize the intercept
#    """
#    x = np.matrix(x).T
#    B = np.matrix(beta).T
#    if not len(x)==len(B):
#        print("ERROR")
#    p = 1. / (1. + np.exp(-1*B.T*x))
#    if intercept:
#        B = B + gamma*np.float_(y-p)*x - gamma*2*mu*B
#    else:
#        B = B + gamma*np.float_(y-p)*x - np.insert(gamma*2*mu*B[1:],0,0)
#    return(np.array(B.T)[0,:])
# 
#def bts_update(x, y, params, func, J=100, noisesd=.5):
#    """ Takes a J * k matrix of parameters for a model with k params
#    given a value and an update function updates half of the J values
#    
#    Input arguments:
#    x: Feature vector
#    y: Observation
#    params: Matrix of current parameters (if vector then a J*k matrix will be created)
#    func: Function for update
#    J: size of matrix
#    noisesd: randge of noise when initializing
#    
#    Return values:
#    An J*k matrix containing the updated values
#    """
#    if not params.shape[0]==J:
#        params = bts_init(params, J, noisesd)        
#    
#    i=0
#    for row in params:
#        if np.random.binomial(1,.5,1) == 1:
#            params[i,:] = func(x, y, params[i,:])
#        i+=1
#    
#    return(params)    
#    
#def bts_init(params, J, noisesd):
#    """ Initializes a bts J*k matrix
#    Utility function for bts_update
#    """
#    betas = np.zeros([J, len(params)])
#    i = 0
#    for x in params:
#        vals = np.random.normal(x, noisesd, J)
#        betas[:,i] = vals
#        i+=1
#    return(np.matrix(betas))
#   
#def bts_select(context, params, xmin, xmax, func):
#    """ Select a single strategy and arg max it.
#    
#    Input arguments:
#    context: vector of the context
#    params: current parameters of the model
#    xmin: smalles value to search
#    xmax: largest value to search
#    func: function for multiplying context with continuous value of x
#    
#    Response:
#    A float which is the action to take
#    """
#    select = np.random.choice(params.shape[0])
#    beta = params[select,:]
#    
#    ### SHIT, THIS MAXIMIZES THE PROBABILITY, NOT THE PRICE...
#    #res = minimize_scalar(lambda x: -1*(func(x, context)*beta.T), bounds=(xmin,xmax), method="bounded")  
#    res = minimize_scalar(lambda x: -1.*x*(1./(1.+np.exp(-1*(func(x, context)*beta.T)))), bounds=(xmin,xmax), method="bounded")
#    return(res.x)
#    
#def to_factor(x, levels):
#    """ Converts a specific level of a factor to a array of dummys
#    Takes the first category as reference (0,0...) by default
#    
#    Input arguments:
#    x: The actual level of the current feature
#    levels: The array of possible levels
#    
#    Returns
#    An array with possibly a 1
#    """
#    zeros = np.zeros(len(levels)-1, dtype=np.int)
#    if not levels.index(x)==0:
#        zeros[levels.index(x)-1]=1
#    return zeros 
#
#def to_string(mat):
#    arr = np.array(mat.flatten())
#    ls = arr.tolist()
#    return ','.join(map(str, ls))
#    
#    
#def to_mat(obj, key, rows):
#    string = obj[key]
#    string = string[1:-1]
#    arr = np.asarray(string.split(','), dtype=float)
#    size = arr.size
#    return np.matrix(arr.reshape(rows, arr.size/rows))
