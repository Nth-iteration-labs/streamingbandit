import numpy as np

id1 = "3ea45886b5" # The exp_id of E-First
id2 = "121e3e0aeb" # The exp_id of E-Greedy

choice = np.random.binomial(1,0.5)

# Run the e-first experiment
if choice == 0:
    exp_nested = Experiment(exp_id = id1)
    self.action = exp_nested.run_action_code(context = {})
    # We feed the experiment number for later use
    self.action["experiment"] = id1
# or, run the e-greedy experiment
else: 
    exp_nested = Experiment(exp_id = id2)
    self.action = exp_nested.run_action_code(context = {})
    self.action["experiment"] = id2