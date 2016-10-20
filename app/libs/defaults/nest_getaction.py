# Let's assume that we want to run an A/B test on two different experiments
# Where we have experiments with id=1 and id=2
# Using the exp_nested.run_action_code() function we can run either of two experiments
import numpy as np

# First let us randomly decide which action to pick
choice = np.random.binomial(1,0.5)
# Then run the experiment
if choice == 0:
    exp_nested = Experiment(exp_id = 1)
    self.action = exp_nested.run_action_code(context = {})
    # We feed the experiment number for later use
    self.action["Experiment"] = 1
else: # thus if choice is 1
    exp_nested = Experiment(exp_id = 2)
    self.action = exp_nested.run_action_code(context = {})
    self.action["Experiment"] = 2
