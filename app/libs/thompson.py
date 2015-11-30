# Thompson sampling for bernoulli 
# See "old" tools.py
from libs.base import *

class BBThompsonList(List):
    """ Class to draw decisions using a Bernoulli Bandit Thompson sampler.
    """
    def __init__(self, objects, value_names):
        """ Create an instance of a BB Thompson Sampler.

        :param dict objects: A dict of dict of thetas (which should be
        proportions, see documentation of Proportions on how it should look like.)
        :param list value_names: A list with the possible value names for the
        actions
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
        
