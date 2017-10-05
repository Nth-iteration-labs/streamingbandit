# Let's assume that we want to run an A/B test on two different experiments
# Where we have experiments with id1 (E-First) and id2 (E-Greedy)
# Using the exp_nested.run_action_code() function we can run either of two experiments
import numpy as np

id1 = 1 # Set the exp_id of E-First
id2 = 2 # Set the exp_id of E-Greedy

# First let us randomly decide which action to pick
choice = np.random.binomial(1,0.5)
# Then run the experiment
if choice == 0:
    exp_nested = Experiment(exp_id = id1)
    self.action = exp_nested.run_action_code(context = {})
    # We feed the experiment number for later use
    self.action["experiment"] = id1
    # We control the propensity for playing two experiments
    self.action["propensity"] = self.action["propensity"] * 0.5
else: 
    exp_nested = Experiment(exp_id = id2)
    self.action = exp_nested.run_action_code(context = {})
    self.action["experiment"] = id2
    self.action["propensity"] = self.action["propensity"] * 0.5
