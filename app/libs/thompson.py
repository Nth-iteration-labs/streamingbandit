# Thompson sampling for bernoulli 
# See "old" tools.py
from libs.base import *

class ThompsonList(List):
    """ Class to draw decisions using a Bernoulli Bandit Thompson sampler.

    :variable dict objects: A dict of dict of thetas (which should be proportions)
    :variable list value_names: A list with the possible value names for the
    actions
    """
    def __init__(self, objects, value_names):
        super(ThompsonList, self).__init__(objects, Proportion, value_names)

    # Summary is done with AB setrewards

    def thompson(self):
        
        # MOVE THIS TO LIST INIT
        for val in self.value_names:
            if val not in self.base_list:
                self.base_list[val] = Proportion()
                choice = val
                return val
        # END MOVE

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
        
