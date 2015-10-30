# Thompson sampling for bernoulli 
# See "old" tools.py
from libs.base import *

class BernoulliBanditThompson(object):
    """ Class to draw decisions using a Bernoulli Bandit Thompson sampler.

    :variable dict thetas: A dict of dict of thetas (which should be proportions
    """
    def __init__(self, thetas):
        self.theta_list = list_of_base(thetas, Proportion) 

    # Summary is done with AB setrewards

    def decision(self):
        min = 0
        choice = None
        for key, obj in self.theta_list.items():
            theta = obj.get_dict()
            a = float(theta['p']) * int(theta['n'])
            b = int(theta['n']) - a
            draw = np.random.beta(a,b)
            if draw > min:
                min = draw
                # We want to return something of the form of an action choice.
                # Do we return 
                choice = key
        return choice
        
