# Implementation of Lock in Feedback.
import random as rand
import math as math


##### WARNING: TOTALLY UNTESTED AND UNSURE WHETHER THIS WORKS
##### AND, LITTERED WITH SYNTAX ERRORS ;)

class Lif():
    
    def __init__(self, values, x0=0, inttime = 20, amplitude = 1, learnrate = .1, omega=.5):
         """ Initialize a new Lock in Feedback process for scalar optimizaiton 
         of an unknown function y = f(x). Lif sequentially finds xmax = arg max x f(x)

        :param dict values: 
        :param ....
        
        :returns: ....
        """
        self.values = values   # Make a 3 (t,x,y) * inttime (1:intime) matrix of the values (dict)
        self.x0 = x0
        self.inttime =inttime
        self.amplitude = amplitude
        self.learnrate = learnrate
        self.omega=omega
        
        
    def suggest(self):
        
        # If the integration time is exceeded:
        if dim(self.values)[1] > self.inttime:
            # determine x0 as mean of stream: the mean of the x's in the integration time
            self.x0 = mean(self.values[,2])
            # move according to LiF: (see also R code)
            self.x0 = self.x0 + self.learnrate * sum ( math.cos(self.omega * self.values[,1])*self.values[,3])
        
        # Increment t
        t = incremental t based on values.   
        self.x0 + self.amplitude * math.cos(self.omega * t)
        # Should return an X and a T!!!
    
    
    def update(self, t,x,y):
        self.values push/pop (t,x,y)     # just add to the value matrix
   
     
    def get_dict(self):
        return # dict of values for storage in Redis
        