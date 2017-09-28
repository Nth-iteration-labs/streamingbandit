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
