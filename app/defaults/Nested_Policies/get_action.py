id1 = "275fc0a66" # The exp_id of E-First
id2 = "18aec502c2" # The exp_id of E-Greedy

choice = np.random.binomial(1,0.5)

# Run the e-first experiment
if choice == 0:
    exp_nested = Experiment(exp_id = id1)
    self.action = exp_nested.run_action_code(context = {})
    # We return the experiment number for later use
    self.action["experiment"] = id1
    # We re-compute the propensity based on the probability of picking
    # the nested experiment
    self.action["propensity"] = self.action["propensity"] * 0.5
# or, run the e-greedy experiment
else: 
    exp_nested = Experiment(exp_id = id2)
    self.action = exp_nested.run_action_code(context = {})
    self.action["experiment"] = id2
    self.action["propensity"] = self.action["propensity"] * 0.5