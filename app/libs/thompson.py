# Thompson sampling for bernoulli 
# See "old" tools.py
from libs.base import *

class BBThompsonList(List):
    """ Class to draw decisions using a Bernoulli Bandit Thompson sampler.

    :var dict objects: A dict of dict of thetas (which should be \
    proportions, see documentation of Proportions on how it should look like.)
    :var list value_names: A list with the possible value names for the \
    actions
    """
    def __init__(self, objects, value_names):
        """ Create an instance of a BB Thompson Sampler.
        """
        super(BBThompsonList, self).__init__(objects, Proportion, value_names)

    # Summary is done with AB setrewards

    def thompson(self):
        """ Draw decision using the Bernoulli Bandit Thompson sampler.

        :returns string choice: The choice of action that's made.
        """
        min_prob = 0
        choice = None
        for key, obj in self.base_list.items():
            theta = obj.get_dict()
            a = float(theta['p']) * int(theta['n'])
            b = int(theta['n']) - a
            draw = np.random.beta(a,b)
            if draw > min_prob:
                min_prob = draw
                # We want to return something of the form of an action choice.
                # Do we return 
                choice = key
        return choice

    def propensity(self, value, n = 1000):
        """ Calculate propensity of given arm using n draws.
        
        :returns int propensity: The propensity of the arm.
        """
        index = self.value_names.index(value)
        
        stacked_draws = np.zeros((self.num_values, n))
        for i in self.value_names:
            theta = self.base_list[i].get_dict()
            a = float(theta['p']) * int(theta['n'])
            b = int(theta['n']) - a
            draws = np.random.beta(a,b,n)
            stacked_draws[self.value_names.index(i),:] = draws
        maxes = np.argmax(stacked_draws, axis = 0)
        propensity = sum(maxes == index) / n
        return propensity 

class ThompsonVarList(List):
    """ Class to allocate observations in 2 group a within subjects desing
    such as to maximize the precision of the estimated effect size 
    (assuming unequal variance of the two groups)
    """
    
    def __init__(self, objects, value_names):
        """ Create instance of a BB Thompson Variance Sampler
        by creating a variance list
        """
        super(ThompsonVarList, self).__init__(objects, Variance, value_names)


    def experimentThompson(self):
        """ Obtain draw and allocate to minimize estimation precision
        """
        max_criterion = 0
        choice = None
        for key, obj in self.base_list.items():

            # Get the objects
            theta = obj.get_dict()

            # Get sum of squares and N
            SS = float(theta['s'])            
            n = int(theta['n']) 
            if n < 2:
                choice = key
                break
            
            # Computer criterion based on posterior variance
            criterion = self._postVariance(SS,n) / n
            
            # Return condition with hightest criterion
            if criterion > max_criterion:
                max_criterion = criterion
                choice = key
        return choice
  
      
    def _postVariance(self, SS, n):
        """ Obtain a sample from the posterior variance given 
        the sum of squares (SS) and the sample size n
        """ 
        s2 = SS / np.random.chisquare(n-1)
        return(np.sqrt(s2))
    
    
    def _postMean(self, m, SS, n):
        """ Obtain a sample from the posterior mean of a normal normal
        model (CURRNTLY NOT USED)
        """
        s2 = self._postVariance(SS, n)
        mean = np.random.normal(m, (np.sqrt(s2)/ np.sqrt(n)))
        return(mean)
