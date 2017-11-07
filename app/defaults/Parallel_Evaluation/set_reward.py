# Create a list of experiments / policies to evaluate
policies = ["18aec502c2", # E-Greedy
            "275fc0a66"] # E-First

# For each experiment
for exp_id in policies:

    # Initialize the experiment:
    exp_nested = Experiment(exp_id)
    
    # Compute the suggested action:
    suggestion = exp_nested.run_action_code(context = {})
    
    # See if the suggested action matches the actual action:
    if suggestion["treatment"] == self.action["treatment"]:
        
        # And if so store the performance of the policy:
        mean = base.Mean(self.get_theta(key = "policy_means", value = exp_id))
        mean.update(self.reward["value"])
        self.set_theta(mean, key = "policy_means", value = exp_id)
        
        # And finally update the policy:
        exp_nested.run_reward_code(context = {}, action = self.action, reward = self.reward)