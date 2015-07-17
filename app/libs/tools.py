import numpy as np
import json
from scipy.optimize import minimize_scalar


def update(func, args):
    out = func(*args)
    return out
    
def count(theta, r):
    theta['N'] = theta['N'] + r
    return theta
    
def mean(theta, r):
    theta['M'] = (theta['M'] + r) / theta['N']
    return theta
    
def tryout():
    return "TOOLS!"

def reg_log_sgd(x, y, beta, gamma=.1, mu=.01, intercept=False):
    """ Computes an update for a regularized logistic regression for 
    k predictors (not specified explicitly)
    With mu=0 there is no penalty
    
    Input arguments:
    x: Feature vector (vector of length k)
    y: Observation {0,1} (scalar)
    beta: current state of model params (vector of length k)
    gamma: learn rate
    mu: ridge penalty
    intercept:If true also penalize the intercept
    """
    x = np.matrix(x).T
    B = np.matrix(beta).T
    if not len(x)==len(B):
        print("ERROR")
    p = 1. / (1. + np.exp(-1*B.T*x))
    if intercept:
        B = B + gamma*np.float_(y-p)*x - gamma*2*mu*B
    else:
        B = B + gamma*np.float_(y-p)*x - np.insert(gamma*2*mu*B[1:],0,0)
    return(np.array(B.T)[0,:])
 
def bts_update(x, y, params, func, J=100, noisesd=.5):
    """ Takes a J * k matrix of parameters for a model with k params
    given a value and an update function updates half of the J values
    
    Input arguments:
    x: Feature vector
    y: Observation
    params: Matrix of current parameters (if vector then a J*k matrix will be created)
    func: Function for update
    J: size of matrix
    noisesd: randge of noise when initializing
    
    Return values:
    An J*k matrix containing the updated values
    """
    if not params.shape[0]==J:
        params = bts_init(params, J, noisesd)        
    
    i=0
    for row in params:
        if np.random.binomial(1,.5,1) == 1:
            params[i,:] = func(x, y, params[i,:])
        i+=1
    
    return(params)    
    
def bts_init(params, J, noisesd):
    """ Initializes a bts J*k matrix
    Utility function for bts_update
    """
    betas = np.zeros([J, len(params)])
    i = 0
    for x in params:
        vals = np.random.normal(x, noisesd, J)
        betas[:,i] = vals
        i+=1
    return(np.matrix(betas))
   
def bts_select(context, params, xmin, xmax, func):
    """ Select a single strategy and arg max it.
    
    Input arguments:
    context: vector of the context
    params: current parameters of the model
    xmin: smalles value to search
    xmax: largest value to search
    func: function for multiplying context with continuous value of x
    
    Response:
    A float which is the action to take
    """
    select = np.random.choice(params.shape[0])
    beta = params[select,:]
    
    ### SHIT, THIS MAXIMIZES THE PROBABILITY, NOT THE PRICE...
    #res = minimize_scalar(lambda x: -1*(func(x, context)*beta.T), bounds=(xmin,xmax), method="bounded")  
    res = minimize_scalar(lambda x: -1.*x*(1./(1.+np.exp(-1*(func(x, context)*beta.T)))), bounds=(xmin,xmax), method="bounded")
    return(res.x)
    
def to_factor(x, levels):
    """ Converts a specific level of a factor to a array of dummys
    Takes the first category as reference (0,0...) by default
    
    Input arguments:
    x: The actual level of the current feature
    levels: The array of possible levels
    
    Returns
    An array with possibly a 1
    """
    zeros = np.zeros(len(levels)-1, dtype=np.int)
    if not levels.index(x)==0:
        zeros[levels.index(x)-1]=1
    return zeros 

def to_string(mat):
    arr = np.array(mat.flatten())
    ls = arr.tolist()
    return ','.join(map(str, ls))
    
    
def to_mat(obj, key, rows):
    string = obj[key]
    string = string[1:-1]
    arr = np.asarray(string.split(','), dtype=float)
    size = arr.size
    return np.matrix(arr.reshape(rows, arr.size/rows))